"""Typed write/read contracts; server fields never accepted as user-controlled scope."""

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ppm_api.capacity_schemas import (
    AllocationInput,
    AvailabilityInput,
    CalendarInput,
    CapacitySnapshotInput,
    EffortCoverageInput,
    EffortInput,
    ResourceAccessInput,
    ResourceInput,
    ResourceSkillInput,
    ResourceTeamInput,
    TimeOffInput,
)

Kind = Literal[
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


class SettingsInput(Common):
    kind: Literal["settings"] = "settings"
    timezone: str
    currency: Currency

    @field_validator("timezone")
    @classmethod
    def valid_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError) as e:
            raise ValueError("Use an IANA timezone") from e
        return value


class DepartmentInput(Owned):
    kind: Literal["departments"] = "departments"


class GoalInput(Owned):
    kind: Literal["goals"] = "goals"


class PortfolioInput(Owned):
    kind: Literal["portfolios"] = "portfolios"


class TeamInput(Owned):
    kind: Literal["teams"] = "teams"
    department_id: UUID | None = None


class ProgramInput(Owned):
    kind: Literal["programs"] = "programs"
    portfolio_id: UUID


class ProjectInput(Owned):
    kind: Literal["projects"] = "projects"
    portfolio_id: UUID
    program_id: UUID | None = None
    department_id: UUID | None = None
    team_id: UUID | None = None
    status: Literal["draft", "active", "on_hold", "completed", "cancelled"] = "draft"
    reported_health: Health = "Unknown"
    currency: Currency
    ledger_complete: bool = False
    start_date: date | None = None
    target_end_date: date | None = None
    forecast_end_date: date | None = None
    actual_start_date: date | None = None
    actual_end_date: date | None = None

    @model_validator(mode="after")
    def dates(self) -> "ProjectInput":
        for end in [self.target_end_date, self.forecast_end_date, self.actual_end_date]:
            if self.start_date and end and end < self.start_date:
                raise ValueError("End precedes start")
        if (
            self.actual_start_date
            and self.actual_end_date
            and self.actual_end_date < self.actual_start_date
        ):
            raise ValueError("Actual end precedes actual start")
        if self.status == "completed" and not self.actual_end_date:
            raise ValueError("Completed project needs actual finish")
        return self


class GrantInput(Common):
    kind: Literal["grants"] = "grants"
    user_id: UUID
    project_id: UUID | None = None
    portfolio_id: UUID | None = None
    access: Literal["read", "edit", "manage"] = "read"

    @model_validator(mode="after")
    def target(self) -> "GrantInput":
        if (self.project_id is None) == (self.portfolio_id is None):
            raise ValueError("Choose exactly one scope")
        if self.portfolio_id and self.access == "edit":
            raise ValueError("Portfolio grants are read or manage")
        return self


class TeamMemberInput(Common):
    kind: Literal["team_members"] = "team_members"
    team_id: UUID
    user_id: UUID
    start_date: date
    end_date: date | None = None

    @model_validator(mode="after")
    def dates(self) -> "TeamMemberInput":
        if self.end_date and self.end_date <= self.start_date:
            raise ValueError("End must follow start")
        return self


class ProjectChild(Common):
    project_id: UUID


class SprintInput(ProjectChild):
    kind: Literal["sprints"] = "sprints"
    team_id: UUID
    start_date: date
    end_date: date
    status: Literal["planned", "active", "closed"] = "planned"

    @model_validator(mode="after")
    def dates(self) -> "SprintInput":
        if self.end_date < self.start_date:
            raise ValueError("End precedes start")
        return self


class WorkInput(ProjectChild):
    kind: Literal["work_items"] = "work_items"
    owner_id: UUID | None = None
    sprint_id: UUID | None = None
    status: Literal["backlog", "ready", "in_progress", "done"] = "backlog"
    blocked: bool = False
    points: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)] | None = None
    start_date: date | None = None
    due_date: date | None = None

    @model_validator(mode="after")
    def dates(self) -> "WorkInput":
        if self.start_date and self.due_date and self.due_date < self.start_date:
            raise ValueError("Due date precedes start")
        return self


class MilestoneInput(ProjectChild):
    kind: Literal["milestones"] = "milestones"
    due_date: date
    actual_date: date | None = None
    critical: bool = False


class BlockerInput(ProjectChild):
    kind: Literal["blockers"] = "blockers"
    work_item_id: UUID | None = None
    owner_id: UUID | None = None
    status: Literal["open", "resolved"] = "open"


class DependencyInput(ProjectChild):
    kind: Literal["dependencies"] = "dependencies"
    target_project_id: UUID
    source_milestone_id: UUID | None = None
    source_work_item_id: UUID | None = None
    target_milestone_id: UUID | None = None
    target_work_item_id: UUID | None = None

    @model_validator(mode="after")
    def endpoints(self) -> "DependencyInput":
        if (
            self.source_milestone_id
            and self.source_work_item_id
            or self.target_milestone_id
            and self.target_work_item_id
        ):
            raise ValueError("Only one node type per endpoint")
        return self


class BudgetInput(ProjectChild):
    kind: Literal["budget_lines"] = "budget_lines"
    amount: Money = Field(ge=0)
    currency: Currency
    approved: bool = True


class ExpenditureInput(ProjectChild):
    kind: Literal["expenditures"] = "expenditures"
    amount: Money
    currency: Currency
    spent_on: date
    reversal_of: UUID | None = None


class StatusInput(ProjectChild):
    kind: Literal["status_updates"] = "status_updates"
    reported_health: Health


class BaselineInput(ProjectChild):
    kind: Literal["baselines"] = "baselines"


class AlignmentInput(Common):
    kind: Literal["alignments"] = "alignments"
    project_id: UUID | None = None
    portfolio_id: UUID | None = None
    goal_id: UUID
    weight: Fraction
    contribution: Fraction

    @model_validator(mode="after")
    def target(self) -> "AlignmentInput":
        if (self.project_id is None) == (self.portfolio_id is None):
            raise ValueError("Choose exactly one alignment target")
        return self


Input = Annotated[
    SettingsInput
    | DepartmentInput
    | GoalInput
    | PortfolioInput
    | TeamInput
    | ProgramInput
    | ProjectInput
    | GrantInput
    | TeamMemberInput
    | SprintInput
    | WorkInput
    | MilestoneInput
    | BlockerInput
    | DependencyInput
    | BudgetInput
    | ExpenditureInput
    | StatusInput
    | BaselineInput
    | AlignmentInput
    | ResourceInput
    | CalendarInput
    | AvailabilityInput
    | ResourceTeamInput
    | ResourceSkillInput
    | TimeOffInput
    | AllocationInput
    | ResourceAccessInput
    | EffortInput
    | EffortCoverageInput
    | CapacitySnapshotInput,
    Field(discriminator="kind"),
]


class RecordView(BaseModel):
    id: UUID
    organization_id: UUID
    revision: int
    created_at: datetime
    updated_at: datetime
    data: Input


class PageView(BaseModel):
    items: list[RecordView]
    total: int
    offset: int
    limit: int
    as_of: datetime


class BaselineView(BaseModel):
    id: UUID
    version: int
    created_at: datetime
    reason: str
    snapshot: dict


class MoneyTotal(BaseModel):
    currency: str
    approved_budget: Decimal
    recorded_spend: Decimal
    usage_percent: Decimal | None
    ledger_complete: bool


class SummaryView(BaseModel):
    project: RecordView
    can_edit: bool
    can_manage: bool
    money: list[MoneyTotal]
    alignment_percent: Decimal | None
    alignment_complete: bool
    computed_health: None = None
    baselines: list[BaselineView]
    work_counts: dict[str, int]
    as_of: datetime
    metric_version: Literal["delivery-v1"] = "delivery-v1"


class AlignmentSet(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[AlignmentInput] = Field(max_length=100)


class PersonView(BaseModel):
    id: UUID
    name: str


class HistoryView(BaseModel):
    id: UUID
    created_at: datetime
    actor_id: UUID
    before: dict | None
    after: dict


class PortfolioSummary(BaseModel):
    portfolio: RecordView
    visible_projects: int
    money: list[MoneyTotal]
    as_of: datetime
    scope: Literal["authorized_projects"] = "authorized_projects"
