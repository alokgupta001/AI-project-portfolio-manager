"""Fixture results prove only the selection pipeline, never real semantic accuracy."""

from uuid import uuid4

import pytest
from ppm_api.modules.agents import guided_review as G
from ppm_api.modules.agents.schemas import AnalysisInput
from ppm_api.modules.ai.registry import digest
from ppm_api.modules.selection.protocol import PROMPT, fixture_sources, protocol, summarize
from pydantic import ValidationError


def test_protocol_is_frozen_numeric_only_and_has_independent_reserved_cases():
    p = protocol()
    assert p["strategy_sha256"] == digest(PROMPT)
    assert p["corpus_sha256"] == protocol()["corpus_sha256"]
    assert [c["expected"] for c in p["cases"]] == [
        ["o1"],
        [],
        ["o1"],
        ["o2"],
        ["o1", "o2"],
        [],
        ["o1"],
        [],
        ["o1"],
        ["o1"],
        ["o1", "o2"],
        [],
    ]
    assert sum(c["split"] == "held_out" for c in p["cases"]) == 6
    project = str(uuid4())
    for case in p["cases"]:
        sources = fixture_sources(project, case["id"])
        snapshot = dict(sources=sources, selection_pilot={"id": "fixture"})
        context = G.pack(snapshot, "financial", {s["source"]: s for s in sources})
        assert project not in context["payload"]
        assert all(o["fact"] in context["payload"] for o in case["observations"])
        assert context["categories"] == ["metric:usage"]
        assert context["system"] == PROMPT
        result = G.validate(context, {"choices": case["expected"]})
        assert len(result["guided_cards"]) == len(case["expected"])


def test_even_twelve_correct_synthetic_cases_cannot_qualify_semantics():
    rows = [
        dict(c, status="measured", selected=c["expected"], correct=True, latency_ms=100)
        for c in protocol()["cases"]
    ]
    output = summarize(rows)
    assert output["state"] == "fixture_passed" and output["correct_cases"] == 12
    assert output["precision"] == output["recall"] == 1
    assert output["at17"] == "BLOCKED" and not output["semantic_qualified_classes"]
    assert output["added_interpretations"] == 0
    assert output["deterministic_rule_available"] and "deterministic_correct_cases" not in output
    assert summarize(rows[:11])["state"] == "insufficient_data"
    rows[0].update(correct=False, selected=[])
    assert summarize(rows)["state"] == "fixture_failed"
    rows[0].update(status="unavailable", selected=["o1"], correct=None)
    output = summarize(rows)
    assert output["measured_cases"] == 11 and output["unavailable_cases"] == 1
    assert output["correct_cases"] == 11


@pytest.mark.parametrize(
    "change",
    [
        {"analysis_mode": "metrics"},
        {"requested_agents": ["risk"]},
        {"version_ids": [uuid4()]},
        {"assessment_id": uuid4()},
        {"prior_run_id": uuid4()},
        {"guided_case_id": None},
    ],
)
def test_pilot_selection_cannot_add_real_evidence_or_other_roles(change):
    body = dict(
        project_id=uuid4(),
        analysis_mode="guided",
        requested_agents=["financial"],
        guided_pilot_id=uuid4(),
        guided_case_id="f01",
    )
    with pytest.raises(ValidationError):
        AnalysisInput(**(body | change))
