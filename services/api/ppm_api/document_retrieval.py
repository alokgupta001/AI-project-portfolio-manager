"""Versioned source/provider boundary. Sprint 10 implements budgeted indexing via Runtime."""

from typing import Literal, Protocol
from uuid import UUID

from pydantic import Field

from ppm_api.document_schemas import Strict


class EmbeddingRequest(Strict):
    organization_id: UUID
    project_id: UUID | None
    version_id: UUID
    sha256: str
    chunk_version: Literal["locations-1200-v1"] = "locations-1200-v1"
    chunk_ids: list[UUID] = Field(max_length=100)


class EmbeddingBackend(Protocol):
    async def index(self, request: EmbeddingRequest) -> None:
        """Sprint 10 must enforce gateway budgets and revalidate every source chunk."""
        ...


class CandidateFinding(Strict):
    """Sprint 11 review input, never an authoritative domain mutation."""

    run_id: UUID
    organization_id: UUID
    project_id: UUID | None
    source_version_id: UUID
    source_sha256: str
    kind: Literal["risk", "blocker", "dependency", "compliance_gap", "maturity_evidence"]
    statement: str = Field(min_length=1, max_length=1000)
    evidence_chunk_ids: list[UUID] = Field(min_length=1, max_length=20)
    status: Literal["suggested"] = "suggested"
