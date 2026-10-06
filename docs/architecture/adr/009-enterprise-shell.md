# ADR 009 — Enterprise shell and shared UI

2026-10-05. Implemented under explicit Sprint 03 authorization. Retain the existing Next.js/React/TypeScript/Tailwind baseline and identity transport; no backend/schema changes.

Use a restrained slate/indigo design, semantic light/dark tokens and shared React components. Native dialog supplies modality and focus containment; CSS supplies modest transitions and reduced-motion behavior. This deliberately implements the required behavior without adding shadcn/Radix, Motion, Zustand, a query cache or chart runtime in this sprint. Those suggested stack items remain partial/deferred, not falsely marked installed. Adding a library later requires an explicit consumer migration and verified need; reuse the exported component contract first.

The current shell has only a small identity data surface. Retaining its existing loader avoids introducing another session/cache authority during a visual sprint. React local state is sufficient for transient dialogs and filters. The gallery chart is an explicitly illustrative CSS distribution with a table alternative; analytics charting and Gantt remain future module work.

Add only test dependency `@axe-core/playwright` 4.13.0 (MPL-2.0), exact lockfile and refreshed license inventory. Existing Playwright 1.63.0/Node 24 runs it successfully. [Deque documentation](https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright) and [native dialog behavior](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog) informed implementation. No dependency or UI claim establishes complete accessibility certification.

Move technical service status from `/` to `/system`, retaining the real API/database round-trip test there. The workspace overview uses live account/session data; future business modules remain explicit unavailable states. Authentication routes stay compatible. See [frontend contract](../../contracts/frontend.md) for reuse and interaction details.
