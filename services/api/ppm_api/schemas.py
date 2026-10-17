from datetime import datetime
from typing import Final, Literal
from uuid import UUID

from pydantic import BaseModel, Field

SCHEMA_REVISION: Final = "0014_specialist_reviewer"


class ErrorDetail(BaseModel):
    field: str
    reason: str


class ErrorBody(BaseModel):
    code: str
    message: str
    request_id: str
    details: list[ErrorDetail] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    error: ErrorBody


class HealthResponse(BaseModel):
    status: Literal["alive"] = "alive"
    service: Literal["enterprise-ppm-api"] = "enterprise-ppm-api"


class DependencyStatus(BaseModel):
    name: Literal["database", "redis", "storage"]
    status: Literal["ready", "unavailable"]


class ReadyResponse(BaseModel):
    status: Literal["ready", "not_ready"]
    dependencies: list[DependencyStatus]


class FoundationResponse(BaseModel):
    instance_id: UUID
    initialized_at: datetime
    schema_revision: Literal["0014_specialist_reviewer"] = SCHEMA_REVISION
    environment: Literal["local", "test", "demo"]
