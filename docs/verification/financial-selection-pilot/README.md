# Financial selection pilot — actual local verification

This is the original implementation receipt for the work now named
[Sprint 12.1](../../03-sprints/active/sprint-12.1/README.md). Its counters and
earlier empty-history observation are historical checkpoints. The current
[handoff](../../03-sprints/active/sprint-12.1/HANDOFF.md) records the live access
mismatch: demo Admin membership alone does not satisfy the explicit grant gate.
No access expansion or human approval is inferred from the earlier assumptions below.

26 October 2026. Work starts from merged main `5d5ce87`, on local branch
`financial-api-qualification-pilot`. PR 7 is merged. No new publication, deployment,
forecast serving, provider activation or broad qualification is implied.

Starting diff, protected file hashes, schema 0018, private database backup and all
82 established table hashes are captured under ignored `artifacts/local/financial-pilot`.
All 21 original verification artifact edits remain excluded and protected.

- Focused backend: **59 passed in 94.70 seconds**. Includes 12-case mocked API flow,
  independent-review gate, duplicate cases, pacing, direct-route denial, cross-tenant
  RLS, Viewer denial, revoked reviewer, changed policy, malformed/unknown output,
  existing guided behavior and model qualification/routing contracts.
- Earlier native Windows test attempt: 17 passed; 23 setup errors because sandbox
  temp directories were inaccessible. A workspace-temp retry stalled and was stopped;
  the same affected cases pass in the isolated Linux test container above.
- Full guarded backend/lifecycle: **552 passed, one skipped, one inherited Starlette
  deprecation warning, 793.48 seconds**. Disposable lifecycle 0019 → 0006 → 0019 →
  base → 0019 → 0019 and zero Alembic drift. An earlier run passed 550 with one skip
  and failed only the old schema-0018 readiness expectation; that assertion was
  corrected before the clean rerun. The rerun also adds reviewer-demotion coverage.
- Browser: **three unique journeys passed**. Two existing guided access/checklist
  journeys passed in the initial run; the new pilot journey passed in **28.2 seconds**
  after correcting its test to sign out from Account. It verifies two-account label
  review, disabled-provider handling, zero counted fallback successes, reload and
  current-access report download. Axe violations and page overflow are zero at
  1440/768/360; [desktop](pilot-1440.png) and [mobile](pilot-360.png) were visually inspected.
- Static/contracts/documentation: Ruff/check+format, mypy (74 modules), generated
  OpenAPI/TypeScript parity, TS, ESLint, Prettier, source hashes, prior-package
  checks, source inventories, local Markdown links/anchors and whitespace pass.
- Normal local forward upgrade **0018 → 0019** preserves all 82 established table
  hashes/counts, all protected inputs and the 21 original artifact edits. The first
  migrate command used an old service image and left 0018 unchanged; rebuilding
  the migrate service applied 0019, then preservation was independently rechecked.
  Applied 0001–0019 are frozen. Normal app services are healthy.
- **One real Gemini guided connectivity call passed**, using the approved synthetic
  demo and the normal shared SQL ledger: two selected IDs, 143 input/nine output
  tokens, 18.477 seconds, $0 app charge. [Sanitized receipt](live-connectivity.json).
  This is an ordinary guided run, not a pilot case or quality result. The existing
  demo login has no explicit pilot grant; no grant was added. The four existing
  granted human accounts retain their access and can prepare/review the pilot.

All model outputs and human approvals in tests are explicit test doubles in isolated
`ppm_test`. **No live pilot calls or real human label review have occurred.**
No fabricated accuracy, automatic promotion or model-generated outcome labels.
Broad AT17 remains **BLOCKED** even if a later real-provider fixture pilot passes.

Provider policy/overlay fingerprints are unchanged. Gemini/Puter/Groq remain at
50/day/provider, one/minute and one concurrent request; qualified semantic classes
remain empty, benchmark-only remains true and Ollama remains off. No usage reset,
paid service, extra key, new PR/push or Sprint 13. Historical source/prompt/Word
records and the Sprint 12 closeout retain their original evidence.

[Machine-readable validation](validation.json) records all 12 final checks and
runtime readiness. Memberships, guided grants, project grants and shared provider
authority also hash-match the starting checkpoint after the new connectivity call.
Normal pilot history is empty: no human approval or live fixture measurement is invented.

See [walkthrough](../../limitations/FINANCIAL_SELECTION_PILOT.md) and
[API/schema contract](../../contracts/selection-pilot.md).
