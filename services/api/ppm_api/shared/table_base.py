"""Shared SQLAlchemy record-table construction and registry primitives."""

import sqlalchemy as sa
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


def tenant_table(name: str, *columns: sa.Column | sa.Constraint) -> sa.Table:
    return sa.Table(
        name,
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.UniqueConstraint("organization_id", "id"),
        *columns,
    )
