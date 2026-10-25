# ADR 019 — Scoped unattended ingestion and local outcome baselines

25 October 2026. Accepted for the authorized local sample; full external/model
acceptance remains open. [Contract](../../contracts/ml.md).

Extend owning ingestion/delivery/jobs modules. An organization approves a connector
principal for one connection/project; database policy checks it independently of
creator sessions. Generation rotation cancels queued old work and live polling reuses
beat. Canonical record identity spans connection IDs. A source conflict stores a
candidate and optimistic versions; domain writes continue through the existing
validators. No automatic local edit replacement or new workforce permission.

Use immutable aggregate numeric history and outcome facts with explicit permissions,
provenance and five target definitions. Manual imports and seed-12 synthetic lineage
work without external credentials. No public dataset is fetched because no license
and target suitability review has established one. No raw notes are ingested. An
as-of manifest records label availability, horizon embargo and entity purging.

Use pandas 3.1.0 and scikit-learn 1.9.1, pinned/locked and BSD-3-Clause, compatible
with Python 3.12; [pandas metadata](https://pypi.org/project/pandas/3.1.0/) and
[scikit-learn installation](https://scikit-learn.org/stable/install.html).
One-thread constant, linear and bounded Random Forest baselines avoid an inference
service/model download. MLflow-compatible JSON tracking is an explicit local substitute;
native MLflow tracking/import remains an open limitation, not an implementation claim.
XGBoost/DistilBERT require suitable genuine labels and a later resource comparison.

No serving/promotion before Sprint 13. No hosted training, paid services or new AI
scopes. Existing Gemini/Puter/Groq ceilings, pacing, users, keys, ledgers and AT17
status are unchanged. Deployment controls are recorded separately.
