"""Real tenant authority and shared quotas; synthetic model responses, no external calls."""

import json
import os
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from ppm_api import agent_task_tables as T
from ppm_api import guided_review as G
from ppm_api.identity import now
from ppm_api.model_contracts import ModelFailure, ModelResult, ModelUsage
from ppm_api.model_registry import ModelPolicy
from ppm_api.model_router import RouteRequirements, candidates
from test_agent_v2_runtime import configure
from test_agents import start, work
from test_delivery import create
from test_identity import identity as identity

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires isolated ppm_test"
    ),
]


@pytest.mark.parametrize("case", ["success", "malformed", "quota", "unknown", "disabled"])
async def test_guided_selection_is_optional_single_call_and_never_qualifies_interpretation(
    identity, monkeypatch, tmp_path, case
):
    c, app, owner, ids, project, accepted, _ = await configure(
        identity, monkeypatch, tmp_path, True, "groq"
    )
    settings = app.state.settings
    settings.ai_guided_enabled = case != "disabled"
    policy = ModelPolicy.model_validate_json(settings.ai_model_registry_path.read_bytes())
    profile = policy.profiles[0]
    profile.benchmark_only = True
    profile.qualified_task_classes = []
    profile.assigned_task_classes = ["executive_synthesis"]
    profile.guided_selection_enabled = True
    settings.ai_model_registry_path.write_text(policy.model_dump_json(), encoding="utf-8")
    settings.ai_egress_policy_path.write_text(
        json.dumps(
            {
                str(ids["a"]): {
                    project["id"]: {
                        "groq": ["metric:risk", "metric:health", "metric:critical", "metric:usage"]
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    async with owner.begin() as conn:
        await conn.execute(
            T.scopes.update()
            .where(T.scopes.c.id == profile.quota_scope)
            .values(policy_hash=policy.policy_hash)
        )
    assert not candidates(
        policy,
        RouteRequirements(ids["a"], UUID(project["id"]), "executive_synthesis", 10),
        settings,
    )[0]
    await create(
        c,
        "milestones",
        project_id=project["id"],
        critical=True,
        due_date=(now().date() - timedelta(days=1)).isoformat(),
    )
    seen = []

    async def execute(self, request):
        self.permit(request)
        G.check_request(request)
        seen.append(request)
        if case == "unknown":
            raise ModelFailure("TIMEOUT", "unknown")
        wire = {"choices": ["fabricated"]} if case == "malformed" else {"choices": ["o1"]}
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="groq",
            model_id=profile.model,
            completion="complete",
            text=json.dumps(wire),
            usage=ModelUsage(input_tokens=10, output_tokens=8, source="reported"),
        )

    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", execute)
    key = str(uuid4())
    body = dict(
        runtime_version="v2",
        analysis_mode="guided",
        requested_agents=["executive"],
        version_ids=[accepted["version_id"]],
    )
    response = await start(c, project, key=key, **body)
    if case == "disabled":
        assert response.status_code == 422 and not seen
        return
    assert response.status_code == 202, response.text
    output, _ = await work(c, app, owner, ids, response.json())
    assert len(seen) == 1, output
    assert seen[0].max_output_tokens == 128
    assert "Supplier" not in seen[0].payload and "edit_plan" not in seen[0].payload
    assert output["guided_review"]["status"] == (
        "api_selected" if case in {"success", "quota"} else "rules_only"
    )
    assert output["model_quality"] == "UNVERIFIED/BLOCKED"
    assert len(output["guided_review"]["checklists"]) == 9
    assert output["guided_review"]["cards"]
    assert output["suggestions"] == []
    assert all(d["semantic_outcome"] == "not_requested" for d in output["capability_details"])
    assert output["run"]["charged_usd"] == "0.000000"
    assert (await start(c, project, key=key, **body)).json()["run"]["id"] == output["run"]["id"]
    assert len(seen) == 1
    if case == "quota":
        second = await start(c, project, **body)
        fallback, _ = await work(c, app, owner, ids, second.json())
        assert fallback["guided_review"]["status"] == "rules_only"
        assert fallback["guided_review"]["code"] == "QUOTA_EXHAUSTED"
        assert fallback["guided_review"]["cards"] and len(seen) == 1
    if case == "success":

        async def withdrawn(*args):
            return {}

        monkeypatch.setattr("ppm_api.agents.current_sources", withdrawn)
        reread = (await c.get("/api/v1/agents/runs/" + output["run"]["id"])).json()
        assert reread["guided_review"]["status"] == "rules_only"
        assert not reread["guided_review"]["cards"]
