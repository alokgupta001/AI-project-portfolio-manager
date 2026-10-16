# Sprint 10 implementation report

**Closeout — 16 October 2026: Sprints 8.1 and 10 are COMPLETED for their implemented development scope.** The reviewed application checkpoint `631c149` passed [hosted CI](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/38885041673), including regression, migration and browser checks. The current pilot Word guide is rendered and visually verified in the linked closeout evidence. Earlier blocked/active statements below describe their recorded checkpoints. Production deployment, broad real-model/agent quality and scale remain OPEN release/successor gates. Stop before 11. [Acceptance matrix](../../../10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md).

## Historical record before closeout

## Current reconciliation — 16 October 2026

**Local implementation VERIFIED; bounded real Gemini completion/embedding smoke
VERIFIED; overall model/retrieval-quality and production acceptance remain OPEN.**
The previous missing-provider authorization blocker is resolved: the user
authorized Gemini free tier on a confirmed unbilled project, maximum spend $0.
The user subsequently removed daily confirmation expiry. Stop before 11.

The recorded full local baseline was 150 backend tests, 16 browser scenarios and
12 offline validator cases. The Gemini follow-up recorded a real exact-excerpt
completion and 256-dimension embedding smoke, an isolated UI check, and 63 final
AI/provider regression cases after removing expiry. These are separate runs and
must not be added into one test-suite total. See [follow-up evidence](../../../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md),
[current runtime](../../../verification/gemini-runtime.json) and
[no-expiry checks](../../../verification/gemini-no-expiry-checks.json).

Current normal schema remains `0012_ai_runtime`; no follow-up migration was needed.
Defaults stay disabled for new installations; the local private configuration
selects `gemini-3.5-flash-lite` and `gemini-embedding-2`. No paid model/provider
failover is enabled. Operator confirmation remains bound to the saved key/project;
all USD settings are zero. Per-run and rolling tenant request limits, authority,
source/citation validation, cancellation and source fallback remain active.

The one-sentence synthetic smoke establishes a narrow working connection, not
agent accuracy or general semantic retrieval quality. JSONB vectors remain bounded
to 20 chunks/index and 200 candidates, not pgvector/ANN or production scale.
Hosted CI at the reviewed working tree, archived Word every-page visual QA and
production/release requirements remain unverified. No Sprint 11 implementation,
commit/push or external deployment is authorized by documentation reconciliation.

The [previous-sprint documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md)
is the current documentation audit. The original checkpoint below and its
hash manifest remain historical; they are not overwritten by the new evidence.

## Historical 15 October record

15 October 2026. Status: LOCAL AUTHORIZED IMPLEMENTATION VERIFIED. Overall acceptance remains
OPEN because required real-provider smoke is BLOCKED by explicit user instruction.
Implement mocks and fallback; no provider/model/spending authorization exists.
No paid request, external deployment, commit, push or Sprint 11 work is authorized.

## Scope and actual checkpoint

Base main at b98110e with pre-existing uncommitted Sprint 09 source/docs preserved.
Actual normal starting revision 0011_document_sources verified by PostgreSQL.
New additive migration 0012_ai_runtime is applied to normal after isolated acceptance.
Private .env/source/prompt/migration hashes, Git patch/untracked archive, database
backup, object archive and 66 table hashes are under ignored artifacts/local/sprint10.
No destructive normal/demo lifecycle or volume removal. Frozen source prompts,
assessment histories, identity/grants/privacy and shared metric math are retained.

Read the applicable entry, MASTER/original master, Sprint 09 handoff/report/testing/
documentation checks, revised 10 roadmap and planned hub, original ordered scope,
coverage/decisions/traceability/release gates, source/permission/API/jobs/frontend/
pilot/assessment/metric contracts, ADRs and shared documentation checklist/mapping.
Current user authorization permits only Sprint 10 and a safe local forward rollout.

## Implemented slice

PPM-10-001: shared completion/embedding boundary with disabled defaults, optional
fixed-origin OpenAI adapter and test-only injected doubles; immutable prompt/schema/
tool/graph/model/rate snapshots; redacted diagnostics and usage/latency; serialized
tenant budget reservations, bounded concurrency, deadlines/retries and circuit.
Budgeted current-version embeddings and hybrid rank fusion reuse Sprint 09 source
interfaces and citation checks. No-key queries return explicitly labeled keyword
source excerpts. Real provider acceptance remains BLOCKED; no fixture is a smoke.

PPM-10-002: fixed two-branch typed orchestration, independently authorized allowlisted
read-only tools, persisted stage progress/SSE, cooperative cancellation and fenced
publication. Broker replay preserves accounting; crashed paid calls become unknown
outcomes instead of unbounded retries. Untrusted evidence cannot add tools, scope
or mutations. Only full exact source excerpts can pass the output support gate.

PPM-10-003: connected /ai UI with disabled/empty/loading/error/recovery/partial states,
Admin budgets/usage/circuit/run inspection and versioned evaluation counts/failures.
PM/Viewer diagnostics are denied. Twelve offline gate fixtures declare support,
citation and completion 100%, leakage/unsupported numbers zero before Sprint 11.

## Decisions and limitations

ADR 016 explicitly records bounded JSONB exact vectors instead of adding pgvector
to the established PostgreSQL image. At most 20 chunks per indexing request and
200 permitted semantic candidates; larger sets fall back truthfully to keywords.
This is a rebuildable pilot projection, no ANN or scale/performance acceptance.
USD charges conservatively retain each attempt cap; they are not verified invoices.
Current PM grants lack explicit costly-analysis authority, so starting work is
Admin-only. Assessment private evidence and workforce data are not tool inputs.

## Acceptance evidence and documentation closure

- Local implementation/fixtures: **150 backend tests passed**, one inherited warning,
  296.40 seconds. Clean/prior/base/repeated migrations and drift passed; explicit
  disposable 0011-to-0012 check passed. Twelve versioned offline gate cases passed. Final supplemental AI/SSE suite: 25 passed, 47.83 s.
- Browser: **16 passed (4.0 minutes)**, including real no-key source processing,
  recovery, role denial and full delivery/review/revocation walkthrough. Corrected
  desktop/tablet/mobile/light/dark renders visually reviewed; serious/critical axe
  and overflow checks pass, without full WCAG certification.
- Static/contracts/audits: TypeScript, ESLint, Prettier, Ruff/format, mypy 42 source
  files and generated OpenAPI/TypeScript pass. npm and pinned locked Python audit
  report no known vulnerabilities. Final documentation inventory/link/source checks
  and exact file hashes are recorded in the closure/checkpoint.
- Normal forward rollout: **0012_ai_runtime** applied; all **66 existing table
  counts/hashes**, **five original object keys/byte hashes** and **21 unique frozen
  .env/source/prompt/earlier-migration paths** match. Eleven applied predecessor
  migration files are untouched. PgAdmin and existing named volumes retained.
- Runtime: normal web/API/worker/dispatcher/PostgreSQL/Redis/scanner healthy;
  real worker-to-database checkpoint and live scanner probe pass. Probes create
  no source/domain fixture data. Provider disabled, authorization false, spend 0.
- Documentation: report/user/handoff, tests/task receipts/bugs/evaluation/screenshots,
  practical learning, current user/demo/operator guides, architecture/contracts/ADR,
  generated inventories, status/catalogue/coverage/gaps/mapping/tracker/indexes,
  roadmap, CHANGELOG, MASTER/LATEST and validators reconciled. One active home.
- BLOCKED: real-provider completion/embedding smoke by explicit user instruction;
  no paid request made. Hosted CI, archived Word visual QA and production/full
  release gates remain open. Bounded JSONB projection is an explicit ADR 016
  alternative; pgvector/ANN scale and real retrieval quality remain unverified.

Exact commands, failed runs and outcomes: [testing report](../../../04-testing/sprint-based/sprint-10/TESTING_REPORT.md).
Affected paths and remaining owner actions: [documentation matrix](../../../04-testing/sprint-based/sprint-10/DOCUMENTATION_CHECKS.md).
Task receipts: [001](../../../verification/PPM-10-001.md), [002](../../../verification/PPM-10-002.md),
[003](../../../verification/PPM-10-003.md). Exact uncommitted content revision:
[local source/evidence checkpoint](../../../verification/sprint10-checkpoint.json).

Stop before 11. Overall Sprint 10 acceptance remains OPEN while the required real
provider criterion is BLOCKED. Do not enable a provider, spend, commit/push, deploy
or start the successor without separate explicit authorization.
