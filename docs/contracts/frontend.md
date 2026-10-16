# Frontend contract — Sprint 03

Sprint 05 adds `/resources` using the same identity transport and shell. Capacity
forms extend the shared typed record editor; staffing lists, daily heatmap/table,
weekly reconciliation, team signals, history and snapshots follow the
[capacity contract](capacity.md). Tables scroll horizontally on narrow screens.

Sprint 04 extends the shared UI with delivery routes and typed forms, server-paged tables, work board, calendar-date timeline, dependency relationships and baseline/audit history. See [delivery UI limits](delivery.md). `DataTable external` disables internal filtering/pagination for server-managed lists while preserving existing defaults.

Implemented shell and connected delivery/capacity/assessment/command/source/job modules; /ai adds the controlled disabled/fallback evidence runtime. The [reuse/screen plan](../planning/PRODUCT-REUSE-AND-SCREEN-PLAN.md) remains the product reference.

## Components and ownership

- `apps/web/components/ui.tsx`: Button (primary/secondary/danger), Badge, Field, StatePanel (empty/error/forbidden/partial), Skeleton, MetricCard, native Modal/drawer, ConfirmDialog, typed DataTable and ChartFrame.
- `components/shell.tsx`: Shell, AuthFrame, Brand and ThemeControl; organization control comes from the existing identity client. Navigation lists only functioning routes. Future modules are plain planned labels, not links.
- `components/workspace-home.tsx`: current user's live role, organization count and session count (API cap 100), account actions and module availability. No project metrics are inferred.
- `components/gallery.tsx`: authenticated local development gallery. All examples are labeled, in-memory and separate from tenant records.
- `app/account/identity-client.tsx`: existing generated API transport and atomic account loading; owns account/membership mutations, organization preconditions and confirmation intents. No parallel auth provider or duplicated token store.

Routes: `/` workspace overview or sign-in entry; `/account` identity administration; `/login`, `/account/reset`, `/account/complete` existing auth; `/design-system` authenticated gallery; `/system` public local operator diagnostics, moved from `/`. Backend routes and DTOs are unchanged. Direct unauthenticated protected-page visits show sign-in access and expose no account content.

## Tokens and interaction

`app/globals.css` owns semantic background/surface/surface-alt/text/muted/line/accent/on-accent/success/warning/danger/focus tokens plus radius, spacing, shadow and duration. Font is the local Arial/Helvetica sans-serif stack; no external font dependency. Layout uses 600/900/1150/1600px breakpoints, with acceptance at 360/768/1440px. Native controls retain accessible labels. Focus uses a 3px contrasting outline; reduced motion disables transitions and animations. Blur is limited to modal backdrops, not text surfaces.

Light/dark theme initializes before render from `ppm-theme` or system preference, persists only that non-sensitive preference in localStorage, and falls back to in-memory changes if storage is unavailable. Credentials remain Secure/HttpOnly cookies. Theme storage must never become a session store.

Modal uses `showModal()` for inert background and focus containment; Escape/close returns focus to the trigger, body scrolling is restored on cleanup. Cancel is the initial confirmation action. Session revocation and role/deactivation changes require confirmation before invoking the existing mutation. Backend authorization/revisions remain authoritative.

Ctrl/Cmd+K opens page commands; search filters only available destinations, with Arrow keys/Tab/Enter/Escape. Members command is Admin-only. Notifications open an explicit unavailable state; there is no fabricated feed. Navigation search is not project/data search.

DataTable accepts typed rows, stable keys, render/sort accessors and search text. Filtering, sorting, density and pagination apply only to loaded rows; labels disclose this. Server cursor loading remains separate. Reset tenant-specific table state with an organization key. Do not present loaded-row totals as organization totals. ChartFrame requires a description and equivalent table; decorative visual marks are hidden from assistive technology.

## Limits

Account detail still uses the proven sequential identity load, with no new query cache. A future server-state library must key and clear tenant caches correctly. Domain-scale table querying and saved views belong to their owning modules. Screen-reader names/roles and keyboard behavior are exercised in Chromium; no full assistive-technology or WCAG certification is claimed. Performance/FCP/60fps targets remain unmeasured.

## Sprint 06 assessment UI

`/assessments` and `components/assessments.tsx` reuse the shell, authenticated transport, shared Modal/Field/Button/ChartFrame and generated API DTOs. A nested form edits framework dimensions/questions/weights/rubrics, then publishes frozen versions and assigns respondents/reviewers. Answers autosave after 900 ms; failed saves retain unsaved state and block submission. Workflow controls follow server capabilities. Scoped evidence uses escaped previews and explicit independent release. Score and comparison tables scroll horizontally with keyboard focus on small screens; comparisons disclose their latest-100 loaded-record limit and require identical version IDs. Browser evidence covers desktop/tablet/mobile and automated serious/critical accessibility checks; this is not full WCAG certification.

## Sprint 07 command center

`/command-center` reuses the authenticated shell, typed `CommandSnapshot`, modal evidence drawer and record editor. Four views share date/portfolio filters. Explicit metric units/period/source/freshness, accessible chart table, keyboard drawer return, truthful empty/unknown/partial states and personal saved views are implemented. JSON DTO download rechecks current access. [Contract](command-center.md).

## Sprint 09 source extension

`/documents` is registered in the authenticated shell/client. `documents.tsx` uses generated transport, server paging, escaped previews, job polling, can_manage actions and revalidated citations/original tickets. Open is disabled during pending save/load; mobile tables use a focusable horizontal region. [Source contract](documents.md) and [user guide](../03-sprints/completed/sprint-09/USER_GUIDE.md) define supported actions; semantic UI is deferred.
## Sprint 10 AI runtime extension

[ai-evidence-v1](ai.md) owns the additive /api/v1/ai and /ai behavior, immutable
snapshots, budgets/accounting, protected source tools, citation reauthorization,
versioned evaluation and disabled fallback. durable_jobs references exactly one
integration, document version or AI run; existing event/SSE/authority rules remain.
Bounded Gemini free-tier smoke verified; broad model quality unverified. No semantic agents, private assessment ingestion,
metric changes or automatic plan edits. Admin-only restricted operations apply.
