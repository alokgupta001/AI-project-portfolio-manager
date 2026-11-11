"""Typed record inputs owned by this package."""

from datetime import date
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, model_validator

from ppm_api.shared.record_schemas import Common, Money, ProjectChild


class RiskInput(ProjectChild):
    kind: Literal["risks"] = "risks"
    owner_id: UUID | None = None
    severity: int = Field(ge=1, le=5)
    likelihood: int = Field(ge=1, le=5)
    mitigation: str = Field(default="", max_length=4000)
    status: Literal["open", "mitigating", "accepted", "closed"] = "open"
    review_on: date
    resolution: str = Field(default="", max_length=4000)

    @model_validator(mode="after")
    def readiness(self) -> "RiskInput":
        if self.status == "mitigating" and (not self.owner_id or not self.mitigation):
            raise ValueError("Mitigation requires an owner and plan")
        if self.status in ("accepted", "closed") and (not self.owner_id or not self.resolution):
            raise ValueError("Acceptance/closure requires an owner and resolution")
        return self


class BenefitInput(ProjectChild):
    kind: Literal["benefits"] = "benefits"
    unit: str = Field(min_length=1, max_length=40)
    target: Money
    realized: Money | None = None
    period_start: date
    period_end: date

    @model_validator(mode="after")
    def period(self) -> "BenefitInput":
        if self.period_end <= self.period_start:
            raise ValueError("End must follow start")
        return self


class MetricPlanInput(ProjectChild):
    kind: Literal["metric_plans"] = "metric_plans"
    baseline_id: UUID
    calendar_id: UUID
    forecast_cost: Money | None = Field(default=None, ge=0)


class MetricPolicyInput(Common):
    kind: Literal["metric_policies"] = "metric_policies"
    amber: Annotated[Decimal, Field(gt=0, le=100, decimal_places=2)] = Decimal(30)
    red: Annotated[Decimal, Field(gt=0, le=100, decimal_places=2)] = Decimal(60)
    stale_days: int = Field(default=7, ge=1, le=365)

    @model_validator(mode="after")
    def thresholds(self) -> "MetricPolicyInput":
        if self.red <= self.amber or self.archived:
            raise ValueError("Red must exceed amber; policy cannot be archived")
        return self


class SavedViewInput(Common):
    kind: Literal["saved_views"] = "saved_views"
    user_id: UUID
    portfolio_id: UUID | None = None
    start_date: date
    end_date: date
    dashboard: Literal["Executive", "Delivery", "Risk", "Resource"] = "Executive"

    @model_validator(mode="after")
    def period(self) -> "SavedViewInput":
        if not 0 < (self.end_date - self.start_date).days <= 366:
            raise ValueError("Choose 1–366 days, end excluded")
        return self
