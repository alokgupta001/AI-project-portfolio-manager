"""Explicit guided grants keep PM/Viewer roles and revalidate source authority."""

import json
import os
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api import agent_task_tables as T
from ppm_api import ai_tables as A
from ppm_api.identity import context, now
from ppm_api.identity_tables import memberships
from ppm_api.model_contracts import ModelResult, ModelUsage
from ppm_api.model_registry import ModelPolicy
from ppm_api.ppm_tables import TABLES
from sqlalchemy.exc import DBAPIError
from test_agent_v2_runtime import configure
from test_agents import start, work
from test_delivery import create
from test_identity import identity as identity
from test_identity import login, send

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires isolated ppm_test"
    ),
]


@pytest.mark.parametrize("role", ["pm", "viewer"])
async def test_guided_grant_preserves_role_and_checks_every_boundary(
    identity, monkeypatch, tmp_path, role
):
    c, app, owner, ids, project, accepted, _ = await configure(
        identity, monkeypatch, tmp_path, True, "groq"
    )
    emails = identity[4]
    settings = app.state.settings
    settings.ai_guided_enabled = True
    policy = ModelPolicy.model_validate_json(settings.ai_model_registry_path.read_bytes())
    profile = policy.profiles[0]
    profile.benchmark_only = True
    profile.qualified_task_classes = []
    profile.assigned_task_classes = ["executive_synthesis"]
    profile.guided_selection_enabled = True
    settings.ai_model_registry_path.write_text(policy.model_dump_json())
    settings.ai_egress_policy_path.write_text(
        json.dumps(
            {
                str(ids["a"]): {
                    project["id"]: {
                        "groq": ["metric:critical", "metric:risk", "metric:health", "metric:usage"]
                    }
                }
            }
        )
    )
    await create(
        c,
        "milestones",
        project_id=project["id"],
        critical=True,
        due_date=(now().date() - timedelta(days=1)).isoformat(),
    )
    source_grant = await create(
        c, "grants", user_id=str(ids[role]), project_id=project["id"], access="read"
    )
    assert (
        await send(
            c,
            "PATCH",
            "/ai/budget",
            headers={"if-match": "1"},
            json={"limit_usd": "0", "concurrency": 1},
        )
    ).status_code == 200
    async with owner.begin() as conn:
        await conn.execute(
            T.scopes.update()
            .where(T.scopes.c.id == profile.quota_scope)
            .values(policy_hash=policy.policy_hash)
        )
    await login(c, emails, role, ids["a"])
    body = dict(runtime_version="v2", analysis_mode="guided", requested_agents=["executive"])
    assert (await start(c, project, **body)).status_code == 403
    async with owner.begin() as conn:
        await conn.execute(
            T.guided_grants.insert().values(
                organization_id=ids["a"],
                user_id=ids[role],
                project_id=UUID(project["id"]),
                enabled=True,
                created_at=now(),
            )
        )
    defs = (await c.get("/api/v1/agents/definitions")).json()
    assert defs[0]["guided_project_ids"] == [project["id"]]
    assert (
        await start(c, project, runtime_version="v2", analysis_mode="metrics")
    ).status_code == 403
    assert (
        await start(c, project, **body, version_ids=[accepted["version_id"]])
    ).status_code == 403
    assert (await start(c, {"id": str(uuid4())}, **body)).status_code == 403
    assert (await c.get("/api/v1/ai/operations")).status_code == 403
    assert (
        await send(
            c,
            "PATCH",
            "/ai/budget",
            headers={"if-match": "2"},
            json={"limit_usd": "0", "concurrency": 4},
        )
    ).status_code == 403
    seen = []

    async def execute(self, request):
        self.permit(request)
        seen.append(request)
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="groq",
            model_id=profile.model,
            completion="complete",
            text='{"choices":["o1"]}',
            usage=ModelUsage(input_tokens=10, output_tokens=8, source="reported"),
        )

    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", execute)
    response = await start(c, project, **body)
    assert response.status_code == 202, response.text
    output, _ = await work(c, app, owner, ids | {"admin": ids[role]}, response.json())
    assert output["guided_review"]["status"] == "api_selected", output
    assert len(seen) == 1
    expected_role = "Project Manager" if role == "pm" else "Viewer"
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(memberships.c.role).where(
                    memberships.c.organization_id == ids["a"], memberships.c.user_id == ids[role]
                )
            )
            == expected_role
        )
    async with app.state.engine.begin() as conn:
        await context(conn, ids[role], ids["a"], expected_role)
        assert (
            await conn.execute(
                A.budgets.update()
                .where(A.budgets.c.organization_id == ids["a"])
                .values(concurrency=4)
            )
        ).rowcount == 0
    with pytest.raises(DBAPIError):
        async with app.state.engine.begin() as conn:
            await context(conn, ids[role], ids["a"], expected_role)
            await conn.execute(T.guided_grants.update().values(enabled=False))
    queued = await start(c, project, **body)
    assert queued.status_code == 202, queued.text
    cancelled = await send(
        c,
        "POST",
        "/ai/runs/" + queued.json()["run"]["id"] + "/cancel",
        headers={"if-match": str(queued.json()["run"]["revision"])},
        json={},
    )
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    queued = await start(c, project, **body)
    assert queued.status_code == 202, queued.text
    async with owner.begin() as conn:
        await conn.execute(
            T.guided_grants.update()
            .where(T.guided_grants.c.user_id == ids[role])
            .values(enabled=False)
        )
    revoked, _ = await work(c, app, owner, ids | {"admin": ids[role]}, queued.json())
    assert revoked["run"]["status"] == "cancelled" and len(seen) == 1
    assert (await start(c, project, **body)).status_code == 403
    async with owner.begin() as conn:
        await conn.execute(
            T.guided_grants.update()
            .where(T.guided_grants.c.user_id == ids[role])
            .values(enabled=True)
        )
        await conn.execute(
            TABLES["grants"]
            .update()
            .where(TABLES["grants"].c.id == UUID(source_grant["id"]))
            .values(archived=True)
        )
    assert (await start(c, project, **body)).status_code == 403
