# Sprint 08 implementation report

## Status and scope
2026-10-09. Durable jobs, integrations and live progress: **complete locally within documented connector bounds**. Base `90564405bcacc8389e34f3b06d8ab8d00984c5c1`, branch `main`; implementation remains uncommitted. The pre-existing README edit and learning documents/artifacts are preserved. Scope: F-038, N-008, E-007 and E-009; supplementary live visibility/asynchronous processing and ingestion support. Live Jira/GitHub authentication and sync remain unverified because credentials are absent, as explicitly permitted by the Sprint 08 prompt. No Sprint 09 work started.

## What was built
`/integrations` lets an Admin configure project-bound CSV, Jira Cloud issue/sprint and GitHub issue/PR connections, preview mapped fixture rows, queue imports, inspect validation errors and provenance, renew delegated authority, enable/disable connections and cancel jobs. Sync history includes ordered live stages, attempts, heartbeat, partial results and dead-letter reasons. Reads retain tenant, project and initiating-actor restrictions. Command center watches authorized jobs and refreshes its stored metric snapshot after completion or degradation.

A durable PostgreSQL job/outbox pipeline now survives Redis delivery repetition and worker interruption. Fixture mode is clearly labelled; live mode uses bounded provider adapters and server-side credential references. There is no demo connector silently presented as authenticated live access.

## Why it was built
PPM source records need repeatable ingestion without making users wait for external calls or allowing background work to bypass scope. The job pipeline commits progress with each domain effect, exposes rejected rows and preserves local edits. [ADR 014](../../../architecture/adr/014-durable-ingestion.md) records recovery, delegated authority and provider tradeoffs; [jobs-v1](../../../contracts/jobs-integrations.md) defines guarantees and limits.

## How it works
An Admin maps provider fields to an existing work-item or sprint input. The API validates scope, CSRF, size and an idempotency key, then atomically stores the frozen input/configuration, job, audit, first event and version-1 outbox envelope. A ten-second dispatcher scan sends identifiers through Redis. The worker resolves persisted authority using the restricted app role, claims a fenced 45-second lease and rechecks live session/Admin/project access before each transaction.

Each accepted row commits its delivery mutation, source identity/version, audit, progress and checkpoint together. Duplicate imports reuse the same connection/external identity; changed local revisions are rejected. Bad rows become visible partial results. Provider retryable failures use bounded backoff and at most five attempts; terminal failures remain visible as dead letters. Cancelled/revoked work stops before the next effect, retaining committed effects. A crashed process resumes after its lease expires.

Authenticated SSE uses ordered per-run IDs, Last-Event-ID resume, 15-second heartbeats and a 24-hour replay window. A gap/expired cursor requests a current snapshot; session/scope is rechecked every second. The proxy streams without buffering. Source modification and observation timestamps are separate; Jira sprint modification time remains unknown. Imported historical closures never invent sprint velocity.

## How to use and demonstrate it
Keep the existing ignored `.env` and data. Run `docker compose up --build -d --wait`; open http://localhost:3000/integrations and sign in as an Admin. Choose an existing scoped project, create a CSV fixture connection with explicit headers/status mapping, preview a labelled sample, then queue it. Inspect accepted/rejected rows, live stages and source evidence. Repeat the same source through the same connection: domain effects are deduplicated. Use a new sync after correcting rejected rows.

For Jira/GitHub choose the explicit fixture preset for local demonstration. Live mode requires an operator-provisioned secret reference beginning `PPM_CONNECTOR_<UPPERCASE_ORG_UUID_WITHOUT_HYPHENS>_<PROVIDER>_`; put the referenced value in ignored `artifacts/local/connector-secrets.env` and recreate API/worker/dispatcher. Obtain least-privilege credentials from the provider. Jira uses a base64 email/API-token Basic value and a UTC search account; GitHub uses a bearer token and separate HMAC reference for native webhooks. Never paste values into connection settings. Native GitHub intake is `/api/v1/integrations/hooks/github/{id}`; localhost is not a deployed webhook destination.

Use `node scripts/check-identity-browser.mjs integrations.spec.ts` for an isolated labelled fixture walkthrough. Screenshots: [desktop](../../../verification/sprint-08-1440.png), [tablet](../../../verification/sprint-08-768.png), [mobile](../../../verification/sprint-08-360.png). Normal user data is never seeded by the demonstration.

## Implementation record
- `job_tables.py`, `jobs.py`, `ingestion.py`, `job_limits.py`: scoped durable state, API/SSE, bounded mappings/provider fetches and request limits.
- Additive migration `0007_durable_jobs`: five RLS tables, composite provenance constraints and narrow fixed-search-path discovery/revocation functions. Applied migrations 0001–0006 remain unchanged.
- `ppm_worker/app.py`, Compose: leased Celery execution and dispatcher; no new dependencies.
- `integrations.tsx`, `live-jobs.ts`, route/shell and streaming API proxy: settings, activity, provenance and dashboard refresh using existing design components. Generated OpenAPI/TypeScript updated.
- `delivery.py`: explicit incomplete historical coverage for imported sprint closure; existing calculations and lifecycle guards preserved.
- `test_jobs.py`, `integrations.spec.ts`, guarded backend/preservation/static scripts: real recovery and security evidence.

## Verification evidence
| Acceptance criterion | Check | Result | Evidence |
| --- | --- | --- | --- |
| Backend regressions, clean/prior/downgrade/repeat/drift migration lifecycle | Linux test profile | 63 passed, one inherited warning | [full backend](../../../verification/sprint-08-backend-security-final.txt) |
| Actual process crash/restart, replay, partial recovery, dead letter, cancellation, authorization and SSE | Focused jobs suite after restart | 8 passed | [focused](../../../verification/sprint-08-jobs-accepted.txt) |
| UI workflow and previous browser regressions | Isolated browser stack | 9 passed; keyboard/axe/no overflow at 1440/768/360 | [browser](../../../verification/sprint-08-browser-final.txt) |
| Contracts/types/lint/format/Ruff/mypy/source hashes | Static gate script | All eight exit 0; seven source hashes unchanged | [results](../../../verification/sprint-08-static-results.json) |
| Dependency audit | npm audit | Zero vulnerabilities | [audit](../../../verification/sprint-08-audit.txt) |
| Normal forward migration and existing data | Private backup + before/after hashes | 54 established tables unchanged, head 0007 | [final preservation](../../../verification/sprint-08-preservation-final.txt) |
| Real worker and restart/storage | Normal worker/checkpoint and persistence checks | Passed, original checkpoint retained | [worker](../../../verification/sprint-08-worker.txt), [persistence](../../../verification/sprint-08-persistence.txt) |

[Acceptance checks](../../../04-testing/sprint-based/sprint-08/TESTING_REPORT.md) record exact commands, failures/repairs and boundaries. No hosted CI or production load/SLA acceptance is claimed.

## Operational and security behavior
Only mapped scalar source fields are persisted; raw incidental notes and private reasoning never enter progress. Secret values are resolved server-side and excluded from DTOs/logs. Tenant-prefixed references prevent selecting another tenant's credentials. Requests are bounded before parsing; live URLs are provider allowlisted, redirects denied, DNS addresses checked public and requests timed out. Native GitHub HMAC/repository/type/delivery validation has a narrowly scoped CSRF exception; the signed batch gateway still requires authenticated CSRF. Jira uses polling.

RLS applies in worker retry paths, not just API requests. Forged broker identifiers cannot replace persisted authority. Revocation/disable/session expiry stop work and streams. Outbox scan repairs lost dispatch; expired leases repair interrupted work. Retained idempotency/source records protect repeats. SSE replay expiry is not physical deletion; organizational deletion/retention policy and service identities need production decisions. No external notifications, AI calls, paid resources or cloud deployment were introduced.

## Remaining work and decisions
No required local Sprint 08 gate remains failing. Live credentials/provider authentication, deployed webhooks, production throughput and proxy topology remain unverified. Definitions are immutable; create a new connection to change mappings, and avoid duplicate connection namespaces for one logical source/project. CSV is bounded to 500 rows; provider pages to 100 rows/2 MB and 20 pages/job. UI lists show first 100. GitHub PR/Jira sprint adapters replay bounded pages because their APIs lack compatible modification cursors. Partial/page-ceiling jobs do not advance the watermark. Local field edits cause quality errors rather than overwrite. These support limits are explicit in jobs-v1, not production completeness claims.

## Next sprint readiness
Durable job and existing local storage prerequisites are verified. Sprint 09 document intelligence still requires separate authorization and its own extraction, quarantine, retrieval and security contracts; none is implemented here. See [handoff](HANDOFF.md) and [coverage](../../../requirements/coverage.md). Stop at Sprint 08.

## Subsequent verification — 9 October 2026

The original checkpoint claims above are retained. Fresh Sprint 00–08 checks, the connector mapping repair, current runtime evidence and remaining live-provider blockers are recorded in the [sprint verification report](../../../04-testing/SPRINT_VERIFICATION_REPORT.md).
