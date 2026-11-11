"""Add an isolated synthetic selection pilot without changing provider authority or history."""

from alembic import op

revision = "0019_selection_pilot"
down_revision = "0018_csv_source_namespaces"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""CREATE TABLE ai_selection_pilots (
      id uuid PRIMARY KEY, organization_id uuid NOT NULL REFERENCES organizations(id),
      UNIQUE(organization_id,id), project_id uuid NOT NULL, actor_id uuid NOT NULL,
      binding jsonb NOT NULL, review jsonb, case_runs jsonb NOT NULL,
      created_at timestamptz NOT NULL, revision integer NOT NULL,
      FOREIGN KEY(organization_id,project_id) REFERENCES ppm_projects(organization_id,id),
      FOREIGN KEY(organization_id,actor_id) REFERENCES memberships(organization_id,user_id),
      CHECK(revision > 0 AND octet_length(case_runs::text) <= 2000))""")
    op.execute("ALTER TABLE ai_selection_pilots ENABLE ROW LEVEL SECURITY")
    op.execute("REVOKE ALL ON ai_selection_pilots FROM PUBLIC,ppm_app")
    op.execute("GRANT SELECT,INSERT,UPDATE ON ai_selection_pilots TO ppm_app")
    scope = (
        "organization_id=NULLIF(current_setting('ppm.organization_id',true),'')::uuid "
        "AND current_setting('ppm.role',true)='Admin'"
    )
    op.execute(
        f"CREATE POLICY selection_admin ON ai_selection_pilots TO ppm_app "
        f"USING ({scope}) WITH CHECK ({scope})"
    )


def downgrade():
    op.drop_table("ai_selection_pilots")
