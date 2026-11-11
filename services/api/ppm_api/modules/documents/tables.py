"""Reusable source versions; indexes and processing are derived from immutable bytes."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.database import Base


def tab(name: str, *columns: sa.Column | sa.Constraint) -> sa.Table:
    return sa.Table(
        name,
        Base.metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.UniqueConstraint("organization_id", "id"),
        *columns,
    )


documents = tab(
    "source_documents",
    sa.Column("project_id", sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.Column("title", sa.String(160), nullable=False),
    sa.Column("category", sa.String(24), nullable=False),
    sa.CheckConstraint(
        "category IN ('SRS','BRD','PRD','MOM','sprint_report','risk_log','charter','policy')"
    ),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("deleted_at", sa.DateTime(timezone=True)),
    sa.Column("legal_hold", sa.Boolean(), nullable=False),
    sa.Column("retain_until", sa.DateTime(timezone=True), nullable=False),
    sa.Column("policy", JSONB(), nullable=True),
)
versions = tab(
    "source_versions",
    sa.Column("document_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "document_id"],
        ["source_documents.organization_id", "source_documents.id"],
    ),
    sa.Column("number", sa.Integer(), nullable=False),
    sa.UniqueConstraint("document_id", "number"),
    sa.Column("sha256", sa.String(64), nullable=False),
    sa.UniqueConstraint("document_id", "sha256"),
    sa.Column("filename", sa.String(160), nullable=False),
    sa.Column("size", sa.Integer(), nullable=False),
    sa.Column("object_key", sa.String(300), nullable=False),
    sa.Column("uploaded_by", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "uploaded_by"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("status", sa.String(24), nullable=False),
    sa.CheckConstraint(
        "status IN ('queued','processing','ready','quarantined','failed','cancelled','purged')"
    ),
    sa.Column("diagnostic", sa.String(48)),
    sa.Column("scanner", sa.String(48)),
    sa.Column("parser_version", sa.String(48), nullable=False),
)
chunks = tab(
    "source_chunks",
    sa.Column("version_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "version_id"], ["source_versions.organization_id", "source_versions.id"]
    ),
    sa.Column("ordinal", sa.Integer(), nullable=False),
    sa.UniqueConstraint("version_id", "ordinal"),
    sa.Column("location", sa.String(200), nullable=False),
    sa.Column("text", sa.Text(), nullable=False),
    sa.Column("confidence", sa.Float()),
    sa.Column("method", sa.String(24), nullable=False),
)
links = tab(
    "source_evidence_links",
    sa.Column("version_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "version_id"], ["source_versions.organization_id", "source_versions.id"]
    ),
    sa.Column("attachment_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "attachment_id"],
        ["ppm_evidence_attachments.organization_id", "ppm_evidence_attachments.id"],
    ),
    sa.UniqueConstraint("version_id", "attachment_id"),
)
TABLES = (documents, versions, chunks, links)
