"""Synthetic operator smoke obeys private binding, call caps and ambiguous outcomes."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest
from ppm_api.model_contracts import ModelFailure

from scripts import check_provider_setup as setup
from scripts import smoke_groq_provider as smoke


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    monkeypatch.setattr(setup, "PRIVATE", tmp_path)
    folder = tmp_path / "ai-v2"
    folder.mkdir()
    key_hash = hashlib.sha256(b"synthetic-only").hexdigest()
    (tmp_path / "ai-v2.env").write_text("PPM_AI_GROQ_API_KEY=synthetic-only\n", encoding="utf-8")
    policy = json.loads(Path("config/model-policy.example.json").read_text())
    profile = next(p for p in policy["profiles"] if p["id"] == "groq-candidate")
    profile.update(
        credential_sha256=key_hash,
        free_tier_confirmed=True,
        requests_per_minute=6,
        tokens_per_minute=24000,
    )
    (folder / "policy.json").write_text(json.dumps(policy), encoding="utf-8")
    record = dict(
        provider="groq",
        model=smoke.MODEL,
        account_scope=profile["quota_scope"],
        key_sha256=key_hash,
        corpus_sha256=smoke.CORPUS_HASH,
        synthetic_only=True,
        free_tier_confirmed=True,
        max_spend_usd="0",
        max_calls=3,
    )
    authorization = folder / "smoke-authorization.json"
    authorization.write_text(json.dumps(record), encoding="utf-8")
    return tmp_path, authorization


def response(request):
    body = json.loads(request.content)
    assert (
        request.method == "POST"
        and str(request.url) == "https://api.groq.com/openai/v1/chat/completions"
    )
    assert body["max_completion_tokens"] == 512 and body["stream"] is False
    payload = json.loads(body["messages"][1]["content"])
    content = dict(
        section=payload["section"],
        mode="findings",
        outcome="no_findings",
        covered=["e1"],
        findings=[],
        matches=[],
        narrative=[],
        gaps=[],
    )
    return httpx.Response(
        200,
        json=dict(
            model=smoke.MODEL,
            choices=[dict(finish_reason="stop", message=dict(content=json.dumps(content)))],
            usage=dict(prompt_tokens=100, completion_tokens=50),
        ),
    )


async def test_default_is_dry_run_without_network_or_promotion(prepared):
    root, authorization = prepared

    def forbidden(request):
        pytest.fail("HTTP during dry run")

    result = await smoke.run(root, authorization, 3, False, httpx.MockTransport(forbidden))
    assert result["status"] == "prepared_no_requests" and not result["attempts"]
    assert not (root / "ai-v2/groq-smoke-ledger.json").exists()
    assert not result["profile_activated"] and not result["independent_quality_qualification"]


async def test_three_calls_are_durable_and_cannot_be_repeated_same_day(prepared):
    root, authorization = prepared
    result = await smoke.run(root, authorization, 3, True, httpx.MockTransport(response))
    assert len(result["attempts"]) == 3
    assert "synthetic-only" not in json.dumps(result)
    # Deliberately wrong supported fixture is a control failure, not a quality pass.
    assert result["attempts"][0]["control_expectation_passed"] is False
    ledger = json.loads((root / "ai-v2/groq-smoke-ledger.json").read_text())
    assert len(ledger) == 3 and all(row["state"] == "completed" for row in ledger)
    with pytest.raises(ModelFailure, match="QUOTA_EXHAUSTED"):
        await smoke.run(root, authorization, 1, True, httpx.MockTransport(response))


async def test_changed_key_and_changed_corpus_are_denied_before_http(prepared):
    root, authorization = prepared
    record = json.loads(authorization.read_text())
    record["corpus_sha256"] = "a" * 64
    authorization.write_text(json.dumps(record))
    with pytest.raises(ValueError):
        await smoke.run(root, authorization, 1, True, httpx.MockTransport(response))


async def test_ambiguous_failure_stops_and_blocks_replay(prepared):
    root, authorization = prepared
    calls = []

    def timeout(request):
        calls.append(request)
        raise httpx.ReadTimeout("private diagnostic", request=request)

    result = await smoke.run(root, authorization, 3, True, httpx.MockTransport(timeout))
    assert len(calls) == 1 and result["status"] == "stopped_on_unknown"
    assert "private diagnostic" not in json.dumps(result)
    with pytest.raises(ModelFailure, match="OUTCOME_UNKNOWN"):
        await smoke.run(root, authorization, 1, True, httpx.MockTransport(response))


async def test_cooldown_stops_subsequent_requests(prepared):
    root, authorization = prepared

    def quota(request):
        return httpx.Response(429, headers={"retry-after": "120"}, text="private")

    result = await smoke.run(root, authorization, 3, True, httpx.MockTransport(quota))
    assert len(result["attempts"]) == 1 and result["attempts"][0]["code"] == "QUOTA_EXHAUSTED"
    with pytest.raises(ModelFailure, match="QUOTA_EXHAUSTED"):
        await smoke.run(root, authorization, 1, True, httpx.MockTransport(response))


async def test_logical_section_attempt_limit_survives_a_new_invocation(prepared):
    root, authorization = prepared
    ledger = [
        dict(
            state="completed",
            admitted_at=datetime.now(UTC).isoformat(),
            case="supported",
            reserved_tokens=100,
        )
        for _ in range(2)
    ]
    (root / "ai-v2/groq-smoke-ledger.json").write_text(json.dumps(ledger))

    def forbidden(request):
        pytest.fail("Third attempt for the same logical section")

    result = await smoke.run(root, authorization, 1, True, httpx.MockTransport(forbidden))
    assert result["status"] == "quota_stopped" and not result["attempts"]


def test_runtime_schema_binds_identity_before_external_decoding():
    node, context = smoke.fixture_context("missing", dict(smoke.FIXTURES)["missing"])
    schema = context["schema"]
    assert schema["properties"]["section"]["const"] == node["key"]
    assert schema["properties"]["mode"]["const"] == "findings"
    assert schema["properties"]["covered"]["items"]["enum"] == ["e1"]
    assert schema["$defs"]["SectionGap"]["properties"]["item"]["enum"] == ["e1"]
    assert "s1" not in schema["$defs"]["SectionGap"]["properties"]["item"]["enum"]
