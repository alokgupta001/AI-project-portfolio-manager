"""Three-provider assignment, native Puter controls and durable calibration limits."""

import hashlib
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest
from ppm_api.agent_prompts import ROLE_PROVIDERS, cloud_prompt
from ppm_api.agent_registry import BY_AGENT
from ppm_api.agent_runtime import complete_task
from ppm_api.model_adapters import NativeAdapter
from ppm_api.model_contracts import ModelFailure
from ppm_api.model_registry import ModelPolicy
from ppm_api.model_router import RouteRequirements, candidates
from test_model_routing import configured as configured

from scripts import benchmark_cloud_specialists as cloud_benchmark
from scripts.benchmark_agent_runtime import CORPUS
from scripts.benchmark_cloud_specialists import check_admission
from scripts.prepare_agent_training import examples


def test_assignment_covers_nine_roles_without_granting_qualification():
    policy = ModelPolicy.model_validate_json(
        open("config/model-policy.cloud.example.json", encoding="utf-8").read()
    )
    assigned = []
    for profile in policy.profiles:
        own = [agent for agent, provider in ROLE_PROVIDERS.items() if provider == profile.provider]
        assert len(own) == 3
        assert set(profile.assigned_task_classes) == {BY_AGENT[a].task_class for a in own}
        assert not profile.enabled and profile.benchmark_only
        assert not profile.qualified_task_classes and not profile.allowed_tenants
        assigned += profile.assigned_task_classes
    assert len(set(assigned)) == len(BY_AGENT) == 9


def test_assigned_role_cannot_be_bypassed_by_qualification(configured):
    settings, profile, _, request = configured
    assigned = profile.model_copy(update={"assigned_task_classes": ["risk_extraction"]})
    rows, reasons = candidates(
        ModelPolicy(profiles=[assigned]),
        RouteRequirements(request.tenant, request.project, "executive_synthesis", 100),
        settings,
    )
    assert not rows and reasons[profile.id] == "ROLE_NOT_ASSIGNED"


async def test_pending_task_cannot_resume_with_changed_prompt(settings):
    settings.ai_execution_mode = "hybrid"
    settings.ai_cloud_enabled = True
    with pytest.raises(ModelFailure) as failure:
        await complete_task(
            SimpleNamespace(settings=settings),
            {"prompt_hash": "old-prompt"},
            dict(agent="risk", kind="semantic", mode="findings"),
            {},
            None,
        )
    assert failure.value.code == "CONFIGURATION"


@pytest.fixture
def puter(configured, monkeypatch):
    settings, original, _, request = configured
    key = "synthetic-puter-key"
    monkeypatch.setenv("PPM_FIXTURE_KEY", key)
    settings.ai_execution_mode = "hybrid"
    settings.ai_cloud_enabled = settings.ai_real_calls_authorized = True
    profile = original.model_copy(
        update=dict(
            provider="puter",
            model="gpt-4.1-mini-2025-04-14",
            upstream_provider="openai-completion",
            billing_class="verified_free",
            quota_scope="puter:fixture",
            credential_ref="PPM_FIXTURE_KEY",
            credential_sha256=hashlib.sha256(key.encode()).hexdigest(),
            free_tier_confirmed=True,
            data_policy_confirmed=True,
        )
    )
    policy = ModelPolicy(profiles=[profile])
    settings.ai_model_registry_path.write_text(policy.model_dump_json(), encoding="utf-8")
    settings.ai_egress_policy_path = settings.ai_model_registry_path.with_name("egress.json")
    settings.ai_egress_policy_path.write_text(
        json.dumps({str(request.tenant): {str(request.project): {"puter": ["document:project"]}}}),
        encoding="utf-8",
    )
    request = replace(
        request,
        categories=("document:project",),
        permit=replace(
            request.permit,
            provider_id="puter",
            model_id=profile.model,
            policy_hash=policy.policy_hash,
        ),
    )
    return settings, profile, request


@pytest.mark.parametrize(
    "reason,completion",
    [
        ("stop", "complete"),
        ("length", "incomplete"),
        ("content_filter", "refused"),
        ("unknown", "unknown"),
    ],
)
async def test_native_puter_preserves_actual_completion_and_bounds(puter, reason, completion):
    settings, profile, request = puter
    seen = []

    def respond(req):
        seen.append(req)
        body = json.loads(req.content)
        assert str(req.url) == "https://api.puter.com/drivers/call"
        assert req.headers["authorization"] == "Bearer synthetic-puter-key"
        assert body["driver"] == "ai-chat" and body["method"] == "complete"
        args = body["args"]
        assert args["provider"] == "openai-completion" and args["model"] == profile.model
        assert args["stream"] is False and args["max_tokens"] == 512
        assert args["normalize"] is True and args["outputFormat"]["strict"] is True
        assert "tools" not in args and "auth_token" not in body
        return httpx.Response(
            200,
            json={
                "success": True,
                "result": dict(
                    model=profile.model,
                    message={"content": "{}"},
                    finish_reason=reason,
                    usage={"prompt_tokens": 17, "completion_tokens": 9},
                ),
            },
        )

    result = await NativeAdapter(settings, profile, httpx.MockTransport(respond)).execute(request)
    assert result.completion == completion and result.usage.output_tokens == 9
    assert len(seen) == 1


@pytest.mark.parametrize("change", ["reasoning", "tool", "model", "funds", "redirect"])
async def test_native_puter_rejects_unsafe_or_unbound_responses(puter, change):
    settings, profile, request = puter

    def respond(req):
        result = dict(model=profile.model, finish_reason="stop", message={"content": "{}"})
        if change == "reasoning":
            result["message"]["reasoning"] = "private"
        if change == "tool":
            result["message"]["tool_calls"] = [dict(id="tool")]
        if change == "model":
            result["model"] = "different-model"
        if change == "funds":
            return httpx.Response(
                200, json={"success": False, "error": {"code": "insufficient_funds"}}
            )
        if change == "redirect":
            return httpx.Response(302, headers={"location": "https://untrusted.invalid"})
        return httpx.Response(200, json={"result": result})

    with pytest.raises(ModelFailure):
        await NativeAdapter(settings, profile, httpx.MockTransport(respond)).execute(request)


@pytest.mark.parametrize(
    "service,model,accepted",
    [
        ("openai-completion", "gpt-4.1-mini", True),
        ("openrouter", "gpt-4.1-mini", False),
        ("openai-completion", "different-model", False),
    ],
)
def test_puter_native_catalogue_identity_is_preserved(puter, service, model, accepted):
    settings, profile, request = puter
    data = dict(
        result=dict(message=dict(content="{}"), finish_reason="stop"),
        metadata=dict(service_used=service, providerUsed=model),
    )
    adapter = NativeAdapter(settings, profile)
    if accepted:
        result = adapter.puter_result(request, data, 1)
        assert result.model_id == profile.model and result.reported_model_id == model
    else:
        with pytest.raises(ModelFailure):
            adapter.puter_result(request, data, 1)


def test_training_examples_are_separate_and_hard_validated():
    rows, report = examples()
    assert report["examples"] == len(rows) == 36
    assert set(report["role_counts"]) == set(BY_AGENT)
    assert not report["model_weights_trained"] and not report["labels_independently_reviewed"]
    assert all(r["id"].startswith("training_") for r in rows)
    for agent in BY_AGENT:
        prompt = cloud_prompt(
            agent, "synthesis" if agent in ("sentiment", "pmo", "executive") else "findings"
        )
        assert "required aliases" in prompt and "no_findings requires" in prompt


def test_history_unknown_budget_and_root_limits_are_preserved():
    profile = ModelPolicy.model_validate_json(
        open("config/model-policy.cloud.example.json", encoding="utf-8").read()
    ).profiles[0]
    now = datetime.now(UTC)
    old = (now - timedelta(hours=1)).isoformat()
    row = dict(root="same", state="completed", admitted_at=old, reserved_tokens=100)
    auth = dict(max_calls=9)
    check_admission(profile, auth, [], [row] * 3, "new", 100, 0, now)
    for rows, history, external in [
        ([row] * 2, [], 0),
        ([], [row] * 20, 0),
        ([], [], 20),
        ([dict(row, state="unknown")], [], 0),
        ([row] * 9, [], 0),
    ]:
        with pytest.raises(ModelFailure):
            check_admission(profile, auth, rows, history, "same", 100, external, now)


@pytest.fixture
def calibration(tmp_path, monkeypatch, settings):
    folder = tmp_path / "ai-v2"
    folder.mkdir()
    policy = ModelPolicy.model_validate_json(
        Path("config/model-policy.cloud.example.json").read_bytes()
    )
    profile = policy.profiles[0]
    # Exercise the preserved historical single-role calibration format.
    profile.assigned_task_classes = [
        "financial_interpretation",
        "schedule_interpretation",
        "resource_interpretation",
    ]
    monkeypatch.setattr(
        cloud_benchmark, "ROLE_PROVIDERS", dict(financial="groq", schedule="groq", resource="groq")
    )
    profile.free_tier_confirmed = True
    profile.credential_sha256 = hashlib.sha256(b"synthetic-key").hexdigest()
    (folder / "policy.json").write_text(ModelPolicy(profiles=[profile]).model_dump_json())
    (folder / "groq-specialist-authorization.json").write_text(
        json.dumps(
            dict(
                provider="groq",
                model=profile.model,
                account_scope=profile.quota_scope,
                key_sha256=profile.credential_sha256,
                corpus_sha256=hashlib.sha256(CORPUS.read_bytes()).hexdigest(),
                synthetic_only=True,
                calibration_only=True,
                free_tier_confirmed=True,
                max_spend_usd="0",
                max_calls=9,
            )
        )
    )
    monkeypatch.setattr(
        cloud_benchmark, "read_keys", lambda p: {profile.credential_ref: "synthetic-key"}
    )
    monkeypatch.setattr(cloud_benchmark, "gemini_settings", lambda: settings)
    monkeypatch.setattr(cloud_benchmark, "retained_history", lambda *a: [])
    return folder, profile


async def test_cloud_calibration_dry_run_never_calls_or_promotes(calibration):
    folder, _ = calibration

    def forbid(req):
        raise AssertionError("No HTTP in dry run")

    report = await cloud_benchmark.run(
        "groq", ["financial_01"], False, folder, httpx.MockTransport(forbid)
    )
    assert report["status"] == "prepared_no_requests" and not report["profile_activated"]
    assert not (folder / "groq-specialist-ledger.json").exists()
    for ids in (["financial_02"], ["risk_01"], ["financial_01"] * 4):
        with pytest.raises(ValueError):
            await cloud_benchmark.run("groq", ids, True, folder, httpx.MockTransport(forbid))


async def test_cloud_unknown_is_checkpointed_and_cannot_be_replayed(calibration):
    folder, _ = calibration
    calls = []

    def lose(req):
        calls.append(req)
        raise httpx.ReadTimeout("synthetic lost reply")

    report = await cloud_benchmark.run(
        "groq", ["financial_01"], True, folder, httpx.MockTransport(lose)
    )
    assert report["status"] == "stopped_on_unknown"
    assert (
        json.loads((folder / "groq-specialist-ledger.json").read_bytes())[0]["state"] == "unknown"
    )
    again = await cloud_benchmark.run(
        "groq", ["schedule_01"], True, folder, httpx.MockTransport(lose)
    )
    assert again["code"] == "OUTCOME_UNKNOWN" and len(calls) == 1


async def test_cloud_success_retains_raw_and_semantic_review_is_pending(calibration):
    folder, profile = calibration

    def respond(req):
        payload = json.loads(json.loads(req.content)["messages"][1]["content"])
        value = dict(
            section=payload["section"],
            mode=payload["mode"],
            outcome="no_findings",
            findings=[],
            matches=[],
            narrative=[],
            covered=payload["required"],
            gaps=[],
        )
        return httpx.Response(
            200,
            json=dict(
                model=profile.model,
                choices=[dict(finish_reason="stop", message=dict(content=json.dumps(value)))],
                usage=dict(prompt_tokens=100, completion_tokens=40),
            ),
        )

    report = await cloud_benchmark.run(
        "groq", ["financial_07"], True, folder, httpx.MockTransport(respond)
    )
    assert report["status"] == "completed_pending_review" and not report["qualified_classes"]
    assert report["attempts"][0]["native_sha256"]
    assert len(list(folder.glob("cloud-native-*.json"))) == 1
