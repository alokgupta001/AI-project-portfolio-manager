"""Critique abstention, dependent withdrawal, distinct claims and live evidence gates."""

from uuid import uuid4

import pytest
from ppm_api.agent_critique import Critique, pack_review, validate_review
from ppm_api.agent_runtime import baseline, reviewed_findings
from ppm_api.agent_validation import reconcile
from ppm_api.model_contracts import ModelFailure


def finding(key="risk", basis=None):
    return dict(
        key=key,
        title="Reported supplier delay may affect delivery.",
        improvement="Verify dependency.",
        kind="risk",
        signal="adverse",
        severity="high",
        epistemic="hypothesis",
        agents=["risk"],
        spans=[dict(source="doc", start=0, end=15)],
        predicate="risk_present",
        basis=basis or [],
        confidence=None,
        discrepancy=False,
        conflicts=[],
        semantic_status="unreviewed",
    )


def test_python_baseline_does_not_count_uninterpreted_documents_as_covered():
    source = dict(
        source="doc",
        kind="document",
        text="Narrative needs interpretation.",
        fresh=True,
        permitted_agents=["risk"],
    )
    result = baseline(dict(sources=[source]), "risk", [], {"doc": source})
    assert result["base_covered_ids"] == [] and result["outcome"] == "insufficient_evidence"


def test_critique_withdraws_transitive_synthesis_but_preserves_original_sections():
    item = finding()
    current = {
        "doc": dict(
            source="doc",
            text="Supplier delay. No confirmed cause.",
            category="document:project",
            kind="document",
        )
    }
    context = pack_review([item], current)
    result = validate_review(
        context,
        Critique(
            section="semantic-review",
            decisions=[
                dict(
                    claim="c1",
                    disposition="insufficient_evidence",
                    reason="Cause is unknown.",
                    spans=[],
                )
            ],
        ),
    )
    sections = [
        dict(result=dict(findings=[item, finding("pmo", ["risk"]), finding("exec", ["pmo"])])),
        dict(result=result),
    ]
    visible, withdrawn = reviewed_findings(sections, current)
    assert not visible and withdrawn == {"risk", "pmo", "exec"}
    assert len(sections[0]["result"]["findings"]) == 3
    with pytest.raises(ModelFailure):
        validate_review(
            context,
            Critique(
                section="semantic-review",
                decisions=[
                    dict(
                        claim="c1",
                        disposition="supported",
                        reason="Agrees.",
                        spans=[],
                    )
                ],
            ),
        )


def test_distinct_claims_preserved_and_source_overlap_is_not_proven_opposition():
    one, two = finding(), finding(str(uuid4()))
    two.update(
        title="A separate dependency has missing ownership.",
        signal="clear",
        predicate="dependency_unresolved",
    )
    result = reconcile([one, two])
    assert len(result) == 2 and not any(f["conflicts"] for f in result)
    two["predicate"] = one["predicate"]
    assert all(f["conflicts"] for f in reconcile([one, two]))
    with pytest.raises(ModelFailure):
        pack_review([one], {})
