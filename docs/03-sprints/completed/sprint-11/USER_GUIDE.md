# Sprint 11 user guide

Open `/agents` through **Agents & recommendations** in the workspace navigation.
The isolated browser test runs this screen against persistent synthetic data.
The normal database is not upgraded by this task; using this code in a normal
runtime requires a separately controlled forward application of 0013.

1. As Admin, choose an analysis project. Optionally select a private assessment
   you may read and up to five ready document versions. Existing source-library
   controls still govern upload, scanning and version readiness.
2. Select **Run nine specialists**. Run details show execution status, model,
   cost, source snapshot hash and versions. Expand processing stages to see
   progress. **Cancel specialist run** uses the existing revision/fencing rules.
3. Inspect all nine outcomes and missing agents. Provider-disabled, timeout,
   quota or malformed responses retain deterministic metric findings where
   possible and label semantic interpretation unavailable. Missing data does
   not mean healthy. No provider upgrades occur automatically.
4. Open a candidate to read its exact source spans, source version/hash,
   severity, separate confidence, discrepancies and improvement prompt. Treat
   documents and model interpretations as untrusted evidence for review.
5. For an assessment, compare **Original deterministic**, **AI suggestion** and
   **Reviewer approved** columns. Maturity uses 0–100; confidence uses 0–1 and is
   uncalibrated. Unknown suggestions stay unavailable rather than becoming zero.
6. A different authorized human reviews the run. Ordinary findings require
   independent project edit authority; assessment-linked runs require the
   assigned independent assessment reviewer plus project scope. Enter a reason
   and optionally an approved maturity override. **Accept as reviewed** records
   a decision only. **Reject suggestion** appends a rejection and preserves all
   prior decisions. Original scores and project plans are unchanged.
7. Refresh/reopen the run. Source, assignment, group-size and permission changes
   can make old evidence unavailable. Acceptance is disabled for unsupported
   proposals. Start a new analysis after fixing inputs; do not reuse old sources
   as if they were current.

Sentiment is a team delivery-blocker support signal from a privacy-safe summary,
not an individual/emotional label. Groups below five or insufficient capacity
scope are suppressed. No individual workforce note is passed to this agent.

Real-model quality is **UNVERIFIED/BLOCKED**. The deterministic demo is evidence
of application controls, not a claim about real-provider interpretation quality.
