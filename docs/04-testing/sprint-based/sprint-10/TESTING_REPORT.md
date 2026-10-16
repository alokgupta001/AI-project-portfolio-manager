# Sprint 10 checks

**Closeout — 16 October 2026: Sprints 8.1 and 10 are COMPLETED for their implemented development scope.** The reviewed application checkpoint `631c149` passed [hosted CI](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/38885041673), including regression, migration and browser checks. The current pilot Word guide is rendered and visually verified in the linked closeout evidence. Earlier blocked/active statements below describe their recorded checkpoints. Production deployment, broad real-model/agent quality and scale remain OPEN release/successor gates. Stop before 11. [Closeout](../../../10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md).

## Historical record before closeout

## Current evidence and documentation status — 16 October 2026

The original 15 October disabled-provider checkpoint below is retained history.
The user later authorized Gemini free tier at $0; bounded real completion and
256-dimension embedding smoke passed, and daily confirmation expiry was removed.
The final expiry-removal regression recorded 63 AI/provider passes. See
[follow-up results](GEMINI-FOLLOWUP.md) and the
[current cross-sprint documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).
The missing-key authorization blocker is resolved. General model/retrieval
quality, scale, hosted CI, archived Word visual QA and production/release gates
remain unverified. Stop before 11; this audit adds no application/provider work.

## Historical 15 October record

15 October 2026. Base main b98110e plus preserved uncommitted Sprint 09/10 changes.
Local implementation gates and the preservation-verified normal forward rollout passed.
Overall Sprint 10 acceptance **OPEN**: required real-provider smoke is **BLOCKED**
by explicit user instruction (mocks/fallback only, no paid calls). Stop before 11.

All logs below live under docs/verification/. Python commands on Windows used
.venv/Scripts/python.exe; npm/node use the existing locked workspace. Docker commands
run from repository root. Only test/ppm_test underwent destructive lifecycle checks.

| Actual command / environment | Result | Evidence filename |
| --- | --- | --- |
| docker compose -f compose.yaml -f compose.documents.yaml --profile test build test | Final test image built, existing lockfiles/runtime packages retained | sprint10-test-image-accepted.txt |
| Same Compose profile: run --rm --no-deps test python scripts/test_backend.py | **150 passed**, one inherited Starlette TestClient deprecation warning, 296.40 s; clean/prior/base/repeated upgrade and Alembic drift passed | sprint10-backend-accepted.txt |
| Same test service: python scripts/check_ai_migration.py | Guarded 0011 downgrade/0012 upgrade and no drift passed | sprint10-migration-accepted.txt |
| Same test service: pytest -q tests/test_ai.py (initial slice) | 13 passed, 34.58 s; later expanded checks included in 150-pass full run | sprint10-ai-initial.txt |
| python scripts/evaluate_ai.py | Twelve versioned offline validator cases passed; real-provider acceptance BLOCKED | sprint10-evaluation.json |
| node scripts/check-identity-browser.mjs tests/browser/ai.spec.ts | Corrected focused no-key journey passed, 38.4 s | sprint10-browser-third.txt |
| node scripts/check-identity-browser.mjs | **16 passed (4.0 m)**, including corrected responsive AI page and complete delivery/review/Viewer-revocation walkthrough | sprint10-browser-all.txt |
| npm run typecheck; npm run lint; npm run format:check; npm run contracts:check | PASS, generated OpenAPI/TypeScript match; 106 operations / 93 paths | sprint10-types.txt; sprint10-lint.txt; sprint10-format.txt; sprint10-contracts-check.txt |
| ruff check services scripts tests; ruff format --check services scripts tests; mypy services/api/ppm_api services/worker/ppm_worker | PASS at final recorded static checkpoint; mypy 42 source files | sprint10-ruff.txt; sprint10-python-format.txt; sprint10-mypy.txt |
| npm audit --audit-level=high | Zero vulnerabilities | sprint10-npm-audit.txt |
| Existing frozen uv export plus pinned pip-audit==2.9.0 in test image | No known vulnerabilities; retains no-hashes/no-deps advisory warning | sprint10-python-audit.json; sprint10-python-audit.txt |
| python scripts/sprint10_preserve.py files; database before | Private patch/untracked archive, frozen files, database/object backup and 66 table counts/hashes captured before upgrade | Private ignored artifacts/local/sprint10; public summaries in preservation logs |
| docker compose -f compose.yaml -f compose.documents.yaml build api worker dispatcher migrate web | Normal images built without upgrading data | sprint10-normal-build.txt |
| Same Compose: run --rm --no-deps migrate | Forward-only normal 0011 to **0012_ai_runtime** applied | sprint10-normal-migration.txt |
| python scripts/sprint10_preserve.py database after | **66 established table counts/hashes unchanged** before application restart | sprint10-preservation-database.txt |
| python scripts/sprint10_preserve.py objects; check | **Five original object keys/byte hashes**, .env, all eleven applied migrations and frozen sources/prompts unchanged (21 unique frozen paths) | sprint10-preservation-objects.txt; sprint10-preservation-files.txt |
| python scripts/sprint10_regression_evidence.py | Sixteen fresh regression renders saved with Sprint 10 prefix; original tracked/uncommitted Sprint 06–09 evidence restored | sprint10-regression-preservation.txt |

## Positive, negative and failure matrix

Seventeen AI integration tests plus eight pure contract cases are included in the
full 150-test total (parameterized cases count as pytest cases). The full suite
retains identity, delivery, resources, assessments, metric, source/parser, pilot,
worker and ingestion regressions. Exact collection/results are in the accepted log.

- Two tenants/overlapping names; Admin/PM/Viewer; foreign run/source IDs; hidden counts;
  real app-role RLS without context and after pooled tenant switching; CSRF/revision/
  idempotency conflicts and private Admin diagnostic denial.
- Prompt injection remains quoted data; arbitrary tools/scope/mutation inputs fail;
  malformed provider output cannot publish reasoning; SSE stages contain no source,
  query, provider body, credential or private reasoning.
- Latest-version byte/text/citation integrity; superseded/deleted evidence withheld;
  embeddings invalidated on append/deletion/reprocess; in-flight indexing cannot
  publish after tombstone; legal hold retains originals.
- Concurrent budget reservations serialize; over-budget/concurrency requests fail;
  bounded quota/timeout/retry and conservative replay accounting; unknown outcomes
  retain charges; circuit opens, cooldown/probe recovers; malformed/nonfinite/zero/
  wrong-dimension embeddings fail safely.
- Actual async attempt deadline (shortened in the deterministic fixture), queued
  deadline, cancellation, live Admin revocation, broker crash/replay and worker
  token fencing block unauthorized late publication. Partial branch failure preserves
  only supported source fallback; missing evidence stays unavailable.
- Unsupported numerical output and foreign/duplicate/deleted citations fail the
  exact-excerpt evaluation gate. No normal metric formula or assessment score is
  recomputed by AI. Existing private-evidence regressions remain in the full suite.

## Real browser and visual review

The real isolated 3001/8001 journey uses actual DB/API/scanner/jobs and no model key.
It covers loading/empty/disabled, current source fallback, no-evidence, stage progress,
citation reads, Admin diagnostics, budget-limit failure, transport-error recovery,
Viewer denial and organization reset. Automated checks at 1440/768/360 pass overflow
and axe serious/critical gates; light/dark screenshots were visually inspected.

Canonical corrected renders: [desktop](../../../verification/sprint10-ai-1440.png),
[tablet](../../../verification/sprint10-ai-768.png), [mobile](../../../verification/sprint10-ai-360.png),
[dark](../../../verification/sprint10-ai-dark.png). Mobile diagnostic table now scrolls instead
of compressing headings. Other fresh regression renders use sprint10-regression-*;
historical evidence bytes were restored. Keyboard focus and existing shell tests
pass; this is not complete assistive-technology or WCAG certification.

## Retained failed/intermediate runs

sprint10-backend-full.txt: 149 passed / one missing fixture import; corrected.
sprint10-backend-final.txt: interim image stopped after static review caught a
missing json import; no acceptance inferred. Initial Ruff/mypy/format logs retain
integration corrections. sprint10-browser-initial.txt: organization-switch cookie
race (401); sprint10-browser-second.txt: missing isolated timezone/currency (409).
Both fixture issues were corrected before the focused/full accepted runs. The
layout issue came from visual review, not a false automated accessibility claim.

## Remaining gates

Real-provider completion/embedding smoke and model retrieval/relevance quality are
BLOCKED, not passed by doubles. Separate record: sprint10-real-provider-status.json.
Full Sprint 10/full-product acceptance remains OPEN. Bounded JSONB exact vectors
are an explicit interim ADR 016 deviation; pgvector/ANN/large-source/scale performance
is unverified. Hosted CI at this uncommitted revision, archived Word every-page
visual QA, production storage/retention/erasure/recovery, availability and full
release criteria remain open. No Sprint 11 work, paid provider call, commit/push
or external deployment occurred.

## Normal runtime and final closure

| Actual command | Result | Evidence under docs/verification |
| --- | --- | --- |
| docker compose -f compose.yaml -f compose.documents.yaml up -d --no-build --wait | All normal services healthy; existing pgAdmin and volumes retained | sprint10-normal-start.txt |
| python scripts/sprint10_runtime.py | API readiness and /ai HTTP 200; actual 0012; provider disabled, real-call flag false, zero USD ceiling | sprint10-normal-runtime.txt; sprint10-runtime-probe.json |
| docker compose exec -T api python scripts/smoke_worker.py | Real Redis/Celery/PostgreSQL checkpoint passed, original installation UUID retained | sprint10-normal-worker.txt |
| Normal API live scan of synthetic bytes | clamd-instream passed; no object/source/domain record created | sprint10-normal-scanner.txt |
| Final isolated pytest -q tests/test_ai.py tests/test_ai_contracts.py | **25 passed, 47.83 s**, including already-connected SSE revoked/cancelled during provider work; no source/credential leakage | sprint10-security-final.txt |
| Final documentation inventory / drift / link / source / frozen-file / static / whitespace checks | Actual commands/exit codes recorded in final-checks JSON and individual logs | sprint10-final-checks.json |
| python scripts/sprint10_checkpoint.py | Final exact uncommitted source/evidence hashes; original frozen inputs unchanged | sprint10-checkpoint.json; sprint10-checkpoint.txt |

The supplemental test adds assertions to the existing in-flight revocation fixture;
application code is unchanged from the 150-pass full/backend and 16-pass browser
candidate. Earlier full results are not relabeled as a new full run. Normal probes
are read-only or non-persisted; isolated fixture work never changes normal data.
