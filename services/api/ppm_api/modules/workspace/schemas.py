"""Validated request/response contracts for this feature."""

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

SearchKind = Literal["projects", "work_items", "risks", "assessments"]


class SearchItem(BaseModel):
    id: UUID
    kind: SearchKind
    name: str
    organization_id: UUID
    project_id: UUID | None = None
    href: str
    due_date: date | None = None


class SearchPage(BaseModel):
    items: list[SearchItem]
    total: int
    offset: int
    limit: int


class PreferenceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool
