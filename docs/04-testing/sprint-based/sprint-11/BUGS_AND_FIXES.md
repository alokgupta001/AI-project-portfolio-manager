# Sprint 11 bugs found during implementation

- Internal shared metrics contain typed record models. Initial capture used
  dictionary access directly and failed. Capture now uses the existing JSON
  encoder at that boundary. Hidden-risk/API integration fixtures verify it.
- A new analysis INSERT RLS parent lookup recursed through AI run read policy.
  Replaced it with a narrowly scoped trigger validating immutable parent identity;
  tenant/role INSERT RLS remains. Tested only in disposable 0013 candidates.
- JSON null versus SQL NULL initially conflicted with write-once output guards.
  New output mapping explicitly uses SQL NULL until publication. No normal 0013
  migration was applied during development.
- The first score-preservation assertion compared role-specific capability
  flags from Admin and PM views. It now compares the same authenticated role;
  original scores, answers and assessment revision remain unchanged.

The historical six PR #1 fixes remain protected by their original regression
tests. New AI dispatch preserves completed-call accounting and disabled
embedding admission behavior. No production/model quality bug is declared
resolved by an offline double.

- Browser integration found the new route missing from the shared account-load
  hook; it is now registered consistently with other authenticated screens.
- Maturity review keys originally used a colon rejected by the existing proxy
  path allowlist. Keys now use safe hyphens; the proxy boundary is unchanged.
- Browser polling exposed separate READ COMMITTED reads pairing old AI result
  data with a newly terminal job, which made polling stop too soon. `ai.access`
  now reads run/job in one statement. A deterministic two-transaction regression
  forces completion between reads and checks terminal diagnostics remain present.
- Document browser navigation raced its organization-switch POST. The test now
  waits for that response, retaining the original project-null version-append
  CodeRabbit regression unchanged.
- The real durable-worker browser path exposed metric tables registered only by
  web startup. The owning metrics module now registers its tables for worker
  callers too. A fresh-process test imports agents without the web application
  and verifies required metric registry entries; the real worker fallback passes.
- The new browser test initially tried to log out on the agents page. It now
  uses the existing account-page logout action. A temporary test collection
  error while adding the cold-import regression was corrected before the final
  executed regression set.
- A new scrollable specialist table lacked keyboard focus at 360px. All four
  scroll regions now have accessible names and focus targets, with an ArrowRight
  scrolling regression and zero automated WCAG violations at all three widths.
