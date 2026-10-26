# Sprint 12 — Import history and inspect a small baseline

26 October 2026. The local sample is complete at schema 0018. Its
[reviewed application checkpoint](../../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md)
passed CI and CodeRabbit's final review had no actionable comments. This does not
establish real-world prediction accuracy or live Jira/GitHub integration.

## What you can do

- In **Integrations & jobs**, an Admin approves a connector so work can continue
  after its creator signs out. Rotate or revoke that authority when needed.
  Source conflicts show saved local and proposed source values for human review.
- In **History & baselines**, an Admin imports dated numeric history or loads an
  explicitly synthetic example. The application freezes a dataset with provenance,
  time boundaries and separate training/validation/test entities.
- Run a small CPU baseline using the existing worker, inspect its model card and
  download its lineage/artifacts. Repeat the same dataset to check reproduction.
- Withdraw a history version to block later use of it and its descendants. Missing
  genuine outcomes correctly produce an insufficient-data result, not invented scores.

## Try it

Open the existing local website, choose an organization where you are Admin, and
follow [the complete walkthrough](../../03-sprints/completed/sprint-12/USER_GUIDE.md).
Use synthetic examples for demonstrations. Share a CSV namespace only for the same
source; omitted API namespaces are isolated automatically. Never paste credentials
into history JSON or use model output as an observed outcome.

## What remains open

Live connector credentials/source comparison and sufficient independently verified
outcome labels were unavailable. Synthetic metrics do not prove real accuracy.
Broad AI accuracy AT17 remains BLOCKED. No additional AI key, Ollama, paid service
or new always-on infrastructure is needed for this local journey. Forecast serving
and promotion belong to Sprint 13 and were not implemented.

[Technical report](../../03-sprints/completed/sprint-12/SPRINT_REPORT.md) ·
[Actual checks](../../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) ·
[Limitations](../../limitations/FUTURE_DEPLOYMENT_POINTS.md).
