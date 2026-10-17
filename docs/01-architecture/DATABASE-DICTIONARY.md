# Current source-derived database dictionary

Generated from SQLAlchemy `Base.metadata` without a database connection. Source chain ends at `0012_ai_runtime`; the normal local applied head is independently recorded in the [Sprint 10 handoff](../03-sprints/completed/sprint-10/HANDOFF.md). Run `python scripts/documentation_inventory.py --check` for drift. SQL-only RLS, triggers, privileges and security-definer functions require reading [the migrations](../../services/api/migrations/versions) and [document contract](../contracts/documents.md); metadata is not a complete policy inventory.

## Important data flows

Live organization membership → transaction-local principal/RLS → scoped domain facts. Published assessment history remains immutable. `source_documents` owns scope/retention; `source_versions` owns immutable byte identity and mutable processing status; `source_chunks` is replaceable derived text; `source_evidence_links` references separately authorized released attachments. `durable_jobs` references exactly one integration, document version or AI run according to job kind. AI run provenance/budgets, attempt accounting and rebuildable vectors follow the [AI contract](../contracts/ai.md). Originals remain private objects; logical deletion revokes reads, guarded purge removes bytes/text/links but retains tombstones. `ai_embeddings` stores the bounded exact JSONB projection; no pgvector/ANN or semantic-finding table is activated.

**Inventory:** 72 metadata tables (Alembic's runtime version table is separate).

## agent_analyses

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ai_runs.organization_id, memberships.organization_id, organizations.id, ppm_assessments.organization_id, ppm_projects.organization_id |
| `run_id` | `CHAR(32)` | False | False | ai_runs.id |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `assessment_id` | `CHAR(32)` | True | False | ppm_assessments.id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `snapshot` | `JSONB` | False | False | — |
| `output` | `JSONB` | True | False | — |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, actor_id
- ForeignKeyConstraint (unnamed): organization_id, assessment_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, run_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): run_id

## agent_reviews

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | agent_analyses.organization_id, memberships.organization_id, organizations.id |
| `analysis_id` | `CHAR(32)` | False | False | agent_analyses.id |
| `item_key` | `VARCHAR(96)` | False | False | — |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `decision` | `VARCHAR(16)` | False | False | — |
| `reason` | `VARCHAR(1000)` | False | False | — |
| `approved_score` | `NUMERIC(7, 4)` | True | False | — |
| `revision` | `INTEGER` | False | False | — |
| `key` | `CHAR(32)` | False | False | — |
| `fingerprint` | `VARCHAR(64)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

- CheckConstraint (unnamed): approved_score IS NULL OR approved_score BETWEEN 0 AND 100
- CheckConstraint (unnamed): decision IN ('accepted','rejected')
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, actor_id
- ForeignKeyConstraint (unnamed): organization_id, analysis_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): analysis_id, item_key, revision
- UniqueConstraint (unnamed): organization_id, actor_id, key
- UniqueConstraint (unnamed): organization_id, id

## ai_budgets

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id |
| `limit_usd` | `NUMERIC(12, 6)` | False | False | — |
| `spent_usd` | `NUMERIC(12, 6)` | False | False | — |
| `reserved_usd` | `NUMERIC(12, 6)` | False | False | — |
| `concurrency` | `INTEGER` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `failures` | `INTEGER` | False | False | — |
| `circuit_until` | `DATETIME` | True | False | — |

- CheckConstraint (unnamed): concurrency BETWEEN 1 AND 4
- CheckConstraint (unnamed): limit_usd>=0 AND spent_usd>=0 AND reserved_usd>=0
- ForeignKeyConstraint (unnamed): organization_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id
- UniqueConstraint (unnamed): organization_id, id

## ai_calls

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ai_runs.organization_id, organizations.id |
| `run_id` | `CHAR(32)` | False | False | ai_runs.id |
| `operation` | `VARCHAR(24)` | False | False | — |
| `attempt` | `INTEGER` | False | False | — |
| `status` | `VARCHAR(16)` | False | False | — |
| `code` | `VARCHAR(48)` | True | False | — |
| `charged_usd` | `NUMERIC(12, 6)` | False | False | — |
| `input_tokens` | `INTEGER` | True | False | — |
| `output_tokens` | `INTEGER` | True | False | — |
| `latency_ms` | `INTEGER` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, run_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): run_id, operation, attempt

## ai_embeddings

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ai_runs.organization_id, organizations.id, source_chunks.organization_id |
| `chunk_id` | `CHAR(32)` | False | False | source_chunks.id |
| `source_sha256` | `VARCHAR(64)` | False | False | — |
| `text_sha256` | `VARCHAR(64)` | False | False | — |
| `model` | `VARCHAR(160)` | False | False | — |
| `chunk_version` | `VARCHAR(48)` | False | False | — |
| `vector` | `JSONB` | False | False | — |
| `run_id` | `CHAR(32)` | False | False | ai_runs.id |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, chunk_id
- ForeignKeyConstraint (unnamed): organization_id, run_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): chunk_id
- UniqueConstraint (unnamed): organization_id, id

## ai_runs

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_projects.organization_id |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `session_id` | `CHAR(32)` | False | False | identity_sessions.id |
| `snapshot` | `JSONB` | False | False | — |
| `input_sha256` | `VARCHAR(64)` | False | False | — |
| `versions` | `JSONB` | False | False | — |
| `evidence` | `JSONB` | False | False | — |
| `result` | `JSONB` | False | False | — |
| `diagnostic` | `VARCHAR(48)` | True | False | — |
| `limitations` | `JSONB` | False | False | — |
| `retrieval` | `VARCHAR(16)` | False | False | — |
| `reservation` | `NUMERIC(12, 6)` | False | False | — |
| `charged_usd` | `NUMERIC(12, 6)` | False | False | — |
| `settled` | `BOOLEAN` | False | False | — |
| `deadline` | `DATETIME` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

- CheckConstraint (unnamed): reservation>=0 AND charged_usd>=0 AND charged_usd<=reservation
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, actor_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): session_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id

## durable_jobs

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | ai_runs.organization_id, job_integrations.organization_id, memberships.organization_id, organizations.id, source_versions.organization_id |
| `integration_id` | `CHAR(32)` | True | False | job_integrations.id |
| `document_version_id` | `CHAR(32)` | True | False | source_versions.id |
| `ai_run_id` | `CHAR(32)` | True | False | ai_runs.id |
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

- CheckConstraint (ck_job_source_kind): num_nonnulls(integration_id,document_version_id,ai_run_id)=1
- CheckConstraint (unnamed): status IN ('queued','running','retry_wait','succeeded','partially_succeeded','failed','cancelled')
- ForeignKeyConstraint (fk_job_ai_run): organization_id, ai_run_id
- ForeignKeyConstraint (fk_job_document_version): organization_id, document_version_id
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, actor_id
- ForeignKeyConstraint (unnamed): organization_id, integration_id
- ForeignKeyConstraint (unnamed): session_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, actor_id, key
- UniqueConstraint (unnamed): organization_id, id

## foundation_state

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `INTEGER` | False | True | — |
| `instance_id` | `CHAR(32)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

- CheckConstraint (ck_foundation_singleton): id = 1
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

- ForeignKeyConstraint (unnamed): organization_id, actor_id
- PrimaryKeyConstraint (unnamed): id
- Index `ix_identity_audit_organization_id` (unique=False): identity_audit.organization_id

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

- CheckConstraint (ck_challenge_kind): kind IN ('activate','reset','invite','register')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, inviter_id
- PrimaryKeyConstraint (unnamed): token_hash
- UniqueConstraint (unnamed): invitation_id

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

- ForeignKeyConstraint (unnamed): token_hash
- PrimaryKeyConstraint (unnamed): id

## identity_refresh_tokens

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `token_hash` | `VARCHAR(64)` | False | True | — |
| `session_id` | `CHAR(32)` | False | False | identity_sessions.id |
| `used` | `BOOLEAN` | False | False | — |

- ForeignKeyConstraint (unnamed): session_id
- PrimaryKeyConstraint (unnamed): token_hash

## identity_sessions

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `user_id` | `CHAR(32)` | False | False | identity_users.id, memberships.user_id |
| `organization_id` | `CHAR(32)` | True | False | memberships.organization_id |
| `csrf_hash` | `VARCHAR(64)` | False | False | — |
| `expires_at` | `DATETIME` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `revoked` | `BOOLEAN` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id, user_id
- ForeignKeyConstraint (unnamed): user_id
- PrimaryKeyConstraint (unnamed): id
- Index `ix_identity_sessions_user_id` (unique=False): identity_sessions.user_id

## identity_users

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `email` | `VARCHAR(254)` | False | False | — |
| `name` | `VARCHAR(120)` | False | False | — |
| `password_hash` | `VARCHAR(128)` | True | False | — |
| `verified` | `BOOLEAN` | False | False | — |
| `active` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): email

## ingestion_sources

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | durable_jobs.organization_id, job_integrations.organization_id, job_integrations.organization_id, organizations.id, ppm_sprints.organization_id, ppm_work_items.organization_id |
| `integration_id` | `CHAR(32)` | False | False | job_integrations.id, job_integrations.id |
| `project_id` | `CHAR(32)` | False | False | job_integrations.project_id, ppm_sprints.project_id, ppm_work_items.project_id |
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

- CheckConstraint (unnamed): (target_kind='work_items' AND target_id=work_item_id AND work_item_id IS NOT NULL AND sprint_id IS NULL) OR (target_kind='sprints' AND target_id=sprint_id AND sprint_id IS NOT NULL AND work_item_id IS NULL)
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, integration_id
- ForeignKeyConstraint (unnamed): organization_id, job_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, integration_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, sprint_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, work_item_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): integration_id, external_id
- UniqueConstraint (unnamed): organization_id, id

## job_events

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | durable_jobs.organization_id, organizations.id |
| `job_id` | `CHAR(32)` | False | False | durable_jobs.id |
| `sequence` | `INTEGER` | False | False | — |
| `stage` | `VARCHAR(40)` | False | False | — |
| `occurred_at` | `DATETIME` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, job_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): job_id, sequence
- UniqueConstraint (unnamed): organization_id, id

## job_integrations

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_projects.organization_id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `session_id` | `CHAR(32)` | False | False | identity_sessions.id |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id |
| `config` | `JSONB` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `enabled` | `BOOLEAN` | False | False | — |
| `cursor` | `VARCHAR(200)` | True | False | — |
| `updated_at` | `DATETIME` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, actor_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): session_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id

## job_outbox

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | durable_jobs.organization_id, organizations.id |
| `job_id` | `CHAR(32)` | False | False | durable_jobs.id |
| `envelope` | `JSONB` | False | False | — |
| `dispatched_at` | `DATETIME` | True | False | — |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, job_id
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

- CheckConstraint (ck_membership_role): role IN ('Admin','Project Manager','Viewer')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): user_id
- PrimaryKeyConstraint (unnamed): organization_id, user_id

## notification_preferences

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `organization_id` | `CHAR(32)` | False | True | memberships.organization_id |
| `user_id` | `CHAR(32)` | False | True | memberships.user_id |
| `enabled` | `BOOLEAN` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): organization_id, user_id

## organizations

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `name` | `VARCHAR(120)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `description` | `VARCHAR(1000)` | True | False | — |
| `industry` | `VARCHAR(120)` | True | False | — |
| `website` | `VARCHAR(500)` | True | False | — |

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

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, user_id, event_key

## ppm_alignments

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_goals.organization_id, ppm_portfolios.organization_id, ppm_projects.organization_id |
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

- CheckConstraint (unnamed): (project_id IS NULL) <> (portfolio_id IS NULL)
- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): weight >= 0 AND weight <= 1 AND contribution >= 0 AND contribution <= 1
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, goal_id
- ForeignKeyConstraint (unnamed): organization_id, portfolio_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_alignments_org` (unique=False): ppm_alignments.organization_id

## ppm_allocations

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
| `start_date` | `DATE` | False | False | — |
| `end_date` | `DATE` | False | False | — |
| `hours_per_day` | `NUMERIC(4, 2)` | False | False | — |

- CheckConstraint (unnamed): end_date > start_date
- CheckConstraint (unnamed): hours_per_day >= 0 AND hours_per_day <= 24
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_allocations_org` (unique=False): ppm_allocations.organization_id

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

- CheckConstraint (unnamed): reviewer_score IS NULL OR (reviewer_score >= 0 AND reviewer_score <= 100)
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, assessment_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, assessment_id, question_id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_answers_org` (unique=False): ppm_answers.organization_id

## ppm_assessment_access

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_assessments.organization_id, ppm_frameworks.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `user_id` | `CHAR(32)` | False | False | memberships.user_id |
| `framework_id` | `CHAR(32)` | True | False | ppm_frameworks.id |
| `assessment_id` | `CHAR(32)` | True | False | ppm_assessments.id |
| `active` | `BOOLEAN` | False | False | — |

- CheckConstraint (unnamed): (framework_id IS NULL) <> (assessment_id IS NULL)
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, assessment_id
- ForeignKeyConstraint (unnamed): organization_id, framework_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_assessment_access_org` (unique=False): ppm_assessment_access.organization_id

## ppm_assessment_events

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_assessments.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `assessment_id` | `CHAR(32)` | False | False | ppm_assessments.id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `event` | `VARCHAR(30)` | False | False | — |
| `note` | `TEXT` | False | False | — |
| `details` | `JSONB` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, actor_id
- ForeignKeyConstraint (unnamed): organization_id, assessment_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_assessment_events_org` (unique=False): ppm_assessment_events.organization_id

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

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, user_id, key
- Index `ix_ppm_assessment_requests_org` (unique=False): ppm_assessment_requests.organization_id

## ppm_assessments

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, memberships.organization_id, memberships.organization_id, organizations.id, ppm_departments.organization_id, ppm_framework_versions.organization_id, ppm_teams.organization_id |
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

- CheckConstraint (unnamed): assigned_to <> reviewer_id
- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): status IN ('draft','submitted','in_review','returned','completed')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, assigned_to
- ForeignKeyConstraint (unnamed): organization_id, department_id
- ForeignKeyConstraint (unnamed): organization_id, framework_version_id
- ForeignKeyConstraint (unnamed): organization_id, reviewer_id
- ForeignKeyConstraint (unnamed): organization_id, submitted_by
- ForeignKeyConstraint (unnamed): organization_id, team_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_assessments_org` (unique=False): ppm_assessments.organization_id

## ppm_audit

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, ppm_projects.organization_id |
| `project_id` | `CHAR(32)` | True | False | ppm_projects.id |
| `actor_id` | `CHAR(32)` | False | False | memberships.user_id |
| `resource` | `VARCHAR(30)` | False | False | — |
| `target_id` | `CHAR(32)` | False | False | — |
| `before` | `JSONB` | True | False | — |
| `after` | `JSONB` | False | False | — |
| `request_id` | `CHAR(32)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id, actor_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id

## ppm_availability

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_calendars.organization_id, ppm_resources.organization_id |
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

- CheckConstraint (unnamed): end_date > start_date
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, calendar_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_availability_org` (unique=False): ppm_availability.organization_id

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

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- UniqueConstraint (unnamed): organization_id, project_id, version
- Index `ix_ppm_baselines_org` (unique=False): ppm_baselines.organization_id

## ppm_benefits

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
| `unit` | `VARCHAR(40)` | False | False | — |
| `target` | `NUMERIC(18, 2)` | False | False | — |
| `realized` | `NUMERIC(18, 2)` | True | False | — |
| `period_start` | `DATE` | False | False | — |
| `period_end` | `DATE` | False | False | — |

- CheckConstraint (unnamed): period_end > period_start
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_benefits_org` (unique=False): ppm_benefits.organization_id

## ppm_blockers

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_projects.organization_id, ppm_work_items.organization_id |
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

- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): status IN ('open','resolved')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, work_item_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_blockers_org` (unique=False): ppm_blockers.organization_id

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

- CheckConstraint (unnamed): amount >= 0
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_budget_lines_org` (unique=False): ppm_budget_lines.organization_id

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

- CheckConstraint (unnamed): friday >= 0 AND friday <= 24
- CheckConstraint (unnamed): monday >= 0 AND monday <= 24
- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): saturday >= 0 AND saturday <= 24
- CheckConstraint (unnamed): sunday >= 0 AND sunday <= 24
- CheckConstraint (unnamed): thursday >= 0 AND thursday <= 24
- CheckConstraint (unnamed): tuesday >= 0 AND tuesday <= 24
- CheckConstraint (unnamed): wednesday >= 0 AND wednesday <= 24
- ForeignKeyConstraint (unnamed): organization_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_calendars_org` (unique=False): ppm_calendars.organization_id

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

- CheckConstraint (unnamed): end_date > start_date
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_capacity_snapshots_org` (unique=False): ppm_capacity_snapshots.organization_id

## ppm_departments

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
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_departments_org` (unique=False): ppm_departments.organization_id

## ppm_dependencies

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_milestones.organization_id, ppm_milestones.organization_id, ppm_projects.organization_id, ppm_projects.organization_id, ppm_work_items.organization_id, ppm_work_items.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_milestones.project_id, ppm_projects.id, ppm_work_items.project_id |
| `target_project_id` | `CHAR(32)` | False | False | ppm_milestones.project_id, ppm_projects.id, ppm_work_items.project_id |
| `source_milestone_id` | `CHAR(32)` | True | False | ppm_milestones.id |
| `source_work_item_id` | `CHAR(32)` | True | False | ppm_work_items.id |
| `target_milestone_id` | `CHAR(32)` | True | False | ppm_milestones.id |
| `target_work_item_id` | `CHAR(32)` | True | False | ppm_work_items.id |

- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): source_milestone_id IS NULL OR source_work_item_id IS NULL
- CheckConstraint (unnamed): target_milestone_id IS NULL OR target_work_item_id IS NULL
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, source_milestone_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, source_work_item_id
- ForeignKeyConstraint (unnamed): organization_id, target_project_id
- ForeignKeyConstraint (unnamed): organization_id, target_project_id, target_milestone_id
- ForeignKeyConstraint (unnamed): organization_id, target_project_id, target_work_item_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_dependencies_org` (unique=False): ppm_dependencies.organization_id

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

- CheckConstraint (unnamed): hours >= 0 AND hours <= 24
- CheckConstraint (unnamed): overtime_hours >= 0 AND overtime_hours <= hours
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_effort_org` (unique=False): ppm_effort.organization_id

## ppm_effort_coverage

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
| `worked_on` | `DATE` | False | False | — |
| `complete` | `BOOLEAN` | False | False | — |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, resource_id, worked_on
- Index `ix_ppm_effort_coverage_org` (unique=False): ppm_effort_coverage.organization_id

## ppm_evidence_attachments

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_assessments.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `assessment_id` | `CHAR(32)` | False | False | ppm_assessments.id |
| `question_id` | `CHAR(32)` | False | False | — |
| `file_name` | `VARCHAR(160)` | False | False | — |
| `file_size` | `INTEGER` | False | False | — |
| `sha256` | `VARCHAR(64)` | False | False | — |
| `released` | `BOOLEAN` | False | False | — |
| `storage_path` | `TEXT` | False | False | — |
| `uploaded_by` | `CHAR(32)` | False | False | memberships.user_id |

- CheckConstraint (unnamed): file_size > 0 AND file_size <= 524288
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, assessment_id
- ForeignKeyConstraint (unnamed): organization_id, uploaded_by
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_evidence_attachments_org` (unique=False): ppm_evidence_attachments.organization_id

## ppm_expenditures

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_expenditures.organization_id, ppm_projects.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_expenditures.project_id, ppm_projects.id |
| `amount` | `NUMERIC(18, 2)` | False | False | — |
| `currency` | `VARCHAR(3)` | False | False | — |
| `spent_on` | `DATE` | False | False | — |
| `reversal_of` | `CHAR(32)` | True | False | ppm_expenditures.id |

- CheckConstraint (unnamed): (amount >= 0 AND reversal_of IS NULL) OR (amount < 0 AND reversal_of IS NOT NULL)
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, reversal_of
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- UniqueConstraint (unnamed): organization_id, reversal_of
- Index `ix_ppm_expenditures_org` (unique=False): ppm_expenditures.organization_id

## ppm_framework_versions

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_frameworks.organization_id |
| `created_at` | `DATETIME` | False | False | — |
| `framework_id` | `CHAR(32)` | False | False | ppm_frameworks.id |
| `version` | `INTEGER` | False | False | — |
| `snapshot` | `JSONB` | False | False | — |
| `published_by` | `CHAR(32)` | False | False | memberships.user_id |

- CheckConstraint (unnamed): version > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, framework_id
- ForeignKeyConstraint (unnamed): organization_id, published_by
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, framework_id, version
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_framework_versions_org` (unique=False): ppm_framework_versions.organization_id

## ppm_frameworks

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id |
| `created_at` | `DATETIME` | False | False | — |
| `definition` | `JSONB` | False | False | — |
| `revision` | `INTEGER` | False | False | — |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_frameworks_org` (unique=False): ppm_frameworks.organization_id

## ppm_goals

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
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_goals_org` (unique=False): ppm_goals.organization_id

## ppm_grants

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_portfolios.organization_id, ppm_projects.organization_id |
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

- CheckConstraint (unnamed): (project_id IS NULL) <> (portfolio_id IS NULL)
- CheckConstraint (unnamed): access IN ('read','edit','manage')
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, portfolio_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, user_id, portfolio_id
- UniqueConstraint (unnamed): organization_id, user_id, project_id
- Index `ix_ppm_grants_org` (unique=False): ppm_grants.organization_id

## ppm_metric_plans

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_baselines.organization_id, ppm_calendars.organization_id, ppm_projects.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_baselines.project_id, ppm_projects.id |
| `baseline_id` | `CHAR(32)` | False | False | ppm_baselines.id |
| `calendar_id` | `CHAR(32)` | False | False | ppm_calendars.id |
| `forecast_cost` | `NUMERIC(18, 2)` | True | False | — |

- CheckConstraint (unnamed): forecast_cost IS NULL OR forecast_cost >= 0
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, calendar_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, baseline_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_metric_plans_org` (unique=False): ppm_metric_plans.organization_id

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

- CheckConstraint (unnamed): amber > 0 AND red > amber AND red <= 100
- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): stale_days BETWEEN 1 AND 365
- ForeignKeyConstraint (unnamed): organization_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_metric_policies_org` (unique=False): ppm_metric_policies.organization_id

## ppm_milestones

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
| `due_date` | `DATE` | False | False | — |
| `actual_date` | `DATE` | True | False | — |
| `critical` | `BOOLEAN` | False | False | — |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_milestones_org` (unique=False): ppm_milestones.organization_id

## ppm_portfolios

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
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_portfolios_org` (unique=False): ppm_portfolios.organization_id

## ppm_programs

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_portfolios.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `portfolio_id` | `CHAR(32)` | False | False | ppm_portfolios.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- ForeignKeyConstraint (unnamed): organization_id, portfolio_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, portfolio_id, id
- Index `ix_ppm_programs_org` (unique=False): ppm_programs.organization_id

## ppm_projects

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, memberships.organization_id, organizations.id, ppm_departments.organization_id, ppm_portfolios.organization_id, ppm_programs.organization_id, ppm_teams.organization_id |
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
| `portfolio_id` | `CHAR(32)` | False | False | ppm_portfolios.id, ppm_programs.portfolio_id |
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

- CheckConstraint (ck_ppm_projects_category): category IS NULL OR category IN ('delivery','transformation','compliance','research','other')
- CheckConstraint (ck_ppm_projects_industry): industry IS NULL OR industry IN ('fintech','technology','healthcare','public_sector','other')
- CheckConstraint (ck_ppm_projects_methodology): methodology IS NULL OR methodology IN ('agile','waterfall','hybrid','other')
- CheckConstraint (ck_ppm_projects_priority): priority IS NULL OR priority IN ('low','normal','high','urgent')
- CheckConstraint (ck_ppm_projects_size_band): size_band IS NULL OR size_band IN ('small','medium','large')
- CheckConstraint (unnamed): reported_health IN ('Green','Amber','Red','Unknown')
- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): status IN ('draft','active','on_hold','completed','cancelled')
- CheckConstraint (unnamed): target_end_date IS NULL OR start_date IS NULL OR target_end_date >= start_date
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, created_by
- ForeignKeyConstraint (unnamed): organization_id, department_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- ForeignKeyConstraint (unnamed): organization_id, portfolio_id
- ForeignKeyConstraint (unnamed): organization_id, portfolio_id, program_id
- ForeignKeyConstraint (unnamed): organization_id, team_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_projects_org` (unique=False): ppm_projects.organization_id

## ppm_requests

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `organization_id` | `CHAR(32)` | False | True | memberships.organization_id |
| `user_id` | `CHAR(32)` | False | True | memberships.user_id |
| `key` | `CHAR(32)` | False | True | — |
| `fingerprint` | `VARCHAR(64)` | False | False | — |
| `resource` | `VARCHAR(30)` | False | False | — |
| `target_id` | `CHAR(32)` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): organization_id, user_id, key

## ppm_resource_access

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_resources.organization_id |
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

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, resource_id, user_id
- Index `ix_ppm_resource_access_org` (unique=False): ppm_resource_access.organization_id

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

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_resource_skills_org` (unique=False): ppm_resource_skills.organization_id

## ppm_resource_teams

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_resources.organization_id, ppm_teams.organization_id |
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

- CheckConstraint (unnamed): end_date > start_date
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- ForeignKeyConstraint (unnamed): organization_id, team_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_resource_teams_org` (unique=False): ppm_resource_teams.organization_id

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

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_resources_org` (unique=False): ppm_resources.organization_id

## ppm_risks

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_projects.organization_id |
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

- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): severity BETWEEN 1 AND 5 AND likelihood BETWEEN 1 AND 5
- CheckConstraint (unnamed): status IN ('open','mitigating','accepted','closed')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_risks_org` (unique=False): ppm_risks.organization_id

## ppm_saved_views

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_portfolios.organization_id |
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

- CheckConstraint (unnamed): dashboard IN ('Executive','Delivery','Risk','Resource')
- CheckConstraint (unnamed): end_date > start_date AND end_date - start_date <= 366
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, portfolio_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_saved_views_org` (unique=False): ppm_saved_views.organization_id

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

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_settings_org` (unique=False): ppm_settings.organization_id

## ppm_sprint_closures

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id, ppm_sprints.organization_id, ppm_teams.organization_id |
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

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, sprint_id
- ForeignKeyConstraint (unnamed): organization_id, team_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- UniqueConstraint (unnamed): organization_id, sprint_id
- Index `ix_ppm_sprint_closures_org` (unique=False): ppm_sprint_closures.organization_id

## ppm_sprints

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id, ppm_teams.organization_id |
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

- CheckConstraint (unnamed): end_date >= start_date
- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): status IN ('planned','active','closed')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, team_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_sprints_org` (unique=False): ppm_sprints.organization_id

## ppm_status_updates

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
| `reported_health` | `VARCHAR(10)` | False | False | — |

- CheckConstraint (unnamed): reported_health IN ('Green','Amber','Red','Unknown')
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_status_updates_org` (unique=False): ppm_status_updates.organization_id

## ppm_team_members

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_teams.organization_id |
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

- CheckConstraint (unnamed): end_date IS NULL OR end_date > start_date
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, team_id
- ForeignKeyConstraint (unnamed): organization_id, user_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_team_members_org` (unique=False): ppm_team_members.organization_id

## ppm_teams

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_departments.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `department_id` | `CHAR(32)` | True | False | ppm_departments.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |

- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, department_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_teams_org` (unique=False): ppm_teams.organization_id

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

- CheckConstraint (unnamed): end_date > start_date
- CheckConstraint (unnamed): hours_per_day >= 0 AND hours_per_day <= 24
- CheckConstraint (unnamed): revision > 0
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, resource_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- Index `ix_ppm_time_off_org` (unique=False): ppm_time_off.organization_id

## ppm_work_items

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, ppm_projects.organization_id, ppm_sprints.organization_id |
| `name` | `VARCHAR(160)` | False | False | — |
| `description` | `TEXT` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `archived` | `BOOLEAN` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `updated_at` | `DATETIME` | False | False | — |
| `priority` | `VARCHAR(30)` | True | False | — |
| `work_type` | `VARCHAR(30)` | True | False | — |
| `project_id` | `CHAR(32)` | False | False | ppm_projects.id, ppm_sprints.project_id |
| `sprint_id` | `CHAR(32)` | True | False | ppm_sprints.id |
| `owner_id` | `CHAR(32)` | True | False | memberships.user_id |
| `status` | `VARCHAR(12)` | False | False | — |
| `blocked` | `BOOLEAN` | False | False | — |
| `points` | `NUMERIC(10, 2)` | True | False | — |
| `start_date` | `DATE` | True | False | — |
| `due_date` | `DATE` | True | False | — |

- CheckConstraint (ck_ppm_work_items_priority): priority IS NULL OR priority IN ('low','normal','high','urgent')
- CheckConstraint (ck_ppm_work_items_work_type): work_type IS NULL OR work_type IN ('task','bug','story','feature','other')
- CheckConstraint (unnamed): due_date IS NULL OR start_date IS NULL OR due_date >= start_date
- CheckConstraint (unnamed): points IS NULL OR points >= 0
- CheckConstraint (unnamed): revision > 0
- CheckConstraint (unnamed): status IN ('backlog','ready','in_progress','done')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, owner_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- ForeignKeyConstraint (unnamed): organization_id, project_id, sprint_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): organization_id, project_id, id
- Index `ix_ppm_work_items_org` (unique=False): ppm_work_items.organization_id

## source_chunks

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, source_versions.organization_id |
| `version_id` | `CHAR(32)` | False | False | source_versions.id |
| `ordinal` | `INTEGER` | False | False | — |
| `location` | `VARCHAR(200)` | False | False | — |
| `text` | `TEXT` | False | False | — |
| `confidence` | `FLOAT` | True | False | — |
| `method` | `VARCHAR(24)` | False | False | — |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, version_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): version_id, ordinal

## source_documents

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_projects.organization_id |
| `project_id` | `CHAR(32)` | True | False | ppm_projects.id |
| `title` | `VARCHAR(160)` | False | False | — |
| `category` | `VARCHAR(24)` | False | False | — |
| `created_at` | `DATETIME` | False | False | — |
| `revision` | `INTEGER` | False | False | — |
| `deleted_at` | `DATETIME` | True | False | — |
| `legal_hold` | `BOOLEAN` | False | False | — |
| `retain_until` | `DATETIME` | False | False | — |
| `policy` | `JSONB` | True | False | — |

- CheckConstraint (unnamed): category IN ('SRS','BRD','PRD','MOM','sprint_report','risk_log','charter','policy')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, project_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id

## source_evidence_links

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | organizations.id, ppm_evidence_attachments.organization_id, source_versions.organization_id |
| `version_id` | `CHAR(32)` | False | False | source_versions.id |
| `attachment_id` | `CHAR(32)` | False | False | ppm_evidence_attachments.id |

- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, attachment_id
- ForeignKeyConstraint (unnamed): organization_id, version_id
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): organization_id, id
- UniqueConstraint (unnamed): version_id, attachment_id

## source_versions

| Column | SQL type | Nullable | Primary key | Foreign reference |
| --- | --- | --- | --- | --- |
| `id` | `CHAR(32)` | False | True | — |
| `organization_id` | `CHAR(32)` | False | False | memberships.organization_id, organizations.id, source_documents.organization_id |
| `document_id` | `CHAR(32)` | False | False | source_documents.id |
| `number` | `INTEGER` | False | False | — |
| `sha256` | `VARCHAR(64)` | False | False | — |
| `filename` | `VARCHAR(160)` | False | False | — |
| `size` | `INTEGER` | False | False | — |
| `object_key` | `VARCHAR(300)` | False | False | — |
| `uploaded_by` | `CHAR(32)` | False | False | memberships.user_id |
| `created_at` | `DATETIME` | False | False | — |
| `status` | `VARCHAR(24)` | False | False | — |
| `diagnostic` | `VARCHAR(48)` | True | False | — |
| `scanner` | `VARCHAR(48)` | True | False | — |
| `parser_version` | `VARCHAR(48)` | False | False | — |

- CheckConstraint (unnamed): status IN ('queued','processing','ready','quarantined','failed','cancelled','purged')
- ForeignKeyConstraint (unnamed): organization_id
- ForeignKeyConstraint (unnamed): organization_id, document_id
- ForeignKeyConstraint (unnamed): organization_id, uploaded_by
- PrimaryKeyConstraint (unnamed): id
- UniqueConstraint (unnamed): document_id, number
- UniqueConstraint (unnamed): document_id, sha256
- UniqueConstraint (unnamed): organization_id, id
