"""Project-bound pilot protocol and independent label review, separate from training data."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.document_tables import tab

pilots = tab(
    "ai_selection_pilots",
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("binding", JSONB(), nullable=False),
    sa.Column("review", JSONB(none_as_null=True)),
    sa.Column("case_runs", JSONB(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.CheckConstraint("revision > 0 AND octet_length(case_runs::text) <= 2000"),
)
