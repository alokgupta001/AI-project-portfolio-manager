"""Assessment tables; definitions and results retain immutable version snapshots."""

from __future__ import annotations

from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.database import Base

metadata = Base.metadata
KINDS = (
    "frameworks",
    "framework_versions",
    "assessments",
    "answers",
    "assessment_events",
    "evidence_attachments",
    "assessment_requests",
    "assessment_access",
)


def ref(name: Any, field: Any) -> Any:
    return sa.ForeignKeyConstraint(
        ["organization_id", field], ["ppm_" + name + ".organization_id", "ppm_" + name + ".id"]
    )


def member(field: Any) -> Any:
    return sa.ForeignKeyConstraint(
        ["organization_id", field], ["memberships.organization_id", "memberships.user_id"]
    )


def tab(name: Any, *cols: Any) -> Any:
    return sa.Table(
        "ppm_" + name,
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("organization_id", "id"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.Index("ix_ppm_" + name + "_org", "organization_id"),
        *cols,
    )


def revision() -> Any:
    return sa.Column("revision", sa.Integer(), nullable=False)


frameworks = tab(
    "frameworks",
    sa.Column("definition", JSONB(), nullable=False),
    revision(),
    sa.CheckConstraint("revision > 0"),
)
framework_versions = tab(
    "framework_versions",
    sa.Column("framework_id", sa.Uuid(), nullable=False),
    ref("frameworks", "framework_id"),
    sa.Column("version", sa.Integer(), nullable=False),
    sa.Column("snapshot", JSONB(), nullable=False),
    sa.Column("published_by", sa.Uuid(), nullable=False),
    member("published_by"),
    sa.UniqueConstraint("organization_id", "framework_id", "version"),
    sa.CheckConstraint("version > 0"),
)
assessments = tab(
    "assessments",
    sa.Column("framework_version_id", sa.Uuid(), nullable=False),
    ref("framework_versions", "framework_version_id"),
    sa.Column("name", sa.String(160), nullable=False),
    sa.Column("department_id", sa.Uuid()),
    ref("departments", "department_id"),
    sa.Column("team_id", sa.Uuid()),
    ref("teams", "team_id"),
    sa.Column("assigned_to", sa.Uuid(), nullable=False),
    member("assigned_to"),
    sa.Column("reviewer_id", sa.Uuid(), nullable=False),
    member("reviewer_id"),
    sa.Column("submitted_by", sa.Uuid()),
    member("submitted_by"),
    sa.Column("status", sa.String(20), nullable=False),
    sa.Column("results", JSONB()),
    revision(),
    sa.CheckConstraint("assigned_to <> reviewer_id"),
    sa.CheckConstraint("revision > 0"),
    sa.CheckConstraint("status IN ('draft','submitted','in_review','returned','completed')"),
)
answers = tab(
    "answers",
    sa.Column("assessment_id", sa.Uuid(), nullable=False),
    ref("assessments", "assessment_id"),
    sa.Column("question_id", sa.Uuid(), nullable=False),
    sa.Column("value", sa.Text()),
    sa.Column("evidence_text", sa.Text(), nullable=False),
    sa.Column("reviewer_score", sa.Numeric(7, 4)),
    sa.Column("reviewer_note", sa.Text()),
    sa.UniqueConstraint("organization_id", "assessment_id", "question_id"),
    sa.CheckConstraint("reviewer_score IS NULL OR (reviewer_score >= 0 AND reviewer_score <= 100)"),
)
assessment_events = tab(
    "assessment_events",
    sa.Column("assessment_id", sa.Uuid(), nullable=False),
    ref("assessments", "assessment_id"),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    member("actor_id"),
    sa.Column("event", sa.String(30), nullable=False),
    sa.Column("note", sa.Text(), nullable=False),
    sa.Column("details", JSONB(), nullable=False),
)
evidence_attachments = tab(
    "evidence_attachments",
    sa.Column("assessment_id", sa.Uuid(), nullable=False),
    ref("assessments", "assessment_id"),
    sa.Column("question_id", sa.Uuid(), nullable=False),
    sa.Column("file_name", sa.String(160), nullable=False),
    sa.Column("file_size", sa.Integer(), nullable=False),
    sa.Column("sha256", sa.String(64), nullable=False),
    sa.Column("released", sa.Boolean(), nullable=False),
    sa.Column("storage_path", sa.Text(), nullable=False),
    sa.Column("uploaded_by", sa.Uuid(), nullable=False),
    member("uploaded_by"),
    sa.CheckConstraint("file_size > 0 AND file_size <= 524288"),
)
assessment_requests = tab(
    "assessment_requests",
    sa.Column("user_id", sa.Uuid(), nullable=False),
    member("user_id"),
    sa.Column("key", sa.Uuid(), nullable=False),
    sa.Column("fingerprint", sa.String(64), nullable=False),
    sa.Column("response", JSONB(), nullable=False),
    sa.UniqueConstraint("organization_id", "user_id", "key"),
)
assessment_access = tab(
    "assessment_access",
    sa.Column("user_id", sa.Uuid(), nullable=False),
    member("user_id"),
    sa.Column("framework_id", sa.Uuid()),
    ref("frameworks", "framework_id"),
    sa.Column("assessment_id", sa.Uuid()),
    ref("assessments", "assessment_id"),
    sa.Column("active", sa.Boolean(), nullable=False),
    sa.CheckConstraint("(framework_id IS NULL) <> (assessment_id IS NULL)"),
)
