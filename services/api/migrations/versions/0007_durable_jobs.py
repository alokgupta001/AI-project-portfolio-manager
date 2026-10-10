# ruff: noqa: E501
"""Persistent asynchronous authority. Broker messages contain identifiers only."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0007_durable_jobs"
down_revision = "0006_command_center"
branch_labels = None
depends_on = None
metadata = sa.MetaData()


def tenant_table(name: str, *columns: sa.Column | sa.Constraint) -> sa.Table:
    return sa.Table(
        name,
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.UniqueConstraint("organization_id", "id"),
        *columns,
    )


integrations = tenant_table(
    "job_integrations",
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("session_id", sa.Uuid(), sa.ForeignKey("identity_sessions.id"), nullable=False),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.UniqueConstraint("organization_id", "project_id", "id"),
    sa.Column("config", JSONB(), nullable=False),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.Column("enabled", sa.Boolean(), nullable=False),
    sa.Column("cursor", sa.String(200), nullable=True),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
)
jobs = tenant_table(
    "durable_jobs",
    sa.Column("integration_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.id"],
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("session_id", sa.Uuid(), sa.ForeignKey("identity_sessions.id"), nullable=False),
    sa.Column("key", sa.String(160), nullable=False),
    sa.Column("request_hash", sa.String(64), nullable=False),
    sa.UniqueConstraint("organization_id", "actor_id", "key"),
    sa.Column("config", JSONB(), nullable=False),
    sa.Column("input", JSONB(), nullable=False),
    sa.Column("status", sa.String(24), nullable=False),
    sa.CheckConstraint(
        "status IN ('queued','running','retry_wait','succeeded',"
        "'partially_succeeded','failed','cancelled')"
    ),
    sa.Column("attempt", sa.Integer(), nullable=False),
    sa.Column("position", sa.Integer(), nullable=False),
    sa.Column("accepted", sa.Integer(), nullable=False),
    sa.Column("errors", JSONB(), nullable=False),
    sa.Column("cancel_requested", sa.Boolean(), nullable=False),
    sa.Column("lease_token", sa.Uuid(), nullable=True),
    sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("lease_until", sa.DateTime(timezone=True), nullable=True),
    sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("sequence", sa.Integer(), nullable=False),
)
outbox = tenant_table(
    "job_outbox",
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
    sa.UniqueConstraint("job_id"),
    sa.Column("envelope", JSONB(), nullable=False),
    sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
)
events = tenant_table(
    "job_events",
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
    sa.Column("sequence", sa.Integer(), nullable=False),
    sa.UniqueConstraint("job_id", "sequence"),
    sa.Column("stage", sa.String(40), nullable=False),
    sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
)
sources = tenant_table(
    "ingestion_sources",
    sa.Column("integration_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.id"],
    ),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "integration_id"],
        ["job_integrations.organization_id", "job_integrations.project_id", "job_integrations.id"],
    ),
    sa.Column("work_item_id", sa.Uuid(), nullable=True),
    sa.Column("sprint_id", sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "work_item_id"],
        ["ppm_work_items.organization_id", "ppm_work_items.project_id", "ppm_work_items.id"],
    ),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id", "sprint_id"],
        ["ppm_sprints.organization_id", "ppm_sprints.project_id", "ppm_sprints.id"],
    ),
    sa.CheckConstraint(
        "(target_kind='work_items' AND target_id=work_item_id AND work_item_id IS NOT NULL AND sprint_id IS NULL) OR (target_kind='sprints' AND target_id=sprint_id AND sprint_id IS NOT NULL AND work_item_id IS NULL)"
    ),
    sa.Column("external_id", sa.String(160), nullable=False),
    sa.UniqueConstraint("integration_id", "external_id"),
    sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("source_observed_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("fingerprint", sa.String(64), nullable=False),
    sa.Column("target_id", sa.Uuid(), nullable=False),
    sa.Column("target_kind", sa.String(20), nullable=False),
    sa.Column("target_revision", sa.Integer(), nullable=False),
    sa.Column("job_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "job_id"], ["durable_jobs.organization_id", "durable_jobs.id"]
    ),
)
TABLES = (integrations, jobs, outbox, events, sources)


OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"
ADMIN = "current_setting('ppm.role',true)='Admin'"


def upgrade():
    metadata.reflect(
        op.get_bind(),
        only=[
            "organizations",
            "memberships",
            "identity_sessions",
            "ppm_projects",
            "ppm_work_items",
            "ppm_sprints",
        ],
    )
    metadata.create_all(op.get_bind(), tables=list(TABLES))
    for t in TABLES:
        name = t.name
        read = "true"
        if name != "job_integrations":
            read = (
                f"({ADMIN} OR EXISTS (SELECT 1 FROM durable_jobs j WHERE j.id={name}.job_id AND j.actor_id={UID}))"
                if name != "durable_jobs"
                else f"({ADMIN} OR actor_id={UID})"
            )
        if name == "job_integrations":
            read = f"({ADMIN} OR EXISTS (SELECT 1 FROM ppm_projects p WHERE p.id=job_integrations.project_id))"
        if name == "job_integrations":
            read = "EXISTS (SELECT 1 FROM ppm_projects p WHERE p.id=job_integrations.project_id AND NOT p.archived)"
        elif name == "durable_jobs":
            read = f"({ADMIN} OR actor_id={UID}) AND EXISTS (SELECT 1 FROM job_integrations i WHERE i.id=durable_jobs.integration_id)"
        else:
            read = f"EXISTS (SELECT 1 FROM durable_jobs j WHERE j.id={name}.job_id)"
        op.execute(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY tenant_read ON {name} FOR SELECT TO ppm_app USING (organization_id={OID} AND ({read}))"
        )
        op.execute(
            f"CREATE POLICY tenant_write ON {name} FOR INSERT TO ppm_app WITH CHECK (organization_id={OID} AND ({ADMIN}))"
        )
        op.execute(
            f"CREATE POLICY tenant_update ON {name} FOR UPDATE TO ppm_app USING (organization_id={OID} AND ({ADMIN})) WITH CHECK (organization_id={OID} AND ({ADMIN}))"
        )
        op.execute(f"GRANT SELECT,INSERT,UPDATE ON {name} TO ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_webhook_reference(target uuid)
        RETURNS TABLE(organization_id uuid, actor_id uuid, session_id uuid, secret_ref text)
        LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog, public AS $$
        SELECT i.organization_id,i.actor_id,i.session_id,i.config->>'webhook_secret_ref'
        FROM public.job_integrations i WHERE i.id=target AND i.enabled AND i.config->>'provider'='github' $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_webhook_reference(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_webhook_reference(uuid) TO ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_job_session(target uuid) RETURNS uuid
        LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog, public AS $$
        SELECT j.session_id FROM public.durable_jobs j WHERE j.id=target
          AND j.actor_id=NULLIF(current_setting('ppm.user_id',true),'')::uuid
          AND j.organization_id=NULLIF(current_setting('ppm.organization_id',true),'')::uuid $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_job_session(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_job_session(uuid) TO ppm_app")
    # Narrow control-plane discovery: identifiers only; every task reauthorizes under app RLS.
    op.execute("""CREATE FUNCTION public.ppm_due_jobs() RETURNS TABLE(job_id uuid, organization_id uuid, actor_id uuid)
        LANGUAGE sql SECURITY DEFINER SET search_path = pg_catalog, public AS $$
        SELECT j.id, j.organization_id, j.actor_id FROM public.durable_jobs j
        WHERE (j.status IN ('queued','retry_wait') AND j.available_at <= now())
           OR (j.status='running' AND j.lease_until < now())
        ORDER BY j.available_at,j.id LIMIT 100 $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_due_jobs() FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_due_jobs() TO ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_cancel_unauthorized_job(target uuid) RETURNS boolean
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog, public AS $$
        DECLARE j public.durable_jobs%ROWTYPE; seq integer;
        BEGIN
          SELECT * INTO j FROM public.durable_jobs WHERE id=target;
          IF NOT FOUND OR j.status IN ('succeeded','partially_succeeded','failed','cancelled') THEN RETURN false; END IF;
          PERFORM pg_advisory_xact_lock(hashtextextended(j.organization_id::text,2));
          SELECT * INTO j FROM public.durable_jobs WHERE id=target FOR UPDATE;
          IF j.status IN ('succeeded','partially_succeeded','failed','cancelled') THEN RETURN false; END IF;
          IF NOT EXISTS (SELECT 1 FROM public.memberships m JOIN public.identity_sessions s ON s.user_id=m.user_id
            JOIN public.identity_users u ON u.id=m.user_id
            WHERE m.organization_id=j.organization_id AND m.user_id=j.actor_id AND m.active AND m.role='Admin'
              AND s.id=j.session_id AND s.organization_id=j.organization_id AND NOT s.revoked AND s.expires_at>now() AND u.verified
              AND EXISTS (SELECT 1 FROM public.job_integrations i JOIN public.ppm_projects p
                ON p.organization_id=i.organization_id AND p.id=i.project_id
                WHERE i.id=j.integration_id AND i.organization_id=j.organization_id
                  AND i.enabled AND NOT p.archived))
          THEN
            seq := j.sequence + 1;
            UPDATE public.durable_jobs SET status='cancelled', lease_until=NULL, sequence=seq, updated_at=now(),
              errors=errors || '[{"code":"AUTHORITY_REVOKED"}]'::jsonb WHERE id=target;
            INSERT INTO public.job_events(id,organization_id,job_id,sequence,stage,occurred_at)
              VALUES(gen_random_uuid(),j.organization_id,j.id,seq,'access_revoked',now());
            RETURN true;
          END IF;
          RETURN false;
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) TO ppm_app")


def downgrade():
    op.execute("DROP FUNCTION IF EXISTS public.ppm_cancel_unauthorized_job(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.ppm_webhook_reference(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.ppm_job_session(uuid)")
    op.execute("DROP FUNCTION IF EXISTS public.ppm_due_jobs()")
    for t in reversed(TABLES):
        op.drop_table(t.name)
