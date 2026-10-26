"""Give pre-namespace CSV connections separate identities without rewriting source data."""

import sqlalchemy as sa
from alembic import op

revision = "0018_csv_source_namespaces"
down_revision = "0017_local_ml_foundations"
branch_labels = None
depends_on = None


def upgrade():
    # Explicit namespaces, including 'manual', intentionally remain shared.
    # Clear only the derived key for affected sources so first sync can re-key
    # in place under the new namespace, retaining target IDs and local revisions.
    op.execute(
        sa.text("""
        WITH backfilled AS (
            UPDATE job_integrations
            SET config = config ||
                jsonb_build_object('source_namespace', 'integration-' || id::text)
            WHERE config->>'provider' = 'csv' AND NOT config ? 'source_namespace'
            RETURNING id
        )
        UPDATE ingestion_sources SET logical_key = NULL
        WHERE integration_id IN (SELECT id FROM backfilled)
    """)
    )


def downgrade():
    # Data backfills survive disposable schema downgrades; never discard identity.
    pass
