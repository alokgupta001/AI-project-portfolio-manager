# Local history and baseline contract — v1

Owning modules: `connectors.py`, existing `jobs.py`/`ingestion.py`/`delivery.py`,
`ml_schemas.py`, `ml_pipeline.py`, `ml.py`, `ml_tables.py`. Schema 0017 adds five
scoped tables and two durable-job columns plus canonical source keys. See the
[generated database dictionary](../01-architecture/DATABASE-DICTIONARY.md).
Forward data migration 0018 assigns an integration-specific namespace only to legacy
CSV configurations without one. Explicit namespaces (including `manual`) stay unchanged;
affected derived source keys are rebuilt in place on sync, preserving local targets.
Queued legacy job snapshots use the same fallback without rewriting their history.

## Connector authority

`GET/PUT /api/v1/integrations/{id}/authority` uses Admin + Origin/CSRF + active
organization + `If-Match` (0 for initial enrollment). Every approval/rotation increments
revision and generation. Secrets are environment references with tenant/provider
prefixes; no raw credential is accepted. Live reference configuration remains local
operator work; rotation updates the reference and fences pending old generations.
A principal authorizes only imported work/sprints in its exact project. RLS adds
scoped connector policies, never Admin sessions or new memberships. Original actor
and session IDs are attribution, not effective authority. Unenrolled connections
retain the older live-session contract. Revoked enrollment cannot fall back to it.

Optional live polling uses the existing beat/dispatcher every ten seconds; configured
interval is 1–10080 minutes (0 off), no overlap with pending jobs, at most 20 due
connections per dispatch. Existing page/rate/retry/lease/cursor limits apply. Revocation,
rotation, connection disable and project archival are rechecked at every source effect.
Scheduling errors roll back only that connector and attempt a five-minute backoff in a
separate scoped transaction; later connectors and due job dispatch continue. Revoked or
disabled connectors cannot regain authority through this recovery path.

Canonical identity hashes provider/mode/normalized resource/Jira project/board/entity/
CSV namespace/external ID within tenant+project. Remote providers ignore the manual namespace. Unique database constraint plus the
existing organization lock prevents two connections creating the same new logical
record. Legacy null keys are matched across compatible connections on first sync;
ambiguous legacy duplicates stop rather than delete or overwrite records.

`GET .../{id}/conflicts` returns current local values and newest pending source
candidate. `POST .../{id}/conflicts/{conflict}/resolve` requires Admin, conflict
`If-Match`, exact source fingerprint and reviewed current local revision. New source
versions supersede pending candidates, invalidating old reviews. Keeping local edits
acknowledges that source version without writing domain fields; its local override remains protected on subsequent upstream changes. Accepting uses the
existing delivery validator/audit/lifecycle. Same-timestamp content collisions are
reviewable, never silent overwrites. Conflict errors retain the existing
`LOCAL_REVISION_CONFLICT` job code. Partial sync does not advance the cursor.

## History and datasets

`GET /api/v1/ml/template?project_id=...&target=...` returns a seeded fixture and
example dataset specification. `GET/POST /histories`, `POST /histories/{id}/withdraw`,
`GET/POST /datasets`, `GET /datasets/{id}`, `GET/POST /runs`, `GET /runs/{id}` and
`GET /runs/{id}/artifacts` are relative to `/api/v1/ml`. All research routes require
Admin, project validity and tenant RLS. Writes require Origin/CSRF + active organization;
creates require an idempotency key (1–100 characters). Replays with different input
fail 409. Request bodies are capped before JSON parsing at 650 KB, imports at 500 rows.
Lists return the newest 100; retain identifiers for older versions/artifacts.

History versions are immutable, with permanent withdrawal as their sole update.
Datasets are append-only and hash their manifest/rows. Project composite FKs prevent
cross-project lineage. Only aggregate numeric feature columns are accepted: velocity
(team points/period), bugs/count, scope change/work-count delta, spend ratio,
dependencies/count and allocation/percent. Unknowns stay null. Raw text is rejected,
so consent withdrawal cannot leave text in training. Dataset/run/artifact delivery
rechecks withdrawal and current authority. Downloads already copied out cannot be
recalled; retention/erasure beyond local use is a deployment follow-up.

Features and baseline facts must be known by observation; all timestamps need UTC
offsets and finite values. Outcome must follow observation, label availability cannot
precede outcome, and outcome must fall inside the declared horizon. Labels must be
available at train/validation/cutoff boundaries. Rows crossing a horizon boundary are
excluded; an entity occurring in multiple splits is purged entirely. No temporal or
entity overlap is allowed. The manifest records exclusions and evidence references. Complete-case selection
inside a horizon can bias results when delayed/censored outcomes are excluded.
This is not survival analysis; missing outcomes never become negative labels.
Historical timing is importer-attested and cannot detect falsely backdated facts.

| Target | Outcome definition | Metric |
| --- | --- | --- |
| delay | Positive days actual finish exceeds plan known at observation; project/milestone/sprint history | MAE, days |
| overrun | Positive percent actual spend exceeds approved budget known at observation | MAE, percentage points |
| failure | Observed cancellation, abandonment or missed commitment versus accepted delivery | PR-AUC (average precision), recall at .5, Brier, calibration bins |
| risk | Independent outcome adjudication of adverse category 0/1; never a current heuristic | Same classifier metrics; no heuristic accuracy claim |
| sentiment | Consented team survey mean <=2 on a 1–5 scale; minimum five respondents | Same classifier metrics; no individual diagnosis |

Real histories require an explicit organization authorization and observed-outcome
(or unlabeled) declaration. Imports are attestations, not independent verification.
Synthetic and observed labels cannot mix. AI/heuristic evidence references are rejected.
No external real dataset is accepted by v1 without separate license/target review.
The internal seeded fixture is CC0-1.0; its lineage remains synthetic.

## Evaluation and eligibility

Minimum 12 training, 4 validation and 4 test rows; classifiers need both classes in
each. Missing/out-of-horizon/unavailable outcomes yield reasons, not invented labels.
Insufficient inputs still produce an inspectable model card without metrics.

Existing durable jobs carry `ml_run_id`, use the current Admin/session authority,
and serialize bounded CPU work with the organization lock. Interrupted transactions
roll back and are rediscovered. Maximum three pending jobs per tenant, 500 rows,
32 trees, depth 4, one CPU thread, seed 12. Preprocessing fits training medians and
missing indicators only; empty training columns use zero. Constant mean/prior,
Ridge/logistic and Random Forest are compared on validation MAE/Brier; a fixed tie-break
selects the reported held-out test result. Tests are never used for tuning.
Two hundred seeded row bootstraps give descriptive 95% intervals, not population proof.

Cards record dataset/code/library/seed/model/artifact hashes, counts/imbalance,
validation/test results, baseline comparison, missing data and limitations. JSON
artifacts contain predictions, forest trees, linear coefficients and preprocessing;
no executable pickle or forecast endpoint. Repeats compare stable result hashes;
documented numeric tolerance 1e-10, actual pinned-environment checks use exact equality.
Eligibility is `insufficient_data`, `demo_only`, `research_only`, `source_unavailable`,
`authority_revoked` or `evaluation_failed`. All promotion/serving remains BLOCKED before
Sprint 13. Synthetic metrics never establish real accuracy. Native MLflow tracking/import,
XGBoost and text model comparisons remain explicitly deferred; an MLflow-compatible
JSON record preserves local tracking provenance without a new service.
