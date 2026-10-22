"""Durable hybrid checkpoints and owner-only shared provider admission state."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.database import Base
from ppm_api.document_tables import tab

tasks = tab(
    "agent_tasks",
    sa.Column("run_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id"], ["ai_runs.organization_id", "ai_runs.id"]
    ),
    sa.UniqueConstraint("organization_id", "run_id", "id"),
    sa.Column("task_key", sa.String(64), nullable=False),
    sa.UniqueConstraint("run_id", "task_key"),
    sa.Column("agent", sa.String(20), nullable=False),
    sa.Column("kind", sa.String(16), nullable=False),
    sa.Column("logical_section_id", sa.String(64), nullable=False),
    sa.Column("section_id", sa.String(64), nullable=False),
    sa.Column("parent_task_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id", "parent_task_id"],
        ["agent_tasks.organization_id", "agent_tasks.run_id", "agent_tasks.id"],
    ),
    sa.Column("dependencies", JSONB(), nullable=False),
    sa.Column("input_manifest", JSONB(), nullable=False),
    sa.Column("input_hash", sa.String(64), nullable=False),
    sa.Column("schema_hash", sa.String(64), nullable=False),
    sa.Column("prompt_hash", sa.String(64), nullable=False),
    sa.Column("policy_hash", sa.String(64), nullable=False),
    sa.Column("state", sa.String(16), nullable=False),
    sa.Column("outcome", sa.String(24)),
    sa.Column("required", sa.Boolean(), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("attempt_count", sa.Integer(), nullable=False),
    sa.Column("next_attempt_at", sa.DateTime(timezone=True)),
    sa.Column("lease_token", sa.Uuid()),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("diagnostic", sa.String(48)),
    sa.Column("candidate_payload", JSONB(none_as_null=True)),
    sa.Column("candidate_hash", sa.String(64)),
    sa.Column("candidate_attempt_id", sa.Uuid()),
    sa.Column("resolved_context_manifest", JSONB(none_as_null=True)),
    sa.Column("resolved_input_hash", sa.String(64)),
    sa.Column("bound_at", sa.DateTime(timezone=True)),
    sa.CheckConstraint("revision>0 AND attempt_count BETWEEN 0 AND 2"),
    sa.CheckConstraint("kind IN ('deterministic','semantic','evaluator','reconcile')"),
    sa.CheckConstraint(
        "state IN ('WAITING','READY','RUNNING','VALIDATING','RETRY_WAIT',"
        "'SUCCEEDED','FAILED','BLOCKED','SKIPPED','CANCELLED')"
    ),
    sa.CheckConstraint(
        "jsonb_array_length(dependencies)<=24 AND octet_length(input_manifest::text)<=90000"
    ),
)
sa.Index("ix_agent_tasks_due", tasks.c.run_id, tasks.c.state, tasks.c.next_attempt_at)
sections = tab(
    "agent_sections",
    sa.Column("run_id", sa.Uuid(), nullable=False),
    sa.Column("task_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id", "task_id"],
        ["agent_tasks.organization_id", "agent_tasks.run_id", "agent_tasks.id"],
    ),
    sa.Column("section_id", sa.String(64), nullable=False),
    sa.Column("logical_section_id", sa.String(64), nullable=False),
    sa.Column("result", JSONB(), nullable=False),
    sa.Column("validation", JSONB(), nullable=False),
    sa.Column("content_sha256", sa.String(64), nullable=False),
    sa.Column("schema_version", sa.String(48), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.UniqueConstraint("task_id", "section_id"),
    sa.CheckConstraint(
        "octet_length(result::text)<=64000 AND octet_length(validation::text)<=64000"
    ),
)
sa.Index("ix_agent_sections_run", sections.c.organization_id, sections.c.run_id)
scopes = sa.Table(
    "ai_provider_scopes",
    Base.metadata,
    sa.Column("id", sa.String(160), primary_key=True),
    sa.Column("provider_id", sa.String(32), nullable=False),
    sa.Column("policy_hash", sa.String(64), nullable=False),
    sa.Column("billing_class", sa.String(24), nullable=False),
    sa.Column("enabled", sa.Boolean(), nullable=False),
    sa.Column("allowed_tenants", JSONB(), nullable=False),
    sa.Column("allowed_models", JSONB(), nullable=False),
    sa.Column("concurrency_slots", sa.Integer(), nullable=False),
    sa.Column("requests_per_minute", sa.Integer(), nullable=False),
    sa.Column("requests_per_day", sa.Integer(), nullable=False),
    sa.Column("tenant_requests_per_day", sa.Integer(), nullable=False),
    sa.Column("tokens_per_minute", sa.Integer(), nullable=False),
    sa.Column("circuit_until", sa.DateTime(timezone=True)),
    sa.Column("failure_count", sa.Integer(), nullable=False),
    sa.Column("disabled_reason", sa.String(48)),
    sa.Column("quarantined_attempt_id", sa.Uuid()),
    sa.Column("quarantine_reason", sa.String(48)),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.CheckConstraint(
        "concurrency_slots BETWEEN 1 AND 4 AND requests_per_minute>0 "
        "AND requests_per_day>0 AND tokens_per_minute>0 AND revision>0"
    ),
)
quotas = sa.Table(
    "ai_quota_reservations",
    Base.metadata,
    sa.Column("attempt_id", sa.Uuid(), primary_key=True),
    sa.Column("organization_id", sa.Uuid(), nullable=False),
    sa.Column("run_id", sa.Uuid(), nullable=False),
    sa.Column("task_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id", "task_id"],
        ["agent_tasks.organization_id", "agent_tasks.run_id", "agent_tasks.id"],
    ),
    sa.Column(
        "quota_scope_id", sa.String(160), sa.ForeignKey("ai_provider_scopes.id"), nullable=False
    ),
    sa.Column("admitted_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("window_expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("slot_expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("request_count", sa.Integer(), nullable=False),
    sa.Column("reserved_input", sa.Integer(), nullable=False),
    sa.Column("reserved_output", sa.Integer(), nullable=False),
    sa.Column("reported_input", sa.Integer()),
    sa.Column("reported_output", sa.Integer()),
    sa.Column("outcome", sa.String(16), nullable=False),
    sa.Index("ix_model_quota_time", "quota_scope_id", "admitted_at"),
    sa.Index("ix_model_quota_slots", "quota_scope_id", "slot_expires_at"),
)
TABLES = (tasks, sections, scopes, quotas)
