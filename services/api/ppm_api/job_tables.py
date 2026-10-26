"""Persistent asynchronous authority. Broker messages contain identifiers only."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.database import Base

metadata = Base.metadata


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


integrations = tenant_table(
    "job_integrations",
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("session_id", sa.Uuid(), sa.ForeignKey("identity_sessions.id"), nullable=False),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.UniqueConstraint("organization_id", "project_id", "id"),
    sa.Column("config", JSONB(), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("enabled", sa.Boolean(), nullable=False),
    sa.Column("cursor", sa.String(200), nullable=True),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)
jobs = tenant_table(
    "durable_jobs",
    sa.Column("integration_id", sa.Uuid(), nullable=True),
    sa.Column("document_version_id", sa.Uuid(), nullable=True),
    sa.Column("ai_run_id", sa.Uuid(), nullable=True),
    sa.Column("ml_run_id", sa.Uuid(), nullable=True),
    sa.Column("connector_generation", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "ml_run_id"],
        ["ml_runs.organization_id", "ml_runs.id"],
        name="fk_job_ml_run",
    ),
    sa.ForeignKeyConstraint(
        ["organization_id", "ai_run_id"],
        ["ai_runs.organization_id", "ai_runs.id"],
        name="fk_job_ai_run",
    ),
    sa.ForeignKeyConstraint(
        ["organization_id", "document_version_id"],
        ["source_versions.organization_id", "source_versions.id"],
        name="fk_job_document_version",
    ),
    sa.CheckConstraint(
        "num_nonnulls(integration_id,document_version_id,ai_run_id,ml_run_id)=1",
        name="ck_job_source_kind",
    ),
    sa.ForeignKeyConstraint(
        ["organization_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.id"],
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("session_id", sa.Uuid(), sa.ForeignKey("identity_sessions.id"), nullable=False),
    sa.Column("key", sa.String(160), nullable=False),
    sa.Column("request_hash", sa.String(64), nullable=False),
    sa.UniqueConstraint("organization_id", "actor_id", "key"),
    sa.Column("config", JSONB(), nullable=False),
    sa.Column("input", JSONB(), nullable=False),
    sa.Column("status", sa.String(24), nullable=False),
    sa.CheckConstraint(
        "status IN ('queued','running','retry_wait','succeeded',"
        "'partially_succeeded','failed','cancelled')"
    ),
    sa.Column("attempt", sa.Integer(), nullable=False),
    sa.Column("position", sa.Integer(), nullable=False),
    sa.Column("accepted", sa.Integer(), nullable=False),
    sa.Column("errors", JSONB(), nullable=False),
    sa.Column("cancel_requested", sa.Boolean(), nullable=False),
    sa.Column("lease_token", sa.Uuid(), nullable=True),
    sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("lease_until", sa.DateTime(timezone=True), nullable=True),
    sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("sequence", sa.Integer(), nullable=False),
)
outbox = tenant_table(
    "job_outbox",
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
    sa.UniqueConstraint("job_id"),
    sa.Column("envelope", JSONB(), nullable=False),
    sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
)
events = tenant_table(
    "job_events",
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
    sa.Column("sequence", sa.Integer(), nullable=False),
    sa.UniqueConstraint("job_id", "sequence"),
    sa.Column("stage", sa.String(40), nullable=False),
    sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
)
sources = tenant_table(
    "ingestion_sources",
    sa.Column("integration_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.id"],
    ),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.project_id", "job_integrations.id"],
    ),
    sa.Column("work_item_id", sa.Uuid(), nullable=True),
    sa.Column("sprint_id", sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "work_item_id"],
        ["ppm_work_items.organization_id", "ppm_work_items.project_id", "ppm_work_items.id"],
    ),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "sprint_id"],
        ["ppm_sprints.organization_id", "ppm_sprints.project_id", "ppm_sprints.id"],
    ),
    sa.CheckConstraint(
        "(target_kind='work_items' AND target_id=work_item_id "
        "AND work_item_id IS NOT NULL AND sprint_id IS NULL) OR "
        "(target_kind='sprints' AND target_id=sprint_id "
        "AND sprint_id IS NOT NULL AND work_item_id IS NULL)"
    ),
    sa.Column("external_id", sa.String(160), nullable=False),
    sa.Column("logical_key", sa.String(64), nullable=True),
    sa.UniqueConstraint("organization_id", "project_id", "logical_key", name="uq_source_logical"),
    sa.UniqueConstraint("integration_id", "external_id"),
    sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("source_observed_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("fingerprint", sa.String(64), nullable=False),
    sa.Column("target_id", sa.Uuid(), nullable=False),
    sa.Column("target_kind", sa.String(20), nullable=False),
    sa.Column("target_revision", sa.Integer(), nullable=False),
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
)
TABLES = (integrations, jobs, outbox, events, sources)
