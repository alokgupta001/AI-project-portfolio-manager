# Sprint 06 assessment contract

The API prefix is `/api/v1/assessment`; the UI is `/assessments`. OpenAPI is authoritative. All writes use the existing cookie/CSRF/active-organization transport, a UUID `Idempotency-Key`, and (when editing an existing aggregate) `If-Match`. Conflicts return 412, missing preconditions 428, reused keys with different requests 409. An organization transaction lock rechecks live membership before authorization or replay. Requests are capped at 2 MiB before JSON parsing.

## Frameworks and ownership

Admins create frameworks and publish immutable versions. An Admin may grant an active Project Manager draft editing for a particular framework through `/access`. Publication remains Admin-only. A draft is a typed JSON definition containing stable dimension/question UUIDs, positive question weights, answer types and rubric levels. Dimension weights must sum exactly to 1; every published dimension requires a numeric question; rubric levels must contain at least two distinct integers. Text questions are unscored but can be required. Only listed rubric values are valid answers. Four explicitly labelled product examples can be loaded idempotently. Saving draft edits never changes published definitions or assigned assessments.

Published definitions and assessment events are append-only for the application database role. Sprint 06 uses one frozen migration, `0005_assessment`; it supersedes the unaccepted working-tree implementation, not a previously deployed supported API. Existing Sprint 01–05 migrations and consumers are unchanged. Normal local data was still at 0004 when repair began. Disposable earlier 0005 test schemas are removed only by the guarded test lifecycle.

## Workflow and permissions

An Admin assigns a version to the organization, department or team and names different active Admin/PM members as respondent and reviewer. A supplied department/team pair must agree. This named responsibility is the explicit assessment scope; it grants no project/capacity access. Only the respondent can save answers, attach evidence and submit. Only the named independent reviewer can start review, return or complete. Admin status does not bypass either role. Viewers cannot answer or review. Admins can explicitly grant completed-result reads to active members; this exposes the saved result and framework, never private answers, event details or attachments.

Draft/returned autosaves replace only the supplied question answers, validate against the frozen version and advance the assessment revision. Answer changes clear that answer's reviewer override. Submission requires every required answer and a computable score in every dimension. Submitted → in_review → completed or returned; direct submitted → completed/returned is also permitted. Reviewer adjustments require numeric answers in that exact assessment and a reason, with immutable before/after events. Completion repeats validation and refuses quarantined evidence. Completed results/answers are immutable via API and protected by app-role database policies. Replays repeat the original response only after live access checks.

## Scores and comparisons

Rule version: `assessment-v1` (frozen framework version plus recorded result). Rubric normalization uses Decimal `(value-min)/(max-min)`, booleans 0/1. M11 is `100 × sum(answer_weight × normalized_score) / sum(valid_numeric_answer_weights)`. M12 is the sum of dimension weight times dimension score, with no final renormalization. All-missing numeric dimensions produce unknown, not zero. Scores are provisional until review completes. Answer coverage is valid-answer weight divided by all question weight, including required text completeness; evidence coverage is the fraction of questions with nonempty evidence notes or released attachments. These are distinct labels, bounded 0–100. Unreleased files do not count as evidence. Optional missing answers are explicitly reflected in coverage.

The UI compares only completed departmental assessments with the identical framework-version UUID among the latest 100 authorized loaded records. It discloses that limit and excludes incompatible versions. A score chart includes an equivalent labelled table. Stored approved results are not recalculated when the draft or a later version changes.

Worked acceptance: Engineering has two questions, weights 1 and 3. Rubric level 1 of 0–2 contributes 0.5; boolean true contributes 1. `(1×0.5+3×1)/4×100=87.5`. Reviewer changes the first answer to 0 with a reason, producing 75. Operations answers 0/false and scores 0. Same version, different answers and documented adjustment explain the difference. With only the first answer, the provisional score is 50 and weight coverage is 25%; finalization is refused.

## Evidence and retention

Current intake deliberately accepts only UTF-8 `.txt` files, 1 byte–512 KiB, at most 50 per assessment. Paths are server-generated tenant/assessment/UUID keys in the existing ObjectStore. Names, base64, control characters and active-markup/test-malware signatures are checked; SHA-256 is verified on preview/download. No PDF/Office parsing or AI ingestion is enabled. All uploads are quarantined. Authorized respondents/reviewers/Admins may see an escaped plain-text JSON preview; raw download is unavailable until the independent assigned reviewer records an explicit release reason during review. Release is human attestation, not a claim of automated antivirus scanning. Downloads require current authorization and use attachment/nosniff headers. Never interpret evidence as instructions.

Respondents may remove attachment metadata only from draft/returned assessments. Submitted/completed evidence remains retained for the assessment history. Removed or rolled-back object bytes are inaccessible orphan objects retained for recovery; automatic physical purge and production retention policy are not configured. Do not claim regulatory retention compliance. Private details remain excluded from result-only grants and cross-tenant reads.

## Verification

`tests/test_assessment.py` covers scoring, missing/invalid data, two departments, immutable versions, review/return, adjustments, wrong-assessment attacks, Viewer denial, delegated editing, result-only access, CSRF, tenant/RLS, immutable SQL records, revision conflicts and replay. `tests/browser/assessment.spec.ts` exercises the real UI and escaped evidence flow on isolated fixtures, with 1440/768/360px screenshots and automated accessibility checks. See Sprint 06 checks for actual final command results and limitations.
