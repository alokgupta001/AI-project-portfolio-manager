# From source conflicts to honest local baselines

Start with [the local walkthrough](../../03-sprints/completed/sprint-12/USER_GUIDE.md)
and [contract](../../contracts/ml.md). This feature has no LLM dependency.

`jobs.worker_transaction` distinguishes an enrolled connector generation from the
older interactive session. `connectors.connector_principal` sets a transaction-scoped
Connector role; `ppm_connector_scope` limits RLS to one project. `delivery.lock` rechecks
that grant for each effect. The same organization lock orders revocations and writes.
`jobs.apply_source` derives canonical identity before domain creation. Local revisions
cause `record_conflict`, not an overwrite. `resolve` validates source fingerprint,
conflict revision and the current local revision, then uses `delivery.write`.

`HistoryInput` rejects raw text/AI labels and separates synthetic/observed lineage.
`ml_pipeline.label` derives delay/overrun from outcome facts, failure from recorded
disposition, risk from independent outcome adjudication, and sentiment from consented
team survey aggregates. A reference is a traceable import assertion, not a guarantee
that the underlying enterprise record is correct. Never treat a current heuristic as
observed failure. Existing normal data has no complete dated outcome history.

`build_dataset` checks which facts were known at each observation. It drops labels
not available by a split boundary and observations whose horizon crosses that boundary.
If an entity appears on both sides, all its candidate observations are purged. This
costs data but prevents the same project/team identity leaking between partitions.
The manifest records every exclusion, label reference, hash and missing feature count.

`evaluate` fits imputation/scaling on training only. Validation selects by MAE or
Brier; the held-out test is reported separately. The fixture has 30/30/30 observations.
A constant baseline prevents an attractive model score hiding a trivial target.
Random Forest has 32 trees/depth 4/one thread. Artifacts use JSON, not untrusted pickle.
The card shows imbalance, descriptive bootstrap uncertainty and exact repeat hashes.
These measurements verify a pipeline; synthetic success says nothing about real data.

Debug queued work via existing worker/beat health and the run ID. `insufficient_data`
is an expected result when outcomes/splits/classes are missing. A withdrawn history
causes source_unavailable/409 and blocks descendants. New authorization requires a
new history version. Native MLflow import, larger candidates, live source equality,
independent label verification and deployment remain separate work.

## Why the final source identity fixes matter

API creation uses `ConnectorConfig.model_fields_set` to distinguish an omitted CSV
namespace from an explicitly shared `manual` value. A deterministic integration UUID
makes the generated namespace stable across a create replay. During sync, `apply_source`
orders canonical keyed matches before own legacy NULL-key matches, preserving existing
targets and avoiding a uniqueness collision. [Final review/CI closeout](../../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md)
and the keyed/legacy/omission regressions record the verification; they do not establish
live provider equality. Loading/poll cancellation examples are in the frontend contract.
