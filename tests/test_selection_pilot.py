"""Real app-role pilot persistence and access; all provider responses are synthetic."""

import json
import os
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api import agent_task_tables as T
from ppm_api import ai_tables as A
from ppm_api.ai_provider import GEMINI_COMPLETION_MODEL
from ppm_api.identity import context, now
from ppm_api.identity_tables import memberships
from ppm_api.model_contracts import ModelFailure, ModelResult, ModelUsage
from ppm_api.model_registry import ModelPolicy
from ppm_api.selection_protocol import PROMPT, protocol
from ppm_api.selection_tables import pilots
from pydantic import SecretStr
from test_agent_v2_runtime import configure
from test_agents import work
from test_identity import identity as identity
from test_identity import login, send

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires isolated ppm_test"
    ),
]


async def setup(identity, monkeypatch, tmp_path):
    c, app, owner, ids, project, _, _ = await configure(
        identity, monkeypatch, tmp_path, True, "groq"
    )
    settings = app.state.settings
    settings.ai_guided_enabled = True
    settings.ai_api_key = SecretStr("synthetic-not-real")
    settings.ai_gemini_daily_call_limit = 50
    policy = ModelPolicy.model_validate_json(settings.ai_model_registry_path.read_bytes())
    profile = policy.profiles[0]
    profile.provider = "gemini"
    profile.model = GEMINI_COMPLETION_MODEL
    profile.assigned_task_classes = ["financial_interpretation"]
    profile.qualified_task_classes = []
    profile.benchmark_only = True
    profile.guided_selection_enabled = True
    profile.requests_per_minute = 1
    profile.requests_per_day = profile.tenant_requests_per_day = 50
    profile.max_output_tokens = 128
    profile.tokens_per_minute = 8000
    settings.ai_model_registry_path.write_text(policy.model_dump_json(), encoding="utf-8")
    settings.ai_egress_policy_path.write_text(
        json.dumps({str(ids["a"]): {project["id"]: {"gemini": ["metric:usage"]}}}), encoding="utf-8"
    )
    monkeypatch.setattr("ppm_api.model_router.ai_provider.gemini_block_reason", lambda _: None)
    async with owner.begin() as conn:
        await conn.execute(
            T.scopes.update()
            .where(T.scopes.c.id == profile.quota_scope)
            .values(
                provider_id="gemini",
                allowed_models=[profile.model],
                policy_hash=policy.policy_hash,
                requests_per_minute=1,
                requests_per_day=50,
                tenant_requests_per_day=50,
                tokens_per_minute=8000,
            )
        )
        await conn.execute(
            memberships.update()
            .where(memberships.c.organization_id == ids["a"], memberships.c.user_id == ids["pm"])
            .values(role="Admin")
        )
        for actor in (ids["admin"], ids["pm"]):
            await conn.execute(
                T.guided_grants.insert().values(
                    organization_id=ids["a"],
                    user_id=actor,
                    project_id=UUID(project["id"]),
                    enabled=True,
                    created_at=now(),
                )
            )
    return c, app, owner, ids, project, policy


async def post(c, path, body, rev=None, key=None):
    return await send(
        c,
        "POST",
        "/agents/selection-pilots" + path,
        json=body,
        headers={"idempotency-key": key or str(uuid4()), **({"if-match": str(rev)} if rev else {})},
    )


def review_body(pilot):
    return dict(
        corpus_sha256=pilot["protocol"]["corpus_sha256"],
        strategy_sha256=pilot["protocol"]["strategy_sha256"],
        reviewed_case_ids=[c["id"] for c in pilot["cases"]],
        human_reviewed=True,
        reason="Human approval is simulated only inside this isolated integration test.",
    )


async def approved(identity, monkeypatch, tmp_path):
    c, app, owner, ids, project, policy = await setup(identity, monkeypatch, tmp_path)
    response = await post(c, "", {"project_id": project["id"]})
    assert response.status_code == 201, response.text
    item = response.json()
    assert item["summary"]["state"] == "awaiting_label_review"
    assert (await post(c, f"/{item['id']}/label-review", review_body(item), 1)).status_code == 403
    assert (await post(c, f"/{item['id']}/cases/f01", {}, 1)).status_code == 409
    await login(c, identity[4], "pm", ids["a"])
    response = await post(c, f"/{item['id']}/label-review", review_body(item), 1)
    assert response.status_code == 200, response.text
    item = response.json()
    assert item["binding_current"] and item["revision"] == 2
    await login(c, identity[4], "admin", ids["a"])
    return c, app, owner, ids, project, policy, item


async def auto_approved(identity, monkeypatch, tmp_path):
    c, app, owner, ids, project, policy = await setup(identity, monkeypatch, tmp_path)
    item = (await post(c, "", {"project_id": project["id"]})).json()
    app.state.settings.app_env = "local"  # In-memory only; DB remains guarded ppm_test.
    app.state.settings.ai_fixture_automated_pilots = [UUID(item["id"])]
    body = {k: item["protocol"][k] for k in ("corpus_sha256", "strategy_sha256")} | {
        "synthetic_only": True
    }
    response = await post(c, f"/{item['id']}/automated-review", body, item["revision"])
    assert response.status_code == 200, response.text
    item = response.json()
    assert item["review_kind"] == "automated_rule_audit" and item["human_reviewed"] is False
    assert item["review"]["human_reviewed"] is False and item["binding_current"]
    return c, app, owner, ids, project, policy, item


@pytest.mark.parametrize("review_mode", ["human", "automated"])
async def test_twelve_case_pilot_uses_normal_jobs_quota_and_never_promotes(
    identity, monkeypatch, tmp_path, review_mode
):
    c, app, owner, ids, project, policy, item = await (
        approved(identity, monkeypatch, tmp_path)
        if review_mode == "human"
        else auto_approved(identity, monkeypatch, tmp_path)
    )
    seen = []
    expected = iter(c["expected"] for c in protocol()["cases"])

    async def execute(self, request):
        self.permit(request)
        from ppm_api.guided_review import check_request

        check_request(request)
        assert request.system == PROMPT and request.max_output_tokens == 128
        assert request.timeout == request.permit.timeout_seconds == 22
        if not seen:
            async with app.state.engine.begin() as conn:
                await context(conn, ids["admin"], ids["a"], "Admin")
                call = (
                    (
                        await conn.execute(
                            sa.select(A.calls).where(A.calls.c.id == request.permit.attempt_id)
                        )
                    )
                    .mappings()
                    .one()
                )
                task = (
                    (await conn.execute(sa.select(T.tasks).where(T.tasks.c.id == call["task_id"])))
                    .mappings()
                    .one()
                )
                profile = policy.profiles[0]
                denied = await conn.scalar(
                    sa.text(
                        "SELECT public.ppm_model_admit"
                        "(:rid,:tid,:sid,:mid,:phash,:lease,:aid,10,128,60)"
                    ),
                    dict(
                        rid=call["run_id"],
                        tid=task["id"],
                        sid=profile.quota_scope,
                        mid=profile.model,
                        phash=policy.policy_hash,
                        lease=task["lease_token"],
                        aid=uuid4(),
                    ),
                )
                assert denied["code"] == "AUTHORITY_REVOKED"
        assert project["id"] not in request.payload and request.categories == ("metric:usage",)
        seen.append(request)
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="gemini",
            model_id=GEMINI_COMPLETION_MODEL,
            text=json.dumps({"choices": next(expected)}),
            completion="complete",
            latency_ms=100,
            usage=ModelUsage(input_tokens=80, output_tokens=8, source="reported"),
        )

    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", execute)
    assert (await post(c, f"/{item['id']}/cases/f07", {}, item["revision"])).status_code == 409
    generic = await send(
        c,
        "POST",
        "/agents/runs",
        headers={"idempotency-key": str(uuid4())},
        json=dict(
            project_id=project["id"],
            runtime_version="v2",
            analysis_mode="guided",
            requested_agents=["financial"],
            guided_pilot_id=item["id"],
            guided_case_id="f01",
        ),
    )
    assert generic.status_code == 403
    for case in protocol()["cases"]:
        response = await post(c, f"/{item['id']}/cases/{case['id']}", {}, item["revision"])
        assert response.status_code == 202, response.text
        item = response.json()
        run_id = next(r["run_id"] for r in item["cases"] if r["id"] == case["id"])
        output = (await c.get("/api/v1/agents/runs/" + run_id)).json()
        output, _ = await work(c, app, owner, ids, output)
        assert output["guided_review"]["status"] == "api_selected", output
        duplicate = await post(c, f"/{item['id']}/cases/{case['id']}", {}, item["revision"])
        assert duplicate.status_code == 202 and len(seen) == int(case["id"][1:])
        item = duplicate.json()
        assert item["cases"][int(case["id"][1:]) - 1]["correct"]
        if case["id"] == "f01":
            assert (
                await post(c, f"/{item['id']}/cases/f02", {}, item["revision"])
            ).status_code == 429
        # Time shift only disposable SQL fixtures; all attempts remain counted in the daily ledger.
        async with owner.begin() as conn:
            assert await conn.scalar(sa.text("SELECT current_database()")) == "ppm_test"
            await conn.execute(
                T.quotas.update()
                .where(T.quotas.c.run_id == UUID(run_id))
                .values(admitted_at=now() - timedelta(seconds=62))
            )
            await conn.execute(
                A.calls.update()
                .where(A.calls.c.run_id == UUID(run_id))
                .values(started_at=now() - timedelta(seconds=62))
            )
    assert (
        item["summary"]["state"] == "fixture_passed" and item["summary"]["held_out_measured"] == 6
    )
    assert (
        item["summary"]["at17"] == "BLOCKED" and not item["summary"]["semantic_qualified_classes"]
    )
    assert item["human_reviewed"] is (review_mode == "human")
    assert item["summary"]["independent_human_review"] is (review_mode == "human")
    assert (
        ModelPolicy.model_validate_json(app.state.settings.ai_model_registry_path.read_bytes())
        .profiles[0]
        .benchmark_only
    )
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(T.quotas)
                .where(T.quotas.c.quota_scope_id == policy.profiles[0].quota_scope)
            )
            == 12
        )


@pytest.mark.parametrize(
    "failure", ["unknown", "malformed", "reviewer_revoked", "reviewer_demoted", "policy_changed"]
)
async def test_unavailable_or_stale_pilot_cannot_measure_or_count_fallback(
    identity, monkeypatch, tmp_path, failure
):
    c, app, owner, ids, project, policy, item = await approved(identity, monkeypatch, tmp_path)
    seen = []

    async def execute(self, request):
        seen.append(request)
        if failure == "unknown":
            raise ModelFailure("TIMEOUT", "unknown")
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="gemini",
            model_id=GEMINI_COMPLETION_MODEL,
            completion="complete",
            text='{"choices":["foreign-source"]}',
            usage=ModelUsage(source="unknown"),
        )

    clock = iter([100.0, 122.0])
    monkeypatch.setattr("ppm_api.agent_runtime.perf_counter", lambda: next(clock))
    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", execute)
    if failure == "policy_changed":
        policy.profiles[0].enabled = False
        app.state.settings.ai_model_registry_path.write_text(policy.model_dump_json())
        assert (await post(c, f"/{item['id']}/cases/f01", {}, item["revision"])).status_code == 409
        assert not seen
        return
    response = await post(c, f"/{item['id']}/cases/f01", {}, item["revision"])
    assert response.status_code == 202, response.text
    if failure == "reviewer_revoked":
        async with owner.begin() as conn:
            await conn.execute(
                T.guided_grants.update()
                .where(T.guided_grants.c.user_id == ids["pm"])
                .values(enabled=False)
            )
    if failure == "reviewer_demoted":
        async with owner.begin() as conn:
            await conn.execute(
                memberships.update()
                .where(
                    memberships.c.organization_id == ids["a"], memberships.c.user_id == ids["pm"]
                )
                .values(role="Viewer")
            )
    run_id = response.json()["cases"][0]["run_id"]
    output = (await c.get("/api/v1/agents/runs/" + run_id)).json()
    await work(c, app, owner, ids, output)
    item = (await c.get("/api/v1/agents/selection-pilots/" + item["id"])).json()
    assert item["summary"]["measured_cases"] == 0
    assert item["summary"]["state"] != "fixture_passed"
    if failure == "unknown":
        case = item["cases"][0]
        assert case["elapsed_ms"] == case["latency_ms"] == 22000
        assert case["timing_kind"] == "unavailable_attempt"
        assert item["summary"]["p95_ms"] is None
        async with owner.begin() as conn:
            call = (
                (await conn.execute(sa.select(A.calls).where(A.calls.c.run_id == UUID(run_id))))
                .mappings()
                .one()
            )
            quota = (
                (await conn.execute(sa.select(T.quotas).where(T.quotas.c.attempt_id == call["id"])))
                .mappings()
                .one()
            )
            assert call["status"] == quota["outcome"] == "unknown"
            assert call["input_tokens"] is None and call["output_tokens"] is None
            assert call["usage_source"] == "unknown"
            assert call["charged_usd"] == 0
            # Reproduce a legacy zero only in the disposable test database.
            await conn.execute(
                A.calls.update().where(A.calls.c.id == call["id"]).values(latency_ms=0)
            )
        legacy = (await c.get("/api/v1/agents/selection-pilots/" + item["id"])).json()
        assert legacy["cases"][0]["elapsed_ms"] is None
        assert legacy["cases"][0]["timing_kind"] == "not_recorded"
    assert len(seen) == (0 if failure in {"reviewer_revoked", "reviewer_demoted"} else 1)
    assert (await post(c, f"/{item['id']}/cases/f02", {}, item["revision"])).status_code == 409


async def test_tenant_roles_grant_and_approval_binding_are_enforced(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, policy = await setup(identity, monkeypatch, tmp_path)
    key = str(uuid4())
    item = (await post(c, "", {"project_id": project["id"]}, key=key)).json()
    assert (await post(c, "", {"project_id": project["id"]}, key=key)).json()["id"] == item["id"]
    await login(c, identity[4], "pm", ids["a"])
    bad = review_body(item) | {"reviewed_case_ids": ["f01"] * 12}
    assert (await post(c, f"/{item['id']}/label-review", bad, 1)).status_code == 409
    assert (await post(c, f"/{item['id']}/label-review", review_body(item), 99)).status_code == 412
    await login(c, identity[4], "viewer", ids["a"])
    assert (await c.get("/api/v1/agents/selection-pilots/" + item["id"])).status_code == 403


async def test_automated_review_is_local_one_pilot_bound_and_cannot_claim_human(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, _ = await setup(identity, monkeypatch, tmp_path)
    item = (await post(c, "", {"project_id": project["id"]})).json()
    other = (await post(c, "", {"project_id": project["id"]})).json()
    path = f"/{item['id']}/automated-review"
    body = {k: item["protocol"][k] for k in ("corpus_sha256", "strategy_sha256")} | {
        "synthetic_only": True
    }
    assert (await post(c, path, body, 1)).status_code == 403
    app.state.settings.ai_fixture_automated_pilots = [UUID(item["id"])]
    assert (await post(c, path, body, 1)).status_code == 403  # Test environment is not local.
    app.state.settings.app_env = "local"
    assert (await post(c, f"/{other['id']}/automated-review", body, 1)).status_code == 403
    assert (await post(c, path, body | {"corpus_sha256": "0" * 64}, 1)).status_code == 409
    assert (await post(c, path, body, 99)).status_code == 412
    assert (await post(c, path, body | {"human_reviewed": True}, 1)).status_code == 422
    assert (await post(c, path, body | {"synthetic_only": False}, 1)).status_code == 422
    response = await post(c, path, body, 1)
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["review_kind"] == "automated_rule_audit" and not result["human_reviewed"]
    assert result["review"]["actor_id"] == str(ids["admin"])  # Same actor; never independent human.
    assert (await post(c, path, body, 1)).json()["revision"] == result["revision"]
    assert (
        await post(c, f"/{item['id']}/label-review", review_body(item), result["revision"])
    ).status_code == 409
    app.state.settings.ai_fixture_automated_pilots = []
    reloaded = (await c.get("/api/v1/agents/selection-pilots/" + item["id"])).json()
    assert not reloaded["binding_current"] and reloaded["summary"]["state"] == "binding_changed"
    assert (await post(c, f"/{item['id']}/cases/f01", {}, result["revision"])).status_code == 409
    await login(c, identity[4], "viewer", ids["a"])
    assert (await post(c, path, body, 1)).status_code == 403
    await login(c, identity[4], "other", ids["b"])
    assert (await post(c, path, body, 1)).status_code == 404


async def test_revoked_automated_authorization_stops_queued_worker_without_call(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, _, item = await auto_approved(identity, monkeypatch, tmp_path)
    response = await post(c, f"/{item['id']}/cases/f01", {}, item["revision"])
    assert response.status_code == 202, response.text
    run_id = response.json()["cases"][0]["run_id"]
    seen = []

    async def forbidden(*args):
        seen.append(True)
        raise AssertionError("Revoked mode must never reach the adapter")

    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", forbidden)
    app.state.settings.ai_fixture_automated_pilots = []
    output = (await c.get("/api/v1/agents/runs/" + run_id)).json()
    output, _ = await work(c, app, owner, ids, output)
    assert (
        output["run"]["status"] == "failed" and output["run"]["diagnostic"] == "AUTHORITY_REVOKED"
    )
    assert not seen
    report = (await c.get("/api/v1/agents/selection-pilots/" + item["id"])).json()
    assert report["summary"]["measured_cases"] == 0 and not report["human_reviewed"]
    await login(c, identity[4], "other", ids["b"])
    assert (await c.get("/api/v1/agents/selection-pilots/" + item["id"])).status_code == 404
    async with app.state.engine.begin() as conn:
        await context(conn, ids["other"], ids["b"], "Admin")
        assert not (
            await conn.execute(sa.select(pilots).where(pilots.c.id == UUID(item["id"])))
        ).first()
    await login(c, identity[4], "admin", ids["a"])
    async with owner.begin() as conn:
        await conn.execute(
            T.guided_grants.update()
            .where(T.guided_grants.c.user_id == ids["admin"])
            .values(enabled=False)
        )
    assert (await c.get("/api/v1/agents/selection-pilots/" + item["id"])).status_code == 403
