# ruff: noqa: E501
"""Add command-center records without changing prior migrations or history."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.schema import SchemaItem

revision = "0006_command_center"
down_revision = "0005_assessment"
branch_labels = None
depends_on = None
metadata = sa.MetaData()
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

KINDS = tuple(TABLES)
OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"
ADMIN = "current_setting('ppm.role',true)='Admin'"
PM = "current_setting('ppm.role',true)='Project Manager'"


def upgrade():
    metadata.reflect(
        op.get_bind(),
        only=[
            "organizations",
            "memberships",
            "ppm_projects",
            "ppm_calendars",
            "ppm_baselines",
            "ppm_portfolios",
            "ppm_sprints",
            "ppm_teams",
        ],
    )
    metadata.create_all(op.get_bind(), tables=[TABLES[k] for k in KINDS])
    for kind in KINDS:
        name = "ppm_" + kind
        read = f"EXISTS (SELECT 1 FROM ppm_projects p WHERE p.id={name}.project_id AND p.organization_id={OID})"
        write = f"({ADMIN} OR ({PM} AND EXISTS (SELECT 1 FROM ppm_grants g WHERE g.organization_id={OID} AND g.user_id={UID} AND NOT g.archived AND g.project_id={name}.project_id AND g.access IN ('edit','manage'))))"
        if kind == "metric_policies":
            read, write = "true", ADMIN
        if kind == "saved_views":
            read = write = f"user_id={UID}"
        op.execute(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY tenant_read ON {name} FOR SELECT TO ppm_app USING (organization_id={OID} AND ({read}))"
        )
        op.execute(
            f"CREATE POLICY tenant_insert ON {name} FOR INSERT TO ppm_app WITH CHECK (organization_id={OID} AND ({write}))"
        )
        op.execute(f"GRANT SELECT,INSERT ON {name} TO ppm_app")
        if kind != "sprint_closures":
            op.execute(
                f"CREATE POLICY tenant_update ON {name} FOR UPDATE TO ppm_app USING (organization_id={OID} AND ({write})) WITH CHECK (organization_id={OID} AND ({write}))"
            )
            op.execute(f"GRANT UPDATE ON {name} TO ppm_app")


def downgrade():
    for kind in reversed(KINDS):
        op.drop_table("ppm_" + kind)
