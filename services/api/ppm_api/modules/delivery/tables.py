"""Sprint 04 relational system of record; tenant-safe keys on every relationship."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.shared.table_base import col, metadata, owner, project, ref, table

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
    *[
        col(key, sa.String(30), True)
        for key in ["priority", "industry", "category", "methodology", "size_band"]
    ],
    *[
        sa.CheckConstraint(f"{key} IS NULL OR {key} IN ({options})", name=f"ck_ppm_projects_{key}")
        for key, options in {
            "priority": "'low','normal','high','urgent'",
            "industry": "'fintech','technology','healthcare','public_sector','other'",
            "category": "'delivery','transformation','compliance','research','other'",
            "methodology": "'agile','waterfall','hybrid','other'",
            "size_band": "'small','medium','large'",
        }.items()
    ],
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
    col("priority", sa.String(30), True),
    col("work_type", sa.String(30), True),
    sa.CheckConstraint(
        "priority IS NULL OR priority IN ('low','normal','high','urgent')",
        name="ck_ppm_work_items_priority",
    ),
    sa.CheckConstraint(
        "work_type IS NULL OR work_type IN ('task','bug','story','feature','other')",
        name="ck_ppm_work_items_work_type",
    ),
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
