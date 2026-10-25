# Sprint 12 final local handoff

26 October 2026. **Local sample complete; full live/model acceptance OPEN.**
Normal schema is **0018_csv_source_namespaces**; the local runtime was verified
healthy after the final source fixes. [PR 7](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/7)
contains application commit `f93a596`. Both hosted CI runs passed, and CodeRabbit's
final review of that commit reported **no actionable comments**. See
[the closeout](../../../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md),
[review evidence](../../../verification/sprint12/REVIEW_FIXES.md),
[actual checks](../../../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) and
[report](SPRINT_REPORT.md).

## Use and recover the local sample

Open http://localhost:3000/ml as Admin in an existing authorized organization.
[User steps](USER_GUIDE.md) cover history → dataset → baseline → repeated model card
→ download → withdrawal. `/integrations` owns connector approval, rotation/revocation
and source conflict review. CSV omission isolates identities; explicit namespaces
remain shareable. Canonical keys win over legacy unkeyed rows without deleting targets.

Existing local restart, with the approved private configuration retained:

```powershell
docker compose -f compose.yaml -f compose.guided.yaml -f artifacts/local/guided-review/cloud.compose.yaml up -d --wait api worker dispatcher web
```

Rebuild the owning images before a future code/schema change, including `migrate`
for a new forward migration. Never bootstrap/reset an established installation or
downgrade normal data. Applied **0001–0018 are frozen**; earlier image/retry failures
remain documented in the testing report.

## Evidence and preserved boundaries

- Final affected checks: 36 backend cases, the strengthened keyed/legacy case and
  six browser journeys pass; static/contracts/inventories pass. The preceding full
  local run passed 535 tests/one skipped with one inherited warning and lifecycle/drift.
  These sets overlap; the full local run predates the last two fixes, which subsequently
  passed full hosted CI on `f93a596`.
- Forward 0016 → 0017 → 0018 preserved 77 established table hashes/counts and 26
  original frozen inputs; original five objects/eight job links were verified at the
  implementation checkpoint. All 21 original artifact edits remain byte-identical,
  local and excluded from the PR. Private diffs/backups/receipts are in
  `artifacts/local/sprint12`.
- Gemini/Puter/Groq retain approved scopes/four-user access, shared 50/day ceilings,
  one/minute pacing, concurrency one and $0. Ollama is off; no Sprint 12 inference.
- Genuine outcomes/live connector credentials were absent. Synthetic metrics are
  demo evidence only; AT17 stays BLOCKED. Native MLflow/larger text candidates,
  deployment and real quality remain separate gates. [Deployment concerns](../../../limitations/FUTURE_DEPLOYMENT_POINTS.md)
  do not prevent local use.

The hourly review follow-up was explicitly approved, created and then paused when
review and CI were clean. Earlier pending-authorization/rate-limited states are history.
The owner authorized this documentation refresh and push to the existing PR; its
new CI status is separate from application `f93a596`. No merge/deployment or Sprint 13.
