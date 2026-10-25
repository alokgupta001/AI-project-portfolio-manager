# Sprint 12 local implementation report

26 October 2026. **LOCAL SAMPLE ACCEPTED; full original live/model acceptance OPEN.**
Application commit `f93a596` is pushed to [PR 7](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/7).
Both hosted CI runs passed and CodeRabbit's final review generated no actionable
comments. Nine findings and one test nitpick were corrected. Normal schema is 0018;
[the closeout](../../../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records the current
status, preservation and remaining gates. This documentation refresh follows that
reviewed application checkpoint; it does not establish new live/model acceptance.

## Scope and tracker

| Package | Implemented local behavior | Acceptance |
| --- | --- | --- |
| PPM-12-001 | Narrow connector authority independent of creator sessions; generation rotation/revocation, scheduled polling via existing beat, canonical source identity, preserving/reviewing local edits with both version checks | Local API/browser controls accepted; live Jira/GitHub BLOCKED |
| PPM-12-002 | Immutable versioned aggregate history, provenance/permission declarations, five explicit targets, cutoff/horizon checks, label embargo, entity purging, withdrawal | Local dataset gates accepted; no externally verified genuine labels |
| PPM-12-003 | Durable CPU runs, constant + regularized linear + 32-tree RF comparisons, artifacts/hashes/model cards, reproducibility and insufficient-data states | Local CPU pipeline/cards accepted; real quality/promotion BLOCKED |

## Actual starting conditions

Normal schema verified as `0016_guided_project_access`; 77 existing tables captured
with private database/object backups before edits. There were zero connections,
zero ingestion sources, zero closed-sprint snapshots, zero completed projects,
four expenditures, two baselines, nine work items and one allocation. No connector
secret file/credentials were configured. These current-state records are not
complete dated outcome labels. No public external dataset was downloaded.

Twenty-one pre-existing verification artifact modifications were preserved. Frozen
.env, applied 0001–0016 migrations, original source/prompts and provider policies
are hashed. The forward migrations are 0017 plus the 0018 legacy CSV identity backfill. Legacy session-delegated connections
remain compatible until explicitly enrolled; enrollment never silently expands scope.

## Delivered journey

`/integrations` owns connection approval, secret-reference rotation, revocation,
manual preview/import, durable progress, source evidence and conflict review.
`/ml` owns manual numeric history import, isolated seeded fixtures, versioned dataset
creation, small worker jobs, saved model cards and authorized JSON artifact downloads.
No new always-on infrastructure or inference is used.

Real imports are organization-attested, not independently verified. Optional raw
text is excluded entirely; withdrawal blocks all descendant evaluation/downloads.
No AI-generated label is accepted. Dataset eligibility describes pipeline sufficiency,
not approval for production. All model promotion/serving stays blocked before 13.

## Validation and limitations

Actual commands/results are in the [testing report](../../../04-testing/sprint-based/sprint-12/TESTING_REPORT.md).
Native MLflow tracking/import is deferred: local artifacts provide an explicitly
identified MLflow-compatible JSON export, not a running MLflow service. XGBoost and
DistilBERT comparison is deferred until suitable genuine labels/resources justify it.
Synthetic metrics are pipeline evidence only. AT17, external credentials/source
comparison, real label quality and product deployment remain unresolved.

[User steps](USER_GUIDE.md), [contract](../../../contracts/ml.md),
[deployment follow-up](../../../limitations/FUTURE_DEPLOYMENT_POINTS.md).

## Final disposition and preservation

All three packages meet the bounded local definition of done. Full original external/model
acceptance remains OPEN. The original implementation gate passed 528 tests/one skipped. The first correction
passed a full local 535-case gate/one skipped with the inherited warning. Final affected
checks passed 36 backend cases plus a strengthened case and six browser journeys.
Full hosted CI subsequently passed the final application commit `f93a596`. Static/contract/inventory/source/audit checks pass. The test sets
overlap and are not additive. See the test report for the exact sequence and repaired failures.

Normal schema is 0018, services verified healthy; 77 original table counts/hashes, five objects,
26 frozen file hashes and eight original job/AI associations match. No inference occurred.
All 21 starting artifact modifications are preserved byte-for-byte. The installed dependency
inventory is deliberately regenerated; fresh browser regressions are saved under a new
Sprint 12 folder. No original source/prompts or applied 0001–0016 migration was edited.
After the normal upgrades, 0017 and 0018 are frozen too. No database/usage reset, new AI scope,
new human grant, merge, production deployment or Sprint 13 work. The implementation
and review fixes are committed/pushed to PR 7 with explicit owner authorization.

Publication is complete on `sprint-12-local-foundations`; all 21 unrelated artifact
edits remain outside the commits. The owner authorized the current documentation
reconciliation and push to the same PR. This does not authorize merge, deployment or Sprint 13.
