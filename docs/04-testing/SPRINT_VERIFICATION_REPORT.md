# Sprint verification and repairs

**Current reconciliation — 16 October 2026:** Current verification is Sprint 10 at `0012_ai_runtime`: the recorded baseline is 150 backend/16 browser/12 offline gate cases; later Gemini smoke and 63 AI/provider regressions passed. See [current evidence](sprint-based/sprint-10/GEMINI-FOLLOWUP.md). The dated Sprint 09 and earlier records below remain historical; no new application test was run by this documentation audit.

**Current checkpoint — 15 October 2026:** [Sprint 09 verification](sprint-based/sprint-09/TESTING_REPORT.md)
supersedes availability/head statements below: normal head `0011_document_sources`,
123 full backend passes, 14 browser regressions plus the affected document flow passed
separately. Later sections retain historical outcomes. Development Gmail was separately
verified on 10 October; current hosted CI and Word visual gates remain open.

**Sprint 8.1 execution update:** 74 full backend checks plus focused SSE verification, 12 full browser checks plus 6 affected closure checks and all eight static gates pass. Existing 59 table hashes/counts and the object hash match after additive head 0008; scratch restore passed. See the [current report](../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md) for open SMTP, hosted CI and Word visual gates. The detailed Sprint 08 walkthrough below is retained as historical evidence.

Date: 9 October 2026 (Asia/Calcutta). Scope: implemented Sprints 00–08 only. No Sprint 09 features, paid provider calls, external messages or deployment were performed.

## Historical Sprint 08 state and evidence

Historical checkpoint latest implemented sprint: **08**, migration **0007_durable_jobs**. Git branch `main`, base `9056440`. Sprint 08 and learning materials were already uncommitted; their presence is not inferred from Git history alone. Existing edits were preserved. Git inspection used a per-command `safe.directory` override, without changing global configuration.

Scope comes from `docs/03-sprints/completed/sprint-00/SPRINT_REPORT.md` through `SPRINT-08-REPORT.md`, Sprint 08 handoff/checks, README, local/identity setup, architecture overview, coverage, and delivery/capacity/assessment/command-center/jobs contracts. Source routes, models, migration runner and test assertions were inspected together. Historical sprint results are context; PASS below refers to fresh tests from this run.

Available environment: Python 3.12.14, Node 24.20.0, npm 11.19.0, installed locked dependencies, Docker Linux engine, PostgreSQL 18, Redis 8, API, Next.js web, Linux Celery worker and dispatcher. Normal database `ppm_local` contains established data and was treated as important. Backend mutations/lifecycle tests use guarded `ppm_test` and Redis database 1. Browser tests use a separate Compose project and separate volumes, on web/API 3001/8001; normal services remain on 3000/8000. Existing `.env` configuration was checked by key/presence only. No `connector-secrets.env` exists; actual provider access is BLOCKED.

## Overall results

- Checklist: **61 grouped requirement rows** across Sprints 00–08, with explicit untested, blocked and unimplemented boundaries.
- Baseline backend: **63 passed**, with one inherited Starlette/httpx deprecation warning.
- Post-fix backend: **67 passed**, including the four added regression cases; guarded migration lifecycle/drift passed before and after the fix.
- Focused mapping unit/API checks: **4 passed**, including rejection before persistence. Two new unit cases failed against the original code, confirming missing validation.
- Existing full browser workflows: **9 passed**, including real identity, delivery, capacity, assessment, command center and durable import flows.
- Enhanced post-fix browser import workflow: **1 passed**, including visible 422 validation feedback, successful corrected import, SSE/dashboard refresh, repeat deduplication, tenant switch and zero captured page runtime errors.
- Direct SQL on persisted browser records: **seven assertions passed** for project/work persistence, archive, imported work, provenance, two partial jobs and absence of rejected connection.
- Production build: initial sandbox filesystem denial; retry with access **passed**. This is an environment failure, not an application build defect.
- Ruff, Python formatting, mypy, generated contract drift, TypeScript, ESLint, Prettier and seven original-source hashes: **PASS**. npm audit: **zero vulnerabilities**.
- Local connector mapping defect: fixed; detailed API and UI evidence below. Setup documentation corrected to the implemented checkpoint.
- Actual live Jira/GitHub authentication, externally delivered webhook and production-scale behavior: **BLOCKED / NOT TESTED**, not inferred from fixtures.

Evidence is stored under `docs/verification/current-*`; older sprint logs/screenshots were preserved. Synthetic test credentials/mailbox records stay in ignored private artifacts, not this report.

## Sprint-by-sprint checklist

Rows group related acceptance requirements; each test column identifies the concrete behavior checked. A backend PASS does not imply UI coverage beyond the separate UI rows.

### Sprint 00 — planning and preservation

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Original source and prompt preservation | Seven preserved inputs match their manifest | `scripts/check_sources.py` SHA256 comparisons | PASS |
| Implementation scope distinguished from roadmap | Implemented requirements trace to reports/code, future modules remain planned | Reports 00–08, current modules/migration chain and owning contracts | PASS for reviewed scope |
| Planning-only historical workspace validator | Verify the Sprint 00 state before application files existed | Old `check-sprint-00.ps1` intentionally not rerun against a later sprint | NOT TESTED; historical only |

### Sprint 01 — runtime foundation

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Live/ready distinction and sanitized failures | Process remains live when dependencies fail; readiness reports failure without secrets | `test_api.py`, `test_config_storage.py`; real normal readiness probe | PASS |
| PostgreSQL persistence and restricted app role | Commit/read round trip; app cannot mutate checkpoint or bypass security | `test_integration.py` on real PostgreSQL; normal role flags | PASS |
| Storage adapter and path safety | Objects survive adapter recreation; escaping keys rejected | `test_config_storage.py` | PASS |
| Real worker/broker/database chain | Celery process returns established checkpoint | Normal `scripts/smoke_worker.py`; actual subprocess recovery in job tests | PASS |
| Frontend-to-API checkpoint and reload/mobile | Browser displays real checkpoint and reloads without overflow | Two `foundation.spec.ts` cases | PASS |
| Migrations, production build and contracts | Schema lifecycle/drift passes; compiled client matches API | Guarded backend runner, build, contracts/type checks | PASS |
| Existing normal data survives service update | Existing records retain counts/hashes and original checkpoint | Fresh private before/after snapshot and worker probe | PASS; all 60 tables unchanged |
| Off-host backups and disaster recovery | Restore operational deployment elsewhere | No off-host environment configured | NOT TESTED; outside local acceptance |

### Sprint 02 — identity and tenant authorization

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Activation, invitation and supported sign-in | Single-use challenges, role-bound invitations, invalid credentials rejected | Identity integration cases and real browser lifecycle | PASS |
| Secure session lifecycle | CSRF, forged/expired credentials, refresh replay and concurrent refresh rejected appropriately | `test_identity.py` session/CSRF/replay cases | PASS |
| Logout, reset and live revocation | Revoked sessions stop authorizing; reset invalidates sessions | Identity API cases plus browser recovery/logout | PASS |
| Organization switch and roles | Admin/PM/Viewer privileges, hidden IDs and tenant policies enforced | Identity/RLS/pool-reuse/foreign-write cases and browser tenant switch | PASS |
| Final administrator and concurrency | Cannot remove/demote last active Admin; stale writes rejected | Final-admin, concurrent demotion and revision cases | PASS |
| Rate limiter and sanitized logging | Fail closed on limiter problems; secrets absent in response/log records | Identity rate-limit cases and `test_api.py` | PASS |
| Real external email delivery | Invitations/reset reach external mailbox | Implementation uses private operator mailbox | NOT IMPLEMENTED; documented local scope |

### Sprint 03 — shell and design system

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Navigation, theme and responsive drawer | Routes work; theme persists; mobile navigation remains usable | `shell.spec.ts` | PASS |
| Keyboard palette/dialogs/gallery | Commands and dialogs work from keyboard; gallery is labelled | Shell test, accessibility and keyboard assertions | PASS |
| Organization/permission-aware shell | Switching membership changes visible actions and authorized data | Shell/identity tests and later domain tenant-switch tests | PASS |
| Loading/error/empty/forbidden states | Scoped empty data and permission errors remain visible | Domain/browser empty states, API failures and permission cases | PASS for exercised states; exhaustive visual states NOT TESTED |
| Full accessibility certification | All assistive technologies and routes certified | Automated axe/keyboard/overflow checks only | NOT TESTED; broader certification not established |

### Sprint 04 — portfolio and delivery

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Hierarchy and project lifecycle | Create/list/detail/edit/archive retains records and history | `test_delivery.py`; UI portfolio/project/work lifecycle, refresh and archive | PASS |
| Work, milestones and relationships | Valid references/dates/statuses; cycles and foreign project links rejected | Delivery relationship/cycle/reference tests and browser work editing | PASS |
| Decimal money and currency groups | Budgets/spend/reversals reconcile without mixed-currency totals | Money immutability, currency-group and browser budget tests | PASS |
| Immutable baselines and audit | New forecast/baseline preserves prior plan and append-only ledger/history | Delivery backend cases and browser baseline workflow | PASS |
| Role/project access and database integrity | Unauthorized edits, tenant references and direct invalid database writes rejected | Real restricted-role RLS/composite-FK cases | PASS |
| Revisions, idempotency and concurrency | Repeated writes reuse effect; conflicting/stale edits rejected | Delivery retry/concurrent revision cases | PASS |
| Demo seed idempotency | Repeated demo seed preserves existing demo rows | Only non-demo seed refusal was rerun; no demo reseed performed | NOT TESTED for repeat demo seed; refusal PASS |

### Sprint 05 — resource and capacity

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Independent profiles/calendars/leave/allocations | Staffing persists separately from login authority | `test_capacity.py` and UI staffing lifecycle | PASS |
| Capacity arithmetic | Split-project totals, holidays, leave, zero/missing capacity, part-time and DST reconcile | Known arithmetic fixtures and daily/weekly assertions | PASS |
| Sensitive effort and coverage | Separate grant required; amendments invalidate completeness and access revokes live | Sensitive-effort/coverage/audit cases | PASS |
| Resource/project grants, revisions and snapshots | Scoped PM editing, Viewer reads, concurrent updates and immutable snapshots | Capacity integration/RLS cases and UI reload/snapshot | PASS |
| Team privacy and support signals | Cohorts under five suppressed; explicit skills/overload semantics | Team privacy and sustained-overload cases | PASS |
| Real unlimited staffing throughput | Large resource populations meet SLA | Only bounded fixture acceptance | NOT TESTED; outside local acceptance |

### Sprint 06 — maturity assessments

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Frameworks, examples and immutable versions | Validate rubric/weights/IDs and preserve old publication | `test_assessment.py` examples/publishing/invalid-input cases | PASS |
| Assignment, autosave and independent review | Respondent submits; independent reviewer releases/adjusts/completes | API two-department workflow and real browser autosave/evidence/review | PASS |
| Weighted scoring and unknown/completeness | Engineering 87.5, reviewed 75, Operations 0; missing numeric data stays unknown | Independent expected-score assertions in assessment tests | PASS |
| Evidence quarantine and scope | Only bounded text accepted; release/download requires live authorized reviewer | Assessment evidence/security cases and UI quarantined→released flow | PASS |
| Results/history/comparison | Frozen result/version survives republish; comparisons use identical version | Backend history/version assertions and UI result chart/table | PASS |
| Radar charts | Actual implementation provides dimension bars and accessible table | Source/report inspection; bars/table exercised | NOT IMPLEMENTED as radar; supported visualization PASS |
| Grant administration UI | Complete assessment access administration through frontend | Report explicitly documents API-only grant management | NOT IMPLEMENTED; API authorization PASS |

### Sprint 07 — command center and metrics

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| Executive/Delivery/Risk/Resource snapshot | Authorized metrics reconcile with source records | `test_command.py` arithmetic, scope and reconciliation cases; UI dashboard | PASS |
| Health, calendar variance and currency semantics | Defined thresholds/weights, missing coverage and currency-separated money | Arithmetic fixtures and expected source-record sums | PASS |
| Reported-vs-evidence discrepancy | Green reported status with overdue critical gate exposes discrepancy | Backend case plus browser evidence drawer | PASS |
| Risks/benefits and frozen sprint closure | Validate lifecycle, immutable velocity and explicit incomplete history | Command/delivery cases; UI risk creation | PASS |
| Filters, saved views and export | Empty filter returns no projects; private view persists; export matches authorized snapshot | Backend and `command.spec.ts` reload/filter/download assertions | PASS |
| Privacy, CSRF and retry authorization | Resource privacy retained; saved filters/replays cannot bypass access | Command security cases and Viewer switch | PASS |
| Layout and chart accessibility | Tables/axe/keyboard/overflow at desktop/tablet/mobile | Browser assertions and fresh screenshots | PASS within exercised coverage |

### Sprint 08 — durable ingestion and live progress

| Requirement | Expected behavior | How to test it | Result |
| --- | --- | --- | --- |
| CSV preview/import/mapping validation | Valid rows import; invalid rows show partial results; unsafe mappings rejected before persistence | Jobs cases, new mapping tests and real import UI | PASS; mapping fix detailed below |
| Jira issue/sprint and GitHub issue/PR fixtures | Supported mapped fields/timestamps normalize to actual delivery records | Provider fixture and historical sprint cases | PASS for fixtures |
| Durable outbox, lease and crash recovery | Actual worker crash/restart resumes with exactly 500 domain/source effects | Linux subprocess kill, expired lease and resumed-run assertions | PASS |
| Retry/backoff/dead-letter/cancel | Bounded attempts, page checkpoint recovery, cancellation retains committed effects | Jobs retry/recovery/dead-letter/cancellation tests | PASS |
| Idempotency/provenance/local edit preservation | Repeat import/delivery does not duplicate; local revision conflicts become quality errors | Job replay, source rows, DB references and revision-conflict cases | PASS |
| Worker tenant/session/role authority | Forged broker context, expired/revoked scope and foreign secret references cannot authorize work | Restricted-role jobs/RLS/revocation cases | PASS |
| Ordered SSE/resume/replay expiry/revocation | Correct sequence replay, resync and stream revocation; proxy forwards cursor | Backend SSE cases and real browser resumed terminal stream | PASS |
| Dashboard refresh after durable sync | Authorized sibling command center refreshes after terminal job | Real browser response-count assertion | PASS |
| Native GitHub signed webhook | HMAC/repository/type/replay validates; revoked delegation rejected | Signed ASGI HTTP intake and persisted job effects | PASS locally; external delivery BLOCKED |
| Real provider authentication and sync | Connect to actual authorized Jira/GitHub source | No operator credentials configured; no paid/external calls attempted | BLOCKED |
| Production proxy/throughput/retention purge | Verify deployed topology, scale and physical retention | No deployment; retained replay rows intentionally not purged | NOT TESTED / purge NOT IMPLEMENTED within this scope |

## Bugs and repairs

### B1 — overlapping mapping paths (medium; functional integrity)

**Reproduce:** create a connection mapping `external_id` to `id`, `name` to `id.title`, and `source_updated_at` to `updated_at`. Before the fix both mapping orders were accepted. In scalar-first order, `project_rows` traverses an already-projected scalar and raises a `TypeError`, which preview/enqueue do not handle as a validation failure. Reverse order overwrites the projected nested field and loses information. Either can render an immutable connection unusable.

**Root cause:** field-path syntax and target allowlists were checked, but scalar/descendant overlap was not. Projection requires every selected parent of a nested field to be an object.

**Fix:** reject strict parent/descendant path conflicts in `ConnectorConfig.mapping_allowlist`; preserve supported nested siblings and repeated identical scalar paths. No migration, dependencies, permissions or scoring changes.

**Files:** `services/api/ppm_api/ingestion.py`, `tests/test_ingestion_mapping.py`, `tests/test_jobs.py`, `tests/browser/integrations.spec.ts`.

**Verification:** two new unit cases failed before the fix; three unit cases pass afterward. Focused real API test confirms both orders return 422 and leave the integration list unchanged. Full backend increases from 63 to 67 passing cases. Browser regression submits the malformed mapping, checks visible validation feedback, restores the valid mapping and continues the existing durable import flow. See [before](../verification/current-mapping-before.txt), [unit after](../verification/current-mapping-after.txt), [API](../verification/current-mapping-api.txt), [full regression](../verification/current-backend-after.txt).

**Result: FIXED AND VERIFIED**, including [enhanced browser acceptance](../verification/current-browser-fix-retry.txt): one passed in 30.5 seconds. Desktop/tablet/mobile screenshots were visually reviewed as well as tested for overflow and serious/critical axe violations.

**Remaining concern:** no established connections were modified. A read-only normal-data query found **zero** existing connections with overlapping mappings. For other environments, a previously saved overlapping mapping requires inspection and replacement with a valid connection; immutability remains the supported contract. [Exact query/result](../verification/current-existing-mappings.txt).

### B2 — stale setup/current-state guidance (low; operational)

README identified Sprint 07 and told users to authorize Sprint 08; local setup described Sprint 03, checkpoint-only workers and unimplemented business data, and its direct browser command could skip identity-dependent scenarios without a fixture. Current limitations listed durable jobs as planned.

Updated only the relevant current guidance in README, `docs/07-setup-and-deployment/LOCAL-DEVELOPMENT.md` and `docs/02-learning/08-deployment-and-operations/OPERATIONS_AND_LIMITS.md` to Sprint 08/head 0007, dispatcher/ingestion responsibilities, isolated browser command and live-provider limits. Historical sprint reports retain their original requirements; append-only dated links point here.

### Verification failures retained

- First `npm run build`: Turbopack could not canonicalize the workspace under sandbox filesystem restrictions. Same build passed with access; no build-code workaround was introduced.
- First enhanced focused browser run: the new exact `getByLabel` selector did not resolve the mapping textarea. The page snapshot showed its textbox role/name. Corrected the test to the observed accessible role/name, retaining the rejection and import assertions. This was introduced by this verification test, not a pre-existing product defect. Failed transcript remains `current-browser-fix.txt`.
- Inherited Starlette/httpx deprecation warning remains; it does not fail the established suite. No dependency churn was performed to suppress it.

## Security, data integrity and boundaries

Real PostgreSQL tests exercise RLS under `ppm_app`, composite foreign keys, hidden tenants/projects, append-only records, session revocation, CSRF, revision conflicts and atomic retry effects. Normal role flags are non-superuser/non-bypass. Test migration lifecycle includes head→0006→head→base→head→repeat upgrade plus Alembic metadata drift; normal data is never downgraded, reseeded or reset. No applied migration was edited.

Provider fixtures prove adapter contracts and local error behavior, not real authentication. Signed local webhook tests prove intake behavior, not a deployed publicly reachable webhook. Secret references remain operator managed; values are absent from test transcripts/report. No AI component is implemented through Sprint 08, so AI provider/model testing is NOT IMPLEMENTED rather than PASS.

Explicit existing boundaries remain: lists/selector caps, bounded CSV/pages/jobs, current-state dashboard semantics, unknown imported historical closures, separate sensitive effort grants/minimum-five team suppression, plain-text manually released assessment evidence, API-only assessment access administration and retained inaccessible evidence objects. These are not silently expanded or removed.

## Runtime and data preservation

Fresh normal stack update **passed**. All **60 public table counts/hashes remained identical** across the update. Migration remains 0007; PostgreSQL/Redis/storage readiness passed directly and through the frontend proxy. Unauthenticated integrations/snapshot reads returned 401. The real worker retained the original checkpoint. No error markers were found in the last five minutes of API/web/worker/dispatcher logs at inspection time; this bounded scan does not certify all historical logs.

Direct SQL against the retained **isolated browser database** separately confirmed the UI-created project remained archived, its work item persisted, the imported work/provenance matched the expected identity/status/timestamp, both repeated imports retained exactly one accepted row and one rejected row, and no invalid connection was stored. All seven booleans were true: [query](../verification/current-browser-db.sql), [result](../verification/current-browser-db.txt). Only isolated PostgreSQL was temporarily started for this read; no rows/volumes were modified or removed.

Evidence: `current-startup.txt`, `current-preservation-before.txt`, `current-preservation-after.txt`, `current-runtime.txt` and `current-worker.txt`. Private hashes contain no exported row values. Fresh screenshots are `current-command-*`, `current-sprint-06-*`, `current-sprint-08-{width}.png` and `current-fixed-sprint-08-{width}.png`; historical screenshots were restored byte-for-byte from a pre-run backup. Normal services are left running with the fix; isolated browser containers were stopped without removing named volumes.

## Exact commands and evidence

Commands ran from the `enterprise-ppm` root in PowerShell. Long runs redirected stdout/stderr to the linked files. Docker/build/browser access was retried with required environment access; no global Git trust configuration was changed.

| Command | Outcome | Evidence |
| --- | --- | --- |
| `git -c safe.directory=C:/Users/alokg/OneDrive/Documents/Codex/enterprise-ppm status --short` / `branch --show-current` / `log -5 --oneline` | Existing main/uncommitted checkpoint inspected | Current state above |
| `docker compose ps`; `docker compose config --quiet` | Services running; configuration valid | Initial inspection / runtime |
| `docker compose --profile test build test` | PASS before/after fix | `current-backend-build.txt`, `current-backend-fix-build.txt` |
| `docker compose --profile test run --rm test` | 63 before; 67 after; lifecycle/drift PASS | `current-backend.txt`, `current-backend-after.txt` |
| `.venv/Scripts/python.exe -m pytest tests/test_ingestion_mapping.py -q` | 2 failed/1 passed before; 3 passed after | `current-mapping-before.txt`, `current-mapping-after.txt` |
| `docker compose --profile test run --rm test python -m pytest tests/test_ingestion_mapping.py tests/test_jobs.py -k 'mapping' -q` | 4 passed, 8 deselected by deliberate focused selection; all run in full suite | `current-mapping-api.txt` |
| `$env:PPM_VERIFICATION_PREFIX='current-command'; node scripts/check-identity-browser.mjs` | 9 passed | `current-browser.txt` |
| `node scripts/check-identity-browser.mjs integrations.spec.ts` | Enhanced regression failed locator; corrected retry 1 passed | `current-browser-fix.txt`, `current-browser-fix-retry.txt` |
| `.venv/Scripts/python.exe -m ruff check services scripts tests` | PASS | `current-ruff-final.txt` |
| `.venv/Scripts/python.exe -m ruff format --check services scripts tests` | PASS | `current-python-format-final.txt` |
| `.venv/Scripts/python.exe -m mypy services/api/ppm_api services/worker/ppm_worker` | PASS, 27 source files | `current-mypy-final.txt` |
| `.venv/Scripts/python.exe scripts/check_sources.py` | PASS, seven hashes | `current-sources.txt` |
| `npm.cmd run contracts:check`; `npm.cmd run typecheck`; `npm.cmd run lint`; `npm.cmd run format:check` | PASS after fix | `current-contracts-final.txt`, `current-types-final.txt`, `current-lint-final.txt`, `current-format-final.txt` |
| `npm.cmd run build` | Sandbox attempt failed; access retry PASS | `current-build.txt`, `current-build-retry.txt` |
| `npm.cmd audit --audit-level=high` | PASS, zero vulnerabilities | `current-audit.txt` |
| `.venv/Scripts/python.exe artifacts/local/current_runtime.py before` / `after` / `inspect` | PASS; 60 tables unchanged, dependency readiness/proxy and 401 protection passed | `current-preservation-*.txt`, `current-runtime.txt` |
| `docker compose up --build -d --wait` | Tested fix built into normal services | `current-startup.txt` |
| `docker compose exec -T api python scripts/smoke_worker.py` | Real Redis→Celery→PostgreSQL round trip; original checkpoint | `current-worker.txt` |
| `docker compose exec -T postgres psql -U postgres -d ppm_local -At -v ON_ERROR_STOP=1 -c $query` | Zero established overlapping mappings; exact SQL below | `current-existing-mappings.txt` |
| `docker compose -f compose.yaml -f compose.identity-test.yaml up -d --wait postgres`; `docker compose -f compose.yaml -f compose.identity-test.yaml exec -T postgres psql -U postgres -d ppm_test -At -v ON_ERROR_STOP=1 -c $query`; `docker compose -f compose.yaml -f compose.identity-test.yaml down` | PASS, read-only browser DB assertions; `$query` is preserved in `current-browser-db.sql`; ports 15433/16380/3001/8001 and origin localhost:3001 | `current-browser-db-start.txt`, `current-browser-db.txt`, `current-browser-db-stop.txt` |

## Remaining problems and final status

**NOT VERIFIED** for every implemented capability end-to-end: actual Jira/GitHub sync remains BLOCKED on operator-provisioned least-privilege credentials and an approved synthetic provider source. A deployed webhook needs an explicitly authorized reachable environment. These checks were not replaced by fixture success. The tested local workflows have passing evidence; this status does not imply they failed.

No new hosted CI run, production load/SLA, complete accessibility certification, production proxy topology or off-host disaster recovery was tested. These remain outside local sprint acceptance. Physical retention purge/service identities and broader evidence formats remain documented future decisions/features, not work started here. No normal accounts or user records were fabricated to unblock testing.
