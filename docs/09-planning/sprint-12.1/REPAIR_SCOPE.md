# Sprint 12.1 repair-verification scope

Owner request: repair the failed financial API selection pilot using the added
repository tooling, then retry the interrupted work on 28 October 2026.
The supplied repair instructions explicitly authorize one new experiment, at most
twelve Gemini calls, through normal jobs and the shared ledger. This supersedes
the earlier “no further experiment authorized” statement only for this exact scope.

Prepared through the normal Ashu UI session in the existing Guided Review Demo ·
synthetic / Demo project: **3f0f3a7f-99c6-57f7-896b-205f9a54f0db**.
Original pilot **ce874a14-bbd0-50c5-b9b6-f7909a8bda8a** and both attempts are preserved.

The local API/worker allowlist is replaced with the new ID, never expanded to two
IDs. No project grant, role, provider data scope or account changes. The existing
four approved Demo Admin grants remain intact. The exact Fraction audit is recorded
through the UI with `kind=automated_rule_audit`, `human_reviewed=false`; no personal
attestation or second person's identity is used.

The experiment retains the original frozen CC0 numeric corpus, labels, prompt,
six calibration/six reserved split, Gemini model, 128 output-token reservation,
22-second deadline, shared 50/day ceiling, one/minute pacing, one generation slot
and $0 policy. It records measurement version `attempt-elapsed-v2`. Calibration
precedes reserved cases; no tuning or selecting successes across experiments.

Stop at the first unavailable/unknown attempt. Do not create another pilot, retry
until pass, reset ledger/health state, raise the 20-second gate or change provider.
All twelve exact matches and accepted-response p95 ≤20 seconds are still required.
Broad AT17 remains BLOCKED even if this synthetic fixture gate passes.

The private repair Compose overlay changes only the one-ID allowlist and local
worker INFO logging so sanitized timing events can be collected. It adds no service
and preserves provider policy files. Local builds/restarts are authorized; commits,
PRs, pushes, merges, production deployment and Sprint 13 are not in this scope.

See the [repair report](../../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) and
[timing contract](../../contracts/selection-pilot.md).
