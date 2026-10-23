"""Batch isolation, per-role gates, call bounds and durable cross-format history."""

import json
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import httpx
import pytest
from ppm_api.agent_batch import batch_prompt, pack_batch, validate_batch
from ppm_api.agent_planner import build_plan
from ppm_api.agent_registry import BY_AGENT
from ppm_api.agent_runtime import batch_window_delay, live_sections
from ppm_api.agent_schemas import AnalysisInput
from ppm_api.agent_validation import PREDICATES
from ppm_api.model_adapters import NativeAdapter
from ppm_api.model_contracts import ModelFailure, ModelResult, ModelUsage
from ppm_api.model_registry import ModelPolicy, digest
from ppm_api.model_router import candidates
from test_agent_planner import snapshot
from test_cloud_specialists import calibration as calibration
from test_model_routing import configured as configured

from scripts import benchmark_cloud_batches as B
from scripts.benchmark_agent_runtime import CLOUD_CORPUS, CORPUS, load_corpus
from scripts.benchmark_cloud_batches import fixture_batch
from scripts.benchmark_cloud_specialists import check_admission
from scripts.prepare_cloud_acceptance import approval, prepare_authorization
from scripts.score_agent_benchmark import review_template, sha
from scripts.score_cloud_benchmark import score


def cases(*ids):
    corpus, _ = load_corpus(CORPUS)
    return [next(c for c in corpus["cases"] if c["id"] == cid) for cid in ids]


def compact(role, context):
    value = dict(
        state="supported",
        covered=context["required_aliases"],
        cites=["e1"],
        claim="The cited concern requires review.",
        advice="Check the evidence with its owner.",
        epistemic="interpretation",
    )
    if role in ("pmo", "executive", "sentiment"):
        value["basis"] = list(context["basis"])[:1]
    else:
        value.update(
            predicate=sorted(PREDICATES[role] - {"no_adverse_evidence"})[0],
            signal="adverse",
            kind="risk",
            severity="medium",
        )
    return value


def test_all_nine_plan_has_four_calls_and_real_synthesis_dependencies():
    data = snapshot()
    plan = build_plan(data, AnalysisInput(project_id=uuid4(), analysis_mode="all_specialists"))
    batches = [n for n in plan["nodes"] if n["kind"] == "semantic"]
    assert len(batches) == 4 and len(plan["nodes"]) == 13
    assert {m["agent"] for n in batches for m in n["members"]} == set(BY_AGENT)
    assert "portfolio-batch" in batches[-1]["dependencies"]
    assert {"delivery-batch", "assurance-batch"} <= set(batches[-2]["dependencies"])
    assert not any(n["kind"] == "evaluator" for n in plan["nodes"])
    seen = set()
    for node in plan["nodes"]:
        assert set(node["dependencies"]) <= seen
        seen.add(node["key"])


def test_batch_roles_cannot_cover_or_cite_each_others_aliases():
    node, ctx = fixture_batch(cases("financial_05", "schedule_05", "resource_05"))
    values = {r: compact(r, c) for r, c in ctx["members"].items()}
    checked = validate_batch(node, ctx, values)
    assert set(checked["members"]) == {"financial", "schedule", "resource"}
    values["financial"]["covered"] = ["e2"]
    with pytest.raises(ModelFailure):
        validate_batch(node, ctx, values)
    values["financial"] = compact("financial", ctx["members"]["financial"])
    values["financial"]["cites"] = ["e2"]
    with pytest.raises(ModelFailure):
        validate_batch(node, ctx, values)


def test_no_adverse_predicate_cannot_report_an_adverse_signal():
    node, ctx = fixture_batch(cases("governance_01"))
    values = {"governance": compact("governance", ctx["members"]["governance"])}
    assert validate_batch(node, ctx, values)["members"]["governance"]["findings"]
    # Reproduces the contradictory metadata in the independently reviewed Puter output.
    values["governance"]["predicate"] = "no_adverse_evidence"
    with pytest.raises(ModelFailure, match="INVALID_OUTPUT"):
        validate_batch(node, ctx, values)


@pytest.mark.parametrize(
    "change", ["number", "foreign", "extra_role", "missing_role", "duplicate_cite", "clear_metric"]
)
def test_invalid_member_rejects_whole_batch(change):
    node, ctx = fixture_batch(cases("financial_05", "resource_05"))
    values = {r: compact(r, c) for r, c in ctx["members"].items()}
    if change == "number":
        values["financial"]["advice"] = "Reduce costs by 10 percent."
    if change == "foreign":
        values["resource"]["cites"] = ["e99"]
    if change == "extra_role":
        values["risk"] = {}
    if change == "missing_role":
        del values["resource"]
    if change == "duplicate_cite":
        values["financial"]["cites"] = ["e1", "e1"]
    if change == "clear_metric":
        values["resource"]["signal"] = "clear"
    with pytest.raises(ModelFailure):
        validate_batch(node, ctx, values)


def test_batch_eligibility_requires_every_member_class(configured):
    settings, profile, _, req = configured
    from ppm_api.model_router import RouteRequirements

    requirements = RouteRequirements(
        req.tenant,
        req.project,
        "risk_extraction",
        100,
        additional_task_classes=("governance_interpretation",),
    )
    profile = profile.model_copy(update={"qualified_task_classes": ["risk_extraction"]})
    assert (
        candidates(ModelPolicy(profiles=[profile]), requirements, settings)[1][profile.id]
        == "QUALITY_UNVERIFIED"
    )
    profile = profile.model_copy(
        update={
            "qualified_task_classes": ["risk_extraction", "governance_interpretation"],
            "assigned_task_classes": ["risk_extraction"],
        }
    )
    assert (
        candidates(ModelPolicy(profiles=[profile]), requirements, settings)[1][profile.id]
        == "ROLE_NOT_ASSIGNED"
    )


def test_batch_wait_respects_one_minute_and_deadline(configured):
    from types import SimpleNamespace

    instant = datetime.now(UTC)
    profile = SimpleNamespace(provider="groq", requests_per_minute=1)
    rows = [dict(provider_id="groq", started_at=instant - timedelta(seconds=10))]
    assert batch_window_delay(rows, profile, instant, instant + timedelta(seconds=80), 22) == 51
    with pytest.raises(ModelFailure, match="DEADLINE_EXCEEDED"):
        batch_window_delay(rows, profile, instant, instant + timedelta(seconds=70), 22)
    assert (
        batch_window_delay(
            rows, profile, instant + timedelta(seconds=62), instant + timedelta(seconds=100), 22
        )
        == 0
    )


def test_batch_revocation_withholds_all_members_including_no_findings():
    node, ctx = fixture_batch(cases("financial_05", "resource_05"))
    values = {
        r: dict(state="no_findings", covered=c["required_aliases"])
        for r, c in ctx["members"].items()
    }
    result = validate_batch(node, ctx, values)
    sources = list(ctx["evidence"].values())
    # Whole source refs are bound even when no findings exist.
    task = dict(id="t", resolved_context_manifest=ctx)
    section = dict(task_id="t", result=result, section_id="batch")
    current = {s["source"]: s for s in sources}
    assert {
        s["agent"] for s in live_sections(dict(sources=sources), [section], [task], current)
    } == set(values)
    changed = deepcopy(current)
    changed[sources[0]["source"]]["sha256"] = "changed"
    assert not live_sections(dict(sources=sources), [section], [task], changed)


def test_batched_and_individual_attempts_share_case_exhaustion():
    from ppm_api.model_registry import ModelProfile

    p = ModelProfile(
        id="probe",
        provider="groq",
        model="fixed",
        quota_scope="scope",
        requests_per_day=20,
        requests_per_minute=1,
        tokens_per_minute=8000,
    )
    stamp = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
    rows = [
        dict(root="same", state="completed", admitted_at=stamp, reserved_tokens=1),
        dict(roots=["same", "other"], state="completed", admitted_at=stamp, reserved_tokens=1),
    ]
    with pytest.raises(ModelFailure):
        check_admission(p, dict(max_calls=15), rows, [], "same", 100, 0, datetime.now(UTC))
    check_admission(p, dict(max_calls=15), rows, [], "other", 100, 0, datetime.now(UTC))


def test_real_packer_isolated_and_private_answers_rejected():
    data = snapshot()
    plan = build_plan(data, AnalysisInput(project_id=uuid4(), analysis_mode="all_specialists"))
    node = next(n for n in plan["nodes"] if n.get("members"))
    live = {s["source"]: s for s in data["sources"]}
    ctx = pack_batch(data, node, live, [])
    payload = json.loads(ctx["payload"])
    assert set(payload) == {"financial", "schedule", "resource"}
    assert all("source-risk" not in json.dumps(v) for v in payload.values())
    assert len(batch_prompt(node)) < 2000
    data["sources"][0]["kind"] = "answer"
    with pytest.raises(ModelFailure, match="UNSUPPORTED_CAPABILITY"):
        pack_batch(data, node, live, [])


@pytest.fixture
def repair(calibration, monkeypatch, settings):
    folder, profile = calibration
    (folder / "groq-specialist-ledger.json").write_text("[]", encoding="utf-8")
    monkeypatch.setattr(B, "read_keys", lambda p: {profile.credential_ref: "synthetic-key"})
    monkeypatch.setattr(B, "gemini_settings", lambda: settings)
    monkeypatch.setattr(B, "retained_history", lambda *args: [])
    B.prepare_phase("groq", folder)
    return folder, profile


async def test_repair_dry_run_keeps_original_authorization_and_rejects_holdout(repair):
    folder, _ = repair
    original = (folder / "groq-specialist-authorization.json").read_bytes()

    def forbid(req):
        raise AssertionError("No HTTP")

    r = await B.run(
        "groq",
        ["financial_05", "schedule_05", "resource_05"],
        False,
        folder,
        httpx.MockTransport(forbid),
    )
    assert r["status"] == "prepared_no_requests" and not r["attempts"]
    assert json.loads((folder / "groq-specialist-ledger.json").read_bytes()) == []
    assert (folder / "groq-specialist-authorization.json").read_bytes() == original
    with pytest.raises(ValueError):
        await B.run("groq", ["risk_02"], True, folder, httpx.MockTransport(forbid))


async def test_batch_unknown_blocks_replay_and_retains_each_case_root(repair):
    folder, _ = repair
    seen = []

    def lose(req):
        seen.append(req)
        raise httpx.ReadTimeout("lost", request=req)

    r = await B.run(
        "groq", ["financial_05", "resource_05"], True, folder, httpx.MockTransport(lose)
    )
    assert r["status"] == "stopped_on_unknown"
    rows = json.loads((folder / "groq-specialist-ledger.json").read_bytes())
    assert len(rows) == 1 and len(rows[0]["roots"]) == 2 and rows[0]["state"] == "unknown"
    with pytest.raises(ModelFailure, match="OUTCOME_UNKNOWN"):
        await B.run("groq", ["financial_05"], True, folder, httpx.MockTransport(lose))
    assert len(seen) == 1


@pytest.mark.parametrize(
    "message,code",
    [
        ("Generated JSON does not match expected schema", "INVALID_OUTPUT"),
        ("max completion tokens reached before generating a valid document", "TRUNCATED"),
    ],
)
async def test_groq_schema_errors_are_repairable_but_counted(configured, message, code):
    settings, profile, _, _ = configured
    profile = profile.model_copy(update={"provider": "groq"})
    captured = []
    transport = httpx.MockTransport(
        lambda req: httpx.Response(
            400, json={"error": {"code": "json_validate_failed", "message": message}}
        )
    )
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ModelFailure, match=code) as exc:
            await NativeAdapter(settings, profile, checkpoint_response=captured.append).read(
                client, "POST", "https://synthetic.invalid", {}
            )
    assert exc.value.certainty == "completed" and len(captured) == 1


def test_cloud_review_cannot_approve_itself_or_ignore_frozen_strategy():
    corpus, corpus_hash = load_corpus(CORPUS)
    draft = review_template(corpus, corpus_hash)
    draft["schema_version"] = "cloud-review-v1"
    draft["strategy_sha256"] = B.strategy_hash()
    draft["label_review"] = dict(
        independent=False, id=None, reviewer=None, reviewed_before_held_out_inference=False
    )
    with pytest.raises(ValueError, match="Independent"):
        score(corpus, corpus_hash, draft, [])


def test_fresh_acceptance_cases_are_unseen_distinct_and_prepare_offline():
    fresh, _ = load_corpus(CLOUD_CORPUS)
    old, _ = load_corpus(CORPUS)
    assert {c["id"] for c in fresh["cases"]}.isdisjoint({c["id"] for c in old["cases"]})
    assert (
        len(fresh["cases"]) == 108 and sum(c["split"] == "held_out" for c in fresh["cases"]) == 54
    )
    assert len([c for c in fresh["cases"] if c.get("rubric")]) == 2
    old_inputs = {json.dumps(c["sources"], sort_keys=True) for c in old["cases"]}
    for case in fresh["cases"]:
        assert json.dumps(case["sources"], sort_keys=True) not in old_inputs
        _, context = fixture_batch([case])
        assert "interpretation_rubric" not in context["payload"]


async def test_independent_approval_is_required_before_heldout_cloud_prepare(repair, tmp_path):
    folder, profile = repair
    _, corpus_hash = load_corpus(CLOUD_CORPUS)
    path = tmp_path / "synthetic-review.json"
    value = dict(
        corpus_sha256=corpus_hash,
        strategy_sha256=B.strategy_hash(),
        label_review=dict(
            id="synthetic-test-only",
            reviewer="synthetic-test-reviewer",
            independent=False,
            approved_at=(datetime.now(UTC) - timedelta(hours=1)).isoformat(),
            reviewed_before_held_out_inference=True,
        ),
    )
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="Independent"):
        prepare_authorization("groq", path, corpus_hash, B.strategy_hash(), folder)
    assert not (folder / "groq-acceptance-authorization.json").exists()
    value["label_review"]["independent"] = True
    path.write_text(json.dumps(value), encoding="utf-8")
    record = prepare_authorization("groq", path, corpus_hash, B.strategy_hash(), folder)
    assert record["prior_calls"] == 0 and record["max_calls"] == 36
    profile.assigned_task_classes = [
        "team_support_advice",
        "portfolio_synthesis",
        "executive_synthesis",
    ]
    (folder / "policy.json").write_text(
        ModelPolicy(profiles=[profile]).model_dump_json(), encoding="utf-8"
    )

    def forbid(req):
        raise AssertionError("Dry run cannot infer")

    report = await B.run(
        "groq",
        ["cloud_executive_02"],
        False,
        folder,
        httpx.MockTransport(forbid),
        acceptance_review=path,
        corpus_path=CLOUD_CORPUS,
    )
    assert report["status"] == "prepared_no_requests" and not report["attempts"]
    assert json.loads((folder / "groq-specialist-ledger.json").read_bytes()) == []
    value["strategy_sha256"] = "changed"
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        approval(path, corpus_hash, B.strategy_hash())


def test_cloud_score_binds_approval_candidate_and_complete_ledger_without_qualifying(tmp_path):
    corpus, corpus_hash = load_corpus(CLOUD_CORPUS)
    case = next(c for c in corpus["cases"] if c["id"] == "cloud_executive_01")
    node, ctx = fixture_batch([case])
    label = dict(
        id="synthetic-only",
        reviewer="synthetic-reviewer",
        independent=True,
        approved_at=(datetime.now(UTC) - timedelta(hours=1)).isoformat(),
        reviewed_before_held_out_inference=True,
    )
    approval_path = tmp_path / "approval.json"
    approval_path.write_text(
        json.dumps(
            dict(corpus_sha256=corpus_hash, strategy_sha256=B.strategy_hash(), label_review=label)
        ),
        encoding="utf-8",
    )
    aid = uuid4()
    result = ModelResult(
        attempt_id=aid,
        provider_id="groq",
        model_id="openai/gpt-oss-20b",
        completion="complete",
        text=json.dumps(dict(executive=compact("executive", ctx["members"]["executive"]))),
        latency_ms=1000,
        usage=ModelUsage(output_tokens=100, source="reported"),
    )
    candidate = tmp_path / ("cloud-candidate-" + str(aid) + ".json")
    candidate.write_text(result.model_dump_json(), encoding="utf-8")
    report = dict(
        schema_version="cloud-batch-calibration-v1",
        provider="groq",
        model=result.model_id,
        corpus_sha256=corpus_hash,
        strategy_sha256=B.strategy_hash(),
        label_approval_sha256=sha(approval_path),
        max_output_tokens=512,
        context_tokens=8192,
        selected_cases=[case["id"]],
        prompt_sha256=digest(batch_prompt(node)),
        request_sha256=digest([batch_prompt(node), ctx["payload"], ctx["schema"]]),
        attempts=[
            dict(
                attempt_id=str(aid),
                cases=[case["id"]],
                candidate_sha256=sha(candidate),
                admitted_at=datetime.now(UTC).isoformat(),
            )
        ],
    )
    review = review_template(corpus, corpus_hash)
    review.update(
        schema_version="cloud-review-v1",
        provider="groq",
        strategy_sha256=B.strategy_hash(),
        label_review=label,
        label_approval_sha256=sha(approval_path),
        reports=["a" * 64],
    )
    row = next(r for r in review["cases"] if r["case"] == case["id"])
    row.update(
        attempt_id=str(aid),
        candidate_sha256=sha(candidate),
        correct_claims=1,
        recalled_items=1,
        correct_abstention=False,
        canonical_preserved=True,
        supported_added_interpretations=1,
        citation_errors=0,
        unsupported_numbers=0,
        privacy_or_control_errors=0,
        advice_relevant=True,
        material_omissions=0,
        review_note="Synthetic test only; no actual human approval.",
    )
    ledger = tmp_path / "groq-specialist-ledger.json"
    ledger.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="All bound"):
        score(corpus, corpus_hash, review, [report], tmp_path, approval_path)
    history = dict(
        attempt_id=str(aid),
        phase="acceptance-v1",
        corpus_sha256=corpus_hash,
        strategy_sha256=B.strategy_hash(),
        model=result.model_id,
        label_approval_sha256=sha(approval_path),
    )
    ledger.write_text(json.dumps([history]), encoding="utf-8")
    measured = score(corpus, corpus_hash, review, [report], tmp_path, approval_path)
    assert measured.measured_calls == 1 and not measured.qualified_classes()
    ledger.write_text(
        json.dumps([history, history | dict(attempt_id=str(uuid4()))]), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="All bound"):
        score(corpus, corpus_hash, review, [report], tmp_path, approval_path)
