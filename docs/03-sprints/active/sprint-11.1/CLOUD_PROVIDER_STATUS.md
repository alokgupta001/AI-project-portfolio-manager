# Cloud credentials and bounded connection checks

**Current: user-requested three-provider integration.** See
[role assignment/setup](CLOUD_SPECIALISTS.md) and
[calibration evidence](../../../verification/sprint11_1/CLOUD_CALIBRATION_RESULTS.md).
26 bounded synthetic requests: Groq 9/Gemini 9/Puter 8. Every role has a supported
current-prompt result passing hard checks; seven/nine absence cases pass, financial/
resource rejected. Puter uses the verified native free-allowance route; no paid
compatible gateway. Gemini/Groq free integrations offer no usable weight-tuning path.
Ollama processes stopped; DeepInfra remains excluded. All seven profiles remain
disabled/unqualified with no normal egress scope. Original three Groq probes and
current nine-call calibration authorizations remain counted; no reset or renewal.
The following metadata/setup table and three-call probe record are historical.

17 October 2026 (Asia/Calcutta). This is the current provider checkpoint following
the user's saved credentials and explicit choice to continue cloud setup while
local testing is deferred. All secrets stay in ignored operator files. No normal
database migration, provider activation, commit/push or Sprint 12 occurred.

| Provider | Observed status | Current inference disposition |
| --- | --- | --- |
| Groq | Saved key verified by authenticated models GET; planned exact model is available | Three fixed synthetic requests made under the user's confirmed free account; no class qualified or normal profile enabled |
| Puter | User confirmed Free plan with billing screenshot; saved token verified through authenticated `/whoami` GET | No AI request. Free native-driver compatibility with strict schemas/caps is unverified; paid-compatible gateway is not used |
| DeepInfra | Saved key verified by documented authenticated billing-checklist GET; API reports balance suspension, no available scoped credits, no payment method and no auto-top-up | No inference request. Disabled; signup alone did not establish usable free inference |
| OpenRouter/Mistral | No credentials provided; transport contracts exist | Disabled; no account requests |
| Existing Gemini | Existing key/confirmation unchanged; not rechecked or rotated in this follow-up | Existing authorization preserved; no new Gemini request |
| Local Ollama | Runtime/model installed from prior setup | User chose cloud setup for now; no local generation or repeated RAM checks |

The read-only checker prints presence/authentication and allowlisted readiness flags.
It never prints tokens, account identity, addresses, payment details or raw bodies.
DeepInfra's [billing checklist](https://docs.deepinfra.com/api-reference/billing/get-checklist)
is the observed source for its balance suspension; no funds, card, top-up or other
billing configuration was changed. There is no DeepInfra inference adapter activated.

Puter's [current quota reference](https://docs.puter.com/rate-limits-and-quotas/)
states that the OpenAI/Anthropic-compatible inference gateways require a paid plan,
while native `puter.ai.*`/`drivers/call` use the account allowance. The screenshot and
token verification establish the user's current Free account/credential, not this
backend's native free-driver compatibility. Do not install a browser SDK, expose the
token to the frontend, choose a paid gateway or upgrade the account as a workaround.

## Groq synthetic transport check

`scripts/smoke_groq_provider.py` accepts only three bundled synthetic cases; no
arbitrary prompts, tenant snapshots or external corpora. Dry-run is the default.
Execution requires a private authorization tied to the exact key hash, model,
account scope and corpus hash. The ordinary model profile remains disabled,
benchmark-only and without tenants/projects/qualified classes.

The operator-only transport probe does not claim production SQL admission. It has
a separate durable per-account ledger/lock: at most three conservative admissions
per rolling day, at most two per logical case, original request/token limits, one
request at a time, 512 output tokens, 22 seconds/request and a 90-second batch.
Known quota cooldown and unknown outcomes stop further calls; invocation/output
changes do not reset counts. Existing model limits and normal app guards stay intact.
Reconcile these setup requests with actual account quota before future activation.

Observed receipts:

- [Preflight](../../../verification/sprint11_1/implementation/groq-smoke-preflight.json): no inference.
- [First request](../../../verification/sprint11_1/implementation/groq-synthetic-smoke.json): configuration rejection, stopped immediately.
- [Second request](../../../verification/sprint11_1/implementation/groq-synthetic-smoke-retry.json): complete JSON, 894 reported input/187 output/53 reasoning tokens, 762 ms; rejected during output/evidence validation.
- [Third request](../../../verification/sprint11_1/implementation/groq-synthetic-missing.json): complete JSON, 897 input/104 output/40 reasoning tokens, 623 ms; rejected because a missing-evidence gap used subject alias `s1` instead of evidence alias `e1`.

These two latencies are individual observations, not p95, cold-start, semantic
accuracy or per-class qualification. The initial supported case's response was not
retained before candidate checkpointing was added; do not infer its precise hard-gate
failure. The final candidate is saved privately without exposing prose/reasoning.

Groq now uses low reasoning for GPT-OSS, with returned reasoning disabled. Strict
cloud schemas type even unreachable empty-array items. Runtime context schemas now
bind exact section/mode and valid evidence/question/basis/subject identifiers before
external decoding; the hard validator remains authoritative. This prevents the
observed subject-versus-evidence gap ambiguity without relaxing any acceptance rule.
The full three-request allowance is consumed. **No further live retest or successful
model-quality/activation claim follows from the offline fix.**

## Remaining work

The final focused offline suite has 110 passes. The current DB receipt and static/
fingerprint checks are linked from [verification](../../../verification/sprint11_1/IMPLEMENTATION.md).
Full independent qualification (12 cases/class, six held out, measured usefulness and
quality gates) remains open. A new bounded retest must respect retained account/case
history and original caps. Puter's free native path remains unimplemented/unqualified;
DeepInfra must remain unavailable while its account reports the balance blocker.
Normal v2/cloud flags stay off. No paid fallback, extra output tokens, account upgrade
or renewed Gemini confirmation is implied.
