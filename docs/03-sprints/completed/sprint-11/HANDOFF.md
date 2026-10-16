# Sprint 11 technical handoff

## Verified checkpoint

16 October 2026. PPM-11-001/002/003 implemented for local deterministic acceptance;
real-model semantic quality **UNVERIFIED/BLOCKED**. Current branch
`close-sprints-8-1-and-10`, base 77b330a. Remote fetch succeeded; origin/main
275e50b and merged PR #1 fix 631c149 are ancestors. All task changes are
uncommitted. No push, merge, deployment or Sprint 12 implementation.

Normal database was verified at **0012_ai_runtime** and remains there. Only
guarded disposable `ppm_test` databases were upgraded to **0013_specialist_reviews**.
Normal `.env`, provider configuration, stored objects, volumes and records are
preserved. Private backups/checkpoints are under ignored `artifacts/local/sprint11`.
Do not rerun bootstrap, downgrade the normal database or delete volumes.

## Read first

- [Report](SPRINT_REPORT.md), [actual tests](../../../04-testing/sprint-based/sprint-11/TESTING_REPORT.md),
  [documentation closure](../../../04-testing/sprint-based/sprint-11/DOCUMENTATION_CHECKS.md).
- [Specialist contract](../../../contracts/agents.md), [ADR 017](../../../architecture/adr/017-specialists-and-human-review.md),
  existing AI/document/assessment/metrics/permissions contracts.
- `services/api/ppm_api/agents.py`, `agent_engine.py`, `agent_provider.py`,
  `agent_schemas.py`, `agent_tables.py`, `ai.py`; additive migration 0013.
- `tests/test_agents.py`, `tests/browser/agents.spec.ts`, generated OpenAPI/client.

## Current implementation and contracts to preserve

`/agents` and `/api/v1/agents` cover nine agents, run details, observable progress,
exact cited spans, partial outcomes, conflict/duplicate handling, semantic scores
and independent review. Existing durable jobs/outbox/worker, budget ledger,
reservations, cancellation/lease fencing, sessions, app-role RLS and source
revocation remain authoritative. Two new tables hold immutable snapshots/results
and append-only human decisions. No original score or plan mutation path exists.

Preserve provider/model allowlist, zero-dollar operator policy, four calls/run,
rolling tenant request limit, retry/output/deadline limits and non-expiring
key-bound confirmation. Nine agents are batched, never nine automatic calls.
Sentiment sees only a privacy-safe group blocker summary, with minimum five;
raw workforce notes/individual labels remain excluded. Real-provider quality is
blocked; no paid review/coding agent was used. Untrusted comments/documents/model
output cannot become commands or tools.

## Reproduce

Use existing dependencies and `.env`; do not recreate credentials or source data.

```powershell
docker compose -f compose.yaml -f compose.documents.yaml --profile test build test
docker compose -f compose.yaml -f compose.documents.yaml --profile test run --rm --no-deps test python scripts/test_backend.py
node scripts/check-identity-browser.mjs agents.spec.ts ai.spec.ts documents.spec.ts assessment.spec.ts
npm run contracts:check
.venv\Scripts\python.exe scripts/documentation_inventory.py --check
.venv\Scripts\python.exe scripts/check_documentation.py
.venv\Scripts\python.exe scripts/check_previous_sprint_docs.py
.venv\Scripts\python.exe scripts/check_sources.py
```

The lifecycle runner explicitly refuses databases other than `test/ppm_test`.
Browser acceptance uses its own Compose project/ports 3001/8001/15433/16380 and
disabled providers. Guarded in-process doubles seed semantic browser results;
the dispatcher pauses during fixture creation and resumes for real durable
provider-disabled runs. Synthetic credentials are private and temporary.

## Known limits and next owner action

Exact final test counts are in the [testing report](../../../04-testing/sprint-based/sprint-11/TESTING_REPORT.md).
Hosted CI at this uncommitted revision, real-provider interpretation/semantic
quality, scale and production release are unverified. No billing or paid
fallback is authorized. Current bounds can yield partial output for large
assessments. Source failures conservatively withhold evidence. Independent
assistive-technology review remains a release gate.

Any future normal runtime adoption must apply 0013 forward with preservation
checks before starting this code; readiness now expects 0013. Recovery is
forward-only against normal data. Review original histories and tombstones
before any recovery. Sprint 12 remains unstarted and separately authorized.
