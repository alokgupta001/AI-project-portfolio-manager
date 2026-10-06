"""Sprint 02 identity snapshot. Keep independent of future application models."""

import sqlalchemy as sa
from alembic import op

metadata = sa.MetaData()
users = sa.Table(
    "identity_users",
    metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("email", sa.String(254), nullable=False, unique=True),
    sa.Column("name", sa.String(120), nullable=False),
    sa.Column("password_hash", sa.String(128)),
    sa.Column("verified", sa.Boolean, nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
)
organizations = sa.Table(
    "organizations",
    metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("name", sa.String(120), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
)
memberships = sa.Table(
    "memberships",
    metadata,
    sa.Column("organization_id", sa.Uuid, sa.ForeignKey("organizations.id"), primary_key=True),
    sa.Column("user_id", sa.Uuid, sa.ForeignKey("identity_users.id"), primary_key=True),
    sa.Column("role", sa.String(20), nullable=False),
    sa.Column("active", sa.Boolean, nullable=False),
    sa.Column("revision", sa.Integer, nullable=False),
    sa.CheckConstraint("role IN ('Admin','Project Manager','Viewer')", name="ck_membership_role"),
)
sessions = sa.Table(
    "identity_sessions",
    metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("user_id", sa.Uuid, sa.ForeignKey("identity_users.id"), nullable=False, index=True),
    sa.Column("organization_id", sa.Uuid, nullable=False),
    sa.Column("csrf_hash", sa.String(64), nullable=False),
    sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("revoked", sa.Boolean, nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
)
refresh_tokens = sa.Table(
    "identity_refresh_tokens",
    metadata,
    sa.Column("token_hash", sa.String(64), primary_key=True),
    sa.Column("session_id", sa.Uuid, sa.ForeignKey("identity_sessions.id"), nullable=False),
    sa.Column("used", sa.Boolean, nullable=False),
)
challenges = sa.Table(
    "identity_challenges",
    metadata,
    sa.Column("token_hash", sa.String(64), primary_key=True),
    sa.Column("kind", sa.String(12), nullable=False),
    sa.Column("email", sa.String(254), nullable=False),
    sa.Column("organization_id", sa.Uuid, sa.ForeignKey("organizations.id")),
    sa.Column("inviter_id", sa.Uuid),
    sa.Column("role", sa.String(20)),
    sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("used", sa.Boolean, nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "inviter_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.CheckConstraint("kind IN ('activate','reset','invite')", name="ck_challenge_kind"),
)
audit = sa.Table(
    "identity_audit",
    metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("organization_id", sa.Uuid, nullable=False, index=True),
    sa.Column("actor_id", sa.Uuid, nullable=False),
    sa.Column("action", sa.String(60), nullable=False),
    sa.Column("target_id", sa.Uuid),
    sa.Column("request_id", sa.Uuid, nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
)

revision = "0002_identity"
down_revision = "0001_foundation"
branch_labels = None
depends_on = None


def upgrade():
    metadata.create_all(op.get_bind())
    op.execute(
        "GRANT SELECT, INSERT, UPDATE ON identity_users, identity_sessions, "
        "identity_refresh_tokens, identity_challenges TO ppm_app"
    )
    op.execute("GRANT SELECT ON organizations TO ppm_app")
    op.execute("GRANT SELECT, INSERT, UPDATE ON memberships TO ppm_app")
    op.execute("GRANT SELECT, INSERT ON identity_audit TO ppm_app")
    for table in ("organizations", "memberships", "identity_audit"):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    uid = "NULLIF(current_setting('ppm.user_id', true), '')::uuid"
    oid = "NULLIF(current_setting('ppm.organization_id', true), '')::uuid"
    admin = "current_setting('ppm.role', true) = 'Admin'"
    op.execute(
        f"CREATE POLICY organization_read ON organizations FOR SELECT TO "
        f"ppm_app USING (id = {oid} OR EXISTS (SELECT 1 FROM memberships m "
        f"WHERE m.organization_id = organizations.id AND m.user_id = {uid} "
        f"AND m.active))"
    )
    op.execute(
        f"CREATE POLICY membership_read ON memberships FOR SELECT TO ppm_app "
        f"USING (user_id = {uid} OR organization_id = {oid})"
    )
    op.execute(
        f"CREATE POLICY membership_insert ON memberships FOR INSERT TO "
        f"ppm_app WITH CHECK (organization_id = {oid} AND {admin})"
    )
    op.execute(
        f"CREATE POLICY membership_update ON memberships FOR UPDATE TO "
        f"ppm_app USING (organization_id = {oid} AND {admin}) WITH CHECK "
        f"(organization_id = {oid} AND {admin})"
    )
    op.execute(
        f"CREATE POLICY audit_read ON identity_audit FOR SELECT TO ppm_app "
        f"USING (organization_id = {oid} AND {admin})"
    )
    op.execute(
        f"CREATE POLICY audit_insert ON identity_audit FOR INSERT TO ppm_app "
        f"WITH CHECK (organization_id = {oid} AND actor_id = {uid})"
    )


def downgrade():
    op.execute("DROP POLICY organization_read ON organizations")
    metadata.drop_all(op.get_bind())
