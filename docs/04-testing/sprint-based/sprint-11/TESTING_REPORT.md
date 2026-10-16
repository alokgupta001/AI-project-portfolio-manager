# Sprint 11 testing report — 16 October 2026

Environment: Windows host, Python 3.12.14, Node 24.20.0; Linux Compose PostgreSQL
18/Redis and existing locked app dependencies. All acceptance data is synthetic.
Runtime test providers are disabled. Enabled-provider paths use local doubles or
intercepted HTTP with explicit network denial; real provider requests **0**, spend
**USD 0**. Paid coding/review agents were not invoked.

## Executed commands and current results

| Command / check | Observed result |
| --- | --- |
| `git fetch origin` with per-command safe.directory | PASS after sandbox DNS failure; fetched remote ancestry verified |
| Read normal `alembic_version` | 0012_ai_runtime; 70 established table hashes/private backups captured |
| `docker compose -f compose.yaml -f compose.documents.yaml --profile test run --rm --no-deps test python -m pytest tests/test_agents.py -q --tb=short` (current source mounted during focused development) | **50 passed in 69.99 s** |
| `python scripts/test_backend.py` in guarded test container | Clean/base and prior-head migration cycles plus metadata drift PASS; first full regression 250 passed, one readiness-version failure, corrected before final rerun |
| Full backend pytest with private JUnit | **251 passed in 479.94 s**, one existing Starlette/httpx deprecation warning; before final atomic-read/key correction |
| AI/fencing follow-up before cold-worker correction | **122 passed in 194.38 s**, including 51 specialist tests |
| Final affected worker/metrics/AI/provider/readiness suite | **127 passed in 167.24 s**, including **52 specialist tests**, the concurrent-completion regression and fresh-process registry regression |
| Final guarded `check_agent_migration.py` | **PASS** disposable 0012 → 0013 lifecycle; no metadata drift |
| Normal preservation verification | **PASS** all 70 table counts/hashes, five objects and 22 frozen file hashes unchanged; head remains 0012 |
| Combined browser regression run, `agents.spec.ts ai.spec.ts documents.spec.ts assessment.spec.ts --workers=1` | **AI, assessment and document journeys PASS** (36.1/10.9/29.9 s); new agent test found a keyboard issue then fixed |
| Final `node scripts/check-identity-browser.mjs agents.spec.ts --workers=1` | **1 passed in 26.0 s** (journey 24.2 s): persistent semantic accept/reject, exact evidence, real worker disabled fallback, self-review denial, 1440/768/360 WCAG and keyboard scroll checks |
| Ruff lint/format, mypy, ESLint, TypeScript, Prettier and OpenAPI/client drift | **PASS** final source checks |

The four browser journeys passed in separate applicable runs, not one all-green combined run. Final verification [receipt](../../../verification/sprint11/results.json).

## Scope of deterministic fixtures

`tests/test_agents.py` provides supported, missing, contradictory and malicious
inputs for each of the nine agents (36 cases), strict tool/shape/confidence gates,
stable duplicate merging, explicit partial failure, published-rubric weighting,
missing/invalid/duplicate matches and intercepted Gemini transport limits.

Database fixtures cover Green with an overdue critical milestone; disabled
fallback and zero calls; independent accept/reject history; original score,
answer and plan preservation; Viewer/PM/cross-tenant denial; RLS/immutable SQL;
semantic original 0, suggestion 87.5, override 75, rejection and stale answers;
quota/timeout/malformed responses; request budget exhaustion; cancellation,
lease replacement, authority revocation, source deletion and replay. The full
nine-agent path includes four-versus-five group suppression and live group
revocation. Original CodeRabbit regressions remain in the full suite. A fresh-process regression also verifies that metric registration works without web startup.

The browser fixture persists a deterministic semantic run in its own tenant.
The journey accepts/rejects as an independent reviewer, reloads history, views
exact evidence and discrepancies, checks responsive screenshots/automated WCAG,
then starts a provider-disabled durable run and verifies self-review denial.
AI, document and assessment regressions run against the actual isolated API.

The full regression and final affected suite are separate runs, not additive unique-test counts.

## Initial failures and remaining gates

[Bugs/fixes](BUGS_AND_FIXES.md) records internal typed-record serialization,
recursive RLS, SQL NULL and role-specific assertion fixes. A readiness check
still pinned to 0012 blocked the first browser startup/full regression; it now
uses the shared 0013 contract. Browser testing also corrected proxy-unsafe review keys, an omitted account-load hook, a READ COMMITTED run/job race and a keyboard-inaccessible scroll region. The first semantic browser fixture reused the
assessment tenant, causing ambiguous legacy locators; it now owns a separate
tenant. Historical test results and screenshots are preserved.

Host-only pytest hit Windows temporary-directory access/hang; Linux test
containers execute the authoritative tests. An exploratory mypy command included
historical untyped migrations; the configured CI target is application/worker
modules and is the actual static acceptance command. Applied migration files
were not changed to fix unrelated historical typing.

Real-provider semantic quality, production scale, calibration and manual
assistive-technology acceptance are **UNVERIFIED/BLOCKED**. Mock success proves
bounded controls/attribution, not interpretation quality. Hosted CI at the
uncommitted Sprint 11 revision is unrun. Normal deployment/migration is not run.

Responsive screenshots in `docs/verification/sprint11/` were visually inspected at desktop and mobile widths. Ten historical regression screenshots were restored byte-for-byte, with fresh renders saved privately. Automated checks do not replace manual assistive-technology release acceptance.

Final command: `docker compose -f compose.yaml -f compose.documents.yaml --profile test run --rm --no-deps` with read-only source/test mounts, `python -m pytest tests/test_agents.py tests/test_ai.py tests/test_gemini.py tests/test_ai_contracts.py tests/test_integration.py tests/test_command.py -q --tb=short --junitxml=/evidence/final-worker-ai-junit.xml`. Private JUnit files are under `artifacts/local/sprint11/`.
