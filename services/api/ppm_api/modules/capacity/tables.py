"""Workforce and capacity table definitions."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.schema import SchemaItem

from ppm_api.shared.table_base import col, project, ref, table

resources = table(
    "resources",
    col("user_id", sa.Uuid(), True),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
)

calendars = table(
    "calendars",
    col("timezone", sa.String(80)),
    col("holidays", sa.Text()),
    *[
        col(day, sa.Numeric(4, 2))
        for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    ],
    *[
        sa.CheckConstraint(f"{day} >= 0 AND {day} <= 24")
        for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    ],
)


def resource() -> list[SchemaItem]:
    return [col("resource_id", sa.Uuid()), ref("resources", "resource_id")]


def period() -> list[SchemaItem]:
    return [
        col("start_date", sa.Date()),
        col("end_date", sa.Date()),
        sa.CheckConstraint("end_date > start_date"),
    ]


availability = table(
    "availability",
    *resource(),
    *period(),
    col("calendar_id", sa.Uuid()),
    ref("calendars", "calendar_id"),
)

resource_teams = table(
    "resource_teams", *resource(), *period(), col("team_id", sa.Uuid()), ref("teams", "team_id")
)

resource_skills = table("resource_skills", *resource(), col("skill", sa.String(80)))

time_off = table(
    "time_off",
    *resource(),
    *period(),
    col("hours_per_day", sa.Numeric(4, 2)),
    sa.CheckConstraint("hours_per_day >= 0 AND hours_per_day <= 24"),
)

allocations = table(
    "allocations",
    *resource(),
    *project(),
    *period(),
    col("hours_per_day", sa.Numeric(4, 2)),
    sa.CheckConstraint("hours_per_day >= 0 AND hours_per_day <= 24"),
)

resource_access = table(
    "resource_access",
    *resource(),
    col("user_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    col("manage", sa.Boolean()),
    col("effort", sa.Boolean()),
    sa.UniqueConstraint("organization_id", "resource_id", "user_id"),
)

effort = table(
    "effort",
    *resource(),
    *project(),
    col("worked_on", sa.Date()),
    col("hours", sa.Numeric(4, 2)),
    col("overtime_hours", sa.Numeric(4, 2)),
    sa.CheckConstraint("hours >= 0 AND hours <= 24"),
    sa.CheckConstraint("overtime_hours >= 0 AND overtime_hours <= hours"),
)

effort_coverage = table(
    "effort_coverage",
    *resource(),
    col("worked_on", sa.Date()),
    col("complete", sa.Boolean()),
    sa.UniqueConstraint("organization_id", "resource_id", "worked_on"),
)

capacity_snapshots = table("capacity_snapshots", *resource(), *period(), col("snapshot", JSONB()))
