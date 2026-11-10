# Financial selection pilot contract v1

Current implementation: [selection feature](../../services/api/ppm_api/modules/selection/README.md).
The [step 28 grouping](../04-testing/BACKEND_STRUCTURE_STEP_28.md) changes
file/import ownership while preserving the contract and permission/workflow rules below.

Ordinary guided cloud reviews gained a separately approved maximum of 60 seconds
on 30 October 2026. **This does not change fixture binding, its 22-second limit,
the 20-second gate, or stopped-case behavior.** See [ordinary guided policy](agents.md).

## Sprint 12.1 timing repair (28 October 2026)

New bindings include `measurement_version=attempt-elapsed-v2` and effective
`timeout_seconds` (still capped at 22). Model, prompt, corpus, labels, 128-token
cap and the 20-second fixture gate are unchanged. Earlier rows and receipts remain
immutable; the current UI can show `binding_changed` for historical bindings.

Case views/downloads add nullable `elapsed_ms` and `timing_kind`:

- `accepted_response`: accepted response latency, included in p95.
- `unavailable_attempt`: unsuccessful attempt elapsed time, excluded from p95
  and match counts. Unknown usage remains unknown.
- `not_recorded`: no timing evidence, including legacy failed attempts with a
  stored zero. UI says “Elapsed time not recorded”; it does not infer zero latency.

Existing `latency_ms` remains for compatibility. New failures without a ModelResult
retain monotonic elapsed time before settlement; returned responses keep adapter
latency. Cancellation still settles unknown and propagates. No migration or ledger
rewrite is involved.

Safe `model_attempt_timing` worker events contain only attempt UUID, fixed event
name/version, outcome code, elapsed milliseconds and allowlisted HTTP milestone
offsets. Trace info, headers, bodies and exception text are discarded. Success logs
use INFO, failures WARNING. These are client-side milestones, not provider-internal
measurements. No retry or request optimization was introduced. See the
[repair follow-up](../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md).

Owning sub-sprint: [Sprint 12.1](../03-sprints/active/sprint-12.1/README.md).
The owner approved four demo-only guided grants to satisfy the existing gate;
no authorization check was removed. The owner subsequently authorized an
[automated fixture-audit exception](../09-planning/sprint-12.1/AUTOMATED_AUDIT_PROPOSAL.md)
for saved pilot ce874a14 only. Other pilots retain the personal human review path.

Authority: `selection_pilot.py`, `selection_protocol.py`, `selection_tables.py` and
generated OpenAPI. UI uses generated types in `selection-pilot.tsx`. This is an
additive guided experiment, separate from semantic interpretation and ML training.

| Endpoint under `/api/v1/agents/selection-pilots` | Behavior |
| --- | --- |
| `GET ?project_id=…` | Up to ten recent pilots for an authorized project; scores rebuilt from saved calls/sections. |
| `POST` | Body `{project_id}`; idempotency key maps to one pilot/actor/tenant. Same key with another project conflicts. No inference. |
| `GET /{id}` | Live project, role, grant and tenant checks; returns protocol, case results, review and limitation states. No inference. |
| `POST /{id}/label-review` | Twelve distinct reviewed case IDs, corpus/strategy hashes, human attestation and reason. Requires a different Admin with a guided grant and current `If-Match`; immutable in the API. Identical review replay by its actor returns the saved result. |
| `POST /{id}/automated-review` | Corpus/strategy hashes and `synthetic_only=true`, current `If-Match`, unchanged binding and no prior attempts. Requires local environment plus an operator allowlist containing this one pilot ID. Audits the pinned original corpus using exact Fraction arithmetic, independently of Decimal label generation. Records immutable `kind=automated_rule_audit`, executing actor, method/checks/hash and `human_reviewed=false`; identical replay returns the saved audit. |
| `POST /{id}/cases/{case}` | Current `If-Match`, frozen binding/review and strict protocol order. One existing durable AI run per case. Duplicate case requests return that run. Active/unavailable cases block later cases; early pacing returns 429 before queueing. |

All endpoints require current Admin and the caller's existing explicit guided
project grant. RLS additionally requires the active organization and Admin role.
CSRF/Origin/session controls are inherited. Mutations serialize using the existing
organization authority lock; case starts also lock the pilot row. No endpoint grants
provider scope or alters policy. Pilot creation/review is audited. Role demotion,
membership/grant revocation and private source controls remain live.

Optional `guided_pilot_id` / `guided_case_id` fields extend hybrid selection DTOs.
They require guided financial mode with no assessment, documents or prior run.
Generic AI/agent creation rejects these fields: only the pilot case endpoint may
queue them. Legacy query/index, v1 and ordinary v2 request fingerprints exclude the
new empty fields to retain idempotency. Synthetic runs have a `synthetic_fixture`
lineage label in their guided results and contain no real project metric snapshot.

Normal guided prompt/context hashes remain unchanged. A pilot uses its own
versioned prompt and immutable numeric fixtures. Workers recheck the pilot's
project, current reviewer authority, corpus and strategy through current source
resolution. Existing routing, NativeAdapter validation, 128-token output cap,
SQL quota admission/settlement, worker lease/cancel checks and source revalidation
own execution. Gemini remains assigned; no alias or new account scope is added.

`PPM_AI_FIXTURE_AUTOMATED_PILOTS` defaults to `[]` and permits at most one UUID.
It is effective only with `PPM_APP_ENV=local`. It grants no project or provider
access. Both API and worker must receive the same explicitly approved value.
Automated audits accept only the original pinned CC0 numeric corpus and strategy;
changed facts, labels, splits, hashes or lineage fail closed. Removing the
allowlist blocks new cases and worker execution of queued automated cases.
The audit actor must retain active Admin membership and an explicit guided grant.
Human approval remains a separate immutable kind with its distinct-person gate.

Views/downloads include `review_kind`, `human_reviewed`, `can_automated_review`,
and summary fields `label_review_kind` / `independent_human_review`. A machine
audit cannot set human provenance. The UI exposes the automated button only when
the API returns eligibility. No automated audit result is model accuracy evidence;
actual provider case calls are measured separately.

`ai_selection_pilots` stores organization/project/creator, versioned binding (including
the frozen protocol), typed review provenance, case-to-run links, creation time and revision.
Forward migration 0019 adds it without changing established tables, SQL admission
functions, usage ledgers or grants. Downgrade is only exercised on disposable tests.
The automated kind uses that existing JSON review column; applied 0019 is unchanged.
There is no model promotion/activation write. Reports always return `at17=BLOCKED`,
no semantic-qualified classes and zero added interpretations. Synthetic exact-match
results are not genuine outcome labels or training data.

See [user guide and state definitions](../limitations/FINANCIAL_SELECTION_PILOT.md)
and [ADR 020](../architecture/adr/020-financial-selection-pilot.md).
