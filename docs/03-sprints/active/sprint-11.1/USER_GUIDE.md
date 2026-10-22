# Using the hybrid analysis controls

**Current deployment note:** Ollama is stopped. The requested
[Groq/Gemini/Puter role split](CLOUD_SPECIALISTS.md) has synthetic calibration
results, but is not enabled in the normal application. The latest repair trials
retain three Groq failures and 42 role results passing hard checks. These small
calibration samples do not establish accuracy. Independent accuracy/egress/rollout
gates remain open. The 36 authored
examples improve prompts; no cloud model weights were trained. Existing limits
still defer work that cannot fit four attempts per run. Earlier native-chat commands
are retained setup history, not the selected current path.

These controls are implemented in source and verified in the isolated browser stack. The normal application has not been upgraded or enabled for v2. An operator must complete schema/configuration and model qualification before activation. Existing independent review behavior remains available in the current application.

1. Open **Agents & recommendations** as an Admin and choose an analysis project. Select up to five ready document versions and an optional permitted assessment.
2. Choose **Metrics only** for canonical checks with no model calls. Choose **Selected specialist interpretation** and check roles for a focused AI request. Selection order sets priority. Assessment mode needs an assessment; portfolio/executive mode reserves the relevant synthesis role.
3. Choose **All nine specialists** for the explicit full-role plan: Gemini handles financial/schedule/resource, Puter handles risk/governance/agile coaching, and Groq handles team support/PMO followed by executive synthesis. This uses four bounded batch calls. Selected-role modes allow up to three initial sections and a fourth shared repair/critique attempt. Every mode retains the four-attempt run limit; a failure, quota or deadline can leave partial coverage. Narrowing scope does not grant additional provider authority.
4. Read **Baseline and AI coverage** separately. A baseline result never means requested AI reasoning completed. Unknown data is not zero; no findings is not a clean bill of health. Missing/failed/deferred interpretations and material conflicts remain visible. Model usage is unknown when the provider did not report it.
5. Open a candidate's evidence and record a reason through an independent authorized reviewer. Acceptance records review only; it does not edit project plans, approve changes or replace the original maturity score. Revoked/changed evidence cannot support acceptance.

If no qualified profile is available, useful canonical results remain with explicit unavailable AI status. A semantic-only run with no useful surviving result fails. Real-model quality remains **UNVERIFIED/BLOCKED** until measured per task class. Team support uses only the permitted aggregate summary; individual/emotional diagnosis is outside scope.

The separate [small Ollama native-chat preset](OLLAMA_SMALL.md) is now installed for
experimental use. Its launcher checks initial RAM, requests thinking off and unloads
after each response. It is not an enabled project specialist: actual project-format
tests failed and remain rejected. Native chat does not change scores, recommendations
or independent review in this application.
