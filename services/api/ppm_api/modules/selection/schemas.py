"""Validated request/response contracts for this feature."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import Field

from ppm_api.modules.documents.schemas import Strict


class PilotInput(Strict):
    project_id: UUID


class LabelReview(Strict):
    corpus_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    strategy_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    reviewed_case_ids: list[str] = Field(min_length=12, max_length=12)
    human_reviewed: Literal[True]
    reason: str = Field(min_length=12, max_length=1000)


class AutomatedReview(Strict):
    corpus_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    strategy_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    synthetic_only: Literal[True]


class PilotCase(Strict):
    id: str
    split: str
    expected: list[str]
    selected: list[str]
    status: str
    run_id: UUID | None
    correct: bool | None
    latency_ms: int
    elapsed_ms: int | None
    timing_kind: Literal["accepted_response", "unavailable_attempt", "not_recorded"]
    diagnostic: str | None


class PilotObservation(Strict):
    id: str
    value: str
    partial: bool
    fact: str


class ProtocolCase(Strict):
    id: str
    split: str
    observations: list[PilotObservation]
    expected: list[str]


class PilotProtocol(Strict):
    version: str
    lineage: str
    license: str
    rule: str
    cases: list[ProtocolCase]
    corpus_sha256: str
    strategy_sha256: str


class PilotView(Strict):
    id: UUID
    project_id: UUID
    actor_id: UUID
    created_at: datetime
    revision: int
    binding: dict
    review: dict | None
    protocol: PilotProtocol
    cases: list[PilotCase]
    summary: dict
    binding_current: bool
    can_review: bool
    next_case_at: datetime | None
    can_automated_review: bool
    review_kind: Literal["human", "automated_rule_audit"] | None
    human_reviewed: bool
