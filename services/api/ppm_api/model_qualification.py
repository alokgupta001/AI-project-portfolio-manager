"""Offline acceptance of measured, independently labeled benchmark reports. No promotion."""

from typing import Literal

from pydantic import Field, model_validator

from ppm_api.document_schemas import Strict
from ppm_api.model_contracts import TaskClass


class ClassMeasurement(Strict):
    task_class: TaskClass
    labeled_cases: int = Field(ge=0)
    held_out_cases: int = Field(ge=0)
    supported_items: int = Field(ge=0)
    emitted_claims: int = Field(ge=0)
    correct_claims: int = Field(ge=0)
    recalled_items: int = Field(ge=0)
    abstention_cases: int = Field(ge=0)
    correct_abstentions: int = Field(ge=0)
    canonical_checks: int = Field(ge=0)
    canonical_preserved: int = Field(ge=0)
    supported_added_interpretations: int = Field(ge=0)
    citation_errors: int = Field(ge=0)
    unsupported_numbers: int = Field(ge=0)
    privacy_or_control_errors: int = Field(ge=0)

    @model_validator(mode="after")
    def denominators(self) -> "ClassMeasurement":
        if any(
            a > b
            for a, b in (
                (self.held_out_cases, self.labeled_cases),
                (self.correct_claims, self.emitted_claims),
                (self.recalled_items, self.supported_items),
                (self.correct_abstentions, self.abstention_cases),
                (self.canonical_preserved, self.canonical_checks),
            )
        ):
            raise ValueError("Invalid measurement denominator")
        return self

    def qualifies(self) -> bool:
        return (
            self.labeled_cases >= 12
            and self.held_out_cases >= 6
            and self.emitted_claims > 0
            and self.supported_items > 0
            and self.abstention_cases > 0
            and self.correct_claims / self.emitted_claims >= 0.9
            and self.recalled_items / self.supported_items >= 0.8
            and self.correct_abstentions / self.abstention_cases >= 0.9
            and self.canonical_checks > 0
            and self.canonical_preserved == self.canonical_checks
            and self.supported_added_interpretations >= 1
            and not (
                self.citation_errors or self.unsupported_numbers or self.privacy_or_control_errors
            )
        )


class QualificationReport(Strict):
    schema_version: Literal["qualification-v1"] = "qualification-v1"
    model_digest: str = Field(pattern=r"^[a-f0-9]{64}$")
    hardware_record_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    corpus_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    independent_label_review_id: str = Field(min_length=1, max_length=160)
    context_tokens: Literal[2048, 4096]
    output_tokens: int = Field(ge=64, le=512)
    warm_repeats: int = Field(ge=0)
    p95_warm_seconds: float = Field(ge=0, allow_inf_nan=False)
    cold_seconds: float = Field(ge=0, allow_inf_nan=False)
    minimum_host_headroom_mb: int = Field(ge=0)
    peak_model_mb: int = Field(gt=0)
    out_of_memory_events: int = Field(ge=0)
    maximum_simultaneous_generations: int = Field(ge=0)
    classes: list[ClassMeasurement] = Field(min_length=1, max_length=10)

    @model_validator(mode="after")
    def distinct_classes(self) -> "QualificationReport":
        if len({m.task_class for m in self.classes}) != len(self.classes):
            raise ValueError("Duplicate qualification class")
        return self

    def qualified_classes(self) -> list[TaskClass]:
        if (
            self.warm_repeats < 5
            or self.p95_warm_seconds > 20
            or self.cold_seconds > 22
            or self.minimum_host_headroom_mb < 2048
            or self.out_of_memory_events
            or self.maximum_simultaneous_generations != 1
        ):
            return []
        return [m.task_class for m in self.classes if m.qualifies()]


class CloudQualificationReport(Strict):
    """Cloud acceptance binds measured service identity; it never invents a local digest/RAM."""

    schema_version: Literal["cloud-qualification-v1"] = "cloud-qualification-v1"
    provider: Literal["groq", "gemini", "puter"]
    model: str = Field(min_length=1, max_length=160)
    reported_model_ids: list[str] = Field(min_length=1, max_length=10)
    corpus_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    strategy_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    independent_label_review_id: str = Field(min_length=1, max_length=160)
    measurement_reports: list[str] = Field(min_length=1, max_length=100)
    context_tokens: int = Field(ge=512, le=32768)
    output_tokens: int = Field(ge=64, le=512)
    measured_calls: int = Field(ge=0)
    p95_seconds: float = Field(ge=0, allow_inf_nan=False)
    failed_or_unknown_calls: int = Field(ge=0)
    observed_runtime_batches: list[list[str]] = Field(default_factory=list, max_length=10)
    expected_runtime_batches: list[list[str]] = Field(min_length=1, max_length=10)
    classes: list[ClassMeasurement] = Field(min_length=1, max_length=10)

    @model_validator(mode="after")
    def distinct(self) -> "CloudQualificationReport":
        if len({m.task_class for m in self.classes}) != len(self.classes):
            raise ValueError("Duplicate qualification class")
        return self

    def qualified_classes(self) -> list[TaskClass]:
        if (
            self.measured_calls < 5
            or self.p95_seconds > 20
            or self.failed_or_unknown_calls
            or not {tuple(sorted(v)) for v in self.expected_runtime_batches}
            <= {tuple(sorted(v)) for v in self.observed_runtime_batches}
        ):
            return []
        return [m.task_class for m in self.classes if m.qualifies()]
