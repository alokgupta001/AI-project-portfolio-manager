# Current source-derived database dictionary

Derived from current SQLAlchemy `Base.metadata` definitions, including pilot tables, without opening a connection. Schema source has migrations 0001–0008. This does not independently inspect the applied runtime schema. Constraints/indexes/RLS installed by migration SQL must also be read in [the migration directory](../../services/api/migrations/versions); metadata alone is not the complete database-policy definition. No migration/schema/data was changed by this audit.

## Important data flows

Organization → membership → transaction-local principal/RLS → domain records. Portfolio/project links constrain work/risks/milestones/allocations; resource profiles differ from login identities. Published framework versions preserve assessment scoring history. Jobs/outbox persist ingestion state. Identity deliveries reference challenge hashes privately. Notification membership references and unique event keys isolate recipients and deduplicate receipts. Optional project/work metadata remains null for unknown historical classification.

For transactional query/debugging steps use [database learning](../02-learning/04-database/DATABASE_GUIDE.md); for planned schema changes use [roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md) marked PLANNED. Historical pre-audit dictionary remains [an archived snapshot](../10-reference/history/DATABASE_DICTIONARY_PRE_AUDIT.md).

## durable_jobs

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, memberships.organization_id, job_integrations.organization_id |
| `integration_id` | `CHAR(32)` | False | False | job_integrations.id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `session_id` | `CHAR(32)` | False | False | identity_sessions.id |
| `key` | `VARCHAR(160)` | False | False | — |
| `request_hash` | `VARCHAR(64)` | False | False | — |
| `config` | `JSONB` | False | False | — |
| `input` | `JSONB` | False | False | — |
| `status` | `VARCHAR(24)` | False | False | — |
| `attempt` | `INTEGER` | False | False | — |
| `position` | `INTEGER` | False | False | — |
| `accepted` | `INTEGER` | False | False | — |
| `errors` | `JSONB` | False | False | — |
| `cancel_requested` | `BOOLEAN` | False | False | — |
| `lease_token` | `CHAR(32)` | True | False | — |
| `heartbeat_at` | `DATETIME` | True | False | — |
| `lease_until` | `DATETIME` | True | False | — |
| `available_at` | `DATETIME` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `sequence` | `INTEGER` | False | False | — |

Metadata check expressions: status IN ('queued','running','retry_wait','succeeded','partially_succeeded','failed','cancelled')

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, actor_id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): session_id

- ForeignKeyConstraint (unnamed): organization_id, integration_id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, actor_id, key

## foundation_state

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `INTEGER` | False | True | — |
| `instance_id` | `CHAR(32)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

Metadata check expressions: id = 1

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): instance_id

## identity_audit

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `action` | `VARCHAR(60)` | False | False | — |
| `target_id` | `CHAR(32)` | True | False | — |
| `request_id` | `CHAR(32)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, actor_id

- Index ix_identity_audit_organization_id: identity_audit.organization_id

## identity_challenges

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `token_hash` | `VARCHAR(64)` | False | True | — |
| `kind` | `VARCHAR(12)` | False | False | — |
| `email` | `VARCHAR(254)` | False | False | — |
| `organization_id` | `CHAR(32)` | True | False | memberships.organization_id, organizations.id |
| `inviter_id` | `CHAR(32)` | True | False | memberships.user_id |
| `role` | `VARCHAR(20)` | True | False | — |
| `expires_at` | `DATETIME` | False | False | — |
| `used` | `BOOLEAN` | False | False | — |
| `invitation_id` | `CHAR(32)` | True | False | — |
| `organization_name` | `VARCHAR(120)` | True | False | — |

Metadata check expressions: kind IN ('activate','reset','invite','register')

- ForeignKeyConstraint (unnamed): organization_id, inviter_id

- UniqueConstraint (unnamed): invitation_id

- ForeignKeyConstraint (unnamed): organization_id

- PrimaryKeyConstraint (unnamed): token_hash

## identity_deliveries

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `token_hash` | `VARCHAR(64)` | False | False | identity_challenges.token_hash |
| `payload` | `JSONB` | False | False | — |
| `status` | `VARCHAR(20)` | False | False | — |
| `attempts` | `INTEGER` | False | False | — |
| `available_at` | `DATETIME` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `error_code` | `VARCHAR(30)` | True | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): token_hash

## identity_refresh_tokens

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `token_hash` | `VARCHAR(64)` | False | True | — |
| `session_id` | `CHAR(32)` | False | False | identity_sessions.id |
| `used` | `BOOLEAN` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): session_id

- PrimaryKeyConstraint (unnamed): token_hash

## identity_sessions

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id, identity_users.id |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id |
| `csrf_hash` | `VARCHAR(64)` | False | False | — |
| `expires_at` | `DATETIME` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `revoked` | `BOOLEAN` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): user_id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, user_id

- Index ix_identity_sessions_user_id: identity_sessions.user_id

## identity_users

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `email` | `VARCHAR(254)` | False | False | — |
| `name` | `VARCHAR(120)` | False | False | — |
| `password_hash` | `VARCHAR(128)` | True | False | — |
| `verified` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): email

## ingestion_sources

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | job_integrations.organization_id, ppm_work_items.organization_id, job_integrations.organization_id, organizations.id, ppm_sprints.organization_id, durable_jobs.organization_id |
| `integration_id` | `CHAR(32)` | False | False | job_integrations.id, job_integrations.id |
| `project_id` | `CHAR(32)` | False | False | ppm_work_items.project_id, job_integrations.project_id, ppm_sprints.project_id |
| `work_item_id` | `CHAR(32)` | True | False | ppm_work_items.id |
| `sprint_id` | `CHAR(32)` | True | False | ppm_sprints.id |
| `external_id` | `VARCHAR(160)` | False | False | — |
| `source_updated_at` | `DATETIME` | True | False | — |
| `source_observed_at` | `DATETIME` | False | False | — |
| `fingerprint` | `VARCHAR(64)` | False | False | — |
| `target_id` | `CHAR(32)` | False | False | — |
| `target_kind` | `VARCHAR(20)` | False | False | — |
| `target_revision` | `INTEGER` | False | False | — |
| `job_id` | `CHAR(32)` | False | False | durable_jobs.id |

Metadata check expressions: (target_kind='work_items' AND target_id=work_item_id AND work_item_id IS NOT NULL AND sprint_id IS NULL) OR (target_kind='sprints' AND target_id=sprint_id AND sprint_id IS NOT NULL AND work_item_id IS NULL)

- ForeignKeyConstraint (unnamed): organization_id, project_id, work_item_id

- UniqueConstraint (unnamed): integration_id, external_id

- ForeignKeyConstraint (unnamed): organization_id, project_id, integration_id

- ForeignKeyConstraint (unnamed): organization_id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, project_id, sprint_id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, job_id

- ForeignKeyConstraint (unnamed): organization_id, integration_id

## job_events

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | durable_jobs.organization_id, organizations.id |
| `job_id` | `CHAR(32)` | False | False | durable_jobs.id |
| `sequence` | `INTEGER` | False | False | — |
| `stage` | `VARCHAR(40)` | False | False | — |
| `occurred_at` | `DATETIME` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): organization_id, job_id

- ForeignKeyConstraint (unnamed): organization_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): job_id, sequence

- UniqueConstraint (unnamed): organization_id, id

## job_integrations

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, memberships.organization_id, ppm_projects.organization_id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `session_id` | `CHAR(32)` | False | False | identity_sessions.id |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `config` | `JSONB` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `enabled` | `BOOLEAN` | False | False | — |
| `cursor` | `VARCHAR(200)` | True | False | — |
| `updated_at` | `DATETIME` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): session_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- ForeignKeyConstraint (unnamed): organization_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, actor_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

## job_outbox

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, durable_jobs.organization_id |
| `job_id` | `CHAR(32)` | False | False | durable_jobs.id |
| `envelope` | `JSONB` | False | False | — |
| `dispatched_at` | `DATETIME` | True | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): organization_id, job_id

- ForeignKeyConstraint (unnamed): organization_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): job_id

- UniqueConstraint (unnamed): organization_id, id

## memberships

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `organization_id` | `CHAR(32)` | False | True | organizations.id |
| `user_id` | `CHAR(32)` | False | True | identity_users.id |
| `role` | `VARCHAR(20)` | False | False | — |
| `active` | `BOOLEAN` | False | False | — |
| `revision` | `INTEGER` | False | False | — |

Metadata check expressions: role IN ('Admin','Project Manager','Viewer')

- PrimaryKeyConstraint (unnamed): organization_id, user_id

- ForeignKeyConstraint (unnamed): user_id

- ForeignKeyConstraint (unnamed): organization_id

## notification_preferences

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `organization_id` | `CHAR(32)` | False | True | memberships.organization_id |
| `user_id` | `CHAR(32)` | False | True | memberships.user_id |
| `enabled` | `BOOLEAN` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- PrimaryKeyConstraint (unnamed): organization_id, user_id

- ForeignKeyConstraint (unnamed): organization_id, user_id

## organizations

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `name` | `VARCHAR(120)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `revision` | `INTEGER` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- PrimaryKeyConstraint (unnamed): id

## personal_notifications

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `kind` | `VARCHAR(30)` | False | False | — |
| `target_id` | `CHAR(32)` | False | False | — |
| `event_key` | `VARCHAR(160)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `read` | `BOOLEAN` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, user_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, user_id, event_key

## ppm_alignments

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_portfolios.organization_id, ppm_projects.organization_id, ppm_goals.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | True | False | ppm_projects.id |
| `portfolio_id` | `CHAR(32)` | True | False | ppm_portfolios.id |
| `goal_id` | `CHAR(32)` | False | False | ppm_goals.id |
| `weight` | `NUMERIC(6, 5)` | False | False | — |
| `contribution` | `NUMERIC(6, 5)` | False | False | — |

Metadata check expressions: (project_id IS NULL) <> (portfolio_id IS NULL); weight >= 0 AND weight <= 1 AND contribution >= 0 AND contribution <= 1; revision > 0

- ForeignKeyConstraint (unnamed): organization_id, portfolio_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, goal_id

- Index ix_ppm_alignments_org: ppm_alignments.organization_id

## ppm_allocations

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_projects.organization_id, ppm_resources.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `hours_per_day` | `NUMERIC(4, 2)` | False | False | — |

Metadata check expressions: revision > 0; end_date > start_date; hours_per_day >= 0 AND hours_per_day <= 24

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- Index ix_ppm_allocations_org: ppm_allocations.organization_id

## ppm_answers

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_assessments.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `assessment_id` | `CHAR(32)` | False | False | ppm_assessments.id |
| `question_id` | `CHAR(32)` | False | False | — |
| `value` | `TEXT` | True | False | — |
| `evidence_text` | `TEXT` | False | False | — |
| `reviewer_score` | `NUMERIC(7, 4)` | True | False | — |
| `reviewer_note` | `TEXT` | True | False | — |

Metadata check expressions: reviewer_score IS NULL OR (reviewer_score >= 0 AND reviewer_score <= 100)

- ForeignKeyConstraint (unnamed): organization_id, assessment_id

- UniqueConstraint (unnamed): organization_id, id

- UniqueConstraint (unnamed): organization_id, assessment_id, question_id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_answers_org: ppm_answers.organization_id

## ppm_assessment_access

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_frameworks.organization_id, memberships.organization_id, ppm_assessments.organization_id, organizations.id |
| `created_at` | `DATETIME` | False | False | — |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `framework_id` | `CHAR(32)` | True | False | ppm_frameworks.id |
| `assessment_id` | `CHAR(32)` | True | False | ppm_assessments.id |
| `active` | `BOOLEAN` | False | False | — |

Metadata check expressions: (framework_id IS NULL) <> (assessment_id IS NULL)

- UniqueConstraint (unnamed): organization_id, id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, framework_id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, assessment_id

- ForeignKeyConstraint (unnamed): organization_id, user_id

- Index ix_ppm_assessment_access_org: ppm_assessment_access.organization_id

## ppm_assessment_events

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_assessments.organization_id, memberships.organization_id, organizations.id |
| `created_at` | `DATETIME` | False | False | — |
| `assessment_id` | `CHAR(32)` | False | False | ppm_assessments.id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `event` | `VARCHAR(30)` | False | False | — |
| `note` | `TEXT` | False | False | — |
| `details` | `JSONB` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- UniqueConstraint (unnamed): organization_id, id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, assessment_id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, actor_id

- Index ix_ppm_assessment_events_org: ppm_assessment_events.organization_id

## ppm_assessment_requests

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id |
| `created_at` | `DATETIME` | False | False | — |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `key` | `CHAR(32)` | False | False | — |
| `fingerprint` | `VARCHAR(64)` | False | False | — |
| `response` | `JSONB` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- UniqueConstraint (unnamed): organization_id, id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, user_id, key

- ForeignKeyConstraint (unnamed): organization_id, user_id

- Index ix_ppm_assessment_requests_org: ppm_assessment_requests.organization_id

## ppm_assessments

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, memberships.organization_id, ppm_departments.organization_id, organizations.id, ppm_framework_versions.organization_id, memberships.organization_id, ppm_teams.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `framework_version_id` | `CHAR(32)` | False | False | ppm_framework_versions.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `department_id` | `CHAR(32)` | True | False | ppm_departments.id |
| `team_id` | `CHAR(32)` | True | False | ppm_teams.id |
| `assigned_to` | `CHAR(32)` | False | False | memberships.user_id |
| `reviewer_id` | `CHAR(32)` | False | False | memberships.user_id |
| `submitted_by` | `CHAR(32)` | True | False | memberships.user_id |
| `status` | `VARCHAR(20)` | False | False | — |
| `results` | `JSONB` | True | False | — |
| `revision` | `INTEGER` | False | False | — |

Metadata check expressions: revision > 0; status IN ('draft','submitted','in_review','returned','completed'); assigned_to <> reviewer_id

- UniqueConstraint (unnamed): organization_id, id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, framework_version_id

- ForeignKeyConstraint (unnamed): organization_id, reviewer_id

- ForeignKeyConstraint (unnamed): organization_id, team_id

- ForeignKeyConstraint (unnamed): organization_id, submitted_by

- ForeignKeyConstraint (unnamed): organization_id, assigned_to

- ForeignKeyConstraint (unnamed): organization_id, department_id

- Index ix_ppm_assessments_org: ppm_assessments.organization_id

## ppm_audit

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_projects.organization_id, memberships.organization_id |
| `project_id` | `CHAR(32)` | True | False | ppm_projects.id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `resource` | `VARCHAR(30)` | False | False | — |
| `target_id` | `CHAR(32)` | False | False | — |
| `before` | `JSONB` | True | False | — |
| `after` | `JSONB` | False | False | — |
| `request_id` | `CHAR(32)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): organization_id, actor_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- PrimaryKeyConstraint (unnamed): id

## ppm_availability

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_resources.organization_id, ppm_calendars.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `calendar_id` | `CHAR(32)` | False | False | ppm_calendars.id |

Metadata check expressions: revision > 0; end_date > start_date

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, calendar_id

- Index ix_ppm_availability_org: ppm_availability.organization_id

## ppm_baselines

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `version` | `INTEGER` | False | False | — |
| `snapshot` | `JSONB` | False | False | — |

Metadata check expressions: revision > 0

- UniqueConstraint (unnamed): organization_id, project_id, id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, project_id, version

- ForeignKeyConstraint (unnamed): organization_id, project_id

- Index ix_ppm_baselines_org: ppm_baselines.organization_id

## ppm_benefits

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_projects.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `unit` | `VARCHAR(40)` | False | False | — |
| `target` | `NUMERIC(18, 2)` | False | False | — |
| `realized` | `NUMERIC(18, 2)` | True | False | — |
| `period_start` | `DATE` | False | False | — |
| `period_end` | `DATE` | False | False | — |

Metadata check expressions: revision > 0; period_end > period_start

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- Index ix_ppm_benefits_org: ppm_benefits.organization_id

## ppm_blockers

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_work_items.organization_id, ppm_projects.organization_id, organizations.id, memberships.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id, ppm_work_items.project_id |
| `work_item_id` | `CHAR(32)` | True | False | ppm_work_items.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |
| `status` | `VARCHAR(10)` | False | False | — |

Metadata check expressions: status IN ('open','resolved'); revision > 0

- UniqueConstraint (unnamed): organization_id, project_id, id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, project_id, work_item_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- PrimaryKeyConstraint (unnamed): id

- Index ix_ppm_blockers_org: ppm_blockers.organization_id

## ppm_budget_lines

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `amount` | `NUMERIC(18, 2)` | False | False | — |
| `currency` | `VARCHAR(3)` | False | False | — |
| `approved` | `BOOLEAN` | False | False | — |

Metadata check expressions: amount >= 0; revision > 0

- ForeignKeyConstraint (unnamed): organization_id, project_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- Index ix_ppm_budget_lines_org: ppm_budget_lines.organization_id

## ppm_calendars

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `timezone` | `VARCHAR(80)` | False | False | — |
| `holidays` | `TEXT` | False | False | — |
| `monday` | `NUMERIC(4, 2)` | False | False | — |
| `tuesday` | `NUMERIC(4, 2)` | False | False | — |
| `wednesday` | `NUMERIC(4, 2)` | False | False | — |
| `thursday` | `NUMERIC(4, 2)` | False | False | — |
| `friday` | `NUMERIC(4, 2)` | False | False | — |
| `saturday` | `NUMERIC(4, 2)` | False | False | — |
| `sunday` | `NUMERIC(4, 2)` | False | False | — |

Metadata check expressions: wednesday >= 0 AND wednesday <= 24; sunday >= 0 AND sunday <= 24; monday >= 0 AND monday <= 24; thursday >= 0 AND thursday <= 24; friday >= 0 AND friday <= 24; tuesday >= 0 AND tuesday <= 24; saturday >= 0 AND saturday <= 24; revision > 0

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_calendars_org: ppm_calendars.organization_id

## ppm_capacity_snapshots

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_resources.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `snapshot` | `JSONB` | False | False | — |

Metadata check expressions: revision > 0; end_date > start_date

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- Index ix_ppm_capacity_snapshots_org: ppm_capacity_snapshots.organization_id

## ppm_departments

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, memberships.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

Metadata check expressions: revision > 0

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_departments_org: ppm_departments.organization_id

## ppm_dependencies

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_projects.organization_id, ppm_milestones.organization_id, ppm_milestones.organization_id, organizations.id, ppm_projects.organization_id, ppm_work_items.organization_id, ppm_work_items.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_milestones.project_id, ppm_work_items.project_id, ppm_projects.id |
| `target_project_id` | `CHAR(32)` | False | False | ppm_projects.id, ppm_milestones.project_id, ppm_work_items.project_id |
| `source_milestone_id` | `CHAR(32)` | True | False | ppm_milestones.id |
| `source_work_item_id` | `CHAR(32)` | True | False | ppm_work_items.id |
| `target_milestone_id` | `CHAR(32)` | True | False | ppm_milestones.id |
| `target_work_item_id` | `CHAR(32)` | True | False | ppm_work_items.id |

Metadata check expressions: source_milestone_id IS NULL OR source_work_item_id IS NULL; target_milestone_id IS NULL OR target_work_item_id IS NULL; revision > 0

- ForeignKeyConstraint (unnamed): organization_id, target_project_id, target_milestone_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- UniqueConstraint (unnamed): organization_id, project_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, target_project_id

- ForeignKeyConstraint (unnamed): organization_id, project_id, source_work_item_id

- ForeignKeyConstraint (unnamed): organization_id, target_project_id, target_work_item_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- ForeignKeyConstraint (unnamed): organization_id, project_id, source_milestone_id

- Index ix_ppm_dependencies_org: ppm_dependencies.organization_id

## ppm_effort

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id, ppm_resources.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `worked_on` | `DATE` | False | False | — |
| `hours` | `NUMERIC(4, 2)` | False | False | — |
| `overtime_hours` | `NUMERIC(4, 2)` | False | False | — |

Metadata check expressions: overtime_hours >= 0 AND overtime_hours <= hours; revision > 0; hours >= 0 AND hours <= 24

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- PrimaryKeyConstraint (unnamed): id

- Index ix_ppm_effort_org: ppm_effort.organization_id

## ppm_effort_coverage

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_resources.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `worked_on` | `DATE` | False | False | — |
| `complete` | `BOOLEAN` | False | False | — |

Metadata check expressions: revision > 0

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- UniqueConstraint (unnamed): organization_id, resource_id, worked_on

- Index ix_ppm_effort_coverage_org: ppm_effort_coverage.organization_id

## ppm_evidence_attachments

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_assessments.organization_id, organizations.id, memberships.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `assessment_id` | `CHAR(32)` | False | False | ppm_assessments.id |
| `question_id` | `CHAR(32)` | False | False | — |
| `file_name` | `VARCHAR(160)` | False | False | — |
| `file_size` | `INTEGER` | False | False | — |
| `sha256` | `VARCHAR(64)` | False | False | — |
| `released` | `BOOLEAN` | False | False | — |
| `storage_path` | `TEXT` | False | False | — |
| `uploaded_by` | `CHAR(32)` | False | False | memberships.user_id |

Metadata check expressions: file_size > 0 AND file_size <= 524288

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, uploaded_by

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, assessment_id

- Index ix_ppm_evidence_attachments_org: ppm_evidence_attachments.organization_id

## ppm_expenditures

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_expenditures.organization_id, organizations.id, ppm_projects.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id, ppm_expenditures.project_id |
| `amount` | `NUMERIC(18, 2)` | False | False | — |
| `currency` | `VARCHAR(3)` | False | False | — |
| `spent_on` | `DATE` | False | False | — |
| `reversal_of` | `CHAR(32)` | True | False | ppm_expenditures.id |

Metadata check expressions: (amount >= 0 AND reversal_of IS NULL) OR (amount < 0 AND reversal_of IS NOT NULL); revision > 0

- UniqueConstraint (unnamed): organization_id, project_id, id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- UniqueConstraint (unnamed): organization_id, reversal_of

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- ForeignKeyConstraint (unnamed): organization_id, project_id, reversal_of

- Index ix_ppm_expenditures_org: ppm_expenditures.organization_id

## ppm_framework_versions

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_frameworks.organization_id, memberships.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `framework_id` | `CHAR(32)` | False | False | ppm_frameworks.id |
| `version` | `INTEGER` | False | False | — |
| `snapshot` | `JSONB` | False | False | — |
| `published_by` | `CHAR(32)` | False | False | memberships.user_id |

Metadata check expressions: version > 0

- ForeignKeyConstraint (unnamed): organization_id, published_by

- ForeignKeyConstraint (unnamed): organization_id, framework_id

- UniqueConstraint (unnamed): organization_id, id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, framework_id, version

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_framework_versions_org: ppm_framework_versions.organization_id

## ppm_frameworks

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id |
| `created_at` | `DATETIME` | False | False | — |
| `definition` | `JSONB` | False | False | — |
| `revision` | `INTEGER` | False | False | — |

Metadata check expressions: revision > 0

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, id

- PrimaryKeyConstraint (unnamed): id

- Index ix_ppm_frameworks_org: ppm_frameworks.organization_id

## ppm_goals

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, memberships.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

Metadata check expressions: revision > 0

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- PrimaryKeyConstraint (unnamed): id

- Index ix_ppm_goals_org: ppm_goals.organization_id

## ppm_grants

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id, memberships.organization_id, ppm_portfolios.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `project_id` | `CHAR(32)` | True | False | ppm_projects.id |
| `portfolio_id` | `CHAR(32)` | True | False | ppm_portfolios.id |
| `access` | `VARCHAR(10)` | False | False | — |

Metadata check expressions: revision > 0; (project_id IS NULL) <> (portfolio_id IS NULL); access IN ('read','edit','manage')

- UniqueConstraint (unnamed): organization_id, user_id, project_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- ForeignKeyConstraint (unnamed): organization_id, portfolio_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, user_id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, user_id, portfolio_id

- Index ix_ppm_grants_org: ppm_grants.organization_id

## ppm_metric_plans

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_baselines.organization_id, ppm_calendars.organization_id, ppm_projects.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id, ppm_baselines.project_id |
| `baseline_id` | `CHAR(32)` | False | False | ppm_baselines.id |
| `calendar_id` | `CHAR(32)` | False | False | ppm_calendars.id |
| `forecast_cost` | `NUMERIC(18, 2)` | True | False | — |

Metadata check expressions: revision > 0; forecast_cost IS NULL OR forecast_cost >= 0

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, project_id, baseline_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- ForeignKeyConstraint (unnamed): organization_id, calendar_id

- UniqueConstraint (unnamed): organization_id, project_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- Index ix_ppm_metric_plans_org: ppm_metric_plans.organization_id

## ppm_metric_policies

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `amber` | `NUMERIC(5, 2)` | False | False | — |
| `red` | `NUMERIC(5, 2)` | False | False | — |
| `stale_days` | `INTEGER` | False | False | — |

Metadata check expressions: revision > 0; amber > 0 AND red > amber AND red <= 100; stale_days BETWEEN 1 AND 365

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id

- PrimaryKeyConstraint (unnamed): id

- Index ix_ppm_metric_policies_org: ppm_metric_policies.organization_id

## ppm_milestones

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_projects.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `due_date` | `DATE` | False | False | — |
| `actual_date` | `DATE` | True | False | — |
| `critical` | `BOOLEAN` | False | False | — |

Metadata check expressions: revision > 0

- UniqueConstraint (unnamed): organization_id, project_id, id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- Index ix_ppm_milestones_org: ppm_milestones.organization_id

## ppm_portfolios

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, memberships.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

Metadata check expressions: revision > 0

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_portfolios_org: ppm_portfolios.organization_id

## ppm_programs

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_portfolios.organization_id, memberships.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `portfolio_id` | `CHAR(32)` | False | False | ppm_portfolios.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

Metadata check expressions: revision > 0

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, portfolio_id

- UniqueConstraint (unnamed): organization_id, portfolio_id, id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- Index ix_ppm_programs_org: ppm_programs.organization_id

## ppm_projects

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, ppm_portfolios.organization_id, ppm_departments.organization_id, organizations.id, memberships.organization_id, ppm_programs.organization_id, ppm_teams.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `priority` | `VARCHAR(30)` | True | False | — |
| `industry` | `VARCHAR(30)` | True | False | — |
| `category` | `VARCHAR(30)` | True | False | — |
| `methodology` | `VARCHAR(30)` | True | False | — |
| `size_band` | `VARCHAR(30)` | True | False | — |
| `portfolio_id` | `CHAR(32)` | False | False | ppm_programs.portfolio_id, ppm_portfolios.id |
| `program_id` | `CHAR(32)` | True | False | ppm_programs.id |
| `department_id` | `CHAR(32)` | True | False | ppm_departments.id |
| `team_id` | `CHAR(32)` | True | False | ppm_teams.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |
| `created_by` | `CHAR(32)` | False | False | memberships.user_id |
| `status` | `VARCHAR(20)` | False | False | — |
| `reported_health` | `VARCHAR(10)` | False | False | — |
| `currency` | `VARCHAR(3)` | False | False | — |
| `ledger_complete` | `BOOLEAN` | False | False | — |
| `start_date` | `DATE` | True | False | — |
| `target_end_date` | `DATE` | True | False | — |
| `forecast_end_date` | `DATE` | True | False | — |
| `actual_start_date` | `DATE` | True | False | — |
| `actual_end_date` | `DATE` | True | False | — |

Metadata check expressions: category IS NULL OR category IN ('delivery','transformation','compliance','research','other'); reported_health IN ('Green','Amber','Red','Unknown'); revision > 0; priority IS NULL OR priority IN ('low','normal','high','urgent'); methodology IS NULL OR methodology IN ('agile','waterfall','hybrid','other'); target_end_date IS NULL OR start_date IS NULL OR target_end_date >= start_date; size_band IS NULL OR size_band IN ('small','medium','large'); industry IS NULL OR industry IN ('fintech','technology','healthcare','public_sector','other'); status IN ('draft','active','on_hold','completed','cancelled')

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, created_by

- ForeignKeyConstraint (unnamed): organization_id, portfolio_id, program_id

- ForeignKeyConstraint (unnamed): organization_id, team_id

- ForeignKeyConstraint (unnamed): organization_id, portfolio_id

- ForeignKeyConstraint (unnamed): organization_id, department_id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- Index ix_ppm_projects_org: ppm_projects.organization_id

## ppm_requests

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `organization_id` | `CHAR(32)` | False | True | memberships.organization_id |
| `user_id` | `CHAR(32)` | False | True | memberships.user_id |
| `key` | `CHAR(32)` | False | True | — |
| `fingerprint` | `VARCHAR(64)` | False | False | — |
| `resource` | `VARCHAR(30)` | False | False | — |
| `target_id` | `CHAR(32)` | False | False | — |

Metadata check expressions: See referential/primary/unique definitions and migrations

- ForeignKeyConstraint (unnamed): organization_id, user_id

- PrimaryKeyConstraint (unnamed): organization_id, user_id, key

## ppm_resource_access

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, memberships.organization_id, ppm_resources.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `manage` | `BOOLEAN` | False | False | — |
| `effort` | `BOOLEAN` | False | False | — |

Metadata check expressions: revision > 0

- ForeignKeyConstraint (unnamed): organization_id, user_id

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- UniqueConstraint (unnamed): organization_id, resource_id, user_id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_resource_access_org: ppm_resource_access.organization_id

## ppm_resource_skills

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_resources.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `skill` | `VARCHAR(80)` | False | False | — |

Metadata check expressions: revision > 0

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_resource_skills_org: ppm_resource_skills.organization_id

## ppm_resource_teams

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_teams.organization_id, organizations.id, ppm_resources.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `team_id` | `CHAR(32)` | False | False | ppm_teams.id |

Metadata check expressions: revision > 0; end_date > start_date

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, team_id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_resource_teams_org: ppm_resource_teams.organization_id

## ppm_resources

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `user_id` | `CHAR(32)` | True | False | memberships.user_id |

Metadata check expressions: revision > 0

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, user_id

- PrimaryKeyConstraint (unnamed): id

- Index ix_ppm_resources_org: ppm_resources.organization_id

## ppm_risks

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id, memberships.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |
| `severity` | `INTEGER` | False | False | — |
| `likelihood` | `INTEGER` | False | False | — |
| `mitigation` | `TEXT` | False | False | — |
| `status` | `VARCHAR(20)` | False | False | — |
| `review_on` | `DATE` | False | False | — |
| `resolution` | `TEXT` | False | False | — |

Metadata check expressions: severity BETWEEN 1 AND 5 AND likelihood BETWEEN 1 AND 5; status IN ('open','mitigating','accepted','closed'); revision > 0

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- Index ix_ppm_risks_org: ppm_risks.organization_id

## ppm_saved_views

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_portfolios.organization_id, memberships.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `portfolio_id` | `CHAR(32)` | True | False | ppm_portfolios.id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `dashboard` | `VARCHAR(20)` | False | False | — |

Metadata check expressions: dashboard IN ('Executive','Delivery','Risk','Resource'); revision > 0; end_date > start_date AND end_date - start_date <= 366

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, portfolio_id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, user_id

- Index ix_ppm_saved_views_org: ppm_saved_views.organization_id

## ppm_settings

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `timezone` | `VARCHAR(80)` | False | False | — |
| `currency` | `VARCHAR(3)` | False | False | — |

Metadata check expressions: revision > 0

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id

- Index ix_ppm_settings_org: ppm_settings.organization_id

## ppm_sprint_closures

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_teams.organization_id, organizations.id, ppm_projects.organization_id, ppm_sprints.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id, ppm_sprints.project_id |
| `sprint_id` | `CHAR(32)` | False | False | ppm_sprints.id |
| `team_id` | `CHAR(32)` | False | False | ppm_teams.id |
| `end_date` | `DATE` | False | False | — |
| `points` | `NUMERIC(18, 2)` | False | False | — |
| `complete` | `BOOLEAN` | False | False | — |
| `snapshot` | `JSONB` | False | False | — |

Metadata check expressions: revision > 0

- ForeignKeyConstraint (unnamed): organization_id, project_id, sprint_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, team_id

- ForeignKeyConstraint (unnamed): organization_id

- UniqueConstraint (unnamed): organization_id, sprint_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- Index ix_ppm_sprint_closures_org: ppm_sprint_closures.organization_id

## ppm_sprints

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_teams.organization_id, ppm_projects.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `team_id` | `CHAR(32)` | False | False | ppm_teams.id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `status` | `VARCHAR(12)` | False | False | — |

Metadata check expressions: status IN ('planned','active','closed'); revision > 0; end_date >= start_date

- UniqueConstraint (unnamed): organization_id, project_id, id

- PrimaryKeyConstraint (unnamed): id

- ForeignKeyConstraint (unnamed): organization_id, team_id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- Index ix_ppm_sprints_org: ppm_sprints.organization_id

## ppm_status_updates

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_projects.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `reported_health` | `VARCHAR(10)` | False | False | — |

Metadata check expressions: reported_health IN ('Green','Amber','Red','Unknown'); revision > 0

- ForeignKeyConstraint (unnamed): organization_id, project_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_status_updates_org: ppm_status_updates.organization_id

## ppm_team_members

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, memberships.organization_id, ppm_teams.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `team_id` | `CHAR(32)` | False | False | ppm_teams.id |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | True | False | — |

Metadata check expressions: revision > 0; end_date IS NULL OR end_date > start_date

- ForeignKeyConstraint (unnamed): organization_id, user_id

- ForeignKeyConstraint (unnamed): organization_id, team_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_team_members_org: ppm_team_members.organization_id

## ppm_teams

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, ppm_departments.organization_id, organizations.id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `department_id` | `CHAR(32)` | True | False | ppm_departments.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

Metadata check expressions: revision > 0

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, department_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- Index ix_ppm_teams_org: ppm_teams.organization_id

## ppm_time_off

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_resources.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `resource_id` | `CHAR(32)` | False | False | ppm_resources.id |
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `hours_per_day` | `NUMERIC(4, 2)` | False | False | — |

Metadata check expressions: hours_per_day >= 0 AND hours_per_day <= 24; revision > 0; end_date > start_date

- ForeignKeyConstraint (unnamed): organization_id, resource_id

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id

- Index ix_ppm_time_off_org: ppm_time_off.organization_id

## ppm_work_items

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ppm_projects.organization_id, memberships.organization_id, organizations.id, ppm_sprints.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `priority` | `VARCHAR(30)` | True | False | — |
| `work_type` | `VARCHAR(30)` | True | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_sprints.project_id, ppm_projects.id |
| `sprint_id` | `CHAR(32)` | True | False | ppm_sprints.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |
| `status` | `VARCHAR(12)` | False | False | — |
| `blocked` | `BOOLEAN` | False | False | — |
| `points` | `NUMERIC(10, 2)` | True | False | — |
| `start_date` | `DATE` | True | False | — |
| `due_date` | `DATE` | True | False | — |

Metadata check expressions: work_type IS NULL OR work_type IN ('task','bug','story','feature','other'); points IS NULL OR points >= 0; due_date IS NULL OR start_date IS NULL OR due_date >= start_date; revision > 0; priority IS NULL OR priority IN ('low','normal','high','urgent'); status IN ('backlog','ready','in_progress','done')

- PrimaryKeyConstraint (unnamed): id

- UniqueConstraint (unnamed): organization_id, id

- ForeignKeyConstraint (unnamed): organization_id, owner_id

- ForeignKeyConstraint (unnamed): organization_id

- ForeignKeyConstraint (unnamed): organization_id, project_id, sprint_id

- UniqueConstraint (unnamed): organization_id, project_id, id

- ForeignKeyConstraint (unnamed): organization_id, project_id

- Index ix_ppm_work_items_org: ppm_work_items.organization_id
