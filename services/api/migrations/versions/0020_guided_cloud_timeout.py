"""Bound ordinary guided cloud admission to its frozen policy, at most sixty seconds."""

from alembic import op

revision = "0020_guided_cloud_timeout"
down_revision = "0019_selection_pilot"
branch_labels = None
depends_on = None

OLD = "timeout_s NOT BETWEEN 1 AND 22"
NEW = """(timeout_s NOT BETWEEN 1 AND 60 OR (timeout_s>22 AND NOT COALESCE(
          r.snapshot->>'operation'='agents' AND r.snapshot->>'analysis_mode'='guided'
          AND COALESCE(r.snapshot->>'guided_pilot_id','')=''
          AND jsonb_typeof(r.versions->'guided_cloud_timeout_seconds')='number'
          AND (r.versions->>'guided_cloud_timeout_seconds') ~ '^(2[3-9]|[3-5][0-9]|60)$'
          AND timeout_s <= CASE
            WHEN (r.versions->>'guided_cloud_timeout_seconds') ~ '^(2[3-9]|[3-5][0-9]|60)$'
            THEN (r.versions->>'guided_cloud_timeout_seconds')::integer ELSE 0 END,
          false)))"""
SCOPE_OLD = "IF s.provider_id='ollama' THEN"
SCOPE_NEW = """IF timeout_s>22 AND s.provider_id='ollama' THEN
          RETURN jsonb_build_object('code','CONFIGURATION'); END IF;
        IF s.provider_id='ollama' THEN"""


def change(forward: bool) -> None:
    """Replace checked fragments only; retain quota, authority and settlement safeguards."""
    source = (
        op.get_bind()
        .exec_driver_sql(
            "SELECT pg_get_functiondef('public.ppm_model_admit"
            "(uuid,uuid,text,text,text,uuid,uuid,integer,integer,integer)'::regprocedure)"
        )
        .scalar_one()
    )
    for previous, replacement in ((OLD, NEW), (SCOPE_OLD, SCOPE_NEW)):
        if not forward:
            previous, replacement = replacement, previous
        if source.count(previous) != 1:
            raise RuntimeError("Unexpected model admission definition")
        source = source.replace(previous, replacement)
    op.execute(source)


def upgrade() -> None:
    """Permit a longer quota slot only for an explicitly versioned ordinary guided run."""
    change(True)


def downgrade() -> None:
    """Restore the original bound in disposable migration checks only."""
    change(False)
