"""Tenant budget ledger, immutable run provenance and rebuildable embedding projection."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.document_tables import tab

budgets = tab(
    "ai_budgets",
    sa.UniqueConstraint("organization_id"),
    sa.Column("limit_usd", sa.Numeric(12, 6), nullable=False),
    sa.Column("spent_usd", sa.Numeric(12, 6), nullable=False),
    sa.Column("reserved_usd", sa.Numeric(12, 6), nullable=False),
    sa.Column("concurrency", sa.Integer(), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("failures", sa.Integer(), nullable=False),
    sa.Column("circuit_until", sa.DateTime(timezone=True)),
    sa.CheckConstraint("limit_usd>=0 AND spent_usd>=0 AND reserved_usd>=0"),
    sa.CheckConstraint("concurrency BETWEEN 1 AND 4"),
)
runs = tab(
    "ai_runs",
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("session_id", sa.Uuid(), sa.ForeignKey("identity_sessions.id"), nullable=False),
    sa.Column("snapshot", JSONB(), nullable=False),
    sa.Column("input_sha256", sa.String(64), nullable=False),
    sa.Column("versions", JSONB(), nullable=False),
    sa.Column("evidence", JSONB(), nullable=False),
    sa.Column("result", JSONB(), nullable=False),
    sa.Column("diagnostic", sa.String(48)),
    sa.Column("limitations", JSONB(), nullable=False),
    sa.Column("retrieval", sa.String(16), nullable=False),
    sa.Column("reservation", sa.Numeric(12, 6), nullable=False),
    sa.Column("charged_usd", sa.Numeric(12, 6), nullable=False),
    sa.Column("settled", sa.Boolean(), nullable=False),
    sa.Column("deadline", sa.DateTime(timezone=True), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("reservation>=0 AND charged_usd>=0 AND charged_usd<=reservation"),
)
calls = tab(
    "ai_calls",
    sa.Column("run_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id"], ["ai_runs.organization_id", "ai_runs.id"]
    ),
    sa.Column("operation", sa.String(24), nullable=False),
    sa.Column("attempt", sa.Integer(), nullable=False),
    sa.UniqueConstraint("run_id", "operation", "attempt"),
    sa.Column("status", sa.String(16), nullable=False),
    sa.Column("code", sa.String(48)),
    sa.Column("charged_usd", sa.Numeric(12, 6), nullable=False),
    sa.Column("input_tokens", sa.Integer()),
    sa.Column("output_tokens", sa.Integer()),
    sa.Column("latency_ms", sa.Integer(), nullable=False),
)
embeddings = tab(
    "ai_embeddings",
    sa.Column("chunk_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "chunk_id"],
        ["source_chunks.organization_id", "source_chunks.id"],
        ondelete="CASCADE",
    ),
    sa.UniqueConstraint("chunk_id"),
    sa.Column("source_sha256", sa.String(64), nullable=False),
    sa.Column("text_sha256", sa.String(64), nullable=False),
    sa.Column("model", sa.String(160), nullable=False),
    sa.Column("chunk_version", sa.String(48), nullable=False),
    sa.Column("vector", JSONB(), nullable=False),
    sa.Column("run_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id"], ["ai_runs.organization_id", "ai_runs.id"]
    ),
)
TABLES = (budgets, runs, calls, embeddings)
