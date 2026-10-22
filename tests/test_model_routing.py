"""Zero-spend and transport contracts with synthetic profiles; real HTTP is never used."""

import json
from dataclasses import replace
from datetime import timedelta
from uuid import uuid4

import httpx
import pytest
from ppm_api.identity import now
from ppm_api.model_adapters import NativeAdapter
from ppm_api.model_contracts import ExecutionPermit, ModelFailure, ModelRequest
from ppm_api.model_registry import ModelPolicy, ModelProfile
from ppm_api.model_router import RouteRequirements, candidates
from test_gemini import gemini as gemini
from test_gemini import response as gemini_response


@pytest.fixture
def configured(settings, tmp_path):
    tenant, project = uuid4(), uuid4()
    settings.storage_root = tmp_path / "objects"
    settings.ai_runtime_v2_enabled = settings.ai_ollama_enabled = True
    settings.ai_local_available_memory_mb = 8192
    profile = ModelProfile(
        id="local-test",
        provider="ollama",
        model="test:4b",
        enabled=True,
        billing_class="local",
        quota_scope="ollama:host-one",
        allowed_tenants=[tenant],
        qualified_task_classes=["risk_extraction", "executive_synthesis"],
        benchmark_only=False,
        installed_digest="a" * 64,
        requests_per_minute=20,
        requests_per_day=100,
        tokens_per_minute=100000,
    )
    policy = ModelPolicy(profiles=[profile])
    path = tmp_path / "policy.json"
    path.write_text(policy.model_dump_json(), encoding="utf-8")
    settings.ai_model_registry_path = path
    permit = ExecutionPermit(
        uuid4(), profile.provider, profile.model, policy.policy_hash, now() + timedelta(seconds=10)
    )
    request = ModelRequest(
        permit, "Read only", "{}", {"type": "object"}, 2, tenant, project, "risk_extraction"
    )
    return settings, profile, policy, request


def test_rank_only_eligible_and_task_class_specific(configured):
    settings, profile, policy, request = configured
    need = RouteRequirements(request.tenant, request.project, "executive_synthesis", 100)
    assert candidates(policy, need, settings)[0] == [profile]
    assert (
        candidates(
            policy,
            RouteRequirements(request.tenant, request.project, "financial_interpretation", 100),
            settings,
        )[1][profile.id]
        == "QUALITY_UNVERIFIED"
    )
    settings.ai_local_available_memory_mb = None
    assert candidates(policy, need, settings)[1][profile.id] == "LOCAL_RESOURCE"
    settings.ai_local_available_memory_mb = 8192
    settings.ai_execution_mode = "disabled"
    assert not candidates(policy, need, settings)[0]


async def test_retry_after_is_normalized_without_internal_retry(configured):
    settings, profile, _, request = configured
    count = 0

    def respond(req):
        nonlocal count
        count += 1
        if req.url.path == "/api/tags":
            return httpx.Response(
                200, json={"models": [{"name": profile.model, "digest": profile.installed_digest}]}
            )
        return httpx.Response(429, headers={"retry-after": "120"})

    with pytest.raises(ModelFailure) as raised:
        await NativeAdapter(settings, profile, httpx.MockTransport(respond)).execute(request)
    assert raised.value.code == "QUOTA_EXHAUSTED" and raised.value.retry_after == 120
    assert count == 2


@pytest.mark.parametrize("change", ["paid", "unknown", "no_auth", "no_egress"])
def test_cloud_is_fail_closed(configured, change):
    settings, profile, _, request = configured
    profile = profile.model_copy(
        update={
            "provider": "gemini",
            "billing_class": change if change in ("paid", "unknown") else "verified_free",
        }
    )
    policy = ModelPolicy(profiles=[profile])
    settings.ai_execution_mode = "hybrid"
    settings.ai_cloud_enabled = True
    rows, _ = candidates(
        policy, RouteRequirements(request.tenant, request.project, "risk_extraction", 100), settings
    )
    assert rows == []


@pytest.mark.parametrize(
    "finish,expected", [("stop", "complete"), ("length", "incomplete"), (None, "incomplete")]
)
async def test_ollama_finish_usage_and_bounded_payload(configured, finish, expected):
    settings, profile, _, request = configured
    seen = []

    def handler(req):
        if req.url.path == "/api/tags":
            return httpx.Response(
                200, json={"models": [{"name": profile.model, "digest": profile.installed_digest}]}
            )
        seen.append(json.loads(req.content))
        return httpx.Response(
            200,
            json=dict(
                done=True,
                done_reason=finish,
                message={"content": "{}"},
                prompt_eval_count=10,
                eval_count=4,
            ),
        )

    result = await NativeAdapter(settings, profile, httpx.MockTransport(handler)).execute(request)
    assert result.completion == expected and result.usage.input_tokens == 10
    assert seen[0]["options"]["num_predict"] == 512 and seen[0]["think"] is False
    assert seen[0]["stream"] is False


async def test_missing_model_does_not_download(configured):
    settings, profile, _, request = configured
    paths = []

    def handler(req):
        paths.append(req.url.path)
        return httpx.Response(200, json={"models": []})

    with pytest.raises(ModelFailure, match="MODEL_NOT_INSTALLED"):
        await NativeAdapter(settings, profile, httpx.MockTransport(handler)).execute(request)
    assert paths == ["/api/tags"]


@pytest.mark.parametrize(
    "status,code",
    [
        (302, "CONFIGURATION"),
        (401, "AUTHENTICATION"),
        (403, "AUTHENTICATION"),
        (429, "QUOTA_EXHAUSTED"),
        (503, "UNAVAILABLE"),
    ],
)
async def test_transport_errors_are_codes_without_provider_body(configured, status, code):
    settings, profile, _, request = configured

    def handler(req):
        return httpx.Response(status, text="SECRET must never enter diagnostics")

    with pytest.raises(ModelFailure, match=code) as error:
        await NativeAdapter(settings, profile, httpx.MockTransport(handler)).execute(request)
    assert "SECRET" not in str(error.value)


async def test_direct_adapter_rechecks_policy_and_url(configured):
    settings, profile, _, request = configured

    def forbidden(req):
        pytest.fail("Network attempted after policy denial")

    settings.ai_execution_mode = "disabled"
    with pytest.raises(ModelFailure, match="SPENDING_NOT_AUTHORIZED"):
        await NativeAdapter(settings, profile, httpx.MockTransport(forbidden)).execute(request)
    settings.ai_execution_mode = "local_only"
    settings.ai_ollama_base_url = "http://attacker.invalid:11434"
    with pytest.raises(ModelFailure, match="CONFIGURATION"):
        await NativeAdapter(settings, profile, httpx.MockTransport(forbidden)).execute(request)


def test_shared_host_cannot_duplicate_quota_through_profile_alias(configured):
    _, profile, _, _ = configured
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        ModelPolicy(
            profiles=[profile, profile.model_copy(update={"id": "alias", "requests_per_day": 200})]
        )


@pytest.mark.parametrize(
    "finish,expected", [("STOP", "complete"), ("MAX_TOKENS", "incomplete"), ("SAFETY", "refused")]
)
async def test_authorized_native_gemini_preserves_finish_usage_and_egress(
    configured, gemini, monkeypatch, finish, expected
):
    from ppm_api import ai_provider as P

    settings, profile, _, request = configured
    settings.ai_execution_mode, settings.ai_cloud_enabled = "hybrid", True
    settings.ai_provider = "disabled"  # V2 cloud must not share the legacy dispatch path.
    key = settings.ai_api_key.get_secret_value()
    monkeypatch.setenv("PPM_FIXTURE_CLOUD_KEY", key)
    profile = profile.model_copy(
        update=dict(
            provider="gemini",
            model=P.GEMINI_COMPLETION_MODEL,
            billing_class="verified_free",
            quota_scope="gemini:fixture-account",
            credential_ref="PPM_FIXTURE_CLOUD_KEY",
            credential_sha256=settings.ai_gemini_free_tier_key_sha256,
            free_tier_confirmed=True,
            data_policy_confirmed=True,
            requests_per_day=settings.ai_gemini_daily_call_limit,
        )
    )
    policy = ModelPolicy(profiles=[profile])
    settings.ai_model_registry_path.write_text(policy.model_dump_json(), encoding="utf-8")
    settings.ai_egress_policy_path = settings.ai_model_registry_path.with_name("egress.json")
    settings.ai_egress_policy_path.write_text(
        json.dumps({str(request.tenant): {str(request.project): {"gemini": ["document:project"]}}}),
        encoding="utf-8",
    )
    request = replace(
        request,
        permit=replace(
            request.permit,
            provider_id="gemini",
            model_id=profile.model,
            policy_hash=policy.policy_hash,
        ),
        categories=("document:project",),
    )
    seen = []

    def respond(req):
        seen.append(req)
        body = json.loads(req.content)
        assert body["generationConfig"]["maxOutputTokens"] == 512
        schema = body["generationConfig"]["responseJsonSchema"]
        if "properties" in schema:
            assert set(schema["required"]) == set(schema["properties"])
        assert req.headers["x-goog-api-key"] == key
        value = gemini_response()
        value["candidates"][0]["finishReason"] = finish
        return httpx.Response(200, json=value)

    result = await NativeAdapter(settings, profile, httpx.MockTransport(respond)).execute(request)
    assert result.completion == expected and len(seen) == 1
    assert result.usage.input_tokens == 10 and result.usage.reasoning_tokens == 2
    settings.ai_provider = "gemini"
    need = RouteRequirements(
        request.tenant, request.project, "risk_extraction", 100, categories=request.categories
    )
    assert candidates(policy, need, settings)[1][profile.id] == "CONFIGURATION"
    settings.ai_provider = "disabled"
    excessive = profile.model_copy(
        update={"requests_per_day": settings.ai_gemini_daily_call_limit + 1}
    )
    assert (
        candidates(ModelPolicy(profiles=[excessive]), need, settings)[1][profile.id]
        == "CONFIGURATION"
    )
    settings.ai_egress_policy_path.write_text("{}", encoding="utf-8")
    empty_categories = replace(request, categories=())
    with pytest.raises(ModelFailure):
        await NativeAdapter(settings, profile, httpx.MockTransport(respond)).execute(
            empty_categories
        )
    assert len(seen) == 1
