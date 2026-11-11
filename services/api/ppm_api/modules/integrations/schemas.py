"""Validated request/response contracts for this feature."""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ppm_api.modules.integrations.ingestion import (
    ConnectorConfig,
)


class IntegrationView(BaseModel):
    id: UUID
    config: ConnectorConfig
    revision: int
    enabled: bool
    cursor: str | None
    updated_at: datetime


class StageView(BaseModel):
    id: UUID
    sequence: int
    stage: str
    occurred_at: datetime


class JobView(BaseModel):
    id: UUID
    integration_id: UUID | None
    ml_run_id: UUID | None = None
    status: str
    attempt: int
    position: int
    accepted: int
    errors: list[dict[str, Any]]
    cancel_requested: bool
    heartbeat_at: datetime | None
    created_at: datetime
    updated_at: datetime
    sequence: int


class Preview(BaseModel):
    valid: int
    errors: list[dict[str, Any]]
    examples: list[dict[str, Any]]


class EnabledInput(BaseModel):
    enabled: bool


class SourceView(BaseModel):
    external_id: str
    source_updated_at: datetime | None
    source_observed_at: datetime
    target_id: UUID
    target_kind: str
    target_revision: int
    job_id: UUID


class AuthorityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    active: bool = True
    interval_minutes: int = Field(default=0, ge=0, le=10080)
    secret_ref: str = Field(default="", max_length=80, pattern=r"^(PPM_CONNECTOR_[A-Z0-9_]+)?$")
    webhook_secret_ref: str = Field(
        default="", max_length=80, pattern=r"^(PPM_CONNECTOR_[A-Z0-9_]+)?$"
    )


class AuthorityView(BaseModel):
    id: UUID
    integration_id: UUID
    active: bool
    generation: int
    revision: int
    interval_minutes: int
    next_due: datetime
    updated_at: datetime


class ConflictView(BaseModel):
    id: UUID
    source_id: UUID
    project_id: UUID
    revision: int
    status: str
    candidate: dict
    local: dict
    source_updated_at: datetime | None
    source_observed_at: datetime
    fingerprint: str


class Resolution(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: Literal["keep_local", "accept_source"]
    local_revision: int
    source_fingerprint: str
