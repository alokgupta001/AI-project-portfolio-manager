"""Sprint 09 public source contract. No semantic inference is activated."""

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

Category = Literal["SRS", "BRD", "PRD", "MOM", "sprint_report", "risk_log", "charter", "policy"]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Upload(Strict):
    title: str = Field(min_length=1, max_length=160)
    category: Category
    project_id: UUID | None = None
    document_id: UUID | None = None
    filename: str = Field(pattern=r"^[A-Za-z0-9 _().-]{1,150}\.[A-Za-z0-9]{1,10}$")
    content_base64: str = Field(min_length=4, max_length=11184812)


class Policy(Strict):
    owner_id: UUID
    applicability: str = Field(min_length=1, max_length=500)
    state: Literal["draft", "current", "superseded"]
    version_id: UUID
    effective_date: date
    review_date: date

    @model_validator(mode="after")
    def ordered(self) -> "Policy":
        if self.review_date < self.effective_date:
            raise ValueError("Review date must follow effective date")
        return self


class Governance(Strict):
    legal_hold: bool
    retain_until: datetime
    policy: Policy | None = None

    @model_validator(mode="after")
    def timezone(self) -> "Governance":
        if self.retain_until.tzinfo is None:
            raise ValueError("Retention requires a timezone-aware instant")
        return self


class VersionView(BaseModel):
    id: UUID
    document_id: UUID
    number: int
    sha256: str
    filename: str
    size: int
    uploaded_by: UUID
    created_at: datetime
    status: str
    diagnostic: str | None
    scanner: str | None
    parser_version: str


class DocumentView(BaseModel):
    id: UUID
    project_id: UUID | None
    title: str
    category: Category
    revision: int
    created_at: datetime
    legal_hold: bool
    retain_until: datetime
    policy: Policy | None
    policy_label: str | None = None
    versions: list[VersionView]
    can_manage: bool


class DocumentPage(BaseModel):
    items: list[DocumentView]
    total: int
    as_of: datetime


class ChunkView(BaseModel):
    id: UUID
    version_id: UUID
    ordinal: int
    location: str
    text: str
    confidence: float | None
    method: str


class SearchHit(ChunkView):
    title: str
    document_id: UUID
    version_number: int
    sha256: str
    score: float


class Retrieval(BaseModel):
    mode: Literal["keyword"] = "keyword"
    chunk_version: str = "locations-1200-v1"
    embedding_status: Literal["budgeted_ai_runtime"] = "budgeted_ai_runtime"
    items: list[SearchHit]


class DownloadTicket(BaseModel):
    token: str
    expires_at: datetime


class JobStatus(BaseModel):
    id: UUID
    status: str
    attempt: int
    stages: list[str]


class Accepted(BaseModel):
    document: DocumentView
    version_id: UUID
    job_id: UUID | None
    duplicate: bool = False


class EvidenceLink(Strict):
    attachment_id: UUID


class EvidenceReference(BaseModel):
    attachment_id: UUID
    assessment_id: UUID
    assessment_name: str


class Result(BaseModel):
    status: str


class OrphanPage(BaseModel):
    keys: list[str]
    minimum_age_days: int = 30
    scan_limit: int = 10000


class OrphanPurge(Strict):
    keys: list[str] = Field(min_length=1, max_length=100)
