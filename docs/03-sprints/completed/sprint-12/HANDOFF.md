# Sprint 12 final local handoff

25 October 2026. **Local sample complete; full original live/model acceptance OPEN.**
Normal schema **0018_csv_source_namespaces**; API/web/worker/dispatcher are healthy.
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

## PR review follow-up — 26 October 2026

[PR 7](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/7) is open
on `sprint-12-local-foundations`. The owner authorized checking/fixing its CodeRabbit
findings and pushing corrections. [Review evidence](../../../verification/sprint12/REVIEW_FIXES.md)
records all seven valid inline findings and the test nitpick. Forward 0018 isolates
implicit legacy CSV namespaces; applied 0001–0017 remain unchanged. Normal services
are healthy, all 77 established table hashes/counts and 26 frozen input hashes match,
and the 21 pre-existing artifact edits remain byte-identical. Fresh validation:
535 backend tests passed/one skipped (one inherited warning), lifecycle/drift,
ten focused integration cases, five Sprint 12 browser cases and nine static gates pass.
Both hosted CI runs passed for first-fix commit `faf1668`. CodeRabbit's second review
found two more valid source-identity issues; omitted CSV namespaces now isolate new
connections and canonical keys win over legacy NULL keys. Current affected checks:
36 backend cases, the strengthened keyed/legacy case, six browser journeys and static
checks pass. These supplement the preceding full gate, not a new full local run.
Fresh head CI and the next included CodeRabbit review are pending. CodeRabbit permits
one included review/hour; its last completed review was 25 October 21:19:46 UTC.
An hourly persistent follow-up was rejected by automatic approval review and is NOT
created; explicit authorization for recurring writes/pushes/review comments is pending.
Keep the current review loop within the included allowance. AT17 remains BLOCKED;
stop before 13 and never merge/deploy.
