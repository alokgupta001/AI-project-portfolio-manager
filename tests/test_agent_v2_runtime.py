"""Real app-role v2 persistence/admission with synthetic model results, never real AI."""

import asyncio
import hashlib
import json
import os
from contextlib import suppress
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api import agent_task_tables as T
from ppm_api import ai_tables as A
from ppm_api import job_tables as J
from ppm_api.ai import ai_worker
from ppm_api.identity import now
from ppm_api.model_contracts import ModelFailure, ModelResult, ModelUsage
from ppm_api.model_registry import ModelPolicy, ModelProfile
from sqlalchemy.exc import DBAPIError
from test_agents import fixture, start, work
from test_delivery import create
from test_identity import identity as identity
from test_identity import send

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.environ.get("PPM_RUN_INTEGRATION") != "1", reason="Requires isolated ppm_test"
    ),
]


async def configure(identity, monkeypatch, tmp_path, with_profile=False, provider="ollama"):
    c, app, owner, ids, emails, project, accepted = await fixture(identity, monkeypatch)
    config = app.state.settings
    config.ai_runtime_v2_enabled = True
    config.ai_ollama_enabled = True
    config.ai_local_available_memory_mb = 8192
    seen = []
    if with_profile:
        cloud = provider != "ollama"
        models = {
            "ollama": "fixture:4b",
            "groq": "openai/gpt-oss-20b",
            "openrouter": "test/pinned:free",
            "mistral": "ministral-8b-2512",
            "puter": "gpt-4.1-mini-2025-04-14",
        }
        if cloud:
            config.ai_execution_mode = "hybrid"
            config.ai_cloud_enabled = config.ai_real_calls_authorized = True
            monkeypatch.setenv("PPM_FIXTURE_CLOUD_KEY", "synthetic-not-real")
            config.ai_egress_policy_path = tmp_path / "egress.json"
            config.ai_egress_policy_path.write_text(
                json.dumps(
                    {
                        str(ids["a"]): {
                            project["id"]: {
                                provider: [
                                    "document:project",
                                    "metric:risk",
                                    "record:risks",
                                    "record:blockers",
                                ]
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
        profile = ModelProfile(
            id="synthetic",
            provider=provider,
            model=models[provider],
            enabled=True,
            billing_class="verified_free" if cloud else "local",
            quota_scope=provider + ":" + str(uuid4()),
            credential_ref="PPM_FIXTURE_CLOUD_KEY" if cloud else None,
            credential_sha256=hashlib.sha256(b"synthetic-not-real").hexdigest() if cloud else None,
            free_tier_confirmed=cloud,
            data_policy_confirmed=cloud,
            upstream_provider="fixture"
            if provider == "openrouter"
            else "openai-completion"
            if provider == "puter"
            else None,
            installed_digest="a" * 64,
            allowed_tenants=[ids["a"]],
            qualified_task_classes=["risk_extraction"],
            benchmark_only=False,
            context_tokens=8192 if cloud else 4096,
            requests_per_minute=100,
            requests_per_day=1 if cloud else 1000,
            tokens_per_minute=1000000,
        )
        policy = ModelPolicy(profiles=[profile])
        path = tmp_path / "policy.json"
        path.write_text(policy.model_dump_json(), encoding="utf-8")
        config.ai_model_registry_path = path
        async with owner.begin() as conn:
            await conn.execute(
                T.scopes.insert().values(
                    id=profile.quota_scope,
                    provider_id=profile.provider,
                    policy_hash=policy.policy_hash,
                    billing_class=profile.billing_class,
                    enabled=True,
                    allowed_tenants=[str(ids["a"])],
                    allowed_models=[profile.model],
                    concurrency_slots=1,
                    requests_per_minute=100,
                    requests_per_day=profile.requests_per_day,
                    tenant_requests_per_day=100,
                    tokens_per_minute=1000000,
                    failure_count=0,
                    revision=1,
                )
            )

        async def execute(self, request):
            seen.append(request)
            payload = json.loads(request.payload)
            alias = payload["required"][0]
            result = dict(
                section=payload["section"],
                mode="findings",
                outcome="supported",
                covered=[alias],
                findings=[
                    dict(
                        subject="s1",
                        predicate="risk_present",
                        kind="risk",
                        signal="adverse",
                        severity="medium",
                        claim="Supplier risk requires review.",
                        advice="Verify the cited evidence.",
                        epistemic="interpretation",
                        spans=[dict(e=alias, start=0, end=10)],
                    )
                ],
            )
            return ModelResult(
                attempt_id=request.permit.attempt_id,
                provider_id=profile.provider,
                model_id=profile.model,
                completion="complete",
                text=json.dumps(result),
                native_finish_reason="stop",
                usage=ModelUsage(input_tokens=11, output_tokens=13, source="reported"),
            )

        monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", execute)
    return c, app, owner, ids, project, accepted, seen


@pytest.mark.parametrize("repair", [False, True, "checkpoint"])
async def test_nine_roles_use_four_durable_admissions_and_never_hide_a_fifth(
    identity, monkeypatch, tmp_path, repair
):
    from ppm_api import agents
    from ppm_api.agent_planner import build_plan
    from ppm_api.agent_registry import BY_AGENT, DOMAIN
    from ppm_api.model_registry import digest
    from test_agent_batches import compact

    c, app, owner, ids, project, accepted, _ = await configure(
        identity, monkeypatch, tmp_path, True, "groq"
    )
    settings = app.state.settings
    policy = ModelPolicy.model_validate_json(settings.ai_model_registry_path.read_bytes())
    profile = policy.profiles[0]
    profile.qualified_task_classes = [v.task_class for v in BY_AGENT.values()]
    profile.requests_per_day = 100
    profile.context_tokens = 8192
    settings.ai_model_registry_path.write_text(policy.model_dump_json(), encoding="utf-8")
    categories = sorted({category for role in BY_AGENT.values() for category in role.categories})
    settings.ai_egress_policy_path.write_text(
        json.dumps({str(ids["a"]): {project["id"]: {"groq": categories}}}), encoding="utf-8"
    )
    async with owner.begin() as conn:
        await conn.execute(
            T.scopes.update()
            .where(T.scopes.c.id == profile.quota_scope)
            .values(policy_hash=policy.policy_hash, requests_per_day=100)
        )
    original = agents.capture

    async def synthetic_capture(p, body, period=None):
        # Keep project/tenant authorization real; replace only the captured
        # evidence seam to exercise all nine roles without real provider data.
        data = await original(p, body, period)
        sources = []
        for role in DOMAIN:
            text = "An unresolved delivery concern requires owner review."
            item = dict(
                source="group:blockers" if role == "sentiment" else "synthetic:" + role,
                kind="group"
                if role == "sentiment"
                else "metric"
                if role == "resource"
                else "document",
                category=BY_AGENT[role].categories[0],
                text=text,
                sha256=digest(text),
                version="fixture",
                location="synthetic batch",
                fresh=True,
                permitted_agents=[role],
            )
            if role == "resource":
                item["metric"] = dict(key="capacity_risk", value="1")
            sources.append(item)
        data["sources"] = sources
        data["framework"] = None
        data["hybrid_plan"] = build_plan(data, body)
        return data

    monkeypatch.setattr(agents, "capture", synthetic_capture)
    seen = []

    async def batch_execute(self, request):
        self.permit(request)
        payload = json.loads(request.payload)
        seen.append(request)
        if repair is True and len(seen) == 1:
            return ModelResult(
                attempt_id=request.permit.attempt_id,
                provider_id="groq",
                model_id=profile.model,
                completion="incomplete",
                text="{",
            )
        values = {}
        for role, item in payload.items():
            value = compact(
                role, dict(required_aliases=item["required"], basis=item.get("basis", {}))
            )
            value["cites"] = list(item["evidence"])[:2]
            if "basis" in value:
                value["basis"] = list(item["basis"])
            values[role] = value
        assert {request.task_class, *request.additional_task_classes} == {
            BY_AGENT[r].task_class for r in payload
        }
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="groq",
            model_id=profile.model,
            completion="complete",
            text=json.dumps(values),
            usage=ModelUsage(input_tokens=100, output_tokens=300, source="reported"),
        )

    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", batch_execute)
    response = await start(c, project, runtime_version="v2", analysis_mode="all_specialists")
    assert response.status_code == 202, response.text
    if repair == "checkpoint":
        from ppm_api import agent_runtime

        class ProcessLost(BaseException):
            pass

        original_commit = agent_runtime.commit_section
        crashed = False

        async def lose_candidate(runtime, task, output):
            nonlocal crashed
            if "members" in output and not crashed:
                crashed = True
                raise ProcessLost()
            return await original_commit(runtime, task, output)

        monkeypatch.setattr(agent_runtime, "commit_section", lose_candidate)
        async with owner.connect() as conn:
            job = await conn.scalar(
                sa.select(J.jobs.c.id).where(
                    J.jobs.c.ai_run_id == UUID(response.json()["run"]["id"])
                )
            )
        with pytest.raises(ProcessLost):
            await ai_worker(app.state.engine, job, ids["a"], ids["admin"], settings)
        async with owner.begin() as conn:
            await conn.execute(
                J.jobs.update()
                .where(J.jobs.c.id == job)
                .values(lease_until=now() - timedelta(seconds=1))
            )
    result, _ = await work(c, app, owner, ids, response.json())
    assert len(seen) == 4, result
    assert len(result["task_summary"]) == 13
    if repair is True:
        assert result["run"]["status"] == "partially_succeeded", result
        assert (
            next(d for d in result["capability_details"] if d["agent"] == "executive")["code"]
            == "QUOTA_EXHAUSTED"
        )
    else:
        assert result["semantic_status"] == "hybrid_complete", result
        assert all(d["semantic_outcome"] == "completed" for d in result["capability_details"])
        final = json.loads(seen[-1].payload)["executive"]
        assert final["basis"] and len(seen[2].additional_task_classes) == 1
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(A.calls)
                .where(A.calls.c.run_id == UUID(result["run"]["id"]))
            )
            == 4
        )


@pytest.mark.parametrize("provider", ["groq", "openrouter", "mistral", "puter"])
async def test_new_cloud_provider_uses_real_shared_admission_and_daily_cap(
    identity, monkeypatch, tmp_path, provider
):
    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True, provider
    )
    body = dict(
        runtime_version="v2",
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    first = await start(c, project, **body)
    assert first.status_code == 202, first.text
    result, _ = await work(c, app, owner, ids, first.json())
    assert len(seen) == 1, result
    assert result["run"]["charged_usd"] == "0.000000"
    second = await start(c, project, **body)
    assert second.status_code == 202, second.text
    limited, _ = await work(c, app, owner, ids, second.json())
    assert len(seen) == 1, limited
    # This fixture has no independently useful canonical baseline for risk.
    # Exhausted interpretation must fail instead of claiming partial analysis.
    assert limited["run"]["status"] == "failed"
    async with owner.connect() as conn:
        calls = (
            (
                await conn.execute(
                    sa.select(A.calls).where(
                        A.calls.c.run_id == UUID(result["run"]["id"]),
                        A.calls.c.operation == "agent_v2",
                    )
                )
            )
            .mappings()
            .all()
        )
        assert len(calls) == 1 and calls[0]["provider_id"] == provider
        assert calls[0]["charged_usd"] == 0


async def test_metrics_runs_persist_tasks_and_never_call_model(identity, monkeypatch, tmp_path):
    c, app, owner, ids, project, accepted, seen = await configure(identity, monkeypatch, tmp_path)
    await create(
        c,
        "milestones",
        project_id=project["id"],
        critical=True,
        due_date=(now().date() - timedelta(days=1)).isoformat(),
    )
    response = await start(
        c,
        project,
        runtime_version="v2",
        analysis_mode="metrics",
    )
    assert response.status_code == 202, response.text
    result, job = await work(c, app, owner, ids, response.json())
    assert result["runtime_version"] == "v2" and result["run"]["status"] == "succeeded", result
    assert result["run"]["model"] is None and not result["missing_agents"]
    assert not seen and all(
        d["semantic_outcome"] == "not_requested" for d in result["capability_details"]
    )
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(T.sections)
                .where(T.sections.c.run_id == UUID(result["run"]["id"]))
            )
            == 9
        )
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(A.calls)
                .where(A.calls.c.run_id == UUID(result["run"]["id"]))
            )
            == 0
        )
    async with app.state.engine.begin() as conn:
        from ppm_api.identity import context

        await context(conn, ids["other"], ids["b"], "Admin")
        assert not (await conn.execute(sa.select(T.tasks))).all()
        assert not (await conn.execute(sa.select(T.sections))).all()


async def test_real_admission_checkpoint_replay_and_immutable_result(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True
    )
    key = str(uuid4())
    body = dict(
        runtime_version="v2",
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    response = await start(c, project, key=key, **body)
    assert response.status_code == 202, response.text
    result, job = await work(c, app, owner, ids, response.json())
    assert len(seen) == 1, result
    assert result["capability_details"][3]["semantic_outcome"] == "completed", result
    assert result["run"]["charged_usd"] == "0.000000"
    replay = await start(c, project, key=key, **body)
    assert replay.json()["run"]["id"] == result["run"]["id"]
    await work(c, app, owner, ids, response.json())
    assert len(seen) == 1
    async with owner.begin() as conn:
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(
                    T.sections.update()
                    .where(T.sections.c.run_id == UUID(result["run"]["id"]))
                    .values(result={})
                )
    assert (
        await start(c, project, key=key, **(body | {"requested_agents": ["financial"]}))
    ).status_code == 409


async def test_no_profile_preserves_baseline_but_cannot_claim_ai_complete(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, accepted, _ = await configure(identity, monkeypatch, tmp_path)
    created = await start(
        c,
        project,
        runtime_version="v2",
        analysis_mode="domain",
        requested_agents=["financial"],
        version_ids=[accepted["version_id"]],
    )
    assert created.status_code == 202, created.text
    result, _ = await work(c, app, owner, ids, created.json())
    detail = result["capability_details"][0]
    assert detail["semantic_outcome"] in ("unavailable", "deferred"), result
    assert result["run"]["status"] == "partially_succeeded", result


async def test_v2_flag_does_not_enable_itself(identity, monkeypatch):
    c, app, owner, ids, _, project, _ = await fixture(identity, monkeypatch)
    assert not app.state.settings.ai_runtime_v2_enabled
    response = await start(c, project, runtime_version="v2", analysis_mode="metrics")
    assert response.status_code == 422
    async with app.state.engine.begin() as conn:
        from ppm_api.identity import context

        await context(conn, ids["admin"], ids["a"], "Admin")
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(sa.select(T.scopes))


async def test_truncation_uses_one_smaller_replacement_and_retains_usage(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True
    )
    from ppm_api.agent_runtime import NativeAdapter

    original = NativeAdapter.execute
    requests = []

    async def truncated(self, request):
        requests.append(request)
        if len(requests) == 1:
            return ModelResult(
                attempt_id=request.permit.attempt_id,
                provider_id="ollama",
                model_id=self.profile.model,
                completion="incomplete",
                text="{",
                usage=ModelUsage(input_tokens=11, output_tokens=512, source="reported"),
            )
        return await original(self, request)

    monkeypatch.setattr(NativeAdapter, "execute", truncated)
    response = await start(
        c,
        project,
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    assert response.status_code == 202, response.text
    result, _ = await work(c, app, owner, ids, response.json())
    assert len(requests) == 2 and len(seen) == 1, result
    assert "Replacement after TRUNCATED" in requests[1].system
    assert requests[1].schema["properties"]["findings"]["maxItems"] == 1
    assert result["route_summary"][0]["output_tokens"] == 512
    assert result["route_summary"][0]["code"] == "TRUNCATED"
    assert result["capability_details"][3]["semantic_outcome"] == "completed"


async def test_unknown_outcome_is_not_replayed_and_quarantines_local_host(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, accepted, _ = await configure(
        identity, monkeypatch, tmp_path, True
    )
    attempts = []

    async def unknown(self, request):
        attempts.append(request.permit.attempt_id)
        raise ModelFailure("OUTCOME_UNKNOWN", "unknown")

    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", unknown)
    response = await start(
        c,
        project,
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    assert response.status_code == 202, response.text
    result, _ = await work(c, app, owner, ids, response.json())
    # Uninterpreted text is not a completed deterministic baseline. This fixture
    # has no other useful result to turn the ambiguous semantic-only run partial.
    assert len(attempts) == 1 and result["run"]["status"] == "failed", result
    async with owner.begin() as conn:
        quota = (
            (await conn.execute(sa.select(T.quotas).where(T.quotas.c.attempt_id == attempts[0])))
            .mappings()
            .one()
        )
        assert quota["outcome"] == "unknown" and quota["reported_output"] is None
        scope = (
            (
                await conn.execute(
                    sa.select(T.scopes).where(T.scopes.c.id == quota["quota_scope_id"])
                )
            )
            .mappings()
            .one()
        )
        assert scope["quarantined_attempt_id"] == attempts[0]
        # Synthetic call has stopped; explicit test-owner cleanup cannot be performed by app role.
        await conn.execute(
            T.scopes.update()
            .where(T.scopes.c.id == scope["id"])
            .values(quarantined_attempt_id=None, quarantine_reason=None)
        )
        await conn.execute(
            T.quotas.update().where(T.quotas.c.attempt_id == attempts[0]).values(outcome="failed")
        )


async def test_exhausted_daily_scope_makes_no_external_call(identity, monkeypatch, tmp_path):
    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True
    )
    async with owner.begin() as conn:
        await conn.execute(
            T.scopes.update()
            .where(T.scopes.c.allowed_tenants.contains([str(ids["a"])]))
            .values(tokens_per_minute=1)
        )
    response = await start(
        c,
        project,
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    result, _ = await work(c, app, owner, ids, response.json())
    assert not seen and result["capability_details"][3]["code"] == "QUOTA_EXHAUSTED", result


async def test_two_workers_share_one_local_generation(identity, monkeypatch, tmp_path):
    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True
    )
    from ppm_api.agent_runtime import NativeAdapter

    original = NativeAdapter.execute
    entered, release = asyncio.Event(), asyncio.Event()

    async def paused(self, request):
        entered.set()
        await release.wait()
        return await original(self, request)

    monkeypatch.setattr(NativeAdapter, "execute", paused)
    async with owner.begin() as conn:
        await conn.execute(
            A.budgets.update().where(A.budgets.c.organization_id == ids["a"]).values(concurrency=2)
        )
    body = dict(
        analysis_mode="domain", requested_agents=["risk"], version_ids=[accepted["version_id"]]
    )
    first = await start(c, project, **body)
    # The first request lazily creates the tenant budget row.
    async with owner.begin() as conn:
        await conn.execute(
            A.budgets.update().where(A.budgets.c.organization_id == ids["a"]).values(concurrency=2)
        )
    second = await start(c, project, **body)
    assert first.status_code == second.status_code == 202
    worker = asyncio.create_task(work(c, app, owner, ids, first.json()))
    try:
        await asyncio.wait_for(entered.wait(), 10)
        blocked, _ = await work(c, app, owner, ids, second.json())
        assert not seen and not blocked["route_summary"], blocked
        assert blocked["capability_details"][3]["semantic_outcome"] == "unavailable"
    finally:
        release.set()
        result, _ = await worker
    assert len(seen) == 1 and result["capability_details"][3]["semantic_outcome"] == "completed"


async def test_crash_after_candidate_resumes_without_second_inference(
    identity, monkeypatch, tmp_path
):
    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True
    )
    from ppm_api import agent_runtime

    class ProcessLost(BaseException):
        pass

    original = agent_runtime.commit_section
    crashed = False

    async def checkpoint(runtime, task, result):
        nonlocal crashed
        if task["kind"] == "semantic" and not crashed:
            crashed = True
            raise ProcessLost()
        return await original(runtime, task, result)

    monkeypatch.setattr(agent_runtime, "commit_section", checkpoint)
    response = await start(
        c,
        project,
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    rid = UUID(response.json()["run"]["id"])
    async with owner.connect() as conn:
        job = await conn.scalar(sa.select(J.jobs.c.id).where(J.jobs.c.ai_run_id == rid))
    with pytest.raises(ProcessLost):
        await ai_worker(app.state.engine, job, ids["a"], ids["admin"], app.state.settings)
    async with owner.begin() as conn:
        await conn.execute(
            J.jobs.update()
            .where(J.jobs.c.id == job)
            .values(lease_until=now() - timedelta(seconds=1))
        )
    result, _ = await work(c, app, owner, ids, response.json())
    assert len(seen) == 1 and result["capability_details"][3]["semantic_outcome"] == "completed", (
        result
    )


@pytest.mark.parametrize("settlement_fails", [False, True])
@pytest.mark.parametrize("provider", ["ollama", "groq"])
async def test_worker_cancellation_settles_and_propagates(
    identity, monkeypatch, tmp_path, settlement_fails, provider
):
    from ppm_api.ai import worker_context

    c, app, owner, ids, project, accepted, _ = await configure(
        identity, monkeypatch, tmp_path, True, provider
    )
    entered = asyncio.Event()
    attempts = []

    async def interrupted(self, request):
        attempts.append(request.permit.attempt_id)
        entered.set()
        await asyncio.Event().wait()

    monkeypatch.setattr("ppm_api.agent_runtime.NativeAdapter.execute", interrupted)
    created = await start(
        c,
        project,
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    rid = UUID(created.json()["run"]["id"])
    async with owner.connect() as conn:
        job = await conn.scalar(sa.select(J.jobs.c.id).where(J.jobs.c.ai_run_id == rid))
    worker = asyncio.create_task(
        ai_worker(app.state.engine, job, ids["a"], ids["admin"], app.state.settings)
    )
    try:
        await asyncio.wait_for(entered.wait(), 10)
        if settlement_fails:

            async def unavailable(*args):
                raise RuntimeError("synthetic settlement failure")

            monkeypatch.setattr("ppm_api.ai.worker_context", unavailable)
        worker.cancel("synthetic shutdown")
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(worker, 10)
        assert worker.cancelled() and len(attempts) == 1
        async with owner.connect() as conn:
            call = (
                (await conn.execute(sa.select(A.calls).where(A.calls.c.id == attempts[0])))
                .mappings()
                .one()
            )
            quota = (
                (
                    await conn.execute(
                        sa.select(T.quotas).where(T.quotas.c.attempt_id == attempts[0])
                    )
                )
                .mappings()
                .one()
            )
        assert call["status"] == "unknown"
        if settlement_fails:
            assert call["completed_at"] is None
            assert quota["outcome"] == "admitted"
        else:
            assert call["code"] == "CANCELLED" and call["completed_at"] is not None
            assert quota["outcome"] == "unknown"
        monkeypatch.setattr("ppm_api.ai.worker_context", worker_context)
        async with owner.begin() as conn:
            await conn.execute(
                J.jobs.update()
                .where(J.jobs.c.id == job)
                .values(lease_until=now() - timedelta(seconds=1))
            )
        result, _ = await work(c, app, owner, ids, created.json())
        assert len(attempts) == 1
        task = next(t for t in result["task_summary"] if t["task_key"] == "risk-01")
        assert task["state"] == "BLOCKED" and task["diagnostic"] == "OUTCOME_UNKNOWN"
    finally:
        if not worker.done():
            worker.cancel()
        with suppress(asyncio.CancelledError, Exception):
            await worker
        # This intercepted call has stopped; retain its usage history while
        # releasing the synthetic host quarantine for subsequent tests.
        async with owner.begin() as conn:
            await conn.execute(
                T.quotas.update()
                .where(T.quotas.c.attempt_id.in_(attempts))
                .values(outcome="released_unknown")
            )
            await conn.execute(
                T.scopes.update()
                .where(T.scopes.c.quarantined_attempt_id.in_(attempts))
                .values(quarantined_attempt_id=None, quarantine_reason=None)
            )


@pytest.mark.parametrize("failure", ["database", "RUN_CANCELLED", "DEADLINE_EXCEEDED"])
async def test_failed_heartbeat_does_not_replace_completed_result(
    identity, monkeypatch, tmp_path, failure
):
    from ppm_api import ai_provider

    c, app, owner, ids, project, _, _ = await configure(identity, monkeypatch, tmp_path)
    await create(
        c,
        "milestones",
        project_id=project["id"],
        due_date=(now().date() - timedelta(days=1)).isoformat(),
        critical=True,
    )

    async def failed(runtime, stop):
        if failure == "database":
            raise RuntimeError("synthetic heartbeat failure")
        raise ai_provider.ProviderError(failure)

    monkeypatch.setattr("ppm_api.agent_runtime.heartbeat", failed)
    created = await start(c, project, analysis_mode="metrics")
    result, _ = await work(c, app, owner, ids, created.json())
    assert result["run"]["status"] == "succeeded", result
    assert result["capability_details"]
    assert any(d["base_covered_ids"] for d in result["capability_details"])


async def test_oversized_bound_context_keeps_baseline_and_reports_partial(
    identity, monkeypatch, tmp_path
):
    from ppm_api import agent_runtime

    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True
    )
    original = agent_runtime.pack
    await create(
        c,
        "milestones",
        project_id=project["id"],
        due_date=(now().date() - timedelta(days=1)).isoformat(),
        critical=True,
    )

    def oversized(*args, **kwargs):
        context = original(*args, **kwargs)
        context["payload"] += " " * 95000
        return context

    monkeypatch.setattr(agent_runtime, "pack", oversized)
    created = await start(
        c,
        project,
        analysis_mode="domain",
        requested_agents=["risk", "schedule"],
        version_ids=[accepted["version_id"]],
    )
    result, _ = await work(c, app, owner, ids, created.json())
    assert not seen
    assert result["run"]["status"] == "partially_succeeded", result
    assert any(d["base_covered_ids"] for d in result["capability_details"])
    async with owner.connect() as conn:
        task = (
            (
                await conn.execute(
                    sa.select(T.tasks).where(
                        T.tasks.c.run_id == UUID(created.json()["run"]["id"]),
                        T.tasks.c.kind == "semantic",
                        T.tasks.c.agent == "risk",
                    )
                )
            )
            .mappings()
            .one()
        )
    assert task["state"] == "BLOCKED" and task["diagnostic"] == "CONTEXT_LIMIT"
    assert task["bound_at"] is None and task["resolved_context_manifest"] is None


@pytest.mark.parametrize("mode", ["cancel", "lease", "revoke", "source"])
async def test_v2_late_output_is_fenced(identity, monkeypatch, tmp_path, mode):
    c, app, owner, ids, project, accepted, seen = await configure(
        identity, monkeypatch, tmp_path, True
    )
    from ppm_api import agent_tables
    from ppm_api.agent_runtime import NativeAdapter
    from ppm_api.identity_tables import memberships

    original = NativeAdapter.execute
    entered, release = asyncio.Event(), asyncio.Event()

    async def paused(self, request):
        entered.set()
        await release.wait()
        return await original(self, request)

    monkeypatch.setattr(NativeAdapter, "execute", paused)
    created = await start(
        c,
        project,
        analysis_mode="domain",
        requested_agents=["risk"],
        version_ids=[accepted["version_id"]],
    )
    rid = UUID(created.json()["run"]["id"])
    async with owner.connect() as conn:
        job = await conn.scalar(sa.select(J.jobs.c.id).where(J.jobs.c.ai_run_id == rid))
    worker = asyncio.create_task(
        ai_worker(app.state.engine, job, ids["a"], ids["admin"], app.state.settings)
    )
    try:
        await asyncio.wait_for(entered.wait(), 10)
        if mode == "cancel":
            current = (await c.get(f"/api/v1/agents/runs/{rid}")).json()
            result = await send(
                c,
                "POST",
                f"/ai/runs/{rid}/cancel",
                headers={"if-match": str(current["run"]["revision"])},
            )
            assert result.status_code == 200
        elif mode == "source":
            result = await send(
                c, "DELETE", f"/documents/{accepted['document']['id']}", headers={"if-match": "1"}
            )
            assert result.status_code == 200
        else:
            async with owner.begin() as conn:
                if mode == "lease":
                    await conn.execute(
                        J.jobs.update()
                        .where(J.jobs.c.id == job)
                        .values(lease_token=uuid4(), lease_until=now() - timedelta(seconds=1))
                    )
                else:
                    await conn.execute(
                        memberships.update()
                        .where(
                            memberships.c.organization_id == ids["a"],
                            memberships.c.user_id == ids["admin"],
                        )
                        .values(active=False)
                    )
    finally:
        release.set()
        await asyncio.wait_for(worker, 15)
    assert len(seen) == 1
    async with owner.begin() as conn:
        output = await conn.scalar(
            sa.select(agent_tables.analyses.c.output).where(agent_tables.analyses.c.run_id == rid)
        )
        assert output is None or not any(
            f.get("epistemic") != "deterministic" for f in output["findings"]
        )
        calls = (
            (await conn.execute(sa.select(A.calls).where(A.calls.c.run_id == rid))).mappings().all()
        )
        assert len(calls) == 1 and calls[0]["charged_usd"] == 0
        # If revoked authority prevented settlement, the synthetic stopped attempt
        # is explicitly released by the test owner without removing usage history.
        await conn.execute(
            T.quotas.update()
            .where(T.quotas.c.attempt_id == calls[0]["id"])
            .values(outcome="released_unknown")
        )
        await conn.execute(
            T.scopes.update()
            .where(T.scopes.c.allowed_tenants.contains([str(ids["a"])]))
            .values(quarantined_attempt_id=None, quarantine_reason=None)
        )
