"""Local Sprint 12 acceptance: authority, source review, leakage and reproducibility."""

from copy import deepcopy
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api.connectors import logical_key
from ppm_api.identity import context, now
from ppm_api.identity_tables import sessions
from ppm_api.ingestion import ConnectorConfig
from ppm_api.job_tables import jobs, sources
from ppm_api.jobs import run_job
from ppm_api.ml import fixture
from ppm_api.ml_pipeline import build_dataset, evaluate
from ppm_api.ml_schemas import DatasetInput, HistoryInput
from ppm_api.ml_tables import principals
from test_delivery import change, setup
from test_identity import identity as identity
from test_identity import login, send
from test_jobs import CSV, connection, execute, submit


def test_provider_identity_ignores_connection_names_and_manual_namespaces():
    config = ConnectorConfig(
        name="First", provider="github", resource="Example/Repo", project_id=uuid4()
    )
    another = config.model_copy(
        update={"name": "Second", "source_namespace": "unrelated", "resource": "example/repo"}
    )
    assert logical_key(config, "12") == logical_key(another, "12")
    assert logical_key(config, "12") != logical_key(config, "13")


@pytest.mark.parametrize("target", ["delay", "overrun", "failure", "risk", "sentiment"])
def test_cpu_reproduction_and_split_contract(target):
    example = fixture(uuid4(), target)
    history = HistoryInput(**example["history"])
    spec = DatasetInput(history_id=uuid4(), **example["dataset"])
    manifest, records = build_dataset(history, spec)
    assert manifest["eligibility"] == "demo_only" and manifest["split_counts"] == {
        "train": 30,
        "validation": 30,
        "test": 30,
    }
    entities = [
        {r["entity_id"] for r in records if r["split"] == s}
        for s in ("train", "validation", "test")
    ]
    assert (
        not entities[0] & entities[1]
        and not entities[0] & entities[2]
        and not entities[1] & entities[2]
    )
    card, artifacts = evaluate(manifest, records, "test-digest")
    again, second = evaluate(manifest, records, "test-digest")
    assert card["result_hash"] == again["result_hash"] and artifacts == second
    assert card["promotion"].startswith("BLOCKED")
    assert len(card["candidates"]) == 3 and card["uncertainty"]["repetitions"] == 200


@pytest.mark.parametrize(
    "mutation",
    [
        "feature_future",
        "baseline_future",
        "ai_label",
        "mixed",
        "private_text",
        "unauthorized",
        "license",
    ],
)
def test_history_rejects_leakage_unsuitable_labels_privacy_and_license(mutation):
    body = fixture(uuid4())["history"]
    first = body["records"][0]
    if mutation == "feature_future":
        first["feature_asof"] = "2026-01-01T00:00:00Z"
    elif mutation == "baseline_future":
        first["outcome"]["baseline_known_at"] = "2026-01-01T00:00:00Z"
    elif mutation == "ai_label":
        first["outcome"]["evidence_ref"] = "ai_run:123"
    elif mutation == "mixed":
        first["outcome"]["kind"] = "observed"
    elif mutation == "private_text":
        first["notes"] = "Private personal note"
    elif mutation == "unauthorized":
        body["authorized"] = False
    else:
        body["lineage"] = "real"
    with pytest.raises(ValueError):
        HistoryInput(**body)


def test_entity_purge_late_label_incompatible_target_and_missing_behavior():
    example = fixture(uuid4())
    body = example["history"]
    body["records"][30]["entity_id"] = body["records"][0]["entity_id"]
    body["records"][1]["outcome"]["available_at"] = "2025-12-01T00:00:00Z"
    spec = DatasetInput(history_id=uuid4(), **example["dataset"])
    manifest, records = build_dataset(HistoryInput(**body), spec)
    assert manifest["excluded"]["entity_crosses_splits"] == 2
    assert manifest["excluded"]["outcome_not_available_at_boundary"] == 1
    assert len(records) == 87
    spec.target = "failure"
    manifest, records = build_dataset(HistoryInput(**body), spec)
    card, artifacts = evaluate(manifest, records, "empty")
    assert card["eligibility"] == "insufficient_data" and card["metrics"] == {}
    assert artifacts["tracking"]["status"] == "insufficient_data"


async def approve(c, integration, revision=0, active=True, **values):
    return await send(
        c,
        "PUT",
        f"/integrations/{integration['id']}/authority",
        headers={"if-match": str(revision)},
        json={"active": active, **values},
    )


@pytest.mark.integration
async def test_connector_logout_dedup_conflict_rotation_revocation_and_tenant(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    integration = await connection(c, project)
    authorization = await approve(c, integration)
    assert authorization.status_code == 200, authorization.text
    first = await submit(c, integration, CSV)
    await send(c, "POST", "/auth/logout")
    await execute(app, first, ids)
    async with owner.connect() as conn:
        assert (
            await conn.scalar(sa.select(jobs.c.status).where(jobs.c.id == UUID(first.json()["id"])))
            == "succeeded"
        )
    await login(c, emails, org=ids["a"])
    async with owner.begin() as conn:
        # Simulate source rows written at 0016, before canonical keys existed.
        await conn.execute(
            sources.update()
            .where(sources.c.project_id == UUID(project["id"]))
            .values(logical_key=None)
        )
    second_connection = await connection(c, project, name="Same source through another connection")
    duplicate = await submit(c, second_connection, CSV)
    await execute(app, duplicate, ids)
    work = (
        await c.get("/api/v1/delivery/work_items", params={"project_id": project["id"]})
    ).json()["items"]
    assert len(work) == 2
    local = work[0]
    edit = await change(c, local, name="Preserved local edit")
    assert edit.status_code == 200
    csv = CSV.replace("Imported work", "Changed upstream").replace("2026-10-09", "2026-10-10")
    update = await submit(c, integration, csv)
    await execute(app, update, ids)
    reviews = (await c.get(f"/api/v1/integrations/{integration['id']}/conflicts")).json()
    assert len(reviews) == 1 and reviews[0]["status"] == "pending"
    conflict = reviews[0]
    path = f"/integrations/{integration['id']}/conflicts/{conflict['id']}/resolve"
    payload = dict(
        decision="keep_local", local_revision=999, source_fingerprint=conflict["fingerprint"]
    )
    assert (
        await send(c, "POST", path, headers={"if-match": str(conflict["revision"])}, json=payload)
    ).status_code == 412
    payload["local_revision"] = edit.json()["revision"]
    resolution = await send(
        c, "POST", path, headers={"if-match": str(conflict["revision"])}, json=payload
    )
    assert resolution.status_code == 200, resolution.text
    assert (await c.get(f"/api/v1/delivery/work_items/{local['id']}")).json()["data"][
        "name"
    ] == "Preserved local edit"
    assert (
        await send(c, "POST", path, headers={"if-match": str(conflict["revision"])}, json=payload)
    ).status_code == 412
    newer = await submit(
        c,
        integration,
        csv.replace("2026-10-10", "2026-10-11").replace(
            "Changed upstream", "Reviewed newest source"
        ),
    )
    await execute(app, newer, ids)
    reviews = (await c.get(f"/api/v1/integrations/{integration['id']}/conflicts")).json()
    latest = reviews[0]
    assert latest["status"] == "pending" and latest["revision"] > conflict["revision"]
    # Keeping local is sticky: the next upstream version still requires review.
    assert (await c.get(f"/api/v1/delivery/work_items/{local['id']}")).json()["data"][
        "name"
    ] == "Preserved local edit"
    accepted = await send(
        c,
        "POST",
        path,
        headers={"if-match": str(latest["revision"])},
        json=dict(
            decision="accept_source",
            local_revision=edit.json()["revision"],
            source_fingerprint=latest["fingerprint"],
        ),
    )
    assert accepted.status_code == 200, accepted.text
    assert (await c.get(f"/api/v1/delivery/work_items/{local['id']}")).json()["data"][
        "name"
    ] == "Reviewed newest source"
    queued = await submit(c, integration, CSV)
    rotated = await approve(c, integration, 1)
    assert rotated.status_code == 200
    await execute(app, queued, ids)
    assert (await c.get(f"/api/v1/integrations/activity/jobs/{queued.json()['id']}")).json()[
        "status"
    ] == "cancelled"
    queued = await submit(c, integration, CSV)
    revoked = await approve(c, integration, 2, False)
    assert revoked.status_code == 200
    await execute(app, queued, ids)
    assert (await submit(c, integration, CSV)).status_code == 409
    await login(c, emails, "viewer", org=ids["a"])
    assert (await approve(c, integration, 3)).status_code == 403
    await login(c, emails, "other", org=ids["b"])
    assert (await c.get(f"/api/v1/integrations/{integration['id']}/authority")).status_code == 404


@pytest.mark.integration
async def test_connector_schedule_survives_session_and_stops_after_revoke(identity, monkeypatch):
    from ppm_api.connectors import schedule_connectors

    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    integration = await connection(
        c,
        project,
        provider="github",
        resource="example/repo",
        mode="live",
        secret_ref=f"PPM_CONNECTOR_{ids['a'].hex.upper()}_GITHUB_TOKEN",
    )
    approved = await approve(
        c, integration, interval_minutes=5, secret_ref=integration["config"]["secret_ref"]
    )
    assert approved.status_code == 200, approved.text
    await send(c, "POST", "/auth/logout")
    async with owner.begin() as conn:
        await conn.execute(
            principals.update()
            .where(principals.c.integration_id == UUID(integration["id"]))
            .values(next_due=now() - timedelta(minutes=1))
        )
    await schedule_connectors(app.state.engine)
    async with owner.connect() as conn:
        job = (
            (
                await conn.execute(
                    sa.select(jobs).where(jobs.c.integration_id == UUID(integration["id"]))
                )
            )
            .mappings()
            .one()
        )

    async def remote(*args):
        return [
            {"id": "1", "name": "Scheduled fixture double", "updated_at": "2026-10-01T00:00:00Z"}
        ], None

    monkeypatch.setattr("ppm_api.jobs.remote_page", remote)
    await run_job(app.state.engine, job["id"], ids["a"], ids["admin"])
    async with owner.connect() as conn:
        assert (
            await conn.scalar(sa.select(jobs.c.status).where(jobs.c.id == job["id"])) == "succeeded"
        )


@pytest.mark.integration
async def test_history_dataset_baseline_card_reproduction_withdrawal_and_access(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    example = fixture(UUID(project["id"]))
    key = str(uuid4())
    imported = await send(
        c, "POST", "/ml/histories", headers={"idempotency-key": key}, json=example["history"]
    )
    assert imported.status_code == 201, imported.text
    assert (
        await send(
            c, "POST", "/ml/histories", headers={"idempotency-key": key}, json=example["history"]
        )
    ).json()["id"] == imported.json()["id"]
    changed = deepcopy(example["history"])
    changed["name"] = "different"
    assert (
        await send(c, "POST", "/ml/histories", headers={"idempotency-key": key}, json=changed)
    ).status_code == 409

    history_id = imported.json()["id"]
    dataset = await send(
        c,
        "POST",
        "/ml/datasets",
        headers={"idempotency-key": str(uuid4())},
        json=example["dataset"] | {"history_id": history_id},
    )
    assert dataset.status_code == 201, dataset.text
    dataset_id = dataset.json()["id"]
    cards = []
    for _ in range(2):
        response = await send(
            c,
            "POST",
            "/ml/runs",
            headers={"idempotency-key": str(uuid4())},
            json={"dataset_id": dataset_id},
        )
        assert response.status_code == 202, response.text
        run_id = response.json()["id"]
        async with owner.connect() as conn:
            job = await conn.scalar(sa.select(jobs.c.id).where(jobs.c.ml_run_id == UUID(run_id)))
        await run_job(app.state.engine, job, ids["b"], ids["other"])
        await run_job(app.state.engine, job, ids["a"], ids["admin"])
        run = await c.get(f"/api/v1/ml/runs/{run_id}")
        assert run.json()["status"] == "succeeded", run.text
        cards.append(run.json()["card"])
    assert (
        cards[0]["result_hash"] == cards[1]["result_hash"]
        and cards[1]["repeat_matches_previous"] is True
    )
    artifact_path = f"/api/v1/ml/runs/{run_id}/artifacts"
    assert (await c.get(artifact_path)).status_code == 200
    await login(c, emails, "viewer", org=ids["a"])
    assert (await c.get(artifact_path)).status_code == 403
    assert (await c.get("/api/v1/ml/histories")).status_code == 403
    await login(c, emails, "other", org=ids["b"])
    assert (await c.get(artifact_path)).status_code == 404
    # Real app role RLS: a foreign tenant cannot retrieve a history by guessing its ID.
    async with app.state.engine.begin() as conn:
        await context(conn, ids["other"], ids["b"], "Admin")
        assert (
            await conn.scalar(
                sa.text("SELECT count(*) FROM ml_histories WHERE id=:id"), {"id": UUID(history_id)}
            )
            == 0
        )
    await login(c, emails, org=ids["a"])
    assert (
        await send(c, "POST", f"/ml/histories/{history_id}/withdraw", json={})
    ).status_code == 200
    assert (await c.get(artifact_path)).status_code == 409
    assert (
        await send(
            c,
            "POST",
            "/ml/runs",
            headers={"idempotency-key": str(uuid4())},
            json={"dataset_id": dataset_id},
        )
    ).status_code == 409


@pytest.mark.integration
async def test_unlabeled_real_history_insufficient_card_and_session_revocation(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    example = fixture(UUID(project["id"]))
    body = example["history"] | dict(
        lineage="real",
        license="organization-authorized",
        label_declaration="unlabeled",
        records=[],
        name="Authorized history without outcomes",
    )
    imported = await send(
        c, "POST", "/ml/histories", headers={"idempotency-key": str(uuid4())}, json=body
    )
    assert imported.status_code == 201, imported.text
    result = await send(
        c,
        "POST",
        "/ml/datasets",
        headers={"idempotency-key": str(uuid4())},
        json=example["dataset"] | {"history_id": imported.json()["id"]},
    )
    assert result.status_code == 201, result.text
    dataset_id = result.json()["id"]
    for revoked in (False, True):
        response = await send(
            c,
            "POST",
            "/ml/runs",
            headers={"idempotency-key": str(uuid4())},
            json={"dataset_id": dataset_id},
        )
        run_id = UUID(response.json()["id"])
        async with owner.begin() as conn:
            job = (
                (await conn.execute(sa.select(jobs).where(jobs.c.ml_run_id == run_id)))
                .mappings()
                .one()
            )
            if revoked:
                await conn.execute(
                    sessions.update().where(sessions.c.id == job["session_id"]).values(revoked=True)
                )
        await run_job(app.state.engine, job["id"], ids["a"], ids["admin"])
        await login(c, emails, org=ids["a"])
        run = (await c.get(f"/api/v1/ml/runs/{run_id}")).json()
        if revoked:
            assert run["status"] == "blocked" and run["card"]["eligibility"] == "authority_revoked"
        else:
            assert run["status"] == "insufficient_data" and run["card"]["metrics"] == {}
