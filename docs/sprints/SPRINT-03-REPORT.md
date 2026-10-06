# Sprint 03 implementation report

## Status and scope

2026-10-05: Enterprise design system/application shell implemented on the Sprint 02 identity baseline. N-004/N-005 and E-004 accepted for this shell; N-013 accepted for tested core flows with release-wide accessibility still ongoing. Sources: S4.2 and master frontend contract. Git remains main, uncommitted, with no remote. No domain modules or paid services introduced.

## What, why and how

The app now has a recognizable enterprise workspace: responsive sidebar and mobile drawer, organization switcher, breadcrumbs, account shortcut, page search/command palette, notification availability drawer and persistent light/dark themes. The overview shows real membership/session information and useful account actions. Future portfolios, assessments, analytics and AI are visibly planned, not fabricated dashboards.

Existing account, invitation, recovery and membership controls use the shared visual system. Session revocation and membership permission changes require confirmation. The existing typed API, CSRF/session checks, tenant precondition and revision checks still authorize mutations; successful account loads update the organization view atomically. Errors retain actionable messages. No AI call, new database table or background job is involved.

Reusable components cover buttons, forms, dialogs/drawers, filterable/sortable/paginated tables with density, badges, metric cards, chart/table frames, skeletons and empty/error/forbidden/partial states. The gallery contains labeled in-memory examples. The audit table uses real authorized records. Details and intentional technology choices are in the [frontend contract](../contracts/frontend.md) and [ADR 009](../architecture/adr/009-enterprise-shell.md).

## Use and demonstration

Start the existing stack with `docker compose up --build -d --wait`. Open http://localhost:3000/login and use your activated local account. Login retains the existing `/account` destination; select Workspace overview to see the new home. Switch organizations in the top bar, try Ctrl/Cmd+K, toggle theme, inspect notifications and the component gallery. Admins can filter members and browse audit records; Viewers see their own account controls. Technical diagnostics moved to `/system`.

The Demo Admin was created separately after Sprint 02; this sprint neither changes its password nor seeds business records. Use the [identity guide](../IDENTITY-DEVELOPMENT.md) for activation/recovery.

## Implementation and verification

New files: `apps/web/components/{ui,shell,workspace-home,gallery}.tsx`, `/design-system` and `/system`; updated identity client, root page/layout, semantic CSS and browser tests. Added exact dev-only axe dependency and lock/license inventory. API contracts, migrations and originals unchanged.

[Acceptance evidence](../verification/SPRINT-03-CHECKS.md) records four passing Chromium tests, automated accessibility and keyboard/theme/responsive checks, static/contract checks, source preservation, dependency audit and local container build/start. Screenshot review covers desktop/tablet/mobile. No claim of full screen-reader certification or measured performance targets.

## Operations and next sprint

Only `ppm-theme` is persisted in browser storage; credentials remain secure cookies. No external email/provider, cloud cost or hosted CI run. Native components intentionally avoid unnecessary UI dependencies; future libraries must preserve their documented contracts. Domain-aware server filtering and analytics charts remain later work.

Sprint 04 can introduce the portfolio/project system of record and isolated business demo fixtures using these components. Sprint 04 has not started. [Technical handoff](../handoffs/SPRINT-03-HANDOFF.md).
