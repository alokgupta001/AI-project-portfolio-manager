# ruff: noqa: E501
"""Add specialist snapshots and independent append-only review decisions after 0012."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0013_specialist_reviews"
down_revision = "0012_ai_runtime"
branch_labels = None
depends_on = None
metadata = sa.MetaData()


def tab(name, *columns):
    return sa.Table(
        name,
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.UniqueConstraint("organization_id", "id"),
        *columns,
    )


analyses = tab(
    "agent_analyses",
    sa.Column("run_id", sa.Uuid(), nullable=False, unique=True),
    sa.ForeignKeyConstraint(
        ["organization_id", "run_id"], ["ai_runs.organization_id", "ai_runs.id"]
    ),
    sa.Column("project_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "project_id"], ["ppm_projects.organization_id", "ppm_projects.id"]
    ),
    sa.Column("assessment_id", sa.Uuid()),
    sa.ForeignKeyConstraint(
        ["organization_id", "assessment_id"],
        ["ppm_assessments.organization_id", "ppm_assessments.id"],
    ),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("snapshot", JSONB(), nullable=False),
    sa.Column("output", JSONB(none_as_null=True)),
)
reviews = tab(
    "agent_reviews",
    sa.Column("analysis_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "analysis_id"], ["agent_analyses.organization_id", "agent_analyses.id"]
    ),
    sa.Column("item_key", sa.String(96), nullable=False),
    sa.Column("actor_id", sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(
        ["organization_id", "actor_id"], ["memberships.organization_id", "memberships.user_id"]
    ),
    sa.Column("decision", sa.String(16), nullable=False),
    sa.CheckConstraint("decision IN ('accepted','rejected')"),
    sa.Column("reason", sa.String(1000), nullable=False),
    sa.Column("approved_score", sa.Numeric(7, 4)),
    sa.CheckConstraint("approved_score IS NULL OR approved_score BETWEEN 0 AND 100"),
    sa.Column("revision", sa.Integer(), nullable=False),
    sa.CheckConstraint("revision > 0"),
    sa.UniqueConstraint("analysis_id", "item_key", "revision"),
    sa.Column("key", sa.Uuid(), nullable=False),
    sa.UniqueConstraint("organization_id", "actor_id", "key"),
    sa.Column("fingerprint", sa.String(64), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
)

OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"
ROLE = "current_setting('ppm.role',true)"
ADMIN = f"{ROLE}='Admin'"
EDIT = f"({ADMIN} OR ({ROLE}='Project Manager' AND EXISTS (SELECT 1 FROM ppm_grants g WHERE g.project_id=agent_analyses.project_id AND g.user_id={UID} AND NOT g.archived AND g.access IN ('edit','manage'))))"
PRIVATE = f"(assessment_id IS NULL OR {ADMIN} OR ({ROLE}='Project Manager' AND EXISTS (SELECT 1 FROM ppm_assessments a WHERE a.id=assessment_id AND (a.assigned_to={UID} OR a.reviewer_id={UID}))))"
SCOPE = f"organization_id={OID} AND EXISTS (SELECT 1 FROM ppm_projects p WHERE p.id=project_id AND NOT p.archived) AND {PRIVATE} AND ({ADMIN} OR actor_id={UID} OR {EDIT})"
INDEPENDENT = f"a.actor_id<>{UID} AND ({ROLE} IN ('Admin','Project Manager')) AND ((a.assessment_id IS NOT NULL AND EXISTS (SELECT 1 FROM ppm_assessments s WHERE s.id=a.assessment_id AND s.reviewer_id={UID} AND s.assigned_to<>{UID} AND (s.submitted_by IS NULL OR s.submitted_by<>{UID}))) OR (a.assessment_id IS NULL AND ({ADMIN} OR EXISTS (SELECT 1 FROM ppm_grants g WHERE g.project_id=a.project_id AND g.user_id={UID} AND NOT g.archived AND g.access IN ('edit','manage')))))"


def upgrade():
    metadata.reflect(
        op.get_bind(),
        only=["organizations", "memberships", "ai_runs", "ppm_projects", "ppm_assessments"],
    )
    metadata.create_all(op.get_bind(), tables=[analyses, reviews])
    op.execute("ALTER TABLE agent_analyses ENABLE ROW LEVEL SECURITY")
    op.execute(f"CREATE POLICY agent_read ON agent_analyses FOR SELECT TO ppm_app USING ({SCOPE})")
    op.execute(
        f"CREATE POLICY agent_insert ON agent_analyses FOR INSERT TO ppm_app WITH CHECK (organization_id={OID} AND {ADMIN} AND actor_id={UID})"
    )
    op.execute(
        f"CREATE POLICY agent_update ON agent_analyses FOR UPDATE TO ppm_app USING (organization_id={OID} AND {ADMIN}) WITH CHECK (organization_id={OID} AND {ADMIN})"
    )
    op.execute("GRANT SELECT,INSERT,UPDATE ON agent_analyses TO ppm_app")
    op.execute("""CREATE FUNCTION public.ppm_agent_parent() RETURNS trigger
        LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public AS $$ BEGIN
          IF NEW.output IS NOT NULL OR NOT EXISTS (SELECT 1 FROM public.ai_runs r
            WHERE r.id=NEW.run_id AND r.organization_id=NEW.organization_id
              AND r.project_id=NEW.project_id AND r.actor_id=NEW.actor_id
              AND r.snapshot->>'operation'='agents' AND NOT r.settled)
          THEN RAISE check_violation USING MESSAGE='Specialist parent mismatch'; END IF;
          RETURN NEW;
        END $$""")
    op.execute("REVOKE ALL ON FUNCTION public.ppm_agent_parent() FROM PUBLIC")
    op.execute(
        "CREATE TRIGGER agent_parent BEFORE INSERT ON agent_analyses FOR EACH ROW EXECUTE FUNCTION public.ppm_agent_parent()"
    )
    op.execute("ALTER TABLE agent_reviews ENABLE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY review_read ON agent_reviews FOR SELECT TO ppm_app USING (organization_id={OID} AND EXISTS (SELECT 1 FROM agent_analyses a WHERE a.id=analysis_id))"
    )
    op.execute(
        f"CREATE POLICY review_insert ON agent_reviews FOR INSERT TO ppm_app WITH CHECK (organization_id={OID} AND actor_id={UID} AND EXISTS (SELECT 1 FROM agent_analyses a WHERE a.id=analysis_id AND {INDEPENDENT}))"
    )
    op.execute("GRANT SELECT,INSERT ON agent_reviews TO ppm_app")
    op.execute(
        f"CREATE POLICY agent_read ON ai_runs FOR SELECT TO ppm_app USING (organization_id={OID} AND EXISTS (SELECT 1 FROM agent_analyses a WHERE a.run_id=ai_runs.id))"
    )
    op.execute("""CREATE FUNCTION public.ppm_agent_immutable() RETURNS trigger LANGUAGE plpgsql SET search_path=pg_catalog,public AS $$ BEGIN
        IF TG_TABLE_NAME='agent_reviews' OR TG_OP='DELETE' THEN
          RAISE check_violation USING MESSAGE='Specialist history is append-only';
        END IF;
        IF (NEW.id,NEW.organization_id,NEW.run_id,NEW.project_id,NEW.assessment_id,NEW.actor_id,NEW.snapshot)
          IS DISTINCT FROM (OLD.id,OLD.organization_id,OLD.run_id,OLD.project_id,OLD.assessment_id,OLD.actor_id,OLD.snapshot)
          OR OLD.output IS NOT NULL OR EXISTS (SELECT 1 FROM public.ai_runs r WHERE r.id=OLD.run_id AND r.settled)
        THEN RAISE check_violation USING MESSAGE='Specialist provenance/results are immutable'; END IF;
        RETURN NEW;
        END $$""")
    for name in ("agent_analyses", "agent_reviews"):
        op.execute(
            f"CREATE TRIGGER agent_immutable BEFORE UPDATE OR DELETE ON {name} FOR EACH ROW EXECUTE FUNCTION public.ppm_agent_immutable()"
        )


def downgrade():
    # Destructive lifecycle is guarded by the test runner; normal recovery is forward-only.
    op.execute("DROP POLICY agent_read ON ai_runs")
    for table in (reviews, analyses):
        op.execute(f"DROP TRIGGER agent_immutable ON {table.name}")
        table.drop(op.get_bind())
    op.execute("DROP FUNCTION public.ppm_agent_parent()")
    op.execute("DROP FUNCTION public.ppm_agent_immutable()")
