# Current guided review handoff

**Current disposition — 25 October 2026:** Sprint 11/11.1 is complete for the
local guided-sample scope; Sprint 12 local foundations are ready to start, not yet
implemented. Broad AI accuracy **AT17 remains BLOCKED**. Normal schema is 0016;
Gemini/Puter/Groq guided access covers the two approved projects with shared
50/day provider ceilings. See [the closeout](../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md) and
[reconciled plan](../09-planning/LOCAL_SAMPLE_PLAN_UPDATE.md) for evidence, current scope and the Sprint 12 prompt.
This supersedes older runtime/rollout/stop statements below; dated test results
and original full-product acceptance requirements remain unchanged.

**Owner direction, 25 October 2026:** prioritize local sample use now. Keep the
working 50/day configuration; defer deployment-specific improvements to
[FUTURE_DEPLOYMENT_POINTS](FUTURE_DEPLOYMENT_POINTS.md). No new keys, paid service,
production rollout or broad AI qualification is required to continue this sample.
Existing protections and unresolved acceptance statuses remain in place.

24 October 2026. Read this and [TRY_IT_NOW](TRY_IT_NOW.md) before older sprint notes.

**25 October quota follow-up:** the user asked whether the cap can be 50/day.
[QUOTA_REVIEW](QUOTA_REVIEW.md) now records actual Gemini free-project quotas
(500/day) and Puter's 962.41/1,000 remaining monthly credits, plus the token-cost
estimate. The requested ceiling is now 50/day per provider with unchanged pacing,
scope and history. Gemini's private runtime guard is also 50. No stress/model calls
or provider billing changes were made. Puter allowance remains token-dependent;
50 successful calls every day for arbitrary payload sizes is not guaranteed.
Project activation below is complete; no scope approval is pending.

**Latest access update:** normal schema is now **0016_guided_project_access**.
Alok Gupta, Hement, Blaze and Ashu have verified demo-only Admin memberships and
explicit guided grants for Customer Onboarding Portal, preserving their existing
business roles. See [USER_ACCESS](USER_ACCESS.md) for current receipts and validation.
The user explicitly approved Customer Onboarding Portal's bounded payload to all
three providers. Its scope is now activated; the earlier approval block is resolved.
All nine assigned routes and four grants were checked without model calls; raw
documents, other projects and broad semantics remain blocked. Shared caps and
quota/failure/quarantine history were preserved. See private `scope-activation.json`.
No additional live calls were made. Local services are healthy, established data
and objects preserved. Code remains uncommitted. The following 0015 deployment
and test counts describe the preceding guided-mode checkpoint.

The user's current scope is to review Sprint 11.1 and deliver a limited usable
solution with supplied Gemini/Puter/Groq, plus a separate limitations folder.
No new key, paid service, Ollama or Sprint 12 execution is required. Do not promote
the failed broad semantic qualification or edit earlier labels/attempt receipts.

Normal `ppm_local` is now schema **0015_agent_task_runtime**, with existing data
backed up and preserved. API/worker/web guided mode is active through
`compose.guided.yaml` plus the ignored `artifacts/local/guided-review/cloud.compose.yaml`;
cloud is enabled only for the explicitly approved synthetic demo. Separate organization:
`da69d9f9-e400-5268-941e-b091c8c8e611`, project
`3ba23317-7ce9-540c-9ca8-b34303d74c08`. The ignored private login is
`artifacts/local/guided-review/demo-login.json`. Never print its password or keys.

Source is dirty on `sprint-11-1-review-closeout`, base `e3bf8a3`, with 21 prior
artifact changes preserved. No commit/push/new PR performed. This limited work is
additional to the earlier PR #5 closeout; its original AT17 block remains.

Verification: full backend 509 passed/one skipped, migration lifecycle/drift,
two browser journeys, responsive/axe checks, full mypy, Ruff, frontend typecheck,
lint, formatting, contracts and frozen inputs passed. Actual normal financial,
risk and executive runs persisted with nine checklists and no provider call.
Actual localhost UI demo login, guided default, agile sprint observation, nine
checklists and logout also passed; `local-demo.png` was visually inspected.
Risk has insufficient composite evidence; use agile_coach for the Puter demo.
See [report](IMPLEMENTATION_REPORT.md) for evidence and preservation detail.

**Scoped approval received and activation completed.** The user explicitly approved
synthetic demo only. The original automatic-review scope block is resolved for
that scope. All three live financial/agile_coach/executive runs succeeded through
Gemini/Puter/Groq respectively, with exactly one request each and $0 recorded.
All three saved API results displayed/reopened correctly without new provider calls.
See [live verification](LIVE_API_VERIFICATION.md), [scope](API_DATA_SCOPE.md) and
[start/disable commands](TRY_IT_NOW.md). No further live call is needed for this task.

The private copied profiles retain `benchmark_only=true`, empty broad qualified
classes and original credential bindings/quota_scope IDs. Only guided selection
for the single demo tenant/project is allowed. Account caps are ten/day, one/minute,
one concurrent; older ledger usage was outside the prior 24-hour window. Original
policy and historical ledgers are unchanged; no quarantine was cleared. Do not run
old benchmarks concurrently. Other projects, broad tasks and raw document categories
were verified blocked. Never expand the approved scope without operator instruction.

No remaining implementation action for this limited-mode request. Broader semantic
quality, production and future sprint gates remain in the limitations register.

Commands already checked, from repository root:

```text
npm run typecheck
npm run lint
npm run format:check
npm run contracts:check
.venv/Scripts/ruff.exe check services scripts tests
.venv/Scripts/ruff.exe format --check services scripts tests
.venv/Scripts/mypy.exe services/api/ppm_api services/worker/ppm_worker
.venv/Scripts/python.exe scripts/check_sources.py
docker compose --profile test run --rm test
PPM_TEST_AI_V2=1 node scripts/check-identity-browser.mjs guided-review.spec.ts agents-v2.spec.ts --workers=1
```

The last command's environment assignment is shell notation; in PowerShell set
`$env:PPM_TEST_AI_V2='1'` first. Do not rerun passing full suites without a change
or concern. Private receipts/backups are in `artifacts/local/guided-review/`.
