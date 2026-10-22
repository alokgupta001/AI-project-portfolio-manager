# Sprint 11.1 benchmark and qualification

Cloud follow-up: use the separate [cloud batching/acceptance workflow](../../../verification/sprint11_1/CLOUD_BATCH_REPAIR.md)
and [independent reviewer packet](../../../verification/sprint11_1/REVIEWER_GUIDE.md).
Cloud acceptance binds service identity and measured calls; local hardware fields
below must never be replaced with invented cloud RAM/digest values.

**Current cloud work:** [three-provider guide](CLOUD_SPECIALISTS.md) and
[results/review packet](../../../verification/sprint11_1/CLOUD_CALIBRATION_RESULTS.md)
describe the new separate bounded synthetic cloud calibration. 26 requests, nine
supported role results passing hard checks, seven/nine absence cases passing; no
independent quality/held-out or promotion claim. Groq/Gemini calibration authorizations
are consumed and must not be reset. The local runner/scorer below remains a local
measurement workflow, not a cloud promotion tool. Ollama has been stopped. Original
training examples are separate from this frozen quality corpus.

Subsequent [small-model trial](OLLAMA_SMALL.md): explicit user approval resumed
controlled local testing for Qwen3 0.6B. Native setup controls passed; project-format
initial/replacement attempts failed and are retained. The runner now accepts
`--keep-alive 0` for immediate unloading; warm-repeat measurement requires 60-second
residency, and cold timings are excluded from warm statistics. No model qualified.
The earlier no-generation/deferred statements below describe the pre-trial checkpoint.

The remaining benchmark implementation now exists. This is a measurement and review
workflow; it does not activate a provider. The user previously deferred local testing
in favor of cloud setup, so this completion pass prepares local evaluation without
loading a model. The latest measured host memory failure remains historical evidence,
not a new measurement. No profile has qualified.

## Frozen evaluation inputs

The [bundled corpus](../../../../tests/fixtures/agent_v2_quality.json) contains 108
synthetic cases: twelve per interpretation class, six held out per class. Supported
delivery implications, absent/irrelevant evidence, conflict, injection, privacy and
unsupported causality are represented for every role. Two governance cases exercise
rubric levels. Financial, schedule and resource cases carry separate canonical
numbers. Resource positive cases use only the published canonical aggregate metric,
and team positive cases use only the current privacy-safe blocker-count text. They
cannot qualify richer staffing narratives, emotional inference or individual analysis.
A model that only restates those limited inputs fails the added-interpretation gate;
no unavailable narrative is invented to make it pass. Aggregate team advice and PMO/Executive use the actual synthesis packer and
basis aliases. Expected support, advice relevance, omissions and abstention labels
are excluded from every model payload.

Labels are **draft**, authored before inference. They have not received independent
approval. Held-out inputs must not be used to tune prompts. A changed prompt invalidates
the evaluation's claim to an untouched holdout; obtain a new independent set. The
36 additional role/control combinations in `tests/test_agent_benchmark.py` cover
metrics-only zero calls, scoped evidence, unavailable semantics and rejected authority.
These controls and the corpus's existence are not semantic accuracy measurements.

[Prepared groups](../../../verification/sprint11_1/benchmarks/current/prepared-1.json) cover
cases 1–30, [31–60](../../../verification/sprint11_1/benchmarks/current/prepared-2.json),
[61–90](../../../verification/sprint11_1/benchmarks/current/prepared-3.json) and
[91–108](../../../verification/sprint11_1/benchmarks/current/prepared-4.json).
All are dry runs, with zero model/network requests. The
[review template](../../../verification/sprint11_1/benchmarks/current/independent-review-template.json)
has no invented reviewer, ratings or approval. Review the labels first; after actual
inference, independently judge each candidate against the frozen labels. Keep a
private working copy of the completed review, including report/candidate hashes.
The earlier prepared draft groups are retained one directory above `current/`; their
corpus hash is superseded after aligning resource/team inputs to the actual contracts.

## Local execution

Run commands from the repository root. The runner defaults to dry-run. It accepts only
the bundled synthetic corpus, a disabled installed local benchmark profile and a
fresh output filename. It rejects cloud mode and enabled local production profiles.
Never run it while another operator is using Ollama. Production profiles remain
disabled throughout benchmarking. Its exclusive lock coordinates benchmark invocations;
it is not a substitute for production's SQL admission or authorization.

```powershell
.venv/Scripts/python.exe scripts/benchmark_agent_runtime.py --mode local-only --model qwen3:4b --case-id risk_01 --max-calls 1 --output artifacts/local/ai-v2/risk-prepared.json
```

After local testing resumes, independently approved labels and enough measured RAM:

```powershell
.venv/Scripts/python.exe scripts/benchmark_agent_runtime.py --mode local-only --model qwen3:4b --case-id risk_01 --context 4096 --max-output 512 --concurrency 1 --max-calls 6 --warm-repeats 5 --execute --output artifacts/local/ai-v2/risk-measured.json
```

At most thirty explicitly selected calls per invocation. Each quality fixture is one
synthetic analysis with one attempt, bounded by 22 seconds (inside the 90-second run
limit); no repair or retry is automatic. Repeat explicit invocations only for the
remaining named cases. Persistent per-corpus/model/case quality counters allow at most
two attempts. Warm repeats are explicitly requested timing measurements, excluded from
semantic votes/recall and limited to five per invocation. Do not use them to retry a
failed case or erase its quality result. Unknown requests quarantine subsequent runs;
never delete the ledger or lock to replay an uncertain generation. An operator must
verify the process stopped and retain an incident disposition before recovery.

The preflight checks host RAM, installed digest and resident models. Each request
rechecks the digest. During inference it samples host headroom and Ollama process
working sets every 100 ms, cancels below 2 GiB, and retains conservative unknown state.
The observed peak is a **sampled sum of process working sets**, not exclusive memory or
a guaranteed instantaneous peak. Windows host measurement is required. Cold status is
observed from residency; the runner never unloads someone else's model. It retains
load time, generation duration, reported tokens and end-to-end timing when available;
time-to-first-byte and GPU utilization are not measured by this runner. No inferred
throughput or estimated latency is labeled measured. Record Docker limits, active
services, browser/API activity and GPU use separately in the reviewed hardware receipt.

## Review and promotion boundary

```powershell
.venv/Scripts/python.exe scripts/score_agent_benchmark.py --template --output artifacts/local/ai-v2/review-draft.json
.venv/Scripts/python.exe scripts/score_agent_benchmark.py --review artifacts/local/ai-v2/review-completed.json --reports artifacts/local/ai-v2/risk-measured.json --output artifacts/local/ai-v2/qualification.json
.venv/Scripts/python.exe scripts/check_model_qualification.py artifacts/local/ai-v2/qualification.json
```

The scorer requires independent label review, report/candidate fingerprint binding,
actual candidates, hard validation and explicit judgments on interpretation, advice,
omissions, canonical preservation and abstention. A real but irrelevant quote can pass
the hard gate and receive zero correct semantic claims. Incomplete classes, missing
ratings, changed candidates or absent cold/warm/memory measurements cannot qualify.
Model, prompt, corpus, context/output and stable hardware identity must agree across
merged reports. No script enables or promotes a profile. The report checker still
requires operator provenance verification, representative extraction/rubric/advice
timing, complete hardware evidence and explicit deployment review before promotion.

Thresholds remain twelve labeled/six held-out per activated class, 90% precision,
80% recall, 90% abstention, canonical preservation 100%, no citation/numeric/privacy
errors, and at least one added supported interpretation per class. Local gates remain
five warm measurements, p95 ≤20 seconds, cold ≤22 seconds, ≥2 GiB headroom, one
generation and no OOM. No free cloud qualification is claimed: the separate Groq
transport probe's three retained attempts remain its full allowance. Puter native free
inference, DeepInfra funding and local embeddings remain optional disabled slices.
