# AI-PPM development workflow

Read `ANTIGRAVITY.md`, the top of `docs/handoffs/LATEST.md`, and the handoff it
identifies. These remain the canonical sprint context; read only affected contracts
and code after that. This file adds Codex discovery and development guidance, not a
new sprint plan. Start Codex in this repository, not its parent directory.

## Scope and continuity

- Check Git status before editing; preserve unrelated uncommitted work. If Windows
  reports ownership mismatch, use a command-scoped `git -c safe.directory=<root>`
  after verifying the root. Do not add a global wildcard trust exception.
- Follow the requested scope: understand affected code, implement small changes,
  run relevant checks, inspect rendered UI when applicable, fix regressions, and
  report actual results plus remaining work. Investigate root causes and add a
  regression test for a bug fix.
- Preserve existing APIs, business rules, organization/RLS boundaries, explicit
  project grants, identity/CSRF controls, quotas and error handling. Review these
  when affected. Never print credentials or private test fixtures.
- Keep existing sprint authorization and documentation workflow. Do not begin a
  successor sprint, restart stopped provider experiments, commit, push or deploy
  without authorization. Never reset normal/demo databases or edit applied
  migrations. Destructive actions, significant upgrades and paid calls need approval.
- Subagents can help with independent research or review when authorized; keep one
  writer per affected file and follow the existing single-checkout coding rule.

## UI implementation

- Read `docs/contracts/frontend.md` for existing components, semantic tokens,
  typography, themes, layout and accessibility behavior. Choose an enterprise SaaS
  visual direction appropriate to the requested task before significant UI work.
  Reuse `apps/web/components/ui.tsx`, shell, tables and chart/table equivalents.
- Use the project `ui-ux-pro-max` skill for focused typography, palette, chart,
  dashboard and UX research. Its suggestions supplement existing tokens; do not
  introduce fonts, component libraries or a redesign automatically. Run its Python
  search without `--persist` unless a saved design specification is requested.
- Use `frontend-app-builder` for an explicitly requested new visual surface or
  redesign and `frontend-testing-debugging` for rendered behavior/QA. Existing
  design-system fixes need no new concept images. User scope and cost constraints
  take precedence over upstream suggestions for image generation or extra packages.
- Implement real interactions, accessible labels/focus/keyboard behavior and
  loading, empty, error and success states. Check the affected flow, runtime errors,
  mobile/tablet/desktop layouts (360/768/1440), light/dark themes when relevant,
  overflow, tables and charts. Inspect fresh screenshots; fix visible problems.
- Prefer repeatable Playwright regression checks plus relevant axe checks. Use
  synthetic accounts/data and disabled or mocked model providers. Browser testing
  does not establish live-provider quality or full accessibility certification.

## Existing tools and checks

Node 24/npm 11 or 12, Python 3.12 and the locked dependencies are already configured.
Do not add another formatter, linter, test framework or package manager.

- `npm run check`: existing static, contract/source and offline backend unit checks.
- `npm run check:static`: static checks only; `npm run check -- --build` also builds.
- `npm run test:e2e`: existing isolated Compose/fixture runner on 3001/8001.
  `npm run test:e2e:smoke` selects identity/org switching, shell/accessibility,
  project management, assessments/results, command center and assistant fallback.
- `npm run test:e2e:list` lists tests without services; `npm run test:e2e:debug --
  <spec>` uses the same isolated runner with Playwright Inspector.
- For hybrid/pilot UI, set `PPM_TEST_AI_V2=1` for the isolated runner as documented in
  `docs/07-setup-and-deployment/LOCAL-DEVELOPMENT.md`; no real providers are enabled.
- Use existing guarded Compose backend integration checks when FastAPI/SQL/RLS,
  migrations, workers or storage are affected. Keep lifecycle downgrades restricted
  to the explicitly disposable `ppm_test` database.

Run focused checks during edits, then the required regression scope. Distinguish
passed, failed, skipped, blocked and not run. Never report a test/build as passed
without a successful execution. Record useful current results in existing setup,
testing or sprint documentation; do not rewrite historical evidence.
