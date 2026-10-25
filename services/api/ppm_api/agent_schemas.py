"""Bounded, read-only specialist contracts; confidence is never a maturity score."""

from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import Field

from ppm_api.ai_schemas import AIRunView
from ppm_api.document_schemas import Strict
from ppm_api.guided_review import GuidedReview
from ppm_api.jobs import StageView
from ppm_api.model_contracts import AnalysisMode, CapabilityDetail, HybridSelection

Agent = Literal[
    "financial",
    "schedule",
    "sentiment",
    "risk",
    "resource",
    "governance",
    "agile_coach",
    "pmo",
    "executive",
]
Kind = Literal["risk", "blocker", "dependency", "compliance_gap", "maturity_evidence"]
AGENTS: tuple[str, ...] = (
    "financial",
    "schedule",
    "sentiment",
    "risk",
    "resource",
    "governance",
    "agile_coach",
    "pmo",
    "executive",
)
PROMPT = "specialists-rubric-v1"
RULE = "specialist-support-v1"


class AnalysisInput(HybridSelection):
    project_id: UUID
    version_ids: list[UUID] = Field(default_factory=list, max_length=5)
    assessment_id: UUID | None = None


class Span(Strict):
    source: str = Field(min_length=1, max_length=160)
    start: int = Field(ge=0, le=20000)
    end: int = Field(gt=0, le=20000)


class Candidate(Strict):
    kind: Kind
    signal: Literal["adverse", "clear", "uncertain"] = "adverse"
    severity: Literal["low", "medium", "high"]
    confidence: Decimal = Field(ge=0, le=1)
    spans: list[Span] = Field(min_length=1, max_length=5)


class SpecialistOutput(Strict):
    agent: Agent
    status: Literal["supported", "unavailable", "failed"]
    findings: list[Candidate] = Field(default_factory=list, max_length=5)


class RubricMatch(Strict):
    question_id: UUID
    level: int = Field(ge=0, le=1000)
    confidence: Decimal = Field(ge=0, le=1)
    spans: list[Span] = Field(min_length=1, max_length=5)


class AgentBatch(Strict):
    agents: list[SpecialistOutput] = Field(default_factory=list, max_length=9)
    matches: list[RubricMatch] = Field(default_factory=list, max_length=50)


class AgentDefinition(Strict):
    agent: Agent
    inputs: list[str]
    tools: list[str]
    timeout_seconds: int
    fallback: str
    output_schema: str = "SpecialistOutput"
    execution_policy: str | None = None
    guided_enabled: bool = False
    guided_project_ids: list[UUID] = Field(default_factory=list)
    task_class: str | None = None
    modes: list[str] = Field(default_factory=list)
    evaluation_cases: list[str] = ["supported", "missing", "contradictory", "malicious"]


class EvidenceView(Strict):
    source: str
    version: str
    sha256: str
    location: str
    text: str


class AgentState(Strict):
    agent: Agent
    status: Literal["supported", "fallback", "unavailable", "failed"]
    code: str | None = None


class ReviewInput(Strict):
    decision: Literal["accepted", "rejected"]
    reason: str = Field(min_length=1, max_length=1000)
    approved_score: Decimal | None = Field(default=None, ge=0, le=100, decimal_places=4)


class ReviewView(ReviewInput):
    id: UUID
    item_key: str
    actor_id: UUID
    created_at: datetime
    revision: int


class FindingView(Strict):
    key: str
    kind: Kind
    signal: Literal["adverse", "clear", "uncertain"]
    severity: Literal["low", "medium", "high"]
    confidence: Decimal | None
    title: str
    improvement: str
    agents: list[Agent]
    spans: list[Span]
    discrepancy: bool
    conflicts: list[str]
    available: bool
    review_revision: int
    reviews: list[ReviewView]
    epistemic: Literal["deterministic", "interpretation", "hypothesis"] = "deterministic"
    semantic_status: str = "not_assessed"
    predicate: str | None = None
    basis: list[str] = Field(default_factory=list)


class SuggestionView(Strict):
    key: str
    dimension_id: UUID
    dimension_name: str
    original_score: Decimal | None
    suggested_score: Decimal | None
    confidence: Decimal | None
    approved_score: Decimal | None
    gaps: list[str]
    improvement: str
    spans: list[Span]
    available: bool
    review_revision: int
    reviews: list[ReviewView]


class AnalysisRunSummary(Strict):
    id: UUID
    status: str
    created_at: datetime


class AnalysisSummary(Strict):
    run: AnalysisRunSummary
    semantic_status: str


class AnalysisView(Strict):
    run: AIRunView
    prompt_version: str = PROMPT
    rule_version: str = RULE
    framework_version_id: UUID | None
    assessment_id: UUID | None
    assessment_revision: int | None
    source_snapshot_sha256: str
    semantic_status: str
    model_quality: Literal["UNVERIFIED/BLOCKED"] = "UNVERIFIED/BLOCKED"
    agents: list[AgentState]
    missing_agents: list[Agent]
    findings: list[FindingView]
    suggestions: list[SuggestionView]
    evidence: list[EvidenceView]
    stages: list[StageView]
    limitations: list[str]
    can_review: bool
    can_cancel: bool = False
    runtime_version: str | None = None
    analysis_mode: AnalysisMode | None = None
    capability_details: list[CapabilityDetail] = Field(default_factory=list, max_length=9)
    task_summary: list[dict] = Field(default_factory=list, max_length=24)
    validation_summary: dict = Field(default_factory=dict)
    briefing: list[FindingView] = Field(default_factory=list, max_length=20)
    route_summary: list[dict] = Field(default_factory=list, max_length=4)
    blocked_reason: str | None = None
    guided_review: GuidedReview | None = None
