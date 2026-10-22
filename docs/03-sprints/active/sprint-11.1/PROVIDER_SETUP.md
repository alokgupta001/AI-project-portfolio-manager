# Local runtime and additional provider setup

**Current:** the user selected [three cloud specialists](CLOUD_SPECIALISTS.md) and
requested Ollama shutdown. Ollama processes are stopped; do not restart local models
as a prerequisite for cloud work. Groq/Gemini/Puter native free-allowance integration
has live synthetic calibration evidence. All profiles stay disabled/unqualified.
Saved keys/confirmations are preserved; do not ask for them again. Private candidate
preparation uses `scripts/prepare_cloud_specialists.py`; calibration is dry-run by
default with retained counters. Current nine-call Groq/Gemini calibration authorizations
are consumed. No counter reset, billing change or normal activation is implied.

Subsequent user-approved [small-model setup](OLLAMA_SMALL.md) is installed and tested
for experimental native chat. Qwen3 0.6B/`ppm-small` fits the measured trial envelope;
project-format initial/replacement requests both failed strict validation, so its
application profile remains disabled. Earlier local-deferral/no-generation statements
below describe the prior checkpoint. No cloud credentials or 4B memory gates changed.

17 October 2026 (Asia/Calcutta). The user authorized the remaining setup and selected
Groq, OpenRouter and Mistral AI, confirming free-tier use. Existing Gemini credentials,
confirmation and normal database are preserved. New provider transport support does
not establish model quality or enable normal application inference.

Current [cloud credential status](CLOUD_PROVIDER_STATUS.md) supersedes the original
empty-key checkpoint: Groq/Puter/DeepInfra now authenticate; DeepInfra is balance
suspended, and Puter's Free account needs native free-driver integration. Only Groq
received the three bounded synthetic requests; none passed all evidence checks or
qualified a class. Local testing was deferred by the user.

## Private keys

Enter available keys only in ignored `artifacts/local/ai-v2.env`; absent providers
may stay blank. Puter/DeepInfra currently have metadata checks only, while the
Groq/OpenRouter/Mistral inference transports remain subject to qualification:

```dotenv
PPM_AI_GROQ_API_KEY=
PPM_AI_OPENROUTER_API_KEY=
PPM_AI_MISTRAL_API_KEY=
PPM_AI_PUTER_API_KEY=
PPM_AI_DEEPINFRA_API_KEY=
```

The local editor was requested for that file. Never send key values in chat, command
arguments, source control or verification receipts. The existing Gemini key stays in
its established private file. Additional keys do not create additional account quota;
profiles for the same provider account must share the existing account scope.

Read-only local check (prints presence/status only):

```powershell
.venv/Scripts/python.exe scripts/check_provider_setup.py --confirmed-free-tier groq puter --record-bindings
```

After keys are saved, add `--verify` to issue authenticated metadata GETs to fixed
official origins. It never requests inference, follows redirects or prints response
bodies/account balances/key labels. Key hashes and operator confirmation are stored
privately in `artifacts/local/ai-v2/provider-bindings.json`; available model IDs stay
private. This verifies credentials only. It cannot verify account billing controls,
data-policy acceptance, model capability or semantic quality by itself.

## Ollama

Ollama 0.40.5 was installed through the official Windows package, with the installer
hash verified by WinGet. Native host API and Docker-to-host API version requests
passed; Docker reached `http://host.docker.internal:11434` while Ollama remained bound
to loopback. This observation needs rechecking after networking/security changes.

The following user environment settings were configured for the new installation:
`OLLAMA_NO_CLOUD=1`, `OLLAMA_HOST=127.0.0.1:11434`,
`OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_NUM_PARALLEL=1`,
`OLLAMA_CONTEXT_LENGTH=4096`. Server startup must retain these controls.
See [official Windows setup](https://docs.ollama.com/windows) and
[server controls](https://docs.ollama.com/faq).

The selected candidate is Qwen3 4B. Installation/download is separate from loading,
qualification and application activation. No generation is authorized by an inventory
check. The [benchmark protocol](../../../09-planning/sprint-11.1/SPRINT_11_1_TEST_PLAN.md#benchmark-protocol-and-thresholds)
still requires sufficient measured memory, independently reviewed labels and measured
latency/quality per task class. The subsequent [benchmark implementation](BENCHMARK.md)
now supplies the runner, 108 draft cases and independent review/scoring workflow.
Actual local inference remains user-deferred; no independently approved labels or
model qualification is claimed.

Downloaded `qwen3:4b` is Q4_K_M, digest
`359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7`.
The [publisher model card](https://huggingface.co/Qwen/Qwen3-4B) lists Apache-2.0.
The current [inventory receipt](../../../verification/sprint11_1/implementation/local-readiness-installed.json)
records advertised model metadata separately from the configured 4096-context cap.
No model was loaded; changing a mutable download tag later requires digest revalidation
and qualification again.

Fresh host readiness, from a Windows terminal in the repository:

```powershell
.venv/Scripts/python.exe scripts/check_local_model.py --model qwen3:4b --reservation-mb 4096
```

This uses Windows host available memory, not container RAM. It checks only private
GET version/tags/residency endpoints and cannot pull, load, unload or generate. It
requires at least 6144 MiB available for the initial 4B reservation/headroom envelope.
The smaller candidate starts at 4096 MiB. Readiness is a point-in-time observation,
not a production host monitor, reservation or model qualification. Do not copy its
available-memory reading into a permanent production guarantee.

## New cloud transports and activation gates

All three use fixed official HTTPS origins, one bounded non-streaming JSON-schema
request, no tools, no app-level retries/redirects, preserved finish/usage information
and sanitized errors. Schema/citation validation, tenant/project egress, shared SQL
account quotas and all original output/run limits remain authoritative. Returned
tool calls/reasoning are rejected. Unknown usage stays unknown.

Groq and Mistral require an exact reviewed model ID, confirmed free account, current
key-hash binding and data-policy acceptance. Mistral uses a dated model ID rather
than a moving `latest` alias. [Groq organization quotas](https://console.groq.com/docs/rate-limits)
and [Mistral account limits](https://docs.mistral.ai/admin/billing-usage/usage-limits)
must be checked for the actual account; sample limits are conservative placeholders.
Neither provider has a request-level free-only switch, so the confirmed non-billable
account configuration remains necessary.

OpenRouter additionally requires an exact `:free` model and one reviewed upstream
provider, a fresh zero-price endpoint catalog, zero request price caps, no fallback
routing, parameter support, data-collection denial and ZDR. A missing/nonzero catalog
price or missing/nonzero reported cost fails closed. Requests may be unavailable when
no upstream satisfies all constraints. See [provider routing and price caps](https://openrouter.ai/docs/guides/routing/provider-selection)
and [structured-output endpoint support](https://openrouter.ai/docs/guides/features/structured-outputs).

`config/model-policy.example.json` contains disabled candidates only. OpenRouter's
model/upstream values are placeholders, and all candidate IDs must be reconciled with
current availability. No tenant/project/category egress is implicitly granted.
Every activated task class still needs real qualification; metadata authentication
and intercepted tests do not supply it. Keep v2/cloud flags disabled until those gates
and the existing Gemini legacy-dispatch transition are satisfied. See the
[main operator guide](../../../09-planning/sprint-11.1/SPRINT_11_1_SETUP.md).
