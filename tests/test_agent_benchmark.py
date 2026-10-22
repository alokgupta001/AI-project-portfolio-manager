"""Corpus, benchmark admission and independent review tests; no model is qualified."""

import json
from copy import deepcopy
from uuid import UUID, uuid4

import httpx
import pytest
from ppm_api.agent_planner import build_plan
from ppm_api.agent_registry import REGISTRY
from ppm_api.agent_schemas import AnalysisInput
from ppm_api.model_contracts import CapabilityDetail, ModelFailure, SectionOutput
from ppm_api.model_registry import ModelProfile
from pydantic import ValidationError

from scripts import benchmark_agent_runtime as B
from scripts.score_agent_benchmark import review_template, score
from scripts.score_agent_benchmark import sha as file_sha


def profile():
    return ModelProfile(
        id="local-test",
        provider="ollama",
        model="qwen3:4b",
        quota_scope="local-host",
        billing_class="local",
        installed_digest="a" * 64,
        requests_per_minute=10,
        requests_per_day=100,
        tokens_per_minute=100000,
    )


def corpus():
    return B.load_corpus(B.CORPUS)


def test_corpus_has_all_classes_and_holdouts_and_never_packs_labels():
    data, corpus_hash = corpus()
    assert len(corpus_hash) == 64
    assert data["label_status"] == "draft_requires_independent_review"
    for capability in REGISTRY:
        rows = [c for c in data["cases"] if c["task_class"] == capability.task_class]
        assert len(rows) == 12 and sum(c["split"] == "held_out" for c in rows) == 6
        assert {c["scenario"] for c in rows} >= {"supported", "absent", "conflicting", "injection"}
    for case in data["cases"]:
        node, packed = B.fixture_context(case)
        assert node["agent"] == case["agent"] and packed["required_aliases"]
        payload = json.loads(packed["payload"])
        assert not {"labels", "split", "scenario", "supported_items"} & payload.keys()
        assert case["labels"]["interpretation_rubric"] not in packed["payload"]
        # Decoder labels and required coverage agree even for aggregate advice/rubric/synthesis.
        assert set(packed["required_aliases"]) <= set(
            packed["schema"]["properties"]["covered"]["items"]["enum"]
        )


@pytest.mark.parametrize("entry", REGISTRY, ids=lambda e: e.agent)
@pytest.mark.parametrize("control", ["metrics", "scope", "no_model", "malicious_authority"])
def test_each_role_baseline_and_control_cases(entry, control):
    data, _ = corpus()
    case = next(c for c in data["cases"] if c["agent"] == entry.agent)
    node, packed = B.fixture_context(case)
    if control == "metrics":
        snapshot = dict(sources=[], framework=None, answers={})
        plan = build_plan(
            snapshot,
            AnalysisInput(
                project_id=uuid4(),
                analysis_mode="metrics",
                requested_agents=[entry.agent],
            ),
        )
        assert not any(n["kind"] == "semantic" for n in plan["nodes"])
    elif control == "scope":
        assert all(entry.agent in s["permitted_agents"] for s in packed["evidence"].values())
        assert "raw_personnel_notes" not in packed["payload"]
        assert set(packed["subjects"]) == {"s1"}
    elif control == "no_model":
        with pytest.raises(ValidationError):
            CapabilityDetail(
                agent=entry.agent, base_outcome="supported", semantic_outcome="completed"
            )
    else:
        with pytest.raises(ValidationError):
            SectionOutput(
                section=node["key"],
                mode=node["mode"],
                outcome="no_findings",
                covered=packed["required_aliases"],
                approve=True,
            )


async def test_dry_run_cannot_make_http_and_does_not_create_ledger(tmp_path):
    data, corpus_hash = corpus()

    def refuse(request):
        raise AssertionError("Dry-run attempted HTTP")

    result = await B.run(
        data["cases"][:1],
        corpus_hash,
        profile(),
        tmp_path,
        False,
        4096,
        512,
        0,
        httpx.MockTransport(refuse),
    )
    assert result["status"] == "prepared_no_requests" and not result["attempts"]
    assert not list(tmp_path.iterdir())


def test_new_artifact_hash_survives_lf_checkout(tmp_path):
    path = tmp_path / "bound-review.json"
    B.write_new(path, {"evidence": "Original Unicode evidence: café."})
    original = path.read_bytes()
    assert original == original.replace(b"\r\n", b"\n")
    with pytest.raises(FileExistsError):
        B.write_new(path, {"evidence": "replacement"})
    assert path.read_bytes() == original


async def test_memory_failure_never_generates_or_forges_latency(monkeypatch, tmp_path):
    data, corpus_hash = corpus()
    monkeypatch.setattr(
        B,
        "readiness",
        lambda *a, **k: dict(
            blocked=["LOCAL_RESOURCE"],
            model_digest="a" * 64,
        ),
    )
    result = await B.run(data["cases"][:1], corpus_hash, profile(), tmp_path, True, 4096, 512, 0)
    assert result["status"] == "blocked_preflight" and not result["attempts"]
    assert "p95_warm_seconds" not in result and not result["qualified_classes"]
    assert not (tmp_path / "local-benchmark.lock").exists()


async def test_unknown_attempt_survives_restart(monkeypatch, tmp_path):
    data, corpus_hash = corpus()
    B.save_ledger(tmp_path / "local-benchmark-ledger.json", [dict(state="unknown")])
    monkeypatch.setattr(B, "readiness", lambda *a, **k: pytest.fail("Replayed unknown attempt"))
    with pytest.raises(ModelFailure, match="OUTCOME_UNKNOWN"):
        await B.run(data["cases"][:1], corpus_hash, profile(), tmp_path, True, 4096, 512, 0)


@pytest.fixture
def missing_benchmark(monkeypatch):
    data, _ = corpus()
    case = data["cases"][6]
    posts = []
    monkeypatch.setattr(
        B,
        "readiness",
        lambda *a, **k: dict(
            blocked=[], model_digest="a" * 64, hardware=dict(memory=dict(total_mb=16000))
        ),
    )
    monkeypatch.setattr(B, "windows_memory", lambda: dict(available_mb=10000, total_mb=16000))
    monkeypatch.setattr(B, "ollama_rss_mb", lambda: 4000)

    def respond(request):
        if request.url.path == "/api/ps":
            return httpx.Response(200, json=dict(models=[]))
        if request.url.path == "/api/tags":
            return httpx.Response(200, json=dict(models=[dict(name="qwen3:4b", digest="a" * 64)]))
        body = json.loads(request.content)
        posts.append(body)
        payload = json.loads(body["messages"][-1]["content"])
        output = dict(
            section=payload["section"],
            mode=payload["mode"],
            outcome="insufficient_evidence",
            gaps=[dict(item=payload["required"][0], code="missing_evidence")],
        )
        return httpx.Response(
            200,
            json=dict(
                done=True,
                done_reason="stop",
                message=dict(content=json.dumps(output)),
                eval_count=32,
            ),
        )

    return case, httpx.MockTransport(respond), posts


async def test_logical_attempts_survive_output_corpus_and_case_name_changes(
    missing_benchmark, tmp_path
):
    case, transport, posts = missing_benchmark
    for output in (512, 256):
        result = await B.run(
            [case], "a" * 64, profile(), tmp_path, True, 4096, output, 0, transport
        )
        assert result["status"] == "completed_pending_review"
    renamed = deepcopy(case)
    renamed["id"] = "renamed-without-new-evidence"
    result = await B.run([renamed], "b" * 64, profile(), tmp_path, True, 4096, 512, 0, transport)
    assert result["status"] == "logical_attempt_limit"
    assert len(posts) == 2
    ledger = json.loads((tmp_path / "local-benchmark-ledger.json").read_text())
    assert len(ledger) == 2 and ledger[0]["root"] == ledger[1]["root"]


async def test_reordered_sources_cannot_renew_quality_attempts(missing_benchmark, tmp_path):
    case, transport, posts = missing_benchmark
    assert len(case["sources"]) == 2
    for _ in range(2):
        result = await B.run([case], "a" * 64, profile(), tmp_path, True, 4096, 512, 0, transport)
        assert result["status"] == "completed_pending_review"
    reordered = deepcopy(case)
    reordered["sources"].reverse()
    result = await B.run([reordered], "b" * 64, profile(), tmp_path, True, 4096, 512, 0, transport)
    assert result["status"] == "logical_attempt_limit" and len(posts) == 2


@pytest.mark.parametrize("root_version", [None, 2])
async def test_legacy_opaque_roots_fail_closed_without_rewriting_history(
    monkeypatch, tmp_path, root_version
):
    data, corpus_hash = corpus()
    path = tmp_path / "local-benchmark-ledger.json"
    row = dict(root="old-format-root", state="completed")
    if root_version is not None:
        row["root_version"] = root_version
    B.save_ledger(path, [row])
    before = path.read_bytes()
    monkeypatch.setattr(B, "readiness", lambda *a, **k: pytest.fail("Admitted legacy history"))
    with pytest.raises(ValueError, match="Legacy benchmark ledger"):
        await B.run(data["cases"][:1], corpus_hash, profile(), tmp_path, True, 4096, 512, 0)
    assert path.read_bytes() == before


async def test_warm_timing_does_not_consume_or_replace_quality_attempts(
    missing_benchmark, tmp_path
):
    case, transport, posts = missing_benchmark
    first = await B.run([case], "a" * 64, profile(), tmp_path, True, 4096, 512, 1, transport)
    assert [r["timing_only"] for r in first["attempts"]] == [False, True]
    second = await B.run([case], "a" * 64, profile(), tmp_path, True, 4096, 256, 0, transport)
    assert second["status"] == "completed_pending_review"
    final = await B.run([case], "b" * 64, profile(), tmp_path, True, 4096, 512, 0, transport)
    assert final["status"] == "logical_attempt_limit" and len(posts) == 3


async def test_explicit_budget_and_context_fail_before_inference(tmp_path):
    data, corpus_hash = corpus()
    with pytest.raises(ValueError, match="Warm measurements"):
        await B.run(
            data["cases"][:1], corpus_hash, profile(), tmp_path, False, 4096, 512, 1, keep_alive=0
        )
    with pytest.raises(ValueError, match="Thirty calls"):
        await B.run(data["cases"][:30], corpus_hash, profile(), tmp_path, False, 4096, 512, 1)
    case = deepcopy(data["cases"][0])
    case["sources"][0]["text"] = "X" * 12000
    with pytest.raises(ModelFailure, match="CONTEXT_LIMIT"):
        await B.run([case], corpus_hash, profile(), tmp_path, False, 4096, 512, 0)


def test_draft_review_and_empty_measurements_cannot_qualify():
    data, corpus_hash = corpus()
    review = review_template(data, corpus_hash)
    with pytest.raises(ValueError, match="Independent label review"):
        score(data, corpus_hash, review, [])


def test_every_fixture_fits_bounded_context_without_expected_answers():
    data, _ = corpus()
    for case in data["cases"]:
        _, context = B.fixture_context(case)
        assert context["input_tokens"] + len(B.PROMPT.encode()) + 512 + 256 <= 4096


def test_memory_inventory_includes_runner_descendants_without_unrelated_processes():
    processes = [
        (30, 20, "runner.exe"),
        (10, 1, "OLLAMA.EXE"),
        (20, 10, "model-server.exe"),
        (40, 99, "runner.exe"),
        (99, 1, "unrelated.exe"),
        (50, 1, "ollama_llama_server.exe"),
    ]
    assert B.ollama_process_ids(processes) == {10, 20, 30, 50}


def test_review_must_match_candidate_and_can_reject_real_citation(tmp_path):
    data, corpus_hash = corpus()
    case = next(c for c in data["cases"] if c["agent"] == "risk")
    node, context = B.fixture_context(case)
    attempt_id = str(uuid4())
    output = dict(
        section=node["key"],
        mode="findings",
        outcome="supported",
        covered=["e1"],
        findings=[
            dict(
                subject="s1",
                predicate="risk_present",
                kind="risk",
                signal="adverse",
                severity="medium",
                claim="An unrelated risk exists.",
                advice="Review an unrelated concern.",
                epistemic="interpretation",
                spans=[dict(e="e1", start=0, end=10)],
            )
        ],
    )
    # Real offsets pass hard checks even though this deliberately unsupported interpretation
    # must receive a semantic failure from the independent reviewer.
    from ppm_api.agent_validation import validate_section

    validate_section(node, context, SectionOutput(**output))
    candidate = tmp_path / (attempt_id + ".json")
    B.write_new(
        candidate,
        dict(
            attempt_id=attempt_id,
            provider_id="ollama",
            model_id="qwen3:4b",
            completion="complete",
            text=json.dumps(output),
        ),
    )
    row = dict(
        attempt_id=attempt_id,
        case=case["id"],
        timing_only=False,
        cold=True,
        candidate_sha256=file_sha(candidate),
        end_to_end_seconds=1,
        samples=[dict(available_mb=4000, ollama_rss_mb=3000)],
    )
    report = dict(
        schema_version="agent-benchmark-v1",
        model_digest="a" * 64,
        corpus_sha256=corpus_hash,
        prompt_sha256="b" * 64,
        context_tokens=4096,
        output_tokens=512,
        hardware_record_sha256="c" * 64,
        attempts=[row]
        + [dict(row, attempt_id=str(uuid4()), timing_only=True, cold=False) for _ in range(5)],
    )
    review = review_template(data, corpus_hash)
    review["label_review"] = dict(
        id="synthetic-test-only",
        reviewer="unit-test",
        independent=True,
        reviewed_before_inference=True,
    )
    rating = next(r for r in review["cases"] if r["case"] == case["id"])
    rating.update(
        attempt_id=attempt_id,
        candidate_sha256=file_sha(candidate),
        correct_claims=0,
        recalled_items=0,
        correct_abstention=False,
        canonical_preserved=True,
        supported_added_interpretations=0,
        citation_errors=0,
        unsupported_numbers=0,
        privacy_or_control_errors=0,
        advice_relevant=False,
        material_omissions=1,
        review_note="Cited text does not support this interpretation or advice.",
    )
    result = score(data, corpus_hash, review, [report], tmp_path)
    assert result.classes[0].correct_claims == 0 and not result.qualified_classes()
    rating["candidate_sha256"] = ""
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        score(data, corpus_hash, review, [report], tmp_path)
    review["label_review"] = dict(
        id="unit-test-only", reviewer="synthetic", independent=True, reviewed_before_inference=True
    )
    with pytest.raises(ValueError, match="Measured reports"):
        score(data, corpus_hash, review, [])


@pytest.mark.parametrize("keep_alive", [0, 60])
async def test_transport_complete_is_still_pending_independent_review(
    monkeypatch, tmp_path, keep_alive
):
    data, corpus_hash = corpus()
    case = data["cases"][6]  # Explicit missing evidence, not a positive quality label.
    monkeypatch.setattr(
        B,
        "readiness",
        lambda *a, **k: dict(
            blocked=[],
            model_digest="a" * 64,
            hardware=dict(memory=dict(total_mb=16000)),
        ),
    )
    monkeypatch.setattr(B, "windows_memory", lambda: dict(available_mb=10000, total_mb=16000))
    monkeypatch.setattr(B, "ollama_rss_mb", lambda: 4000)
    node, context = B.fixture_context(case)
    payload = dict(
        section=node["key"],
        mode=node["mode"],
        outcome="insufficient_evidence",
        gaps=[dict(item=context["required_aliases"][0], code="missing_evidence")],
    )

    def respond(request):
        if request.url.path == "/api/ps":
            return httpx.Response(200, json=dict(models=[]))
        if request.url.path == "/api/tags":
            return httpx.Response(200, json=dict(models=[dict(name="qwen3:4b", digest="a" * 64)]))
        body = json.loads(request.content)
        assert body["think"] is False and body["options"]["num_predict"] == 512
        assert body["keep_alive"] == keep_alive
        return httpx.Response(
            200,
            json=dict(
                done=True,
                done_reason="stop",
                message=dict(content=json.dumps(payload)),
                eval_count=32,
            ),
        )

    result = await B.run(
        [case],
        corpus_hash,
        profile(),
        tmp_path,
        True,
        4096,
        512,
        0,
        httpx.MockTransport(respond),
        keep_alive=keep_alive,
    )
    assert result["status"] == "completed_pending_review" and not result["qualified_classes"]
    attempt = result["attempts"][0]
    assert attempt["hard_validation"] == "partially_validated"
    assert UUID(attempt["attempt_id"]) and attempt["samples"]
    assert (
        json.loads((tmp_path / "local-benchmark-ledger.json").read_text())[0]["state"]
        == "completed"
    )
