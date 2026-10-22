"""Model-independent v2 contracts. Models cannot express authority or executable tools."""

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Literal, Protocol
from uuid import UUID

from pydantic import Field, StrictInt, model_validator

from ppm_api.document_schemas import Strict

AgentId = Literal[
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
AnalysisMode = Literal[
    "auto", "metrics", "domain", "assessment", "portfolio", "executive", "all_specialists"
]
SectionMode = Literal["findings", "rubric", "synthesis"]
Outcome = Literal["supported", "no_findings", "insufficient_evidence"]
TaskClass = Literal[
    "financial_interpretation",
    "schedule_interpretation",
    "team_support_advice",
    "risk_extraction",
    "resource_interpretation",
    "governance_interpretation",
    "agile_advice",
    "portfolio_synthesis",
    "executive_synthesis",
    "semantic_review",
]
Predicate = Literal[
    "budget_overrun",
    "schedule_late",
    "delivery_blocked",
    "dependency_unresolved",
    "capacity_exceeded",
    "policy_gap",
    "rubric_gap",
    "practice_gap",
    "risk_present",
    "no_adverse_evidence",
]
Alias = Annotated[str, Field(pattern=r"^[eqsfb][1-9][0-9]{0,3}$", max_length=5)]
Nonnegative = Annotated[StrictInt, Field(ge=0)]
V2_FIELDS = {"runtime_version", "analysis_mode", "requested_agents", "question_ids", "prior_run_id"}


class HybridSelection(Strict):
    runtime_version: Literal["v2"] | None = None
    analysis_mode: AnalysisMode | None = None
    requested_agents: list[AgentId] | None = Field(default=None, min_length=1, max_length=9)
    question_ids: list[UUID] | None = Field(default=None, max_length=50)
    prior_run_id: UUID | None = None

    @model_validator(mode="after")
    def distinct_selection(self) -> "HybridSelection":
        """Reject duplicate role and question selections and invalid prior-run modes."""
        for values in (self.requested_agents, self.question_ids):
            if values is not None and len(values) != len(set(values)):
                raise ValueError("Selections must be distinct")
        if self.analysis_mode == "domain" and not self.requested_agents:
            raise ValueError("Domain mode requires ordered requested agents")
        if (
            self.analysis_mode == "all_specialists"
            and self.requested_agents is not None
            and len(self.requested_agents) != 9
        ):
            raise ValueError("All-specialists mode requires all nine roles")
        role = {"portfolio": "pmo", "executive": "executive", "assessment": "governance"}.get(
            self.analysis_mode or ""
        )
        if role and self.requested_agents is not None and role not in self.requested_agents:
            raise ValueError("Analysis mode requires its specialist")
        if self.analysis_mode == "assessment" and not getattr(self, "assessment_id", None):
            raise ValueError("Assessment mode requires an assessment")
        if self.question_ids and not getattr(self, "assessment_id", None):
            raise ValueError("Question selection requires an assessment")
        return self

    def uses_v2(self) -> bool:
        """Detect an explicit hybrid selection while preserving legacy request behavior."""
        return any(getattr(self, key) is not None for key in V2_FIELDS)


class CompactSpan(Strict):
    e: Annotated[str, Field(pattern=r"^e[1-9][0-9]{0,3}$")]
    start: Annotated[StrictInt, Field(ge=0, le=20000)]
    end: Annotated[StrictInt, Field(gt=0, le=20000)]

    @model_validator(mode="after")
    def nonempty(self) -> "CompactSpan":
        """Reject reversed or empty Unicode evidence spans."""
        if self.start >= self.end:
            raise ValueError("Span must be nonempty")
        return self


class SectionFinding(Strict):
    subject: Annotated[str, Field(pattern=r"^s[1-9][0-9]{0,3}$")]
    predicate: Predicate
    kind: Literal["risk", "blocker", "dependency", "compliance_gap", "maturity_evidence"]
    signal: Literal["adverse", "clear", "uncertain"]
    severity: Literal["low", "medium", "high"]
    claim: str = Field(min_length=1, max_length=160)
    advice: str = Field(min_length=1, max_length=160)
    epistemic: Literal["interpretation", "hypothesis"]
    spans: list[CompactSpan] = Field(min_length=1, max_length=2)


class SectionMatch(Strict):
    question: Annotated[str, Field(pattern=r"^q[1-9][0-9]{0,3}$")]
    level: Annotated[StrictInt, Field(ge=0, le=1000)]
    spans: list[CompactSpan] = Field(min_length=1, max_length=2)


class NarrativeItem(Strict):
    claim: str = Field(min_length=1, max_length=160)
    advice: str = Field(min_length=1, max_length=160)
    epistemic: Literal["interpretation", "hypothesis"]
    basis: list[Annotated[str, Field(pattern=r"^[fb][1-9][0-9]{0,3}$")]] = Field(
        min_length=1, max_length=3
    )
    spans: list[CompactSpan] = Field(min_length=1, max_length=2)


class SectionGap(Strict):
    item: Alias
    code: Literal["missing_evidence", "conflicting_evidence", "unprocessed"]


class SectionOutput(Strict):
    section: str = Field(pattern=r"^[a-z0-9_-]{1,64}$")
    mode: SectionMode
    outcome: Outcome
    findings: list[SectionFinding] = Field(default_factory=list, max_length=2)
    matches: list[SectionMatch] = Field(default_factory=list, max_length=2)
    narrative: list[NarrativeItem] = Field(default_factory=list, max_length=2)
    covered: list[Alias] = Field(default_factory=list, max_length=20)
    gaps: list[SectionGap] = Field(default_factory=list, max_length=20)

    @model_validator(mode="after")
    def consistent(self) -> "SectionOutput":
        """Require mode-consistent items, explicit gaps and nonoverlapping coverage."""
        payloads = {"findings": self.findings, "rubric": self.matches, "synthesis": self.narrative}
        if any(rows for mode, rows in payloads.items() if mode != self.mode):
            raise ValueError("Section mode and payload disagree")
        if self.outcome == "supported" and not payloads[self.mode]:
            raise ValueError("Supported section requires an item")
        if self.outcome != "supported" and payloads[self.mode]:
            raise ValueError("Unsupported section cannot contain supported items")
        if len(set(self.covered)) != len(self.covered):
            raise ValueError("Duplicate coverage")
        if set(self.covered) & {g.item for g in self.gaps}:
            raise ValueError("Item cannot be covered and missing")
        if self.outcome == "no_findings" and not self.covered:
            raise ValueError("No findings requires inspected scope")
        if self.outcome == "insufficient_evidence" and not self.gaps:
            raise ValueError("Insufficient evidence requires a gap")
        return self


class CapabilityDetail(Strict):
    agent: AgentId
    execution_method: Literal["deterministic", "semantic", "hybrid"] = "deterministic"
    base_outcome: Outcome = "insufficient_evidence"
    semantic_outcome: Literal[
        "not_requested", "not_needed", "completed", "deferred", "unavailable", "failed"
    ] = "not_requested"
    interpretation_reason: Literal[
        "explicit_request",
        "explanatory_text",
        "conflicting_evidence",
        "cross_domain_synthesis",
        "none",
    ] = "none"
    base_required_ids: list[str] = Field(default_factory=list, max_length=1000)
    base_covered_ids: list[str] = Field(default_factory=list, max_length=1000)
    semantic_required_ids: list[str] = Field(default_factory=list, max_length=1000)
    semantic_covered_ids: list[str] = Field(default_factory=list, max_length=1000)
    semantic_deferred_ids: list[str] = Field(default_factory=list, max_length=1000)
    code: str | None = Field(default=None, max_length=48)

    @model_validator(mode="after")
    def honest_coverage(self) -> "CapabilityDetail":
        """Reject foreign or deferred covered IDs and false complete-coverage claims."""
        required, covered = set(self.semantic_required_ids), set(self.semantic_covered_ids)
        if not covered <= required or set(self.semantic_deferred_ids) & covered:
            raise ValueError("Invalid interpretation coverage")
        if self.semantic_outcome == "completed" and (not required or covered != required):
            raise ValueError("Incomplete interpretation cannot be completed")
        return self


class ModelUsage(Strict):
    input_tokens: Nonnegative | None = None
    output_tokens: Nonnegative | None = None
    reasoning_tokens: Nonnegative | None = None
    source: Literal["reported", "estimated", "unknown"] = "unknown"


class ModelResult(Strict):
    attempt_id: UUID
    provider_id: str
    model_id: str
    reported_model_id: str | None = Field(default=None, max_length=160)
    completion: Literal["complete", "incomplete", "refused", "unknown"]
    text: str = Field(default="", max_length=16000)
    native_finish_reason: str | None = Field(default=None, max_length=48)
    usage: ModelUsage = Field(default_factory=ModelUsage)
    latency_ms: Nonnegative = 0
    load_ms: Nonnegative | None = None
    provider_request_id: str | None = Field(default=None, max_length=160)


ErrorCode = Literal[
    "TRUNCATED",
    "INVALID_OUTPUT",
    "CONTEXT_LIMIT",
    "TIMEOUT",
    "UNAVAILABLE",
    "RATE_LIMIT",
    "QUOTA_EXHAUSTED",
    "AUTHENTICATION",
    "UNSUPPORTED_CAPABILITY",
    "MODEL_NOT_INSTALLED",
    "LOCAL_RESOURCE",
    "CONFIGURATION",
    "SPENDING_NOT_AUTHORIZED",
    "REFUSED",
    "CANCELLED",
    "AUTHORITY_REVOKED",
    "UNKNOWN",
    "OUTCOME_UNKNOWN",
    "DEADLINE_EXCEEDED",
]


class ModelFailure(Exception):
    def __init__(
        self,
        code: ErrorCode,
        certainty: Literal["not_sent", "completed", "unknown"] = "not_sent",
        retry_after: int | None = None,
    ) -> None:
        """Retain a sanitized failure code, send certainty and optional retry cooldown."""
        self.code, self.certainty, self.retry_after = code, certainty, retry_after
        super().__init__(code)


@dataclass(frozen=True)
class ExecutionPermit:
    """Internal admission binding. Never included in model messages or API schemas."""

    attempt_id: UUID
    provider_id: str
    model_id: str
    policy_hash: str
    expires_at: datetime


@dataclass(frozen=True)
class ModelRequest:
    permit: ExecutionPermit
    system: str
    payload: str
    schema: dict
    timeout: float
    tenant: UUID
    project: UUID
    task_class: TaskClass
    categories: tuple[str, ...] = ()
    num_ctx: int = 4096
    max_output_tokens: int = 512
    additional_task_classes: tuple[TaskClass, ...] = ()


class ModelAdapter(Protocol):
    async def execute(self, request: ModelRequest) -> ModelResult:
        """Return one normalized result or raise a classified failure for an admitted request."""
        ...
