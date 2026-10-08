"""Typed Sprint 06 contracts. Frozen definitions are the scoring authority."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

Weight = Annotated[Decimal, Field(gt=0, le=1000, max_digits=10, decimal_places=5)]
Score = Annotated[Decimal, Field(ge=0, le=100, max_digits=7, decimal_places=4)]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Level(Strict):
    level: int = Field(ge=0, le=1000)
    label: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=2000)


class Question(Strict):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=160)
    text: str = Field(min_length=1, max_length=2000)
    answer_type: Literal["boolean", "rubric", "text"] = "rubric"
    weight: Weight = Decimal(1)
    required: bool = True
    rubric_levels: list[Level] = Field(default_factory=list, max_length=30)


class Dimension(Strict):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=2000)
    weight: Annotated[Decimal, Field(gt=0, le=1, max_digits=6, decimal_places=5)]
    questions: list[Question] = Field(default_factory=list, max_length=50)


class FrameworkInput(Strict):
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=4000)
    category: Literal["pmo", "agile", "governance", "delivery", "custom"] = "custom"
    dimensions: list[Dimension] = Field(default_factory=list, max_length=20)
    archived: bool = False

    @model_validator(mode="after")
    def unique_ids(self) -> Any:
        ids = [d.id for d in self.dimensions] + [q.id for d in self.dimensions for q in d.questions]
        if len(set(ids)) != len(ids):
            raise ValueError("Dimension and question identifiers must be unique")
        return self


class FrameworkRecord(FrameworkInput):
    id: UUID
    revision: int
    published_version: int | None
    can_edit: bool


class VersionRecord(BaseModel):
    id: UUID
    framework_id: UUID
    version: int
    snapshot: FrameworkInput
    created_at: datetime


class AssignmentInput(Strict):
    name: str = Field(min_length=1, max_length=160)
    framework_version_id: UUID
    department_id: UUID | None = None
    team_id: UUID | None = None
    assigned_to: UUID
    reviewer_id: UUID

    @model_validator(mode="after")
    def separate_people(self) -> Any:
        if self.assigned_to == self.reviewer_id:
            raise ValueError("Respondent and reviewer must differ")
        return self


class AnswerInput(Strict):
    question_id: UUID
    value: str | None = Field(default=None, max_length=8000)
    evidence_text: str = Field(default="", max_length=8000)


class AnswerBatchInput(Strict):
    items: list[AnswerInput] = Field(max_length=500)


class AnswerRecord(AnswerInput):
    id: UUID
    reviewer_score: Decimal | None
    reviewer_note: str | None


class ActionInput(Strict):
    note: str = Field(default="", max_length=2000)


class Adjustment(Strict):
    answer_id: UUID
    reviewer_score: Score
    reviewer_note: str = Field(min_length=1, max_length=2000)


class ReviewInput(Strict):
    action: Literal["start", "return", "complete"]
    note: str = Field(min_length=1, max_length=2000)
    adjustments: list[Adjustment] = Field(default_factory=list, max_length=500)


class DimensionScoreDetail(Strict):
    dimension_id: UUID
    dimension_name: str
    score: Decimal | None
    weight: Decimal
    answered_count: int
    total_required: int
    coverage_percent: Decimal
    evidence_coverage_percent: Decimal


class AssessmentRecord(AssignmentInput):
    id: UUID
    revision: int
    status: Literal["draft", "submitted", "in_review", "returned", "completed"]
    framework_name: str
    framework_version: int
    overall_score: Decimal | None
    dimension_scores: list[DimensionScoreDetail]
    provisional: bool
    can_read_evidence: bool
    can_answer: bool
    can_review: bool


class AssessmentDetail(Strict):
    assessment: AssessmentRecord
    snapshot: FrameworkInput
    answers: list[AnswerRecord]
    notes: list[str]


class EventRecord(BaseModel):
    id: UUID
    actor_id: UUID
    event: str
    note: str
    details: dict
    created_at: datetime


class EvidenceInput(Strict):
    question_id: UUID
    file_name: str = Field(
        min_length=1, max_length=160, pattern="^[A-Za-z0-9][A-Za-z0-9 _.-]*[.]txt$"
    )
    content_base64: str = Field(max_length=700000)


class EvidenceRecord(BaseModel):
    id: UUID
    question_id: UUID
    file_name: str
    file_size: int
    sha256: str
    released: bool
    created_at: datetime


class AccessInput(Strict):
    user_id: UUID
    framework_id: UUID | None = None
    assessment_id: UUID | None = None
    active: bool = True

    @model_validator(mode="after")
    def one_scope(self) -> Any:
        if (self.framework_id is None) == (self.assessment_id is None):
            raise ValueError("Choose a framework editor grant or assessment result-read grant")
        return self
