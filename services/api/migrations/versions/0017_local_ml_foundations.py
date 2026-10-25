# ruff: noqa: E501
"""Tenant scoped connector authority, conflict review and immutable ML lineage."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0017_local_ml_foundations"
down_revision = "0016_guided_project_access"
branch_labels = None
depends_on = None
metadata = sa.MetaData()


def tenant_table(name, *columns):
    return sa.Table(
        name,
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.UniqueConstraint("organization_id", "id"),
        *columns,
    )


principals = tenant_table(
    "connector_principals",
    sa.Column("integration_id", sa.Uuid(), nullable=False, unique=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.id"],
    ),
    sa.Column("active", sa.Boolean(), nullable=False),
    sa.Column("generation", sa.Integer(), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("interval_minutes", sa.Integer(), nullable=False),
    sa.Column("next_due", sa.DateTime(timezone=True), nullable=False),
    sa.Column("approved_by", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "approved_by"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)
conflicts = tenant_table(
    "ingestion_conflicts",
    sa.Column("source_id", sa.Uuid(), nullable=False, unique=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "source_id"],
        ["ingestion_sources.organization_id", "ingestion_sources.id"],
    ),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("status", sa.String(24), nullable=False),
    sa.Column("candidate", JSONB(), nullable=False),
    sa.Column("local", JSONB(), nullable=False),
    sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("source_observed_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("fingerprint", sa.String(64), nullable=False),
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
)


def project_table(name: str, *columns: sa.Column | sa.Constraint) -> sa.Table:
    """All lineage stays within its owning project and tenant."""
    return tenant_table(
        name,
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
        ),
        sa.UniqueConstraint("organization_id", "project_id", "id"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        *columns,
    )


histories = project_table(
    "ml_histories",
    sa.Column("name", sa.String(160), nullable=False),
    sa.Column("version", sa.Integer(), nullable=False),
    sa.UniqueConstraint("organization_id", "project_id", "name", "version"),
    sa.Column("digest", sa.String(64), nullable=False),
    sa.Column("manifest", JSONB(), nullable=False),
    sa.Column("records", JSONB(), nullable=False),
    sa.Column("withdrawn", sa.Boolean(), nullable=False),
)
datasets = project_table(
    "ml_datasets",
    sa.Column("history_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "history_id"],
        ["ml_histories.organization_id", "ml_histories.project_id", "ml_histories.id"],
    ),
    sa.Column("digest", sa.String(64), nullable=False),
    sa.Column("manifest", JSONB(), nullable=False),
    sa.Column("records", JSONB(), nullable=False),
)
runs = project_table(
    "ml_runs",
    sa.Column("dataset_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "dataset_id"],
        ["ml_datasets.organization_id", "ml_datasets.project_id", "ml_datasets.id"],
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("status", sa.String(32), nullable=False),
    sa.Column("card", JSONB(), nullable=False),
    sa.Column("artifacts", JSONB(), nullable=False),
)
TABLES = (principals, conflicts, histories, datasets, runs)

OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
CID = "NULLIF(current_setting('ppm.connector_id',true),'')::uuid"
ADMIN = "current_setting('ppm.role',true)='Admin'"


def upgrade():
    metadata.reflect(
        op.get_bind(),
        only=[
            "organizations",
            "memberships",
            "job_integrations",
            "ingestion_sources",
            "durable_jobs",
            "ppm_projects",
        ],
    )
    metadata.create_all(op.get_bind(), tables=list(TABLES))
    op.add_column("durable_jobs", sa.Column("ml_run_id", sa.Uuid(), nullable=True))
    op.add_column("durable_jobs", sa.Column("connector_generation", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_job_ml_run",
        "durable_jobs",
        "ml_runs",
        ["organization_id", "ml_run_id"],
        ["organization_id", "id"],
    )
    op.drop_constraint("ck_job_source_kind", "durable_jobs", type_="check")
    op.create_check_constraint(
        "ck_job_source_kind",
        "durable_jobs",
        "num_nonnulls(integration_id,document_version_id,ai_run_id,ml_run_id)=1",
    )
    op.add_column("ingestion_sources", sa.Column("logical_key", sa.String(64), nullable=True))
    op.create_unique_constraint(
        "uq_source_logical", "ingestion_sources", ["organization_id", "project_id", "logical_key"]
    )
    for table in TABLES:
        name = table.name
        op.execute(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY")
        op.execute(f"GRANT SELECT,INSERT ON {name} TO ppm_app")
        op.execute(
            f"CREATE POLICY ml_read ON {name} FOR SELECT TO ppm_app USING (organization_id={OID} AND {ADMIN})"
        )
        op.execute(
            f"CREATE POLICY ml_insert ON {name} FOR INSERT TO ppm_app WITH CHECK (organization_id={OID} AND {ADMIN})"
        )
        if name != "ml_datasets":
            op.execute(f"GRANT UPDATE ON {name} TO ppm_app")
            op.execute(
                f"CREATE POLICY ml_update ON {name} FOR UPDATE TO ppm_app USING (organization_id={OID} AND {ADMIN}) WITH CHECK (organization_id={OID} AND {ADMIN})"
            )
    op.execute(f"""CREATE FUNCTION public.ppm_connector_reference(target uuid)
      RETURNS TABLE(actor_id uuid, session_id uuid, project_id uuid, generation integer)
      LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      SELECT i.actor_id,i.session_id,i.project_id,a.generation FROM public.job_integrations i
      JOIN public.connector_principals a ON a.integration_id=i.id AND a.organization_id=i.organization_id
      JOIN public.ppm_projects p ON p.id=i.project_id AND p.organization_id=i.organization_id
      WHERE i.id=target AND i.organization_id={OID} AND i.enabled AND a.active AND NOT p.archived $$""")
    op.execute(f"""CREATE FUNCTION public.ppm_connector_scope(project uuid) RETURNS boolean
      LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      SELECT current_setting('ppm.role',true)='Connector' AND EXISTS
      (SELECT 1 FROM public.ppm_connector_reference({CID}) r WHERE r.project_id=project) $$""")
    for signature in ("ppm_connector_reference(uuid)", "ppm_connector_scope(uuid)"):
        op.execute(f"REVOKE ALL ON FUNCTION public.{signature} FROM PUBLIC")
        op.execute(f"GRANT EXECUTE ON FUNCTION public.{signature} TO ppm_app")
    scoped = "organization_id=" + OID + " AND public.ppm_connector_scope(project_id)"
    for name, clause, commands in [
        (
            "ppm_projects",
            "organization_id=" + OID + " AND public.ppm_connector_scope(id)",
            ["SELECT"],
        ),
        *[
            (n, scoped, ["SELECT", "INSERT", "UPDATE"])
            for n in ("ppm_work_items", "ppm_sprints", "ingestion_sources", "ingestion_conflicts")
        ],
        ("ppm_sprint_closures", scoped, ["SELECT", "INSERT"]),
        ("job_integrations", f"{scoped} AND id={CID}", ["SELECT", "UPDATE"]),
        (
            "connector_principals",
            f"organization_id={OID} AND integration_id={CID} AND EXISTS (SELECT 1 FROM public.ppm_connector_reference(integration_id))",
            ["SELECT", "UPDATE"],
        ),
        (
            "durable_jobs",
            f"organization_id={OID} AND integration_id={CID} AND EXISTS (SELECT 1 FROM public.ppm_connector_reference(integration_id))",
            ["SELECT", "INSERT", "UPDATE"],
        ),
        *[
            (
                n,
                f"organization_id={OID} AND EXISTS (SELECT 1 FROM durable_jobs j WHERE j.id=job_id AND j.integration_id={CID})",
                ["SELECT", "INSERT", "UPDATE"],
            )
            for n in ("job_events", "job_outbox")
        ],
    ]:
        for command in commands:
            rule = f"WITH CHECK ({clause})" if command == "INSERT" else f"USING ({clause})"
            if command == "UPDATE":
                rule += f" WITH CHECK ({clause})"
            op.execute(
                f"CREATE POLICY connector_{command.lower()} ON {name} FOR {command} TO ppm_app {rule}"
            )
    # ML jobs keep the same Admin/session authority as other user-triggered CPU work.
    op.execute(
        f"CREATE POLICY ml_job_read ON durable_jobs FOR SELECT TO ppm_app USING (organization_id={OID} AND {ADMIN} AND ml_run_id IS NOT NULL)"
    )
    op.execute(
        "ALTER FUNCTION public.ppm_cancel_unauthorized_job(uuid) RENAME TO ppm_pre12_cancel_job"
    )
    op.execute("REVOKE ALL ON FUNCTION public.ppm_pre12_cancel_job(uuid) FROM ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_cancel_unauthorized_job(target uuid) RETURNS boolean
      LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      DECLARE j public.durable_jobs%ROWTYPE; seq integer;
      BEGIN
        SELECT * INTO j FROM public.durable_jobs WHERE id=target;
        IF NOT FOUND OR j.connector_generation IS NULL THEN RETURN public.ppm_pre12_cancel_job(target); END IF;
        PERFORM pg_advisory_xact_lock(hashtextextended(j.organization_id::text,2));
        SELECT * INTO j FROM public.durable_jobs WHERE id=target FOR UPDATE;
        IF j.status IN ('succeeded','partially_succeeded','failed','cancelled') THEN RETURN false; END IF;
        IF EXISTS (SELECT 1 FROM public.connector_principals a
          JOIN public.job_integrations i ON i.id=a.integration_id AND i.organization_id=a.organization_id
          JOIN public.ppm_projects p ON p.id=i.project_id AND p.organization_id=i.organization_id
          WHERE a.organization_id=j.organization_id AND a.integration_id=j.integration_id
            AND a.active AND a.generation=j.connector_generation AND i.enabled AND NOT p.archived)
        THEN RETURN false; END IF;
        seq := j.sequence+1;
        UPDATE public.durable_jobs SET status='cancelled',lease_until=NULL,sequence=seq,updated_at=now(),
          errors=errors || '[{"code":"CONNECTOR_AUTHORITY_REVOKED"}]'::jsonb WHERE id=target;
        INSERT INTO public.job_events(id,organization_id,job_id,sequence,stage,occurred_at)
          VALUES(gen_random_uuid(),j.organization_id,j.id,seq,'access_revoked',now());
        RETURN true;
      END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) TO ppm_app")
    op.execute(f"""CREATE FUNCTION public.ppm_connector_job(target uuid)
      RETURNS TABLE(integration_id uuid, generation integer)
      LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      SELECT j.integration_id,j.connector_generation FROM public.durable_jobs j
      WHERE j.id=target AND j.organization_id={OID}
        AND j.actor_id=NULLIF(current_setting('ppm.user_id',true),'')::uuid
        AND j.connector_generation IS NOT NULL $$""")
    op.execute("""CREATE FUNCTION public.ppm_due_connectors()
      RETURNS TABLE(integration_id uuid, organization_id uuid, actor_id uuid)
      LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      SELECT i.id,i.organization_id,i.actor_id FROM public.job_integrations i
      JOIN public.connector_principals a ON a.integration_id=i.id AND a.organization_id=i.organization_id
      JOIN public.ppm_projects p ON p.id=i.project_id AND p.organization_id=i.organization_id
      WHERE i.enabled AND a.active AND a.interval_minutes>0 AND a.next_due<=now() AND NOT p.archived
        AND i.config->>'mode'='live' AND NOT EXISTS (SELECT 1 FROM public.durable_jobs j
          WHERE j.integration_id=i.id AND j.status IN ('queued','running','retry_wait'))
      ORDER BY a.next_due LIMIT 20 $$""")
    for signature in ("ppm_connector_job(uuid)", "ppm_due_connectors()"):
        op.execute(f"REVOKE ALL ON FUNCTION public.{signature} FROM PUBLIC")
        op.execute(f"GRANT EXECUTE ON FUNCTION public.{signature} TO ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_ml_history_immutable() RETURNS trigger
      LANGUAGE plpgsql AS $$ BEGIN
        IF (to_jsonb(NEW)-'withdrawn') IS DISTINCT FROM (to_jsonb(OLD)-'withdrawn') OR OLD.withdrawn THEN
          RAISE check_violation USING MESSAGE='History versions are immutable; withdrawal is permanent';
        END IF; RETURN NEW; END $$""")
    op.execute(
        "CREATE TRIGGER ml_history_immutable BEFORE UPDATE ON ml_histories FOR EACH ROW EXECUTE FUNCTION public.ppm_ml_history_immutable()"
    )
    op.execute(f"""CREATE FUNCTION public.ppm_ml_job(target uuid)
      RETURNS TABLE(session_id uuid, run_id uuid, authorized boolean)
      LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      DECLARE j public.durable_jobs%ROWTYPE; ok boolean;
      BEGIN
        SELECT * INTO j FROM public.durable_jobs WHERE id=target AND organization_id={OID}
          AND actor_id=NULLIF(current_setting('ppm.user_id',true),'')::uuid AND ml_run_id IS NOT NULL;
        IF NOT FOUND THEN RETURN; END IF;
        PERFORM pg_advisory_xact_lock(hashtextextended(j.organization_id::text,2));
        SELECT EXISTS (SELECT 1 FROM public.identity_sessions s
          JOIN public.memberships m ON m.user_id=s.user_id AND m.organization_id=s.organization_id
          JOIN public.identity_users u ON u.id=s.user_id
          WHERE s.id=j.session_id AND s.user_id=j.actor_id AND s.organization_id=j.organization_id
            AND NOT s.revoked AND s.expires_at>now() AND m.active AND m.role='Admin' AND u.active AND u.verified) INTO ok;
        IF NOT ok AND j.status NOT IN ('succeeded','partially_succeeded','failed','cancelled') THEN
          UPDATE public.durable_jobs SET status='cancelled',updated_at=now(),errors='[{{"code":"AUTHORITY_REVOKED"}}]'::jsonb WHERE id=j.id;
          UPDATE public.ml_runs SET status='blocked',card='{{"eligibility":"authority_revoked","promotion":"BLOCKED"}}'::jsonb WHERE id=j.ml_run_id;
        END IF;
        RETURN QUERY SELECT j.session_id,j.ml_run_id,ok;
      END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_ml_job(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_ml_job(uuid) TO ppm_app")


def downgrade():
    # Disposable lifecycle only; normal data is never downgraded.
    for name in ("job_events", "job_outbox"):
        op.execute(
            f"DELETE FROM {name} WHERE job_id IN (SELECT id FROM durable_jobs WHERE ml_run_id IS NOT NULL)"
        )
    op.execute("DELETE FROM durable_jobs WHERE ml_run_id IS NOT NULL")
    op.execute("DROP FUNCTION public.ppm_ml_job(uuid)")
    op.execute("DROP FUNCTION public.ppm_ml_history_immutable() CASCADE")
    op.execute("DROP FUNCTION public.ppm_due_connectors()")
    op.execute("DROP FUNCTION public.ppm_connector_job(uuid)")
    op.execute("DROP FUNCTION public.ppm_cancel_unauthorized_job(uuid)")
    op.execute(
        "ALTER FUNCTION public.ppm_pre12_cancel_job(uuid) RENAME TO ppm_cancel_unauthorized_job"
    )
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) TO ppm_app")
    op.execute("DROP FUNCTION public.ppm_connector_scope(uuid) CASCADE")
    op.execute("DROP FUNCTION public.ppm_connector_reference(uuid) CASCADE")
    for name in ("durable_jobs", "job_events", "job_outbox"):
        for command in ("select", "insert", "update"):
            op.execute(f"DROP POLICY IF EXISTS connector_{command} ON {name}")
    op.execute("DROP POLICY ml_job_read ON durable_jobs")
    op.drop_constraint("uq_source_logical", "ingestion_sources", type_="unique")
    op.drop_column("ingestion_sources", "logical_key")
    op.drop_constraint("fk_job_ml_run", "durable_jobs", type_="foreignkey")
    op.drop_constraint("ck_job_source_kind", "durable_jobs", type_="check")
    op.create_check_constraint(
        "ck_job_source_kind",
        "durable_jobs",
        "num_nonnulls(integration_id,document_version_id,ai_run_id)=1",
    )
    op.drop_column("durable_jobs", "ml_run_id")
    op.drop_column("durable_jobs", "connector_generation")
    for table in reversed(TABLES):
        op.drop_table(table.name)
