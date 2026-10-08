"""One typed snapshot shared by dashboards and export consumers."""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from ppm_api.capacity_schemas import CapacityView, TeamCapacityView
from ppm_api.ppm_schemas import RecordView


class Fact(BaseModel):
    id: UUID
    kind: str
    name: str
    detail: str
    updated_at: datetime


class Metric(BaseModel):
    key: str
    label: str
    value: Decimal | None
    unit: str
    period: str
    source: str
    source_updated_at: datetime | None
    freshness: Literal["fresh", "stale", "missing"]
    status: Literal["available", "partial", "unknown"]
    coverage_percent: Decimal
    explanation: str
    facts: list[Fact]


class ProjectMetrics(BaseModel):
    id: UUID
    name: str
    portfolio_id: UUID
    reported_health: str
    computed_health: str
    discrepancy: bool
    can_edit: bool
    metrics: list[Metric]


class Velocity(BaseModel):
    sprint_id: UUID
    project_id: UUID
    team_id: UUID
    name: str
    end_date: date
    points: Decimal | None
    recorded_points: Decimal
    source_updated_at: datetime | None
    freshness: str
    policy: str = "team-points-v1: completed work at closure; no cross-team ranking"


class ResourceMetric(BaseModel):
    summary: CapacityView
    source_updated_at: datetime | None
    freshness: str


class TeamMetric(BaseModel):
    name: str
    summary: TeamCapacityView


class CommandSnapshot(BaseModel):
    metric_version: Literal["command-v1"] = "command-v1"
    risk_rule: Literal["risk-rule-v1"] = "risk-rule-v1"
    computed_at: datetime
    start: date
    end: date
    timezone: str
    portfolio_id: UUID | None
    scope: str = "Current authorized projects only; hidden projects are not counted"
    policy_revision: int
    amber: Decimal
    red: Decimal
    stale_days: int
    projects: list[ProjectMetrics]
    totals: list[Metric]
    records: list[RecordView]
    velocity: list[Velocity]
    resources: list[ResourceMetric]
    teams: list[TeamMetric]
    limitations: list[str]
    compute_ms: float
