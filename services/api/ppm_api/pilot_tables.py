"""Sprint 8.1 control-plane delivery and personal notification receipts."""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from ppm_api.database import Base

mail = sa.Table(
    "identity_deliveries",
    Base.metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column(
        "token_hash", sa.String(64), sa.ForeignKey("identity_challenges.token_hash"), nullable=False
    ),
    sa.Column("payload", JSONB, nullable=False),
    sa.Column("status", sa.String(20), nullable=False),
    sa.Column("attempts", sa.Integer, nullable=False),
    sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("error_code", sa.String(30)),
)
notifications = sa.Table(
    "personal_notifications",
    Base.metadata,
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("organization_id", sa.Uuid, sa.ForeignKey("organizations.id"), nullable=False),
    sa.Column("user_id", sa.Uuid, nullable=False),
    sa.Column("kind", sa.String(30), nullable=False),
    sa.Column("target_id", sa.Uuid, nullable=False),
    sa.Column("event_key", sa.String(160), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("read", sa.Boolean, nullable=False),
    sa.UniqueConstraint("organization_id", "user_id", "event_key"),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
)
preferences = sa.Table(
    "notification_preferences",
    Base.metadata,
    sa.Column("organization_id", sa.Uuid, primary_key=True),
    sa.Column("user_id", sa.Uuid, primary_key=True),
    sa.Column("enabled", sa.Boolean, nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
)
