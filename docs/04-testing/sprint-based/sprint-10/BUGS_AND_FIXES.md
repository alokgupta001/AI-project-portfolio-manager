# Sprint 10 bugs, corrections and remaining limits

## Current evidence and documentation status — 16 October 2026

The original 15 October disabled-provider checkpoint below is retained history.
The user later authorized Gemini free tier at $0; bounded real completion and
256-dimension embedding smoke passed, and daily confirmation expiry was removed.
The final expiry-removal regression recorded 63 AI/provider passes. See
[follow-up results](GEMINI-FOLLOWUP.md) and the
[current cross-sprint documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).
The missing-key authorization blocker is resolved. General model/retrieval
quality, scale, hosted CI, archived Word visual QA and production/release gates
remain unverified. Stop before 11; this audit adds no application/provider work.

## Historical 15 October record

- First broad run: missing D import in the held-source fixture after an auto-fix
  had removed a previously unused import. 149 tests passed; failed run retained.
  Restore the explicit document_tables import and rerun the affected/full gates.
- Static integration review: adding prompt/schema/tool provenance required json;
  restored import before acceptance and discarded the interim candidate test run.
- Request-budget review: raw text length alone did not bound serialized Unicode/
  escaped JSON. Enforce the final request-byte ceiling and reserve additional input
  token headroom. No real provider request occurred.
- Source/keyword API still advertised pending_sprint_10 after adding the runtime.
  It now advertises budgeted_ai_runtime, while GET search stays keyword-only and
  performs no provider calls. Updated the existing source compatibility assertion.

Current limits: real provider BLOCKED; exact JSONB vectors bounded to 200 candidates,
20 chunks/index; no semantic agents, invoice reconciliation, production deployment,
full accessibility certification, hosted CI or archived Word visual acceptance.
Later final browser/regression corrections are recorded here with evidence.

## Browser fixture and responsive corrections

The initial AI browser fixture raced organization switching and captured cookies
before rotation completed (401); awaiting auth/switch resolved it. The next run
correctly returned 409 because the new isolated organization lacked timezone/currency;
initialize settings before creating its project. These were test setup defects;
failed logs sprint10-browser-initial.txt and sprint10-browser-second.txt are retained.
The corrected focused journey passed in 38.4 seconds.

Visual review found mobile diagnostic headings compressed into vertical text despite
passing overflow/axe checks. The accounting region now scrolls a 640px minimum-width
table, panels have consistent spacing, and refreshed source choices reload. The full
browser run records the corrected screenshots; this is a product layout correction.
