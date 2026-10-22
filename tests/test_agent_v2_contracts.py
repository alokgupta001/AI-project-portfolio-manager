"""Hybrid contract safety and legacy request identity; never calls a model."""

from uuid import uuid4

import pytest
from ppm_api.agent_registry import REGISTRY
from ppm_api.agent_schemas import AGENTS, AnalysisInput
from ppm_api.ai_schemas import AIRunInput
from ppm_api.model_contracts import V2_FIELDS, CapabilityDetail, ModelUsage, SectionOutput
from pydantic import ValidationError


def test_nine_hybrid_roles_and_legacy_fingerprint_shape():
    assert tuple(c.agent for c in REGISTRY) == AGENTS
    assert all(c.execution_policy == "hybrid_on_demand" for c in REGISTRY)
    assert len({c.task_class for c in REGISTRY}) == 9
    project = uuid4()
    legacy = AIRunInput(project_id=project)
    assert not legacy.uses_v2()
    assert legacy.model_dump(exclude=V2_FIELDS | {"version_ids", "assessment_id"}) == dict(
        project_id=project, operation="query", query="", version_id=None
    )


@pytest.mark.parametrize(
    "values",
    [
        {"analysis_mode": "domain"},
        {"requested_agents": ["risk", "risk"]},
        {"requested_agents": []},
        {"requested_agents": ["root_admin"]},
        {"analysis_mode": "executive", "requested_agents": ["financial"]},
        {"analysis_mode": "assessment"},
        {"question_ids": [uuid4()]},
        {"runtime_version": "v3"},
        {"provider_url": "https://untrusted.invalid"},
    ],
)
def test_invalid_or_scope_expanding_requests_rejected(values):
    with pytest.raises(ValidationError):
        AnalysisInput(project_id=uuid4(), **values)


def test_requested_priority_is_preserved():
    body = AnalysisInput(
        project_id=uuid4(), analysis_mode="domain", requested_agents=["resource", "financial"]
    )
    assert body.requested_agents == ["resource", "financial"] and body.uses_v2()


def test_strict_section_modes_spans_and_coverage():
    accepted = dict(section="risk-01", mode="findings", outcome="no_findings", covered=["e1"])
    assert SectionOutput(**accepted).covered == ["e1"]
    for update in (
        {"outcome": "supported"},
        {"covered": []},
        {"covered": ["e1", "e1"]},
        {"gaps": [{"item": "e1", "code": "unprocessed"}]},
        {"tools": ["write_plan"]},
        {
            "matches": [
                {"question": "q1", "level": True, "spans": [{"e": "e1", "start": 0, "end": 1}]}
            ]
        },
    ):
        with pytest.raises(ValidationError):
            SectionOutput(**(accepted | update))


def test_synthesis_requires_known_alias_shape_and_evidence():
    value = dict(
        section="executive-01",
        mode="synthesis",
        outcome="supported",
        covered=["f1"],
        narrative=[
            dict(
                claim="Review the delivery exception.",
                advice="Validate its impact.",
                epistemic="interpretation",
                basis=["f1"],
                spans=[dict(e="e1", start=0, end=4)],
            )
        ],
    )
    assert SectionOutput(**value).narrative[0].basis == ["f1"]
    value["narrative"][0]["basis"] = []
    with pytest.raises(ValidationError):
        SectionOutput(**value)


def test_baseline_cannot_manufacture_semantic_completion():
    with pytest.raises(ValidationError):
        CapabilityDetail(agent="financial", base_outcome="supported", semantic_outcome="completed")
    with pytest.raises(ValidationError):
        ModelUsage(input_tokens=True)
    assert ModelUsage().input_tokens is None


def test_v2_settings_are_default_off_and_bounded(settings):
    assert not settings.ai_runtime_v2_enabled and not settings.ai_cloud_enabled
    with pytest.raises(ValidationError):
        type(settings)(**(settings.model_dump() | {"ai_max_output_tokens": 513}))
