"""Identity control plane and tenant-owned membership/audit metadata."""

import sqlalchemy as sa

from ppm_api.database import Base

metadata = Base.metadata
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
