# ruff: noqa: E501
"""Explicit project-scoped zero-cost guided execution without organization promotion."""

from alembic import op

revision = "0016_guided_project_access"
down_revision = "0015_agent_task_runtime"
branch_labels = None
depends_on = None

OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"
AUTH = """(m.role='Admin' OR (r.snapshot->>'operation'='agents'
 AND r.snapshot->>'analysis_mode'='guided' AND r.versions->>'runtime_version'='v2'
 AND r.reservation=0 AND r.charged_usd=0
 AND public.ppm_guided_actor(r.organization_id,r.actor_id,r.project_id)))"""


def worker_authority(forward: bool) -> None:
    """Replace only the existing role condition, preserving all other worker fences."""
    for name in ("ppm_ai_job", "ppm_model_admit"):
        source = (
            op.get_bind()
            .exec_driver_sql(
                "SELECT pg_get_functiondef(p.oid) FROM pg_proc p "
                "JOIN pg_namespace n ON n.oid=p.pronamespace "
                f"WHERE n.nspname='public' AND p.proname='{name}'"
            )
            .scalar_one()
        )
        old, new = ("m.role='Admin'", AUTH) if forward else (AUTH, "m.role='Admin'")
        if source.count(old) != 1:
            raise RuntimeError("Unexpected worker authority definition")
        op.execute(source.replace(old, new))


def policies() -> dict[str, dict[str, str]]:
    """Only owned, zero-cost guided runs gain additional app-role permissions."""
    own = f"organization_id={OID} AND actor_id={UID}"
    run = f"organization_id={OID} AND public.ppm_guided_run(run_id)"
    job = (
        f"organization_id={OID} AND EXISTS (SELECT 1 FROM durable_jobs j "
        "WHERE j.id=job_id AND public.ppm_guided_run(j.ai_run_id))"
    )
    start = (
        f"{own} AND snapshot->>'operation'='agents' AND snapshot->>'analysis_mode'='guided' "
        "AND versions->>'runtime_version'='v2' AND reservation=0 AND charged_usd=0 "
        f"AND public.ppm_guided_actor(organization_id,{UID},project_id)"
    )
    task = run + " AND EXISTS (SELECT 1 FROM ai_runs r WHERE r.id=run_id AND NOT r.settled)"
    return {
        "ai_budgets": {
            "SELECT": f"organization_id={OID} AND EXISTS (SELECT 1 FROM ai_guided_grants g WHERE g.organization_id={OID} AND g.user_id={UID} AND public.ppm_guided_actor(g.organization_id,g.user_id,g.project_id))"
        },
        "ai_runs": {"INSERT": start, "UPDATE": start},
        "ai_calls": {
            "SELECT": run,
            "INSERT": run + " AND charged_usd=0",
            "UPDATE": run + " AND charged_usd=0",
        },
        "agent_analyses": {
            "INSERT": run + f" AND actor_id={UID}",
            "UPDATE": run + f" AND actor_id={UID}",
        },
        "agent_tasks": {"INSERT": task, "UPDATE": task},
        "agent_sections": {"INSERT": task},
        "durable_jobs": {
            "INSERT": own + " AND public.ppm_guided_run(ai_run_id)",
            "UPDATE": own + " AND public.ppm_guided_run(ai_run_id)",
        },
        "job_events": {"INSERT": job, "UPDATE": job},
        "job_outbox": {"INSERT": job, "UPDATE": job},
    }


def upgrade():
    op.execute("""CREATE TABLE ai_guided_grants (
      organization_id uuid NOT NULL, user_id uuid NOT NULL, project_id uuid NOT NULL,
      enabled boolean NOT NULL, created_at timestamptz NOT NULL,
      PRIMARY KEY (organization_id,user_id,project_id),
      FOREIGN KEY (organization_id,user_id) REFERENCES memberships(organization_id,user_id),
      FOREIGN KEY (organization_id,project_id) REFERENCES ppm_projects(organization_id,id))""")
    op.execute("ALTER TABLE ai_guided_grants ENABLE ROW LEVEL SECURITY")
    op.execute("REVOKE ALL ON ai_guided_grants FROM PUBLIC,ppm_app")
    op.execute("GRANT SELECT ON ai_guided_grants TO ppm_app")
    op.execute(
        f"CREATE POLICY guided_read ON ai_guided_grants FOR SELECT TO ppm_app USING (organization_id={OID} AND user_id={UID})"
    )
    op.execute("""CREATE FUNCTION public.ppm_guided_actor(tenant uuid, actor uuid, project uuid)
      RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      SELECT EXISTS (SELECT 1 FROM public.ai_guided_grants a
        JOIN public.memberships m ON m.organization_id=a.organization_id AND m.user_id=a.user_id
        JOIN public.identity_users u ON u.id=a.user_id
        JOIN public.ppm_projects p ON p.organization_id=a.organization_id AND p.id=a.project_id
        WHERE a.organization_id=tenant AND a.user_id=actor AND a.project_id=project AND a.enabled
          AND m.active AND u.active AND u.verified AND NOT p.archived
          AND (m.role='Admin' OR EXISTS (SELECT 1 FROM public.ppm_grants g
            WHERE g.organization_id=tenant AND g.user_id=actor AND NOT g.archived
              AND (g.project_id=p.id OR g.portfolio_id=p.portfolio_id)
              AND g.access IN ('read','edit','manage')))) $$""")
    op.execute(f"""CREATE FUNCTION public.ppm_guided_run(rid uuid)
      RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,public AS $$
      SELECT EXISTS (SELECT 1 FROM public.ai_runs r WHERE r.id=rid
        AND r.organization_id={OID} AND r.actor_id={UID}
        AND r.snapshot->>'operation'='agents' AND r.snapshot->>'analysis_mode'='guided'
        AND r.versions->>'runtime_version'='v2' AND r.reservation=0 AND r.charged_usd=0
        AND public.ppm_guided_actor(r.organization_id,r.actor_id,r.project_id)) $$""")
    for signature in ("ppm_guided_actor(uuid,uuid,uuid)", "ppm_guided_run(uuid)"):
        op.execute(f"REVOKE ALL ON FUNCTION public.{signature} FROM PUBLIC")
        op.execute(f"GRANT EXECUTE ON FUNCTION public.{signature} TO ppm_app")
    for table, commands in policies().items():
        for command, clause in commands.items():
            rule = f"WITH CHECK ({clause})" if command == "INSERT" else f"USING ({clause})"
            if command == "UPDATE":
                rule += f" WITH CHECK ({clause})"
            op.execute(
                f"CREATE POLICY guided_{command.lower()} ON {table} FOR {command} TO ppm_app {rule}"
            )
    worker_authority(True)


def downgrade():
    worker_authority(False)
    for table, commands in policies().items():
        for command in commands:
            op.execute(f"DROP POLICY guided_{command.lower()} ON {table}")
    op.execute("DROP FUNCTION public.ppm_guided_run(uuid)")
    op.execute("DROP FUNCTION public.ppm_guided_actor(uuid,uuid,uuid)")
    op.execute("DROP TABLE ai_guided_grants")
