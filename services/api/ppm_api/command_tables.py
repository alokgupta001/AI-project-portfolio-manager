"""Command center facts; delivery owns mutations and audit history."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.ppm_tables import col, owner, project, ref, table

risks = table(
    "risks",
    *project(),
    *owner(),
    col("severity", sa.Integer()),
    col("likelihood", sa.Integer()),
    col("mitigation", sa.Text()),
    col("status", sa.String(20)),
    col("review_on", sa.Date()),
    col("resolution", sa.Text()),
    sa.CheckConstraint("severity BETWEEN 1 AND 5 AND likelihood BETWEEN 1 AND 5"),
    sa.CheckConstraint("status IN ('open','mitigating','accepted','closed')"),
)
benefits = table(
    "benefits",
    *project(),
    col("unit", sa.String(40)),
    col("target", sa.Numeric(18, 2)),
    col("realized", sa.Numeric(18, 2), True),
    col("period_start", sa.Date()),
    col("period_end", sa.Date()),
    sa.CheckConstraint("period_end > period_start"),
)
metric_plans = table(
    "metric_plans",
    *project(),
    col("baseline_id", sa.Uuid()),
    ref("baselines", "baseline_id", True),
    col("calendar_id", sa.Uuid()),
    ref("calendars", "calendar_id"),
    col("forecast_cost", sa.Numeric(18, 2), True),
    sa.CheckConstraint("forecast_cost IS NULL OR forecast_cost >= 0"),
    sa.UniqueConstraint("organization_id", "project_id"),
)
metric_policies = table(
    "metric_policies",
    col("amber", sa.Numeric(5, 2)),
    col("red", sa.Numeric(5, 2)),
    col("stale_days", sa.Integer()),
    sa.CheckConstraint("amber > 0 AND red > amber AND red <= 100"),
    sa.CheckConstraint("stale_days BETWEEN 1 AND 365"),
    sa.UniqueConstraint("organization_id"),
)
saved_views = table(
    "saved_views",
    col("user_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    col("portfolio_id", sa.Uuid(), True),
    ref("portfolios", "portfolio_id"),
    col("start_date", sa.Date()),
    col("end_date", sa.Date()),
    col("dashboard", sa.String(20)),
    sa.CheckConstraint("end_date > start_date AND end_date - start_date <= 366"),
    sa.CheckConstraint("dashboard IN ('Executive','Delivery','Risk','Resource')"),
)
sprint_closures = table(
    "sprint_closures",
    *project(),
    col("sprint_id", sa.Uuid()),
    ref("sprints", "sprint_id", True),
    col("team_id", sa.Uuid()),
    ref("teams", "team_id"),
    col("end_date", sa.Date()),
    col("points", sa.Numeric(18, 2)),
    col("complete", sa.Boolean()),
    col("snapshot", JSONB()),
    sa.UniqueConstraint("organization_id", "sprint_id"),
)
