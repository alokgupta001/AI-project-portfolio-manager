# Account, permission and website workflow repair — 10 October 2026

This is a separate follow-up to the existing Sprint 8.1 evidence. The original [18-section website walkthrough](../06-user-guides/WEBSITE_WALKTHROUGH.md) remains intact. Its execution inventory is linked below; earlier SMTP/Gmail evidence has not been relabelled as a new live-mail test.

## Baseline and scope

The workspace already contained extensive modified and untracked work. Before editing, Git status and SHA-256 hashes of 616 existing source/document/test files were captured privately. No reset, checkout, clean, table truncation, volume deletion, credential replacement or ownership reassignment was used. The running stack was Next.js on localhost:3000, FastAPI on 8000, PostgreSQL `ppm_local` with restricted `ppm_app`, Redis and worker/dispatcher services. Existing local schema head was `0008_pilot_completion`.

The baseline backend run passed **92 tests** in 142.21 seconds with one inherited Starlette/httpx deprecation warning. TypeScript and lint passed. The host production build failed before edits because Turbopack could not canonicalize the sandboxed workspace (`Access is denied`). Docker production builds subsequently succeeded. An attempted host pytest run was interrupted without results; it is not counted as a pass.

Inspection covered the full walkthrough, current gap audit/roadmap, relevant completed sprint reports, contracts, identity/membership/invitation lifecycle, UI forms/navigation, delivery/resource/assessment/command/job policies, schema/migrations, existing fixtures/tests, runtime and non-secret local relationships. Fixes reuse the existing stack and authorization model.

## Root causes and resulting behavior

| Reported issue | Confirmed cause | Correction and evidence |
| --- | --- | --- |
| A: password visibility | Password forms had no visibility control. | Shared accessible `PasswordField`, masked initially, with Show/Hide labels, button semantics and eye icon. Keyboard toggling preserves input and autofill behavior. Browser checks cover both states, invalid credentials and submission. |
| B: accounts lost after membership removal | Login required an eligible membership; sessions required an organization; the principal dependency conflated personal authentication with tenant authorization. Membership deactivation revoked tenant sessions. | Separate globally active identity, nullable selected organization and `AccountAuth` personal routes. Tenant `Auth` still requires live membership. No-member login/profile/refresh/logout work; tenant operations return 403. Other organizations and their distinct roles remain separate. |
| C: permanently editable name | The existing profile always rendered an editable name/save form. | Read-only name plus Edit name, Save and Cancel. Blank/unchanged/busy saves are disabled, revision checked server-side, drafts retained on failure. Cancel discards the draft. |
| D: incomplete profile | The organization model/response exposed too little descriptive/setup information. | Nullable description (1000), industry (120), validated HTTP(S) website (500); creation date, active member counts, setup state and existing timezone/currency. Administrators are derived from active Admin memberships and active identities. No duplicate owner authority, logo subsystem or unused country field was introduced. |
| E: setup appears unfinished | Atomic signup/first Admin persistence already existed. The profile did not display that relationship or operating setup state, and settings/calendar navigation was hard to discover. | Profile displays derived administrators and setup next steps. Existing transactional signup, one-use challenge replay protection and configuration gates are retained. Fresh website signup, settings save/reload and subsequent planning are exercised. |
| F: invited users too restricted | Invitation membership and stored roles worked; membership alone was being mistaken for portfolio/project/resource/assessment authority. Generic errors concealed the distinction. | Preserve role/grant boundaries, improve explanations and onboarding, retain idempotent membership acceptance and existing-account credential checks. Disabled identities/inviters cannot be reactivated or used for invitation authority. Tests include expired/replaced/cancelled challenges and cross-organization isolation. |
| G: calendar unavailable | Calendars were implemented but buried in the planning-record selector. The original organizations had zero calendar rows, so there was nothing to inspect. | Visible Working calendars/Resource profiles/Availability navigation, existing empty state and authenticated creation. Immutable versions, validated seven daily hour values, holidays, timezone and dated availability remain the same model. Save/reload and capacity calculations are tested. |
| H: generic errors | The HTTP exception handler discarded trusted domain messages, and several frontend clients ignored field/reason details. Duplicate grants could fall into a generic constraint error. | Shared `DomainError`, safe status/code/request ID contract, meaningful validation reasons and shared frontend parser. Duplicate grant explains that the existing grant should be edited/restored. Unknown exceptions and database internals remain sanitized. |
| I: Hement sprint creation denied | In the actual local data, Hement was a live PM with portfolio manage, but the portal project had been created by Ashu Admin. There was no direct project edit/manage grant. Portfolio manage permits creation, not editing another creator's project. | Guarded correction adds **project edit** only for that verified relationship. A rerun is a no-op. Organization role, portfolio grant, ownership, credentials and unrelated projects remain unchanged. Regression reproduces portfolio-only denial, explicit-project-grant success, initial-active sprint rejection and Viewer denial. |

The actual correction targets Hement `e33aceb1-937e-4af4-bf66-fc44a584ee73` and portal `1c152bcb-ff85-4f5b-9c18-2678ba4af628`, after checking same organization, live PM, active identity, project name/state and the existing portfolio manage grant. It refuses a changed relationship. Hement's private credentials were not reset or used for an interactive login; verification combines the matching persisted relationship with the same scoped authorization regression. The fictional Priya browser journey creates and closes a sprint under her effective project permission.

## Identity, revocation and migration safety

`0009_account_repair` adds `identity_users.active`, permits null session organization and adds nullable descriptive organization fields. Existing global users, composite membership references, invitations and project ownership are preserved. A null organization gives no tenant scope. `/auth/me`, profile, own sessions/logout and validated organization switching use personal account authentication. Every scoped request reloads live membership; roles are not trusted from old JWT claims. Refresh clears a revoked organization context. Organization switching rotates cookies and remounts the tenant workspace so old UI state does not confer authority.

Globally inactive identities fail login, existing sessions, refresh and reset/invitation completion. The explicit development operator command [`account_status.py`](../../scripts/account_status.py) requires the owner connection, preserves memberships/ownership, revokes sessions, protects the last active verified Admin and requires a new login after enabling. Organization Admin has no global-disable API. No real user's global identity was disabled in this repair.

The new worker regression revealed that checking active identity in Python alone left a globally disabled actor's job queued. `0010_account_authority` replaces the existing cancellation function with the additional global-active check, retaining its locked, identifier-scoped definer boundary and restricted EXECUTE privilege. Such work is cancelled with `AUTHORITY_REVOKED` and cannot apply effects. Worker principals, queued invitation delivery and lock-protected identity/domain mutations also recheck global status.

A private pg_dump was taken before migration. Immediately after `0009`, **all 62 established tables had identical original-column row counts and aggregate hashes**. This excludes only the new columns and schema revision. `0010` changes a function, not established rows. Local startup reached schema head **`0010_account_authority`** and healthy services. Upgrade/down-to-base/re-upgrade/idempotent-upgrade and Alembic drift checks passed on `ppm_test`. Downgrading `0009` drops only organization-free transient sessions/refresh credentials that the old schema cannot represent; it preserves accounts/memberships and loses the newly added profile/status fields. Production configuration remains rejected.

## Error contract and security review

Trusted fixed business messages retain their status and request ID. Validation details contain field paths and bounded explanations, excluding rejected input values. Public authentication remains non-enumerating. Hidden/foreign records remain 404, forbidden actions 403, state/duplicate conflicts 409, validation 422, missing revision 428 and stale revision 412. Unexpected errors do not expose stacks, credentials, SQL or foreign-record names. The shared parser is used by identity, delivery, resources, assessments, command center, integrations and pilot flows.

Regression/browser checks exercise invalid fields, duplicate grants with no duplicate record, CSRF/origin controls, missing/hidden records, unauthorized sprint creation, stale state, sanitized internal exceptions and secret-free request logs. A browser-aborted profile save displays failure while retaining the draft, then succeeds on retry. Buttons alone are not authority: server policies, scoped foreign keys, RLS and the restricted application role continue to enforce access.

Cross-organization IDs, differing organization roles, live membership revocation, refreshed/switching sessions, final-Admin protection, invitation role authority, explicit project/resource permissions, separate sensitive effort and result-only evidence privacy remain tested. The repair adds no AI access path; general AI/document retrieval is PLANNED, so there is no implemented copilot whose isolation was claimed verified here.

## Training data and walkthrough execution

[`seed_walkthrough.py`](../../scripts/seed_walkthrough.py) provisions four reserved fictional identities and **41 manifest records** in a separate Northstar Website Training organization. It uses authenticated application requests for domain records, stable identifiers/idempotency keys and a private manifest. It refuses production/mismatched databases, reserved-email adoption and inconsistent identities. It preserves deliberate edits and does not reset existing data. It sends no external email and fabricates no answers, completed result, AI output or provider success. Credentials are generated once in private ignored storage.

The repeat run and another third run both verified the same accounts/41 records. [`check_walkthrough.py`](../../scripts/check_walkthrough.py) validates roles, global verification/status, important relationships, counts and a content fingerprint. Before and after rerun, the content hash was identical: `d76d8ab13f4cc3e16029298852d505945352e20488d48a8b0bab0d5648d38abe`. The prepared sprint remains planned and the assigned assessment remains draft for user practice. [Provisioning, credentials and non-destructive reset instructions](../05-demos/WALKTHROUGH_DATA.md) explain how to use it.

The browser walkthrough uses a fresh signup and three invitations in four isolated browser contexts, separate from this prepared local data. It exercises setup, calendars/resources, portfolio/project access, delivery records, allocation and effort gates, sprint closure, six supplied evidence answers, autosave, optional quarantined text upload, independent return/resubmit/release/completion, delegated draft editing without publication, result-only sharing/revocation, project revocation/search/dashboard absence, Viewer reads, personal saved views, notifications and authorized live refresh. Browser evidence is automated; screenshots were visually inspected for the account/profile layout. This is not a claim of a separate manual click-through by a human reviewer.

See [the complete instruction inventory](WALKTHROUGH_EXECUTION_CHECKLIST.md) for every numbered action, data-table row, supplied evidence document, worksheet check and final responsibility. It names browser versus API evidence and marks conditional, external and planned branches explicitly.

## Actual verification

| Command/check | Result |
| --- | --- |
| Baseline `docker compose --profile test run --build --rm test` | 92 passed; one inherited deprecation warning |
| Final same backend command | **100 passed**, one inherited warning, 187.56 seconds; migration lifecycle and no schema drift |
| `node scripts/check-identity-browser.mjs` | **14 passed** in 2.3 minutes; complete four-person walkthrough passed in 1.6 minutes, including Viewer evidence drawer and notification mutation/reload |
| `npm run lint`, `npm run typecheck`, `npm run format:check`, `npm run contracts:check` | Passed; OpenAPI and TypeScript match |
| Ruff check / format check | Passed |
| Container `python -m mypy services/api/ppm_api services/worker/ppm_worker` | Passed, 31 source files; host uv launcher failed and is not claimed passed |
| `python scripts/check_sources.py` | All seven frozen source/prompt hashes match |
| Docker Next production build / local `docker compose up --build -d --wait` | Passed; local services healthy at schema head 0010 |
| Migration preservation and seed integrity/rerun | Passed as detailed above |
| `git diff --check` | Passed; line-ending notices only |

Private logs are under `artifacts/local/repair-20261010`: baseline/backend-final4, `browser-all-complete.txt`, earlier browser attempts and final walkthrough logs, action JSON, local-final-start/final-local-health, lint/typecheck/format/contracts/Ruff/mypy/source logs, database preservation, Hement correction/no-op and seed integrity. They contain no printed passwords/tokens. Failed test attempts remain recorded: initial null-organization JWT/test-header assumptions, a rerun-sensitive mail query and browser locator/order mistakes were corrected. The global-worker queued-state regression produced the additional migration. No failed run is counted as a pass. Final lint, TypeScript, format and contract checks passed after the last browser assertions; the retained training-data fingerprint is still unchanged.

## Documentation and Git review

Updated: the walkthrough, user/member guides, local/identity setup, permission/API/capacity contracts, current status, authentication/account-email/scoring learning chapters, testing index, feature-gap traceability and future roadmap. Added this follow-up report, instruction inventory and training provisioning guide. README and the active Sprint 8.1 report link the dated follow-up; earlier results remain historical.

The exact documentation inventory is:

| Document | Update |
| --- | --- |
| `README.md` | Links to the dated repair and training instructions |
| `docs/00-overview/CURRENT_STATUS.md` | Implemented account repair, head 0010 and remaining limits |
| `docs/02-learning/05-security/AUTHENTICATION_AND_AUTHORIZATION.md` | Optional organization authentication, live authority and scoped grant explanation |
| `docs/02-learning/05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md` | Global active status and invitation/reset/worker authority |
| `docs/02-learning/06-ai-and-analytics/SCORING_AND_DASHBOARDS.md` | Calendar/navigation, manual inputs and planned AI distinction |
| `docs/03-sprints/completed/sprint-8.1/SPRINT_REPORT.md` | Dated follow-up link; original sprint evidence retained |
| `docs/04-testing/README.md` | Repair report index |
| `docs/04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md` | This report covering the 14 requested areas |
| `docs/04-testing/WALKTHROUGH_EXECUTION_CHECKLIST.md` | 611-entry original instruction/data/constraint inventory and evidence boundaries |
| `docs/05-demos/WALKTHROUGH_DATA.md` | Guarded provisioning, private credentials, rerun/reset and operator commands |
| `docs/06-user-guides/WEBSITE_WALKTHROUGH.md` | Accurate profile/calendar/sprint labels and dated execution follow-up |
| `docs/06-user-guides/MEMBERS_ROLES_AND_ACCESS.md` | Global identity versus tenant membership/grants |
| `docs/06-user-guides/USER_GUIDE.md` | Account/profile/calendar recovery and report references |
| `docs/07-setup-and-deployment/LOCAL-DEVELOPMENT.md` | Head 0010, additive migration and operator safety |
| `docs/07-setup-and-deployment/IDENTITY-DEVELOPMENT.md` | Account without membership and global status/worker behavior |
| `docs/09-planning/FEATURE_GAP_TRACEABILITY.md` | Completed repairs versus planned follow-up |
| `docs/09-planning/FUTURE_SPRINT_ROADMAP.md` | Remaining production identity/document/AI/provider acceptance scope |
| `docs/contracts/permissions.md` | Live identity/membership/record authority contract |
| `docs/contracts/api-events.md` | Trusted domain error and sanitized field-reason contract |
| `docs/contracts/capacity.md` | Discoverable calendar navigation using the existing immutable model |

Principal implementation files are `identity.py`, `identity_tables.py`, `identity_schemas.py`, `account_mail.py`, `delivery.py`, `jobs.py`, `main.py`, `schemas.py` and new `errors.py` under `services/api/ppm_api`, plus migrations `0009_account_repair.py` and `0010_account_authority.py`. Frontend changes cover `app/account/identity-client.tsx`, `app/globals.css`, new `components/password-field.tsx` and `components/api-error.ts`, and the existing delivery/capacity/assessments/command-center/integrations/pilot clients under `apps/web`. OpenAPI/TypeScript contracts were regenerated. New account/walkthrough tests and the four operator scripts are named above; existing identity/jobs/pilot tests and browser fixtures were updated for the revised semantics.

Implementation changes are confined to identity/schema/migrations, worker/mail authority, shared errors/password control, account/profile/calendar UI, generated contracts, relevant fixtures/regressions and guarded operator scripts. The private comparison records all 616 baseline files and reports no missing files. Pre-existing dirty/untracked source work remains; no commits or PR were requested. Existing browser tests regenerate verification outputs: nine historical screenshot paths were restored from content matching their exact baseline hashes, while three previously untracked pilot screenshots and the command rendering JSON were refreshed by those tests. Those generated outputs must not be cited as earlier-sprint runs. No historical test-report text was rewritten to claim this verification happened earlier.

## Remaining limits and next actions

- Live SMTP/provider inbox delivery was not rerun. The isolated browser journey uses private local mail; earlier authorized Gmail receipt/acceptance evidence remains in [ACCOUNT_EMAIL_VERIFICATION](ACCOUNT_EMAIL_VERIFICATION.md). Remote delivery, provider failures and localhost reachability are operator acceptance concerns.
- Hement's interactive login with his private password was NOT TESTED. His verified narrow relationship/grant correction and corresponding application policy are established; he can use the existing account to perform the real browser confirmation without a password reset.
- Full timesheet coverage is conditional: the four-hour training project entry does not justify declaring a complete eight-hour resource day. The separate coverage/privacy API regression runs; the optional UI completeness assertion is deliberately not fabricated.
- Optional cross-department benchmarking and the optional 80-point reviewer adjustment are outside the basic 92.50 single-assessment path. Cohort/adjustment rules are covered by API regressions; this is not a benchmark or certification.
- Production global account administration, broad document/PDF/Word/OCR intake, Viewer submissions, live Jira/GitHub acceptance, AI copilot/forecasts, scheduled external notifications and executive PDF reports remain PLANNED or unverified under the existing roadmap. They were not built or faked to make the walkthrough pass.

The final run has no failing backend or browser tests. The external/conditional limitations above remain explicitly outside that pass count. Local API, web, PostgreSQL and Redis report healthy; worker/dispatcher remain running. The checklist records 611 original entries: 460 PASS, 147 N/A reference/conditional items, three NOT TESTED live-mail troubleshooting branches and one PLANNED broad-document intake entry. This is not a claim that planned services or external inbox delivery passed.

## Follow-up: populate the portal actually open in the user's browser

The earlier prepared seed was in a separate Northstar Website Training organization. The user was viewing Ashu's existing Northstar Invitation Test portal, whose work/sprint sections had zero records. This explains why the previous seed did not resolve the visible empty project. On the user's explicit follow-up, `scripts/fill_current_portal.py` populated that exact portal atomically using the restricted application's validated, audited command path and a verified live Admin session. It preserves existing identities, organization roles, ownership and unrelated records, and labels new business inputs as fictional demo data.

All 14 tabs now contain records: six work items, three milestones, two planned sprints, one blocker, two risks, two benefits, one metric plan, three acyclic dependencies, two budget lines, two fictional expenditures, two status updates, one frozen baseline, one goal alignment and three explicit project grants. An immutable India calendar supports the metric plan. Ashu retains Admin authority; Hement and Alok have project edit access and assigned work; Blaze has read-only access. Permission checks confirm the two PMs can edit and Viewer cannot. The repeat run created no duplicate records. The user's browser was reloaded and each of the 14 tab tables verified directly; counts/screenshots are retained privately as `current-portal-browser.json`, `current-portal-work.jpg` and `current-portal-access.jpg`. The new script passes Ruff check/format; this data-only follow-up does not constitute another full backend/browser suite run. [Exact data and guarded rerun instructions](../05-demos/WALKTHROUGH_DATA.md#the-project-in-the-users-existing-organization) are recorded separately from the original training seed.
