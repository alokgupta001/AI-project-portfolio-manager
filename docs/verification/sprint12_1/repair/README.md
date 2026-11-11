# Sprint 12.1 timing-repair evidence

This directory contains new follow-up evidence, separate from the original stopped
pilot and its immutable receipts one directory above. See the
[repair report](../../../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md).

`pilot-timing-360.png`, `pilot-timing-768.png` and `pilot-timing-1440.png` are
isolated browser tests with a **mocked** timeout. They verify presentation, responsive
table scrolling and the separation of unavailable elapsed time from accepted-case
p95. They are not provider-performance evidence. The test also downloads the report,
checks the same timing value/kind, verifies the disabled next-case control and
checks the legacy “not recorded” display. Both journeys passed in 45.9 seconds.

The actual repair pilot is `3f0f3a7f-99c6-57f7-896b-205f9a54f0db`.
[Downloaded application report](live-pilot-report.json) and
[normal-ledger receipt](live-evidence.json) record five matches, then f06 TIMEOUT
with 22,037 ms unavailable elapsed. Six cases remain unattempted, including all six
held-out cases. The next-case control is disabled; state is **insufficient_data**.
The fixed twelve-case gate did not pass. Accepted-case p95 is 7,936 ms.

[Actual timeout screenshot](live-timeout.png) is live UI evidence, separate from
the mocked responsive screenshots. [Automated audit](automated-audit.png) records
the preparation step; it is not model evaluation evidence. Review provenance
remains human_reviewed=false. Broad AT17 is BLOCKED.

Transport phase logs cover only f01–f02. f03–f06 results are durable but their phase
events were not recovered after restart, so the timeout's exact cause remains
unresolved. The [repair report](../../../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md)
explains the bounds of the evidence and the session interruption.

[Validation](validation.json) records 566 backend passes, one skip, two browser
journeys and static/migration checks. [Preservation](preservation.json) verifies
144 protected files and unchanged historical/access rows. Original experiment
receipts one directory above remain unchanged; results are not combined.

[29 October closeout receipt](closeout.json) confirms no further model calls and
unchanged ledger/access state since the stop. The saved f06 history opened with
its usable rules-only checklist. [Stopped summary](live-stopped-summary.png)
shows the disabled next-case control, automated-review provenance and counts.
