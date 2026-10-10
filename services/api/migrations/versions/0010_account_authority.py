"""Cancel queued work when its initiating global identity is disabled."""

from alembic import op

revision = "0010_account_authority"
down_revision = "0009_account_repair"
branch_labels = None
depends_on = None


def install(active: bool) -> None:
    account_guard = " AND u.active" if active else ""
    op.execute(f"""CREATE OR REPLACE FUNCTION public.ppm_cancel_unauthorized_job(target uuid)
        RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER
        SET search_path = pg_catalog, public AS $$
        DECLARE j public.durable_jobs%ROWTYPE; seq integer;
        BEGIN
          SELECT * INTO j FROM public.durable_jobs WHERE id=target;
          IF NOT FOUND OR j.status IN ('succeeded','partially_succeeded','failed','cancelled') THEN
            RETURN false;
          END IF;
          PERFORM pg_advisory_xact_lock(hashtextextended(j.organization_id::text,2));
          SELECT * INTO j FROM public.durable_jobs WHERE id=target FOR UPDATE;
          IF j.status IN ('succeeded','partially_succeeded','failed','cancelled') THEN
            RETURN false;
          END IF;
          IF NOT EXISTS (SELECT 1 FROM public.memberships m
            JOIN public.identity_sessions s ON s.user_id=m.user_id
            JOIN public.identity_users u ON u.id=m.user_id
            WHERE m.organization_id=j.organization_id AND m.user_id=j.actor_id
              AND m.active AND m.role='Admin'
              AND s.id=j.session_id AND s.organization_id=j.organization_id
              AND NOT s.revoked AND s.expires_at>now() AND u.verified{account_guard}
              AND EXISTS (SELECT 1 FROM public.job_integrations i JOIN public.ppm_projects p
                ON p.organization_id=i.organization_id AND p.id=i.project_id
                WHERE i.id=j.integration_id AND i.organization_id=j.organization_id
                  AND i.enabled AND NOT p.archived))
          THEN
            seq := j.sequence + 1;
            UPDATE public.durable_jobs SET status='cancelled', lease_until=NULL,
              sequence=seq, updated_at=now(),
              errors=errors || '[{{"code":"AUTHORITY_REVOKED"}}]'::jsonb WHERE id=target;
            INSERT INTO public.job_events(id,organization_id,job_id,sequence,stage,occurred_at)
              VALUES(gen_random_uuid(),j.organization_id,j.id,seq,'access_revoked',now());
            RETURN true;
          END IF;
          RETURN false;
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.ppm_cancel_unauthorized_job(uuid) TO ppm_app")


def upgrade() -> None:
    install(True)


def downgrade() -> None:
    install(False)
