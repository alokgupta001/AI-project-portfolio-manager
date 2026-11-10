"""Strict numeric history contract. Raw notes, identifiers and AI labels are excluded."""

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

FEATURES = ("velocity", "bugs", "scope_change", "spend_ratio", "dependencies", "allocation_percent")
Target = Literal["delay", "overrun", "risk", "failure", "sentiment"]
TARGETS = {
    "delay": "Days after the committed finish, floored at zero; plan known at observation.",
    "overrun": "Percent above approved budget, floored at zero; budget known at observation.",
    "risk": (
        "Independent adjudicated adverse outcome category (0/1), never a current risk heuristic."
    ),
    "failure": (
        "Observed cancellation, abandonment or missed committed delivery (1); "
        "accepted delivery (0)."
    ),
    "sentiment": (
        "Consented team survey mean <=2 on a 1–5 scale (1), otherwise 0; minimum five respondents."
    ),
}


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Features(Strict):
    velocity: float | None = Field(default=None, ge=0, le=100000)
    bugs: float | None = Field(default=None, ge=0, le=100000)
    scope_change: float | None = Field(default=None, ge=-100000, le=100000)
    spend_ratio: float | None = Field(default=None, ge=0, le=10000)
    dependencies: float | None = Field(default=None, ge=0, le=100000)
    allocation_percent: float | None = Field(default=None, ge=0, le=1000)


class Outcome(Strict):
    target: Target
    kind: Literal["observed", "synthetic"]
    evidence_ref: str = Field(min_length=3, max_length=160, pattern=r"^[A-Za-z0-9_:/.-]+$")
    occurred_at: datetime
    available_at: datetime
    baseline_known_at: datetime
    planned_finish: date | None = None
    actual_finish: date | None = None
    budget: float | None = Field(default=None, gt=0, le=1e12)
    actual_spend: float | None = Field(default=None, ge=0, le=1e12)
    disposition: Literal["cancelled", "abandoned", "missed_commitment", "accepted"] | None = None
    adverse_category: Literal[0, 1] | None = None
    adjudication: Literal["independent_outcome_review"] | None = None
    survey_mean: float | None = Field(default=None, ge=1, le=5)
    respondents: int | None = Field(default=None, ge=5, le=100000)
    consent: bool = False

    @field_validator("evidence_ref")
    @classmethod
    def no_ai_labels(cls, value: str) -> str:
        if any(
            term in value.lower() for term in ("ai_run", "synthetic", "heuristic", "model-output")
        ):
            raise ValueError("Evidence references cannot name AI or heuristic labels")
        return value


class Observation(Strict):
    entity_id: str = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9_.-]+$")
    entity_kind: Literal["project", "milestone", "sprint", "team"]
    observed_at: datetime
    feature_asof: datetime
    features: Features
    outcome: Outcome | None = None

    @model_validator(mode="after")
    def dates(self) -> "Observation":
        times = [self.observed_at, self.feature_asof]
        if self.outcome:
            times += [
                self.outcome.occurred_at,
                self.outcome.available_at,
                self.outcome.baseline_known_at,
            ]
        if any(t.tzinfo is None for t in times):
            raise ValueError("All timestamps require timezone offsets")
        if self.feature_asof > self.observed_at:
            raise ValueError("Future feature leakage")
        if self.outcome:
            o = self.outcome
            if o.baseline_known_at > self.observed_at:
                raise ValueError("Future baseline leakage")
            if o.occurred_at <= self.observed_at or o.available_at < o.occurred_at:
                raise ValueError("Outcome must follow observation and precede label availability")
        return self


class HistoryInput(Strict):
    project_id: UUID
    name: str = Field(min_length=1, max_length=160)
    origin: str = Field(min_length=3, max_length=240)
    lineage: Literal["synthetic", "real"]
    license: Literal["organization-authorized", "CC0-1.0"]
    permitted_use: Literal["local-research"] = "local-research"
    privacy: Literal["aggregate-numeric-no-personal-data"] = "aggregate-numeric-no-personal-data"
    authorized: bool
    label_declaration: Literal["observed-outcomes", "synthetic-fixture", "unlabeled"]
    records: list[Observation] = Field(max_length=500)

    @model_validator(mode="after")
    def suitable(self) -> "HistoryInput":
        if not self.authorized:
            raise ValueError("Confirm lawful local research use")
        if self.lineage == "real" and self.license != "organization-authorized":
            raise ValueError(
                "External real datasets require a separate source/license/target review"
            )
        if self.lineage == "synthetic" and self.label_declaration != "synthetic-fixture":
            raise ValueError("Synthetic history requires a synthetic declaration")
        for r in self.records:
            if r.outcome:
                expected = "synthetic" if self.lineage == "synthetic" else "observed"
                if r.outcome.kind != expected or self.label_declaration == "unlabeled":
                    raise ValueError("Mixed or undeclared label lineage")
        keys = [(r.entity_id, r.observed_at) for r in self.records]
        if len(keys) != len(set(keys)):
            raise ValueError("Duplicate entity observations")
        return self


class DatasetInput(Strict):
    history_id: UUID
    target: Target
    horizon_days: int = Field(default=30, ge=1, le=366)
    train_end: datetime
    validation_end: datetime
    cutoff: datetime

    @model_validator(mode="after")
    def chronology(self) -> "DatasetInput":
        if any(t.tzinfo is None for t in (self.train_end, self.validation_end, self.cutoff)):
            raise ValueError("Split boundaries require timezones")
        if not self.train_end < self.validation_end < self.cutoff:
            raise ValueError("Expected train_end < validation_end < cutoff")
        return self


class DatasetView(BaseModel):
    id: UUID
    project_id: UUID
    history_id: UUID
    digest: str
    manifest: dict
    created_at: datetime


class MLHistoryView(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    version: int
    digest: str
    manifest: dict
    withdrawn: bool
    created_at: datetime


class RunInput(Strict):
    dataset_id: UUID


class RunView(BaseModel):
    id: UUID
    project_id: UUID
    dataset_id: UUID
    status: str
    card: dict
    created_at: datetime
