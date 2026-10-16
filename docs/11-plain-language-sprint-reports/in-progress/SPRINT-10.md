# Sprint 10 — Controlled AI evidence tools

**Status:** Local implementation verified; full provider/model-quality acceptance remains open. The 16 October Gemini follow-up adds a bounded free-tier demonstration, not full sprint closure.

## What was built and why it matters

The application gained one controlled way to request AI work, restrict its cost and permissions, keep run history and connect responses to source evidence. When a model cannot supply an answer, the screen can show clearly labelled permitted source excerpts rather than pretending an AI answer succeeded.

Open **AI operations & evidence** at [AI tools](http://localhost:3000/ai). Starting runs, diagnostics and budget controls are Admin-restricted; PM/Viewer use the Document library for permitted searches.

| Implemented function | Where to find it | How to check / expected result |
| --- | --- | --- |
| Evidence-preview request | Admin: **AI project**, **Evidence keywords**, **Retrieve evidence preview**. | Select a permitted project and a distinctive keyword from a ready source. The run reports its outcome and current source evidence. |
| Shared provider gateway | Behind AI requests; provider status is visible on `/ai`. | Read the status before interpreting a result. Disabled, expired, quota-limited and unavailable states must be explicit. |
| Source-only fallback | Run result labelled `source_fallback`. | With provider access unavailable, a matching source can still produce a labelled excerpt; no match remains unavailable. |
| Source/citation rechecking | Run evidence and **Revalidate citation**. | Revalidate a practice source. Removed, superseded or no-longer-permitted evidence must not remain newly retrievable. |
| Run stages and history | AI run list and details. | Inspect queued/running/final state and timestamps. Partial, failed and cancelled outcomes stay visible. |
| Cancellation | Active run cancellation control. | Cancel a suitable practice run and inspect its final state. Already committed effects/attempt accounting are retained. |
| Budget, concurrency and usage controls | Admin tenant budget and diagnostics on `/ai`. | Read the configured limits and redacted usage. A tenant setting cannot override the operator's provider/spend limits. |
| Optional source embeddings | **Index source embeddings**, when configured and authorized. | Read current availability. A successful index means a stored search representation, not proof of semantic search quality. |
| Repeatable evaluation cases | Developer test/evaluation files linked below. | Inspect recorded results and distinguish fixtures from real-provider checks. A fixture pass does not prove real model quality. |
| Gemini free-tier development follow-up | Provider disclosure/status on `/ai`; operator configuration. | Check whether the installation is active or paused. Confirmation expiry/quota/configuration can return it to fallback. |

An embedding is a numerical representation intended to help retrieval. Its existence does not mean the product has completed semantic assessments, a general copilot or autonomous agents.

## A check that works with source evidence

**You need:** Admin, a permitted practice project and a ready document. Start the scanner as described in [Getting access](../START_HERE.md). Read the current provider disclosure before making a request; enabled provider requests may transmit selected source text externally, so use a fictional practice source for this exercise.

1. In Document library, store a TXT containing `Practice supplier delay is 15 days. Approval required.` and wait for ready.
2. Open AI operations & evidence and select that project.
3. Search Evidence keywords for `supplier` and retrieve the preview.
4. Inspect the run status, result label, full excerpt and source version.
5. Revalidate the citation and compare the excerpt with the document preview.

**Expected result with provider disabled/unavailable:** A matching excerpt can appear with `source_fallback` and a partial outcome; it is source text, not a generated answer. Without a current matching source, the run remains unavailable.

**Expected result with currently authorized Gemini:** The bounded extractive response still needs a valid source/citation. Missing authorization, unavailable quota or failed validation can fall back. The verified project confirmation does not expire daily. The screen's current status determines which path to expect.

## The 16 October follow-up, explained simply

The recorded follow-up enabled Gemini on an operator-confirmed project without linked billing, with a maximum spend of $0 and limited attempts. At the user's request, the confirmation no longer expires after 24 hours; no daily renewal is required. One synthetic completion/citation check and one embedding smoke check passed. That establishes a narrow working connection; it does not establish broad answer quality or production readiness.

The application relies on the operator's confirmation about the external project's billing state. Its local $0 ledger does not independently prove that state. Confirm the billing state again if replacing the key/project, and keep billing unlinked. See [Gemini setup](../../07-setup-and-deployment/GEMINI-FREE-TIER.md).

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Evidence request, status, diagnostics and budgets | [AI screen](../../../apps/web/components/ai.tsx) |
| Run admission, limits, cancellation and accounting | [AI service](../../../services/api/ppm_api/ai.py) |
| Provider adapters and source retrieval | [Provider adapters](../../../services/api/ppm_api/ai_provider.py), [AI retrieval](../../../services/api/ppm_api/ai_retrieval.py) |
| Saved AI state | [AI tables](../../../services/api/ppm_api/ai_tables.py), [AI migration](../../../services/api/migrations/versions/0012_ai_runtime.py) |
| Evaluation and browser scenarios | [Evaluation](../../../services/api/ppm_api/ai_evaluation.py), [AI browser scenario](../../../tests/browser/ai.spec.ts), [Gemini browser scenario](../../../tests/browser/gemini.spec.ts) |

## Recorded checks and remaining work

The original sprint's disabled-provider tests and acceptance boundaries are in its testing report. The Gemini follow-up recorded 62 isolated AI/provider regression tests, one intercepted-status browser test and the separate real synthetic smoke. The browser test itself did not make real provider calls.

Full provider/model-quality acceptance, hosted CI and production gates remain open. Sprint 11 agents, semantic assessment findings, automatic score changes, automatic plan edits and the general copilot are not completed features here.

[Original sprint report](../../03-sprints/active/sprint-10/SPRINT_REPORT.md) · [Original testing](../../04-testing/sprint-based/sprint-10/TESTING_REPORT.md) · [Gemini follow-up evidence](../../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md) · [Report index](../README.md)
