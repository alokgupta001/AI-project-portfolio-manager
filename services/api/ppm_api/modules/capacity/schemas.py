"""Versioned resource planning contracts, separate from login membership."""

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Hours = Annotated[Decimal, Field(ge=0, le=24, max_digits=4, decimal_places=2)]


class CapacityCommon(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=4000)
    archived: bool = False


class ResourceInput(CapacityCommon):
    kind: Literal["resources"] = "resources"
    user_id: UUID | None = None


class CalendarInput(CapacityCommon):
    kind: Literal["calendars"] = "calendars"
    timezone: str = Field(max_length=80)
    monday: Hours
    tuesday: Hours
    wednesday: Hours
    thursday: Hours
    friday: Hours
    saturday: Hours
    sunday: Hours
    holidays: str = Field(default="", max_length=5000)

    @field_validator("timezone")
    @classmethod
    def zone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ValueError, ZoneInfoNotFoundError) as e:
            raise ValueError("Use an IANA timezone") from e
        return value

    @field_validator("holidays")
    @classmethod
    def days(cls, value: str) -> str:
        return ",".join(
            sorted(
                {date.fromisoformat(v.strip()).isoformat() for v in value.split(",") if v.strip()}
            )
        )


class ResourceChild(CapacityCommon):
    resource_id: UUID


class DatedResource(ResourceChild):
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def dates(self) -> "DatedResource":
        if self.end_date <= self.start_date:
            raise ValueError("End must follow start; the end date is excluded")
        return self


class AvailabilityInput(DatedResource):
    kind: Literal["availability"] = "availability"
    calendar_id: UUID


class ResourceTeamInput(DatedResource):
    kind: Literal["resource_teams"] = "resource_teams"
    team_id: UUID


class ResourceSkillInput(ResourceChild):
    kind: Literal["resource_skills"] = "resource_skills"
    skill: str = Field(min_length=1, max_length=80)


class TimeOffInput(DatedResource):
    kind: Literal["time_off"] = "time_off"
    hours_per_day: Hours
    # No medical reasons or raw workforce notes are collected.
    description: Literal[""] = ""


class AllocationInput(DatedResource):
    kind: Literal["allocations"] = "allocations"
    project_id: UUID
    hours_per_day: Hours


class ResourceAccessInput(ResourceChild):
    kind: Literal["resource_access"] = "resource_access"
    user_id: UUID
    manage: bool = False
    effort: bool = False


class EffortInput(ResourceChild):
    kind: Literal["effort"] = "effort"
    project_id: UUID
    worked_on: date
    hours: Hours
    overtime_hours: Hours = Decimal(0)

    @model_validator(mode="after")
    def overtime(self) -> "EffortInput":
        if self.overtime_hours > self.hours:
            raise ValueError("Overtime is included in total hours")
        return self


class EffortCoverageInput(ResourceChild):
    kind: Literal["effort_coverage"] = "effort_coverage"
    worked_on: date
    complete: bool = False


class CapacitySnapshotInput(DatedResource):
    kind: Literal["capacity_snapshots"] = "capacity_snapshots"

    @model_validator(mode="after")
    def bounded(self) -> "CapacitySnapshotInput":
        if (self.end_date - self.start_date).days > 366:
            raise ValueError("Snapshot interval must not exceed 366 days")
        return self


class CapacityDay(BaseModel):
    day: date
    timezone: str | None
    calendar_id: UUID | None
    available_hours: Decimal | None
    allocated_hours: Decimal
    excess_hours: Decimal | None
    planned_percent: Decimal | None
    actual_hours: Decimal | None
    overtime_hours: Decimal | None
    actual_percent: Decimal | None
    effort_complete: bool


class CapacityWeek(BaseModel):
    start_date: date
    end_date: date
    available_hours: Decimal | None
    allocated_hours: Decimal
    excess_hours: Decimal | None
    planned_percent: Decimal | None


class CapacityView(BaseModel):
    resource_id: UUID
    resource_name: str
    start_date: date
    end_date: date
    scope: Literal["full_resource", "visible_projects_only"]
    can_manage: bool
    can_effort: bool
    days: list[CapacityDay]
    weeks: list[CapacityWeek]
    available_hours: Decimal | None
    allocated_hours: Decimal
    excess_hours: Decimal | None
    planned_percent: Decimal | None
    actual_hours: Decimal | None
    actual_percent: Decimal | None
    effort_complete: bool
    as_of: datetime
    metric_version: Literal["capacity-v1"] = "capacity-v1"


class TeamCapacityView(BaseModel):
    team_id: UUID
    resource_count: int
    status: Literal["available", "suppressed", "insufficient_scope", "incomplete_capacity"]
    available_hours: Decimal | None = None
    allocated_hours: Decimal | None = None
    excess_hours: Decimal | None = None
    planned_percent: Decimal | None = None
    actual_percent: Decimal | None = None
    sustained_overload: bool | None = None
    overtime_warning: bool | None = None
    as_of: datetime
    label: str = "Team workload support signal; not a diagnosis or individual ranking"


class SnapshotView(BaseModel):
    id: UUID
    created_at: datetime
    snapshot: dict
