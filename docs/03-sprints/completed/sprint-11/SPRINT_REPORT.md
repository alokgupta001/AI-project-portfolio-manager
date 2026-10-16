# Sprint 11 implementation report

## Status and scope

16 October 2026. PPM-11-001/002/003 are implemented for deterministic local
acceptance. Real-provider semantic quality is **UNVERIFIED/BLOCKED**; production
and scale acceptance remain open. Base 77b330a on `close-sprints-8-1-and-10`, with
uncommitted Sprint 11 changes. No commit, push, merge, deployment or Sprint 12 work.
Final executed validation is recorded in the [testing report](../../../04-testing/sprint-based/sprint-11/TESTING_REPORT.md).

Source authority: Word modules 1/2/5 and Supplementary Specification section 4.3;
F-023–025, F-040–049, F-066/067/070–072; gaps G-014/016/017. The current direct
authorization supersedes historical stop-before-11 statements. Original sources,
applied migrations and frozen prompts remain intact.

## What was built and why

`/agents` provides nine specialist outcomes, run details/live stages, cited
recommendations, discrepancy/conflict views, semantic maturity comparisons and
independent review. Financial, Schedule, Sentiment, Risk, Resource, Governance,
Agile Coach, PMO and Executive have explicit input/tool allowlists, strict typed
outputs, exact source spans, bounded timeout, fallback and four evaluation cases.
This makes hidden-risk evidence reviewable without changing a reported Green
status, a project plan or an original maturity score.

Admin starts bounded analyses. Independent project editors review ordinary
findings; assessment-linked runs require the named independent reviewer plus
project scope. Original deterministic scores, AI suggestions and approved scores
are separate columns and records. Confidence is a distinct, uncalibrated support
indicator. Acceptance means reviewed, never applied. Review reasons/history are
append-only, and agents have no approval or mutation tool.

## How it works

`agents.capture` reuses `command.snapshot`, document citations and assessment
evidence authority. Snapshots retain framework/assessment/source/model/prompt/rule
versions and hashes. `ai.create` admits the existing budget/concurrency reservation
and commits the analysis, AI ledger, durable job, audit and outbox together.
`ai_worker` dispatches `agents.execute` under the existing fenced lease.

One bounded structured completion batches all specialists and rubric matches
within unchanged request/retry/output ceilings. The strict support gate permits
only known authorized source spans. Duplicate category/signal/source sets merge
deterministically; conflicting signals stay linked. Missing/failed agents remain
explicit. Shared overdue-critical and reported-health discrepancies survive a
provider failure. No metric formula is duplicated.

Semantic rubric levels use `assessment.compute_scores` with unchanged published
weights. Missing numeric-question matches make the dimension unknown. Review
records retain decisions, reasons and optional overrides without writing existing
assessment answers/results. Evidence is reauthorized before inference,
publication, display and acceptance. Edited/revoked sources or changed assessment
revisions withhold unsupported suggestions; current support is separate from
historic execution success.

Sentiment uses a fixed server-created team blocker summary only after existing
minimum-five group checks. It does not analyze individual notes, label emotions,
diagnose people or rank performance. This is deliberately a limited group support
signal, not a trained sentiment-model claim.

## Implementation record

- `agent_schemas.py`, `agent_engine.py`, `agent_provider.py`, `agents.py`: strict
  registry, read-only interpretation, aggregation, semantic support and review.
- `agent_tables.py`, forward `0013_specialist_reviews`: two tenant tables, RLS,
  composite references, write-once snapshots/results and append-only decisions.
- `ai.py`/`ai_schemas.py`: additive agents operation using the existing ledger,
  accounting, leases and cancellation; old query/index replay hashes preserved.
- `main.py`/`schemas.py`: registered routes and 0013 readiness contract.
- `command.py`: metric registry registration available to cold worker processes;
  `ai.access` observes a coherent run/job snapshot during concurrent completion.
- `apps/web/components/agents.tsx`, `/agents`, shell/auth integration and scoped
  responsive CSS: accessible evidence/review workflow using current UI patterns.
- Generated OpenAPI/TypeScript and three source inventories refreshed.

No dependency, provider/model allowlist, Gemini confirmation, spending ceiling,
request ceiling or paid fallback was added or changed. The six PR #1 fixes remain
in the baseline and their regressions are included. See [contract](../../../contracts/agents.md)
and [ADR 017](../../../architecture/adr/017-specialists-and-human-review.md).

## How to use and demonstrate

Follow the [user guide](USER_GUIDE.md), [practical trace](../../../02-learning/06-ai-and-analytics/SPECIALISTS_REVIEW.md)
and [isolated demo](../../../05-demos/sprint-based/sprint-11/README.md). All new
acceptance uses deterministic doubles/intercepted HTTP with a hard network denial.
Mock interpretation success is not real-provider quality evidence.

## Verification and preservation

The [testing report](../../../04-testing/sprint-based/sprint-11/TESTING_REPORT.md),
[three work-package receipts](../../../verification/PPM-11-001.md) and
[documentation closure](../../../04-testing/sprint-based/sprint-11/DOCUMENTATION_CHECKS.md)
record commands, outcomes, fixtures and remaining gates. Prior 201 backend passes
and the PR #1 document browser pass remain historical results; this task runs
fresh tests. Initial implementation defects and corrected reruns are retained.

Fetched remote references first; merged Sprint 09/10 and PR #1 are ancestors of
the current branch. Existing tree was clean. Normal schema head was read as
0012; private DB/object backups and 70 established table hashes were captured.
Only disposable `ppm_test` databases received migration/lifecycle tests. The
normal database, stored objects, credentials and original source/prompt/migration
files are preserved. No normal deployment or bootstrap occurred.

## Remaining gates and next boundary

Real-provider interpretation quality, broader semantic relevance, calibrated
confidence, emotional sentiment, larger assessment batching and production
performance/assistive-technology testing remain unverified. The 512-token output
limit can yield partial/malformed output for large inputs; the product exposes
that limit honestly instead of increasing budgets. Conservative evidence
recapture can withhold all evidence when a selected source fails authority.

0013 is ready and tested, but intentionally not applied to the normal 0012
database during this no-deployment task. Hosted CI at the uncommitted Sprint 11
revision is unrun. Historical hosted CI/Word closeout remains valid for its own
checkpoint. Sprint 12 is the next planned dependency; it has not begun and needs
separate authorization. [Handoff](HANDOFF.md).

Final validation: full earlier regression **251 passed**; final affected worker/metrics/AI set **127 passed** (overlapping counts), including **52 specialist tests**; four browser journeys passed across their latest applicable runs. Migration, static, generated-contract, source/documentation and preservation checks pass. [Machine receipt](../../../verification/sprint11/results.json).
