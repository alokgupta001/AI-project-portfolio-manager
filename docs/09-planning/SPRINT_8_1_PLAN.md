# Sprint 8.1 — Product Gap Closure and Completion Readiness

**Execution update 2026-10-09:** Sprint 8.1 local implementation is recorded in the [report](../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md); parent acceptance remains OPEN. The planning baseline below is historical. Future task scope and release criteria remain unchanged; no next sprint was started.

**Historical planning baseline (before Sprint 8.1 execution):** 9 October 2026. Documentation only; no feature work is authorized by this pack.** Sprint 08 is complete locally; Sprint 8.1 is proposed, not started. Numbers describe execution order, not dates or delivery promises. The frozen source specifications and original prompt pack remain intact. For future work, this pack supersedes the earlier gap review and the future sections of the original ordered prompts; those prompts remain historical scope evidence. Completed reports retain their original meaning.

Read the [audit](SPRINT_8_1_GAP_AUDIT.md), [Sprint 8.1 plan](SPRINT_8_1_PLAN.md), [future roadmap](FUTURE_SPRINT_ROADMAP.md), [traceability](FEATURE_GAP_TRACEABILITY.md), and [release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) together. A later implementation session must read the latest handoff and current working tree before using these plans.

## Objective and boundaries

Let a new user create or join an organization, understand access, find records and test the existing operational app without unexplained dead ends. Stabilize the existing modules before document/AI expansion. This is an **operational pilot completion gate**, not completion of the original AI-PPM vision.

Ten work packages are ordered below. Split implementation into three reviewable slices: identity/setup (001–003), access/discovery/inbox/metadata (004–008), refresh and evidence (009–010). One developer should not assume they fit a fixed two-week sprint. Keep the parent open until acceptance passes; preserve task IDs if sub-slice reports are needed. Implement P1 first; P2 refresh can be explicitly carried into 09 only with a recorded incomplete parent gate and no claim that 8.1 fully passed.

Entry: normal migration head 0007, local accepted 08, current source/test baseline recorded, working tree inspected, no unrelated work discarded. Take database/object manifests before implementation migrations. Use isolated test databases, additive migrations and explicit contracts. Do not reuse or modify frozen migrations.

## Prioritized work

**Historical pre-execution evidence for PPM-81-001:** G-001 NOT IMPLEMENTED — Login, bootstrap activation and invitation acceptance exist; there is no public registration page or endpoint. A first customer needs operator assistance. (evidence I)

**Existing relevant files:** `apps/web/app/account/identity-client.tsx`, `scripts/bootstrap_identity.py`, `scripts/local_mailbox.py`, `services/api/ppm_api/identity.py`, `services/api/ppm_api/identity_schemas.py`, `services/api/ppm_api/identity_tables.py`, `tests/browser/identity.spec.ts`, `tests/test_identity.py`.

### PPM-81-001 — Verified sign-up and first organization

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** PPM-81-002 for end-to-end mail; existing identity guards.

**Change and user benefit:** Add request/verify registration and a sign-up link. Reuse challenge hashing, throttling and transaction boundaries; avoid revealing existing emails. Keep pending registration separate from membership. After verification, create a named organization with only its first Admin, or accept a scoped invitation. Existing accounts sign in instead of becoming duplicated users.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Add only a new forward migration if pending-registration fields are necessary; never edit 0002/0007. |
| AI / data | None; no model calls. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** An unaided new user can verify an address, set a password and reach their own organization. Concurrent same-email requests produce one user; retries do not duplicate an organization. Invalid, expired, replayed or foreign invitation tokens grant nothing.

**Tests:** API: registration/replay/concurrency/tenant isolation. Browser: sign-up → verify → setup → logout/login; existing account and expired-link paths.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-002:** G-002 PARTIAL — Challenges are written to a local filesystem mailbox; users cannot receive mail through a configured external provider. Pending invitation listing, resend and cancellation are absent. (evidence I)

**Existing relevant files:** `apps/web/app/account/identity-client.tsx`, `scripts/bootstrap_identity.py`, `scripts/local_mailbox.py`, `services/api/ppm_api/identity.py`, `services/api/ppm_api/identity_schemas.py`, `services/api/ppm_api/identity_tables.py`, `tests/browser/identity.spec.ts`, `tests/test_identity.py`.

### PPM-81-002 — Account email and invitation management

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** Identity challenge logic and Sprint 08 outbox; adapter contract before 001.

**Change and user benefit:** Introduce a small delivery adapter for verification, activation, invitation and reset messages. Use durable delivery status and bounded retries without reusing an expired interactive user session as permanent authority. Keep token material private and out of job diagnostics. Add Admin pending-invite list, resend/cancel, and safe local operator preview. Provider-disabled mode must explain how a local tester obtains a link.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Forward migration for invite/delivery state only if current challenge fields cannot represent lifecycle. |
| AI / data | None; identity delivery is independent of AI/report delivery. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** Provider fixture sends each template; a configured real provider sends a test-to-self with arrival evidence. Cancelled/replaced tokens cannot create membership. Generic reset responses resist account enumeration. No public mailbox endpoint or logged token is introduced.

**Tests:** Adapter timeout/ambiguous delivery/retry/redaction tests; Admin/PM/Viewer invite tests; browser resend/cancel; real delivery marked BLOCKED until a provider is configured.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-003:** G-003 PARTIAL — Organization membership and account/session screens work. No guided organization setup, editable organization profile or completion checklist is present. (evidence I,U)

**Existing relevant files:** `apps/web/app/account/identity-client.tsx`, `apps/web/app/system/page.tsx`, `apps/web/components/shell.tsx`, `apps/web/components/workspace-home.tsx`, `scripts/bootstrap_identity.py`, `scripts/local_mailbox.py`, `services/api/ppm_api/identity.py`, `services/api/ppm_api/identity_schemas.py`, `services/api/ppm_api/identity_tables.py`, `tests/browser/identity.spec.ts`, `tests/test_identity.py`.

### PPM-81-003 — Guided setup and basic organization profile

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 001/002 for new users; existing organization and home screens.

**Change and user benefit:** Add a home checklist linking real existing forms: organization name, member invitation, portfolio/project, resource profile, framework/assessment and dashboard. Allow Admin organization profile edits and user display-name edits; explain that a login user and a resource profile are different. Show explicit sample-data opt-in with existing delivery seed support and a preview, rather than creating records silently.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Minimal profile fields by forward migration if required; demo seed must be tenant-bound and idempotent. |
| AI / data | None. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** Checklist derives completion from stored data, survives reload and respects roles. New PM sees usable next steps without Admin links. Organization edits are scoped/audited. Demo labels and cleanup instructions distinguish sample from real data.

**Tests:** Browser first-use/returning-user/mobile/keyboard; two-tenant edit tests; empty organization and no-permission cases.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-004:** G-004 PARTIAL — Domain permissions exist; assessment access grants are API-only. Ownership does not itself grant access and sensitive effort requires a separate grant. (evidence I,D,C,A)

**Existing relevant files:** `apps/web/app/account/identity-client.tsx`, `apps/web/components/assessments.tsx`, `apps/web/components/capacity.tsx`, `apps/web/components/delivery.tsx`, `scripts/bootstrap_identity.py`, `scripts/local_mailbox.py`, `services/api/ppm_api/assessment.py`, `services/api/ppm_api/assessment_tables.py`, `services/api/ppm_api/capacity.py`, `services/api/ppm_api/capacity_schemas.py`, `services/api/ppm_api/delivery.py`, `services/api/ppm_api/identity.py`, `services/api/ppm_api/identity_schemas.py`, `services/api/ppm_api/identity_tables.py`, `services/api/ppm_api/ppm_schemas.py`, `services/api/ppm_api/ppm_tables.py`, `tests/browser/assessment.spec.ts`, `tests/browser/capacity.spec.ts`, `tests/browser/delivery.spec.ts`, `tests/browser/identity.spec.ts`, `tests/test_assessment.py`, `tests/test_capacity.py`, `tests/test_delivery.py`, `tests/test_identity.py`.

### PPM-81-004 — Use and explain existing access controls

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** Existing permissions contract; 003 provides understandable labels.

**Change and user benefit:** Add a clear access panel to project, resource and assessment screens. Reuse current grant APIs, including POST /api/v1/assessment/access. Explain role, explicit access, owner and sensitive effort separately. Let only authorized grant managers edit; expose revocation consequences and safe read-only explanations.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Prefer existing grant tables; no new role hierarchy or custom-role engine. |
| AI / data | No AI; later tools must consume the same effective access rules. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** Admin can grant and revoke assessment result/framework access through the browser. PM actions follow existing framework/project authority. Changing role or removing membership immediately affects list/detail/stream/download access. Being assigned owner never bypasses access checks.

**Tests:** Positive/negative API tests plus browser grant/revoke; object-ID substitution and stale open-tab tests; sensitive effort and completed result sharing.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-004.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-005:** G-005 NOT IMPLEMENTED — The command palette searches available page names only, not projects, work, risks or assessments. (evidence U,D,A)

**Existing relevant files:** `apps/web/app/system/page.tsx`, `apps/web/components/assessments.tsx`, `apps/web/components/delivery.tsx`, `apps/web/components/shell.tsx`, `apps/web/components/workspace-home.tsx`, `services/api/ppm_api/assessment.py`, `services/api/ppm_api/assessment_tables.py`, `services/api/ppm_api/delivery.py`, `services/api/ppm_api/ppm_schemas.py`, `services/api/ppm_api/ppm_tables.py`, `tests/browser/assessment.spec.ts`, `tests/browser/delivery.spec.ts`, `tests/test_assessment.py`, `tests/test_delivery.py`.

### PPM-81-005 — Search project and assessment records

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 004; 006 shared pagination/query contract.

**Change and user benefit:** Extend the page palette with a separate record-search mode for projects, work, risks and assessments. Use bounded server queries and permission-filter before count/search. Include type, organization, project and destination; retain page commands. Provide sort/filter behavior and truthful no-match/loading/error states.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Indexes only when measured query plans justify them; no vector engine for record search. |
| AI / data | None; document/RAG search belongs to 09–14. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** A permitted older project can be found by name and opened directly. Unauthorized names, totals and identifiers never appear. Escaped special characters and empty terms cannot expand access; requests are bounded.

**Tests:** API wildcard/limits/access tests; browser search → detail → return; duplicate project names, revoked membership, zero results and keyboard selection.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-005.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-006:** G-006 PARTIAL — Assessment UI explicitly loads the latest 100; selectors/import destinations are bounded to first 100. API pagination does not make browser records beyond that limit reachable. (evidence A,C,J)

**Existing relevant files:** `apps/web/components/assessments.tsx`, `apps/web/components/capacity.tsx`, `apps/web/components/integrations.tsx`, `apps/web/components/live-jobs.ts`, `services/api/ppm_api/assessment.py`, `services/api/ppm_api/assessment_tables.py`, `services/api/ppm_api/capacity.py`, `services/api/ppm_api/capacity_schemas.py`, `services/api/ppm_api/ingestion.py`, `services/api/ppm_api/job_tables.py`, `services/api/ppm_api/jobs.py`, `services/api/ppm_api/ppm_tables.py`, `services/worker/ppm_worker/app.py`, `tests/browser/assessment.spec.ts`, `tests/browser/capacity.spec.ts`, `tests/test_assessment.py`, `tests/test_capacity.py`, `tests/test_ingestion_mapping.py`, `tests/test_jobs.py`.

### PPM-81-006 — Page through all records and comparison cohorts

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 005 shares filters; existing offset/limit routes.

**Change and user benefit:** Add server-side paging/search to assessment lists and resource/member/import selectors, not client-only filtering over first 100. Define stable sort and page reset on filter changes. Fetch complete authorized cohort aggregates on the server with explicit period/version, rather than implying latest-100 covers the organization.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Use existing pagination where correct; bounded aggregate/index migration only if required. |
| AI / data | None; shared cohorts later reused by 19. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** With 125 fixtures, record 125 is selectable and discoverable. Paging never duplicates/skips a stable dataset. Department comparison equals independently calculated full-cohort totals and displays period/count/coverage. No unauthorized count leaks.

**Tests:** 125-record API/browser fixture; equal timestamps, empty last page, changed filters, incompatible versions and two tenants.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-006.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-007:** G-007 PARTIAL — No personal assigned-work inbox; the notification dialog states no feed is active. Durable jobs are implemented, but there is no user notification model. (evidence U,J)

**Existing relevant files:** `apps/web/app/system/page.tsx`, `apps/web/components/integrations.tsx`, `apps/web/components/live-jobs.ts`, `apps/web/components/shell.tsx`, `apps/web/components/workspace-home.tsx`, `services/api/ppm_api/ingestion.py`, `services/api/ppm_api/job_tables.py`, `services/api/ppm_api/jobs.py`, `services/worker/ppm_worker/app.py`, `tests/test_ingestion_mapping.py`, `tests/test_jobs.py`.

### PPM-81-007 — Personal work and a small in-app notification feed

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 004/006; Sprint 08 events and authority contracts.

**Change and user benefit:** Add My Work links for assigned work, owned open risks and active assessments based on existing ownership. Revalidate access on open and after revocation. Add in-app assignment/review/import-result notifications with read state and preference controls. Use outbox deduplication; avoid mailing or daily scheduling here.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | New tenant/user-scoped notification table and event version via a forward migration. |
| AI / data | None; AI recommendations later attach reviewed items in 11/15. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** A PM sees only permitted assigned items and upcoming dated work; Viewer gets read-only allowed entries. Repeated events create one notification. Read state persists; revoked items no longer expose titles/details. Empty feed explains that no eligible events exist.

**Tests:** Browser role-specific inbox; duplicate event/restart/revocation tests; expiry/retention and read-state tests.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-007.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-008:** G-008 PARTIAL — Dates, ownership, status, goals and budgets exist; project industry, methodology, size/category and work priority/type are absent. Fintech questions and compatible cohorts need these fields. (evidence D,J)

**Existing relevant files:** `apps/web/components/delivery.tsx`, `apps/web/components/integrations.tsx`, `apps/web/components/live-jobs.ts`, `services/api/ppm_api/delivery.py`, `services/api/ppm_api/ingestion.py`, `services/api/ppm_api/job_tables.py`, `services/api/ppm_api/jobs.py`, `services/api/ppm_api/ppm_schemas.py`, `services/api/ppm_api/ppm_tables.py`, `services/worker/ppm_worker/app.py`, `tests/browser/delivery.spec.ts`, `tests/test_delivery.py`, `tests/test_ingestion_mapping.py`, `tests/test_jobs.py`.

### PPM-81-008 — Small metadata additions for future questions

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 005/006; controlled definitions agreed during task kickoff.

**Change and user benefit:** Add project priority, industry/category, methodology and size band, and work priority/type with clear optional unknown values. Keep outcome progress tied to existing milestone/work facts; explain it rather than inventing a completion score. Update UI, validation, contracts and import mapping only for the supported fields.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Additive nullable/default-unknown columns or agreed structured metadata; forward-only migration. |
| AI / data | Later 12/14/19 consume fields; no prediction added now. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** An industry-filtered project list returns correct known records and labels unknown metadata. Existing projects remain valid with unknown values. Historical dates/status/risk formulas and budgets do not change.

**Tests:** Old-row migration preservation, invalid categories, scoped filtering, optional import fields and UI labels; update contract snapshots.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-008.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-009:** G-009 PARTIAL — Job completion/degradation refreshes dashboards. General manual delivery/resource/assessment edits have no common change-event refresh. (evidence M,J)

**Existing relevant files:** `apps/web/components/command-center.tsx`, `apps/web/components/integrations.tsx`, `apps/web/components/live-jobs.ts`, `services/api/ppm_api/command.py`, `services/api/ppm_api/command_tables.py`, `services/api/ppm_api/ingestion.py`, `services/api/ppm_api/job_tables.py`, `services/api/ppm_api/jobs.py`, `services/api/ppm_api/metric_math.py`, `services/worker/ppm_worker/app.py`, `tests/browser/command.spec.ts`, `tests/test_command.py`, `tests/test_ingestion_mapping.py`, `tests/test_jobs.py`.

### PPM-81-009 — Refresh dashboards after ordinary edits

**Status:** proposed, not implemented by this planning task. **Priority:** P2. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** Existing SSE contract; 004 effective access.

**Change and user benefit:** Publish minimal entity-change notices for authorized delivery/resource/assessment writes. Coalesce updates and re-fetch existing metric endpoints; keep freshness markers and reconnect behavior. Do not send detailed objects to every stream subscriber.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | Reuse outbox/event tables and define versioned domain-change envelopes; no alternative message broker. |
| AI / data | None; preserve one deterministic metric service. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** A manual milestone change updates the authorized dashboard without reload; another tenant receives no notice. Reconnect and duplicate notices preserve totals and do not cause unbounded refetches.

**Tests:** Two browser sessions; changed-access streaming tests; duplicate/reconnect bursts and failed-write-no-event checks.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-009.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Historical pre-execution evidence for PPM-81-010:** G-010 BROKEN — The testing guide asks users to create an active sprint; delivery.py requires planned on creation. The system page contains obsolete dashboard readiness wording. (evidence U,D); G-034 UNVERIFIED — Sprint 07 auth-fix hosted CI passed; Sprint 08 workspace is uncommitted and no hosted run for those changes is established. (evidence R); G-035 UNVERIFIED — A planning-session rerun combining two pure-unit files with transaction-boundary ASGI tests stopped after twelve tests without completion; it was interrupted. Prior full-suite log records 67 passing. (evidence R); G-036 PARTIAL — Roadmap intro still says only Sprint 00 completed; frozen original prompts and evolving coverage disagree on 13/14 dependencies and 14/16 decision-log dependencies. (evidence R)

**Existing relevant files:** `apps/web/app/system/page.tsx`, `apps/web/components/delivery.tsx`, `apps/web/components/shell.tsx`, `apps/web/components/workspace-home.tsx`, `services/api/migrations/versions/0007_durable_jobs.py`, `services/api/ppm_api/config.py`, `services/api/ppm_api/delivery.py`, `services/api/ppm_api/main.py`, `services/api/ppm_api/ppm_schemas.py`, `services/api/ppm_api/ppm_tables.py`, `services/api/ppm_api/storage.py`, `tests/browser/delivery.spec.ts`, `tests/test_delivery.py`.

### PPM-81-010 — Pilot guide, regression evidence and closure

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 001–009; 09 carries extended document/object purge; hosted CI needs checkpoint.

**Change and user benefit:** Correct planned→active sprint instructions and obsolete system wording; regenerate the simple user guide during implementation with fictional organization/member/project/rubric examples and activation-set passwords, never real credentials. Establish a scratch restore exercise, contract/source checks and a reviewed CI checkpoint. Reconcile audit statuses only after evidence exists.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend the existing owning module(s) listed above; keep validation, tenant filtering and optimistic version guards. Regenerate API contracts when routes or schemas change. |
| Frontend | Extend existing screens listed above; new components, if needed, are proposed paths under apps/web/app and apps/web/components. Required keyboard/mobile/empty/error states are part of acceptance. |
| Database / migration | No feature schema; any restore uses isolated scratch database and objects, never normal database reset. |
| AI / data | No AI feature work; placeholders remain labeled future. |
| Security | Use live membership/effective grants, bounded input and audit/outbox rules. Never expose challenges/secrets or unauthorized names/counts; test removed permissions after an existing session. |

**Acceptance:** A new tester completes the documented journey without shell access except clearly labeled local operator setup. Existing data/migration hashes are preserved. Relevant API/browser/static checks finish; unresolved live-provider checks remain explicit blockers.

**Tests:** Two tenants × three roles; guide walkthrough; current transaction-boundary tests in isolated established environment; restore to scratch, contracts/build/source hashes and hosted CI for reviewed revision.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/04-testing/sprint-based/sprint-8.1/PPM-81-010.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

## Completion gate

- Signup/activation/invite/reset journeys work without hidden operator steps in a configured environment; local operator-only preview is clearly documented. Real delivery remains BLOCKED if provider access is absent.
- Existing two-tenant Admin/PM/Viewer core journeys still pass; explicit grants, sensitive effort, search, counts, notifications and streams do not leak data.
- At least 125 records prove full list/selector access; comparison totals use complete authorized cohorts. New metadata preserves unknown values and existing records.
- Guide walkthrough, mobile/keyboard flows, contract/type/lint/build/source checks and migration preservation pass. Resolve the interrupted transaction test with an actual completed run in the established test environment.
- Reviewed CI checkpoint and scratch pilot restore evidence exist; no normal database reset, no source/prompt hash change. Each failed or provider-blocked acceptance stays open; screenshots alone cannot close backend/security criteria.
- Produce **proposed** `docs/03-sprints/completed/sprint-8.1/SPRINT_REPORT.md`, `docs/03-sprints/completed/sprint-8.1/HANDOFF.md` and per-task verification notes; update LATEST, coverage and changelog only after implementation. Record planned versus completed work explicitly.

## Deferred work

Document/OCR/evidence links and policy/retention controls belong to 09. Shared embeddings/providers to 10, all nine agents and semantic assessments to 11, connector unattended identity and historical training to 12, forecasts to 13, copilot to 14, generalized approvals/reminders/assessment repeat to 15. No new AI, graph, scenario, meeting, passkey, reporting audio or cloud feature is implemented in this plan. Basic notification assignment/review events in 8.1 do not substitute for the 15/21 due-event and delivery scope.
