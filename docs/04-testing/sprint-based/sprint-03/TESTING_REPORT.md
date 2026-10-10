# Sprint 03 acceptance evidence

Executed 2026-10-05 on the existing Node 24.20.0 / npm 11.19.0 / Docker Linux / Chromium baseline. Only frontend and browser tooling changed; backend/migration code and generated API schema are preserved.

| Check | Result and evidence |
| --- | --- |
| Starting state | Git branch main, no commit/remote, existing files untracked; services healthy; migration-role `alembic current` = `0002_identity (head)`; contracts matched before edits. |
| Browser suite | `node scripts/check-identity-browser.mjs`: **4 passed (21.2s)** covering diagnostic persistence, mobile diagnostics, full identity lifecycle and new enterprise shell. [Transcript](../../../verification/sprint-03-browser.txt). |
| Automated accessibility | Axe WCAG 2 A/AA, 2.1 AA and 2.2 AA tags: no detected violations in tested login/account, workspace both themes at 360/768/1440, gallery and overlays. Not full WCAG certification. |
| Keyboard and semantics | Skip link, focus target, Ctrl+K, command arrows, Escape, dialog cancel and trigger focus restoration, native labeled fields, table captions/sort state, Admin-only command visibility passed. |
| Responsive/theme | No page overflow at tested widths; theme persists across reload; reduced-motion skeleton has no animation. Screenshots under ignored `artifacts/local/sprint03-home-*.png`; light desktop/mobile, dark tablet and account desktop visually inspected. |
| Identity regression | Secure/HttpOnly/SameSite cookies; no stored credentials (only theme preference allowed); real org switching, Viewer denied member API, profile, invitations, activation, reset and revoked session lifecycle passed. Destructive session confirmation cancellation tested. |
| Static/contracts | `npm run lint`, `typecheck`, `format:check`, `contracts:check` passed; outputs observed in tools. |
| Build/runtime | `docker compose up --build -d --wait`; [transcript](../../../verification/sprint-03-runtime.txt). Production web compilation succeeds; local production deployment remains disabled. |
| Dependencies/sources | `npm audit --audit-level=high`: zero reported vulnerabilities. Seven preserved source/prompt hashes pass; npm declared-license inventory refreshed. |

Initial static check caught an unused Skeleton import, repaired before browser execution. Visual review led to a mobile search spacing refinement and a clearer notification icon; browser acceptance was rerun after those changes.

The isolated browser project uses random test identities, separate ports/databases and deletes its private fixture JSON on exit; named volumes remain. The normal local Demo organization is preserved. No production/provider data used.

The 28 backend tests passed at Sprint 02 and were not rerun for this frontend-only change; browser tests exercise the real API and permissions. No new migration exists, so destructive migration lifecycle was not repeated. Hosted CI, other browser engines, actual screen-reader user testing, full WCAG audit, FCP/60fps/load benchmarks and production deployment were not run. No business PPM/AI capability is inferred from these tests.

Final local smoke: signed-out overview shows a neutral sign-in invitation; login navigation and axe scan passed after that isolated presentation refinement. Initial smoke harness incorrectly counted Next.js’s empty route announcer as an application error and used an implicit browser context unsupported by axe; corrected harness passed. Local web/API/Postgres/Redis healthy, worker running. Login screenshot also visually reviewed.
