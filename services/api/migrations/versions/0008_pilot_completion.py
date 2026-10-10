"""Additive pilot identity, notification receipts and optional metadata. Frozen snapshot."""

# ruff: noqa: E501
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0008_pilot_completion"
down_revision = "0007_durable_jobs"
branch_labels = None
depends_on = None

PROJECT_FIELDS = {
    "priority": ["low", "normal", "high", "urgent"],
    "industry": ["fintech", "technology", "healthcare", "public_sector", "other"],
    "category": ["delivery", "transformation", "compliance", "research", "other"],
    "methodology": ["agile", "waterfall", "hybrid", "other"],
    "size_band": ["small", "medium", "large"],
}
WORK_FIELDS = {
    "priority": PROJECT_FIELDS["priority"],
    "work_type": ["task", "bug", "story", "feature", "other"],
}


def upgrade() -> None:
    op.add_column(
        "organizations", sa.Column("revision", sa.Integer, nullable=False, server_default="1")
    )
    op.add_column("identity_challenges", sa.Column("invitation_id", sa.Uuid, unique=True))
    op.add_column("identity_challenges", sa.Column("organization_name", sa.String(120)))
    op.drop_constraint("ck_challenge_kind", "identity_challenges", type_="check")
    op.create_check_constraint(
        "ck_challenge_kind",
        "identity_challenges",
        "kind IN ('activate','reset','invite','register')",
    )
    op.execute("GRANT INSERT,UPDATE ON organizations TO ppm_app")
    op.execute(
        "CREATE POLICY organization_insert ON organizations FOR INSERT TO ppm_app WITH CHECK (id=NULLIF(current_setting('ppm.organization_id',true),'')::uuid AND current_setting('ppm.role',true)='Admin')"
    )
    op.execute(
        "CREATE POLICY organization_update ON organizations FOR UPDATE TO ppm_app USING (id=NULLIF(current_setting('ppm.organization_id',true),'')::uuid AND current_setting('ppm.role',true)='Admin') WITH CHECK (id=NULLIF(current_setting('ppm.organization_id',true),'')::uuid AND current_setting('ppm.role',true)='Admin')"
    )
    op.create_table(
        "identity_deliveries",
        sa.Column("id", sa.Uuid, primary_key=True),
        sa.Column(
            "token_hash",
            sa.String(64),
            sa.ForeignKey("identity_challenges.token_hash"),
            nullable=False,
        ),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("error_code", sa.String(30)),
    )
    # Private identity control plane, like hashed challenges. No route exposes payloads.
    op.execute("GRANT SELECT,INSERT,UPDATE ON identity_deliveries TO ppm_app")
    op.create_table(
        "personal_notifications",
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
    op.create_table(
        "notification_preferences",
        sa.Column("organization_id", sa.Uuid, primary_key=True),
        sa.Column("user_id", sa.Uuid, primary_key=True),
        sa.Column("enabled", sa.Boolean, nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id", "user_id"], ["memberships.organization_id", "memberships.user_id"]
        ),
    )
    for name in ["personal_notifications", "notification_preferences"]:
        op.execute(f"ALTER TABLE {name} ENABLE ROW LEVEL SECURITY")
        scope = "organization_id=NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
        own = "user_id=NULLIF(current_setting('ppm.user_id',true),'')::uuid"
        op.execute(
            f"CREATE POLICY personal_read ON {name} FOR SELECT TO ppm_app USING ({scope} AND {own})"
        )
        op.execute(
            f"CREATE POLICY personal_update ON {name} FOR UPDATE TO ppm_app USING ({scope} AND {own}) WITH CHECK ({scope} AND {own})"
        )
        write = scope if name == "personal_notifications" else f"{scope} AND {own}"
        op.execute(
            f"CREATE POLICY personal_insert ON {name} FOR INSERT TO ppm_app WITH CHECK ({write})"
        )
        op.execute(f"GRANT SELECT,INSERT,UPDATE ON {name} TO ppm_app")
    for table, fields in [("ppm_projects", PROJECT_FIELDS), ("ppm_work_items", WORK_FIELDS)]:
        for field, values in fields.items():
            op.add_column(table, sa.Column(field, sa.String(30)))
            options = ",".join("'" + v + "'" for v in values)
            op.create_check_constraint(
                f"ck_{table}_{field}", table, f"{field} IS NULL OR {field} IN ({options})"
            )


def downgrade() -> None:
    for table, fields in [("ppm_projects", PROJECT_FIELDS), ("ppm_work_items", WORK_FIELDS)]:
        for field in fields:
            op.drop_column(table, field)
    for table in ["notification_preferences", "personal_notifications", "identity_deliveries"]:
        op.drop_table(table)
    op.execute("DROP POLICY organization_insert ON organizations")
    op.execute("DROP POLICY organization_update ON organizations")
    op.execute("REVOKE INSERT,UPDATE ON organizations FROM ppm_app")
    op.drop_column("organizations", "revision")
    op.execute("DELETE FROM identity_challenges WHERE kind='register'")
    op.drop_constraint("ck_challenge_kind", "identity_challenges", type_="check")
    op.create_check_constraint(
        "ck_challenge_kind", "identity_challenges", "kind IN ('activate','reset','invite')"
    )
    op.drop_column("identity_challenges", "invitation_id")
    op.drop_column("identity_challenges", "organization_name")
