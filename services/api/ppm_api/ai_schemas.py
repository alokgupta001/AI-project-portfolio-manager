"""Versioned public contracts for the bounded evidence runtime (no domain agents)."""

from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import Field

from ppm_api.document_schemas import Strict

PROMPT_VERSION = "source-excerpts-v1"
SCHEMA_VERSION = "ai-evidence-v1"
TOOL_VERSION = "source-read-v1"
GRAPH_VERSION = "evidence-graph-v1"


class AIRunInput(Strict):
    project_id: UUID
    operation: Literal["query", "index"] = "query"
    query: str = Field(default="", max_length=160)
    version_id: UUID | None = None


class AIExcerpt(Strict):
    chunk_id: UUID
    quote: str = Field(min_length=1, max_length=1200)


class AIOutput(Strict):
    status: Literal["supported", "unavailable"]
    excerpts: list[AIExcerpt] = Field(max_length=5)


class AIEvidence(Strict):
    chunk_id: UUID
    version_id: UUID
    sha256: str
    text_sha256: str
    location: str
    quote: str


class AIRunView(Strict):
    id: UUID
    organization_id: UUID
    input_snapshot_id: UUID
    project_id: UUID
    operation: str
    status: str
    created_at: datetime
    generated_at: datetime | None
    answer_status: Literal[
        "supported", "unavailable", "source_fallback", "indexed", "not_requested"
    ]
    prompt_version: str
    schema_version: str
    tool_version: str
    graph_version: str
    provider: str
    model: str | None
    diagnostic: str | None
    limitations: list[str]
    evidence: list[AIEvidence]
    retrieval: Literal["keyword", "hybrid", "none"]
    reserved_usd: Decimal
    charged_usd: Decimal
    input_tokens: int | None
    output_tokens: int | None
    latency_ms: int
    sequence: int
    revision: int


class AIBudgetInput(Strict):
    limit_usd: Decimal = Field(ge=0, le=10000, max_digits=12, decimal_places=6)
    concurrency: int = Field(ge=1, le=4)


class AIProviderStatus(Strict):
    provider: str
    enabled: bool
    reason: str
    completion_model: str | None
    embedding_model: str | None
    real_provider_acceptance: Literal["not_verified"] = "not_verified"


class AIOperations(Strict):
    provider: AIProviderStatus
    limit_usd: Decimal
    spent_usd: Decimal
    reserved_usd: Decimal
    deployment_limit_usd: Decimal
    concurrency: int
    revision: int
    failures: int
    circuit_until: datetime | None
    runs: list[AIRunView]


class AICallView(Strict):
    id: UUID
    operation: str
    attempt: int
    status: str
    code: str | None
    charged_usd: Decimal
    input_tokens: int | None
    output_tokens: int | None
    latency_ms: int


class AIDiagnostics(Strict):
    run: AIRunView
    input_sha256: str
    prompt_version: str
    schema_version: str
    tool_version: str
    graph_version: str
    evidence_snapshot: list[dict[str, str]]
    calls: list[AICallView]


class AIEvaluation(Strict):
    version: str
    environment: str
    thresholds: dict[str, float]
    count: int
    passed: int
    failures: list[str]
    eligible: bool
    real_provider_acceptance: str
    limitation: str
