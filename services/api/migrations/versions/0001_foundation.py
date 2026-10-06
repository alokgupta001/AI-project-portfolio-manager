"""Initial non-tenant installation checkpoint. No domain tables."""

from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision = "0001_foundation"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    table = op.create_table(
        "foundation_state",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("instance_id", sa.Uuid, nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("id = 1", name="ck_foundation_singleton"),
    )
    op.bulk_insert(table, [{"id": 1, "instance_id": uuid4(), "created_at": datetime.now(UTC)}])
    op.execute("GRANT SELECT ON foundation_state TO ppm_app")


def downgrade():
    op.drop_table("foundation_state")
