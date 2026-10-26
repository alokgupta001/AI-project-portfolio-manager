# Sprint 12 local implementation plan

Execution status — 26 October 2026: this plan's bounded local scope is
implemented at 0018 and reviewed on PR 7. [Closeout](../../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records
actual evidence and retained live/model gates. The original plan/acceptance below
is retained; do not rerun the starting prompt or begin Sprint 13 automatically.

25 October 2026. **Plan retained; local sample implemented and accepted; full external/model gates open.**
[Current report](../../03-sprints/completed/sprint-12/SPRINT_REPORT.md). Supplements the original
[Sprint 12 packages and acceptance](../FUTURE_SPRINT_ROADMAP.md#sprint-12--connector-reliability-and-historical-model-foundations)
under the [current local plan](../LOCAL_SAMPLE_PLAN_UPDATE.md).

Deliver a usable local journey: import or sync history, review source conflicts,
build an as-of dataset, run a small baseline, and inspect its model card and
eligibility. Do not require more AI keys, Ollama, paid services or new always-on
infrastructure. Preserve the existing guided sample and its permissions/quotas.

## Work packages

| Package | Local implementation and acceptance | Separately retained gate |
| --- | --- | --- |
| PPM-12-001 | Narrow organization-approved connector principal independent of an interactive session; rotation/revocation; source identity deduplication; cursor/rate/partial recovery; version-checked conflict review preserving local edits. Test logout, principal revocation, two connections, stale conflicts and tenant isolation. | Authorized real Jira/GitHub source comparison and sync; fixtures are not live acceptance. |
| PPM-12-002 | Versioned dataset manifests with source/license/privacy/schema/label provenance, target/horizon/cutoff and outcome definitions. Historical velocity, bugs, scope, spend, dependencies and allocations where available. Reject leakage/unsuitable targets, separate temporal/entity splits without overlap, exclude withdrawn text. | Genuine labels for each claimed target; synthetic or heuristic labels cannot establish real accuracy. |
| PPM-12-003 | Reproducible CPU-friendly baselines and evaluations, lineage/hashes/artifacts, model cards, missing-data behavior and explicit eligibility states. Compare to a simple baseline and repeat within a documented tolerance. | Insufficient genuine outcomes means model promotion BLOCKED. Forecast serving/promotion belongs to Sprint 13. |

Define delay, overrun, risk, failure and sentiment targets explicitly, including
when a target cannot be supported by available history. Do not invent outcome
labels or mistake a risk heuristic for observed failure. Use appropriate MAE,
PR-AUC/recall/calibration/Brier measures only for compatible tasks, with sample
size, imbalance, split and uncertainty context. Synthetic demo metrics must be
visibly labeled and excluded from real evaluation.

## Implementation constraints

- Inspect current ingestion, durable jobs, source history, permissions and UI first.
  Extend owning modules/screens for connector work; the roadmap's proposed `ml.py`
  and `/ml` paths do not require moving connectors or duplicating access/formulas.
- Use pandas/scikit-learn small baselines with bounded data, jobs and RAM. Preserve
  the MLflow artifact/lineage requirement with a local approach or explicit tracked
  limitation; do not silently delete it or require a new always-on server. Compare
  Random Forest/XGBoost and text candidates only where suitable. DistilBERT is not
  mandatory on this RAM-constrained host.
- Prefer already authorized history/manual imports. If external data is useful,
  verify license, provenance, privacy and suitability for the exact target before
  using it. A Kaggle, Hugging Face or PROMISE listing alone is not proof of fit.
  Keep seeded synthetic fixtures in a separate demo lineage.
- Optional text needs consent and revocation handling. Do not send new datasets or
  notes to the existing AI APIs; their approved bounded guided scopes stay intact.
- Inspect and capture the dirty working tree and schema before editing. Preserve
  existing records/objects, keys, grants, quota ledgers and unrelated artifacts.
  Verify current head (0016 at handoff); use new forward migrations only.
- Expose progress, empty/error/insufficient-data states and artifact/model-card
  review through a usable API/UI. Scripts alone do not complete the requested journey.

## Definition of done

All three packages have tested local implementations and an end-to-end recorded
journey. Validate relevant unit/integration, negative access, source/version,
leakage, migration/drift, reproducibility, browser/accessibility and regression/
static/contract checks. Record actual commands and results, not expected passes.

Update sprint tracker, report, handoff, user/learning/demo/test guides, API/schema
docs and coverage according to the [shared checklist](../SPRINT_DOCUMENTATION_CHECKLIST.md).
Record missing live integration or genuine model evidence explicitly. Local pipeline
acceptance can be complete while those gates remain blocked; full original Sprint
12/product acceptance cannot be claimed until its required evidence exists.

Do not reopen Sprint 11 AT17 as a prerequisite for independent data work, relabel
it as passed, or use its unqualified outputs as labels. Failed access/integrity
checks still block dependent work. Keep production concerns in [future deployment
points](../../limitations/FUTURE_DEPLOYMENT_POINTS.md). Stop before Sprint 13.

Use the [starting prompt](START_PROMPT.md) to begin implementation separately.
