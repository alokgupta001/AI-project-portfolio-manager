"""Separate global account status from optional organization session context."""

import sqlalchemy as sa
from alembic import op

revision = "0009_account_repair"
down_revision = "0008_pilot_completion"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "identity_users", sa.Column("active", sa.Boolean, nullable=False, server_default=sa.true())
    )
    op.alter_column("identity_sessions", "organization_id", nullable=True)
    for name, size in [("description", 1000), ("industry", 120), ("website", 500)]:
        op.add_column("organizations", sa.Column(name, sa.String(size)))


def downgrade() -> None:
    # An organization-free session has no representation in the older model.
    # Remove only those transient sessions, preserving accounts and memberships.
    op.execute(
        "DELETE FROM identity_refresh_tokens WHERE session_id IN "
        "(SELECT id FROM identity_sessions WHERE organization_id IS NULL)"
    )
    op.execute("DELETE FROM identity_sessions WHERE organization_id IS NULL")
    op.alter_column("identity_sessions", "organization_id", nullable=False)
    for name in ["website", "industry", "description"]:
        op.drop_column("organizations", name)
    op.drop_column("identity_users", "active")
