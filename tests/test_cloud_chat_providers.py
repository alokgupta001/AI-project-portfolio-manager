"""New cloud transports use synthetic keys and intercepted HTTP only."""

import hashlib
import json
from dataclasses import replace

import httpx
import pytest
from ppm_api.model_adapters import CLOUD_CHAT_ORIGINS, NativeAdapter
from ppm_api.model_contracts import ModelFailure
from ppm_api.model_registry import ModelPolicy
from ppm_api.model_router import RouteRequirements, candidates
from test_model_routing import configured as configured


@pytest.fixture(params=["groq", "openrouter", "mistral"])
def cloud(configured, monkeypatch, request):
    settings, original, _, model_request = configured
    provider = request.param
    key = "synthetic-key-never-a-real-credential"
    monkeypatch.setenv("PPM_FIXTURE_KEY", key)
    settings.ai_execution_mode = "hybrid"
    settings.ai_cloud_enabled = settings.ai_real_calls_authorized = True
    models = {
        "groq": "openai/gpt-oss-20b",
        "openrouter": "test/pinned:free",
        "mistral": "ministral-8b-2512",
    }
    profile = original.model_copy(
        update=dict(
            provider=provider,
            model=models[provider],
            billing_class="verified_free",
            quota_scope=provider + ":test-account",
            credential_ref="PPM_FIXTURE_KEY",
            credential_sha256=hashlib.sha256(key.encode()).hexdigest(),
            free_tier_confirmed=True,
            data_policy_confirmed=True,
            upstream_provider="test-upstream" if provider == "openrouter" else None,
        )
    )
    policy = ModelPolicy(profiles=[profile])
    settings.ai_model_registry_path.write_text(policy.model_dump_json(), encoding="utf-8")
    settings.ai_egress_policy_path = settings.ai_model_registry_path.with_name("egress.json")
    settings.ai_egress_policy_path.write_text(
        json.dumps(
            {
                str(model_request.tenant): {
                    str(model_request.project): {provider: ["document:project"]}
                }
            }
        ),
        encoding="utf-8",
    )
    model_request = replace(
        model_request,
        categories=("document:project",),
        permit=replace(
            model_request.permit,
            provider_id=provider,
            model_id=profile.model,
            policy_hash=policy.policy_hash,
        ),
    )
    return settings, profile, policy, model_request


def reply(profile, finish="stop", **message):
    return dict(
        model=profile.model,
        choices=[dict(finish_reason=finish, message=dict(content="{}", **message))],
        usage=dict(prompt_tokens=11, completion_tokens=7, cost=0),
    )


@pytest.mark.parametrize(
    "finish,completion",
    [
        ("stop", "complete"),
        ("length", "incomplete"),
        ("content_filter", "refused"),
        ("other", "unknown"),
    ],
)
async def test_bounded_cloud_requests_preserve_completion_and_usage(cloud, finish, completion):
    settings, profile, _, request = cloud
    posts = []

    def handler(req):
        assert str(req.url).startswith(CLOUD_CHAT_ORIGINS[profile.provider] + "/")
        if req.method == "GET":
            assert req.url.path.endswith("/endpoints")
            assert "authorization" not in req.headers
            return httpx.Response(
                200, json={"data": {"endpoints": [{"pricing": {"prompt": "0", "completion": "0"}}]}}
            )
        assert req.headers["authorization"] == "Bearer synthetic-key-never-a-real-credential"
        posts.append(json.loads(req.content))
        return httpx.Response(200, json=reply(profile, finish))

    result = await NativeAdapter(settings, profile, httpx.MockTransport(handler)).execute(request)
    assert result.completion == completion
    assert result.usage.input_tokens == 11 and result.usage.output_tokens == 7
    assert len(posts) == 1
    body = posts[0]
    assert body.get("max_tokens", body.get("max_completion_tokens")) == 512
    assert body["stream"] is False and "tools" not in body
    assert body["response_format"]["json_schema"]["strict"] is True
    if profile.provider == "openrouter":
        assert body["provider"] == dict(
            only=["test-upstream"],
            allow_fallbacks=False,
            require_parameters=True,
            data_collection="deny",
            zdr=True,
            max_price=dict(prompt=0, completion=0, request=0, image=0),
        )


@pytest.mark.parametrize("change", ["key", "egress", "tier", "quality", "disabled"])
async def test_policy_denial_precedes_any_cloud_http(cloud, change, monkeypatch):
    settings, profile, _, request = cloud
    if change == "key":
        monkeypatch.setenv("PPM_FIXTURE_KEY", "rotated-unconfirmed")
    elif change == "egress":
        settings.ai_egress_policy_path.write_text("{}", encoding="utf-8")
    else:
        profile = profile.model_copy(
            update={
                "tier": dict(free_tier_confirmed=False),
                "quality": dict(benchmark_only=True),
                "disabled": dict(enabled=False),
            }[change]
        )
        settings.ai_model_registry_path.write_text(
            ModelPolicy(profiles=[profile]).model_dump_json(), encoding="utf-8"
        )

    def forbidden(req):
        pytest.fail("HTTP after missing authority")

    with pytest.raises(ModelFailure):
        await NativeAdapter(settings, profile, httpx.MockTransport(forbidden)).execute(request)


@pytest.mark.parametrize(
    "field,value",
    [
        ("tool_calls", [{"function": "x"}]),
        ("reasoning", "hidden must not escape"),
        ("reasoning_details", [{"text": "private"}]),
    ],
)
async def test_tools_and_reasoning_never_become_output(cloud, field, value):
    settings, profile, _, request = cloud
    adapter = NativeAdapter(settings, profile)
    with pytest.raises(ModelFailure, match="INVALID_OUTPUT"):
        adapter.chat_result(request, reply(profile, **{field: value}), 1)


def test_provider_specific_free_and_version_guards(cloud):
    settings, profile, _, request = cloud
    bad = profile.model_copy(update={"model": "moving-latest"})
    need = RouteRequirements(
        request.tenant, request.project, request.task_class, 100, categories=request.categories
    )
    assert candidates(ModelPolicy(profiles=[bad]), need, settings)[0] == []
    if profile.provider == "openrouter":
        for update in (dict(model="test/paid"), dict(upstream_provider=None)):
            assert (
                candidates(
                    ModelPolicy(profiles=[profile.model_copy(update=update)]), need, settings
                )[0]
                == []
            )


async def test_openrouter_nonzero_catalog_price_prevents_generation(cloud):
    settings, profile, _, request = cloud
    if profile.provider != "openrouter":
        return
    methods = []

    def handler(req):
        methods.append(req.method)
        return httpx.Response(
            200, json={"data": {"endpoints": [{"pricing": {"prompt": "0", "completion": "0.1"}}]}}
        )

    with pytest.raises(ModelFailure, match="SPENDING_NOT_AUTHORIZED"):
        await NativeAdapter(settings, profile, httpx.MockTransport(handler)).execute(request)
    assert methods == ["GET"]


async def test_missing_usage_stays_unknown_and_provider_error_is_sanitized(cloud):
    settings, profile, _, request = cloud
    data = reply(profile)
    del data["usage"]
    adapter = NativeAdapter(settings, profile)
    if profile.provider == "openrouter":
        with pytest.raises(ModelFailure):
            adapter.chat_result(request, data, 1)
    else:
        result = adapter.chat_result(request, data, 1)
        assert result.usage.input_tokens is None and result.usage.source == "unknown"
    paths = []

    def fail(req):
        paths.append(req.url.path)
        return httpx.Response(
            429, headers={"retry-after": "95"}, text="private provider diagnostics"
        )

    with pytest.raises(ModelFailure) as error:
        await NativeAdapter(settings, profile, httpx.MockTransport(fail)).execute(request)
    assert error.value.code == "QUOTA_EXHAUSTED" and error.value.retry_after == 95
    assert len(paths) == 1 and "private" not in str(error.value)
