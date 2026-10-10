# Sprint 08 technical handoff

## Verified checkpoint
**Sprint 08 complete locally**, 2026-10-09. Branch `main`, base `90564405bcacc8389e34f3b06d8ab8d00984c5c1`. Sprint changes remain uncommitted; no push performed. Preserve the user's pre-existing README modification and untracked learning documents/artifacts. Normal Docker API/web healthy on 8000/3000, PostgreSQL/Redis on 15432/16379, worker and dispatcher running; applied head `0007_durable_jobs`.

F-038, N-008, E-007 and E-009 accepted locally within documented bounds; **real Jira/GitHub authentication/sync remains unverified**, as allowed without credentials. [Report](SPRINT_REPORT.md), [checks](../../../04-testing/sprint-based/sprint-08/TESTING_REPORT.md). No required local gate remains failing. No Sprint 09 work begun.

## Read these files first
1. `docs/prompts/MASTER.md`, `docs/prompts/02-ORDERED-SPRINT-PROMPTS.md` selected authorized section, `docs/requirements/coverage.md` and decision register.
2. `docs/contracts/jobs-integrations.md`, `api-events.md`, `permissions.md`, ADR `014-durable-ingestion.md`; prior command-center/metrics/delivery/capacity/assessment contracts remain authoritative.
3. `services/api/ppm_api/jobs.py`, `ingestion.py`, `job_tables.py`, `job_limits.py`; frozen migration `services/api/migrations/versions/0007_durable_jobs.py`.
4. `services/worker/ppm_worker/app.py`, `compose.yaml`, `compose.identity-test.yaml`; `apps/web/components/integrations.tsx`, `live-jobs.ts` and streaming `apps/web/app/api/v1/[...path]/route.ts`.
5. `tests/test_jobs.py`, `tests/browser/integrations.spec.ts`, generated OpenAPI/client via targeted lookup, and Sprint 08 checks.

## Current implementation
Working route `/integrations`, API `/api/v1/integrations`, Celery `pipeline.dispatch`/`pipeline.run`, versioned outbox, durable attempts/checkpoints, provenance, ordered SSE and command-center sync refresh. Admin creates/queues/renews/disables/cancels; scoped history/evidence reads remain Admin or initiating actor. CSV imports work locally; Jira/GitHub contract fixtures are explicitly labelled. Live adapters are implemented but unverified with real credentials. No AI/OCR/document/notification jobs or cloud resources enabled.

A sync freezes config and mapped input. Each row effect/audit/provenance/checkpoint/event commits atomically. Retryable failures back off, up to five attempts; expired 45-second leases recover crashes; cancellation retains already committed effects. Dispatcher scan every ten seconds reconciles PostgreSQL authority with replaceable Redis transport. Definitions are immutable, revision protects enable/disable/renewal; retained keys protect repeated job/source/webhook effects.

## Contracts the next prompt must preserve
Preserve current session, Admin/project authority, CSRF, app-role RLS and organizational mutation lock in workers/retries as well as APIs. Discovery functions expose narrow identifiers only; forged broker context cannot replace stored actor/session. Secret references are tenant/provider prefixed. Native signed GitHub hook is the sole exact CSRF exception; signed batch intake remains authenticated. Per-effect session expiry/revocation must stop work. Scope switches abort subscriptions.

Preserve jobs-v1/version-1 envelope and integer ordered SSE IDs, Last-Event-ID forwarding, nonbuffered streaming, one-second scope checks, 15-second heartbeat, 24-hour replay-window resync. Replay-window expiry does not physically delete records. Do not introduce deletion or assume service authority without its contract.

Preserve delivery/capacity/assessment/command formulas, currencies, sensitive effort grants/minimum-five suppression, frozen assessments and sprint closures. Imported historical closure coverage remains unknown. Source observation never becomes modification time. Local revision changes must not be overwritten. No graph/vector/AI interfaces changed; prior planned contracts remain planned. Shared shell/design tokens/components retained.

## Reproduce the current state
Use existing ignored `.env`; **never bootstrap or seed established normal data**. `docker compose up --build -d --wait` runs current normal head. No dependencies added. Tests: `docker compose --profile test build test`, then `docker compose --profile test run --rm test`; focused `docker compose --profile test run --rm test python -m pytest tests/test_jobs.py -q`. Browser `node scripts/check-identity-browser.mjs`; set `PPM_VERIFICATION_PREFIX` for command screenshots to avoid replacing older evidence. Browser fixture stack uses isolated 3001/8001 and cleans itself up. Never run PostgreSQL restart simultaneously with backend tests: normal/test databases share that process.

Statics: `.venv/Scripts/python.exe scripts/verify_sprint08_static.py`; exact recorded commands are in `sprint-08-static-results.json`. Windows Python script writes should use `PYTHONUTF8=1`; use `python -m mypy` rather than executable trampoline. Docker/network checks require environment sandbox escalation. Per-call Git safe.directory is needed; do not modify global config.

Latest full backend **63 passed**, focused **8 passed** (including additional forged-message/secret checks), full browser **9 passed**, eight static gates exit 0, npm audit zero vulnerabilities. One inherited Starlette/httpx warning. Actual worker subprocess kill/lease/restart and normal worker/storage restarts pass. No live provider/hosted CI/production load test. Standalone Windows unit attempt stalled; Linux full suite includes unit cases and is accepted evidence.

Credential references: `PPM_CONNECTOR_<UPPERCASE_ORG_UUID_WITHOUT_HYPHENS>_<PROVIDER>_...` in optional ignored `artifacts/local/connector-secrets.env`, operator-managed values only; recreate API/worker/dispatcher when provisioned. Jira Basic base64 email/token, search account timezone UTC; GitHub bearer plus HMAC reference. Do not reveal values. Localhost native hook cannot receive external deliveries without a separately authorized deployment.

## Data and migration state
Normal head **0007_durable_jobs**, five additive RLS tables. Applied 0001–0006 unchanged; 0007 is now frozen and subsequent repairs require a successor migration. No backfill or normal downgrade. Private binary backup `artifacts/local/sprint08-normal-before.dump`; before/after private JSON records all 54 established table hashes/counts unchanged after migration and restart. Checkpoint remains `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`; storage probes passed. Test fixture resets/downgrades are guarded and never target `ppm_local`. No vector/graph index introduced. Retain existing user data and uncommitted work; older tracked Sprint 06 screenshots regenerated by regressions were restored to baseline.

## Known issues and unresolved choices
No failing local acceptance gate. Live provider access, deployed webhook, production load/topology, delegated service identities and physical retention policy require later verification/decisions. `jobs-integrations.md` defines supported input/host bounds: CSV 500 rows, live 100 rows/2 MB per page and 20 pages, lists first 100. Large sources exceed the page ceiling without advancing cursor. Jira sprint and GitHub PR use bounded replay rather than unsupported modification cursors; Jira sprint source modification time is null. Partial sync leaves watermark unchanged. Configure one connection per logical source/project; distinct immutable connection namespaces can create separate effects. Correct quality errors then start a new sync; cancelled committed effects are not rolled back. These are accepted support boundaries, not silent unfinished capabilities.

Earlier failed logs remain. Final focused run failure was a concurrent normal restart, corrected by rerun after restart; Windows standalone unit stall is not a pass. See checks for exact evidence. No production-readiness claim.

## Next sprint instructions
**Stop before Sprint 09.** Its durable jobs and existing local storage prerequisites are verified, but document intelligence/OCR/retrieval is not implemented or authorized here. On separate authorization, read its selected prompt and document/storage/security contracts before adding bounded extraction, quarantine, scoped retrieval and versioned derivatives. Preserve frozen migrations, existing privacy and jobs-v1; do not reuse ingestion authority to silently turn untrusted documents into authoritative facts. Its format/deletion/security/retrieval gates must be designed and verified independently.

## Copy-ready next prompt
After separate user authorization: Execute Sprint 09 only. Read MASTER, LATEST and the Sprint 08 handoff, then the Sprint 09 ordered prompt and required document/storage/security contracts. Verify the actual checkpoint and prerequisites; preserve data, applied migrations, scope/privacy and uncommitted work. Implement its vertical slice and required gates, update report/checks/coverage/handoff, and stop before Sprint 10.
