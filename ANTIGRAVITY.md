# Antigravity entry point — next sprint

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
- Keep a small checklist in `docs/sprints/SPRINT-06-REPORT.md` while working: done,
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
