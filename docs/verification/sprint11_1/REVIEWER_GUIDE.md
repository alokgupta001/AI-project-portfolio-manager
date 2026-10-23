# Independent cloud acceptance review

**Final disposition:** the [output sample audit failed](review-closeout/output-audit-rejected.json).
The bounded sequence stopped at 20 new calibration calls/42 role outputs, with no
evaluated-provider held-out calls and no qualification. The label-content pass
below binds measured strategy `f9c761cd`; subsequent predicate/cleanup guards
change the current strategy to `f5616c25`. Use the [fresh empty current template](review-closeout/label-approval-template-current.json)
only after deliberate review of that binding. Existing approvals and measurements
remain historical; they cannot authorize inference or qualify the revised strategy.

**Current:** CodeRabbit's [labels-only re-audit passed](review-closeout/label-audit-pass.json)
all 108 revised cases/54 held out, with both hashes verified. The actual
[AI approval record](review-closeout/ai-label-approval.json) is frozen before
inference; it is not human approval or a provider-accuracy verdict. The bounded
measurement sequence is running with unchanged prompts. Independent output
ratings and measured qualification are still required. Earlier packet labels are
historical; use the current source corpus and fresh export for output review.

Current follow-up: 23 October 2026. The user asked us to arrange the review.
CodeRabbit independently audited all 108 labels and [declined approval](review-closeout/label-audit-round-1.json):
18 ambiguous cases, duplicated governance evidence across splits, and a CRLF/LF
fingerprint mismatch. Those drafts are corrected and immutable exports now use LF.
A fresh independent audit must bind the [current request](review-closeout/review-request.json).
This is AI review, not human approval or model accuracy measurement. No label or
model has been approved; older exported labels and strategy hashes are historical.

1. Review [current labels and inputs](../../../tests/fixtures/agent_v2_cloud_quality.json) first. There are
   108 original synthetic cases, twelve per role, with 54 held out. Correct ambiguous
   expected claims, missing-evidence decisions and rubric levels in the source
   [cloud corpus](../../../tests/fixtures/agent_v2_cloud_quality.json) before freezing
   approval. These are author drafts, not established ground truth. They contain no
   real tenant/personnel information or copied external dataset rows.
2. Record your identity, independent review ID and approval time in a copy of the
   [current label approval template](review-closeout/label-approval-template-current.json). Independence
   means that the reviewer did not author the labels. Approval must bind the final
   corpus and strategy hashes and precede held-out inference. A changed corpus or
   strategy requires deliberate review; the runner will reject stale bindings.
   If labels change, the operator must export a new packet directory with
   `scripts/prepare_cloud_review.py --output artifacts/local/cloud-review-revised`
   and use its new approval template. Existing exports are never overwritten.
3. After label review, inspect the separate [historical calibration candidates](reviewer-packet/candidates.json)
   against their [original inputs](reviewer-packet/calibration-inputs.json). The
   eighteen requests include three retained Groq failures and 42 role results passing
   hard checks. Different prompt revisions and these small samples cannot establish
   acceptance or determine which provider has the highest accuracy.
4. After approved labels and bounded acceptance measurements exist, use one copy of
   the [output review template](reviewer-packet/review-template.json) per provider.
   Bind report and candidate hashes. Judge evidence support, added interpretation,
   advice relevance, omissions, abstention, citations, canonical values and privacy.
   A real citation or agreement with another model does not establish correctness.

No held-out request has been sent. Existing calibration attempts, exhausted roots
and failures remain immutable history. The fresh scenarios are a separate acceptance
draft, not renamed retries of those failures or new training examples.

The operator workflow is in [the batch repair report](CLOUD_BATCH_REPAIR.md). No key,
account identifier or private provider error body belongs in the review files.
Reviewer nomination does not authorize sending these files to another person.
