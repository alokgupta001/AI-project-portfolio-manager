# Independent cloud acceptance review

Current follow-up: 23 October 2026. The user asked the implementation agent to
arrange the review instead of nominating a person. A separate CodeRabbit label
audit was requested on [PR #5](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/5#issuecomment-6353350329).
Its findings will be recorded as AI
review; they are not human approval or model accuracy measurements. No label or
model has been approved. The [current request](review-closeout/review-request.json)
binds the updated strategy; older packet strategy hashes remain historical.

1. Review [fresh labels and inputs](reviewer-packet/labels.json) first. There are
   108 original synthetic cases, twelve per role, with 54 held out. Correct ambiguous
   expected claims, missing-evidence decisions and rubric levels in the source
   [cloud corpus](../../../tests/fixtures/agent_v2_cloud_quality.json) before freezing
   approval. These are author drafts, not established ground truth. They contain no
   real tenant/personnel information or copied external dataset rows.
2. Record your identity, independent review ID and approval time in a copy of the
   [label approval template](reviewer-packet/label-approval-template.json). Independence
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
