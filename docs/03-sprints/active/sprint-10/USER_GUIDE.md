# Use AI operations and evidence previews

Sign in, select your organization and open **AI operations & evidence** (`/ai`).
New installations default to disabled source fallback. The configured local
Gemini free-tier provider is authorized at $0 on the verified unbilled project;
the confirmation does not expire daily. The screen's current status determines
which behavior to expect. Use synthetic development sources because selected
excerpts are sent to Google and free-tier content may improve its products.

## Admin walkthrough

1. Select an existing permitted project. In Document library upload a small UTF-8
   source, for example `Supplier delay is 15 days. Approval required.` Wait for
   **ready**. Scanner failure keeps it quarantined; do not bypass scanning.
2. Open `/ai` and inspect Provider status. A configured Gemini provider shows
   **Gemini free tier — $0 spending limit**; disabled/paused status means source
   fallback. Neither label establishes general model accuracy.
3. Select AI project. To exercise the embedding path, choose its ready source
   version and click **Index source embeddings**. Wait for the recorded terminal
   outcome; success stores a rebuildable 256-dimension projection, not a quality
   certification. Disabled provider or missing embedding model disables indexing.
4. Enter a matching Evidence keyword such as `Supplier` and click **Retrieve
   evidence preview**. Watch stage timestamps and run status. A supported model
   output contains only validated full source excerpts with current citations.
   `supported` is an answer label; a job may still be partial when a retrieval
   branch degraded. No matching permitted evidence means unavailable.
5. Read the excerpt/version and use **Revalidate citation**. Deleted, superseded
   or revoked sources no longer return their old evidence. The browser cannot
   retract text already viewed.
6. Inspect redacted diagnostics for attempt status, known token counts, latency
   and $0 ledger values. Unknown token usage stays unknown. No raw provider body,
   signature, API key or private reasoning is displayed.
7. Keep the tenant USD limit at 0. Concurrent AI runs can be 1–4; a current
   revision and Admin role are required to save. A positive tenant budget is
   rejected by the current $0 operator ceiling. Request limits remain active:
   four attempts/run and 20 attempts/tenant for runs created within 24 hours.
8. Cancel an active run if needed. If its revision changed, refresh before
   cancelling again. Cancellation blocks late publication. It cannot unsend a
   request already sent to Google.
9. Use **Refresh AI view** after an error or configuration/access change. History
   lists the latest 25 permitted runs. Daily renewal and re-entering the saved
   key are unnecessary. Initial/replacement-key setup belongs to the operator;
   see [Gemini setup](../../../07-setup-and-deployment/GEMINI-FREE-TIER.md).

## Fallback and failure recovery

`source_fallback` means the displayed result is source text, not a successful
generated answer. Missing keys/authorization, unavailable quota, request-count
limits, timeouts or invalid model output can produce explicit source fallback.
An indexing failure is recorded as a failure; it does not fabricate a projection.
No paid provider or alternate model is enabled automatically. Retry after the
actual dependency/limit recovers; ordinary users cannot raise Google's quota or
enable billing from this screen. Three consecutive provider failures can open the
separate 30-second circuit breaker; this is not a daily confirmation requirement.

## PM and Viewer

Provider status is visible, but starting/cancelling runs, budgets, operations and
diagnostics require Admin. Use Document library for permitted keyword search.
Project/assessment grants do not expose private evidence or workforce notes.
Organization switching resets the workspace; foreign run IDs disclose no evidence.

## Current limits

This is an extractive evidence preview. Agent findings, semantic maturity scores,
prediction, copilot chat and automatic plan edits remain planned. Model confidence
is not a maturity percentage. Indexing is limited to 20 chunks, semantic candidates
to 200 and the source picker to the first 100 permitted sources. Larger retrieval
sets fall back to keywords. See [recorded tests](../../../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md)
for what was actually verified; the steps above are a reproducible walkthrough,
not a claim that this documentation edit reran the UI or real provider.
