# Sprint 09 bugs, fixes and retained failed runs

These are implementation-run findings, not newly executed application checks from
the documentation follow-up. Exact accepted commands/results are in
[TESTING_REPORT.md](TESTING_REPORT.md); intermediate logs are retained.

| Finding | Correction | Accepted evidence / remaining limit |
| --- | --- | --- |
| Initial pypdf 6.12.0 dependency audit reported known vulnerabilities | Pin 6.20.1 in the lock and rebuild | Locked Python audit reports no known vulnerabilities; this is not an OS/security certification |
| Initial document browser flow could reopen a source while a save was pending and display stale data | Disable Open during pending loading/save | `sprint09-browser-accepted.txt`: one affected scenario passed; 14 earlier regressions passed in a separate full run |
| Narrow tables compressed words into vertical letters | Minimum table width in a focusable horizontal scroll region | Final 1440/768/360 renders reviewed; WCAG-tag/body-overflow checks passed |
| Full worker recovery test timed out under load even after attempt 2 began | Widen bounded startup/recovery harness waits without changing the real lease, SIGKILL, attempt-2 or 500-unique-effect assertions | Full final backend run: 123 passed; no performance SLA inferred |
| Archived-project scope could omit held/referenced originals from orphan eligibility | Narrow live-Admin retention-reference function includes all protected references | Final nine security cases passed, including held archived-project objects |
| Forged broker tuple risked cancelling another valid document job | Require persisted matching authority and revoke old worker cancellation entry point | Final security/migration acceptance passed |
| Sources beyond 5,000 chunks could have an inaccessible tail | Reject over-limit expansion | `sprint09-chunk-limit.txt`: one boundary case passed; API/worker rebuilt and healthy |
| Running older browser specs wrote screenshots over historical names | Preserve 13 fresh renders under Sprint 09 names and restore committed originals | Old evidence retained; local checkpoint hashes current files |
| Initial normal-data comparison saw one added refresh-token row while old services were live | Preserve it; take fresh quiesced rollout backup/manifest before migration | All 62 established table hashes/counts match the quiesced baseline, five objects and ten old migrations unchanged |

Local runtime/path-wrapper failures and early failed selector attempts remain in
intermediate logs; they are not recorded as passes. Hosted CI, archived Word visual QA,
production backup erasure/storage, availability/performance and real connector acceptance
remain open. Semantic findings, embeddings and later workflows are deferred scope,
not repaired by these fixes.
