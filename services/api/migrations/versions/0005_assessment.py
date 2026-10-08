# ruff: noqa: E501
"""Frozen Sprint 06 schema, isolated from future runtime metadata changes."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0005_assessment"
down_revision = "0004_capacity"
branch_labels = None
depends_on = None

metadata = sa.MetaData()
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


def ref(name, field):
    return sa.ForeignKeyConstraint(
        ["organization_id", field], ["ppm_" + name + ".organization_id", "ppm_" + name + ".id"]
    )


def member(field):
    return sa.ForeignKeyConstraint(
        ["organization_id", field], ["memberships.organization_id", "memberships.user_id"]
    )


def tab(name, *cols):
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


def revision_column():
    return sa.Column("revision", sa.Integer(), nullable=False)


frameworks = tab(
    "frameworks",
    sa.Column("definition", JSONB(), nullable=False),
    revision_column(),
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
    revision_column(),
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

OID = "nullif(current_setting('ppm.organization_id',true),'')::uuid"
UID = "nullif(current_setting('ppm.user_id',true),'')::uuid"
ROLE = "current_setting('ppm.role',true)"
ADMIN = f"({ROLE}='Admin')"
ELIGIBLE = f"({ROLE} IN ('Admin','Project Manager'))"


def scope(table, evidence=False):
    grant = (
        ""
        if evidence
        else f" OR EXISTS (SELECT 1 FROM ppm_assessment_access g WHERE g.assessment_id={table}.id AND g.user_id={UID} AND g.active)"
    )
    return f"({ADMIN} OR ({ELIGIBLE} AND ({table}.assigned_to={UID} OR {table}.reviewer_id={UID})){grant})"


def upgrade():
    bind = op.get_bind()
    metadata.reflect(
        bind,
        only=["organizations", "memberships", "ppm_departments", "ppm_teams"],
        extend_existing=True,
    )
    metadata.create_all(bind, tables=[metadata.tables["ppm_" + k] for k in KINDS])
    for kind in KINDS:
        table = "ppm_" + kind
        read = "true"
        insert = ADMIN
        update = ADMIN
        delete = None
        if kind == "frameworks":
            update = f"({ADMIN} OR ({ROLE}='Project Manager' AND EXISTS (SELECT 1 FROM ppm_assessment_access g WHERE g.framework_id=ppm_frameworks.id AND g.user_id={UID} AND g.active)))"
        if kind == "framework_versions":
            update = None
        if kind == "assessments":
            read = scope(table)
            update = f"({ELIGIBLE} AND (assigned_to={UID} OR reviewer_id={UID}) AND status <> 'completed')"
        if kind in ("answers", "assessment_events", "evidence_attachments"):
            parent = f"EXISTS (SELECT 1 FROM ppm_assessments a WHERE a.id={table}.assessment_id AND a.organization_id={OID} AND {scope('a', True)})"
            read = parent
            write = f"EXISTS (SELECT 1 FROM ppm_assessments a WHERE a.id={table}.assessment_id AND a.organization_id={OID} AND {ELIGIBLE} AND ((a.assigned_to={UID} AND a.status IN ('draft','returned')) OR (a.reviewer_id={UID} AND a.status IN ('submitted','in_review'))))"
            insert = write
            update = write
            if kind == "assessment_events":
                insert = f"({ELIGIBLE} AND actor_id={UID} AND {parent})"
                update = None
            if kind == "evidence_attachments":
                insert = f"EXISTS (SELECT 1 FROM ppm_assessments a WHERE a.id={table}.assessment_id AND a.assigned_to={UID} AND {ELIGIBLE} AND a.status IN ('draft','returned'))"
                delete = insert
                update = f"EXISTS (SELECT 1 FROM ppm_assessments a WHERE a.id={table}.assessment_id AND a.reviewer_id={UID} AND {ELIGIBLE} AND a.status IN ('submitted','in_review'))"
        if kind == "assessment_access":
            read = f"({ADMIN} OR user_id={UID})"
        if kind == "assessment_requests":
            read = insert = f"({ELIGIBLE} AND user_id={UID})"
            update = None
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY tenant_read ON {table} FOR SELECT TO ppm_app USING (organization_id={OID} AND ({read}))"
        )
        op.execute(
            f"CREATE POLICY tenant_insert ON {table} FOR INSERT TO ppm_app WITH CHECK (organization_id={OID} AND ({insert}))"
        )
        op.execute(f"GRANT SELECT,INSERT ON {table} TO ppm_app")
        if update:
            op.execute(
                f"CREATE POLICY tenant_update ON {table} FOR UPDATE TO ppm_app USING (organization_id={OID} AND ({update})) WITH CHECK (organization_id={OID})"
            )
            op.execute(f"GRANT UPDATE ON {table} TO ppm_app")
        if delete:
            op.execute(
                f"CREATE POLICY tenant_delete ON {table} FOR DELETE TO ppm_app USING (organization_id={OID} AND ({delete}))"
            )
            op.execute(f"GRANT DELETE ON {table} TO ppm_app")


def downgrade():
    inspector = sa.inspect(op.get_bind())
    for kind in KINDS:
        table = "ppm_" + kind
        if inspector.has_table(table):
            for policy in ("tenant_read", "tenant_insert", "tenant_update", "tenant_delete"):
                op.execute(f"DROP POLICY IF EXISTS {policy} ON {table}")
    for kind in (
        "assessment_access",
        "assessment_requests",
        "evidence_attachments",
        "assessment_events",
        "answers",
        "assessments",
        "framework_versions",
        "rubric_levels",
        "questions",
        "dimensions",
        "frameworks",
    ):
        op.execute(f"DROP TABLE IF EXISTS ppm_{kind}")
