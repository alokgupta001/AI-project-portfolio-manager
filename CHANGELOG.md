# Changelog

## 2026-10-08 Sprint 07

- Added four command-center dashboards with shared typed metrics, saved filters, evidence drill-down and scoped JSON DTO download.
- Added risk lifecycle, recorded business benefits, configurable deterministic thresholds, explicit baseline/calendar plans and immutable sprint closure velocity in additive migration 0006.
- Preserved tenant/resource privacy, existing assessment results and normal checkpoint/data; repaired a nondeterministic assessment test without changing scoring.
- Verified 53 backend tests, seven prior browser scenarios and the final command scenario, responsive/axe checks, source hashes, zero-vulnerability npm audit and local worker/restart/storage behavior. See Sprint 07 checks for run boundaries and baseline measurements.

## 2026-10-06 Sprint 06

- Added typed maturity framework builder, immutable publishing, four editable examples, independent review, deterministic scoring, comparisons and history.
- Added scoped RLS/grants, revisions/replay protection and quarantined text evidence with reviewer release.
- Added responsive `/assessments` UI, generated contracts and migration 0005; preserved existing local data.
- Verified 49 backend tests, six existing browser checks plus final assessment case, static/security checks and runtime persistence. See Sprint 06 checks and handoff for evidence and limits.

## 2026-10-06 Sprint 05

- Added independent resource profiles, skills, dated teams/availability, immutable calendars,
  approved time off, allocations, restricted effort/coverage and allocation snapshots.
- Added migration 0004, resource/project grants, sensitive audit RLS, daily/weekly metrics,
  unknown/partial capacity handling and five-resource team support signals.
- Added `/resources` staffing matrix, profiles, heatmap/tables, editors and history using
  existing identity/shared UI. No dependency or existing user-data seed changes.
- Verified 44 backend tests and migration lifecycle; existing five browser regressions
  and final targeted staffing acceptance. See Sprint 05 checks for runtime and limits.

## 2026-10-06 Sprint 04

- Added scoped portfolios/programs/projects, goals, teams, delivery work, dependencies, plan history and decimal budget/expenditure records.
- Added migration 0003, RLS/grants, audited revisions, idempotent creates, validated transitions and immutable baseline/ledger corrections.
- Added delivery UI using shared shell/components and generated consumer DTOs; seeded a separate deterministic business demo.
- Verified 38 backend tests and migration lifecycle; browser/runtime evidence and limits are in the Sprint 04 checks. Updated coverage, contracts, ADR, report and handoff. Sprint 05 not started.

## 2026-10-05 Sprint 03

- Added enterprise workspace overview, responsive navigation, organization switcher, breadcrumbs, command palette and explicit notification availability state.
- Added light/dark semantic themes, shared UI primitives, audit table/filtering, confirmation dialogs and illustrative component gallery.
- Restyled existing identity flows; moved operator diagnostics to `/system`; retained backend/session/tenant contracts and migrations.
- Four Chromium tests passed, including identity, axe accessibility, keyboard and 360/768/1440 theme checks; static/contract/build/source checks passed.
- Added frontend contract, ADR 009, report and handoff. No PPM domain module or paid service; Sprint 04 not started.

## 2026-10-05 Sprint 02

- Added organization identity, Admin/Project Manager/Viewer membership, controlled Admin activation, invitations and password recovery through a private local mailbox.
- Added bcrypt passwords, secure cookie JWT sessions, atomic refresh rotation/replay revocation, CSRF/origin checks, rate limits and immediate session revocation.
- Added migration 0002_identity with tenant RLS, composite membership references, revision checks, final-admin concurrency protection and scoped identity audit. Preserved 0001_foundation.
- Added responsive login/account/recovery/invitation screens and a same-origin typed API transport with stale-organization write preconditions.
- Verified 28 backend tests, three browser tests, static/contract checks, production builds, real worker and restart persistence. Added Sprint 02 report, evidence, operation guide and handoff.
- No external email, paid cloud, later domain modules or hosted CI run. Sprint 03 not started.

## 2026-10-05 Sprint 01

- Implemented locked Next.js/FastAPI/Linux Celery foundation with PostgreSQL, Redis and local object storage; added responsive real-service status UI.
- Added migration 0001_foundation, restricted database roles, environment validation, sanitized errors/logging and UUID request correlation.
- Added deterministic OpenAPI/TypeScript client generation, digest-pinned Compose images, isolated test/demo configuration and CI workflow.
- Verified 16 backend tests, two browser tests, real worker execution, static/contract checks and database/object persistence across service restart.
- Added setup guide, runtime ADR, dependency/license inventories, actual check evidence, Sprint 01 report and technical handoff; preserved all source hashes.
- Hosted CI and a separately running demo stack remain unverified. Identity and later modules are not started.

## 2026-10-05 Sprint 00

- Created the enterprise-ppm workspace and local Git repository without a remote or commit.
- Preserved both user specifications and five prompt-pack files, with SHA256 manifest.
- Added source traceability, personas, roadmap, dependency clarifications and proposed decisions.
- Added module architecture, ER diagrams, six ADRs, permissions, API/event/AI contracts and metric definitions.
- Added quality plan, repeatable documentation verification, Sprint 00 report and technical handoff.
- Application implementation has not started; Sprint 01 is the next work package.
