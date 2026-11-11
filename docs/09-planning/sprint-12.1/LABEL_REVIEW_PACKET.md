# Sprint 12.1 — Frozen twelve-case label-review packet

26 October 2026. **Frozen synthetic labels; automated arithmetic audit 12/12 recorded, personal human approval absent.**
The owner requested this packet and pilot preparation. That request is not a
personal attestation that every label has been reviewed. No model call is made
by generating or reading this packet.

## Protocol binding

- Version: `financial-selection-fixtures-v1`.
- Corpus SHA-256: `537f42bb85456da4e298ef97d3cf9cc46584f3f20b9509a157f83c4e69e7322a`.
- Strategy SHA-256: `71c321aa1579a5e71c90eaa14a0b9c440c8f6837a9cd8fa8c5d29925bd8de4e0`.
- Origin: original in-repository numeric fixtures; CC0-1.0; synthetic lineage.
- Requested provider/model: `gemini` / `gemini-3.5-flash-lite`.
- Policy SHA-256: `4c4983040b04912898dc031519aba6533602e2706fb32cbe1b32f885ab9838b5`.
- Actual saved pilot ID: `ce874a14-bbd0-50c5-b9b6-f7909a8bda8a`; creator Ashu; automated audit recorded, human=false; live run stopped with insufficient_data.

## Rule and labels

Select every usage observation at least 100%, or marked partial; otherwise abstain.

A partial measure is selected even when its numeric value is below 100%.
A complete measure below 100% is not selected. Exactly 100% is selected.
Return every matching ID (at most two), with no prose. If none matches, return
an empty choices list. Order of the selected IDs does not affect correctness.

| Case | Split | Exact fixture observations | Expected choices |
| --- | --- | --- | --- |
| f01 | calibration | o1: Recorded usage: 112.50 %. | `["o1"]` |
| f02 | calibration | o1: Recorded usage: 42.00 %. | `[]` |
| f03 | calibration | o1: Recorded usage: 32.00 %. Incomplete inputs; this is a partial measure. | `["o1"]` |
| f04 | calibration | o1: Recorded usage: 99.99 %.<br>o2: Recorded usage: 100.00 %. | `["o2"]` |
| f05 | calibration | o1: Recorded usage: 120.00 %.<br>o2: Recorded usage: 130.00 %. | `["o1","o2"]` |
| f06 | calibration | o1: Recorded usage: 0.00 %.<br>o2: Recorded usage: 99.00 %. | `[]` |
| f07 | held_out | o1: Recorded usage: 100.01 %. | `["o1"]` |
| f08 | held_out | o1: Recorded usage: 80.00 %. | `[]` |
| f09 | held_out | o1: Recorded usage: 0.00 %. Incomplete inputs; this is a partial measure. | `["o1"]` |
| f10 | held_out | o1: Recorded usage: 100.00 %.<br>o2: Recorded usage: 25.00 %. | `["o1"]` |
| f11 | held_out | o1: Recorded usage: 72.50 %. Incomplete inputs; this is a partial measure.<br>o2: Recorded usage: 105.75 %. | `["o1","o2"]` |
| f12 | held_out | o1: Recorded usage: 0.00 %.<br>o2: Recorded usage: 99.98 %. | `[]` |

## Approved automated provenance for this saved pilot

The owner separately approved the [one-pilot automated exception](AUTOMATED_AUDIT_PROPOSAL.md).
The app recorded the exact Fraction audit and human_reviewed=false before inference.
The corpus and strategy below were not changed. [Actual run](../../03-sprints/active/sprint-12.1/RUN_RECORD.md).
The following is the separate personal-review path for other pilots.

## What a human reviewer records on the personal-review path

Compare every expected list with the rule and source values. Check both sets;
the six reserved cases may be reviewed for labeling but must not be used to tune
the prompt. Record the exact corpus/strategy hashes, every reviewed case ID,
your own authorized account, timestamp and a reason through **Freeze reviewed
labels**. Reject an incorrect/ambiguous label by leaving it unapproved and asking
for a newly versioned protocol. Do not edit this frozen strategy during measurement.

The grant/access decision is separate. The reviewer must differ from the pilot
creator and must personally approve the labels; the assistant cannot manufacture
that approval. See [access proposal](ACCESS_PROPOSAL.md).

## Interpretation of later results

All 12 exact matches and p95 latency no greater than 20 seconds pass only this
small synthetic selection gate. Unknown/failed attempts are retained, fallback
cards are not API success, and no automatic retry is allowed. Report actual
counts/denominators and abstentions. These are not genuine outcomes or training
labels, and they do not demonstrate non-template interpretation or real-world
accuracy. **AT17 stays BLOCKED.**

[Sprint plan](README.md) · [User guide](../../limitations/FINANCIAL_SELECTION_PILOT.md) ·
[Technical report](../../03-sprints/active/sprint-12.1/SPRINT_REPORT.md).
