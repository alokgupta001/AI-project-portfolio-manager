# Implementation tracker and planning checkpoint

**Current disposition — 25 October 2026:** Sprint 11/11.1 is complete for the
local guided-sample scope; Sprint 12 local foundations are ready to start, not yet
implemented. Broad AI accuracy **AT17 remains BLOCKED**. Normal schema is 0016;
Gemini/Puter/Groq guided access covers the two approved projects with shared
50/day provider ceilings. See [the closeout](../../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md) and
[reconciled plan](../LOCAL_SAMPLE_PLAN_UPDATE.md) for evidence, current scope and the Sprint 12 prompt.
This supersedes older runtime/rollout/stop statements below; dated test results
and original full-product acceptance requirements remain unchanged.

**Current repair, 22 October:** [four-call batching and cloud acceptance](../../verification/sprint11_1/CLOUD_BATCH_REPAIR.md)
and [reviewer packet](../../verification/sprint11_1/REVIEWER_GUIDE.md). T06–T10 now
include an explicit all-nine mode with the same limits; three DB batch/budget/resume
cases pass. T12's cloud-specific scorer/runner and fresh 108-case draft are implemented.
T12/AT17 semantic acceptance remains BLOCKED pending the nominated independent reviewer
and actual held-out measurements. The eighteen-call repair allocation is consumed;
old failures/root/account counters remain. No qualification, weight training or rollout.
Final verification: 475 full backend/lifecycle tests, 48 final focused cloud checks
(overlap), three batch DB cases and one responsive/accessibility browser journey pass.
72 source fingerprints and all 70 normal table/five object/24 frozen-file preservation
checks pass. Normal remains 0012; seven profiles off, Ollama stopped. T12/AT17 stays
BLOCKED by independent acceptance, not a passing-format claim.
The earlier current-cloud paragraph below is the previous checkpoint.

**Current cloud follow-up:** [three-provider guide](../../03-sprints/active/sprint-11.1/CLOUD_SPECIALISTS.md)
and [results](../../verification/sprint11_1/CLOUD_CALIBRATION_RESULTS.md). T13's native
Puter/cloud calibration slice is now IMPLEMENTED and bounded synthetically tested;
activation remains BLOCKED with T12/AT17 independent model acceptance. Ollama stopped.
26 calls, all nine supported role formats passing, seven/nine absence cases passing.
36 draft training examples; no weight training. Final 198 offline/101 DB-provider/37
prompt-fence scopes pass (overlap). Full-run fixture failures/corrections and normal
refresh-token preservation exception are explicitly retained in the current handoff.
No previous checkpoint's VERIFIED status establishes semantic accuracy or rollout.

17 October 2026. Planning source baseline `d0ebe32e691a3d63166ced669450911c63151127`. This tracker distinguishes completed architecture work from future code. Status vocabulary: NOT_STARTED, IN_PROGRESS, BLOCKED, IMPLEMENTED, VERIFIED. VERIFIED requires observed evidence; no code task is marked done by documentation.

Hybrid-role revision authorized by the user's follow-up: all nine roles now have optional AI interpretation, while Python owns canonical calculations and execution. ADR 11.1-11 supersedes the initial permanent split. The user subsequently authorized implementation, which is in progress. Planning receipts below remain historical.

## Planning work

| ID | Status | Evidence / remaining limitation |
| --- | --- | --- |
| P01 repository discovery | VERIFIED | Source/symbol audit in discovery; initial Git clean; current snapshot recorded |
| P02 offline baseline | VERIFIED | 148 passed, 1 skipped, 108 deselected; focused 85 passed overlaps; sandbox attempts interrupted, elevated receipts retained |
| P03 architecture/contracts/alternatives | VERIFIED | Nine catalog entries, state/router/validation/persistence and decision records; target still unimplemented |
| P04 implementation handover/traceability | VERIFIED | T01–T14 and AT01–AT20 map in traceability |
| P05 document consistency and links | VERIFIED | Hybrid revision audit reads 18 documents and confirms nine AI paths/classes, 14 NOT_STARTED tasks, 16 requirements and 20 acceptance IDs; fresh link/previous-sprint checks pass. Original source/inventory/contract/application results remain planning baseline; revision receipt records no new runtime claim |

## Future implementation

| ID | Status | Dependencies | Acceptance criteria | Test evidence | Blockers / next action |
| --- | --- | --- | --- | --- | --- |
| T01 | VERIFIED | user authorized implementation | baseline/preservation and source/runtime distinction | implementation-baseline.md; 148 passed, one skipped, 108 excluded | Normal remains 0012; private backups captured |
| T02 | VERIFIED | T01 | nine hybrid policies/task classes, base/semantic coverage, synthesis DTOs and legacy compatibility | final 52-unit scope; generated clients match | control/contract verification; no model quality claim |
| T03 | VERIFIED | T02 | atomic task/quota storage, RLS, forward migration | 314-test full checkpoint, 0015 lifecycle/drift and final 13 v2 DB cases | Normal remains 0012; rollout open |
| T04 | VERIFIED | T02, T03 integration seam | normalized existing transports/zero-spend preserved | intercepted Ollama/Gemini finish/error/usage/retry-after and egress checks | No live provider activation |
| T05 | VERIFIED | T03,T04 | private local adapter/host slot | intercepted tags/chat/digest, no auto-pull; real DB host-slot test | Control checks only; hardware BLOCKED in T12 |
| T06 | VERIFIED | T03,T04,T05 | deterministic eligibility/ranking and shared quotas | truth table, private global tables, atomic request/token/host-slot checks | Real account quotas require operator verification |
| T07 | VERIFIED | T02,T06 | goal-aware slots across nine roles, explicit priority, requested synthesis reservation, scoped evidence | final planner/context tests and v2 browser | All nine requested cannot imply nine completed calls |
| T08 | VERIFIED | T03,T06,T07 | crash/cancel-safe task execution within counters | 13 final v2 DB cases: replay/crash/concurrency/unknown/cancel/lease/member/source | Original attempt/deadline/authority fences retained |
| T09 | VERIFIED | T07,T08 | nine hybrid specialist role paths with canonical baselines and optional qualified interpretation/synthesis | registry/shared handlers/privacy/span/numeric/basis control tests | Real per-role semantic quality remains BLOCKED in T12 |
| T10 | VERIFIED | T08,T09 | bounded repair/critique and truthful unresolved state | final one-item replacement/usage and critique withdrawal checks | Optional review consumes shared fourth attempt; unqualified reviewer abstains |
| T11 | VERIFIED | T09,T10 | truthful API/UI, safe diagnostics and review | final web/static/contracts and hybrid/legacy browser journeys | Local UI/control verification only |
| T12 | IMPLEMENTED; qualification BLOCKED | T05,T09,T10 | measured local profile qualification or explicit failure | Runner/corpus/review; authorized Qwen3 0.6B trial: two basic controls passed, two project-format attempts rejected; final 53 offline tests; measured server+runner peak 1138 MiB | Native chat preset works; project AI remains unqualified. Small reservation raised to 1536 MiB plus unchanged 2048 MiB headroom; 4B gate unchanged; independent broad quality/representative warm measurements pending |
| T13 | VERIFIED extension seams; optional activation DEFERRED | T06,T12 | disabled-by-default second provider/local embedding seams or explicit disabled disposition | Groq/OpenRouter/Mistral adapters and shared SQL controls; metadata auth; packaged 58-case follow-up | Three original Groq diagnostics retained. Optional generalized cloud benchmark/Puter native driver/embeddings disabled; DeepInfra balance suspended. No required second key |
| T14 | VERIFIED local controls/disposition | T01–T11; T12 result; T13 disposition | local regression, preservation, truthful handover and external-gate disposition | Lifecycle/drift passed; 422 full-suite passes plus six packaging fixture errors corrected in 58-case packaged scope; final 51-case corpus scope; full browser 18 passed/separate hybrid one passed; fresh preservation | AT17 model/release acceptance remains OPEN/BLOCKED; normal rollout not performed |

## Resumption checkpoint

Current [small-model setup/results](../../03-sprints/active/sprint-11.1/OLLAMA_SMALL.md)
supersede the earlier blanket local-testing deferral for this user-approved trial.
Four local calls completed with the normal stack running; project risk root exhausted
at two failures, no profile promoted. Experimental native chat preset `ppm-small`
works with its low-memory launcher. Keep both local ledgers and original Groq history.

The whole-sprint completion request supplied the missing T12 implementation. See
[benchmark workflow](../../03-sprints/active/sprint-11.1/BENCHMARK.md) and ADR 11.1-14.
All 108 draft-labeled cases fit the 4096 conservative context and prepare in four
explicit groups with zero calls. The scorer requires independent review and actual
bound candidates; no quality pass is invented. Final focused scope: 51 passed; rebuilt
image benchmark/Groq scope: 58 passed, overlapping those tests. Full lifecycle/drift
passed; backend 422 passed plus six missing-template fixture errors, corrected by
packaging the public disabled example and rerunning all affected fixtures in the
58-case scope. Preserve the failed receipt; do not report an uninterrupted 428-pass run.
Fresh normal preservation: 0012, 70 table counts/hashes, five object hashes and 24
frozen files match. Overall semantic acceptance remains OPEN/AT17 BLOCKED. Local
testing is still user-deferred and no normal rollout is implied. Older checkpoints
below describe their earlier source snapshots.

Implementation checkpoint: T01 preservation is captured privately under ignored `artifacts/local/sprint111`, including normal DB dump/counts/hashes, original objects, `.env`, applied migrations and working-tree history. Fresh baseline: 148 passed, one skipped, 108 excluded; contracts check passed. Normal DB remains `0012_ai_runtime`. See [baseline](../../verification/sprint11_1/implementation-baseline.md).

T02–T11 are locally verified for implementation/control behavior in the new `model_*`, `agent_*` modules, UI and additive migration `0015_agent_task_runtime`. Full-suite checkpoint: 314 passed; final focused source: 52 unit and 13 v2 DB cases passed. Counts overlap. Mypy: 61 modules passed. Both browser journeys passed. Preservation-after confirms normal 0012, all 70 table hashes/counts, five object hashes and 24 frozen files unchanged. No real model calls, local model qualification or normal migration/deployment occurred. See [exact receipts](../../verification/sprint11_1/IMPLEMENTATION.md).

Current [setup follow-up](../../03-sprints/active/sprint-11.1/PROVIDER_SETUP.md) records the installed digest/private endpoint and user-selected free-tier providers. Next work is private key verification, enough measured host RAM, independent labels and bounded real qualification. No completed benchmark runner is claimed. Profiles remain disabled/benchmark-only; local embeddings stay deferred. Current source retains canonical contradiction gates, no unknown replay, explicit egress, request fingerprints and independent baselines. Never treat synthetic results as model qualification. Follow [current handoff](../../03-sprints/active/sprint-11.1/HANDOFF.md).

The [cloud credential checkpoint](../../03-sprints/active/sprint-11.1/CLOUD_PROVIDER_STATUS.md)
supersedes the pending-key step above: Groq/Puter/DeepInfra authenticate, and the user
deferred local testing. Three Groq diagnostic admissions are retained, no class is
qualified and no profile was activated. Independent quality and native/free-provider
contract gates remain; do not reset the diagnostic ledger to repeat failed work.

For each implementation task add receipt path, exact commands and exit results, source hash, unresolved test IDs and the next failing/unfinished step. If external qualification blocks T12/T13, mark only that task/sub-slice BLOCKED and continue safe independent work; do not describe mock qualification as real model acceptance.
