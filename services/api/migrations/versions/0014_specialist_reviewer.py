# ruff: noqa: E501
"""Allow independent assessment reviewers with current project scope to read analyses."""

from alembic import op

revision = "0014_specialist_reviewer"
down_revision = "0013_specialist_reviews"
branch_labels = None
depends_on = None

OID = "NULLIF(current_setting('ppm.organization_id',true),'')::uuid"
UID = "NULLIF(current_setting('ppm.user_id',true),'')::uuid"
ROLE = "current_setting('ppm.role',true)"
ADMIN = f"{ROLE}='Admin'"
EDIT = f"({ADMIN} OR ({ROLE}='Project Manager' AND EXISTS (SELECT 1 FROM ppm_grants g WHERE g.project_id=agent_analyses.project_id AND g.user_id={UID} AND NOT g.archived AND g.access IN ('edit','manage'))))"
PRIVATE = f"(assessment_id IS NULL OR {ADMIN} OR ({ROLE}='Project Manager' AND EXISTS (SELECT 1 FROM ppm_assessments a WHERE a.id=assessment_id AND (a.assigned_to={UID} OR a.reviewer_id={UID}))))"
REVIEWER = f"(actor_id<>{UID} AND assessment_id IS NOT NULL AND {ROLE} IN ('Admin','Project Manager') AND EXISTS (SELECT 1 FROM ppm_assessments r WHERE r.id=assessment_id AND r.reviewer_id={UID} AND r.assigned_to<>{UID} AND (r.submitted_by IS NULL OR r.submitted_by<>{UID})))"
BASE = f"organization_id={OID} AND EXISTS (SELECT 1 FROM ppm_projects p WHERE p.id=project_id AND NOT p.archived) AND {PRIVATE}"
OLD_SCOPE = f"{BASE} AND ({ADMIN} OR actor_id={UID} OR {EDIT})"
SCOPE = f"{BASE} AND ({ADMIN} OR actor_id={UID} OR {EDIT} OR {REVIEWER})"


def upgrade():
    op.execute(f"ALTER POLICY agent_read ON agent_analyses USING ({SCOPE})")


def downgrade():
    op.execute(f"ALTER POLICY agent_read ON agent_analyses USING ({OLD_SCOPE})")
