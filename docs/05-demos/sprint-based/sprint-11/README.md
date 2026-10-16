# Sprint 11 executable synthetic demo

Use the existing isolated browser runner; do not bootstrap normal data or load
real keys. Command from the repository root:

```powershell
node scripts/check-identity-browser.mjs agents.spec.ts
```

It builds the dedicated browser stack, sets all runtime providers disabled,
creates disposable identities and calls guarded `browser_agent_fixture.py`.
The fixture uses an in-process adapter double and a hard network denial to
persist a semantic run at USD 0. No synthetic provider configuration is saved.

The reviewer opens `/agents`, sees reported-health discrepancy and missing
specialists, opens exact text evidence, accepts suggested maturity 87.5 as 75
with a reason, rejects it and reloads persistent history. Original score 0
remains. Admin then starts a real durable run with provider disabled and sees
explicit partial fallback and self-review denial. Responsive screenshots and
WCAG automated checks run at 1440/768/360 pixels.

Synthetic names, scores and interpretations demonstrate controls only. General
real-provider interpretation quality remains **UNVERIFIED/BLOCKED**. No automatic
project edit, external notification or Sprint 12 model pipeline is demonstrated.

[User steps](../../../03-sprints/completed/sprint-11/USER_GUIDE.md) ·
[Actual results](../../../04-testing/sprint-based/sprint-11/TESTING_REPORT.md)
