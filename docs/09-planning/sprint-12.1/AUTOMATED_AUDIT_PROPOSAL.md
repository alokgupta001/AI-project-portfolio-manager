# Sprint 12.1 — Optional automated check for this synthetic pilot

26 October 2026. **Approved by the owner's “ok then do it” after discussing
automated quality checks.** The scoped local implementation and validation are
recorded in the [run record](../../03-sprints/active/sprint-12.1/RUN_RECORD.md).
The owner asked whether the assistant can handle the review. An exact-arithmetic consistency check has
verified all twelve draft labels; [receipt](../../verification/sprint12_1/automated-label-check.json).
This is an automated check, not another person's personal review.

## Exact approved scope

- Only saved pilot `ce874a14-bbd0-50c5-b9b6-f7909a8bda8a`.
- Only the frozen, original CC0 synthetic numeric corpus/strategy in its
  [packet](LABEL_REVIEW_PACKET.md); no imported or genuine outcome data.
- Add a clearly marked local automated-rule-audit review path. Record
  `human_reviewed=false`, its method/hash/case checks and the executing account;
  never impersonate Alok, Blaze or Hement or write a personal attestation for them.
- An operator-controlled local allowlist defaults empty and enables this path
  only for that pilot after explicit owner approval. Keep the existing human
  review path and its distinct-person requirement unchanged.
- Preserve Admin/project/explicit-grant checks, provider egress and shared SQL
  admission. No additional account, role, provider, key, quota or data scope.
- After the automated check is recorded, execute at most the twelve original
  cases through the ordinary jobs, at one/minute within 50/day/provider and $0.
  Retain every attempt and stop on an unavailable/unknown result; no retry/reset.
- Reports and UI explicitly distinguish **automated fixture checking** from
  **independent human approval**. The small fixture gate and latency threshold
  remain unchanged. Broad AT17 stays BLOCKED, with no qualification/promotion,
  training-label claim or Sprint 13 serving.

This is an explicit synthetic-only exception. It does not claim that permission
makes an AI a human reviewer. The distinct-person path remains available and
required for other pilots. The automated record and real provider measurements
are separate evidence, with exact status in the linked run record.
