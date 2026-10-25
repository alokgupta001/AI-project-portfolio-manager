# Current implementation review and limited solution

Reviewer: the coding assistant in this conversation. This is an engineering review,
not independent human sign-off. Scope: source routing, native adapters, durable
admission/checkpoints, evidence revalidation, result assembly, the Agents UI,
local deployment state and the retained Sprint 11.1 evaluation evidence.

## Findings verified against the current implementation

| Finding | Effect | Resolution |
| --- | --- | --- |
| The normal database was still at 0012 while the v2 source required 0015; normal services were stopped at the start of this review | Passing source tests did not give the user a runnable v2 application | Back up data/objects, validate additive migrations, start the updated local application and check its actual UI |
| `model_router.eligibility` requires qualified task classes and all supplied profiles were unqualified | Broad interpretation correctly stayed blocked, but there was no useful API-assisted mode the user could try | Add an independently enabled `guided_selection` task with a closed response schema; retain the original semantic qualification checks |
| Retained model output audit rejected absence handling, privacy interpretation, weak reasoning and contradictory metadata | Schema-valid text was not reliable business reasoning | Do not publish new model claims in guided mode; models select observation IDs only |
| Nine-role batches share 512 output tokens and a four-attempt/90-second budget | Large requests can truncate or defer roles; three shared accounts do not provide nine independent quotas | One requested assisted role per run, eight observations maximum, one call, two selections and 128 output tokens |
| UI emphasized unrestricted specialist modes even though providers could not qualify | The user could request unavailable functionality without a practical alternative | Default to guided review when enabled; show rules-only fallback, all nine checklists, explicit errors and existing canonical coverage |
| Project-wide status documents retained older checkpoints | It was difficult to distinguish a merged implementation from deployed behavior and accepted quality | Add this limitations folder and a current handoff with exact verification and deployment scope |

## Limited-mode behavior

1. Authenticate the existing Admin and capture an authorized snapshot through the
   current metric, privacy, document and assessment services.
2. Compute the nine existing deterministic baseline paths. Keep unknown and partial
   measures explicit; do not manufacture a prediction from a heuristic risk score.
3. For one selected role, construct at most eight small observations from allowed
   structured fields. PMO/executive assistance is limited to the selected project.
   Raw documents, assessment answers, names and personal notes never enter this prompt.
4. Admit one request through the existing account-wide database quotas, lease,
   cancellation, policy-hash, credential, free-account and egress checks.
5. The provider returns at most two existing IDs. Reject extra fields, unknown IDs,
   duplicates, truncation or malformed output. No automatic repair/retry is used.
6. Resolve the IDs to exact application-generated facts and predefined manual review
   actions. Store the checkpoint and recheck source hashes/access whenever it is read.
7. On failure or missing evidence, keep the deterministic checklist available and
   report why API assistance was unavailable. No plan, score or approval is changed.

Provider assignments: Gemini handles financial/schedule/resource; Puter handles
risk/governance/agile coaching; Groq handles team support/PMO/executive. This is
nine role-specific workflows sharing three accounts, not nine separate trained models.

The new policy permission authorizes only `guided_selection`. Setting it does not
populate `qualified_task_classes`, authorize general prompts or make the old AT17
evaluation pass. The adapter verifies the fixed prompt/schema and the role's provider.
The trusted application owns claims and advice; model ranking usefulness remains
unmeasured and the full checklist remains available for human choice.

## Verification and release boundary

The full backend suite passed 509 tests with one skip, including five real-database
guided workflows with synthetic transport. Two browser journeys passed, including
saved results, nine checklists, three viewport sizes and axe checks. Normal local
demo runs completed through authentication, durable jobs and persisted results.
Final regression/browser/live receipts are recorded in the latest handoff and
this folder's usage guide. Do not interpret synthetic tests
as proof that a particular provider account currently responds.

No training dataset was uploaded, model weights changed, held-out evaluation labels
edited or paid capacity added. The earlier rejected results remain evidence for
the broader product's unresolved accuracy gate.
