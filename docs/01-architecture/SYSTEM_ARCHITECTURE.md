# Current system architecture

Status: **IMPLEMENTED AND VERIFIED** within retained local checks; future design is separately labeled in the preserved proposed architecture. Current source uses a modular monolith, not a separate microservice for each business feature.

```mermaid
flowchart LR
    Browser --> Next[Next.js pages and proxy]
    Next --> API[FastAPI routes and principal]
    API --> DB[PostgreSQL domain facts and RLS]
    API --> Store[Private local object storage]
    API --> Redis[Redis rate limits and task transport]
    DB --> Dispatch[Outbox dispatcher]
    Dispatch --> Redis
    Redis --> Worker[Linux Celery worker]
    Worker --> DB
    Worker --> Mail[Local mailbox or SMTP adapter]
```

| Component / real files | Responsibility / flow |
| --- | --- |
| `apps/web/app` and `components` | Routes/forms/selectors; delivery, resources, assessment, command center, integrations and pilot controls |
| `apps/web/app/api/v1/[...path]/route.ts` | Same-origin proxy forwards to API_ORIGIN and preserves transport/identity behavior |
| `packages/contracts/src/client.ts` | Typed openapi-fetch client; generated schema is derived from actual API |
| `main.py`, `identity.py` | Lifespan/config/health, CSRF/request IDs/errors, sessions and function-scoped principal transaction/tenant context |
| `delivery.py`, `capacity.py`, `assessment.py`, `command.py` | Domain rules with SQLAlchemy statements directly; no universal repository abstraction; deterministic scoring/metrics |
| `jobs.py`, `ingestion.py`, `job_tables.py`, worker | Durable PostgreSQL state/outbox with Redis/Celery transport; CSV/fixture adapters and progress; live connector acceptance open |
| `pilot.py`, `pilot_tables.py`, `account_mail.py` | Scoped search/setup/My work/cohorts/receipts/revision SSE, private account deliveries |
| `database.py`, `*tables.py`, migrations 0001–0008 | Metadata, constraints, tenant/reference keys, app-role RLS, migration-owner/application-role separation |

## Request, authorization and failure flow

Form → typed same-origin request → proxy → CSRF and identity → function-scoped transaction/principal → validation and owning domain rule → transaction-local user/organization/role → RLS/constraints → commit → response → component refetch. Permission is checked at the backend/database, not only by hiding a button. Ownership, role, grants and private effort are distinct.

File bytes and database metadata are not one atomic transaction. Import/outbox authority is PostgreSQL; Redis is transport, not durable business truth. Workspace SSE polls committed authorized revisions and broadcasts opaque change notices; it rechecks sessions and scope, closes on revocation, and clients coalesce refetch. SMTP delivery ambiguity requires honest status; accepted transport is not inbox proof.

Validation returns 422; CSRF/authority denial 403; absent/hidden records and authentication errors follow owning routes; stale revisions conflict; dependency readiness is 503. `main.error_response` provides sanitized errors/request IDs and avoids exposing driver credentials. Debug request ID, route, active organization, revision and source completeness.

## Explicit future boundaries

**PLANNED:** reusable documents/keyword retrieval/OCR (09), embeddings/gateway/orchestration (10), agents/semantic extraction (11), labeled models/forecasting (12–13), copilot (14), later enterprise/release modules (15–23). Existing assessment evidence and fixture ingestion are not a working RAG pipeline. Future vector/graph stores are derived views; no invented endpoint or table appears in current inventories.

See [API details](18-api-contracts.md), [schema](DATABASE-DICTIONARY.md), [authentication walkthrough](../02-learning/05-security/AUTHENTICATION_AND_AUTHORIZATION.md), [formula/data flow](../02-learning/06-ai-and-analytics/SCORING_AND_DASHBOARDS.md), [pilot guarantees](../contracts/pilot.md) and [future design](../09-planning/FUTURE_SPRINT_ROADMAP.md). The established contracts/ADRs retain their canonical locations.
