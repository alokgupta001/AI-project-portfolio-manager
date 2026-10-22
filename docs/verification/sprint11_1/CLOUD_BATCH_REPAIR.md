# Cloud batching and acceptance follow-up

Current follow-up: 22 October 2026. Continues the user's request to fix the remaining
Sprint 11.1 issues. The user will nominate an independent reviewer; that review is
pending. The earlier [26-call calibration](CLOUD_CALIBRATION_RESULTS.md) and all failed
attempts remain retained evidence.

## Four calls for nine roles

The explicit `all_specialists` goal requests nine roles in four serial batches.
Automatic/selected-role planning retains its previous behavior. Each batch returns
compact role outputs that Python expands into the existing typed section contract,
validates independently and publishes under separate role coverage. A bad member
rejects the batch; it is never silently rewritten into a supported finding.

| Call | Candidate | Roles | Dependency |
| --- | --- | --- | --- |
| 1 | Gemini `gemini-3.5-flash-lite` | Financial, Schedule, Resource | Canonical baselines and authorized evidence |
| 2 | Puter native `gpt-4.1-mini-2025-04-14` | Risk, Governance, Agile Coach | Canonical baselines and authorized evidence |
| 3 | Groq `openai/gpt-oss-20b` | Team Support, PMO | Committed domain findings and privacy-safe aggregates |
| 4 | Groq `openai/gpt-oss-20b` | Executive | Committed PMO result; other unresolved scope remains explicit |

This operational assignment replaces the earlier provisional allocation: Groq's
three-domain batches failed schema/completion checks under the 512-token ceiling,
whereas its smaller portfolio and executive requests passed. Gemini and Puter both
returned hard-valid three-domain responses. This is measured format/fit evidence,
not an independent semantic ranking. Profile assignment still grants no qualification,
tenant scope or production activation.

The 512 output tokens/attempt, four attempts/run, two attempts/logical batch, 24 nodes
and 90-second deadline remain. There are thirteen planned nodes. Repairs share the
four-call budget; a repair can leave Executive unavailable. Batches do not create
extra runs. Whole evidence excerpts remain intact, with only repeated Python-owned
response identifiers removed from the request. Oversized input produces explicit
partial coverage. Batching private assessment answers across roles is rejected;
use separate scoped assessment analysis.

The two Groq calls share its existing one-request/minute and 8,000-token/minute
account gate. The worker can wait in the same run for its previous admission window
to clear, while refreshing its lease and checking live authority. It stops if the
remaining deadline cannot fit the call. This can add about a minute; it does not
raise quotas or promise completion for arbitrary evidence/latency.

## Evidence and output fixes

Coverage/gaps now reference required scope, not unrelated contextual aliases.
Financial/resource findings must cite primary required evidence and use qualitative
claim/advice without digits. Canonical quantities remain in Python's baseline.
Context metrics cannot substitute for missing primary evidence. These boundaries
are enforced after decoding as well as in provider schemas.

Groq HTTP 400 `json_validate_failed` is classified as a completed invalid output or
truncation when its bounded error explains the completion cap. Configuration errors
remain distinct. Recovery still consumes normal attempts. Private bounded native
error checkpoints support diagnosis; old receipts are not retrospectively changed.

Saved multi-role candidates resume through the same validation and prompt/input
hash fences. Revoking any bound source withholds the batch, including no-findings
responses. Routing and the transport require qualification/assignment for every
member class, not just the first role.

## Measured repair calibration

The user's fix request supplied a separate six-call repair allocation/provider.
Original nine-call authorizations were preserved, not renewed. Each batch admission
charges every included case root; moving a case into another format cannot reset its
two-attempt counter. Account history, prior Groq probes and legacy Gemini usage
remain counted. All eighteen allocations were consumed; do not rerun this phase.

| Provider | New requests | Hard-valid batches | Retained failures |
| --- | ---: | ---: | ---: |
| Gemini | 6 | 6 | 0 |
| Puter | 6 | 6 | 0 |
| Groq | 6 | 3 | 3 |

There are 42 hard-valid role results: 24 supported, seventeen insufficient-evidence
responses and one no-findings response. Three supported Gemini synthesis responses
occurred on draft absence cases: these do not match the draft abstention expectation
and require review. Hard validity alone cannot establish semantic accuracy. The
selected allocation has a positive and abstaining absence observation for each role.
In particular, financial/resource absence cases return gaps on Gemini and Puter.
The old rejected Groq financial/resource results remain failures. Batch prompts were
refined during calibration; results span revisions and do not qualify current models.

Persistent specialist ledgers now contain Groq 15, Gemini 15 and Puter 14 admissions
(44 total), plus the separately retained original three Groq probes. No outcomes are
unknown. Detailed measured candidates/usage/latency and hash-bound receipts are in
the [reviewer packet](REVIEWER_GUIDE.md). Individual timings are not a p95 claim.
Puter's reported canonical alias remains distinct from the requested dated ID.
Native allowance consumption is metered; no paid gateway or billing change occurred.

## Acceptance preparation and remaining gate

The fresh [108-case cloud corpus](../../../tests/fixtures/agent_v2_cloud_quality.json)
contains twelve draft cases/role and six held out/role, including two separate
governance rubric cases. All prepare offline. No fresh case has been sent to a
provider or added to prompt examples. Independent labels/ratings are still required.
The [offline input-bound check](implementation/acceptance-context-preparation.json)
finds five larger financial/schedule/resource triples exceeding the conservative
input envelope. Use deliberately smaller benchmark batches for those cases; private
rubric answers are also tested alone. Production does not add calls to hide an
oversized batch: its corresponding interpretation remains partial.

The cloud scorer uses measured provider/model identity, corpus/strategy/report/
candidate hashes and the original precision/recall/abstention/canonical gates. It
does not fabricate a local model digest, hardware usage or cold/warm measurements.
It requires observed runtime batch shapes, at least five measured calls, p95 at
most twenty seconds, no failed/unknown calls in the bound acceptance evidence, and
twelve cases/six held out for each qualifying class. No score can activate a profile.

After independent approval, an operator can prepare a distinct, immutable acceptance
allocation, at most 36 additional requests/provider. It is not created automatically
and cannot reset existing case/account history. Daily twenty-call, minute, unknown
outcome and two-attempt limits still apply. A complete Groq acceptance can span days.
The tools create no recurring job or hidden follow-up run.

```powershell
# Only after the nominated reviewer has completed and frozen this approval file:
.venv/Scripts/python.exe scripts/benchmark_cloud_batches.py --provider groq --acceptance --label-approval artifacts/local/approved-cloud-labels.json --prepare-phase --output artifacts/local/groq-acceptance-allocation.json
# Dry-run first; repeat for deliberately selected assigned cases/provider.
.venv/Scripts/python.exe scripts/benchmark_cloud_batches.py --provider groq --acceptance --label-approval artifacts/local/approved-cloud-labels.json --case-id cloud_executive_02 --output artifacts/local/groq-executive-prepared.json
# --execute is an explicit bounded inference invocation; never rerun an unknown outcome.
.venv/Scripts/python.exe scripts/score_cloud_benchmark.py --review artifacts/local/groq-output-review.json --label-approval artifacts/local/approved-cloud-labels.json --reports artifacts/local/groq-acceptance-report.json --output artifacts/local/groq-qualification.json
.venv/Scripts/python.exe scripts/check_model_qualification.py artifacts/local/groq-qualification.json
```

Fine-tuning remains unavailable through these current free integrations; no weight
training/upload is claimed. Normal rollout remains gated by reviewed acceptance and
scoped data-egress authorization. Ollama stays stopped, DeepInfra excluded, seven
profiles disabled and the normal database at 0012. No normal migration, scope sync,
deployment, commit/push or Sprint 12 occurred.

## Verification

The full backend/lifecycle checkpoint passes 475 tests. Three isolated database cases
pass: all nine roles in four admissions, repair
exhaustion with honest partial coverage, and crash-after-candidate recovery without
duplicate inference. The final cloud approval/scoring scope passes 48 checks; counts
overlap. All 70 normal table hashes, five original objects and 24 frozen files are
preserved. One focused browser journey passes in 38.6 seconds, with all-nine selection,
terminal partial coverage, accessibility, responsive layouts and keyboard scrolling
at 1440/768/360. Desktop/mobile screenshots were visually inspected and retained.
The initial browser assertions incorrectly inspected a streamed request body and
queued goal metadata; corrected assertions wait for completed coverage. Both failed
receipts remain. [Source/data/provider closeout](implementation/batch-closeout.json)
verifies 72 source fingerprints and unchanged normal 0012/HTTP200. Ruff176/mypy65,
contracts/frontend, documentation inventories/links pass; npm audit zero vulnerabilities.
Ollama's restarted unloaded tray/server were stopped again; zero processes, installed
weights/startup preserved. Earlier failed test fixtures/receipts remain historical.
