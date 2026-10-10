# Source-derived database dictionary

**ARCHIVED pre-audit snapshot.** Use the current architecture/reference inventory; this retained snapshot is not a competing canonical guide.


[Database chapter](../../07-database.md) · [Master guide](../../AI-PPM-MASTER-LEARNING-GUIDE.md)

Generated from current SQLAlchemy metadata, not a live database dump. Migration RLS/grants are documented separately. No database connection was opened. Full source files remain linked instead of reproducing large CREATE TABLE listings.

## foundation_state

**Purpose:** Non-tenant installation checkpoint.
**Model:** [FoundationState](../../../services/api/ppm_api/database.py). **Primary key:** id.
**Foreign keys:** None.
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** UNIQUE(instance_id); id = 1.
**Created in migration:** [services/api/migrations/versions/0001_foundation.py](../../../services/api/migrations/versions/0001_foundation.py).
**Used by:** `main.py / worker app.py`. **API:** `/api/v1/foundation`. **Frontend:** `apps/web/app/system/page.tsx`.
**Schema:** FoundationResponse. **Authorization:** public non-tenant read; owner-only initialization. **Lifecycle:** installation checkpoint.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_integration.py](../../../tests/test_integration.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `INTEGER` | False | Stable record identity (UUID except singleton) |
| `instance_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |

## identity_audit

**Purpose:** Append-only identity action record.
**Model:** [audit](../../../services/api/ppm_api/identity_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id, actor_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_identity_audit_organization_id: identity_audit.organization_id.
**Constraints:** PK/FK/nullability as below.
**Created in migration:** [services/api/migrations/versions/0002_identity.py](../../../services/api/migrations/versions/0002_identity.py).
**Used by:** `identity.py`. **API:** `/api/v1/auth/*; /api/v1/organization/*`. **Frontend:** `apps/web/app/account/identity-client.tsx`.
**Schema:** identity_schemas.py safe views; credential hashes never returned. **Authorization:** identity narrow lookups; organization/membership/audit RLS where applied. **Lifecycle:** identity activation/session/rotation/revocation or membership lifecycle; see chapter 10.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_identity.py](../../../tests/test_identity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `actor_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `action` | `VARCHAR(60)` | False | Domain value; see input schema and constraint definitions above |
| `target_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `request_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |

## identity_challenges

**Purpose:** Single-use activation/reset/invitation hashes.
**Model:** [challenges](../../../services/api/ppm_api/identity_tables.py). **Primary key:** token_hash.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, inviter_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** kind IN ('activate','reset','invite').
**Created in migration:** [services/api/migrations/versions/0002_identity.py](../../../services/api/migrations/versions/0002_identity.py).
**Used by:** `identity.py`. **API:** `/api/v1/auth/*; /api/v1/organization/*`. **Frontend:** `apps/web/app/account/identity-client.tsx`.
**Schema:** identity_schemas.py safe views; credential hashes never returned. **Authorization:** identity narrow lookups; organization/membership/audit RLS where applied. **Lifecycle:** identity activation/session/rotation/revocation or membership lifecycle; see chapter 10.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_identity.py](../../../tests/test_identity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `token_hash` | `VARCHAR(64)` | False | SHA256 digest of random credential |
| `kind` | `VARCHAR(12)` | False | Domain value; see input schema and constraint definitions above |
| `email` | `VARCHAR(254)` | False | Domain value; see input schema and constraint definitions above |
| `organization_id` | `UUID` | True | Tenant boundary; never accepted as delivery payload authority |
| `inviter_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `role` | `VARCHAR(20)` | True | Domain value; see input schema and constraint definitions above |
| `expires_at` | `TIMESTAMP WITH TIME ZONE` | False | Domain value; see input schema and constraint definitions above |
| `used` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## identity_refresh_tokens

**Purpose:** Rotating refresh credential hashes and replay state.
**Model:** [refresh_tokens](../../../services/api/ppm_api/identity_tables.py). **Primary key:** token_hash.
**Foreign keys:** (session_id) → (identity_sessions.id); ON DELETE NO ACTION (default).
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** PK/FK/nullability as below.
**Created in migration:** [services/api/migrations/versions/0002_identity.py](../../../services/api/migrations/versions/0002_identity.py).
**Used by:** `identity.py`. **API:** `/api/v1/auth/*; /api/v1/organization/*`. **Frontend:** `apps/web/app/account/identity-client.tsx`.
**Schema:** identity_schemas.py safe views; credential hashes never returned. **Authorization:** identity narrow lookups; organization/membership/audit RLS where applied. **Lifecycle:** identity activation/session/rotation/revocation or membership lifecycle; see chapter 10.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_identity.py](../../../tests/test_identity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `token_hash` | `VARCHAR(64)` | False | SHA256 digest of random credential |
| `session_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `used` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## identity_sessions

**Purpose:** Live revocation/expiry/tenant and CSRF binding.
**Model:** [sessions](../../../services/api/ppm_api/identity_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (user_id) → (identity_users.id); ON DELETE NO ACTION (default).
**Indexes:** ix_identity_sessions_user_id: identity_sessions.user_id.
**Constraints:** PK/FK/nullability as below.
**Created in migration:** [services/api/migrations/versions/0002_identity.py](../../../services/api/migrations/versions/0002_identity.py).
**Used by:** `identity.py`. **API:** `/api/v1/auth/*; /api/v1/organization/*`. **Frontend:** `apps/web/app/account/identity-client.tsx`.
**Schema:** identity_schemas.py safe views; credential hashes never returned. **Authorization:** identity narrow lookups; organization/membership/audit RLS where applied. **Lifecycle:** identity activation/session/rotation/revocation or membership lifecycle; see chapter 10.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_identity.py](../../../tests/test_identity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `csrf_hash` | `VARCHAR(64)` | False | Domain value; see input schema and constraint definitions above |
| `expires_at` | `TIMESTAMP WITH TIME ZONE` | False | Domain value; see input schema and constraint definitions above |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `revoked` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## identity_users

**Purpose:** Global verified identity and password hash.
**Model:** [users](../../../services/api/ppm_api/identity_tables.py). **Primary key:** id.
**Foreign keys:** None.
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** UNIQUE(email).
**Created in migration:** [services/api/migrations/versions/0002_identity.py](../../../services/api/migrations/versions/0002_identity.py).
**Used by:** `identity.py`. **API:** `/api/v1/auth/*; /api/v1/organization/*`. **Frontend:** `apps/web/app/account/identity-client.tsx`.
**Schema:** identity_schemas.py safe views; credential hashes never returned. **Authorization:** identity narrow lookups; organization/membership/audit RLS where applied. **Lifecycle:** identity activation/session/rotation/revocation or membership lifecycle; see chapter 10.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_identity.py](../../../tests/test_identity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `email` | `VARCHAR(254)` | False | Domain value; see input schema and constraint definitions above |
| `name` | `VARCHAR(120)` | False | Human-readable label |
| `password_hash` | `VARCHAR(128)` | True | bcrypt encoded hash; never response data |
| `verified` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |

## memberships

**Purpose:** User-to-organization role and active state.
**Model:** [memberships](../../../services/api/ppm_api/identity_tables.py). **Primary key:** organization_id, user_id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (user_id) → (identity_users.id); ON DELETE NO ACTION (default).
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** role IN ('Admin','Project Manager','Viewer').
**Created in migration:** [services/api/migrations/versions/0002_identity.py](../../../services/api/migrations/versions/0002_identity.py).
**Used by:** `identity.py`. **API:** `/api/v1/auth/*; /api/v1/organization/*`. **Frontend:** `apps/web/app/account/identity-client.tsx`.
**Schema:** identity_schemas.py safe views; credential hashes never returned. **Authorization:** identity narrow lookups; organization/membership/audit RLS where applied. **Lifecycle:** identity activation/session/rotation/revocation or membership lifecycle; see chapter 10.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_identity.py](../../../tests/test_identity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `role` | `VARCHAR(20)` | False | Domain value; see input schema and constraint definitions above |
| `active` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |
| `revision` | `INTEGER` | False | Optimistic concurrency version |

## organizations

**Purpose:** Tenant identity.
**Model:** [organizations](../../../services/api/ppm_api/identity_tables.py). **Primary key:** id.
**Foreign keys:** None.
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** PK/FK/nullability as below.
**Created in migration:** [services/api/migrations/versions/0002_identity.py](../../../services/api/migrations/versions/0002_identity.py).
**Used by:** `identity.py`. **API:** `/api/v1/auth/*; /api/v1/organization/*`. **Frontend:** `apps/web/app/account/identity-client.tsx`.
**Schema:** identity_schemas.py safe views; credential hashes never returned. **Authorization:** identity narrow lookups; organization/membership/audit RLS where applied. **Lifecycle:** identity activation/session/rotation/revocation or membership lifecycle; see chapter 10.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_identity.py](../../../tests/test_identity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `name` | `VARCHAR(120)` | False | Human-readable label |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |

## ppm_alignments

**Purpose:** Weighted goal contributions.
**Model:** [alignments](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, goal_id) → (ppm_goals.organization_id, ppm_goals.id); ON DELETE NO ACTION (default); (organization_id, portfolio_id) → (ppm_portfolios.organization_id, ppm_portfolios.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_alignments_org: ppm_alignments.organization_id.
**Constraints:** (project_id IS NULL) <> (portfolio_id IS NULL); UNIQUE(organization_id, id); revision > 0; weight >= 0 AND weight <= 1 AND contribution >= 0 AND contribution <= 1.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/alignments`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** AlignmentInput-Input → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | True | Tenant-scoped project relationship |
| `portfolio_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `goal_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `weight` | `NUMERIC(6, 5)` | False | Domain value; see input schema and constraint definitions above |
| `contribution` | `NUMERIC(6, 5)` | False | Domain value; see input schema and constraint definitions above |

## ppm_allocations

**Purpose:** Resource scheduled hours on a project.
**Model:** [allocations](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_allocations_org: ppm_allocations.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); end_date > start_date; hours_per_day >= 0 AND hours_per_day <= 24; revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/allocations`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** AllocationInput-Input → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `hours_per_day` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |

## ppm_answers

**Purpose:** Per-question raw answer/evidence narrative and reviewer adjustment.
**Model:** [answers](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, assessment_id) → (ppm_assessments.organization_id, ppm_assessments.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_answers_org: ppm_answers.organization_id.
**Constraints:** UNIQUE(organization_id, assessment_id, question_id); UNIQUE(organization_id, id); reviewer_score IS NULL OR (reviewer_score >= 0 AND reviewer_score <= 100).
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `apps/web/components/assessments.tsx`.
**Schema:** AnswerBatchInput / AnswerRecord. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `assessment_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `question_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `value` | `TEXT` | True | Domain value; see input schema and constraint definitions above |
| `evidence_text` | `TEXT` | False | Domain value; see input schema and constraint definitions above |
| `reviewer_score` | `NUMERIC(7, 4)` | True | Domain value; see input schema and constraint definitions above |
| `reviewer_note` | `TEXT` | True | Domain value; see input schema and constraint definitions above |

## ppm_assessment_access

**Purpose:** Framework editor or assessment result grants.
**Model:** [assessment_access](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, assessment_id) → (ppm_assessments.organization_id, ppm_assessments.id); ON DELETE NO ACTION (default); (organization_id, framework_id) → (ppm_frameworks.organization_id, ppm_frameworks.id); ON DELETE NO ACTION (default); (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_assessment_access_org: ppm_assessment_access.organization_id.
**Constraints:** (framework_id IS NULL) <> (assessment_id IS NULL); UNIQUE(organization_id, id).
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `API-only grant administration; results/editability consumed by apps/web/components/assessments.tsx`.
**Schema:** AccessInput. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `framework_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `assessment_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `active` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## ppm_assessment_events

**Purpose:** Append-only assessment actions and before/after details.
**Model:** [assessment_events](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, actor_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, assessment_id) → (ppm_assessments.organization_id, ppm_assessments.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_assessment_events_org: ppm_assessment_events.organization_id.
**Constraints:** UNIQUE(organization_id, id).
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `apps/web/components/assessments.tsx`.
**Schema:** EventRecord. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `assessment_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `actor_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `event` | `VARCHAR(30)` | False | Domain value; see input schema and constraint definitions above |
| `note` | `TEXT` | False | Domain value; see input schema and constraint definitions above |
| `details` | `JSONB` | False | Domain value; see input schema and constraint definitions above |

## ppm_assessment_requests

**Purpose:** Idempotent mutation fingerprint and response.
**Model:** [assessment_requests](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_assessment_requests_org: ppm_assessment_requests.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, user_id, key).
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `apps/web/components/assessments.tsx`.
**Schema:** internal response JSON; no public table CRUD. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `key` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `fingerprint` | `VARCHAR(64)` | False | Domain value; see input schema and constraint definitions above |
| `response` | `JSONB` | False | Domain value; see input schema and constraint definitions above |

## ppm_assessments

**Purpose:** Assignment, review state and frozen results.
**Model:** [assessments](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, assigned_to) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, department_id) → (ppm_departments.organization_id, ppm_departments.id); ON DELETE NO ACTION (default); (organization_id, framework_version_id) → (ppm_framework_versions.organization_id, ppm_framework_versions.id); ON DELETE NO ACTION (default); (organization_id, reviewer_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, submitted_by) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, team_id) → (ppm_teams.organization_id, ppm_teams.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_assessments_org: ppm_assessments.organization_id.
**Constraints:** UNIQUE(organization_id, id); assigned_to <> reviewer_id; revision > 0; status IN ('draft','submitted','in_review','returned','completed').
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `apps/web/components/assessments.tsx`.
**Schema:** AssignmentInput / AssessmentRecord / AssessmentDetail. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `framework_version_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `department_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `team_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `assigned_to` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `reviewer_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `submitted_by` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `status` | `VARCHAR(20)` | False | Domain value; see input schema and constraint definitions above |
| `results` | `JSONB` | True | Stored deterministic scoring result |
| `revision` | `INTEGER` | False | Optimistic concurrency version |

## ppm_audit

**Purpose:** Append-only before/after delivery history.
**Model:** [audit](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id, actor_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** PK/FK/nullability as below.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `indirect writes / specialized reads`. **Frontend:** `apps/web/components/delivery.tsx, capacity.tsx or command-center.tsx`.
**Schema:** HistoryView. **Authorization:** actor/tenant/project scoped policies; not directly mutable through public CRUD. **Lifecycle:** append-only audit, receipt or closure history.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `project_id` | `UUID` | True | Tenant-scoped project relationship |
| `actor_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `resource` | `VARCHAR(30)` | False | Domain value; see input schema and constraint definitions above |
| `target_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `before` | `JSONB` | True | Domain value; see input schema and constraint definitions above |
| `after` | `JSONB` | False | Domain value; see input schema and constraint definitions above |
| `request_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |

## ppm_availability

**Purpose:** Effective resource-to-calendar period.
**Model:** [availability](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, calendar_id) → (ppm_calendars.organization_id, ppm_calendars.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_availability_org: ppm_availability.organization_id.
**Constraints:** UNIQUE(organization_id, id); end_date > start_date; revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/availability`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** AvailabilityInput → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `calendar_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |

## ppm_baselines

**Purpose:** Versioned immutable project/work/milestone/sprint/budget snapshot.
**Model:** [baselines](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_baselines_org: ppm_baselines.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); UNIQUE(organization_id, project_id, version); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/baselines`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** BaselineInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** append only; create a new record/version or permitted reversal.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `version` | `INTEGER` | False | Domain value; see input schema and constraint definitions above |
| `snapshot` | `JSONB` | False | Frozen JSONB definition/facts |

## ppm_benefits

**Purpose:** Target and realized benefit in a declared unit/period.
**Model:** [benefits](../../../services/api/ppm_api/command_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_benefits_org: ppm_benefits.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); period_end > period_start; revision > 0.
**Created in migration:** [services/api/migrations/versions/0006_command_center.py](../../../services/api/migrations/versions/0006_command_center.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/benefits`. **Frontend:** `apps/web/components/command-center.tsx and delivery.tsx`.
**Schema:** BenefitInput-Input → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_command.py](../../../tests/test_command.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `unit` | `VARCHAR(40)` | False | Domain value; see input schema and constraint definitions above |
| `target` | `NUMERIC(18, 2)` | False | Domain value; see input schema and constraint definitions above |
| `realized` | `NUMERIC(18, 2)` | True | Domain value; see input schema and constraint definitions above |
| `period_start` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `period_end` | `DATE` | False | Domain value; see input schema and constraint definitions above |

## ppm_blockers

**Purpose:** Open/resolved delivery impediments.
**Model:** [blockers](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, project_id, work_item_id) → (ppm_work_items.organization_id, ppm_work_items.project_id, ppm_work_items.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_blockers_org: ppm_blockers.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); revision > 0; status IN ('open','resolved').
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/blockers`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** BlockerInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `work_item_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `status` | `VARCHAR(10)` | False | Domain value; see input schema and constraint definitions above |

## ppm_budget_lines

**Purpose:** Approved or unapproved decimal funding lines.
**Model:** [budget_lines](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_budget_lines_org: ppm_budget_lines.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); amount >= 0; revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/budget_lines`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** BudgetInput-Input → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `amount` | `NUMERIC(18, 2)` | False | Domain value; see input schema and constraint definitions above |
| `currency` | `VARCHAR(3)` | False | Domain value; see input schema and constraint definitions above |
| `approved` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## ppm_calendars

**Purpose:** Immutable weekly hours, holidays and timezone.
**Model:** [calendars](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_calendars_org: ppm_calendars.organization_id.
**Constraints:** UNIQUE(organization_id, id); friday >= 0 AND friday <= 24; monday >= 0 AND monday <= 24; revision > 0; saturday >= 0 AND saturday <= 24; sunday >= 0 AND sunday <= 24; thursday >= 0 AND thursday <= 24; tuesday >= 0 AND tuesday <= 24; wednesday >= 0 AND wednesday <= 24.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/calendars`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** CalendarInput-Input → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** append only; create a new record/version or permitted reversal.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `timezone` | `VARCHAR(80)` | False | Domain value; see input schema and constraint definitions above |
| `holidays` | `TEXT` | False | Domain value; see input schema and constraint definitions above |
| `monday` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |
| `tuesday` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |
| `wednesday` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |
| `thursday` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |
| `friday` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |
| `saturday` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |
| `sunday` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |

## ppm_capacity_snapshots

**Purpose:** Frozen non-sensitive planning sources and daily results.
**Model:** [capacity_snapshots](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_capacity_snapshots_org: ppm_capacity_snapshots.organization_id.
**Constraints:** UNIQUE(organization_id, id); end_date > start_date; revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/capacity_snapshots`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** CapacitySnapshotInput → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** append only; create a new record/version or permitted reversal.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `snapshot` | `JSONB` | False | Frozen JSONB definition/facts |

## ppm_departments

**Purpose:** Organizational grouping and owner.
**Model:** [departments](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_departments_org: ppm_departments.organization_id.
**Constraints:** UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/departments`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** DepartmentInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_dependencies

**Purpose:** Directed project/work/milestone dependencies.
**Model:** [dependencies](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, project_id, source_milestone_id) → (ppm_milestones.organization_id, ppm_milestones.project_id, ppm_milestones.id); ON DELETE NO ACTION (default); (organization_id, project_id, source_work_item_id) → (ppm_work_items.organization_id, ppm_work_items.project_id, ppm_work_items.id); ON DELETE NO ACTION (default); (organization_id, target_project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, target_project_id, target_milestone_id) → (ppm_milestones.organization_id, ppm_milestones.project_id, ppm_milestones.id); ON DELETE NO ACTION (default); (organization_id, target_project_id, target_work_item_id) → (ppm_work_items.organization_id, ppm_work_items.project_id, ppm_work_items.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_dependencies_org: ppm_dependencies.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); revision > 0; source_milestone_id IS NULL OR source_work_item_id IS NULL; target_milestone_id IS NULL OR target_work_item_id IS NULL.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/dependencies`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** DependencyInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `target_project_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `source_milestone_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `source_work_item_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `target_milestone_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `target_work_item_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_effort

**Purpose:** Sensitive actual and overtime hours.
**Model:** [effort](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_effort_org: ppm_effort.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); hours >= 0 AND hours <= 24; overtime_hours >= 0 AND overtime_hours <= hours; revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/effort`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** EffortInput-Input → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `worked_on` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `hours` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |
| `overtime_hours` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |

## ppm_effort_coverage

**Purpose:** Explicit daily completeness attestation.
**Model:** [effort_coverage](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_effort_coverage_org: ppm_effort_coverage.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, resource_id, worked_on); revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/effort_coverage`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** EffortCoverageInput → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `worked_on` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `complete` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## ppm_evidence_attachments

**Purpose:** Private quarantined text-object metadata.
**Model:** [evidence_attachments](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, assessment_id) → (ppm_assessments.organization_id, ppm_assessments.id); ON DELETE NO ACTION (default); (organization_id, uploaded_by) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_evidence_attachments_org: ppm_evidence_attachments.organization_id.
**Constraints:** UNIQUE(organization_id, id); file_size > 0 AND file_size <= 524288.
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `apps/web/components/assessments.tsx`.
**Schema:** EvidenceInput / EvidenceRecord. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `assessment_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `question_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `file_name` | `VARCHAR(160)` | False | Domain value; see input schema and constraint definitions above |
| `file_size` | `INTEGER` | False | Domain value; see input schema and constraint definitions above |
| `sha256` | `VARCHAR(64)` | False | Domain value; see input schema and constraint definitions above |
| `released` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |
| `storage_path` | `TEXT` | False | Domain value; see input schema and constraint definitions above |
| `uploaded_by` | `UUID` | False | Domain value; see input schema and constraint definitions above |

## ppm_expenditures

**Purpose:** Append-only spend and exact negative reversals.
**Model:** [expenditures](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, project_id, reversal_of) → (ppm_expenditures.organization_id, ppm_expenditures.project_id, ppm_expenditures.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_expenditures_org: ppm_expenditures.organization_id.
**Constraints:** (amount >= 0 AND reversal_of IS NULL) OR (amount < 0 AND reversal_of IS NOT NULL); UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); UNIQUE(organization_id, reversal_of); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/expenditures`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** ExpenditureInput-Input → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** append only; create a new record/version or permitted reversal.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `amount` | `NUMERIC(18, 2)` | False | Domain value; see input schema and constraint definitions above |
| `currency` | `VARCHAR(3)` | False | Domain value; see input schema and constraint definitions above |
| `spent_on` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `reversal_of` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_framework_versions

**Purpose:** Immutable published definitions.
**Model:** [framework_versions](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, framework_id) → (ppm_frameworks.organization_id, ppm_frameworks.id); ON DELETE NO ACTION (default); (organization_id, published_by) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_framework_versions_org: ppm_framework_versions.organization_id.
**Constraints:** UNIQUE(organization_id, framework_id, version); UNIQUE(organization_id, id); version > 0.
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `apps/web/components/assessments.tsx`.
**Schema:** VersionRecord with FrameworkInput snapshot. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `framework_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `version` | `INTEGER` | False | Domain value; see input schema and constraint definitions above |
| `snapshot` | `JSONB` | False | Frozen JSONB definition/facts |
| `published_by` | `UUID` | False | Domain value; see input schema and constraint definitions above |

## ppm_frameworks

**Purpose:** Editable framework JSON definition.
**Model:** [frameworks](../../../services/api/ppm_api/assessment_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_frameworks_org: ppm_frameworks.organization_id.
**Constraints:** UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0005_assessment.py](../../../services/api/migrations/versions/0005_assessment.py).
**Used by:** `assessment.py`. **API:** `/api/v1/assessment/...`. **Frontend:** `apps/web/components/assessments.tsx`.
**Schema:** FrameworkInput / FrameworkRecord. **Authorization:** assessment assignment/editor/result grants and 0005 RLS; private evidence has stricter scope. **Lifecycle:** published snapshot/event/receipt append-only; assignment state gates other mutations.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_assessment.py](../../../tests/test_assessment.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `definition` | `JSONB` | False | Domain value; see input schema and constraint definitions above |
| `revision` | `INTEGER` | False | Optimistic concurrency version |

## ppm_goals

**Purpose:** Strategic objective labels.
**Model:** [goals](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_goals_org: ppm_goals.organization_id.
**Constraints:** UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/goals`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** GoalInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_grants

**Purpose:** User read/edit/manage scope on one project or portfolio.
**Model:** [grants](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, portfolio_id) → (ppm_portfolios.organization_id, ppm_portfolios.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_grants_org: ppm_grants.organization_id.
**Constraints:** (project_id IS NULL) <> (portfolio_id IS NULL); UNIQUE(organization_id, id); UNIQUE(organization_id, user_id, portfolio_id); UNIQUE(organization_id, user_id, project_id); access IN ('read','edit','manage'); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/grants`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** GrantInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `project_id` | `UUID` | True | Tenant-scoped project relationship |
| `portfolio_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `access` | `VARCHAR(10)` | False | Domain value; see input schema and constraint definitions above |

## ppm_metric_plans

**Purpose:** Chosen baseline/calendar and forecast final cost.
**Model:** [metric_plans](../../../services/api/ppm_api/command_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, calendar_id) → (ppm_calendars.organization_id, ppm_calendars.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, project_id, baseline_id) → (ppm_baselines.organization_id, ppm_baselines.project_id, ppm_baselines.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_metric_plans_org: ppm_metric_plans.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id); UNIQUE(organization_id, project_id, id); forecast_cost IS NULL OR forecast_cost >= 0; revision > 0.
**Created in migration:** [services/api/migrations/versions/0006_command_center.py](../../../services/api/migrations/versions/0006_command_center.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/metric_plans`. **Frontend:** `apps/web/components/command-center.tsx and delivery.tsx`.
**Schema:** MetricPlanInput-Input → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_command.py](../../../tests/test_command.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `baseline_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `calendar_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `forecast_cost` | `NUMERIC(18, 2)` | True | Domain value; see input schema and constraint definitions above |

## ppm_metric_policies

**Purpose:** Organization risk thresholds and source-age cadence.
**Model:** [metric_policies](../../../services/api/ppm_api/command_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_metric_policies_org: ppm_metric_policies.organization_id.
**Constraints:** UNIQUE(organization_id); UNIQUE(organization_id, id); amber > 0 AND red > amber AND red <= 100; revision > 0; stale_days BETWEEN 1 AND 365.
**Created in migration:** [services/api/migrations/versions/0006_command_center.py](../../../services/api/migrations/versions/0006_command_center.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/metric_policies`. **Frontend:** `apps/web/components/command-center.tsx and delivery.tsx`.
**Schema:** MetricPolicyInput-Input → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_command.py](../../../tests/test_command.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `amber` | `NUMERIC(5, 2)` | False | Domain value; see input schema and constraint definitions above |
| `red` | `NUMERIC(5, 2)` | False | Domain value; see input schema and constraint definitions above |
| `stale_days` | `INTEGER` | False | Domain value; see input schema and constraint definitions above |

## ppm_milestones

**Purpose:** Dated delivery gates and actual completion.
**Model:** [milestones](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_milestones_org: ppm_milestones.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/milestones`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** MilestoneInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `due_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `actual_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |
| `critical` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## ppm_portfolios

**Purpose:** Top-level investment grouping.
**Model:** [portfolios](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_portfolios_org: ppm_portfolios.organization_id.
**Constraints:** UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/portfolios`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** PortfolioInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_programs

**Purpose:** Grouping within a portfolio.
**Model:** [programs](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, portfolio_id) → (ppm_portfolios.organization_id, ppm_portfolios.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_programs_org: ppm_programs.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, portfolio_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/programs`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** ProgramInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `portfolio_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_projects

**Purpose:** Authoritative delivery plan and reported status.
**Model:** [projects](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, created_by) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, department_id) → (ppm_departments.organization_id, ppm_departments.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, portfolio_id) → (ppm_portfolios.organization_id, ppm_portfolios.id); ON DELETE NO ACTION (default); (organization_id, portfolio_id, program_id) → (ppm_programs.organization_id, ppm_programs.portfolio_id, ppm_programs.id); ON DELETE NO ACTION (default); (organization_id, team_id) → (ppm_teams.organization_id, ppm_teams.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_projects_org: ppm_projects.organization_id.
**Constraints:** UNIQUE(organization_id, id); reported_health IN ('Green','Amber','Red','Unknown'); revision > 0; status IN ('draft','active','on_hold','completed','cancelled'); target_end_date IS NULL OR start_date IS NULL OR target_end_date >= start_date.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/projects`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** ProjectInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `portfolio_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `program_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `department_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `team_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `created_by` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `status` | `VARCHAR(20)` | False | Domain value; see input schema and constraint definitions above |
| `reported_health` | `VARCHAR(10)` | False | Domain value; see input schema and constraint definitions above |
| `currency` | `VARCHAR(3)` | False | Domain value; see input schema and constraint definitions above |
| `ledger_complete` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |
| `target_end_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |
| `forecast_end_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |
| `actual_start_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |
| `actual_end_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |

## ppm_requests

**Purpose:** Idempotent create receipts.
**Model:** [requests](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** organization_id, user_id, key.
**Foreign keys:** (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** No explicit secondary index; PK/unique constraints also create supporting indexes.
**Constraints:** PK/FK/nullability as below.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `indirect writes / specialized reads`. **Frontend:** `apps/web/components/delivery.tsx, capacity.tsx or command-center.tsx`.
**Schema:** internal record; no public CRUD. **Authorization:** actor/tenant/project scoped policies; not directly mutable through public CRUD. **Lifecycle:** append-only audit, receipt or closure history.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `key` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `fingerprint` | `VARCHAR(64)` | False | Domain value; see input schema and constraint definitions above |
| `resource` | `VARCHAR(30)` | False | Domain value; see input schema and constraint definitions above |
| `target_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |

## ppm_resource_access

**Purpose:** Explicit manage/effort capabilities.
**Model:** [resource_access](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default); (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_resource_access_org: ppm_resource_access.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, resource_id, user_id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/resource_access`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** ResourceAccessInput → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `manage` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |
| `effort` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |

## ppm_resource_skills

**Purpose:** Searchable resource skill labels.
**Model:** [resource_skills](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_resource_skills_org: ppm_resource_skills.organization_id.
**Constraints:** UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/resource_skills`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** ResourceSkillInput → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `skill` | `VARCHAR(80)` | False | Domain value; see input schema and constraint definitions above |

## ppm_resource_teams

**Purpose:** Effective reporting-team membership.
**Model:** [resource_teams](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default); (organization_id, team_id) → (ppm_teams.organization_id, ppm_teams.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_resource_teams_org: ppm_resource_teams.organization_id.
**Constraints:** UNIQUE(organization_id, id); end_date > start_date; revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/resource_teams`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** ResourceTeamInput → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `team_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |

## ppm_resources

**Purpose:** Independent workforce identity; not login authority.
**Model:** [resources](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_resources_org: ppm_resources.organization_id.
**Constraints:** UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/resources`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** ResourceInput → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `user_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_risks

**Purpose:** Human-maintained project risk register.
**Model:** [risks](../../../services/api/ppm_api/command_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_risks_org: ppm_risks.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); revision > 0; severity BETWEEN 1 AND 5 AND likelihood BETWEEN 1 AND 5; status IN ('open','mitigating','accepted','closed').
**Created in migration:** [services/api/migrations/versions/0006_command_center.py](../../../services/api/migrations/versions/0006_command_center.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/risks`. **Frontend:** `apps/web/components/command-center.tsx and delivery.tsx`.
**Schema:** RiskInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_command.py](../../../tests/test_command.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `severity` | `INTEGER` | False | Domain value; see input schema and constraint definitions above |
| `likelihood` | `INTEGER` | False | Domain value; see input schema and constraint definitions above |
| `mitigation` | `TEXT` | False | Domain value; see input schema and constraint definitions above |
| `status` | `VARCHAR(20)` | False | Domain value; see input schema and constraint definitions above |
| `review_on` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `resolution` | `TEXT` | False | Domain value; see input schema and constraint definitions above |

## ppm_saved_views

**Purpose:** User-owned dashboard filters.
**Model:** [saved_views](../../../services/api/ppm_api/command_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, portfolio_id) → (ppm_portfolios.organization_id, ppm_portfolios.id); ON DELETE NO ACTION (default); (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_saved_views_org: ppm_saved_views.organization_id.
**Constraints:** UNIQUE(organization_id, id); dashboard IN ('Executive','Delivery','Risk','Resource'); end_date > start_date AND end_date - start_date <= 366; revision > 0.
**Created in migration:** [services/api/migrations/versions/0006_command_center.py](../../../services/api/migrations/versions/0006_command_center.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/saved_views`. **Frontend:** `apps/web/components/command-center.tsx and delivery.tsx`.
**Schema:** SavedViewInput → RecordView / PageView. **Authorization:** current user owns view; saved filters never grant source access. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_command.py](../../../tests/test_command.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `portfolio_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `dashboard` | `VARCHAR(20)` | False | Domain value; see input schema and constraint definitions above |

## ppm_settings

**Purpose:** One organization timezone/currency configuration.
**Model:** [settings](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_settings_org: ppm_settings.organization_id.
**Constraints:** UNIQUE(organization_id); UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/settings`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** SettingsInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `timezone` | `VARCHAR(80)` | False | Domain value; see input schema and constraint definitions above |
| `currency` | `VARCHAR(3)` | False | Domain value; see input schema and constraint definitions above |

## ppm_sprint_closures

**Purpose:** Frozen completed-point evidence at sprint closure.
**Model:** [sprint_closures](../../../services/api/ppm_api/command_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, project_id, sprint_id) → (ppm_sprints.organization_id, ppm_sprints.project_id, ppm_sprints.id); ON DELETE NO ACTION (default); (organization_id, team_id) → (ppm_teams.organization_id, ppm_teams.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_sprint_closures_org: ppm_sprint_closures.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); UNIQUE(organization_id, sprint_id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0006_command_center.py](../../../services/api/migrations/versions/0006_command_center.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `indirect writes / specialized reads`. **Frontend:** `apps/web/components/delivery.tsx, capacity.tsx or command-center.tsx`.
**Schema:** internal record; no public CRUD. **Authorization:** actor/tenant/project scoped policies; not directly mutable through public CRUD. **Lifecycle:** append-only audit, receipt or closure history.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_command.py](../../../tests/test_command.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `sprint_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `team_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `points` | `NUMERIC(18, 2)` | False | Domain value; see input schema and constraint definitions above |
| `complete` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |
| `snapshot` | `JSONB` | False | Frozen JSONB definition/facts |

## ppm_sprints

**Purpose:** Planned/active/closed timebox.
**Model:** [sprints](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, team_id) → (ppm_teams.organization_id, ppm_teams.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_sprints_org: ppm_sprints.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); end_date >= start_date; revision > 0; status IN ('planned','active','closed').
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/sprints`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** SprintInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `team_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `status` | `VARCHAR(12)` | False | Domain value; see input schema and constraint definitions above |

## ppm_status_updates

**Purpose:** Append-only human-reported health narrative.
**Model:** [status_updates](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_status_updates_org: ppm_status_updates.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); reported_health IN ('Green','Amber','Red','Unknown'); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/status_updates`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** StatusInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** append only; create a new record/version or permitted reversal.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `reported_health` | `VARCHAR(10)` | False | Domain value; see input schema and constraint definitions above |

## ppm_team_members

**Purpose:** Dated login-user membership of a delivery team.
**Model:** [team_members](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, team_id) → (ppm_teams.organization_id, ppm_teams.id); ON DELETE NO ACTION (default); (organization_id, user_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_team_members_org: ppm_team_members.organization_id.
**Constraints:** UNIQUE(organization_id, id); end_date IS NULL OR end_date > start_date; revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/team_members`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** TeamMemberInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `team_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `user_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |

## ppm_teams

**Purpose:** Delivery team linked optionally to a department.
**Model:** [teams](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, department_id) → (ppm_departments.organization_id, ppm_departments.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_teams_org: ppm_teams.organization_id.
**Constraints:** UNIQUE(organization_id, id); revision > 0.
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/teams`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** TeamInput → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `department_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |

## ppm_time_off

**Purpose:** Dated unavailable hours.
**Model:** [time_off](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, resource_id) → (ppm_resources.organization_id, ppm_resources.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_time_off_org: ppm_time_off.organization_id.
**Constraints:** UNIQUE(organization_id, id); end_date > start_date; hours_per_day >= 0 AND hours_per_day <= 24; revision > 0.
**Created in migration:** [services/api/migrations/versions/0004_capacity.py](../../../services/api/migrations/versions/0004_capacity.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/time_off`. **Frontend:** `apps/web/components/capacity.tsx`.
**Schema:** TimeOffInput-Input → RecordView / PageView. **Authorization:** capacity.authorize/access plus 0004 RLS; effort requires explicit capability even for Admin. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_capacity.py](../../../tests/test_capacity.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `resource_id` | `UUID` | False | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `end_date` | `DATE` | False | Domain value; see input schema and constraint definitions above |
| `hours_per_day` | `NUMERIC(4, 2)` | False | Domain value; see input schema and constraint definitions above |

## ppm_work_items

**Purpose:** Backlog/ready/in-progress/done work and optional points.
**Model:** [work_items](../../../services/api/ppm_api/ppm_tables.py). **Primary key:** id.
**Foreign keys:** (organization_id) → (organizations.id); ON DELETE NO ACTION (default); (organization_id, owner_id) → (memberships.organization_id, memberships.user_id); ON DELETE NO ACTION (default); (organization_id, project_id) → (ppm_projects.organization_id, ppm_projects.id); ON DELETE NO ACTION (default); (organization_id, project_id, sprint_id) → (ppm_sprints.organization_id, ppm_sprints.project_id, ppm_sprints.id); ON DELETE NO ACTION (default).
**Indexes:** ix_ppm_work_items_org: ppm_work_items.organization_id.
**Constraints:** UNIQUE(organization_id, id); UNIQUE(organization_id, project_id, id); due_date IS NULL OR start_date IS NULL OR due_date >= start_date; points IS NULL OR points >= 0; revision > 0; status IN ('backlog','ready','in_progress','done').
**Created in migration:** [services/api/migrations/versions/0003_delivery.py](../../../services/api/migrations/versions/0003_delivery.py).
**Used by:** `delivery.py, capacity.py, command.py`. **API:** `/api/v1/delivery/work_items`. **Frontend:** `apps/web/components/delivery.tsx`.
**Schema:** WorkInput-Input → RecordView / PageView. **Authorization:** delivery.authorize; tenant/project RLS; protected mutations use lock/revision checks. **Lifecycle:** create → revision-controlled update → guarded archive/restore, subject to domain transition rules.
**Evidence:** IMPLEMENTED table in current metadata and frozen migration; regression family [tests/test_delivery.py](../../../tests/test_delivery.py). Individual ownership not verified.

| Column | PostgreSQL/model type | Nullable | Purpose / contract |
|---|---|---|---|
| `id` | `UUID` | False | Stable record identity (UUID except singleton) |
| `organization_id` | `UUID` | False | Tenant boundary; never accepted as delivery payload authority |
| `name` | `VARCHAR(160)` | False | Human-readable label |
| `description` | `TEXT` | False | Human explanation / reason where required |
| `revision` | `INTEGER` | False | Optimistic concurrency version |
| `archived` | `BOOLEAN` | False | Soft-retirement flag; preserves history |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | False | Creation instant with timezone |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | False | Last source edit instant; dashboard freshness input |
| `project_id` | `UUID` | False | Tenant-scoped project relationship |
| `sprint_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `owner_id` | `UUID` | True | Domain value; see input schema and constraint definitions above |
| `status` | `VARCHAR(12)` | False | Domain value; see input schema and constraint definitions above |
| `blocked` | `BOOLEAN` | False | Domain value; see input schema and constraint definitions above |
| `points` | `NUMERIC(10, 2)` | True | Domain value; see input schema and constraint definitions above |
| `start_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |
| `due_date` | `DATE` | True | Domain value; see input schema and constraint definitions above |
