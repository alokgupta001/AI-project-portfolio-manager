"""Operator setup cannot generate, disclose keys or bypass a host resource block."""

import json

import httpx
import pytest
from ppm_api import local_model_readiness as local

from scripts.check_provider_setup import PROVIDERS, inspect


async def test_metadata_verification_has_only_fixed_gets_and_no_secrets_in_output():
    keys = {var: "synthetic-private-key" for var, _ in PROVIDERS.values()}
    seen = []

    def handler(request):
        seen.append((request.method, str(request.url)))
        assert request.headers["authorization"] == "Bearer synthetic-private-key"
        data = (
            {"is_free_tier": True, "label": "synthetic-private-key"}
            if request.url.path.endswith("/key")
            else [{"id": "fixed-model-2601"}]
        )
        if request.url.path == "/payment/checklist":
            return httpx.Response(
                200,
                json=dict(
                    stripe_balance=0,
                    suspended=True,
                    payment_method=False,
                    topup=False,
                    scoped_credits=[],
                    payment_method_info={"card": {"last4": "private"}},
                ),
            )
        return httpx.Response(
            200,
            json={"uuid": "synthetic-user"} if request.url.path == "/whoami" else {"data": data},
        )

    public, private = await inspect(keys, set(PROVIDERS), True, httpx.MockTransport(handler))
    assert seen == [("GET", url) for _, url in PROVIDERS.values()]
    assert "synthetic-private-key" not in json.dumps(public)
    assert all(
        row["authentication"] == "read_only_verified" for row in public["providers"].values()
    )
    assert all("credential_sha256" in row for row in private["providers"].values())


async def test_unconfirmed_or_missing_credentials_do_not_leave_the_machine():
    def forbidden(request):
        pytest.fail("HTTP without operator confirmation")

    for keys, confirmation in [({}, set(PROVIDERS)), ({"PPM_AI_GROQ_API_KEY": "private"}, set())]:
        public, _ = await inspect(keys, confirmation, True, httpx.MockTransport(forbidden))
        assert all(row["authentication"] == "not_checked" for row in public["providers"].values())


async def test_authentication_error_cannot_echo_key_or_follow_redirect():
    def handler(request):
        return httpx.Response(
            302, headers={"location": "https://attacker.invalid/key"}, text="synthetic-private-key"
        )

    public, _ = await inspect(
        {"PPM_AI_GROQ_API_KEY": "synthetic-private-key"},
        {"groq"},
        True,
        httpx.MockTransport(handler),
    )
    assert public["providers"]["groq"]["authentication"] == "unavailable"
    assert "synthetic-private-key" not in json.dumps(public)


def test_low_memory_stays_blocked_and_ollama_probe_cannot_load_a_model(monkeypatch):
    monkeypatch.setattr(local, "windows_memory", lambda: dict(total_mb=16000, available_mb=900))
    paths = []

    def handler(request):
        assert request.method == "GET"
        paths.append(request.url.path)
        return httpx.Response(200, json={"version": "test", "models": []})

    result = local.readiness("qwen3:4b", transport=httpx.MockTransport(handler))
    assert result["blocked"] == ["LOCAL_RESOURCE", "MODEL_NOT_INSTALLED"]
    assert paths == ["/api/version", "/api/tags", "/api/ps"]
    assert result["inference_requests"] == 0 and not result["qualified"]


def test_unknown_host_memory_and_external_origin_are_denied(monkeypatch):
    def unavailable():
        raise OSError

    monkeypatch.setattr(local, "windows_memory", unavailable)

    def handler(request):
        return httpx.Response(200, json={"version": "test", "models": []})

    assert (
        "HOST_MEMORY_UNAVAILABLE"
        in local.readiness("test", transport=httpx.MockTransport(handler))["blocked"]
    )
    with pytest.raises(ValueError):
        local.readiness("test", "http://attacker.invalid")


def test_other_resident_model_does_not_silently_get_replaced(monkeypatch):
    monkeypatch.setattr(local, "windows_memory", lambda: dict(total_mb=16000, available_mb=8000))

    def handler(request):
        models = (
            [{"name": "different-model"}]
            if request.url.path == "/api/ps"
            else [{"name": "test:4b", "digest": "a" * 64}]
        )
        return httpx.Response(200, json={"version": "test", "models": models})

    result = local.readiness("test:4b", transport=httpx.MockTransport(handler))
    assert result["blocked"] == ["OTHER_MODEL_RESIDENT"]
