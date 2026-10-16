# Sprint 10 current evidence demo

Use the [Admin user walkthrough](../../../03-sprints/completed/sprint-10/USER_GUIDE.md)
with synthetic project sources. This is an extractive preview, not a copilot or
semantic agent demonstration. Current Gemini setup is free-tier only at $0,
with one-time confirmed unbilled project/key and no daily renewal.

## Configured Gemini path

Upload a small fictional source and wait for ready. On `/ai`, verify the Gemini
status and zero ceiling; select the project/source and index embeddings. Then
query a matching keyword, inspect the exact supported excerpt, recorded stage
outcome and current citation. Revalidate it, then inspect redacted diagnostics.
Quota/timeout/invalid output can truthfully produce a partial source fallback;
do not describe such an outcome as a successful model answer. This path uses
the real free-tier quota, so keep demonstrations bounded and synthetic.

## Disabled/fallback path

The isolated browser fixture explicitly disables provider authorization and key.
It exercises no-key source preview, no-evidence unavailability, Admin controls,
transport recovery and Viewer denial without any real model request. Do not
disable a shared live configuration just to stage this demonstration.

Automated fallback journey:
`node scripts/check-identity-browser.mjs tests/browser/ai.spec.ts`.
UI disclosure/recovery fixture:
`node scripts/check-identity-browser.mjs tests/browser/gemini.spec.ts`.
Offline validator gates: `python scripts/evaluate_ai.py` (12 cases, not model
quality). Real synthetic completion/embedding smoke passed separately; see
[Gemini evidence](../../../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md).

No new demo/provider/browser execution is claimed by the documentation audit.
All nine agents, semantic scores and automatic plan changes remain unavailable.
