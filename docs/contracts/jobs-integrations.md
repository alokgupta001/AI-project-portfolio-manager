# Durable jobs and ingestion — jobs-v1

## Sprint 12 extension

[Connector authority and conflict contract](ml.md) adds explicitly approved session-independent principals, scheduled polling, generation fencing, canonical identity and version-checked conflict review. Legacy connections retain their session gate until enrolled. Existing limits, source timestamps, cursor replay and durable jobs are reused.

Sprint 08 adds `/integrations`, API `/api/v1/integrations`, Celery `pipeline.dispatch`
and `pipeline.run`, and migration `0007_durable_jobs`. PostgreSQL is authoritative;
Redis/Celery is replaceable dispatch transport. No AI, notification delivery, OCR,
document ingestion or cloud resources are enabled by this slice.

## Authority and transport

Connection creation, preview, sync, enable/disable, renewal and cancellation require
live Admin membership, session, exact CSRF/origin and the active organization header.
Enable/disable requires integer `If-Match`; definitions and their project/provider
identity are immutable. Create and sync require `Idempotency-Key`: same input returns
the original result, changed input conflicts. Cancellation is a repeatable command;
already committed effects remain. Settings and activity show the first 100 records.

Every table has tenant RLS, and project visibility also bounds settings, jobs,
events and provenance. Only Admin or the initiating actor can read a run; having a
project read grant alone does not confer another actor's run access. Source links
have composite integration/project/work-item/sprint constraints. Workers resolve
the stored actor/session, take the organization mutation lock and recheck active
verified Admin membership, unrevoked/unexpired session and live project scope for
each effect. They use the real non-bypass `ppm_app` role with transaction-local
context. Broker messages contain only job/tenant/actor identifiers; forged messages
cannot replace persisted authority or payloads.

Narrow security-definer functions discover at most 100 due job identifiers, resolve
an initiating session identifier, route an opaque webhook integration identifier,
or cancel a provably unauthorized job. They use a fixed search path, qualified
tables and revoke PUBLIC execution. None returns source bodies or performs domain
effects. Cancellation checks actual persisted authority rather than caller claims.

Secret references must start with
`PPM_CONNECTOR_<UPPERCASE_ORGANIZATION_UUID_WITHOUT_HYPHENS>_<PROVIDER>_`.
Only the referenced environment value is resolved, on the server. This binds secret
selection to the current tenant/provider. Operators may place these variables in
ignored `artifacts/local/connector-secrets.env` (optional Compose env file), restrict
file access, and recreate API/worker/dispatcher after provisioning. No secret value
is returned, stored in a DTO, browser storage or application log. Different scopes
should use separate provider credentials with least privilege.

## Durable state and recovery

Job, initial progress event, audit and version-1 outbox envelope commit together.
The envelope includes event ID/type, schema version, tenant, aggregate ID/version,
source occurrence time, actor, correlation and causation identifiers; its payload
is just a sanitized stage. Beat reconciles every 10 seconds. Queued/retry jobs and
running jobs with expired leases are redispatched. Receipt sets `dispatched_at`.
Duplicate deliveries are harmless: terminal jobs are skipped; a current lease
prevents another attempt. No exactly-once provider-delivery claim is made.

Each attempt has a new fencing token and 45-second lease; every row/page checkpoint
renews heartbeat and lease. At most five attempts are permitted. Retry delays use
`min(300, 5 * 2^attempt + jitter[0..5])` seconds and a bounded provider Retry-After
(maximum 300 seconds). 429, exhausted GitHub rate limit, 502/503/504 and transport
timeouts retry. Authentication/schema errors dead-letter with a fixed reason.
Process crashes/time limits recover after lease expiry, retaining committed row
positions. Failed jobs retain their dead-letter stage and sanitized reason in job
activity; a corrected/new sync is the operator retry path, never a silent replay
of unrelated historical external notifications.

Each domain effect, source identity/version/fingerprint, audit, progress sequence
and row position commit in one transaction. Validation failures roll back just that
row and produce `partially_succeeded`. Integration disable or cancellation stops
before the next effect. Revoked/demoted/expired initiators are cancelled without
an effect. Domain/project conflicts never become successful source records.

## Adapters and provenance

Adapters implement bounded page fetch plus explicit field-path/status mapping into
existing delivery inputs. Supported target fields: source ID, title, source
modification timestamp, status, points and dates. Owners, grants, resources, raw
workforce notes and organization IDs cannot be imported. Only mapped scalar fields
are retained; incidental provider bodies/notes are discarded before persistence.
Preview returns up to five mapped examples and per-row errors without domain writes.

| Adapter | Supported behavior | Bounds and limitations |
| --- | --- | --- |
| CSV | UTF-8 JSON-transported CSV text, explicit header mapping, preview, row validation and repeat-safe work-item import | 500 rows, 500,000 characters; duplicate headers/inconsistent columns/NUL rejected; no binary uploads or formulas evaluated |
| GitHub | Public `api.github.com`, repository issues and PRs as work items; bearer credential reference; issues `since` cursor; updated-order pagination | Issues endpoint PRs filtered into separate PR adapter; pulls are paged/reconciled by source version because the pulls API lacks `since`; no arbitrary enterprise host, commit/notes/workforce ingestion |
| Jira Cloud | Allowlisted `tenant.atlassian.net`, project JQL issue pages with `nextPageToken`, board sprint pages with `startAt`; Basic reference to operator-provisioned base64 email/API-token | Explicit mappings and local team/board required for sprints; no arbitrary/self-hosted URL; project-specific fields must exist in returned DTO |

Live pages are capped at 100 rows/2 MB, 20 pages/job and eight-second request timeout;
redirects are denied and resolved addresses must be public. No caller-supplied full
URL is fetched. Missing configuration fails safely. Fixture mode accepts supplied
provider contract records and never authenticates to a provider; live mode rejects
fixture/CSV injection and fetches only in the worker. Rate/authentication behavior
tested with contract fixtures is not verification of real provider credentials.

Source uniqueness is `(integration_id, external_id)`. Repeat imports into the same
connection do not create another target. Older source versions are ignored; equal
timestamp/different content is a data-quality collision. Local target revision
changes are rejected rather than overwritten. Existing delivery lifecycle rules
still apply to work-item updates. Connection namespaces remain separate: do not
configure duplicate connections for the same logical source and target project.

Source modification time and observation time are distinct UTC fields. Jira sprint
DTOs have no modification time, so it remains null; observation time is recorded,
never relabelled as modification/freshness. Provider timestamped sprint dates retain
the date in the supplied source offset. Imported sprint lifecycle transitions are
audited under existing guards. Imported closure snapshots mark historical point
coverage unknown; they never manufacture velocity from mutable current work.

Issues advance a modification watermark only after every page and row succeeds.
Partial/failed sync leaves the original cursor, so corrected replay rechecks already
applied identities and resumes safely. Jira JQL date filtering uses its search
account's timezone; configure that account to UTC for the current adapter. Sprint
and PR APIs do not expose compatible modification cursors, so they use bounded
page replay plus idempotent source versions instead. A page-ceiling failure does
not advance the watermark. Cursor is operational state, not definition revision.

## Signed webhook intake

`POST /hooks/github/{integration_id}` accepts native GitHub `issues` or
`pull_request` envelopes and validates HMAC-SHA256 over exact bounded body bytes,
event type, repository identity, enabled integration and its current delegated
Admin session. This exact route is the only CSRF exception. No cookies or bearer
token in a URL are needed. `X-GitHub-Delivery` is retained as a tenant/integration
idempotency identity; replay returns the original job and a changed signed body
with the same identity conflicts. Live hooks trigger a configured sync; fixture
hooks consume their explicitly labelled contract record. It sends no external
communication. Localhost is not a deployed webhook destination.

`POST /{id}/webhook` is additionally an authenticated, CSRF-protected signed batch
gateway for contract/CSV fixtures. It is not advertised as native Jira webhook
compatibility; Jira uses polling. The delegated session expires/revokes normally;
an Admin renews via the revision-checked settings action. No unattended service
identity is invented.

## SSE and privacy

`GET /activity/jobs/{id}/events` authenticates the run before streaming, then
reauthorizes session, membership and project access every second using a fresh,
closed transaction. No pooled connection is held for the subscription lifetime.
Stage events carry a stable UUID, monotonically increasing per-run sequence,
sanitized stage and UTC timestamp. There is no raw source body, provider output,
private reasoning, individual effort or sentiment data in events.

`Last-Event-ID` (or `after` query fallback) resumes after the retained integer
sequence. Replay window is 24 hours; an invalid gap, expired or future cursor emits
`resync_required` so the caller fetches a current job snapshot. Heartbeat comments
arrive every 15 seconds. Revocation emits `access_revoked` and closes without further
stages. Terminal streams finish after their final sequence. The web proxy passes
through streaming bodies, cancellation and resume headers without buffering.

Job activity reconnects with its last sequence; command center discovers authorized
runs, listens for completion/degradation and refreshes the authoritative metric
snapshot. Missed events fall back to current activity snapshots. Scope changes
abort old subscriptions. The local small-fixture checks are not a throughput,
proxy-topology or production latency/SLA certification.

Records remain retained locally for audit, provenance and replay protection; SSE's
24-hour *replay window* is not a physical deletion policy. No automatic deletion of
the user's data is introduced. Set organizational physical retention and delegated
service authority before production use. Existing capacity grants, minimum-five
team suppression, frozen assessments and all metric definitions are unchanged.

## Official protocol references

[Celery task acknowledgement/retry](https://docs.celeryq.dev/en/stable/userguide/tasks.html),
[Jira issue search](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/),
[GitHub webhook signatures](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries),
[GitHub event envelopes](https://docs.github.com/en/webhooks/webhook-events-and-payloads).
Reviewed 2026-10-09; existing pinned dependencies retained, no new package introduced.

## Sprint 09 source extension

`durable_jobs` now has an exclusive integration/document-version reference by job kind. Source jobs reuse outbox/dispatcher/Celery but validate persisted actor/session/document authority under organization locking and fenced leases before claim/publication. Three attempts and 120-second leases bound source processing; no unauthorized late publication. Legacy connector cancellation cannot be invoked with a forged document tuple. [Document contract](documents.md) specifies the source extension; existing connector scope/provider gates remain.
## Sprint 10 AI runtime extension

[ai-evidence-v1](ai.md) owns the additive /api/v1/ai and /ai behavior, immutable
snapshots, budgets/accounting, protected source tools, citation reauthorization,
versioned evaluation and disabled fallback. durable_jobs references exactly one
integration, document version or AI run; existing event/SSE/authority rules remain.
Bounded Gemini free-tier smoke verified; broad model quality unverified. No semantic agents, private assessment ingestion,
metric changes or automatic plan edits. Admin-only restricted operations apply.

## Sprint 12 authority, identity and CPU extension

The current durable-job source constraint permits exactly one integration, document
version, AI run or local ML run. Enrolled connector authority is independent of its
creator session and remains scoped to one approved connection/project; generation
rotation/revocation fences queued work. Scheduling failures roll back per connector
and back off separately so other connectors/due jobs continue. Omitted CSV namespaces
are integration-specific; explicit namespaces remain shareable. Canonical keys take
precedence over legacy NULL keys; local edits require version-checked conflict review.
CPU runs reuse the existing dispatcher/worker and produce explicit blocked/insufficient
or evaluated cards. [The ML/connector contract](ml.md) owns current semantics; earlier
extension sections above describe their migration checkpoints. Normal schema is 0018.
