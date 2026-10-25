# Try Sprint 12 locally

Use the existing local stack and account at http://localhost:3000. Select an
organization where you are Admin. Existing roles and the four users' guided grants
are preserved; research administration does not grant access to another organization.

1. Open **Integrations & jobs**. Create a CSV fixture connection for an accessible
   project. The namespace identifies the source: share it for two connections to the
   same source; change it for unrelated CSVs whose IDs overlap. Preview and start sync.
2. Under **Organization connector authority**, approve the connection. It can now
   complete queued work after logout. Rotate to invalidate earlier queued generations;
   submit new work afterward. Revoke to stop scheduled/queued work. Live polling needs
   an already configured tenant/provider-prefixed server credential reference and
   explicit approval of its exact source. Never paste a key into the UI.
3. Edit imported work in Projects, then import a newer upstream value. Refresh
   **Source conflicts**. Compare current local and proposed source values; choose
   **Keep local edits** or **Accept reviewed source**. Any intervening local or source
   revision makes the action fail; refresh and review again. Existing lifecycle
   transition rules still apply. Partial jobs retain their prior cursor for safe replay.
4. Open **History & baselines** (`/ml`). Pick the existing synthetic demo project,
   choose a target, and **Load synthetic example**. It contains 90 numeric records
   in three dated cohorts, with seed 12. Inspect the JSON and **Import history version**.
   This is visibly synthetic and never evidence of real accuracy.
5. **Build dataset version** with the supplied 2025 dates and 30-day horizon. Inspect
   the manifest for provenance, exclusions, class balance and split counts (30/30/30
   for the fixture). Each build is immutable and separately identified by a hash.
6. **Run CPU baseline**. Wait for the existing worker, inspect its model card,
   metrics, uncertainty, baseline comparison and limitations. Repeat the same dataset:
   the card reports whether its result hash matches. Download the card/artifacts JSON.
7. **Withdraw** the history version when its permission/consent is withdrawn.
   New builds/runs and existing artifact delivery now fail closed. A withdrawn version
   cannot be restored; a newly authorized import creates another version.

For your own history, replace the fixture JSON with aggregate observations from the
selected project, set `lineage=real`, `license=organization-authorized` and
`label_declaration=observed-outcomes` (or `unlabeled`). Record the source/origin,
permission, as-of feature timestamps, baseline-known timestamp and actual outcome
references. Numeric facts must be known at the observation; labels become available
later but by each split boundary. Do not relabel fixtures or AI results as real.
An empty/unlabeled history is allowed and produces **insufficient_data**, with no
invented metrics. External real datasets are rejected pending a separate license and
exact-target review. No raw notes, individual identifiers or workforce rankings.

If a run stays queued, check the existing worker/dispatcher health; do not start
Ollama. If it fails, retain the sanitized diagnostic and dataset hash. No forecasts
are served. Gemini/Puter/Groq guided review and its existing limits remain available
at `/agents`; the baseline lab makes no AI requests.
