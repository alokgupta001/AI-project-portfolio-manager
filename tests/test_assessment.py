"""Scoring and real PostgreSQL workflow/security acceptance for Sprint 06."""

import base64
import os
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api.assessment import compute_scores, validate_definition
from ppm_api.assessment_schemas import FrameworkInput
from ppm_api.identity import context
from sqlalchemy.exc import DBAPIError
from test_delivery import create, setup
from test_identity import identity as identity
from test_identity import login, send


def definition():
    return FrameworkInput.model_validate(
        {
            "name": "Governance fixture",
            "dimensions": [
                {
                    "name": "Governance",
                    "weight": "1",
                    "questions": [
                        {
                            "name": "Process",
                            "text": "Process defined?",
                            "answer_type": "rubric",
                            "weight": "1",
                            "rubric_levels": [
                                {"level": 0, "label": "None"},
                                {"level": 1, "label": "Partial"},
                                {"level": 2, "label": "Full"},
                            ],
                        },
                        {
                            "name": "Delivery",
                            "text": "Delivery controlled?",
                            "answer_type": "boolean",
                            "weight": "3",
                        },
                    ],
                }
            ],
        }
    ).model_dump(mode="json")


def test_weighting_unknown_and_coverage():
    d = definition()
    q = d["dimensions"][0]["questions"]
    dim = d["dimensions"][0]["id"]
    a = {q[0]["id"]: {"value": "1"}, q[1]["id"]: {"value": "true", "evidence_text": "Minutes"}}
    score, dims, _ = compute_scores(d, a)
    assert score == Decimal("87.5") and dims[dim]["coverage_percent"] == 100
    assert dims[dim]["evidence_coverage_percent"] == 50
    score, dims, notes = compute_scores(d, {q[0]["id"]: {"value": "1"}})
    assert score == 50 and dims[dim]["coverage_percent"] == 25 and notes
    assert compute_scores(d, {})[0] is None
    d["dimensions"][0]["questions"][1]["required"] = False
    assert compute_scores(d, a)[1][dim]["coverage_percent"] == 100
    assert compute_scores(d, a, {q[0]["id"]: Decimal(0)})[0] == 75


def test_invalid_rubrics_and_duplicate_ids():
    d = definition()
    d["dimensions"][0]["questions"][0]["rubric_levels"] = [{"level": 0, "label": "Only"}]
    with pytest.raises(Exception, match="distinct levels"):
        validate_definition(d)
    d = definition()
    d["dimensions"][0]["questions"][1]["id"] = d["dimensions"][0]["questions"][0]["id"]
    with pytest.raises(ValueError, match="unique"):
        FrameworkInput.model_validate(d)


integration = pytest.mark.skipif(
    os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires guarded test database"
)


async def write(c, method, path, data=None, rev=None, key=None):
    headers = {"idempotency-key": key or str(uuid4())}
    if rev is not None:
        headers["if-match"] = str(rev)
    return await send(c, method, "/assessment" + path, json=data, headers=headers)


async def ok(c, method, path, data=None, rev=None):
    r = await write(c, method, path, data, rev)
    assert r.status_code in (200, 201), r.text
    return r.json()


async def fixture(identity):
    c, app, owner, ids, emails, _, _ = await setup(identity)
    fw = await ok(c, "POST", "/frameworks", definition())
    v = await ok(c, "POST", f"/frameworks/{fw['id']}/publish", {}, fw["revision"])
    dep = await create(c, "departments", name="Engineering")
    a = await ok(
        c,
        "POST",
        "/assessments",
        dict(
            name="Engineering assessment",
            framework_version_id=v["id"],
            department_id=dep["id"],
            assigned_to=str(ids["admin"]),
            reviewer_id=str(ids["pm"]),
        ),
    )
    return c, app, owner, ids, emails, fw, v, a


async def save(c, a, v, low=False):
    qs = v["snapshot"]["dimensions"][0]["questions"]
    return await ok(
        c,
        "PUT",
        f"/assessments/{a['id']}/answers",
        {
            "items": [
                {
                    "question_id": q["id"],
                    "value": ("0" if low else "1")
                    if q["answer_type"] == "rubric"
                    else ("false" if low else "true"),
                }
                for q in qs
            ]
        },
        a["revision"],
    )


@pytest.mark.integration
@integration
async def test_two_departments_review_versions_evidence_and_retries(identity):
    c, app, owner, ids, emails, fw, v, a = await fixture(identity)
    assert (
        await write(c, "POST", f"/assessments/{a['id']}/submit", {}, a["revision"])
    ).status_code == 422
    assert (await write(c, "POST", f"/frameworks/{fw['id']}/publish", {}, 1)).status_code == 412
    filled = await save(c, a, v)
    a = filled["assessment"]
    assert Decimal(a["overall_score"]) == Decimal("87.5")
    q = v["snapshot"]["dimensions"][0]["questions"][0]
    attachment = await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/evidence",
        dict(
            question_id=q["id"],
            file_name="minutes.txt",
            content_base64=base64.b64encode(b"Approved process minutes").decode(),
        ),
        a["revision"],
    )
    download = await c.get(f"/api/v1/assessment/assessments/{a['id']}/evidence/{attachment['id']}")
    assert download.status_code == 409
    preview = await c.get(
        f"/api/v1/assessment/assessments/{a['id']}/evidence/{attachment['id']}/preview"
    )
    assert preview.json()["note"] == "Approved process minutes"
    a = (await c.get(f"/api/v1/assessment/assessments/{a['id']}")).json()["assessment"]
    key = str(uuid4())
    r = await write(c, "POST", f"/assessments/{a['id']}/submit", {}, a["revision"], key)
    assert r.status_code == 200, r.text
    replay = await write(c, "POST", f"/assessments/{a['id']}/submit", {}, a["revision"], key)
    assert replay.json() == r.json()
    assert (
        await write(
            c, "POST", f"/assessments/{a['id']}/submit", {"note": "different"}, a["revision"], key
        )
    ).status_code == 409
    a = r.json()
    assert (
        await write(
            c,
            "POST",
            f"/assessments/{a['id']}/review",
            {"action": "complete", "note": "self"},
            a["revision"],
        )
    ).status_code == 403
    c.cookies.clear()
    await login(c, emails, "pm")
    started = await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/review",
        {"action": "start", "note": "Review begun"},
        a["revision"],
    )
    await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/evidence/{attachment['id']}/release",
        {"note": "Reviewed text in quarantine"},
        started["revision"],
    )
    started = (await c.get(f"/api/v1/assessment/assessments/{a['id']}")).json()["assessment"]
    download = await c.get(f"/api/v1/assessment/assessments/{a['id']}/evidence/{attachment['id']}")
    assert download.content == b"Approved process minutes"
    complete = await ok(
        c,
        "POST",
        f"/assessments/{a['id']}/review",
        {
            "action": "complete",
            "note": "Evidence reviewed",
            "adjustments": [
                {
                    "answer_id": next(
                        answer["id"]
                        for answer in filled["answers"]
                        if answer["question_id"] == q["id"]
                    ),
                    "reviewer_score": "0",
                    "reviewer_note": "Not demonstrated",
                }
            ],
        },
        started["revision"],
    )
    assert complete["status"] == "completed" and Decimal(complete["overall_score"]) == 75
    history = (await c.get(f"/api/v1/assessment/assessments/{a['id']}/events")).json()
    assert any(e["event"] == "score_adjusted" and e["details"]["before"] for e in history)
    c.cookies.clear()
    await login(c, emails, org=ids["a"])
    dep2 = await create(c, "departments", name="Operations")
    b = await ok(
        c,
        "POST",
        "/assessments",
        dict(
            name="Operations assessment",
            framework_version_id=v["id"],
            department_id=dep2["id"],
            assigned_to=str(ids["admin"]),
            reviewer_id=str(ids["pm"]),
        ),
    )
    second = await save(c, b, v, True)
    b = second["assessment"]
    b = await ok(c, "POST", f"/assessments/{b['id']}/submit", {}, b["revision"])
    c.cookies.clear()
    await login(c, emails, "pm")
    # Same-tenant answer outside the currently authorized workflow cannot be adjusted.
    bad = await write(
        c,
        "POST",
        f"/assessments/{b['id']}/review",
        {
            "action": "complete",
            "note": "Invalid target",
            "adjustments": [
                {
                    "answer_id": next(
                        answer["id"]
                        for answer in filled["answers"]
                        if answer["question_id"] == q["id"]
                    ),
                    "reviewer_score": "50",
                    "reviewer_note": "wrong assessment",
                }
            ],
        },
        b["revision"],
    )
    assert bad.status_code == 422, bad.text
    b = await ok(
        c,
        "POST",
        f"/assessments/{b['id']}/review",
        {"action": "return", "note": "Add supporting context"},
        b["revision"],
    )
    c.cookies.clear()
    await login(c, emails, org=ids["a"])
    b = (await save(c, b, v, True))["assessment"]
    b = await ok(c, "POST", f"/assessments/{b['id']}/submit", {}, b["revision"])
    c.cookies.clear()
    await login(c, emails, "pm")
    b = await ok(
        c,
        "POST",
        f"/assessments/{b['id']}/review",
        {"action": "complete", "note": "Reviewed"},
        b["revision"],
    )
    assert Decimal(b["overall_score"]) == 0
    c.cookies.clear()
    await login(c, emails, org=ids["a"])
    changed = definition()
    changed["name"] = "Revised framework"
    fw = await ok(c, "PUT", f"/frameworks/{fw['id']}", changed, 2)
    new = await ok(c, "POST", f"/frameworks/{fw['id']}/publish", {}, fw["revision"])
    assert new["version"] == 2 and new["id"] != v["id"]
    old = (await c.get(f"/api/v1/assessment/assessments/{a['id']}")).json()
    assert (
        old["snapshot"]["name"] == "Governance fixture"
        and Decimal(old["assessment"]["overall_score"]) == 75
    )
    cohort = (
        await c.get("/api/v1/assessment/assessments", params={"framework_version_id": v["id"]})
    ).json()
    assert {r["department_id"] for r in cohort} == {a["department_id"], b["department_id"]}
    await ok(c, "POST", "/access", dict(user_id=str(ids["viewer"]), assessment_id=a["id"]))
    c.cookies.clear()
    await login(c, emails, "viewer")
    limited = (await c.get(f"/api/v1/assessment/assessments/{a['id']}")).json()
    assert limited["assessment"]["status"] == "completed" and limited["answers"] == []
    assert (await c.get(f"/api/v1/assessment/assessments/{a['id']}/evidence")).status_code == 403
    assert (
        await write(
            c,
            "POST",
            f"/assessments/{a['id']}/review",
            {"action": "complete", "note": "viewer"},
            complete["revision"],
        )
    ).status_code == 403


@pytest.mark.integration
@integration
async def test_tenants_rls_immutable_and_invalid_input(identity):
    c, app, owner, ids, emails, fw, v, a = await fixture(identity)
    # App role without tenant context sees no rows; wrong organization cannot see UUIDs.
    async with app.state.engine.begin() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count()).select_from(
                    __import__("ppm_api.assessment_tables", fromlist=["frameworks"]).frameworks
                )
            )
            == 0
        )
        await context(conn, ids["other"], ids["b"], "Admin")
        assert (
            await conn.scalar(
                sa.text("SELECT count(*) FROM ppm_frameworks WHERE id=:id"), {"id": UUID(fw["id"])}
            )
            == 0
        )
    for table, _id in [("ppm_framework_versions", v["id"]), ("ppm_assessment_events", None)]:
        with pytest.raises(DBAPIError):
            async with app.state.engine.begin() as conn:
                await context(conn, ids["admin"], ids["a"], "Admin")
                await conn.execute(sa.text(f"UPDATE {table} SET created_at=created_at"))
    bad = await write(
        c,
        "POST",
        "/assessments",
        dict(
            name="bad",
            framework_version_id=v["id"],
            assigned_to=str(ids["viewer"]),
            reviewer_id=str(ids["pm"]),
        ),
    )
    assert bad.status_code == 422
    q = v["snapshot"]["dimensions"][0]["questions"][0]
    for question_id, value in [(q["id"], "77"), (str(uuid4()), "1")]:
        r = await write(
            c,
            "PUT",
            f"/assessments/{a['id']}/answers",
            {"items": [{"question_id": question_id, "value": value}]},
            a["revision"],
        )
        assert r.status_code == 422, r.text
    r = await write(
        c,
        "POST",
        f"/assessments/{a['id']}/evidence",
        dict(
            question_id=q["id"],
            file_name="bad.txt",
            content_base64=base64.b64encode(b"<script>alert(1)</script>").decode(),
        ),
        a["revision"],
    )
    assert r.status_code == 422
    assert (await c.post("/api/v1/assessment/frameworks", json=definition())).status_code == 403
    # Optimistic concurrency: the second edit cannot silently overwrite the first.
    updated = await ok(c, "PUT", f"/frameworks/{fw['id']}", definition(), 2)
    assert (await write(c, "PUT", f"/frameworks/{fw['id']}", definition(), 2)).status_code == 412
    # Delegated PM can edit draft but cannot publish.
    await ok(c, "POST", "/access", dict(user_id=str(ids["pm"]), framework_id=fw["id"]))
    c.cookies.clear()
    await login(c, emails, "pm")
    updated = await ok(c, "PUT", f"/frameworks/{fw['id']}", definition(), updated["revision"])
    assert (
        await write(c, "POST", f"/frameworks/{fw['id']}/publish", {}, updated["revision"])
    ).status_code == 403
    c.cookies.clear()
    await login(c, emails, "other")
    assert (await c.get(f"/api/v1/assessment/assessments/{a['id']}")).status_code == 404
    assert (await c.get(f"/api/v1/assessment/frameworks/{fw['id']}/versions")).status_code == 404


@pytest.mark.integration
@integration
async def test_examples_publish_and_text_completeness(identity):
    c, app, owner, ids, emails, _, _ = await setup(identity)
    examples = await ok(c, "POST", "/seed-examples", {})
    repeated = await ok(c, "POST", "/seed-examples", {})
    assert len(examples) == 4 and {x["id"] for x in examples} == {x["id"] for x in repeated}
    for fw in examples:
        assert "Example" in fw["name"]
        v = await ok(c, "POST", f"/frameworks/{fw['id']}/publish", {}, fw["revision"])
        assert v["version"] == 1
    data = definition()
    data["dimensions"][0]["questions"].append(
        {
            "id": str(uuid4()),
            "name": "Required context",
            "text": "Explain the practice",
            "answer_type": "text",
            "weight": "1",
            "required": True,
            "rubric_levels": [],
        }
    )
    fw = await ok(c, "POST", "/frameworks", data)
    v = await ok(c, "POST", f"/frameworks/{fw['id']}/publish", {}, fw["revision"])
    a = await ok(
        c,
        "POST",
        "/assessments",
        dict(
            name="Text acceptance",
            framework_version_id=v["id"],
            assigned_to=str(ids["admin"]),
            reviewer_id=str(ids["pm"]),
        ),
    )
    qs = data["dimensions"][0]["questions"]
    detail = await ok(
        c,
        "PUT",
        f"/assessments/{a['id']}/answers",
        {
            "items": [
                {"question_id": qs[0]["id"], "value": "1"},
                {"question_id": qs[1]["id"], "value": "true"},
            ]
        },
        a["revision"],
    )
    a = detail["assessment"]
    assert (
        await write(c, "POST", f"/assessments/{a['id']}/submit", {}, a["revision"])
    ).status_code == 422
    detail = await ok(
        c,
        "PUT",
        f"/assessments/{a['id']}/answers",
        {"items": [{"question_id": qs[2]["id"], "value": "Documented process"}]},
        a["revision"],
    )
    a = detail["assessment"]
    assert Decimal(a["overall_score"]) == Decimal("87.5")
    assert Decimal(a["dimension_scores"][0]["coverage_percent"]) == 100
    await ok(c, "POST", f"/assessments/{a['id']}/submit", {}, a["revision"])
    invalid = definition()
    invalid["dimensions"][0]["questions"][0]["rubric_levels"] = [{"level": 0, "label": "Only"}]
    bad = await ok(c, "POST", "/frameworks", invalid)
    assert (
        await write(c, "POST", f"/frameworks/{bad['id']}/publish", {}, bad["revision"])
    ).status_code == 422
