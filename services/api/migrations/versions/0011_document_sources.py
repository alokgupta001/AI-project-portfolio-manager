# ruff: noqa: E501
"""Reusable source versions; indexes and processing are derived from immutable bytes."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0011_document_sources"
down_revision = "0010_account_authority"
branch_labels = None
depends_on = None
metadata = sa.MetaData()


def tab(name: str, *columns: sa.Column | sa.Constraint) -> sa.Table:
    return sa.Table(
        name,
        metadata,
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

OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"
ADMIN = "current_setting('ppm.role',true)='Admin'"
EDIT = f"""({ADMIN} OR (current_setting('ppm.role',true)='Project Manager' AND
    project_id IS NOT NULL AND EXISTS (SELECT 1 FROM ppm_grants g
    WHERE g.project_id=source_documents.project_id AND g.user_id={UID}
    AND g.organization_id={OID} AND g.access IN ('edit','manage') AND NOT g.archived)))"""


def upgrade() -> None:
    metadata.reflect(
        op.get_bind(),
        only=["organizations", "memberships", "ppm_projects", "ppm_evidence_attachments"],
    )
    metadata.create_all(op.get_bind(), tables=list(TABLES))
    reads = {
        "source_documents": f"({ADMIN} OR deleted_at IS NULL) AND ((project_id IS NULL AND category='policy') OR EXISTS (SELECT 1 FROM ppm_projects p WHERE p.id=project_id AND p.organization_id={OID} AND NOT p.archived))",
        "source_versions": "EXISTS (SELECT 1 FROM source_documents d WHERE d.id=document_id)",
        "source_chunks": "EXISTS (SELECT 1 FROM source_versions v JOIN source_documents d ON d.id=v.document_id WHERE v.id=version_id AND v.status='ready' AND d.deleted_at IS NULL)",
        "source_evidence_links": "EXISTS (SELECT 1 FROM source_versions v WHERE v.id=version_id) AND EXISTS (SELECT 1 FROM ppm_evidence_attachments e WHERE e.id=attachment_id)",
    }
    writes = {
        "source_documents": EDIT,
        "source_versions": f"EXISTS (SELECT 1 FROM source_documents WHERE id=document_id AND ({EDIT}))",
        "source_chunks": f"EXISTS (SELECT 1 FROM source_versions v JOIN source_documents ON source_documents.id=v.document_id WHERE v.id=version_id AND ({EDIT}))",
        "source_evidence_links": f"EXISTS (SELECT 1 FROM source_versions v JOIN source_documents ON source_documents.id=v.document_id WHERE v.id=version_id AND ({EDIT})) AND EXISTS (SELECT 1 FROM ppm_evidence_attachments e WHERE e.id=attachment_id)",
    }
    for table in TABLES:
        name = table.name
        op.execute(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY")
        for command, clause in [
            ("SELECT", reads[name]),
            ("INSERT", writes[name]),
            ("UPDATE", writes[name]),
            ("DELETE", writes[name]),
        ]:
            if command == "DELETE" and name in {"source_documents", "source_versions"}:
                continue
            scoped = f"organization_id={OID} AND ({clause})"
            rule = f"WITH CHECK ({scoped})" if command == "INSERT" else f"USING ({scoped})"
            if command == "UPDATE":
                rule += f" WITH CHECK ({scoped})"
            op.execute(
                f"CREATE POLICY source_{command.lower()} ON {name} FOR {command} TO ppm_app {rule}"
            )
        privileges = (
            "SELECT,INSERT,UPDATE"
            if name in {"source_documents", "source_versions"}
            else "SELECT,INSERT,UPDATE,DELETE"
        )
        op.execute(f"GRANT {privileges} ON {name} TO ppm_app")
    op.add_column("durable_jobs", sa.Column("document_version_id", sa.Uuid()))
    op.alter_column("durable_jobs", "integration_id", nullable=True)
    op.create_foreign_key(
        "fk_job_document_version",
        "durable_jobs",
        "source_versions",
        ["organization_id", "document_version_id"],
        ["organization_id", "id"],
    )
    op.create_check_constraint(
        "ck_job_source_kind",
        "durable_jobs",
        "(integration_id IS NULL) <> (document_version_id IS NULL)",
    )
    # Preserve the exact prior integration authority implementation behind a kind guard.
    # A mismatched broker tuple must never send a document job through connector cancellation.
    op.execute(
        "ALTER FUNCTION public.ppm_cancel_unauthorized_job(uuid) RENAME TO ppm_cancel_unauthorized_integration_job"
    )
    op.execute(
        "REVOKE ALL ON FUNCTION public.ppm_cancel_unauthorized_integration_job(uuid) FROM ppm_app"
    )
    op.execute("""CREATE FUNCTION public.ppm_cancel_unauthorized_job(target uuid) RETURNS boolean
        LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
        SELECT CASE WHEN EXISTS (SELECT 1 FROM public.durable_jobs j
          WHERE j.id=target AND j.integration_id IS NOT NULL)
        THEN public.ppm_cancel_unauthorized_integration_job(target) ELSE false END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) TO ppm_app")
    # Existing integration policies remain intact. Add an independent branch for document jobs.
    visible = "EXISTS (SELECT 1 FROM source_versions v WHERE v.id=document_version_id)"
    writable = f"EXISTS (SELECT 1 FROM source_versions v JOIN source_documents ON source_documents.id=v.document_id WHERE v.id=document_version_id AND ({EDIT}))"
    for command in ("SELECT", "INSERT", "UPDATE"):
        expression = f"organization_id={OID} AND document_version_id IS NOT NULL AND ({ADMIN} OR actor_id={UID}) AND ({visible if command == 'SELECT' else writable})"
        rule = f"WITH CHECK ({expression})" if command == "INSERT" else f"USING ({expression})"
        if command == "UPDATE":
            rule += f" WITH CHECK ({expression})"
        op.execute(
            f"CREATE POLICY document_{command.lower()} ON durable_jobs FOR {command} TO ppm_app {rule}"
        )
    for name in ("job_events", "job_outbox"):
        expression = f"organization_id={OID} AND EXISTS (SELECT 1 FROM durable_jobs j WHERE j.id=job_id AND j.document_version_id IS NOT NULL AND ({ADMIN} OR j.actor_id={UID}))"
        for command in ("INSERT", "UPDATE"):
            rule = (
                f"WITH CHECK ({expression})"
                if command == "INSERT"
                else f"USING ({expression}) WITH CHECK ({expression})"
            )
            op.execute(
                f"CREATE POLICY document_{command.lower()} ON {name} FOR {command} TO ppm_app {rule}"
            )
    op.execute("""CREATE FUNCTION public.ppm_document_job(target uuid, tenant uuid, actor uuid)
        RETURNS TABLE(session_id uuid, version_id uuid, authorized boolean)
        LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
        DECLARE j public.durable_jobs%ROWTYPE; ok boolean;
        BEGIN
          SELECT * INTO j FROM public.durable_jobs WHERE id=target AND organization_id=tenant
            AND actor_id=actor AND document_version_id IS NOT NULL;
          IF NOT FOUND THEN RETURN; END IF;
          PERFORM pg_advisory_xact_lock(hashtextextended(tenant::text,2));
          SELECT * INTO j FROM public.durable_jobs WHERE id=target AND organization_id=tenant
            AND actor_id=actor AND document_version_id IS NOT NULL FOR UPDATE;
          IF NOT FOUND THEN RETURN; END IF;
          SELECT EXISTS (SELECT 1 FROM public.identity_sessions s
            JOIN public.identity_users u ON u.id=s.user_id
            JOIN public.memberships m ON m.user_id=u.id AND m.organization_id=tenant
            JOIN public.source_versions v ON v.id=j.document_version_id
            JOIN public.source_documents d ON d.id=v.document_id
            LEFT JOIN public.ppm_projects p ON p.id=d.project_id AND p.organization_id=tenant
            WHERE s.id=j.session_id AND s.user_id=actor AND s.organization_id=tenant
              AND NOT s.revoked AND s.expires_at>now() AND u.active AND u.verified AND m.active
              AND d.deleted_at IS NULL AND (d.project_id IS NULL OR NOT p.archived)
              AND (m.role='Admin' OR (m.role='Project Manager' AND EXISTS
                (SELECT 1 FROM public.ppm_grants g WHERE g.organization_id=tenant
                 AND g.user_id=actor AND g.project_id=d.project_id AND NOT g.archived
                 AND g.access IN ('edit','manage'))))) INTO ok;
          IF NOT ok AND j.status NOT IN ('succeeded','partially_succeeded','failed','cancelled') THEN
            UPDATE public.durable_jobs SET status='cancelled',lease_until=NULL,updated_at=now(),
              errors='[{"code":"AUTHORITY_REVOKED"}]'::jsonb WHERE id=j.id;
            UPDATE public.source_versions SET status='cancelled',diagnostic='AUTHORITY_REVOKED'
              WHERE id=j.document_version_id AND status IN ('queued','processing');
          END IF;
          RETURN QUERY SELECT j.session_id,j.document_version_id,ok;
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_document_job(uuid,uuid,uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_document_job(uuid,uuid,uuid) TO ppm_app")
    op.execute(f"""CREATE FUNCTION public.ppm_source_retention_refs()
        RETURNS TABLE(object_key text, document_id uuid, legal_hold boolean)
        LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
        BEGIN
          IF NOT EXISTS (SELECT 1 FROM public.memberships m JOIN public.identity_users u ON u.id=m.user_id
            WHERE m.organization_id={OID} AND m.user_id={UID} AND m.active AND m.role='Admin'
              AND u.active AND u.verified) THEN RAISE insufficient_privilege; END IF;
          RETURN QUERY SELECT v.object_key::text,d.id,d.legal_hold FROM public.source_documents d
            LEFT JOIN public.source_versions v ON v.document_id=d.id AND v.organization_id=d.organization_id
            WHERE d.organization_id={OID};
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_source_retention_refs() FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_source_retention_refs() TO ppm_app")
    op.execute(f"""CREATE FUNCTION public.ppm_purge_document(target uuid) RETURNS void
        LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
        DECLARE tenant uuid := {OID}; actor uuid := {UID};
        BEGIN
          PERFORM pg_advisory_xact_lock(hashtextextended(tenant::text,2));
          IF NOT EXISTS (SELECT 1 FROM public.memberships m JOIN public.identity_users u ON u.id=m.user_id
              WHERE m.organization_id=tenant AND m.user_id=actor AND m.active AND m.role='Admin'
                AND u.active AND u.verified) THEN RAISE insufficient_privilege; END IF;
          IF NOT EXISTS (SELECT 1 FROM public.source_documents d WHERE d.id=target
              AND d.organization_id=tenant AND d.deleted_at IS NOT NULL
              AND NOT d.legal_hold AND d.retain_until<=now()) THEN RAISE insufficient_privilege; END IF;
          DELETE FROM public.source_chunks WHERE version_id IN
            (SELECT id FROM public.source_versions WHERE document_id=target AND organization_id=tenant);
          DELETE FROM public.source_evidence_links WHERE version_id IN
            (SELECT id FROM public.source_versions WHERE document_id=target AND organization_id=tenant);
          UPDATE public.source_versions SET status='purged',diagnostic=NULL WHERE document_id=target AND organization_id=tenant;
          UPDATE public.durable_jobs SET status='cancelled',cancel_requested=true,lease_until=NULL
            WHERE organization_id=tenant AND document_version_id IN
            (SELECT id FROM public.source_versions WHERE document_id=target AND organization_id=tenant)
            AND status IN ('queued','running','retry_wait');
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_purge_document(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_purge_document(uuid) TO ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_source_immutable() RETURNS trigger
        LANGUAGE plpgsql SET search_path=pg_catalog,public AS $$ BEGIN
          IF (to_jsonb(NEW)-'status'-'diagnostic'-'scanner'-'parser_version') IS DISTINCT FROM
             (to_jsonb(OLD)-'status'-'diagnostic'-'scanner'-'parser_version') THEN
            RAISE check_violation USING MESSAGE='Source version identity is immutable';
          END IF;
          RETURN NEW;
        END $$""")
    op.execute(
        "CREATE TRIGGER source_version_immutable BEFORE UPDATE ON source_versions FOR EACH ROW EXECUTE FUNCTION public.ppm_source_immutable()"
    )


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS public.ppm_source_retention_refs()")
    op.execute("DROP FUNCTION public.ppm_cancel_unauthorized_job(uuid)")
    op.execute(
        "ALTER FUNCTION public.ppm_cancel_unauthorized_integration_job(uuid) RENAME TO ppm_cancel_unauthorized_job"
    )
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) TO ppm_app")
    op.execute("DROP TRIGGER source_version_immutable ON source_versions")
    op.execute("DROP FUNCTION public.ppm_source_immutable()")
    op.execute("DROP FUNCTION public.ppm_purge_document(uuid)")
    op.execute("DROP FUNCTION public.ppm_document_job(uuid,uuid,uuid)")
    for name in ("durable_jobs", "job_events", "job_outbox"):
        for command in (
            ("select", "insert", "update") if name == "durable_jobs" else ("insert", "update")
        ):
            op.execute(f"DROP POLICY document_{command} ON {name}")
    # Disposable test downgrade only: document jobs have no pre-0011 representation.
    op.execute(
        "DELETE FROM job_events WHERE job_id IN (SELECT id FROM durable_jobs WHERE document_version_id IS NOT NULL)"
    )
    op.execute(
        "DELETE FROM job_outbox WHERE job_id IN (SELECT id FROM durable_jobs WHERE document_version_id IS NOT NULL)"
    )
    op.execute("DELETE FROM durable_jobs WHERE document_version_id IS NOT NULL")
    op.drop_constraint("ck_job_source_kind", "durable_jobs")
    op.drop_constraint("fk_job_document_version", "durable_jobs")
    op.drop_column("durable_jobs", "document_version_id")
    op.alter_column("durable_jobs", "integration_id", nullable=False)
    for table in reversed(TABLES):
        table.drop(op.get_bind())
