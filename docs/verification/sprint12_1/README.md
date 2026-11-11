# Sprint 12.1 — Actual evidence

26 October 2026. [Report](../../03-sprints/active/sprint-12.1/SPRINT_REPORT.md) ·
[Actual run](../../03-sprints/active/sprint-12.1/RUN_RECORD.md) ·
[Tests](../../04-testing/sprint-based/sprint-12.1/TESTING_REPORT.md).

## Current automated run

- [Actual downloaded report](live-pilot-report.json): immutable automated label
  provenance, frozen protocol and human_reviewed=false.
- [Sanitized ledger/call evidence](live-evidence.json): two starts 88.659s apart,
  one attempt each, f01 match at 21.437s, f02 TIMEOUT/unknown. One measured,
  one unavailable, ten unattempted, zero reserved measured. $0 app charge;
  timeout usage and external billing unverified. Fixture gate unmet, AT17 BLOCKED.
- [Automated provenance visible](automated-audit-recorded.png) and
  [stopped pilot visible](live-pilot-stopped.png): actual normal UI, separate
  from the isolated mocked browser journey.
- [Fresh software validation](automated-validation.json): 562 backend passes/one
  skip, guarded lifecycle/drift, two browser journeys, static/contracts/docs and
  preservation checks. Test totals overlap earlier runs.

The arithmetic audit checked 12/12 labels; that is label consistency, not twelve
successful model cases. No human review, promotion, genuine outcome/training
label, quota reset or retry occurred. The approved run ended under its stop rule.

## Historical preparation receipts

- [Four demo-only grants](demo-grants-approved.json): owner-approved four existing
  Admin accounts; other access/policy/usage rows unchanged at that timestamp.
- [Prepared pilot](prepared-pilot.json): Ashu created ce874a14, awaiting review
  with zero cases at that timestamp; [visible preparation](pilot-awaiting-review.png).
- [Offline arithmetic audit](automated-label-check.json): 12/12 draft labels,
  human=false, no app review write at that earlier timestamp. The later approved
  app audit is a distinct event in the current report.

Automatic approval review rejected removing the grant check; that patch never
applied. The owner approved narrow grants, then separately the one-pilot local
automated exception. Every endpoint still requires current Admin plus an explicit
guided grant. Other pilots retain their different-person review gate.
[Earlier implementation receipts](../financial-selection-pilot/README.md).
