# Sprint 03 — A consistent workspace

**Status:** Completed for the application layout and shared screen controls.

## What was built and why it matters

The application gained a common workspace: navigation, page names, organization selection, account access, themes and reusable controls. This made later project and assessment screens feel like parts of one product.

| Delivered function | Where to access it | How to check / expected result |
| --- | --- | --- |
| Sidebar and page-location trail | Any signed-in workspace screen. | Select a page in the sidebar. The active link and page trail reflect where you are. |
| Small-screen navigation drawer | On a narrow browser window, **Open navigation**. | Open the drawer, select a destination and use Escape to close an open dialog. Content remains usable at the smaller width. |
| Organization selector and account shortcut | Top bar; account avatar leads to **Account & access**. | Open each control and confirm the selected organization and person. |
| Page command search | **Go to a page…**, or Ctrl+K / Cmd+K. | Type `Projects`, move through matches with the keyboard and open the page. |
| Light and dark themes | **Dark** / **Light** in the top bar. | Toggle the theme and reload. The browser remembers the selection. |
| Workspace overview | [Home](http://localhost:3000/). | Inspect the signed-in workspace. Account information comes from the current account. Later sprints added setup guidance and My work here. |
| Shared form, dialog, table and status designs | [Component gallery](http://localhost:3000/design-system). | Inspect the labelled examples, table controls, empty states and dialog behavior. Gallery examples are demonstration data. |
| Technical diagnostics in a separate place | Sidebar footer **Service diagnostics**, `/system`. | Open diagnostics without confusing it with a project dashboard. |
| Notification drawer foundation | Top-bar **Open notifications**. | Open and close the drawer. Real personal notification receipts were added later in Sprint 8.1. |

## How to check it

**You need:** Any activated account. See [Getting access](../START_HERE.md).

1. Sign in and open Workspace overview.
2. Use Ctrl+K to reach Account & access.
3. Toggle the theme and reload.
4. Narrow the window until mobile navigation appears, then use it to open the Component gallery.
5. Tab through controls and open/close a sample dialog.

**Expected result:** Navigation works by mouse and keyboard, the selected theme persists, and the layout remains usable on a smaller screen. Wider data tables can have their own horizontal scrolling.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Navigation, theme and shared workspace frame | [Shell](../../../apps/web/components/shell.tsx) |
| Buttons, dialogs, tables and visual states | [Shared controls](../../../apps/web/components/ui.tsx), [styles](../../../apps/web/app/globals.css) |
| Overview and example gallery | [Workspace home](../../../apps/web/components/workspace-home.tsx), [gallery](../../../apps/web/components/gallery.tsx) |
| Browser checks | [Shell scenario](../../../tests/browser/shell.spec.ts) |

## Recorded checks and limits

Four browser tests and layout, keyboard, theme and automated accessibility checks were recorded. This sprint did not implement project records, real record search or working business notifications. The gallery shows reusable examples; it is not evidence of saved portfolio data. Later features appear in the current shell but belong to their respective sprint reports.

[Original report](../../03-sprints/completed/sprint-03/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-03/TESTING_REPORT.md) · [Report index](../README.md)
