"""Tenant scoped connector authority, conflict review and immutable ML lineage."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.job_tables import tenant_table

principals = tenant_table(
    "connector_principals",
    sa.Column("integration_id", sa.Uuid(), nullable=False, unique=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.id"],
    ),
    sa.Column("active", sa.Boolean(), nullable=False),
    sa.Column("generation", sa.Integer(), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("interval_minutes", sa.Integer(), nullable=False),
    sa.Column("next_due", sa.DateTime(timezone=True), nullable=False),
    sa.Column("approved_by", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "approved_by"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)
conflicts = tenant_table(
    "ingestion_conflicts",
    sa.Column("source_id", sa.Uuid(), nullable=False, unique=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "source_id"],
        ["ingestion_sources.organization_id", "ingestion_sources.id"],
    ),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("status", sa.String(24), nullable=False),
    sa.Column("candidate", JSONB(), nullable=False),
    sa.Column("local", JSONB(), nullable=False),
    sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("source_observed_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("fingerprint", sa.String(64), nullable=False),
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
)


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
TABLES = (principals, conflicts, histories, datasets, runs)
