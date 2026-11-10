# Frontend redesign and guided tutorial — 31 October 2026

This local frontend checkpoint preserves the current Sprint 12.1 application and
its server contracts. It does not authorize a successor sprint, provider calls,
deployment or changes to stopped financial-selection experiments. The normal app
uses port 3000; port 3001 belongs to the disposable browser-test stack and is not
a persistent preview.

## Design direction and implementation

The interface uses forest green actions, mint accents, warm neutral surfaces,
locally served Geist typography and one consistent stroke-icon family. The
overview has a connected metric strip, a health distribution beside access
details, a project table and quick routes into daily work. Light and dark themes
share semantic tokens for surfaces, text, borders, status and focus. Shared
components propagate this treatment into existing feature screens.

| Surface | Before | Current implementation |
|---|---|---|
| Workspace `/` | Account/session facts and module entry points | Authorized project snapshot, portfolio/period filters, currency-separated spend, selectable health chart, project drill-down, retained account facts, My Work and setup checklist |
| Shell | Flat navigation and mixed symbols | Grouped Plan & deliver / Evidence & intelligence / Workspace navigation, consistent SVGs, correct active state for nested project routes, existing organization switch/search/notifications |
| Authentication | Existing forms and access rules | Shared forest/neutral visual treatment, clearer sign-in entry copy; existing real identity flows retained |
| Lists and forms | Shared generic table/editor | Server-managed tables show the complete server page; local tables offer row counts and clear-filter action; dirty delivery editors guard dismissal/navigation |
| Project finances | Missing values could appear as undefined; summary could hide currencies | Unavailable is explicit and currency totals remain separate |
| Onboarding | Setup checklist only | Eight-step replayable guided tour plus existing organization setup |
| Other modules | Functioning delivery/evidence/AI modules | Same routes, shared typography/tokens/components and retained behavior; no claim that every module was individually rebuilt |

No new npm dependency was introduced for this redesign. Existing React, native
dialogs, CSS, chart/table components and Playwright/axe were reused. Geist regular
and semibold are local font assets with `apps/web/public/fonts/OFL-Geist.txt`;
fonts do not make a third-party request at runtime. The existing local monospace
stack remains. The concept image is an external design artifact; it is not
rendered as an application screenshot or used in place of working UI.

### Reference techniques

These are research references to public product documentation, not claims that
authenticated dashboards were manually audited:

- [Linear first-time experience](https://linear.app/changelog/2019-05-09-first-time-user-experience): a short welcome and replayable discovery path.
- [Vercel dashboard tour](https://vercel.com/academy/optimize-your-vercel-account/tour-the-dashboard): clear scope and progressive disclosure around operational information.
- [Notion sidebar](https://www.notion.com/help/navigate-with-the-sidebar): grouped navigation and predictable destinations.
- [Stripe search](https://docs.stripe.com/dashboard/search): quick entry to existing records with explicit scope.
- [Figma contextual panels](https://help.figma.com/hc/en-us/articles/360039832014-Design-prototype-and-explore-layer-properties-in-the-right-sidebar): context-specific guidance and controls.
- [Raycast quickstart](https://manual.raycast.com/quickstart) and [action panel](https://manual.raycast.com/action-panel): keyboard discoverability and visible shortcuts.
- [Arc folders](https://resources.arc.net/hc/en-us/articles/19228419623447-Folders-Stash-Similar-Tabs-Together): meaningful grouping rather than more top-level navigation.
- [Loom onboarding reference](https://www.loom.com/community/d97180be7d674f4fbf57744365457162-pg): short, paced feature introductions.

No collaboration presence, fabricated activity, decorative trend data, automatic
sample creation or unsupported bulk operation was added to imitate these products.

## Guided tutorial

The welcome appears on `/` for an authenticated user without a saved tutorial
state. Replay is available in the shell and explicitly in Account & access's
Profile & security section. The
welcome and completion use native modal focus containment; the active tour uses
a floating card and a spotlight that leaves the current target operable. Missing
targets and empty/unauthorized scopes receive explanatory fallback text.

| Step | Title | Real target / destination |
|---|---|---|
| 1 | Your navigation hub | Primary navigation or the mobile navigation opener |
| 2 | Your portfolio, in perspective | Overview metrics and portfolio filters on `/` |
| 3 | Create your first project | Projects create control; Viewers instead see “How projects get started” with permission guidance |
| 4 | Find and manage your work | Server filters on `/projects` |
| 5 | Explore a project in depth | Permitted project detail/section controls; project-list fallback when no detail is available |
| 6 | Track progress with evidence | Shared filters and views on `/command-center` |
| 7 | Keep evidence connected | Existing `/documents` controls |
| 8 | Make the workspace yours | Theme and account preferences |

Back, Next, Skip step, clickable progress dots and confirmed Skip tour are
available. Arrow keys move steps; Enter advances when the card is focused; Escape
opens skip confirmation. Form controls retain their ordinary typing behavior.
Next, Back, Skip step and progress-dot selection now navigate to the destination
for the selected step automatically. The original behavior changed the
instructions without consistently changing the page; this repair keeps the
instructions and feature destination together. Explicit destination links remain
available. Active progress resumes after ordinary navigation. A discovered
project-detail route is remembered in memory within the current user and
organization scope; an empty project scope falls back to the project list. The
tour does not submit forms or broaden permissions. Completion offers
quick-reference tips, Explore workspace and Replay tour.

State is versioned under `ppm-tutorial-v1:<user-id>` with active/completed/skipped
status and step index. This is a browser-local preference, not an account-wide
server preference. Blocked storage has an in-memory page-session fallback and a
visible notice. Reduced-motion CSS disables movement and hides confetti.

### First-visit page guides

A separate, nonmodal three-tip guide introduces each of 15 authenticated page
types: Workspace overview, Projects, Project details, Portfolios, Resource
planning, Maturity assessments, Command center, Document library, Integrations &
jobs, AI operations & evidence, Agents & recommendations, History & baselines,
Organization setup, Account & access and Component gallery. Project detail URLs
share one guide rather than repeating it for every project. Public sign-in,
signup, recovery and operator diagnostics do not mount the authenticated shell
guide.

The card opens on first visit, with Back, Next tip, Got it and Close controls.
Show section scrolls to and highlights the tip's target; the page remains
interactive. The Page guide button replays the guide at any time outside the main
tour. Escape closes a focused guide and arrow keys change tips while the card is
focused. Viewer copy explains that editing may be unavailable. Mobile cards are
bounded and scrollable, and reduced motion disables their 200 ms entrance.

First-visit state uses `ppm-page-guide-v1:<user-id>:<page-type>` with a `seen`
value and a page-session fallback if storage is unavailable. The guide is marked
seen on its initial display; closing or leaving does not automatically restart
it. Page-guide state is per user/page type, not per organization. Guides wait
until the main tutorial has initialized and closed, avoiding competing overlays
during the main tour. These new interactions are under focused verification;
their implementation is not a claim that final browser checks have passed.

## Metric definitions and scope

`WorkspaceHome` uses the existing authenticated transport to request
`GET /api/v1/command/snapshot` and the permitted portfolio selector from
`GET /api/v1/delivery/portfolios?limit=100`. The server remains the authority for
project visibility, grants, health policy and financial values.

| Display | Definition / missing-data behavior |
|---|---|
| Visible projects | Count of projects returned in the authorized snapshot; not an organization-wide or “active project” claim |
| Need attention | Number whose computed category is Amber or Red |
| Healthy projects | Number whose computed category is Green |
| Health coverage | Rounded `(visible − Unknown) / visible × 100`; unavailable when the denominator is zero; clicking inspects Unknown projects |
| Health chart | Counts of Green, Amber, Red and Unknown; unexpected categories normalize to Unknown; bars select matching rows and an equivalent table gives exact values |
| Recorded spend in period | Server totals whose key ends in `_period_spend`; each currency remains separate, with status/freshness/source; null is unavailable and a real recorded zero remains zero |
| Evidence health | Server health metric value/unit or Unavailable; its explanation is retained |
| Reported health | Server reported category and discrepancy indicator; never substituted for computed health |
| Workspace access | Current role, returned organization membership count and returned session count (service cap 100) |

The period is the last 30, 90 or 365 organization calendar days, including today
through an exclusive next-day end. The initial snapshot discovers the server
timezone; a correcting request is made if the UTC bootstrap calendar differs.
Date arithmetic uses calendar days rather than assuming every local day is 24
hours. The timestamp is displayed in the snapshot timezone. Health is explicitly
current, not a historical trend; the period affects activity/spend. Portfolio
selection updates the server scope. Local health filters/search/sort/pagination
operate only on that returned snapshot. Currency conversion and invented trend
comparisons are not performed.

Loading, failed snapshot/retry, empty scope, unavailable portfolio choices,
partial ledgers, unknown health and service scope limits are visible. The
workspace subtree resets on organization change and requests discard stale
responses. The portfolio selector discloses when more than its first 100 choices
exist and points to Command center scope controls.

## Numbered feature coverage matrix

`L/E/F/S` below means loading, empty, failure/forbidden and successful states must
remain represented where applicable. “Retained” is a source-inventory statement,
not a fresh end-to-end pass. The listed browser files define the verification
journeys; their final results belong in the execution ledger below. API entries
are existing endpoint families; generated DTO names identify the boundary rather
than proposing a new schema. All data access remains subject to server roles,
organization RLS and project grants.

| # | Feature / priority | Roles | Route and entry | Existing API / model | States and current implementation | Browser evidence target |
|---|---|---|---|---|---|---|
| 1 | Sign-in, logout, session lifecycle / preserve | Signed-out / all accounts | `/login`, shell account/logout | `/auth/login`, `/auth/logout`, `/auth/sessions`; AccountView, SessionsView | Validation, failure, success retained; password visibility | identity, account-repair |
| 2 | Registration, recovery, invitation completion / preserve | Signed-out, invited user | `/signup`, `/account/reset`, `/account/complete` | `/auth/register`, `/auth/reset-request`, `/auth/complete`; Message | Verified signup, recovery and retained input; MFA is not an implemented flow | identity, pilot, account-repair |
| 3 | Profile, memberships, session revoke / preserve | All, Admin for member actions | `/account`, Account & access | `/auth/profile`, `/organization/members`, invitations, audit; AccountView, MemberView | L/E/F/S and confirmations retained | identity, pilot |
| 4 | Organization setup and switching / preserve | Admin setup; current members switch | `/organization`, shell organization selector, home setup checklist | `/organization/profile`, `/auth/switch`, `/workspace/setup`; profile/setup DTOs | Setup gating, incomplete configuration, error and success | pilot, identity, redesign |
| 5 | Guided tutorial / new high priority | All; role-aware creation | `/`, shell Replay tutorial | Browser-local versioned preference | Welcome/active/skip confirmation/completed/replay/storage denial | tutorial |
| 6 | Overview / high priority | Permitted members | `/`, overview nav | `/command/snapshot`; CommandSnapshot, ProjectMetrics | Real metrics, loading/error/retry/empty/unknown/partial, filters and drill-down | redesign, shell |
| 7 | Global navigation and search / high priority | All; Admin-only entries filtered | Shell, Ctrl/Cmd+K | `/workspace/search`; SearchPage | Page/record search, no matches, allowed destinations, keyboard focus | shell, pilot |
| 8 | My Work, notifications, live refresh / preserve | Scoped members | Home and notification bell | `/workspace/my-work`, `/workspace/notifications`, `/workspace/events`; SearchPage, notifications | Real persisted feed, read state, loading/empty/errors | pilot |
| 9 | Portfolios and hierarchy CRUD / preserve | Authorized Admin/PM; Viewer reads | `/portfolios`, delivery controls | `/delivery/{kind}`, portfolio-summary; RecordView, PageView, PortfolioSummary | L/E/F/S, typed fields/revision errors, audit; dirty editor guard | delivery, walkthrough |
| 10 | Project list, create/edit/archive / high priority | Authorized Admin/PM; Viewer reads | `/projects`, Create projects, row links | `/delivery/projects`; RecordView, PageView | Server search/filter/sort/page; complete server page retained | delivery, redesign, pilot |
| 11 | Project detail and related delivery records / preserve | Project grants | `/projects/[id]`, section controls | `/delivery/{kind}`, project-summary, history; SummaryView, HistoryView | Work/milestones/risks/budget/dependencies/baselines/history; missing money explicit | delivery, walkthrough, redesign |
| 12 | Capacity and resources / preserve | Scoped members and authorized writers | `/resources`, navigation | `/capacity/resources/{rid}`, teams, snapshots; CapacityView, TeamCapacityView, SnapshotView | L/E/F/S, daily heatmap/table, weekly reconciliation, snapshots | capacity |
| 13 | Assessments and scoring / preserve | Framework admins, respondents, reviewers, scoped readers | `/assessments` | `/assessment/frameworks`, assessments, evidence/events; AssessmentDetail, FrameworkRecord | Builder/version publishing, autosave/unsaved failure, review, private evidence, comparisons | assessment, walkthrough, pilot |
| 14 | Command center and export / preserve | Scoped members | `/command-center` | `/command/snapshot`; CommandSnapshot | Executive/Delivery/Risk/Resource, date/portfolio, saved views, evidence drawer, JSON DTO export | command |
| 15 | Integrations and durable activity / preserve | Authorized operators | `/integrations` | `/integrations`, preview/sync/activity/jobs/events; IntegrationView, JobView | Preview, job stages/progress/cancel, retry/revoked scope, connector authority/conflicts | integrations, sprint12 |
| 16 | Documents and governance / preserve | Permission-specific reader/manager | `/documents` | `/documents`, versions, citations, download-ticket; DocumentView | Upload/version/process/preview/download, retention/hold/erasure, safe citations; L/E/F/S | documents |
| 17 | Evidence assistant / preserve | Scoped users; restricted administration | `/ai` | `/ai`; generated runtime DTOs | Disabled-provider and real-source fallback, recovery, diagnostics/citations | ai, gemini |
| 18 | Specialists and guided reviews / preserve | Explicit project grants and role controls | `/agents` | `/agents/definitions`, runs; AnalysisView and guided-review DTOs | Evidence/recommendations, zero-call state, nine checklists, unavailable cloud and permissions | agents, agents-v2, guided-access, guided-review |
| 19 | Financial selection pilot / preserve frozen checkpoint | Authorized Admin | `/agents`, pilot section | `/agents/selection-pilots`; PilotView | Fixture labeling, explicit automated provenance, unavailable/timing, reports; no experiment restart | selection-pilot |
| 20 | History, datasets and baselines / preserve | Scoped authorized users | `/ml` | `/ml/histories`, datasets, runs/artifacts; DatasetView, RunView | Freeze/reproduce/withdraw and insufficient-data/error states; no serving promotion | sprint12 |
| 21 | Shared tables, dialogs and theme / high priority | All | All module surfaces; `/design-system` | Existing UI components; theme preference | Labels/focus/native modal, loaded-row versus server pagination, clear filters, light/dark | shell, redesign, tutorial, delivery |
| 22 | Operator diagnostics / preserve | Public non-sensitive checkpoint | `/system` | Existing foundation health endpoint | Real API/database status and reload/mobile rendering | foundation |
| 23 | Cross-role and tenant isolation / critical preserve | Admin/PM/Viewer and revoked access | All protected routes and switcher | Existing cookie/CSRF transport, RLS and server capabilities | No frontend grant expansion; stale workspace state reset | identity, walkthrough, pilot, redesign and offline authorization tests |
| 24 | First-visit page guides / new high priority | Authenticated workspace users, with Viewer guidance | 15 page types, shell Page guide replay | Browser-local per-user/page-type `seen` preference | Three tips, section highlight, close/back/next and replay. Verified across all 15 page types on 5 November. | page-guide and tutorial journeys |

## Motion and responsive behavior

| Motion | Trigger and duration | Reduced motion |
|---|---|---|
| Button shadow/transform and quick-link arrow | Hover/focus, 140 ms | Disabled |
| Primary-button gradient shift | Pointer hover, 100 ms | Instant state change |
| Overview metric parallax | Pointer hover, 1 degree on each axis, 140 ms | Omitted |
| Theme icon rotation/state change | Theme toggle, 180 ms | Instant icon replacement |
| Native modal panel entrance | Open, 200 ms | Disabled |
| Skeleton pulse | Loading, 1.6 s loop | Disabled |
| Health-bar length | Snapshot/filter data changes, 240 ms | Disabled |
| Tutorial card direction/scale/fade | Step change, 200 ms | Disabled |
| Tutorial progress width | Step change, 200 ms | Disabled |
| Spotlight breathing ring | Active target, 2 s loop | Static ring |
| Completion check | Completion, 250 ms | Static check |
| Completion particles | Completion, 700 ms plus 120 ms delay | Hidden |

The overview test exercises widths 360, 768, 1024, 1440 and 1920 in both themes.
Shared tables use keyboard-focusable horizontal regions rather than allowing
document overflow. Mobile navigation becomes a drawer; tutorial placement is
bounded to the viewport with compact targets and a scrollable card. These are
implemented behaviors; final fresh execution status is recorded separately.

## Execution ledger

Evidence directory: `../output/frontend-redesign` relative to the repository.
The test runner additionally preserves new browser evidence under
`artifacts/local/browser-evidence` instead of replacing historical screenshots.

| Check | Recorded result |
|---|---|
| `npm run check` | Passed: static/contract/tooling stages and **416 backend tests passed, 1 skipped, 166 deselected**. Two warnings: inherited httpx deprecation and pytest cache permission. See `check.log`. This offline check is not the full database integration suite. |
| `npm run check:static` | Passed all 10 stages after the final guide correction: lint, web/browser types, formatting, contracts, source checks and 3 tooling tests. See `static-verified.log`. |
| Production build | Passed. Normal port-3000 web image rebuilt and container restarted with the corrected guides; see `local-web-verified.log`. Existing normal databases were retained. |
| Browser regressions | The 31 October full suite passed 34 of 35, including all four main-tour cases (`browser-verified.log`). The remaining case failed during test data creation. Its corrected fixture creates the required settings, portfolio and project. On 5 November, the focused rerun passed across all 15 page types, including a real project detail, first visit, section highlight, dismissal, reload, replay and mobile keyboard dismissal (`page-guide-final.log`). |
| Screenshot review | Inspected the desktop tutorial spotlight, mobile dark dashboard and the fresh AI page guide at 1440 and 360 pixels. All guide controls fit in view. See `ai-page-guide-desktop.png` and `ai-page-guide-mobile.png` in the evidence directory. Screenshots use synthetic accounts. |
| Accessibility | Main-tour keyboard/focus, reduced motion, storage denial and axe assertions passed, as did the dashboard's five-width/two-theme checks. The focused guide run passed the AI page axe scan, mobile bounds and browser error checks. Manual screen-reader testing remains open. |
| Performance | CLS, FCP, 60 fps and production latency benchmarks **not measured**. |

## Limits and remaining verification

- Direct inspection/refresh of the user's in-app preview was blocked by automatic
  approval review reporting a usage limit. It was not retried through another
  browser path. Existing isolated regression tests continue against synthetic
  accounts on port 3001; the normal build was applied through Compose.
- On 5 November, Docker startup reported stale zero-byte Windows sockets in its
  `run` and `docker-secrets-engine` directories. The stopped runtime directories
  were preserved as sibling backups and recreated. Compose subsequently reported
  the normal web service healthy on port 3000 and the API healthy on port 8000.
- At resumption the normal app containers were found stopped. Existing postgres,
  redis, clamav, API and web services were restored; the provider worker and
  dispatcher remain stopped. No live provider calls were made for this redesign.
  Background-job execution therefore depends on an explicitly restored worker
  lifecycle; isolated browser tests use their own disposable services.
- Final comparison of 107 pre-existing preservation receipts found only four
  intentional documentation changes: `ANTIGRAVITY.md`, `CHANGELOG.md`,
  `docs/contracts/frontend.md` and `docs/handoffs/LATEST.md`. All other receipt
  hashes, including prior backend work, environment files and migrations, match.
- Browser coverage samples journeys and synthetic fixtures; it does not prove
  every field, every permission combination or real-provider quality. Mocked
  category/empty/error cases are separate from live fixture snapshot tests.
- Unsaved-change protection was added to the shared delivery editor. Existing
  autosave/error contracts remain in other forms; no claim of a universal guard
  across every module is made.
- Existing module limits remain: no universal column resizing, universal bulk
  actions, multi-user presence, graph editing or server tutorial-preference API.
- First-run onboarding is browser-local per user. Clearing storage or changing
  browser starts a new tour. Blocked storage retains state only for the page
  session.
- Currency values are not converted or combined. Health is current; no fake
  historical chart or prior-period comparison is shown.
- Normal databases, applied migrations, existing stopped pilot results, quota
  policy and broad AT17 BLOCKED status remain outside this redesign's changes.
