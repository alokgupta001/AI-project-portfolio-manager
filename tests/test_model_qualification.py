"""Synthetic arithmetic for qualification gates; these tests do not qualify a model."""

import pytest
from ppm_api.model_qualification import (
    ClassMeasurement,
    CloudQualificationReport,
    QualificationReport,
)


def report():
    return dict(
        model_digest="a" * 64,
        hardware_record_sha256="b" * 64,
        corpus_sha256="c" * 64,
        independent_label_review_id="synthetic-test-only",
        context_tokens=4096,
        output_tokens=512,
        warm_repeats=5,
        p95_warm_seconds=19,
        cold_seconds=21,
        minimum_host_headroom_mb=2100,
        peak_model_mb=4000,
        out_of_memory_events=0,
        maximum_simultaneous_generations=1,
        classes=[
            dict(
                task_class="risk_extraction",
                labeled_cases=12,
                held_out_cases=6,
                supported_items=10,
                emitted_claims=10,
                correct_claims=9,
                recalled_items=8,
                abstention_cases=10,
                correct_abstentions=9,
                canonical_checks=12,
                canonical_preserved=12,
                supported_added_interpretations=1,
                citation_errors=0,
                unsupported_numbers=0,
                privacy_or_control_errors=0,
            )
        ],
    )


@pytest.mark.parametrize(
    "change",
    [
        dict(p95_warm_seconds=21),
        dict(minimum_host_headroom_mb=2000),
        dict(out_of_memory_events=1),
        dict(warm_repeats=4),
        dict(maximum_simultaneous_generations=2),
    ],
)
def test_failed_hardware_or_latency_never_qualifies(change):
    assert not QualificationReport(**(report() | change)).qualified_classes()


def test_per_class_denominators_and_canonical_safety():
    data = report()
    assert QualificationReport(**data).qualified_classes() == ["risk_extraction"]
    measurement = data["classes"][0]
    for change in [
        dict(emitted_claims=0, correct_claims=0),
        dict(citation_errors=1),
        dict(canonical_preserved=11),
        dict(held_out_cases=5),
        dict(unsupported_numbers=1),
    ]:
        assert not ClassMeasurement(**(measurement | change)).qualifies()


def test_cloud_acceptance_has_real_identity_and_no_fabricated_local_measurements():
    data = dict(
        provider="puter",
        model="gpt-4.1-mini-2025-04-14",
        reported_model_ids=["gpt-4.1-mini"],
        corpus_sha256="a" * 64,
        strategy_sha256="b" * 64,
        independent_label_review_id="synthetic-only",
        measurement_reports=["c" * 64],
        context_tokens=8192,
        output_tokens=512,
        measured_calls=12,
        p95_seconds=2,
        failed_or_unknown_calls=0,
        observed_runtime_batches=[["risk", "governance", "agile_coach"]],
        expected_runtime_batches=[["risk", "governance", "agile_coach"]],
        classes=report()["classes"],
    )
    assert CloudQualificationReport(**data).qualified_classes() == ["risk_extraction"]
    for change in (
        dict(measured_calls=4),
        dict(p95_seconds=21),
        dict(failed_or_unknown_calls=1),
        dict(observed_runtime_batches=[["risk"]]),
    ):
        assert not CloudQualificationReport(**(data | change)).qualified_classes()
