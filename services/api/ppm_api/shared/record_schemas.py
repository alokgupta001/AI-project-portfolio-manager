"""Typed record inputs owned by this package."""

from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

Kind = Literal[
    "risks",
    "benefits",
    "metric_plans",
    "metric_policies",
    "saved_views",
    "resources",
    "calendars",
    "availability",
    "resource_teams",
    "resource_skills",
    "time_off",
    "allocations",
    "resource_access",
    "effort",
    "effort_coverage",
    "capacity_snapshots",
    "settings",
    "departments",
    "teams",
    "goals",
    "portfolios",
    "programs",
    "projects",
    "grants",
    "team_members",
    "sprints",
    "work_items",
    "milestones",
    "blockers",
    "dependencies",
    "budget_lines",
    "expenditures",
    "status_updates",
    "baselines",
    "alignments",
]

Money = Annotated[Decimal, Field(max_digits=18, decimal_places=2, allow_inf_nan=False)]

Fraction = Annotated[
    Decimal, Field(ge=0, le=1, max_digits=6, decimal_places=5, allow_inf_nan=False)
]

Currency = Annotated[str, Field(pattern=r"^[A-Z]{3}$")]

Health = Literal["Green", "Amber", "Red", "Unknown"]


class Common(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=4000)
    archived: bool = False


class Owned(Common):
    owner_id: UUID | None = None


class ProjectChild(Common):
    project_id: UUID
