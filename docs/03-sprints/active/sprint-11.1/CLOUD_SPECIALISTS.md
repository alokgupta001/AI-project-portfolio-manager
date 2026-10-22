# Three cloud providers and nine specialist roles

17 October 2026. The user selected Gemini, Groq and Puter, requested that Ollama be
shut down, and asked for training or fine-tuning where feasible. Ollama's resident
inventory was empty; its verified tray/server processes were stopped. Installed
weights and startup settings were preserved. No further local inference is planned.

## Role assignment

The [public candidate policy](../../../../config/model-policy.cloud.example.json)
divides the existing nine roles as follows. This is an engineering assignment, not
a claim that a provider outperforms the others. Qualification can change the choice.

| Provider / requested model | Roles | Boundary |
| --- | --- | --- |
| Gemini / `gemini-3.5-flash-lite` | Financial, Schedule, Resource | Explain cited pressure/dependencies; Python retains arithmetic and canonical capacity metrics. |
| Puter native / `gpt-4.1-mini-2025-04-14`, provider `openai-completion` | Risk, Governance, Agile Coach | Evidence-linked implications, supplied policies/rubrics and process advice; no invented certification. |
| Groq / `openai/gpt-oss-20b` | Team Support, PMO, Executive | Aggregate support/PMO in one batch, executive synthesis in a separate final call. |

`assigned_task_classes` restricts routing and is separate from
`qualified_task_classes`. Assignment cannot enable a profile, grant tenant/project
scope, establish accuracy or bypass egress/account checks. All seven private
profiles remain disabled/benchmark-only with no qualified classes or tenant scopes.
Normal migration remains 0012; no scope synchronization or normal v2 rollout occurs.

The explicit `all_specialists` goal uses four bounded calls for the nine roles:
Gemini three, Puter three, Groq two then one. Selected/automatic modes retain their
previous planning. The four attempts/run, two/logical batch, 512 output tokens and
90-second deadline remain. Missing evidence, oversized input, repair or account
limits can still produce honest partial coverage. The second Groq call waits for
its existing minute window when the deadline permits. No extra runs or quota increase.
Read the [current batching/repair report](../../../verification/sprint11_1/CLOUD_BATCH_REPAIR.md)
and [reviewer guide](../../../verification/sprint11_1/REVIEWER_GUIDE.md). The allocation
replaces the initial assignment; small calibration does not prove best accuracy.

## Feasible improvement instead of unavailable weight tuning

Checked official documentation:

- [Gemini tuning](https://ai.google.dev/gemini-api/docs/model-tuning.md): no tunable
  model in the developer API/AI Studio. A different enterprise service is required.
- [Groq LoRA](https://console.groq.com/docs/lora): enterprise inference of adapters
  trained externally; free Groq accounts cannot deploy these adapters, and Groq
  does not perform the training.
- [Puter chat](https://docs.puter.com/AI/chat/): inference, output schemas and provider
  pinning are documented. No supported free fine-tuning/deployment path was found.
  Availability through another vendor is not authorization to provision or pay it.

No training job, upload, new account, paid plan or model-weight modification occurred.
The implemented improvement is versioned role instructions plus an original positive
example and a separate missing-evidence format example. This is in-context prompting,
not fine-tuning. Runtime request hashes retain the actual prompt/schema/model. New
cloud runs record the prompt-selection version; old results are not rewritten.

The [36 authored examples](../../../../tests/fixtures/agent_v2_training.json) cover four
scenarios per role, separate from the existing 108-case quality corpus. All expected
outputs pass unchanged schema/span/numeric/coverage checks. Labels are author drafts,
not independent truth. [Exporter](../../../../scripts/prepare_agent_training.py)
produces a private JSONL development artifact without training or uploading it.
The positive runtime examples come only from that training split.

References inform general concepts: [GAO cost](https://www.gao.gov/products/gao-20-195g),
[GAO schedule](https://www.gao.gov/products/gao-16-89g),
[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) and the
[Scrum Guide](https://scrumguides.org/scrum-guide.html) by Ken Schwaber and Jeff
Sutherland, CC-BY-SA-4.0. No document passages or external dataset rows are copied.
[Financial PhraseBank](https://huggingface.co/datasets/takala/financial_phrasebank)
was screened but excluded: financial-news sentiment is a different task and its
CC-BY-NC-SA-3.0 terms do not establish suitability for this enterprise application.
A Kaggle project-risk notebook was located, but underlying provenance/suitability
was not established; no rows were downloaded or claimed to be validated labels.

## Integration corrections and live calibration

Evidence aliases, subjects, basis and questions have distinct meanings. Packing now
provides source lengths and constrains predicates to each role's existing hard gate.
Gemini structured schemas require every output field, matching Groq's strict schema
handling. A complete response without the required finding still fails validation.
Financial instructions prohibit generated quantities/threshold comparisons; canonical
numbers remain in Python's baseline. No validator was weakened to accept a failure.

Puter uses `https://api.puter.com/drivers/call`, never the paid compatible gateway.
The reviewed public catalogue maps the requested dated alias to `gpt-4.1-mini` on
`openai-completion`. Its native response identifies that canonical ID in metadata,
rather than echoing `model` inside ChatResponse. Both service and canonical ID are
checked; the requested ID and reported canonical ID remain separate. This is a
provider identity binding, not proof of immutable remote weights or semantic quality.
Finish reason, usage, refusal and unknown outcomes remain actual provider values.
Puter meters consumption against its monthly allowance; $0 here means the user's
confirmed Free account without paid fallback, not that each inference has zero
metered cost. No billing setting was changed. See
[Puter quotas](https://docs.puter.com/rate-limits-and-quotas/) and
[native response](https://docs.puter.com/Objects/chatresponse/).

The [calibration runner](../../../../scripts/benchmark_cloud_specialists.py) accepts
only named calibration cases in the frozen synthetic corpus and assigned roles.
No real tenant data or held-out input is sent. It defaults to dry-run; execution
requires an exact key/account/model/corpus-bound private record. Limits: nine total
admissions per provider under this authorization, at most three named cases/batch,
22 seconds/attempt, 90 seconds/batch, 512 output tokens, two attempts per logical
evidence case, one request/minute/provider and the preserved 20/day account ceiling.
Changing prompt, output path or corpus filename cannot reset a case counter.
Original Groq smoke admissions, direct Gemini smoke receipts and read-only legacy
Gemini SQL counts are included conservatively. The old three-call diagnostic's own
allowance is not enlarged or reset. Unknown outcomes block further provider calls.

This operator calibration is separate from production SQL admission. It does not
claim atomic coordination with other external account users or prove production
concurrency. Native responses/candidates are checkpointed privately before validation
when available; public receipts contain only hashes, counts and sanitized outcomes.
Early failures without raw checkpoints remain retained and are not retroactively
declared successful. Prompts were refined only against calibration/training inputs.

## Earlier calibration checkpoint; acceptance still required

Observed [results and candidate review packet](../../../verification/sprint11_1/CLOUD_CALIBRATION_RESULTS.md)
and [closeout](../../../verification/sprint11_1/implementation/cloud-specialists-closeout.json):
26 actual requests, nine supported current-prompt roles passing hard checks, seven of
nine absence cases passing. Financial/resource absence outputs were rejected. The
nine supported samples took 679–2,258 ms; these are individual observations, not p95
or a general latency/accuracy guarantee. Groq/Gemini nine-call authorizations are
consumed; Puter has eight admissions. No ledger or exhausted root may be reset.

Final 198 offline, 101 DB/provider and 37 prompt-fence DB checks pass (overlap).
Full backend/lifecycle checkpoint had 446 passes/three cloud context-fixture failures;
all affected fixtures were corrected and rerun in final scopes. Do not combine these
into a clean full-suite pass. Normal revision is 0012, readiness 200. Preservation
checks verified five objects/24 frozen files/69 table hashes. The sole changed table
contains all 65 original refresh-token rows with unchanged session bindings, two
additional tokens and one consumed used flag, consistent with ordinary session
refresh. Both initial strict snapshot failure and private-backup disposition are
retained. No normal migration, data restoration, scope sync or v2 activation occurred.

Hard validation and a small supported/absent sample establish useful integration
evidence, not broad accuracy. The [qualification gates](BENCHMARK.md) remain:
independently reviewed labels/outputs, twelve cases and six untouched held-out cases
per activated class, precision/recall/abstention denominators, supported added
interpretation, preserved canonical results and measured operational behavior.
The old local hardware fields cannot be repurposed into a cloud qualification claim.
A separate bound cloud scorer/runner now exists, with 108 fresh draft cases/54 held
out and no acceptance inference before independent approval. Keep profiles disabled
until an independently reviewed cloud acceptance report and scoped rollout decision
exist. DeepInfra remains excluded by its recorded balance suspension.

The earlier small-Ollama and three-call Groq documents remain historical evidence.
This document supersedes their next-action/deferred-native-Puter statements only.
