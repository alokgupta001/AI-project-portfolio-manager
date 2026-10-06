"""Sprint 04 relational system of record; tenant-safe keys on every relationship."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.schema import SchemaItem

from ppm_api.database import Base

metadata = Base.metadata
TABLES: dict[str, sa.Table] = {}


def col(name: str, type_: sa.types.TypeEngine, nullable: bool = False) -> sa.Column:
    return sa.Column(name, type_, nullable=nullable)


def ref(target: str, field: str, project: bool = False) -> sa.ForeignKeyConstraint:
    local = ["organization_id", "project_id", field] if project else ["organization_id", field]
    remote = (
        [f"ppm_{target}.organization_id", f"ppm_{target}.project_id", f"ppm_{target}.id"]
        if project
        else [f"ppm_{target}.organization_id", f"ppm_{target}.id"]
    )
    return sa.ForeignKeyConstraint(local, remote)


def table(kind: str, *extra: SchemaItem) -> sa.Table:
    t = sa.Table(
        "ppm_" + kind,
        metadata,
        col("id", sa.Uuid()),
        col("organization_id", sa.Uuid()),
        col("name", sa.String(160)),
        col("description", sa.Text()),
        col("revision", sa.Integer()),
        col("archived", sa.Boolean()),
        col("created_at", sa.DateTime(timezone=True)),
        col("updated_at", sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "id"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.CheckConstraint("revision > 0"),
        *extra,
    )
    sa.Index("ix_ppm_" + kind + "_org", t.c.organization_id)
    TABLES[kind] = t
    return t


def owner() -> list[SchemaItem]:
    return [
        col("owner_id", sa.Uuid(), True),
        sa.ForeignKeyConstraint(
            ["organization_id", "owner_id"], ["memberships.organization_id", "memberships.user_id"]
        ),
    ]


def project() -> list[SchemaItem]:
    return [
        col("project_id", sa.Uuid()),
        ref("projects", "project_id"),
        sa.UniqueConstraint("organization_id", "project_id", "id"),
    ]


settings = table(
    "settings",
    col("timezone", sa.String(80)),
    col("currency", sa.String(3)),
    sa.UniqueConstraint("organization_id"),
)
departments = table("departments", *owner())
teams = table(
    "teams", col("department_id", sa.Uuid(), True), ref("departments", "department_id"), *owner()
)
goals = table("goals", *owner())
portfolios = table("portfolios", *owner())
programs = table(
    "programs",
    col("portfolio_id", sa.Uuid()),
    ref("portfolios", "portfolio_id"),
    sa.UniqueConstraint("organization_id", "portfolio_id", "id"),
    *owner(),
)
projects = table(
    "projects",
    col("portfolio_id", sa.Uuid()),
    ref("portfolios", "portfolio_id"),
    col("program_id", sa.Uuid(), True),
    sa.ForeignKeyConstraint(
        ["organization_id", "portfolio_id", "program_id"],
        ["ppm_programs.organization_id", "ppm_programs.portfolio_id", "ppm_programs.id"],
    ),
    col("department_id", sa.Uuid(), True),
    ref("departments", "department_id"),
    col("team_id", sa.Uuid(), True),
    ref("teams", "team_id"),
    *owner(),
    col("created_by", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "created_by"], ["memberships.organization_id", "memberships.user_id"]
    ),
    col("status", sa.String(20)),
    col("reported_health", sa.String(10)),
    col("currency", sa.String(3)),
    col("ledger_complete", sa.Boolean()),
    col("start_date", sa.Date(), True),
    col("target_end_date", sa.Date(), True),
    col("forecast_end_date", sa.Date(), True),
    col("actual_start_date", sa.Date(), True),
    col("actual_end_date", sa.Date(), True),
    sa.CheckConstraint(
        "target_end_date IS NULL OR start_date IS NULL OR target_end_date >= start_date"
    ),
    sa.CheckConstraint("status IN ('draft','active','on_hold','completed','cancelled')"),
    sa.CheckConstraint("reported_health IN ('Green','Amber','Red','Unknown')"),
)
grants = table(
    "grants",
    col("user_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    col("project_id", sa.Uuid(), True),
    ref("projects", "project_id"),
    col("portfolio_id", sa.Uuid(), True),
    ref("portfolios", "portfolio_id"),
    col("access", sa.String(10)),
    sa.CheckConstraint("(project_id IS NULL) <> (portfolio_id IS NULL)"),
    sa.CheckConstraint("access IN ('read','edit','manage')"),
    sa.UniqueConstraint("organization_id", "user_id", "project_id"),
    sa.UniqueConstraint("organization_id", "user_id", "portfolio_id"),
)
team_members = table(
    "team_members",
    col("team_id", sa.Uuid()),
    ref("teams", "team_id"),
    col("user_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    col("start_date", sa.Date()),
    col("end_date", sa.Date(), True),
    sa.CheckConstraint("end_date IS NULL OR end_date > start_date"),
)
sprints = table(
    "sprints",
    *project(),
    col("team_id", sa.Uuid()),
    ref("teams", "team_id"),
    col("start_date", sa.Date()),
    col("end_date", sa.Date()),
    col("status", sa.String(12)),
    sa.CheckConstraint("end_date >= start_date"),
    sa.CheckConstraint("status IN ('planned','active','closed')"),
)
work_items = table(
    "work_items",
    *project(),
    col("sprint_id", sa.Uuid(), True),
    ref("sprints", "sprint_id", True),
    *owner(),
    col("status", sa.String(12)),
    col("blocked", sa.Boolean()),
    col("points", sa.Numeric(10, 2), True),
    col("start_date", sa.Date(), True),
    col("due_date", sa.Date(), True),
    sa.CheckConstraint("status IN ('backlog','ready','in_progress','done')"),
    sa.CheckConstraint("points IS NULL OR points >= 0"),
    sa.CheckConstraint("due_date IS NULL OR start_date IS NULL OR due_date >= start_date"),
)
milestones = table(
    "milestones",
    *project(),
    col("due_date", sa.Date()),
    col("actual_date", sa.Date(), True),
    col("critical", sa.Boolean()),
)
blockers = table(
    "blockers",
    *project(),
    col("work_item_id", sa.Uuid(), True),
    ref("work_items", "work_item_id", True),
    *owner(),
    col("status", sa.String(10)),
    sa.CheckConstraint("status IN ('open','resolved')"),
)
dependencies = table(
    "dependencies",
    *project(),
    col("target_project_id", sa.Uuid()),
    ref("projects", "target_project_id"),
    col("source_milestone_id", sa.Uuid(), True),
    ref("milestones", "source_milestone_id", True),
    col("source_work_item_id", sa.Uuid(), True),
    ref("work_items", "source_work_item_id", True),
    col("target_milestone_id", sa.Uuid(), True),
    sa.ForeignKeyConstraint(
        ["organization_id", "target_project_id", "target_milestone_id"],
        ["ppm_milestones.organization_id", "ppm_milestones.project_id", "ppm_milestones.id"],
    ),
    col("target_work_item_id", sa.Uuid(), True),
    sa.ForeignKeyConstraint(
        ["organization_id", "target_project_id", "target_work_item_id"],
        ["ppm_work_items.organization_id", "ppm_work_items.project_id", "ppm_work_items.id"],
    ),
    sa.CheckConstraint("source_milestone_id IS NULL OR source_work_item_id IS NULL"),
    sa.CheckConstraint("target_milestone_id IS NULL OR target_work_item_id IS NULL"),
)
budget_lines = table(
    "budget_lines",
    *project(),
    col("amount", sa.Numeric(18, 2)),
    col("currency", sa.String(3)),
    col("approved", sa.Boolean()),
    sa.CheckConstraint("amount >= 0"),
)
expenditures = table(
    "expenditures",
    *project(),
    col("amount", sa.Numeric(18, 2)),
    col("currency", sa.String(3)),
    col("spent_on", sa.Date()),
    col("reversal_of", sa.Uuid(), True),
    ref("expenditures", "reversal_of", True),
    sa.UniqueConstraint("organization_id", "reversal_of"),
    sa.CheckConstraint(
        "(amount >= 0 AND reversal_of IS NULL) OR (amount < 0 AND reversal_of IS NOT NULL)"
    ),
)
status_updates = table(
    "status_updates",
    *project(),
    col("reported_health", sa.String(10)),
    sa.CheckConstraint("reported_health IN ('Green','Amber','Red','Unknown')"),
)
baselines = table(
    "baselines",
    *project(),
    col("version", sa.Integer()),
    col("snapshot", JSONB()),
    sa.UniqueConstraint("organization_id", "project_id", "version"),
)
alignments = table(
    "alignments",
    col("project_id", sa.Uuid(), True),
    ref("projects", "project_id"),
    col("portfolio_id", sa.Uuid(), True),
    ref("portfolios", "portfolio_id"),
    col("goal_id", sa.Uuid()),
    ref("goals", "goal_id"),
    col("weight", sa.Numeric(6, 5)),
    col("contribution", sa.Numeric(6, 5)),
    sa.CheckConstraint("(project_id IS NULL) <> (portfolio_id IS NULL)"),
    sa.CheckConstraint("weight >= 0 AND weight <= 1 AND contribution >= 0 AND contribution <= 1"),
)
audit = sa.Table(
    "ppm_audit",
    metadata,
    col("id", sa.Uuid()),
    col("organization_id", sa.Uuid()),
    col("project_id", sa.Uuid(), True),
    ref("projects", "project_id"),
    col("actor_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    col("resource", sa.String(30)),
    col("target_id", sa.Uuid()),
    col("before", JSONB(), True),
    col("after", JSONB()),
    col("request_id", sa.Uuid()),
    col("created_at", sa.DateTime(timezone=True)),
    sa.PrimaryKeyConstraint("id"),
)
requests = sa.Table(
    "ppm_requests",
    metadata,
    col("organization_id", sa.Uuid()),
    col("user_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    col("key", sa.Uuid()),
    col("fingerprint", sa.String(64)),
    col("resource", sa.String(30)),
    col("target_id", sa.Uuid()),
    sa.PrimaryKeyConstraint("organization_id", "user_id", "key"),
)


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
