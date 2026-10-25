# ADR 018 — Limited guided review with closed-choice API assistance

Status: accepted for local implementation, 24 October 2026; scope updated
25 October 2026. Persistent external activation is approved for the synthetic demo
and Customer Onboarding Portal's bounded observations. One synthetic request per
provider succeeded; business-project route/access checks used no inference.
Schema 0016 supplies scoped guided grants without changing business roles. Shared
ceilings are 50/day per provider account and tenant, one/minute, one concurrent;
usage history is preserved. See [current access](../../limitations/USER_ACCESS.md)
and [quota evidence](../../limitations/QUOTA_REVIEW.md).

Supplements ADR 017 and the Sprint 11.1 runtime without changing broad semantic
acceptance. The [local-sample plan](../../09-planning/LOCAL_SAMPLE_PLAN_UPDATE.md)
allows Sprint 12 foundations to proceed; AT17 remains blocked.

The existing Gemini/Puter/Groq accounts have not passed general reasoning
acceptance, and the local machine cannot run the intended Ollama models alongside
the application. The owner authorized a limited working implementation with no
additional providers or paid capacity.

Use Python for canonical calculations, evidence projection and displayed facts/
actions. Allow an optional model to select at most two IDs from eight observations
for one requested role. Admit one 128-token call through the existing scoped quota,
credential, egress and $0 controls. No retries or free-form generated advice.

`analysis_mode=guided` requires exactly one role and produces all nine baseline
paths plus one optional `guided_selection` task. This distinct task requires both
the global and profile guided flags and the role's fixed provider assignment.
It does not populate or bypass broad task qualification. Public responses add an
optional `guided_review` result with status, provider, code, cards and checklists;
agent definitions expose `guided_enabled`. Generated OpenAPI/TypeScript agree.

Keep manual checklists usable when evidence, quota or API output is unavailable.
Validate choice IDs and source authority before display; withdraw stale selections.
The model's selection usefulness remains unmeasured. It cannot certify compliance,
predict outcomes, alter scores or approve actions. All original product obligations
remain in the [limitations register](../../limitations/LIMITS_AND_FUTURE_SOLUTIONS.md).

Alternatives considered: larger unrestricted output budgets do not fix reasoning
quality; fine-tuning lacks a verified free supported path; local inference lacks
RAM and quality evidence. A fully deterministic checklist is the supported fallback
and may remain the better choice if API ranking adds no measurable value.

See [implementation and tests](../../limitations/IMPLEMENTATION_REPORT.md),
[review findings](../../limitations/REVIEW_AND_SOLUTION.md) and the
[exact approved API scope](../../limitations/API_DATA_SCOPE.md).
