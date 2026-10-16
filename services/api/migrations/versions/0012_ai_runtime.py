# ruff: noqa: E501
"""Tenant budget ledger, immutable run provenance and rebuildable embedding projection."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0012_ai_runtime"
down_revision = "0011_document_sources"
branch_labels = None
depends_on = None
metadata = sa.MetaData()


def tab(name, *columns):
    return sa.Table(
        name,
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.UniqueConstraint("organization_id", "id"),
        *columns,
    )


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

OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"
ADMIN = "current_setting('ppm.role',true)='Admin'"


def upgrade():
    metadata.reflect(
        op.get_bind(),
        only=["organizations", "memberships", "identity_sessions", "ppm_projects", "source_chunks"],
    )
    metadata.create_all(op.get_bind(), tables=list(TABLES))
    reads = {
        "ai_budgets": ADMIN,
        "ai_runs": f"({ADMIN} OR actor_id={UID}) AND EXISTS (SELECT 1 FROM ppm_projects p WHERE p.id=project_id AND NOT p.archived)",
        "ai_calls": ADMIN,
        "ai_embeddings": "EXISTS (SELECT 1 FROM source_chunks c JOIN source_versions v ON v.id=c.version_id JOIN source_documents d ON d.id=v.document_id WHERE c.id=chunk_id AND v.sha256=source_sha256 AND v.status='ready' AND d.deleted_at IS NULL AND v.number=(SELECT max(n.number) FROM source_versions n WHERE n.document_id=d.id))",
    }
    for table in TABLES:
        name = table.name
        op.execute(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY ai_read ON {name} FOR SELECT TO ppm_app USING (organization_id={OID} AND ({reads[name]}))"
        )
        for command in ("INSERT", "UPDATE"):
            clause = f"organization_id={OID} AND ({ADMIN})"
            rule = (
                f"WITH CHECK ({clause})"
                if command == "INSERT"
                else f"USING ({clause}) WITH CHECK ({clause})"
            )
            op.execute(
                f"CREATE POLICY ai_{command.lower()} ON {name} FOR {command} TO ppm_app {rule}"
            )
        op.execute(f"GRANT SELECT,INSERT,UPDATE ON {name} TO ppm_app")
    op.execute(
        f"CREATE POLICY ai_delete ON ai_embeddings FOR DELETE TO ppm_app USING (organization_id={OID} AND ({ADMIN}))"
    )
    op.execute("GRANT DELETE ON ai_embeddings TO ppm_app")
    op.add_column("durable_jobs", sa.Column("ai_run_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_job_ai_run",
        "durable_jobs",
        "ai_runs",
        ["organization_id", "ai_run_id"],
        ["organization_id", "id"],
    )
    op.drop_constraint("ck_job_source_kind", "durable_jobs")
    op.create_check_constraint(
        "ck_job_source_kind",
        "durable_jobs",
        "num_nonnulls(integration_id,document_version_id,ai_run_id)=1",
    )
    for command in ("SELECT", "INSERT", "UPDATE"):
        clause = f"organization_id={OID} AND ai_run_id IS NOT NULL AND EXISTS (SELECT 1 FROM ai_runs r WHERE r.id=ai_run_id)"
        if command != "SELECT":
            clause += f" AND ({ADMIN})"
        rule = f"WITH CHECK ({clause})" if command == "INSERT" else f"USING ({clause})"
        if command == "UPDATE":
            rule += f" WITH CHECK ({clause})"
        op.execute(
            f"CREATE POLICY ai_{command.lower()} ON durable_jobs FOR {command} TO ppm_app {rule}"
        )
    # Existing event SELECT policy already resolves the now-visible durable job.
    for name in ("job_events", "job_outbox"):
        for command in ("INSERT", "UPDATE"):
            clause = f"organization_id={OID} AND ({ADMIN}) AND EXISTS (SELECT 1 FROM durable_jobs j WHERE j.id=job_id AND j.ai_run_id IS NOT NULL)"
            rule = (
                f"WITH CHECK ({clause})"
                if command == "INSERT"
                else f"USING ({clause}) WITH CHECK ({clause})"
            )
            op.execute(
                f"CREATE POLICY ai_{command.lower()} ON {name} FOR {command} TO ppm_app {rule}"
            )
    op.execute("""CREATE FUNCTION public.ppm_ai_job(target uuid, tenant uuid, actor uuid)
        RETURNS TABLE(session_id uuid, run_id uuid, authorized boolean)
        LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
        DECLARE j public.durable_jobs%ROWTYPE; r public.ai_runs%ROWTYPE; ok boolean;
        BEGIN
          SELECT * INTO j FROM public.durable_jobs WHERE id=target AND organization_id=tenant
            AND actor_id=actor AND ai_run_id IS NOT NULL;
          IF NOT FOUND THEN RETURN; END IF;
          PERFORM pg_advisory_xact_lock(hashtextextended(tenant::text,2));
          SELECT * INTO j FROM public.durable_jobs WHERE id=target AND organization_id=tenant AND actor_id=actor FOR UPDATE;
          SELECT * INTO r FROM public.ai_runs WHERE id=j.ai_run_id AND organization_id=tenant;
          SELECT EXISTS (SELECT 1 FROM public.identity_sessions s
            JOIN public.identity_users u ON u.id=s.user_id
            JOIN public.memberships m ON m.user_id=u.id AND m.organization_id=tenant
            JOIN public.ppm_projects p ON p.id=r.project_id AND p.organization_id=tenant
            WHERE s.id=j.session_id AND s.user_id=actor AND s.organization_id=tenant
              AND NOT s.revoked AND s.expires_at>now() AND u.active AND u.verified
              AND m.active AND m.role='Admin' AND NOT p.archived) INTO ok;
          IF (NOT ok OR j.cancel_requested OR r.deadline<now()) AND NOT r.settled THEN
            UPDATE public.ai_budgets SET reserved_usd=reserved_usd-r.reservation,spent_usd=spent_usd+r.charged_usd WHERE organization_id=tenant;
            UPDATE public.ai_runs SET settled=true,diagnostic=CASE WHEN NOT ok THEN 'AUTHORITY_REVOKED' WHEN j.cancel_requested THEN 'CANCELLED' ELSE 'DEADLINE_EXCEEDED' END WHERE id=r.id;
            UPDATE public.durable_jobs SET status=CASE WHEN r.deadline<now() THEN 'failed' ELSE 'cancelled' END,lease_until=NULL,updated_at=now() WHERE id=j.id;
          END IF;
          RETURN QUERY SELECT j.session_id,j.ai_run_id,ok;
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_ai_job(uuid,uuid,uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_ai_job(uuid,uuid,uuid) TO ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_ai_invalidate() RETURNS trigger
        LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$ BEGIN
          IF TG_TABLE_NAME='source_versions' THEN
            DELETE FROM public.ai_embeddings e USING public.source_chunks c,public.source_versions v
              WHERE e.chunk_id=c.id AND c.version_id=v.id AND v.document_id=NEW.document_id;
          ELSIF NEW.deleted_at IS NOT NULL THEN
            DELETE FROM public.ai_embeddings e USING public.source_chunks c,public.source_versions v
              WHERE e.chunk_id=c.id AND c.version_id=v.id AND v.document_id=NEW.id;
          END IF;
          RETURN NEW;
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_ai_invalidate() FROM PUBLIC")
    op.execute(
        "CREATE TRIGGER ai_source_version AFTER INSERT ON source_versions FOR EACH ROW EXECUTE FUNCTION public.ppm_ai_invalidate()"
    )
    op.execute(
        "CREATE TRIGGER ai_source_deleted AFTER UPDATE OF deleted_at ON source_documents FOR EACH ROW EXECUTE FUNCTION public.ppm_ai_invalidate()"
    )
    op.execute("""CREATE FUNCTION public.ppm_ai_snapshot_immutable() RETURNS trigger LANGUAGE plpgsql SET search_path=pg_catalog,public AS $$ BEGIN
        IF (NEW.organization_id,NEW.project_id,NEW.actor_id,NEW.session_id,NEW.snapshot,NEW.input_sha256,NEW.versions,NEW.reservation,NEW.deadline,NEW.created_at)
        IS DISTINCT FROM (OLD.organization_id,OLD.project_id,OLD.actor_id,OLD.session_id,OLD.snapshot,OLD.input_sha256,OLD.versions,OLD.reservation,OLD.deadline,OLD.created_at)
        THEN RAISE check_violation USING MESSAGE='AI provenance is immutable'; END IF;
        RETURN NEW; END $$""")
    op.execute(
        "CREATE TRIGGER ai_snapshot_immutable BEFORE UPDATE ON ai_runs FOR EACH ROW EXECUTE FUNCTION public.ppm_ai_snapshot_immutable()"
    )


def downgrade():
    # Only guarded disposable runners may exercise this destructive lifecycle.
    op.execute("DROP TRIGGER ai_snapshot_immutable ON ai_runs")
    op.execute("DROP FUNCTION public.ppm_ai_snapshot_immutable()")
    op.execute("DROP TRIGGER ai_source_version ON source_versions")
    op.execute("DROP TRIGGER ai_source_deleted ON source_documents")
    op.execute("DROP FUNCTION public.ppm_ai_invalidate()")
    op.execute("DROP FUNCTION public.ppm_ai_job(uuid,uuid,uuid)")
    for name in ("durable_jobs", "job_events", "job_outbox"):
        for command in (
            ("select", "insert", "update") if name == "durable_jobs" else ("insert", "update")
        ):
            op.execute(f"DROP POLICY ai_{command} ON {name}")
    for name in ("job_events", "job_outbox"):
        op.execute(
            f"DELETE FROM {name} WHERE job_id IN (SELECT id FROM durable_jobs WHERE ai_run_id IS NOT NULL)"
        )
    op.execute("DELETE FROM durable_jobs WHERE ai_run_id IS NOT NULL")
    op.drop_constraint("ck_job_source_kind", "durable_jobs")
    op.drop_constraint("fk_job_ai_run", "durable_jobs")
    op.drop_column("durable_jobs", "ai_run_id")
    op.create_check_constraint(
        "ck_job_source_kind",
        "durable_jobs",
        "(integration_id IS NULL) <> (document_version_id IS NULL)",
    )
    for table in reversed(TABLES):
        table.drop(op.get_bind())
