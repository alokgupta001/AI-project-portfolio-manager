"""Append-only analysis provenance and human decisions, separate from assessment scores."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.document_tables import tab

analyses = tab(
    "agent_analyses",
    sa.Column("run_id", sa.Uuid(), nullable=False, unique=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id"], ["ai_runs.organization_id", "ai_runs.id"]
    ),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.Column("assessment_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "assessment_id"],
        ["ppm_assessments.organization_id", "ppm_assessments.id"],
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("snapshot", JSONB(), nullable=False),
    sa.Column("output", JSONB(none_as_null=True)),
)
reviews = tab(
    "agent_reviews",
    sa.Column("analysis_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "analysis_id"], ["agent_analyses.organization_id", "agent_analyses.id"]
    ),
    sa.Column("item_key", sa.String(96), nullable=False),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("decision", sa.String(16), nullable=False),
    sa.CheckConstraint("decision IN ('accepted','rejected')"),
    sa.Column("reason", sa.String(1000), nullable=False),
    sa.Column("approved_score", sa.Numeric(7, 4)),
    sa.CheckConstraint("approved_score IS NULL OR approved_score BETWEEN 0 AND 100"),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.CheckConstraint("revision > 0"),
    sa.UniqueConstraint("analysis_id", "item_key", "revision"),
    sa.Column("key", sa.Uuid(), nullable=False),
    sa.UniqueConstraint("organization_id", "actor_id", "key"),
    sa.Column("fingerprint", sa.String(64), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
)
TABLES = (analyses, reviews)
