# Sprint 10 technical handoff

## Current continuation — 16 October 2026

Read this section before the retained historical record. Sprint 10's local
runtime is verified; the Gemini free-tier completion/embedding smoke passed and
the final no-expiry regression run recorded 63 passing cases. The user authorized
Gemini only at maximum spend $0 and confirmed the project has no billing account.
Daily expiry is removed; the saved key/project requires no daily command.

Current schema: `0012_ai_runtime`. Preserve all applied migrations, `.env`, object
volumes, established domain data and earlier uncommitted work. Use
[Gemini setup](../../../07-setup-and-deployment/GEMINI-FREE-TIER.md),
[the current user journey](USER_GUIDE.md),
[follow-up evidence](../../../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md)
and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

Defaults/test services remain disabled. The local provider selects the reviewed
Gemini free-tier models, zero tariffs/ceiling, one-time key-bound project
confirmation, four attempts/run and 20 attempts/tenant for runs created within
24 hours. The rolling request limit is separate from the removed expiry. Quota
exhaustion returns source fallback without automatic model/provider upgrades.
No API key can independently prove Google billing status; keep billing unlinked.

General model/retrieval quality, pgvector/ANN/scale, hosted CI, archived Word
visual QA and production/release acceptance remain open. The bounded smoke is not
an agent evaluation. Do not add agents, semantic scores, automatic plan edits,
commits/pushes or deployment during this documentation task. Stop before 11;
starting the successor requires the user's separate instruction.

## Historical 15 October record

**16 October addendum:** the user subsequently authorized Gemini free-tier calls
with maximum spend $0 and confirmed the Google project has no billing account.
Completion/embedding smoke passed. Use the
[current Gemini guide](../../../07-setup-and-deployment/GEMINI-FREE-TIER.md) and
[follow-up evidence](../../../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md).
The key remains private; all normal schema/data and prior checkpoints are retained.
The original 15 October handoff below remains historical, not current authorization.

15 October 2026. **Authorized local mock/fallback implementation VERIFIED. Overall
Sprint 10 acceptance OPEN; real provider BLOCKED. Stop before 11.** User explicitly
requires no real AI calls or charges until provider/model/max-spend authorization.

Actual Git: main, base b98110e, Sprint 09 and Sprint 10 work remain uncommitted.
Actual normal schema: **0012_ai_runtime**, forward from verified 0011. No reset,
clean, commit, push, external deployment, volume removal or normal/demo downgrade.
All eleven predecessor migration files, original sources/prompts and .env unchanged.
New 0012 is applied and must now remain frozen too. Exact source/evidence hashes:
[checkpoint](../../../verification/sprint10-checkpoint.json).

## Read and continue safely

[Report](SPRINT_REPORT.md), [user guide](USER_GUIDE.md),
[testing report](../../../04-testing/sprint-based/sprint-10/TESTING_REPORT.md),
[documentation matrix](../../../04-testing/sprint-based/sprint-10/DOCUMENTATION_CHECKS.md),
[ai-evidence-v1](../../../contracts/ai.md), ADR 016, AI_GATEWAY practical chapter and
AI-RUNTIME operator guide describe actual source paths and limits. Original ordered
prompt remains preserved scope evidence; revised roadmap and current instruction win.

Core files: ai.py, ai_provider.py, ai_retrieval.py, ai_schemas.py, ai_tables.py,
ai_evaluation.py/ai_evaluation_v1.json, migration 0012, AI component/page and existing
transport/shell/jobs. Runtime.index implements the Sprint 09 EmbeddingBackend seam.
Protected read-only typed tools cannot be chosen or scoped by source text. No private
assessment ingestion, metric rewrite, semantic agents or automatic plan edits.

## Verified evidence

150 full backend tests, clean/prior/base/repeated migration lifecycle and no drift;
explicit disposable 0011-to-0012 check; final 25-case AI/SSE suite; 12 offline evaluation gates; 16 real browser
regressions including source flow and full delivery/review/Viewer revocation. Visual
review at 1440/768/360 and dark mode, overflow/serious-critical axe checks. TypeScript,
ESLint/Prettier, Ruff/format, mypy (42 files), generated contracts and npm/locked
Python vulnerability audits pass. Failed/intermediate runs are retained in testing.
Full WCAG, hosted CI and real provider/model accuracy are not inferred.

Quiesced normal preservation: **66 established table counts/hashes unchanged**,
**five original object hashes unchanged**, **21 unique frozen file hashes unchanged**.
Private database dump/object tar/working-tree patch/untracked archive/manifests are
ignored under artifacts/local/sprint10. Never publish them. Earlier uncommitted
Sprint 09 screenshot bytes and tracked legacy evidence restored; sixteen new
regression renders saved with Sprint 10 prefix. Existing pgAdmin/volumes retained.

Normal web/API/worker/dispatcher/scanner/PostgreSQL/Redis are healthy. Foundation
checkpoint remains 44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c. Read-only real worker round trip
and non-persisted live scanner probe pass. [Runtime probe](../../../verification/sprint10-runtime-probe.json)
confirms disabled provider, real-call authorization false and zero USD ceiling.
No normal source/demo fixtures were inserted. Migration/object comparison occurred
before restarting application services, avoiding concurrent session churn.

## Limits and next owner action

Keep real calls disabled. Provider/model/positive-spend selection requires a new
explicit user authorization; then a separately recorded real completion/embedding
smoke and relevance/citation evaluation are needed. Existing deterministic doubles
never establish real-provider success. Admin-only costly analyses match the absence
of an explicit PM analysis grant. Charges retain conservative per-attempt caps and
unknown outcomes; they are not invoices. Crashed work fails rather than buying
another attempt on broker replay. Inspect before creating a new run.

ADR 016 records bounded JSONB exact vectors on the existing PostgreSQL image:
20 chunks/index, 200 permitted semantic candidates, else keyword fallback. pgvector/
ANN/large-source scale/performance are unverified; no hidden image/extension change.
Production storage/retention/erasure/recovery, availability, hosted CI at reviewed
revision and archived Word every-page visual QA remain open. Preserve those gates.

Documentation validators retain Sprint 09 coverage and add Sprint 10 hubs/status
boundaries. Re-run inventory/check/source/diff only for subsequent edits; refresh the
local checkpoint last. User must separately authorize Sprint 11; do not start it.
