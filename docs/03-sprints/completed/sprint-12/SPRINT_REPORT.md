# Sprint 12 local implementation report

25 October 2026. **LOCAL SAMPLE ACCEPTED. Full original live/model acceptance remains OPEN.** Starting HEAD `c192d69a49c55240876d22c641360d44522d1eba`; current HEAD
and starting diff are captured privately in `artifacts/local/sprint12`. Changes are
captured at the local acceptance checkpoint. The owner subsequently authorized a new
`sprint-12-local-foundations` branch and PR; local validation below predates publication.
No fresh hosted CI or independent acceptance is claimed.

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
are hashed. New schema is forward-only 0017. Legacy session-delegated connections
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
acceptance remains OPEN. The full gate passed 528 tests/one skipped, with the inherited
Starlette warning; 14 offline and four DB cases verify the final tree, and five final
browser journeys pass. Static/contract/inventory/source/audit checks pass. The test sets
overlap and are not additive. See the test report for the exact sequence and repaired failures.

Normal schema is 0017, services healthy; 77 original table counts/hashes, five objects,
26 frozen file hashes and eight original job/AI associations match. No inference occurred.
All 21 starting artifact modifications are preserved byte-for-byte. The installed dependency
inventory is deliberately regenerated; fresh browser regressions are saved under a new
Sprint 12 folder. No original source/prompts or applied 0001–0016 migration was edited.
After the normal upgrade, 0017 is frozen too. No database/usage reset, new AI scope,
new human grant, PR, commit/push/merge, production deployment or Sprint 13 work.

Publication follow-up: the owner authorized committing/pushing the Sprint 12 changes
and opening a PR on `sprint-12-local-foundations`. The 21 unrelated artifact edits
remain outside that commit. This does not authorize merge, deployment or Sprint 13.
