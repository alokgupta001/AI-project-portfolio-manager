# Sprint 12 final local handoff

25 October 2026. **Local sample complete; full original live/model acceptance OPEN.**
Normal schema **0017_local_ml_foundations**; API/web/worker/dispatcher are healthy.
Open http://localhost:3000/ml as Admin in the existing synthetic demo organization.
Use [the walkthrough](USER_GUIDE.md), [report/tracker](SPRINT_REPORT.md),
[actual checks](../../../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) and
[contract](../../../contracts/ml.md).

- 528 full backend tests passed/one skipped, migration lifecycle/drift pass; 27 focused
  cases and 14 current offline cases pass; five final browser journeys pass. Sets overlap.
- API import/dataset/baseline/card/repeat/download and withdrawal flow is verified.
  Four final current-tree DB cases passed; the receipt is recorded in the test report.
- Normal 0016 → 0017 preserved all 77 established table hashes/counts, 26 frozen
  file hashes, five objects and eight original job/AI associations. Private dump,
  objects, starting diff and artifacts are in artifacts/local/sprint12. Never reset them.
- Gemini/Puter/Groq remain enabled for only the existing approved project scopes,
  shared 50/day, one/minute, concurrency one and $0; Ollama remains off. All original
  four users' memberships/grants and usage ledgers match the starting capture.
- No source credentials or complete genuine outcomes were available. Fixtures are
  explicitly synthetic; real imports are organization-attested. AT17 stays BLOCKED.
  Native MLflow tracking/import and larger/text candidates remain deferred.

The old migration image initially kept 0016; rebuilding it applied 0017 and all
preservation/readiness checks passed. Applied 0001–0017 are now frozen. Recover
routine app failures with retained data and a reviewed forward fix, never normal
lifecycle downgrade/reset. Existing local restart uses:

```powershell
docker compose -f compose.yaml -f compose.guided.yaml -f artifacts/local/guided-review/cloud.compose.yaml up -d --wait api worker dispatcher web
```

**Stop before Sprint 13.** No model serving/promotion, PR, commit/push/merge or
production deployment was performed. [Future deployment concerns](../../../limitations/FUTURE_DEPLOYMENT_POINTS.md)
are recorded separately; they do not block bounded local sample use.

## Publication follow-up

The owner subsequently authorized a new branch and PR for this completed local scope.
Publish `sprint-12-local-foundations` from the current main tree, excluding all 21
pre-existing artifact edits. Prior no-push statements describe the implementation
checkpoint. No merge, production deployment or Sprint 13 work is authorized.
