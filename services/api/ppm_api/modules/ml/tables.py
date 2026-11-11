"""Tenant scoped connector authority, conflict review and immutable ML lineage."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.shared.table_base import tenant_table


def project_table(name: str, *columns: sa.Column | sa.Constraint) -> sa.Table:
    """All lineage stays within its owning project and tenant."""
    return tenant_table(
        name,
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
        ),
        sa.UniqueConstraint("organization_id", "project_id", "id"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        *columns,
    )


histories = project_table(
    "ml_histories",
    sa.Column("name", sa.String(160), nullable=False),
    sa.Column("version", sa.Integer(), nullable=False),
    sa.UniqueConstraint("organization_id", "project_id", "name", "version"),
    sa.Column("digest", sa.String(64), nullable=False),
    sa.Column("manifest", JSONB(), nullable=False),
    sa.Column("records", JSONB(), nullable=False),
    sa.Column("withdrawn", sa.Boolean(), nullable=False),
)
datasets = project_table(
    "ml_datasets",
    sa.Column("history_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "history_id"],
        ["ml_histories.organization_id", "ml_histories.project_id", "ml_histories.id"],
    ),
    sa.Column("digest", sa.String(64), nullable=False),
    sa.Column("manifest", JSONB(), nullable=False),
    sa.Column("records", JSONB(), nullable=False),
)
runs = project_table(
    "ml_runs",
    sa.Column("dataset_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "dataset_id"],
        ["ml_datasets.organization_id", "ml_datasets.project_id", "ml_datasets.id"],
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("status", sa.String(32), nullable=False),
    sa.Column("card", JSONB(), nullable=False),
    sa.Column("artifacts", JSONB(), nullable=False),
)
TABLES = (histories, datasets, runs)
