"""Longer ordinary guided waits cannot leak into fixtures, legacy runs or other modes."""

import asyncio
from dataclasses import replace
from datetime import timedelta

import pytest
from ppm_api.modules.agents.guided_review import PROMPT
from ppm_api.modules.ai.adapters import NativeAdapter
from ppm_api.modules.ai.contracts import ModelFailure, ModelResult
from ppm_api.modules.ai.deadlines import completion_timeout
from ppm_api.modules.identity.service import now
from test_model_routing import configured as configured


@pytest.mark.parametrize(
    "snapshot,versions,provider,guided,expected",
    [
        (
            {"operation": "agents", "analysis_mode": "guided"},
            {"guided_cloud_timeout_seconds": 60},
            "gemini",
            True,
            60,
        ),
        ({"operation": "agents", "analysis_mode": "guided"}, {}, "gemini", True, 22),
        (
            {"operation": "agents", "analysis_mode": "guided", "guided_pilot_id": "fixture"},
            {"guided_cloud_timeout_seconds": 60},
            "gemini",
            True,
            22,
        ),
        (
            {"operation": "agents", "analysis_mode": "guided"},
            {"guided_cloud_timeout_seconds": 60},
            "ollama",
            True,
            22,
        ),
        (
            {"operation": "agents", "analysis_mode": "domain"},
            {"guided_cloud_timeout_seconds": 60},
            "groq",
            False,
            22,
        ),
    ],
)
def test_timeout_scope(settings, snapshot, versions, provider, guided, expected):
    assert (
        completion_timeout(settings, dict(snapshot=snapshot, versions=versions), provider, guided)
        == expected
    )


@pytest.mark.parametrize("value", [True, "60", 61, 0])
def test_corrupt_frozen_bound_fails_closed(settings, value):
    with pytest.raises(ModelFailure):
        completion_timeout(
            settings,
            dict(
                snapshot=dict(operation="agents", analysis_mode="guided"),
                versions=dict(guided_cloud_timeout_seconds=value),
            ),
            "gemini",
            True,
        )


def test_operator_can_reduce_but_not_extend_frozen_wait(settings):
    run = dict(
        snapshot=dict(operation="agents", analysis_mode="guided"),
        versions=dict(guided_cloud_timeout_seconds=40),
    )
    assert completion_timeout(settings, run, "gemini", True) == 40
    settings.ai_guided_cloud_timeout_seconds = 30
    assert completion_timeout(settings, run, "gemini", True) == 30


@pytest.mark.parametrize(
    "task,system,permit_limit,timeout",
    [
        ("risk_extraction", PROMPT, 60, 60),
        ("guided_selection", "fixture prompt", 60, 60),
        ("guided_selection", PROMPT, 22, 60),
        ("guided_selection", PROMPT, 61, 61),
    ],
)
def test_adapter_rejects_unadmitted_or_nonordinary_long_wait(
    configured, task, system, permit_limit, timeout
):
    settings, profile, _, request = configured
    profile = profile.model_copy(update=dict(provider="gemini"))
    request = replace(
        request,
        task_class=task,
        system=system,
        timeout=timeout,
        permit=replace(request.permit, provider_id="gemini", timeout_seconds=permit_limit),
    )
    with pytest.raises(ModelFailure, match="CONFIGURATION"):
        NativeAdapter(settings, profile).permit(request)


async def test_actual_delayed_response_past_old_deadline_is_accepted(configured, monkeypatch):
    settings, profile, _, request = configured
    profile = profile.model_copy(update=dict(provider="groq"))
    request = replace(
        request,
        timeout=60,
        permit=replace(
            request.permit, expires_at=now() + timedelta(seconds=60), timeout_seconds=60
        ),
    )
    adapter = NativeAdapter(settings, profile)
    # Admission/permit boundaries are tested separately; this is an offline timer test.
    monkeypatch.setattr(adapter, "permit", lambda _: None)
    seen = []

    async def delayed(*args):
        seen.append(True)
        await asyncio.sleep(23)
        return ModelResult(
            attempt_id=request.permit.attempt_id,
            provider_id="groq",
            model_id=profile.model,
            completion="complete",
            text="{}",
        )

    monkeypatch.setattr(adapter, "cloud_chat", delayed)
    assert (await adapter.execute(request)).completion == "complete"
    assert len(seen) == 1


async def test_expiring_permit_bounds_wait_and_retains_unknown(configured, monkeypatch):
    settings, profile, _, request = configured
    profile = profile.model_copy(update=dict(provider="groq"))
    request = replace(
        request,
        timeout=60,
        permit=replace(
            request.permit, expires_at=now() + timedelta(seconds=0.1), timeout_seconds=60
        ),
    )
    adapter = NativeAdapter(settings, profile)
    monkeypatch.setattr(adapter, "permit", lambda _: None)
    seen = []

    async def stalled(*args):
        seen.append(True)
        await asyncio.sleep(10)

    monkeypatch.setattr(adapter, "cloud_chat", stalled)
    with pytest.raises(ModelFailure) as failure:
        await adapter.execute(request)
    assert failure.value.code == "TIMEOUT" and failure.value.certainty == "unknown"
    assert len(seen) == 1
