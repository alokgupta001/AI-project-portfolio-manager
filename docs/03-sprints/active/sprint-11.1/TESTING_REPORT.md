# Sprint 11.1 acceptance disposition

**Final review checkpoint — 23 October 2026:** 495 backend tests plus migration
lifecycle/drift pass in 470.08 seconds, with one inherited Starlette warning.
Focused 95 offline and nine runtime DB scopes overlap. Independent AI label
review passed 108 cases/54 held out; independent output sample review failed.
20 new calibration calls/42 role outputs are retained, with zero evaluated-provider
held-out calls. No provider qualifies. The new predicate-consistency and heartbeat
cleanup cancellation guards reject reproducible failures; they do not establish
semantic accuracy. AT17 remains BLOCKED. Normal 0012, disabled profiles, $0 and
stopped Ollama are preserved. [Final evidence](../../../verification/sprint11_1/review-closeout/README.md).
Earlier counts below are historical.

**Current cloud follow-up:** [results/review packet](../../../verification/sprint11_1/CLOUD_CALIBRATION_RESULTS.md)
and [closeout](../../../verification/sprint11_1/implementation/cloud-specialists-closeout.json).
26 live synthetic calibration requests: nine supported current-prompt role results
pass hard checks; seven/nine absence cases pass, two rejected. No held-out or
independent semantic-accuracy pass. Final 198 offline (4.20 s), 101 DB/provider
(75.44 s), and 37 final prompt-fence DB cases (81.18 s) pass; counts overlap.
Full backend/lifecycle checkpoint: 446 passes/three cloud context-fixture failures
(413.64 s), corrected and verified in the final scopes, not a clean full-suite pass.
Ruff/format/mypy/contracts pass. 24 frozen files/five objects/69 table hashes preserved;
the refresh-token exception is documented, all original rows retained. Ollama stopped,
normal 0012/HTTP 200, all seven profiles disabled; AT17 remains BLOCKED. No browser
rerun was required for this backend/operator change. Earlier receipts remain historical.

Subsequent [authorized small-model trial](OLLAMA_SMALL.md): two basic fixed-fact
controls passed locally; actual project-format initial and one-item replacement
failed strict consistency validation. Four local calls, no profile activation, no
held-out tests. Corrected descendant memory sampling and cold/warm timing controls
passed 53 offline tests. Local setup works for experimental chat; AT17 remains BLOCKED.

Local control acceptance is distinct from model quality and normal rollout. Exact commands/counts are in [verification](../../../verification/sprint11_1/IMPLEMENTATION.md). Source/receipt fingerprints accompany that record. No model was activated or qualified by synthetic tests.

Whole-sprint implementation follow-up: the [benchmark workflow](BENCHMARK.md) now
exists, with 108 draft cases/54 held out, a durable local runner and fingerprint-bound
independent scorer. All cases prepare offline; final focused scope 51 passed and
packaged scope 58 passed, overlapping. Full lifecycle/drift passed; the backend run
had 422 passes and six missing-template fixture errors, all corrected and rerun in
the packaged scope. AT17 remains BLOCKED, with local tests deferred and independent
label approval/real measurements absent. T13 optional activation remains deferred.

Current credential follow-up: 110 focused offline cases and 16 isolated DB regressions
passed after stricter decoder identity binding. Three real fixed-synthetic Groq
requests all stopped on configuration/output/evidence failures; none establishes
quality. Groq/Puter/DeepInfra metadata authentication passed, but DeepInfra is
balance-suspended and Puter's native free inference contract remains unverified.
See [current provider status](CLOUD_PROVIDER_STATUS.md).

| Acceptance                       | Current evidence / limitation                                                                                                                                                                                                                                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AT01 nine roles                  | Registry IDs/task classes and mode contracts tested; all nine baselines persisted in a metrics run. Real reasoning quality for each class remains T12.                                                                                                                                                                   |
| AT02 goal-aware budget           | Explicit priorities, metrics zero calls, reserved Executive-only synthesis, three initial sections and deferred requested roles tested.                                                                                                                                                                                  |
| AT03 route eligibility           | Scope/class/quality/capability/memory/cloud/paid denials before stable ranking; missing egress binding denies even empty categories.                                                                                                                                                                                     |
| AT04 adapters                    | Intercepted Ollama/Gemini/Groq/OpenRouter/Mistral finish, usage/refusal/429, no tools/reasoning/app retries and fixed origins. OpenRouter paid-price denial before POST. Local inventory and saved Groq/Puter/DeepInfra metadata authentication verified; neither establishes inference quality.                         |
| AT05 quotas                      | Atomic DB admission/retained reservations, private owner tables, two workers sharing one local generation slot, request/token exhaustion and shared-alias policy checks. Account-specific cloud quotas remain operator verified.                                                                                         |
| AT06 recovery/checkpoints        | Idempotent replay and candidate-checkpoint crash resume without another inference; immutable section mutation denied.                                                                                                                                                                                                    |
| AT07 fixed limits                | Strict 512 output, four run/two section attempts, deadline/task bounds, no unknown-timeout replay; all limits remain hard maximums.                                                                                                                                                                                      |
| AT08 live fencing                | Existing legacy cancellation/lease/source/member cases plus final dedicated v2 paused-call cases. Final v2 receipt is authoritative for their disposition.                                                                                                                                                               |
| AT09 authority/privacy           | Existing tenant/project/assessment/session checks reused; direct app-role cross-tenant task/section reads denied, global scopes unavailable to app, sentiment pack admits only group summary.                                                                                                                            |
| AT10 scores/numbers              | Original scoring unchanged; question/level/span gates, no partial suggested dimension, unknown confidence, exact cited numerical prose and canonical adverse-predicate contradiction checks.                                                                                                                             |
| AT11 truncated/oversized work    | One fresh smaller replacement, preserved usage, no concatenation/counter reset; oversized whole sources return explicit context gap. Automatic window decomposition deferred under ADR 11.1-12.                                                                                                                          |
| AT12 reconciliation/synthesis    | Distinct claims retained, exact opposition links, separate base/AI coverage and mandatory gap/conflict disclosures; basis scopes remain provisional.                                                                                                                                                                     |
| AT13 semantic review             | Critique can abstain/withhold and withdraw dependent summaries; no independent-truth or approval claim. Actual precision/recall requires T12 corpus.                                                                                                                                                                     |
| AT14 diagnostics                 | Safe codes/model/finish/latency/nullable usage and task state only; no raw model prompt/key/reasoning in public diagnostics.                                                                                                                                                                                             |
| AT15 local resource/network      | Existing mocked/SQL controls plus four real small-model requests alongside the full stack. Small-model peak 1138 MiB server+runner, min available 3215 MiB, no observed OOM/unknown outcomes; controls unloaded. 4B and representative warm/full-corpus qualification remain unavailable/unverified.                     |
| AT16 compatibility/UI            | Generated clients/static checks; legacy independent review/evidence/privacy browser and v2 goal/coverage/keyboard/mobile/axe journeys passed. Local checks are not full accessibility certification.                                                                                                                     |
| AT17 model qualification         | BLOCKED: installed digest, runner, 108 draft cases and review/scorer exist; independent label approval and inference measurements remain missing. No dry-run/mock qualifies a profile.                                                                                                                                   |
| AT18 optional provider/embedding | Groq plus user-selected OpenRouter/Mistral transports and real shared SQL admission verified with synthetic responses. Groq authenticates; OpenRouter/Mistral keys absent; all model classes unqualified. Optional generalized cloud benchmark/native Puter/embeddings DEFERRED and disabled; keyword fallback retained. |
| AT19 preservation                | Normal 0012, 70 established table counts/hashes, five object keys/hashes and 24 frozen credential/source/prompt/migration files unchanged. 0015 lifecycle only in disposable DB.                                                                                                                                         |
| AT20 docs/handoff                | Current report/tracker/setup/ADR 11.1-14, benchmark/review workflow, generated inventories, requirement mapping, 55 source fingerprints and link/previous-sprint audits maintained.                                                                                                                                      |

No production scale, hosted CI, broad semantic accuracy, hardware performance or normal forward rollout is certified. The optional profile-enablement procedure must not bypass T12, trustworthy host-memory/private-network checks or the existing non-billable cloud confirmation.
