"""Sprint 08 real application-role persistence, recovery and subscription boundaries."""

import hashlib
import hmac
import json
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api.identity import context, now
from ppm_api.ingestion import ConnectorConfig, ImportInput, fetch_page, normalize, rows
from ppm_api.job_tables import events, jobs, outbox, sources
from ppm_api.jobs import run_job
from ppm_api.ppm_tables import TABLES
from test_delivery import change, create, setup
from test_identity import identity as identity
from test_identity import login, send


@pytest.mark.integration
async def test_overlapping_mapping_rejected_before_connection_is_persisted(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    before = (await c.get("/api/v1/integrations")).json()
    for external, name in [("id", "id.title"), ("id.title", "id")]:
        result = await send(
            c,
            "POST",
            "/integrations",
            headers={"idempotency-key": str(uuid4())},
            json=dict(
                name="Invalid overlapping mapping",
                provider="csv",
                project_id=project["id"],
                mapping={
                    "external_id": external,
                    "name": name,
                    "source_updated_at": "updated_at",
                },
            ),
        )
        assert result.status_code == 422, result.text
    assert (await c.get("/api/v1/integrations")).json() == before


@pytest.mark.integration
async def test_public_signed_github_delivery_and_revoked_authority(identity, monkeypatch):
    import httpx
    from ppm_api.identity_tables import sessions

    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    webhook_ref = f"PPM_CONNECTOR_{ids['a'].hex.upper()}_GITHUB_WEBHOOK"
    monkeypatch.setenv(webhook_ref, "fixture-secret")
    integration = await connection(
        c,
        project,
        provider="github",
        resource="example/repo",
        webhook_secret_ref=webhook_ref,
        mapping={
            "external_id": "number",
            "name": "title",
            "status": "state",
            "source_updated_at": "updated_at",
        },
        status_map={"open": "backlog"},
    )
    payload = {
        "repository": {"full_name": "example/repo"},
        "issue": {
            "number": 7,
            "title": "Signed issue",
            "state": "open",
            "updated_at": "2026-10-09T00:00:00Z",
            "body": "Private incidental notes never retained",
        },
    }

    def signed(value, delivery_id="external-delivery"):
        raw = json.dumps(value).encode()
        return dict(
            content=raw,
            headers={
                "content-type": "application/json",
                "x-github-event": "issues",
                "x-github-delivery": delivery_id,
                "x-hub-signature-256": "sha256="
                + hmac.new(b"fixture-secret", raw, hashlib.sha256).hexdigest(),
            },
        )

    path = f"/api/v1/integrations/hooks/github/{integration['id']}"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://testserver"
    ) as external:
        assert (await external.post(path, json=payload)).status_code == 403
        accepted = await external.post(path, **signed(payload))
        assert accepted.status_code == 202, accepted.text
        replay = await external.post(path, **signed(payload))
        assert replay.json()["id"] == accepted.json()["id"]
        changed = payload | {"issue": payload["issue"] | {"title": "Changed signed payload"}}
        assert (await external.post(path, **signed(changed))).status_code == 409
        assert (
            await external.post(
                path, **signed(payload | {"repository": {"full_name": "other/repo"}}, "foreign")
            )
        ).status_code == 422
        await execute(app, accepted, ids)
        async with owner.begin() as conn:
            row = (
                (
                    await conn.execute(
                        sa.select(jobs).where(jobs.c.id == UUID(accepted.json()["id"]))
                    )
                )
                .mappings()
                .one()
            )
            assert "Private incidental notes" not in json.dumps(row["input"])
            await conn.execute(
                sessions.update().where(sessions.c.id == row["session_id"]).values(revoked=True)
            )
        assert (await external.post(path, **signed(payload, "revoked"))).status_code == 403


@pytest.mark.integration
async def test_retry_backoff_partial_page_recovery_and_dead_letter(identity, monkeypatch):
    from ppm_api.ingestion import Retryable

    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    integration = await connection(
        c,
        project,
        provider="github",
        resource="example/repo",
        mode="live",
        secret_ref=f"PPM_CONNECTOR_{ids['a'].hex.upper()}_GITHUB_TOKEN",
    )
    calls = []
    failed = False

    async def remote(config, cursor, page, token):
        nonlocal failed
        calls.append((cursor, page, token))
        if page == 2 and not failed:
            failed = True
            raise Retryable(120)
        return [
            dict(
                id=str(page),
                name=f"Page {page} work",
                updated_at=f"2026-10-0{page + 6}T00:00:00Z",
                status="backlog",
            )
        ], "2" if page == 1 else None

    monkeypatch.setattr("ppm_api.jobs.remote_page", remote)
    first = await submit(c, integration)
    await execute(app, first, ids)
    row = (await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}")).json()
    assert row["status"] == "retry_wait" and row["accepted"] == 1
    async with owner.begin() as conn:
        stored = (
            (await conn.execute(sa.select(jobs).where(jobs.c.id == UUID(first.json()["id"]))))
            .mappings()
            .one()
        )
        assert stored["available_at"] > now() + timedelta(seconds=100)
        await conn.execute(
            jobs.update()
            .where(jobs.c.id == stored["id"])
            .values(available_at=now() - timedelta(seconds=1))
        )
    await execute(app, first, ids)
    row = (await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}")).json()
    assert row["status"] == "succeeded" and row["accepted"] == 2 and row["attempt"] == 2
    assert calls == [(None, 1, None), (None, 2, "2"), (None, 2, "2")]
    assert (await c.get("/api/v1/integrations")).json()[0]["cursor"] == "2026-10-08T00:00:00+00:00"
    exhausted = await submit(c, integration)
    async with owner.begin() as conn:
        await conn.execute(
            jobs.update().where(jobs.c.id == UUID(exhausted.json()["id"])).values(attempt=5)
        )
    await execute(app, exhausted, ids)
    row = (await c.get(f"/api/v1/integrations/activity/jobs/{exhausted.json()['id']}")).json()
    assert row["status"] == "failed" and row["errors"][0]["code"] == "ATTEMPTS_EXHAUSTED"


@pytest.mark.integration
@pytest.mark.parametrize("global_disable", [False, True])
async def test_revoked_worker_and_progress_retention(identity, global_disable):
    from ppm_api.identity_tables import memberships, users

    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    integration = await connection(c, project)
    oversized = await send(
        c, "POST", f"/integrations/{integration['id']}/sync", content=b"x" * 650001
    )
    assert oversized.status_code == 413 and oversized.json()["error"]["code"] == "INPUT_LIMIT"
    first = await submit(c, integration, CSV)
    await execute(app, first, ids)
    async with owner.begin() as conn:
        await conn.execute(
            events.update()
            .where(events.c.job_id == UUID(first.json()["id"]))
            .values(occurred_at=now() - timedelta(hours=25))
        )
    result = await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}/events")
    assert result.status_code == 200 and "resync_required" in result.text
    queued = await submit(c, integration, CSV + "\n4,Revoked work,2026-10-09T00:00:00Z,backlog")
    async with owner.begin() as conn:
        if global_disable:
            await conn.execute(
                users.update().where(users.c.id == ids["admin"]).values(active=False)
            )
        else:
            await conn.execute(
                memberships.update()
                .where(
                    memberships.c.organization_id == ids["a"], memberships.c.user_id == ids["admin"]
                )
                .values(active=False)
            )
    assert (
        await c.get(f"/api/v1/integrations/activity/jobs/{queued.json()['id']}/events")
    ).status_code == (401 if global_disable else 403)
    await execute(app, queued, ids)
    async with owner.connect() as conn:
        row = (
            (await conn.execute(sa.select(jobs).where(jobs.c.id == UUID(queued.json()["id"]))))
            .mappings()
            .one()
        )
        assert row["status"] == "cancelled" and row["errors"][0]["code"] == "AUTHORITY_REVOKED"
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(sources)
                .where(sources.c.integration_id == UUID(integration["id"]))
            )
            == 2
        )


@pytest.mark.integration
async def test_actual_celery_process_crash_and_lease_recovery(identity, tmp_path):
    import asyncio
    import os
    import signal
    import subprocess
    import sys
    from time import monotonic

    from ppm_worker.app import celery_app

    if os.name != "posix":
        pytest.skip("Actual Celery process lifecycle runs in the Linux test container")
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    integration = await connection(c, project)
    text = "id,name,updated_at,status\n" + "\n".join(
        f"{i},Crash recovery work {i},2026-10-09T00:00:00Z,backlog" for i in range(500)
    )
    result = await submit(c, integration, text)
    assert result.status_code == 202, result.text
    id_ = UUID(result.json()["id"])
    queue = "sprint08-crash-" + str(uuid4())
    arguments = [str(id_), str(ids["a"]), str(ids["admin"])]
    with (tmp_path / "worker.log").open("w") as log:

        def start():
            return subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "celery",
                    "-A",
                    "ppm_worker.app:celery_app",
                    "worker",
                    "--pool=solo",
                    "--loglevel=WARNING",
                    "-Q",
                    queue,
                    "--without-mingle",
                    "--without-gossip",
                    "--without-heartbeat",
                ],
                stdout=log,
                stderr=log,
                start_new_session=True,
            )

        process = start()
        started = monotonic()
        try:
            celery_app.send_task("pipeline.run", args=arguments, queue=queue)
            position = 0
            # Startup and 500 database effects vary with concurrent Compose/AV load.
            # These are bounded harness waits, not a product latency/SLA assertion.
            for _ in range(1500):
                async with owner.connect() as conn:
                    position = await conn.scalar(sa.select(jobs.c.position).where(jobs.c.id == id_))
                if position > 0:
                    break
                await asyncio.sleep(0.02)
            assert 0 < position < 500
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
            async with owner.connect() as conn:
                crashed = (
                    (await conn.execute(sa.select(jobs).where(jobs.c.id == id_))).mappings().one()
                )
            assert crashed["status"] == "running" and 0 < crashed["position"] < 500
            process = start()
            # Actual 45-second lease expiry; no owner edit or test-only worker branch.
            for iteration in range(180):
                if iteration % 2 == 0:
                    celery_app.send_task("pipeline.run", args=arguments, queue=queue)
                async with owner.connect() as conn:
                    state = (
                        (await conn.execute(sa.select(jobs).where(jobs.c.id == id_)))
                        .mappings()
                        .one()
                    )
                if state["status"] == "succeeded":
                    break
                await asyncio.sleep(1)
            assert state["status"] == "succeeded" and state["attempt"] == 2
            async with owner.connect() as conn:
                count = await conn.scalar(
                    sa.select(sa.func.count())
                    .select_from(sources)
                    .where(sources.c.integration_id == UUID(integration["id"]))
                )
                effects = await conn.scalar(
                    sa.select(sa.func.count())
                    .select_from(TABLES["work_items"])
                    .where(TABLES["work_items"].c.project_id == UUID(project["id"]))
                )
            assert count == effects == 500
            print(
                f"REAL_WORKER_CRASH position={crashed['position']} "
                f"restart_attempts=2 unique_effects=500 elapsed_seconds={monotonic() - started:.2f}"
            )
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)


def config(**kw):
    return ConnectorConfig(name="CSV fixture", provider="csv", project_id=uuid4(), **kw)


def test_adapter_validation_and_network_allowlist():
    c = config()
    with pytest.raises(ValueError):
        rows(c, ImportInput(csv_text="id,id\nx,x"))
    with pytest.raises(ValueError):
        rows(c, ImportInput(csv_text="id,name\nx"))
    with pytest.raises(ValueError):
        rows(c, ImportInput(csv_text="id\n" + "x\n" * 501))
    for host in ["localhost", "127.0.0.1", "https://tenant.atlassian.net", "evil.com"]:
        with pytest.raises(ValueError):
            ConnectorConfig(name="Bad host", provider="jira", resource=host, project_id=uuid4())
    with pytest.raises(ValueError):
        config(mapping={"organization_id": "org"})
    with pytest.raises(ValueError):
        normalize(c, dict(id="one", name="Issue", updated_at="2026-10-09"))
    with pytest.raises(ValueError):
        fetch_page(
            ConnectorConfig(
                name="GitHub",
                provider="github",
                resource="owner/repo",
                project_id=uuid4(),
                mode="live",
                secret_ref="PPM_CONNECTOR_MISSING",
            ),
            None,
            1,
        )


async def connection(c, project, **kw):
    result = await send(
        c,
        "POST",
        "/integrations",
        headers={"idempotency-key": str(uuid4())},
        json=dict(name="CSV contract fixture", provider="csv", project_id=project["id"]) | kw,
    )
    assert result.status_code == 201, result.text
    return result.json()


async def submit(c, integration, text=None, key=None, **kw):
    return await send(
        c,
        "POST",
        f"/integrations/{integration['id']}/sync",
        headers={"idempotency-key": key or str(uuid4())},
        json=({"csv_text": text} if text is not None else kw),
    )


async def execute(app, result, ids, **kw):
    assert result.status_code == 202, result.text
    await run_job(app.state.engine, UUID(result.json()["id"]), ids["a"], ids["admin"], **kw)


CSV = (
    "id,name,updated_at,status\n"
    "1,Imported work,2026-10-09T00:00:00Z,backlog\n"
    "2,Second work,2026-10-09T00:00:00Z,ready"
)


@pytest.mark.integration
async def test_import_atomic_replay_partial_recovery_revision_conflict_and_sse(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    integration = await connection(c, project)
    preview = await send(
        c, "POST", f"/integrations/{integration['id']}/preview", json={"csv_text": CSV}
    )
    assert preview.status_code == 200 and preview.json()["valid"] == 2
    key = str(uuid4())
    first = await submit(c, integration, CSV, key)
    same = await submit(c, integration, CSV, key)
    assert first.json()["id"] == same.json()["id"]
    await run_job(app.state.engine, UUID(first.json()["id"]), ids["b"], ids["other"])
    assert (await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}")).json()[
        "status"
    ] == "queued"
    assert (
        await submit(c, integration, CSV + "\n3,Other,2026-10-09T00:00:00Z,backlog", key)
    ).status_code == 409
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(outbox)
                .where(outbox.c.job_id == UUID(first.json()["id"]))
            )
            == 1
        )
    await execute(app, first, ids, stop_after=1)
    async with owner.begin() as conn:
        row = (
            (await conn.execute(sa.select(jobs).where(jobs.c.id == UUID(first.json()["id"]))))
            .mappings()
            .one()
        )
        assert row["position"] == 1 and row["status"] == "running"
        await conn.execute(
            jobs.update()
            .where(jobs.c.id == row["id"])
            .values(lease_until=now() - timedelta(seconds=1))
        )
    await execute(app, first, ids)
    snapshot = await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}")
    assert snapshot.json()["status"] == "succeeded" and snapshot.json()["attempt"] == 2
    stream = await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}/events")
    assert (
        stream.status_code == 200 and "event: stage" in stream.text and "completed" in stream.text
    )
    resumed = await c.get(
        f"/api/v1/integrations/activity/jobs/{first.json()['id']}/events",
        headers={"last-event-id": "2"},
    )
    assert "id: 1\n" not in resumed.text and "id: 2\n" not in resumed.text
    expired = await c.get(
        f"/api/v1/integrations/activity/jobs/{first.json()['id']}/events",
        headers={"last-event-id": "999"},
    )
    assert "resync_required" in expired.text
    repeat = await submit(c, integration, CSV)
    await execute(app, repeat, ids)
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(sources)
                .where(sources.c.integration_id == UUID(integration["id"]))
            )
            == 2
        )
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(TABLES["work_items"])
                .where(TABLES["work_items"].c.project_id == UUID(project["id"]))
            )
            == 2
        )
    broken = await submit(c, integration, CSV + "\n3,Bad work,2026-10-09T00:00:00Z,unknown")
    await execute(app, broken, ids)
    partial = (await c.get(f"/api/v1/integrations/activity/jobs/{broken.json()['id']}")).json()
    assert (
        partial["status"] == "partially_succeeded"
        and partial["errors"][0]["code"] == "INVALID_SOURCE_ROW"
    )
    repaired = await submit(c, integration, CSV + "\n3,Repaired work,2026-10-09T00:00:00Z,backlog")
    await execute(app, repaired, ids)
    records = (await c.get("/api/v1/delivery/work_items")).json()["items"]
    row = next(r for r in records if r["data"]["name"] == "Imported work")
    assert (await change(c, row, name="Local edit")).status_code == 200
    conflict = await submit(
        c,
        integration,
        CSV.replace("Imported work", "Remote edit").replace("2026-10-09", "2026-10-10"),
    )
    await execute(app, conflict, ids)
    conflicts = (await c.get(f"/api/v1/integrations/activity/jobs/{conflict.json()['id']}")).json()
    assert conflicts["errors"][0]["code"] == "LOCAL_REVISION_CONFLICT"
    assert any(
        r["data"]["name"] == "Local edit"
        for r in (await c.get("/api/v1/delivery/work_items")).json()["items"]
    )


@pytest.mark.integration
async def test_signed_webhook_replay_cancellation_and_tenant_rls(identity, monkeypatch):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    webhook_ref = f"PPM_CONNECTOR_{ids['a'].hex.upper()}_CSV_WEBHOOK"
    monkeypatch.setenv(webhook_ref, "test-secret-only")
    foreign_secret = await send(
        c,
        "POST",
        "/integrations",
        headers={"idempotency-key": str(uuid4())},
        json=dict(
            name="Invalid foreign secret",
            provider="csv",
            project_id=project["id"],
            webhook_secret_ref=f"PPM_CONNECTOR_{ids['b'].hex.upper()}_CSV_WEBHOOK",
        ),
    )
    assert foreign_secret.status_code == 422
    integration = await connection(c, project, webhook_secret_ref=webhook_ref)
    payload = json.dumps({"csv_text": CSV}).encode()
    headers = {
        "content-type": "application/json",
        "x-github-delivery": "delivery-1",
        "x-hub-signature-256": "sha256="
        + hmac.new(b"test-secret-only", payload, hashlib.sha256).hexdigest(),
    }
    url = f"/integrations/{integration['id']}/webhook"
    bad = await send(
        c, "POST", url, content=payload, headers=headers | {"x-hub-signature-256": "bad"}
    )
    assert bad.status_code == 403
    first = await send(c, "POST", url, content=payload, headers=headers)
    repeat = await send(c, "POST", url, content=payload, headers=headers)
    assert first.status_code == 202 and repeat.json()["id"] == first.json()["id"]
    cancelled = await send(c, "POST", f"/integrations/activity/jobs/{first.json()['id']}/cancel")
    assert cancelled.status_code == 200
    await execute(app, first, ids)
    assert (await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}")).json()[
        "status"
    ] == "cancelled"
    await login(c, emails, "viewer", ids["a"])
    assert (await submit(c, integration, CSV)).status_code == 403
    assert (
        await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}/events")
    ).status_code == 404
    await login(c, emails, "other", ids["b"])
    assert (
        await c.get(f"/api/v1/integrations/activity/jobs/{first.json()['id']}/events")
    ).status_code == 404
    async with app.state.engine.begin() as conn:
        assert await conn.scalar(sa.select(sa.func.count()).select_from(jobs)) == 0
        await context(conn, ids["other"], ids["b"], "Admin")
        assert (
            await conn.scalar(sa.select(jobs.c.id).where(jobs.c.id == UUID(first.json()["id"])))
            is None
        )
    async with app.state.engine.begin() as conn:
        assert await conn.scalar(sa.select(sa.func.count()).select_from(events)) == 0


@pytest.mark.integration
async def test_github_jira_contract_fixtures_and_sprint_ingestion(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    for provider, resource, entity, mapping, record in [
        (
            "github",
            "example/repository",
            "issues",
            {
                "external_id": "number",
                "name": "title",
                "status": "state",
                "source_updated_at": "updated_at",
            },
            {
                "number": 4,
                "title": "GitHub issue",
                "state": "open",
                "updated_at": "2026-10-09T00:00:00Z",
            },
        ),
        (
            "github",
            "example/repository",
            "pulls",
            {
                "external_id": "number",
                "name": "title",
                "status": "state",
                "source_updated_at": "updated_at",
            },
            {
                "number": 5,
                "title": "GitHub PR",
                "state": "closed",
                "updated_at": "2026-10-09T00:00:00Z",
            },
        ),
        (
            "jira",
            "example.atlassian.net",
            "issues",
            {
                "external_id": "id",
                "name": "fields.summary",
                "status": "fields.status.name",
                "source_updated_at": "fields.updated",
            },
            {
                "id": "100",
                "fields": {
                    "summary": "Jira issue",
                    "status": {"name": "To Do"},
                    "updated": "2026-10-09T00:00:00Z",
                },
            },
        ),
    ]:
        result = await send(
            c,
            "POST",
            "/integrations",
            headers={"idempotency-key": str(uuid4())},
            json=dict(
                name="Provider contract fixture",
                provider=provider,
                resource=resource,
                project_id=project["id"],
                entity=entity,
                mapping=mapping,
                status_map={"open": "backlog", "closed": "done", "To Do": "backlog"},
            ),
        )
        assert result.status_code == 201, result.text
        sync = await submit(c, result.json(), records=[record])
        await execute(app, sync, ids)
        assert (await c.get(f"/api/v1/integrations/activity/jobs/{sync.json()['id']}")).json()[
            "status"
        ] == "succeeded"
    team = await create(c, "teams")
    result = await send(
        c,
        "POST",
        "/integrations",
        headers={"idempotency-key": str(uuid4())},
        json=dict(
            name="Jira sprint fixture",
            provider="jira",
            resource="example.atlassian.net",
            project_id=project["id"],
            entity="sprints",
            board_id=1,
            team_id=team["id"],
            mapping={
                "external_id": "id",
                "name": "name",
                "source_updated_at": "updated_at",
                "start_date": "startDate",
                "end_date": "endDate",
                "status": "state",
            },
            status_map={"future": "planned"},
        ),
    )
    assert result.status_code == 201, result.text
    sync = await submit(
        c,
        result.json(),
        records=[
            dict(
                id=8,
                name="Imported planned sprint",
                updated_at="2026-10-09T00:00:00Z",
                startDate="2026-10-12",
                endDate="2026-10-26",
                state="future",
            )
        ],
    )
    await execute(app, sync, ids)
    assert (await c.get(f"/api/v1/integrations/activity/jobs/{sync.json()['id']}")).json()[
        "status"
    ] == "succeeded"
    # Native Jira sprint DTO has no modification timestamp. Never invent historical velocity.
    closed = await submit(
        c,
        result.json(),
        records=[
            dict(
                id=9,
                name="Imported historical sprint",
                startDate="2026-09-01T09:00:00+05:30",
                endDate="2026-09-15T17:00:00+05:30",
                state="closed",
            )
        ],
    )
    await execute(app, closed, ids)
    state = (await c.get(f"/api/v1/integrations/activity/jobs/{closed.json()['id']}")).json()
    assert state["status"] == "succeeded", state
    async with owner.connect() as conn:
        source = (
            (
                await conn.execute(
                    sa.select(sources).where(
                        sources.c.integration_id == UUID(result.json()["id"]),
                        sources.c.external_id == "9",
                    )
                )
            )
            .mappings()
            .one()
        )
        assert source["source_updated_at"] is None and source["source_observed_at"] is not None
        closure = (
            (
                await conn.execute(
                    sa.select(TABLES["sprint_closures"]).where(
                        TABLES["sprint_closures"].c.sprint_id == source["target_id"]
                    )
                )
            )
            .mappings()
            .one()
        )
        assert not closure["complete"]
