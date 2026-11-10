# Antigravity entry point — reviewed local checkpoint

## 10 November 2026 — remaining structure work completed

All 129 feature handlers are thin; domain callers use operations directly. Tables
and typed record inputs have explicit feature/shared owners. Read the
[project map](docs/01-architecture/PROJECT_MAP.md) and
[full verification](docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
All 583 backend cases passed, zero skipped/deselected, including live ClamAV,
real OCR and actual Celery crash recovery. Static/contracts/docs checks pass.
Schema **0020**, normal/demo data, applied migrations and provider/pilot/sprint
boundaries remain. Test services are removed and volumes retained; no publication.

## 10 November 2026 — backend organization pass complete

The API root now has seven shared Python files and twelve feature packages with
file guides. Start with the [project map](docs/01-architecture/PROJECT_MAP.md) and
[final verification](docs/04-testing/BACKEND_STRUCTURE_STEP_29.md). Normal schema
**0020**, data, applied migrations and provider/pilot/sprint boundaries remain.
Temporary verification services are stopped; volumes are retained. No commit,
publication, deployment or new pilot occurred.

## 10 November 2026 — structure cleanup, step 28

The selection files are grouped under modules/selection; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_28.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 27

The workspace files are grouped under modules/workspace; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_27.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 26

The agents files are grouped under modules/agents; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_26.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 25

The ai files are grouped under modules/ai; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_25.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 24

The ml files are grouped under modules/ml; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_24.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 23

The integrations files are grouped under modules/integrations; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_23.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 22

The identity files are grouped under modules/identity; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_22.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 21

The delivery files are grouped under modules/delivery; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_21.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 20

The command files are grouped under modules/command; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_20.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 19

The capacity files are grouped under modules/capacity; callers use the new owners.
Existing statements, API/table definitions and schema **0020** are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_19.md).
Automatic sequential cleanup is authorized; no successor sprint, commit, publication,
deployment or live provider calls are authorized.

## 10 November 2026 — structure cleanup, step 18

Seven lifecycle/retention handlers delegate to operations; the orphan-candidate helper moves with its callers. Authorization, revision, retention/hold, evidence-link and filesystem eligibility statements are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_18.md).
Schema **0020**, existing rules and provider/pilot/sprint boundaries are preserved.
Sequential structural continuation is authorized; no successor, commit, publication
or deployment is authorized.

## 10 November 2026 — structure cleanup, step 17

Four file handlers delegate to operations for upload, download tickets, private downloads and reprocessing. Existing statement bodies, storage/hash checks and transport responses are preserved.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_17.md).
Schema **0020**, existing rules and provider/pilot/sprint boundaries are preserved.
Sequential structural continuation is authorized; no successor, commit, publication
or deployment is authorized.

## 10 November 2026 — structure cleanup, step 16

Seven read handlers delegate to query operations with identical statement bodies. HTTP defaults/Query validation stay on the routes; operations receive Principal and explicit arguments. AI retrieval and agent citations use the query owner directly.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_16.md).
Schema **0020**, existing rules and provider/pilot/sprint boundaries are preserved.
Sequential structural continuation is authorized; no successor, commit, publication
or deployment is authorized.

## 10 November 2026 — structure cleanup, step 15

Response loading, processing-job/outbox enqueueing and authorized replay now have a shared service owner. All three complete definitions move unchanged, reusing the existing scoped transaction.
Read the [latest handoff](docs/handoffs/LATEST.md) and [verification](docs/04-testing/BACKEND_STRUCTURE_STEP_15.md).
Schema **0020**, existing rules and provider/pilot/sprint boundaries are preserved.
Sequential structural continuation is authorized; no successor, commit, publication
or deployment is authorized.

## 10 November 2026 — structure cleanup, step 14

Document revision and request-fingerprint helpers now live in `mutations.py`;
document, AI and agent-review callers use the same definitions directly. Read
the [latest handoff](docs/handoffs/LATEST.md) and
[step 14 verification](docs/04-testing/BACKEND_STRUCTURE_STEP_14.md).
Canonical inputs, lock/replay order, public API and schema **0020** are preserved.
Provider, pilot and sprint boundaries remain; no successor, publication or
deployment is authorized.

## 10 November 2026 — structure cleanup, step 13

Document processing now lives in `modules/documents/worker.py`, called by the
existing job dispatcher and recovery tool. Its complete handler and nested
authorization body are preserved. Read the [latest handoff](docs/handoffs/LATEST.md)
and [step 13 verification](docs/04-testing/BACKEND_STRUCTURE_STEP_13.md).
Public API, permission/lease/scanner rules and schema **0020** are preserved.
Provider, pilot and sprint boundaries remain; no successor, publication or
deployment is authorized.

## 10 November 2026 — structure cleanup, step 12

Document/version lookup and write eligibility now live in `modules/documents/access.py`;
HTTP, worker and direct AI/agent readers use the unchanged checks.
Read the [latest handoff](docs/handoffs/LATEST.md) and
[step 12 verification](docs/04-testing/BACKEND_STRUCTURE_STEP_12.md).
Existing permission rules, public API and schema **0020** are preserved.
Provider, pilot and sprint boundaries remain; no successor, publication or
deployment is authorized.

## 10 November 2026 — structure cleanup, step 11

Document routes/worker, schemas, tables, parser and retrieval types are grouped in
`modules/documents`, with callers and the bounded parser child path updated.
Read the [latest handoff](docs/handoffs/LATEST.md) and
[step 11 verification](docs/04-testing/BACKEND_STRUCTURE_STEP_11.md).
Existing operation statements, public API and schema **0020** are preserved.
Provider, pilot and sprint boundaries remain; no successor, publication or
deployment is authorized.

## 10 November 2026 — structure cleanup, step 10

Framework operations, their response helper and example loader now live in
`modules/assessments/frameworks.py`, independent of the assessment service.
Read the [latest handoff](docs/handoffs/LATEST.md) and
[step 10 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_10.md).
Existing function bodies, route metadata and schema **0020** are preserved.
Provider, pilot and sprint boundaries remain; no successor, publication or
deployment is authorized.

## 10 November 2026 — structure cleanup, step 9

Grant management and private event-history operations now live in the assessment
service. All 21 assessment handlers are thin HTTP adapters; the router has no SQL.
Read the [latest handoff](docs/handoffs/LATEST.md) and
[step 9 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_9.md).
Existing rules, route metadata and schema **0020** are preserved. Provider, pilot
and sprint boundaries remain; no successor, publication or deployment is authorized.

## 10 November 2026 — structure cleanup, step 8

Six evidence HTTP handlers now delegate to `modules/assessments/evidence.py`.
Read the [latest handoff](docs/handoffs/LATEST.md) and
[step 8 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_8.md).
Private access, bounded intake, storage, integrity and quarantine/release behavior,
routes and schema **0020** are preserved. Existing provider, pilot and sprint
boundaries remain; this authorizes no successor, publication or deployment.

## 10 November 2026 — structure cleanup, step 7

Assessment lifecycle HTTP handlers now delegate to service operations; answer saving
uses the service detail reader internally. Read the [latest handoff](docs/handoffs/LATEST.md)
and [step 7 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_7.md).
Routes, rules and schema **0020** are preserved. Existing provider, pilot and sprint
boundaries remain; this refactor authorizes no successor, publication or deployment.

## 10 November 2026 — structure cleanup, step 6

Six framework HTTP handlers now delegate to assessment service operations. Read
the [latest handoff](docs/handoffs/LATEST.md) and
[step 6 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_6.md).
Route signatures/decorators, business statements and schema **0020** are preserved.
Existing provider, pilot and sprint boundaries remain; no successor, publication
or deployment is authorized by this refactor.

## 10 November 2026 — structure cleanup, step 5

Shared assessment workflow/data helpers now live in `modules/assessments/service.py`.
The agent caller uses that service without importing assessment HTTP routes. Read
the [latest handoff](docs/handoffs/LATEST.md) and
[step 5 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_5.md).
The helper bodies, API and normal schema **0020** are preserved; existing provider,
pilot and sprint boundaries remain in force. No successor, publication or deployment.

## 10 November 2026 — structure cleanup, step 4

Assessment write safeguards now live in `modules/assessments/mutations.py`, with
the original decorator/revision bodies and endpoint metadata preserved. Read the
[latest handoff](docs/handoffs/LATEST.md) and
[step 4 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_4.md).
Schema **0020** and the provider, pilot and sprint boundaries remain unchanged;
this does not authorize successor execution, publication or deployment.

## 10 November 2026 — structure cleanup, step 3

Assessment permissions now live in `modules/assessments/access.py`; route,
document and agent callers use the existing rules there. See the
[latest handoff](docs/handoffs/LATEST.md) and
[step 3 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_3.md).
This step preserves schema **0020** and the existing provider, pilot and sprint
boundaries. It does not authorize successor execution, publication or deployment.

## 10 November 2026 — structure cleanup, step 2

The assessment feature now has separate scoring and validation modules; existing
rule bodies and HTTP contracts are preserved. See the [latest handoff](docs/handoffs/LATEST.md)
and [step 2 verification](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_2.md).
This incremental cleanup does not advance a sprint, change schema **0020**, or
authorize provider experiments, publication or deployment.

## 5 November 2026 — structure cleanup, step 1

Assessment backend files are grouped in `services/api/ppm_api/modules/assessments`.
See the [latest handoff](docs/handoffs/LATEST.md) and
[step 1 report](docs/04-testing/ASSESSMENT_STRUCTURE_STEP_1.md) for file mapping,
verification, the generated schema-name change and the next small refactor.
This organization work does not advance a sprint or alter schema **0020**, provider
authorization, stopped pilots or the existing frontend checkpoint below.

## 31 October 2026 — frontend redesign follow-up

User-authorized local frontend work adds the forest/mint visual system, self-hosted
Geist, grouped navigation, real permission-scoped overview metrics and an eight-step
guided tutorial. Shared tables retain full server pages; delivery forms warn before
discarding edits. See [redesign report](docs/04-testing/FRONTEND_REDESIGN.md) for
coverage, actual verification and limitations. The ordinary timeout checkpoint
below remains the backend/sprint authority: schema **0020**, stopped pilots,
unchanged quotas and **AT17 BLOCKED**. No successor sprint or live-provider run.

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](docs/03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](docs/03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

Current sub-sprint: **Sprint 12.1 — Current API financial selection pilot**.
Read [the handoff](docs/03-sprints/active/sprint-12.1/HANDOFF.md) and
[actual run](docs/03-sprints/active/sprint-12.1/RUN_RECORD.md).
Authorized local work is complete. Owner-approved automated labels matched 12/12,
human_reviewed=false. f01 matched but took 21.437 seconds; f02 TIMEOUT stopped the
pilot with insufficient_data. No retries or further cases. Broad AT17 BLOCKED.

Normal schema **0019**, applied migrations frozen. Fresh 562 backend passes/one
skip, lifecycle/drift and two pilot browser checks pass. Preserve original 21
artifact edits, all data, roles/grants, provider policy, quotas and timeout health
state. The owner approved exactly four demo-only grants and the separate one-ID
local automated audit. The explicit grant check remains intact; its earlier
removal proposal was rejected and never applied. Do not ask for granted access
again, invent a human attestation, restart the experiment or begin Sprint 13.
No new commit/PR/push/deployment is authorized.

## Historical Sprint 12 closeout before the pilot

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](docs/10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13. The owner authorized documentation reconciliation and pushing to existing PR 7; no merge or deployment. Preserve all 21 unrelated artifact edits, provider scopes/ceilings and applied migrations.

## Historical checkpoints before Sprint 12

Historical Sprint 11 checkpoint: read the [handoff](docs/03-sprints/completed/sprint-11/HANDOFF.md). Nine typed specialists, semantic suggestions and independent review are implemented; real-model quality UNVERIFIED/BLOCKED. Preserve normal 0012 data, objects, credentials and existing history. 0013 is tested only in disposable databases. No commit/push/deployment; stop before Sprint 12.

## Historical checkpoints before Sprint 11

Historical checkpoint — 16 October 2026: Sprints 8.1 and 10 are COMPLETED for their implemented development scope at `0012_ai_runtime`. Reviewed application checkpoint `631c149` passed hosted CI; 201 backend tests and the document browser regression passed. A current pilot Word guide is rendered and visually verified. Gemini bounded completion/embedding smoke passed at maximum spend $0; confirmation does not expire daily. Production deployment, scale and broad agent/model quality remain OPEN release/successor gates. Sprint 11 is not started. Stop before 11.
Read [LATEST](docs/handoffs/LATEST.md), [MASTER](docs/prompts/MASTER.md) and
[Sprint 10 handoff](docs/03-sprints/completed/sprint-10/HANDOFF.md). Preserve all applied
0001–0012 migrations, .env, established data/objects and prior uncommitted work.
Gemini free-tier calls are authorized at $0; no paid calls or automatic model/provider upgrades.
Normal head 0012_ai_runtime; preservation and healthy runtime verified. Stop before 11.
Earlier Sprint 06 instructions below are historical and grant no successor execution.

Open this repository folder, not its parent:
`C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm`.

This is a portable agent handoff, not an Antigravity settings file. Read it explicitly
in the initial prompt. Creating this document does not start a sprint. The human's
instruction to execute a named sprint supplies authorization; do not ask again for
that same authorization. Do not advance to another sprint automatically.

## Recorded checkpoint

Prepared 2026-10-06: Sprint 05 complete locally; next is **Sprint 06 — Enterprise
maturity assessment engine**. Expected head: `0004_capacity`. Normal workspace is
on 3000/8000; isolated browser tests 3001/8001; delivery demo 3002/8002. These are
recorded observations, not a substitute for checking current state.

Always resolve [LATEST](docs/handoffs/LATEST.md) first. If it has advanced, follow its
checkpoint and the user's selected sprint, not the historical defaults in this file.
Do not run two coding agents against this checkout simultaneously.

## Minimal reading order

1. Applicable repository/parent agent instructions, this file, `docs/handoffs/LATEST.md`
   and the single handoff it identifies. Do not reopen earlier sprint histories unless
   an unresolved dependency requires them.
2. `docs/prompts/MASTER.md` and its canonical `01-MASTER-PROMPT.md`, once. Read only the
   selected sprint section in `02-ORDERED-SPRINT-PROMPTS.md`, ending at the next heading.
   Read `docs/requirements/decisions-and-assumptions.md` as required by MASTER.
3. Latest report/checks and the contracts explicitly required by the handoff. Extract
   selected sprint rows from `docs/requirements/coverage.md`; use targeted source
   passages for those requirements. Preserve original source files and hashes.
4. Inspect Git state, current migrations and generated-contract status. Then read only
   the implementation/test files needed for the first vertical slice. Locate symbols
   with `rg` before opening files. Do not dump the generated OpenAPI/TypeScript files;
   inspect relevant definitions and verify drift with the generator.

For Sprint 06, prioritize permission/metric/frontend contracts and the existing
organization/team hierarchy. Capacity/delivery contracts and ADR 011 are compatibility
boundaries. Reuse their transport, validation, audit and UI patterns; do not rebuild them.

## Sprint 06 completion boundary

The ordered sprint prompt is authoritative. Deliver the framework builder, dimensions,
questions/answer types, weights/rubrics, secure evidence attachments and immutable
published versions. Include editable example frameworks (PMO, Agile, governance,
delivery), assignments, draft autosave, submission/review/return/completion, deterministic
scoring, reasoned reviewer adjustments, scores/charts with tables, evidence coverage,
history and compatible department comparisons. No fabricated AI semantic scoring:
that remains Sprint 11. Secure evidence access/intake is part of the implementation,
not permission to activate later ingestion or AI modules.

Acceptance must include two departmental assessments, review, republishing without
changing old scores, weighting, all-missing answers, invalid rubrics, unauthorized
submissions and a worked explanation of score differences. Also retain required
cross-tenant/RLS, CSRF, revision/idempotency, migration, contract and browser checks.

## Economical execution

- State the scope in a few sentences, then implement. No duplicate architecture plan.
- Keep a small checklist in `docs/03-sprints/completed/sprint-06/SPRINT_REPORT.md` while working: done,
  next, blockers, decisions and evidence. Do not mark acceptance before checks pass.
- Search narrowly, exclude dependencies/build outputs, and bound command output.
  Save long non-sensitive test output under `docs/verification/`; inspect summaries
  and the relevant failure section. Never print `.env`, credentials or private fixtures.
- Run focused tests while editing; run required regression/security/lifecycle checks
  at a coherent integration checkpoint. Do not repeat successful unchanged checks
  unless a subsequent change or unresolved risk justifies it. Token savings do not
  justify omitting a required gate, negative test or visual inspection.
- Reuse locked dependencies and installed tools. Add a dependency only when necessary;
  verify official compatibility, licensing and security when doing so.
- Report only material progress, decisions and blockers. Avoid repeating unchanged
  facts. Final response: under 200 words, with results, limitations and artifact links.
- Before stopping or resetting context, update the current handoff and LATEST with
  the exact checkpoint, unfinished work, commands/results and next action. A resumed
  agent reads that checkpoint and continues; it must not restart completed work.

## Protect the workspace

Existing Git main had no commits/remote and all files were untracked. Verify that fact;
untracked files are not disposable. Never clean/reset, initialize over the project,
overwrite user changes, alter global Git trust or expose secrets. If ownership blocks
Git, use a repository-specific per-command safe.directory after verifying the path.

Reuse ignored `.env`; do not rerun bootstrap on established data. Keep 0001–0004
unchanged; add a single 0005 successor. No destructive downgrade of normal/demo data.
Only the guarded disposable test database may undergo lifecycle downgrade. Normal
checkpoint was `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c`; preserve it. Keep app-role RLS,
live sessions, explicit grants, sensitive effort privacy and immutable histories.
Use UTF-8 explicitly for Windows source edits. Do not copy tool-specific sandbox
workarounds blindly; use your own environment's permission mechanism when needed.

## Validation and final handoff

Use the existing scripts/configuration; read them before changing test execution.
Established commands (run from repository root):

```text
npm run contracts:generate          # after backend DTO changes
npm run contracts:check
npm run typecheck
npm run lint
npm run format:check
.venv/Scripts/ruff.exe check services scripts tests
.venv/Scripts/ruff.exe format --check services scripts tests
.venv/Scripts/mypy.exe services/api/ppm_api services/worker/ppm_worker
.venv/Scripts/python.exe scripts/check_sources.py
npm audit --audit-level=high
docker compose --profile test build test
docker compose --profile test run --rm test
node scripts/check-identity-browser.mjs
```

The backend runner guards the disposable DB and checks migration lifecycle/drift.
The browser runner creates isolated fixtures; an optional spec filename supports
targeted iteration. Required final regression scope follows the actual changes.
Historical Alembic files are outside the established mypy scope. Record inherited
warnings honestly. Do not claim hosted CI, production, performance or full accessibility
certification from local tests.

Finish the report and handoff using `docs/prompts/03-SPRINT-REPORT-TEMPLATE.md` and
`04-FOLLOW-UP-HANDOFF-TEMPLATE.md`. Update checks/evidence, LATEST, requirement coverage,
changed contracts, ADRs and CHANGELOG. Forward-upgrade/verify the authorized local stack
after isolated checks, preserving data. Stop after the authorized sprint.

## Initial prompt to paste

```text
Execute Sprint 06 only in this existing repository. Start by reading ANTIGRAVITY.md,
then follow its minimal reading order and the current docs/handoffs/LATEST.md.
This authorizes Sprint 06 implementation and local verification. Preserve existing
data, applied migrations, identity/privacy controls and unrelated files.
Work token-efficiently: targeted reads, concise output, focused iteration, no repeated
unchanged checks, but all required correctness/security/acceptance gates. Complete
the working slice, report, verification evidence, coverage, changelog and handoff;
stop before Sprint 07. Keep the final response under 200 words.
```
