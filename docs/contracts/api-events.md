# API event and AI contracts

Current implemented checkpoint: Sprint 04, migration `0003_delivery`. [Delivery endpoints/DTOs](delivery.md) extend the identity API; generated OpenAPI/TypeScript is authoritative. Future job/event/AI envelopes below remain planning contracts.

Historical Sprint 02 checkpoint: migration `0002_identity`. Planning conventions below continue to govern future modules; executable OpenAPI and generated client types remain authoritative.

## Implemented identity surface

| Routes under `/api/v1` | Purpose |
| --- | --- |
| GET `/auth/csrf`; POST `/auth/login`, `/auth/refresh`, `/auth/logout` | Cookie/CSRF session lifecycle |
| GET `/auth/me`; PATCH `/auth/profile`; POST `/auth/switch` | Own account and validated organization selection |
| GET `/auth/sessions`; DELETE `/auth/sessions/{session_id}` | Own active sessions and immediate revocation |
| POST `/auth/reset-request`, `/auth/complete` | Non-enumerating recovery request and one-use activation/invite/reset completion |
| GET `/organization/members`; PATCH `/organization/members/{user_id}` | Admin-only member list and revision-checked role/active-state change |
| POST `/organization/invitations`; GET `/organization/audit` | Admin-only local invitations and scoped identity audit |

Cookie transport does not return access/refresh tokens in JSON. Unsafe calls require `Origin` equal to `PPM_WEB_ORIGIN` and `X-CSRF-Token`. Unsafe organization routes additionally require `X-Organization-ID` to match the server-resolved session (409 stale/missing selector). It never grants scope. Membership edits require `If-Match` containing the returned integer revision (428 missing, 412 stale); final-admin conflicts return 409. Hidden/foreign IDs return 404. Public auth failures are generic. Existing error envelope and request IDs are retained, including CSRF rejections.

Member/audit pagination uses `after` UUID, `items`, `next_cursor` and `as_of`, capped at 100 rows. Personal sessions are capped at the latest 100; password recovery revokes all. Self profile-name writes are last-write-wins; identity credential exchange and one-use challenges do not use generic idempotency keys. Repeated invitation creation represents a fresh delivery challenge; acceptance cannot duplicate membership or overwrite an existing one. These scoped exceptions do not relax future business mutation contracts.

Identity audit events are persisted local records, not published outbox events. Future durable events retain the planned envelope below. [ADR 008](../architecture/adr/008-identity-implementation.md) documents transport, RLS, control-plane boundaries and local limitations.

Version 0.1 planning contract. Sprint 01 generates executable OpenAPI/types; this document does not pretend that endpoints exist yet.

## API conventions

Base prefix `/api/v1`. JSON uses snake_case and stable UUID strings. RFC3339 UTC instants end in `Z`; date-only calendar values remain ISO dates with associated calendar/timezone. Money is a decimal string plus ISO currency code, not a binary floating number. Percent metrics use explicit units. IDs from other tenants never produce revealing validation messages.

Collections return `items`, opaque `next_cursor` and `as_of`; proposed default page size 25, max 100. Stable sort includes an ID tie-breaker. Allowlist filters/sort fields and cap date windows; do not pass raw SQL/Cypher from the client. Authorized empty results are distinct from permission errors. Optional totals must state their scope and snapshot consistency.

Responses use 200/201/204 as appropriate; async acceptance uses 202 plus `job_id` and status URL. Errors: 400 malformed request, 401 invalid authentication, 403 known but forbidden action, 404 missing or hidden object, 409 domain/version/idempotency conflict, 422 validated field error, 429 rate limit, 503 unavailable dependency. 429 includes bounded Retry-After when possible. Error body:

```json
{
  "error": {
    "code": "RESOURCE_VERSION_CONFLICT",
    "message": "The record changed. Refresh before saving.",
    "request_id": "uuid",
    "details": [{"field": "revision", "reason": "stale"}]
  }
}
```

Never serialize exception traces, credentials or foreign object existence. For editable records expose integer `revision` and ETag. Mutations use If-Match; missing precondition can return 428, stale 412. Reserve 409 for business conflicts. Use one shared implementation, and document endpoint exceptions explicitly. Archive is a domain transition, not silent hard deletion.

## Command and version safety

Retryable POST/apply operations require an idempotency key scoped to organization, actor, route and canonical request hash. Same key/hash returns the stored outcome; same key/different body returns 409. Proposed retention 24 hours for ordinary API keys; financial/scenario/workflow effects retain unique logical action IDs beyond that. Approval/apply checks expected versions for every affected record in one transaction, failing atomically if stale.

`/projects`, `/portfolios`, `/resources`, `/assessments`, `/documents`, `/ai-runs`, `/workflows`, `/scenarios`, `/reports` are planned resource families, not live routes. Generate clients from backend OpenAPI. Compatible additive fields are allowed when clients ignore unknowns; removing/changing meaning requires version/deprecation plan and impacted-consumer checks. Never rewrite applied migrations; expand/backfill/contract with a single Alembic head.

## Durable event envelope

```json
{
  "event_id": "uuid",
  "event_type": "project.updated",
  "schema_version": 1,
  "organization_id": "uuid",
  "aggregate_type": "project",
  "aggregate_id": "uuid",
  "aggregate_version": 4,
  "occurred_at": "2026-10-05T00:00:00Z",
  "actor_id": "uuid",
  "correlation_id": "uuid",
  "causation_id": "uuid-or-null",
  "payload": {"changed_fields": ["forecast_finish"]}
}
```

Event and domain mutation commit together. Consumers deduplicate by event/consumer ID, track aggregate version and detect gaps; never assume global queue ordering. Sensitive text remains behind source references. Replay must not resend historical notifications by default. Domain errors dead-letter with sanitized reason; retries have finite counts and jitter. Exact limits belong to workload configuration before Sprint 08 acceptance.

Job state: `queued -> running -> succeeded | partially_succeeded | failed | cancelled`; `running -> retry_wait -> queued` for bounded retry. Persist lease/heartbeat/attempt timestamps. A expired lease is reconciled, not assumed successful. Progress events carry per-run sequence and sanitized stage code. Cancellation after an external effect may require compensation, not a pretend rollback.

## SSE progress contract

Authenticated GET by run ID. Event `id` encodes retained per-run sequence; Last-Event-ID resumes retained events after authorization. Proposed heartbeat 15 s and replay retention 24 h; test proxy buffering/idle timeout behavior. If cursor expired, emit `resync_required` and obtain a current snapshot. Stage values include `queued`, `validating_sources`, `retrieving_evidence`, `analyzing_schedule`, `validating_output`, `completed`, `degraded`, `failed`. Send concise stage descriptions and timestamps, not raw model reasoning. Reconnect is not evidence that a job completed.

## Shared AI result contract

Every result includes `run_id`, `organization_id`, allowed `project_ids`, `input_snapshot_id`, `status`, `generated_at`, `provider`, `model_version`, `prompt_version`, `schema_version`, optional `rule_version`, `findings`, `recommendations`, `evidence_refs`, `coverage`, `limitations`, and usage metadata when available. Model IDs may be null in deterministic fallback. Each finding has severity, statement, evidence references and a support state; numeric confidence is allowed only with defined meaning. Predictions additionally require target, unit, horizon, model eligibility and evaluation reference.

Validate evidence existence, source version and permission, not merely JSON shape. Invalid output gets bounded repair/retry or a failed/degraded result. Provider text cannot choose organization context, tool privileges or execute actions. Proposed actions are typed payloads with target versions, never shell commands or unrestricted queries.

## Core state machines

| Entity | Proposed transitions and constraints |
| --- | --- |
| Project | draft → active → on_hold → active; active/on_hold → completed or cancelled; reopen requires reason/new plan; archive is separate visibility state |
| Work item | backlog → ready → in_progress → done; blocked flag with reason; reopen retains history |
| Risk | open → assessing → mitigating → resolved; accepted is an explicit authorized decision; reopen permitted with reason |
| Framework/workflow definition | draft → published → retired; published versions immutable |
| Assessment | draft → submitted → in_review → approved; returned → draft; approved results immutable revisions |
| Recommendation | proposed → accepted/rejected; accepted → execution_requested → applied/failed; acceptance alone does not execute |
| Approval instance | pending → approved/rejected/cancelled/expired; approved → executing → executed/failed; stale versions require new review |
| Document version | uploaded → quarantined/validating → processing → ready/failed; deletion invalidates derived access |
| Scenario | draft → running → ready/failed; ready → approval_requested → applied/rejected/stale; baseline immutable |
| Notification | queued → sending → delivered/failed/unknown/suppressed; retries retain attempt records |

## Change record

Version 0.1 defines the initial proposal. Sprint 01 implements resource-neutral errors/client generation; domain endpoints arrive in their owning sprints. Current migration head is `0002_identity`.

### Implemented foundation surface (Sprint 01)

GET `/api/v1/health/live` reports process liveness (200); GET `/api/v1/health/ready` checks database revision/checkpoint, Redis and storage (200/503); GET `/api/v1/foundation` returns the persisted installation UUID, UTC initialization time, environment and schema revision (200 or sanitized 503). All are local-only and have no domain mutation behavior. Request UUIDs are echoed in `X-Request-ID`, errors use the shared envelope and responses use `Cache-Control: no-store`.

`packages/contracts/openapi.json` is exported deterministically from FastAPI; `src/schema.d.ts` is generated and `src/client.ts` is the shared web transport. `npm run contracts:check` rejects drift. These foundation endpoints do not establish tenant authorization. Sprint 02 identity endpoints use the session, live membership and RLS boundary described above; future enterprise data routes must extend that boundary. No product event producer or durable outbox is implemented yet. New migrations must update the explicit readiness revision check and foundation schema metadata together.
