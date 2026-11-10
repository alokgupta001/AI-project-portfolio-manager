# Sprint 12.1 ordinary guided-review timeout proposal

29 October 2026. Owner requested “fix the timeout” after the repair experiment
stopped at f06. This document records the inspected constraint and the exact
proposed scope; it does not claim implementation or a successful provider call.

## Verified constraint

The failed attempt lasted 22,037 ms. `agent_runtime.complete_task` applies
`ai_local_completion_timeout_seconds` (maximum 22) to cloud requests too.
`NativeAdapter.permit` independently rejects longer requests, and
`NativeAdapter.execute` enforces the total with `asyncio.timeout`.
The database admission function `ppm_model_admit` also requires 1–22 seconds.
Thus changing one HTTP timeout would not safely implement a longer wait.

This identifies the cancellation boundary, not the reason Gemini did not finish
within it. The missing f06 phase events prevent attributing the delay to network,
provider compute or local contention. No speculative request optimization is justified.

## Approved change

The owner selected **“Allow up to 60 seconds for ordinary guided reviews.”**
Implementation and actual evidence are in the
[timeout follow-up](../../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md).

Allow **ordinary cloud guided reviews only** to wait up to 60 seconds, with a
separate bounded setting and the effective value frozen in each new run's versions.
Retain the 90-second total run deadline, five-second settlement margin, ten-second
lease heartbeat, one generation slot, one request per minute, shared 50/day/provider
ceiling, one optional guided request, unknown-outcome accounting and $0 policy.
Admission must deny a call when insufficient run time remains. Cancellation and
revoked access must still prevent result publication and settle usage honestly.

Keep local Ollama and other analysis modes at their existing limits. Fixture pilots
keep their frozen 22-second deadline, unchanged labels/prompts and 20-second gate.
Both stopped pilots remain stopped. No automatic retry, fallback provider, new
experiment, grant expansion or reset accompanies this setting.

Implementation would touch settings, run provenance, timeout selection and adapter
validation, plus one **forward** migration that permits longer admission only for
an ordinary guided cloud run with the recorded bounded policy. Applied 0001–0019
must remain unchanged. Regression checks must cover the SQL bound, a delayed mocked
response, over-bound timeout, quota slot lifetime, cancellation/revocation and
unchanged fixture binding/stop behavior. UI help must distinguish waiting longer
from achieving a faster or qualifying response.

Longer waits can accept a response arriving between 22 and 60 seconds; they cannot
guarantee provider availability or satisfy the pilot's 20-second gate. Broad AT17
remains BLOCKED. No new live experiment is included in this proposal.

## Inspection checkpoint before approval (historical)

No deadline, schema, application code or provider policy was changed by this
follow-up inspection. A starting binary diff and copies/hashes of 222 changed or
untracked files were captured under ignored
`artifacts/local/sprint12_1/timeout-followup/`. Previous repair evidence remains
available in the [repair report](../../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md).
