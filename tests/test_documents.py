"""Real restricted PostgreSQL role and live clamd where configured; no normal data writes."""

import asyncio
import base64
import os
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api import document_tables as D
from ppm_api import job_tables as J
from ppm_api.document_parser import IntakeError, scan
from ppm_api.documents import document_worker
from ppm_api.identity import context, now
from ppm_api.ppm_tables import TABLES
from sqlalchemy.exc import DBAPIError
from test_delivery import create, setup
from test_identity import identity as identity
from test_identity import login, send

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires guarded ppm_test"
    ),
]


async def upload(c, project, text=b"Supplier delay requires approval", **values):
    headers = values.pop("headers", {"idempotency-key": str(uuid4())})
    result = await send(
        c,
        "POST",
        "/documents",
        headers=headers,
        json=dict(
            title="Source evidence",
            category="SRS",
            project_id=project["id"],
            filename="source.txt",
            content_base64=base64.b64encode(text).decode(),
        )
        | values,
    )
    assert result.status_code == 202, result.text
    return result.json()


async def process(app, accepted, ids, actor="admin"):
    assert await document_worker(
        app.state.engine, UUID(accepted["job_id"]), ids["a"], ids[actor], app.state.settings
    )


async def clean_scanner(monkeypatch):
    # Explicit transport double; separate live daemon acceptance is below.
    monkeypatch.setattr("ppm_api.documents.scan", lambda *_: "fixture-clean")


async def test_library_versions_idempotency_retrieval_citations_and_download(identity, monkeypatch):
    await clean_scanner(monkeypatch)
    c, app, owner, ids, emails, _, project = await setup(identity)
    key = str(uuid4())
    one = await upload(c, project, headers={"idempotency-key": key})
    from ppm_api.jobs import run_job

    await run_job(app.state.engine, UUID(one["job_id"]), ids["b"], ids["other"])
    async with owner.connect() as conn:
        assert (
            await conn.scalar(sa.select(J.jobs.c.status).where(J.jobs.c.id == UUID(one["job_id"])))
            == "queued"
        )
    again = await upload(c, project, headers={"idempotency-key": key})
    assert one["version_id"] == again["version_id"]
    await process(app, one, ids)
    await process(app, one, ids)  # broker redelivery creates no duplicate effects
    result = (await c.get("/api/v1/documents/search?q=Supplier")).json()
    assert result["embedding_status"] == "budgeted_ai_runtime" and len(result["items"]) == 1
    hit = result["items"][0]
    assert hit["location"].startswith("paragraph 1")
    assert (await c.get("/api/v1/documents/citations/" + hit["id"])).status_code == 200
    ticket = await send(c, "POST", f"/documents/versions/{one['version_id']}/download-ticket")
    assert ticket.status_code == 200
    token = ticket.json()["token"]
    url = f"/api/v1/documents/versions/{one['version_id']}/download?token={token}"
    assert (await c.get(url)).content == b"Supplier delay requires approval"
    d = (await c.get("/api/v1/documents/" + one["document"]["id"])).json()
    second = await upload(
        c,
        project,
        b"Budget governance charter",
        document_id=d["id"],
        headers={"idempotency-key": str(uuid4()), "if-match": str(d["revision"])},
    )
    assert second["document"]["revision"] == 2
    assert (await c.get("/api/v1/documents/citations/" + hit["id"])).status_code == 409
    await process(app, second, ids)
    assert not (await c.get("/api/v1/documents/search?q=Supplier")).json()["items"]
    assert len((await c.get("/api/v1/documents/search?q=Budget")).json()["items"]) == 1
    # Original version is immutable under the real non-bypass role.
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(
                    D.versions.update()
                    .where(D.versions.c.id == UUID(one["version_id"]))
                    .values(sha256="0" * 64)
                )
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(
                    D.versions.delete().where(D.versions.c.id == UUID(one["version_id"]))
                )
    d = second["document"]
    replayed = await send(
        c,
        "POST",
        f"/documents/versions/{second['version_id']}/reprocess",
        headers={"idempotency-key": str(uuid4()), "if-match": str(d["revision"])},
    )
    assert replayed.status_code == 202, replayed.text
    await process(app, replayed.json(), ids)
    assert len((await c.get("/api/v1/documents/search?q=Budget")).json()["items"]) == 1


async def test_scoped_roles_counts_revocation_worker_and_signed_capabilities(identity, monkeypatch):
    await clean_scanner(monkeypatch)
    c, app, owner, ids, emails, _, project = await setup(identity)
    accepted = await upload(c, project)
    await process(app, accepted, ids)
    v = accepted["version_id"]
    d = accepted["document"]["id"]
    await create(c, "grants", user_id=str(ids["pm"]), project_id=project["id"], access="edit")
    await create(c, "grants", user_id=str(ids["viewer"]), project_id=project["id"], access="read")
    await login(c, emails, "viewer", ids["a"])
    assert (await c.get("/api/v1/documents")).json()["total"] == 1
    ticket = await send(c, "POST", f"/documents/versions/{v}/download-ticket")
    url = f"/api/v1/documents/versions/{v}/download?token={ticket.json()['token']}"
    assert (await c.get(url)).status_code == 200
    denied = await send(
        c,
        "POST",
        "/documents",
        headers={"idempotency-key": str(uuid4())},
        json={
            "title": "Denied",
            "category": "SRS",
            "project_id": project["id"],
            "filename": "x.txt",
            "content_base64": "eA==",
        },
    )
    assert denied.status_code == 403
    async with owner.begin() as conn:
        await conn.execute(
            TABLES["grants"]
            .update()
            .where(TABLES["grants"].c.user_id == ids["viewer"])
            .values(archived=True)
        )
    assert (await c.get(url)).status_code == 404
    assert (await c.get("/api/v1/documents")).json()["total"] == 0
    assert not (await c.get("/api/v1/documents/search?q=Supplier")).json()["items"]
    await login(c, emails, "pm", ids["a"])
    queued = await upload(c, project, b"PM source text")
    async with owner.begin() as conn:
        await conn.execute(
            TABLES["grants"]
            .update()
            .where(TABLES["grants"].c.user_id == ids["pm"])
            .values(archived=True)
        )
    await process(app, queued, ids, "pm")
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(J.jobs.c.status).where(J.jobs.c.id == UUID(queued["job_id"]))
            )
            == "cancelled"
        )
    await login(c, emails, "other", ids["b"])
    assert (await c.get("/api/v1/documents/" + d)).status_code == 404
    assert (await c.get("/api/v1/documents/versions/" + v + "/preview")).status_code == 404
    assert (await c.get("/api/v1/documents")).json()["total"] == 0
    async with app.state.engine.begin() as conn:
        assert not list((await conn.execute(sa.select(D.versions))).mappings())
        await context(conn, ids["other"], ids["b"], "Admin")
        assert not await conn.scalar(sa.select(D.versions.c.id).where(D.versions.c.id == UUID(v)))
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(
                    D.chunks.insert().values(
                        id=uuid4(),
                        organization_id=ids["b"],
                        version_id=UUID(v),
                        ordinal=999,
                        location="forged",
                        text="foreign",
                        method="text",
                    )
                )


async def test_quarantine_failure_cancel_deletion_and_inflight_revocation(identity, monkeypatch):
    c, app, owner, ids, emails, _, project = await setup(identity)
    bad = await upload(c, project, b"not a PDF", filename="bad.pdf")
    await process(app, bad, ids)
    assert (
        await c.get(f"/api/v1/documents/versions/{bad['version_id']}/preview")
    ).status_code == 409
    monkeypatch.setattr(
        "ppm_api.documents.scan",
        lambda *_: (_ for _ in ()).throw(IntakeError("SCANNER_UNAVAILABLE")),
    )
    blocked = await upload(c, project)
    await process(app, blocked, ids)
    d = (await c.get("/api/v1/documents/" + blocked["document"]["id"])).json()
    assert d["versions"][0]["diagnostic"] == "SCANNER_UNAVAILABLE"
    await clean_scanner(monkeypatch)
    retry = await send(
        c,
        "POST",
        f"/documents/versions/{blocked['version_id']}/reprocess",
        headers={"idempotency-key": str(uuid4()), "if-match": str(d["revision"])},
    )
    assert retry.status_code == 202, retry.text
    await process(app, retry.json(), ids)
    recovered = (await c.get("/api/v1/documents/" + d["id"])).json()
    assert recovered["versions"][0]["status"] == "ready"
    queued = await upload(c, project, b"Cancelled source")
    assert (
        await send(
            c,
            "POST",
            f"/documents/versions/{queued['version_id']}/cancel",
            headers={"if-match": "1"},
        )
    ).status_code == 200
    await process(app, queued, ids)
    assert not (await c.get("/api/v1/documents/search?q=Cancelled")).json()["items"]
    running = await upload(c, project, b"In-flight source")
    original = __import__("ppm_api.documents", fromlist=["isolated_extract"]).isolated_extract
    # Simulate deletion while parser is running outside the database transaction.
    entered, release = __import__("threading").Event(), __import__("threading").Event()

    def delayed(*args):
        entered.set()
        assert release.wait(10)
        return original(*args)

    monkeypatch.setattr("ppm_api.documents.isolated_extract", delayed)
    task = asyncio.create_task(process(app, running, ids))
    assert await asyncio.to_thread(entered.wait, 10)
    assert (
        await send(
            c, "DELETE", "/documents/" + running["document"]["id"], headers={"if-match": "1"}
        )
    ).status_code == 200
    release.set()
    await task
    assert not (await c.get("/api/v1/documents/search?q=flight")).json()["items"]
    assert (
        await c.get(f"/api/v1/documents/versions/{running['version_id']}/preview")
    ).status_code == 404


async def test_policy_retention_hold_purge_and_scope(identity, monkeypatch):
    await clean_scanner(monkeypatch)
    c, app, owner, ids, emails, _, project = await setup(identity)
    accepted = await upload(c, {"id": None}, b"Governance policy controls", category="policy")
    await process(app, accepted, ids)
    d = accepted["document"]
    policy = dict(
        owner_id=str(ids["admin"]),
        applicability="Organization governance",
        state="current",
        version_id=accepted["version_id"],
        effective_date="2026-01-01",
        review_date="2026-02-01",
    )
    values = dict(
        legal_hold=True, retain_until=(now() - timedelta(days=1)).isoformat(), policy=policy
    )
    saved = await send(
        c, "PATCH", f"/documents/{d['id']}/governance", json=values, headers={"if-match": "1"}
    )
    assert saved.status_code == 200, saved.text
    assert saved.json()["policy_label"] == "review overdue"
    assert (
        await send(
            c, "PATCH", f"/documents/{d['id']}/governance", json=values, headers={"if-match": "1"}
        )
    ).status_code == 412
    await login(c, emails, "pm", ids["a"])
    assert (await c.get("/api/v1/documents/" + d["id"])).status_code == 200
    assert (
        await send(
            c, "PATCH", f"/documents/{d['id']}/governance", json=values, headers={"if-match": "2"}
        )
    ).status_code == 403
    await login(c, emails, org=ids["a"])
    ticket = (
        await send(c, "POST", f"/documents/versions/{accepted['version_id']}/download-ticket")
    ).json()
    assert (
        await send(c, "DELETE", "/documents/" + d["id"], headers={"if-match": "2"})
    ).status_code == 200
    assert (
        await c.get(
            f"/api/v1/documents/versions/{accepted['version_id']}/download?token={ticket['token']}"
        )
    ).status_code == 404
    assert (
        await send(c, "POST", f"/documents/{d['id']}/purge", headers={"if-match": "3"})
    ).status_code == 409
    values["legal_hold"] = False
    values["policy"] = None
    saved = await send(
        c, "PATCH", f"/documents/{d['id']}/governance", json=values, headers={"if-match": "3"}
    )
    assert saved.status_code == 200, saved.text
    assert (
        await send(c, "POST", f"/documents/{d['id']}/purge", headers={"if-match": "4"})
    ).status_code == 200
    async with owner.connect() as conn:
        v = (
            (
                await conn.execute(
                    sa.select(D.versions).where(D.versions.c.id == UUID(accepted["version_id"]))
                )
            )
            .mappings()
            .one()
        )
        assert v["status"] == "purged"
        assert not await conn.scalar(
            sa.select(D.chunks.c.id).where(D.chunks.c.version_id == v["id"])
        )
        assert not app.state.storage._path(v["object_key"]).exists()


async def test_category_matrix_and_labeled_retrieval_evaluation(identity, monkeypatch):
    await clean_scanner(monkeypatch)
    c, app, owner, ids, emails, _, project = await setup(identity)
    labels = {
        "SRS": "Authentication requirements",
        "BRD": "Revenue objectives",
        "PRD": "Product usability",
        "MOM": "Committee minutes",
        "sprint_report": "Iteration throughput",
        "risk_log": "Supplier disruption",
        "charter": "Sponsorship mandate",
        "policy": "Governance review",
    }
    for category, text in labels.items():
        accepted = await upload(c, project, text.encode(), title=category, category=category)
        await process(app, accepted, ids)
    correct = 0
    for category, text in labels.items():
        result = (await c.get("/api/v1/documents/search", params={"q": text})).json()["items"]
        correct += bool(
            result and result[0]["title"] == category and "paragraph 1" in result[0]["location"]
        )
    assert correct == len(labels), f"Keyword top-1 locations: {correct}/{len(labels)}"


async def test_real_clamd_and_processing_job(identity):
    c, app, owner, ids, emails, _, project = await setup(identity)
    if not app.state.settings.document_scanner_host:
        pytest.skip("Live clamd not configured; fixture results do not establish live scanning")
    assert (
        await asyncio.to_thread(
            scan, b"live clean fixture", app.state.settings.document_scanner_host
        )
        == "clamd-instream"
    )
    with pytest.raises(IntakeError, match="SCAN_REJECTED"):
        await asyncio.to_thread(
            scan,
            b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*",
            app.state.settings.document_scanner_host,
        )
    accepted = await upload(c, project)
    await process(app, accepted, ids)
    d = (await c.get("/api/v1/documents/" + accepted["document"]["id"])).json()
    assert d["versions"][0]["status"] == "ready", d
    assert d["versions"][0]["scanner"] == "clamd-instream"


async def test_125_document_paging_bounds_and_concurrent_replay(identity):
    c, app, owner, ids, emails, _, project = await setup(identity)
    rows = [
        dict(
            id=uuid4(),
            organization_id=ids["a"],
            project_id=UUID(project["id"]),
            title=f"Paging evidence {i:03d}" + (" literal%" if i == 0 else ""),
            category="SRS",
            created_at=now() - timedelta(seconds=i),
            revision=1,
            deleted_at=None,
            legal_hold=False,
            retain_until=now() + timedelta(days=30),
            policy=None,
        )
        for i in range(125)
    ]
    async with owner.begin() as conn:
        await conn.execute(D.documents.insert(), rows)
    page = (await c.get("/api/v1/documents?offset=100&limit=25")).json()
    assert page["total"] == 125 and len(page["items"]) == 25
    assert page["items"][-1]["title"] == "Paging evidence 124"
    assert (await c.get("/api/v1/documents?q=%25")).json()["total"] == 1
    assert (await c.get("/api/v1/documents?q=_")).json()["total"] == 0
    assert (await c.get("/api/v1/documents?limit=101")).status_code == 422
    assert (await c.get("/api/v1/documents?offset=-1")).status_code == 422
    key = str(uuid4())
    repeated = await asyncio.gather(
        *[upload(c, project, headers={"idempotency-key": key}) for _ in range(2)]
    )
    assert repeated[0]["version_id"] == repeated[1]["version_id"]
    assert repeated[0]["job_id"] == repeated[1]["job_id"]
    await login(c, emails, "viewer", ids["a"])
    assert (await c.get("/api/v1/documents?offset=100")).json()["total"] == 0


async def test_transport_replay_integrity_expiry_orphans_and_holds(identity, monkeypatch):

    import jwt

    await clean_scanner(monkeypatch)
    c, app, owner, ids, emails, _, project = await setup(identity)
    key = str(uuid4())
    accepted = await upload(c, project, headers={"idempotency-key": key})
    changed = await send(
        c,
        "POST",
        "/documents",
        headers={"idempotency-key": key},
        json={
            "title": "Changed request",
            "category": "SRS",
            "project_id": project["id"],
            "filename": "source.txt",
            "content_base64": "eA==",
        },
    )
    assert changed.status_code == 409
    assert (await c.post("/api/v1/documents", json={})).status_code == 403
    assert (
        await send(
            c,
            "DELETE",
            "/documents/" + accepted["document"]["id"],
            headers={"x-organization-id": str(ids["b"]), "if-match": "1"},
        )
    ).status_code == 409
    assert (await send(c, "DELETE", "/documents/" + accepted["document"]["id"])).status_code == 428
    await process(app, accepted, ids)
    vid = accepted["version_id"]
    token = (await send(c, "POST", f"/documents/versions/{vid}/download-ticket")).json()["token"]
    claims = jwt.decode(token, options={"verify_signature": False})
    claims["exp"] = now() - timedelta(seconds=1)
    expired = jwt.encode(
        claims, app.state.settings.jwt_secret.get_secret_value(), algorithm="HS256"
    )
    assert (
        await c.get(f"/api/v1/documents/versions/{vid}/download?token={expired}")
    ).status_code == 403
    async with owner.connect() as conn:
        key_path = await conn.scalar(
            sa.select(D.versions.c.object_key).where(D.versions.c.id == UUID(vid))
        )
    app.state.storage.put(key_path, b"tampered bytes")
    assert (
        await c.get(f"/api/v1/documents/versions/{vid}/download?token={token}")
    ).status_code == 409
    orphan = f"{ids['a']}/documents/{uuid4()}/{uuid4()}"
    held = f"{ids['a']}/documents/{accepted['document']['id']}/{uuid4()}"
    fresh = f"{ids['a']}/documents/{uuid4()}/{uuid4()}"
    for path in [orphan, held, fresh]:
        app.state.storage.put(path, b"orphan fixture")
    for path in [orphan, held]:
        os.utime(app.state.storage._path(path), (0, 0))
    os.utime(app.state.storage._path(key_path), (0, 0))
    async with owner.begin() as conn:
        await conn.execute(
            D.documents.update()
            .where(D.documents.c.id == UUID(accepted["document"]["id"]))
            .values(legal_hold=True)
        )
        await conn.execute(
            TABLES["projects"]
            .update()
            .where(TABLES["projects"].c.id == UUID(project["id"]))
            .values(archived=True)
        )
    candidates = (await c.get("/api/v1/documents/retention/orphans")).json()["keys"]
    assert orphan in candidates and held not in candidates and fresh not in candidates
    assert key_path not in candidates, "Archived source references must never become orphan objects"
    assert (
        await send(c, "POST", "/documents/retention/orphans/purge", json={"keys": [held]})
    ).status_code == 409
    assert (
        await send(c, "POST", "/documents/retention/orphans/purge", json={"keys": [orphan]})
    ).status_code == 200
    assert not app.state.storage._path(orphan).exists()
    assert app.state.storage._path(held).exists() and app.state.storage._path(fresh).exists()
    # A forged cross-tenant object key is never accepted as a cleanup target.
    foreign = f"{ids['b']}/documents/{uuid4()}/{uuid4()}"
    assert (
        await send(c, "POST", "/documents/retention/orphans/purge", json={"keys": [foreign]})
    ).status_code == 409


async def test_assessment_bridge_preserves_completed_scores_and_private_grants(
    identity, monkeypatch
):
    from ppm_api.assessment_tables import assessments
    from test_assessment import fixture, ok, save

    await clean_scanner(monkeypatch)
    c, app, owner, ids, emails, fw, v, a = await fixture(identity)
    a = (await save(c, a, v))["assessment"]
    question = v["snapshot"]["dimensions"][0]["questions"][0]
    attachment = await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/evidence",
        {
            "question_id": question["id"],
            "file_name": "minutes.txt",
            "content_base64": base64.b64encode(b"Approved process minutes").decode(),
        },
        a["revision"],
    )
    a = (await c.get(f"/api/v1/assessment/assessments/{a['id']}")).json()["assessment"]
    a = await ok(c, "POST", f"/assessments/{a['id']}/submit", {}, a["revision"])
    await login(c, emails, "pm", ids["a"])
    a = await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/review",
        {"action": "start", "note": "Review"},
        a["revision"],
    )
    await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/evidence/{attachment['id']}/release",
        {"note": "Reviewed source text"},
        a["revision"],
    )
    a = (await c.get(f"/api/v1/assessment/assessments/{a['id']}")).json()["assessment"]
    a = await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/review",
        {"action": "complete", "note": "Accepted evidence"},
        a["revision"],
    )
    async with owner.connect() as conn:
        before = dict(
            (await conn.execute(sa.select(assessments).where(assessments.c.id == UUID(a["id"]))))
            .mappings()
            .one()
        )
    await login(c, emails, org=ids["a"])
    source = await upload(c, {"id": None}, b"Approved process minutes", category="policy")
    await process(app, source, ids)
    response = await send(
        c,
        "POST",
        f"/documents/versions/{source['version_id']}/assessment-link",
        json={"attachment_id": attachment["id"]},
        headers={"if-match": "1"},
    )
    assert response.status_code == 200, response.text
    references = await c.get(f"/api/v1/documents/versions/{source['version_id']}/assessment-links")
    assert references.status_code == 200, references.text
    assert references.json()[0]["assessment_id"] == a["id"]
    async with owner.connect() as conn:
        after = dict(
            (await conn.execute(sa.select(assessments).where(assessments.c.id == UUID(a["id"]))))
            .mappings()
            .one()
        )
    assert before == after
    await login(c, emails, "viewer", ids["a"])
    response = await send(
        c,
        "POST",
        f"/documents/versions/{source['version_id']}/assessment-link",
        json={"attachment_id": attachment["id"]},
        headers={"if-match": "1"},
    )
    assert response.status_code == 403
    hidden = await c.get(f"/api/v1/documents/versions/{source['version_id']}/assessment-links")
    assert hidden.status_code == 200 and hidden.json() == []
