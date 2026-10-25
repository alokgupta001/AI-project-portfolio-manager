# Sprint 12 local sample and PR review closeout

26 October 2026. **Local sample accepted; full live/model acceptance remains OPEN.**
The reviewed application commit is `f93a5960d105518a2851582d7eac64910b6d58e8`
on [PR 7](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/7), branch
`sprint-12-local-foundations`. Local HEAD and the PR head matched at review closeout.
The documentation refresh follows that application checkpoint; its CI must be read
separately from the completed checks below. No merge or deployment is authorized.

## Delivered local behavior

| Package | Usable journey | Remaining external acceptance |
| --- | --- | --- |
| PPM-12-001 | `/integrations`: approval independent of creator sessions, generation rotation/revocation, isolated scheduling failures, canonical identity and version-checked source conflict review preserving local edits | Authorized live Jira/GitHub credentials, source equality and provider-side recovery/rotation |
| PPM-12-002 | `/ml`: immutable manual/fixture history, provenance/license/privacy checks, genuine-outcome contracts, target/horizon/as-of rules and temporal/entity splits | Independently verified genuine labels and suitable licensed external datasets |
| PPM-12-003 | Existing worker runs small reproducible CPU baselines; comparison, JSON lineage/artifacts, model cards, withdrawal and insufficient-data states are usable | Real model quality, native MLflow tracking/import and justified larger/text candidates |

CSV omission now creates an integration-specific namespace. Explicit `manual` or
custom namespaces still share source identity when intended. Canonical keyed sources
take precedence over legacy NULL-key rows; existing targets/local edits are preserved.
No forecast serving or promotion was implemented: that belongs to Sprint 13.

## Verified evidence

- Both hosted Foundation workflows passed for application commit `f93a596`:
  [PR workflow](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/40235833334)
  and [push workflow](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/40235828296).
- CodeRabbit's [latest completed review](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/7#issuecomment-6400061532)
  covered `faf1668..f93a596` and reported **no actionable comments**. It finished
  26 October at 03:58:46 IST (25 October 22:28:46 UTC), run
  `bbd3ba5a-3b48-43de-8896-5e22a77bd502`.
- Nine verified findings and one scheduling-test nitpick were corrected in two
  commits; all seven original inline threads are resolved. An earlier request was
  rate-limited; its initial acknowledgement was not completed review evidence.
- Final affected-path checks: **36 backend cases passed**, a strengthened keyed/legacy
  case passed separately, and **six browser journeys passed**. Static/contracts and
  source inventories passed. These sets overlap.
- The preceding first-fix full local gate passed **535 tests, one skipped**, with
  one inherited Starlette warning; migration lifecycle/drift passed. This predates
  the final two source corrections. Current-head hosted CI supplies the subsequent
  full regression evidence; no second full local run is claimed.

See [exact commands, failures and results](../verification/sprint12/REVIEW_FIXES.md),
[testing report](../04-testing/sprint-based/sprint-12/TESTING_REPORT.md) and
[package coverage](../requirements/coverage.md#sprint-12-package-trace).

## Preserved runtime and limits

Normal schema is **0018_csv_source_namespaces**, reached by forward migrations from
0016 through 0017. Applied 0001–0018 are now frozen. The recorded preservation checks
retain **77 established table hashes/counts**, **26 original frozen inputs**, five
original objects, eight original job/AI associations and all **21 pre-existing
verification artifact edits**. The latter remain local and excluded from the PR.
Starting diffs, private backups and fresh review screenshots remain under ignored
`artifacts/local/sprint12`; credentials and private receipts are not published.

Gemini/Puter/Groq, shared 50/day per-provider ceilings, one/minute pacing, one
concurrent request, $0 policy, approved project scopes and four-user access are
unchanged. Ollama remains off. Sprint 12 baseline work made no inference requests.
No extra keys, paid services, hosted fine-tuning or new always-on service is required.

AT17 remains **BLOCKED**. Synthetic evaluation is pipeline evidence only; AI outputs
are never true training labels. Real manual imports remain organization-attested,
not independent verification. External real datasets were not downloaded or accepted
without license/target review. Production concerns stay in
[future deployment points](../limitations/FUTURE_DEPLOYMENT_POINTS.md).

The owner-approved hourly follow-up was created after explicit authorization and
paused once the application review and CI were clean. Earlier pending-authorization
statements describe the preceding checkpoint. This documentation update does not
reactivate it or imply that a new documentation commit has already passed CI.

## Documentation authority

Current user/setup/learning/contracts/schema/status/report/tracker pages point here
and to the [latest handoff](../handoffs/LATEST.md). Original source/prompts, historical
sprint results, raw receipts, applied migrations and explicitly archived Word/generator
snapshots retain their original evidence. The maintained presentation/user guides are
Markdown; dated Word snapshots are not recertified for Sprint 12.

Use [the local user guide](../03-sprints/completed/sprint-12/USER_GUIDE.md),
[learning trace](../02-learning/06-ai-and-analytics/LOCAL_BASELINES.md) and
[behavior contract](../contracts/ml.md). Stop before Sprint 13.
