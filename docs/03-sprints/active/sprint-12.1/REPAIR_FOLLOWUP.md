# Sprint 12.1 timing repair follow-up

Started 27 October, resumed 28 October 2026 after a tool approval-review usage-limit
interruption. This is the separately authorized repair of the stopped ce874a14
experiment, not Sprint 13. No live repair call occurred before that interruption.

## Verified defect and bounded repair

`agent_runtime.complete_task` discarded timing whenever the adapter produced no
ModelResult, writing zero to the call ledger. The repair records monotonic elapsed
time before settlement on that path, including cancellation. Unknown provider
outcomes, unknown token usage, quota reservations and cancellation propagation are
preserved. No historical call row is backfilled. UI/API/downloads distinguish
unavailable attempt elapsed time from accepted-response latency. Only accepted
cases contribute to fixture p95 and match counts.

The adapter records allowlisted HTTP timing milestone offsets and discards all
trace info. Worker events carry only attempt ID, version, outcome and timing.
New bindings record `attempt-elapsed-v2` and effective timeout. Model, prompt,
corpus, labels, output cap, 22-second deadline and 20-second acceptance gate remain
unchanged. No speculative optimization, model swap, tuning or retry was added.

## Initial diagnostic evidence

Application services were stopped at the initial checkpoint and restarted with
existing provider configuration. That does not establish the earlier timeout cause.
Two credential-free, non-inference GET probes from the worker to the Gemini origin
completed in 270 ms and 228 ms (HTTP 404 for `/`). TCP/TLS completed promptly on
those probes; they do not measure model generation or inference performance.

Official references checked: [Gemini 3.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite)
and [HTTPX trace extensions](https://www.python-httpx.org/advanced/extensions/).
The request already uses minimal thinking and structured output. Trace diagnostics
use the locked HTTPX/httpcore HTTP/1.1 event vocabulary.

## Preservation and evidence

Before edits: binary diff, 202 changed/untracked file copies and hashes, normal schema
`0019_selection_pilot`, access/ledger hashes and private configuration fingerprints
were captured under ignored `artifacts/local/sprint12_1/repair/`. The 19 applied
migrations are frozen. Prior receipts and older unrelated artifacts remain historical
evidence. The new browser runner preserves prior screenshots byte-for-byte.

## Fresh software validation

- Full guarded backend: **566 passed, 1 skipped, 1 inherited Starlette warning;
  907.43 seconds**. Disposable 0019 → 0006 → 0019 → base → 0019 → 0019 lifecycle
  and schema drift checks passed. Normal database stayed at 0019.
- Focused runtime/pilot/timing: **40 passed, 290.39 seconds**, overlapping the full
  suite. Tests retain timeout and cancellation elapsed time, unknown accounting,
  cancellation propagation, legacy-zero handling and p95 exclusion. Existing
  replay/order/pacing, explicit grant, cross-tenant and revoked authority tests pass.
- Two browser journeys: **2 passed, 45.9 seconds**, including a real isolated
  API human-review/unavailable flow and explicitly mocked automated timing/report
  presentation. Zero Axe violations and page overflow at 360/768/1440 pixels.
  Screenshots were inspected; result text now wraps within the scrolling table.
- Python lint/format/types, source preservation, generated OpenAPI/TypeScript,
  ESLint, app/browser types, Prettier and three new tooling tests passed.
- Repaired API/worker/dispatcher/migrate/test images and final web image built.
  Prior-sprint documentation: 13 packages / 115 artifacts passed. Inventories
  refreshed. Full tests/builds finished before live inference began.

The new repository `check:static` and artifact-preserving browser runner were used.
The Browser plugin was not available, so isolated QA used repository Playwright;
the actual owner session used the available in-app computer-use browser. The normal
page identity, meaningful content, lack of framework overlay and clean console were
observed, as were preparation and automated-audit state changes.

[Validation receipt](../../../verification/sprint12_1/repair/validation.json) ·
[mocked responsive screenshots and live evidence](../../../verification/sprint12_1/repair/README.md).
Historical 562-test results remain in the earlier report and are not counted here.

## Authorized repair experiment

The exact [scope](../../../09-planning/sprint-12.1/REPAIR_SCOPE.md) permits only
pilot **3f0f3a7f-99c6-57f7-896b-205f9a54f0db**. API and worker both verified the
one-ID allowlist and 22-second timeout. The original stopped pilot is unchanged.
Preparation and the 12-label exact arithmetic audit were recorded through the
normal Ashu session, revision 2, no calls yet and human_reviewed=false.
Normal API/worker/web CPU samples immediately before inference were 0.17%, 0.26%
and 0.00%; no test container or build was running. These samples do not establish
historical load or rule out transient contention during a call.

## Final live result — 28 October 2026

The authorized experiment stopped at its first unavailable attempt. No further
case, retry or replacement experiment was started. Calls used the normal UI,
jobs and shared SQL admission. The downloaded report and ledger agree:

| Case | Outcome | Response latency / unavailable elapsed |
| --- | --- | --- |
| f01 | Exact match, o1 | 1,833 ms response |
| f02 | Correct abstention | 981 ms response |
| f03 | Exact match, o1 | 7,936 ms response |
| f04 | Exact match, o2 | 7,404 ms response |
| f05 | Exact match, o1 and o2 | 7,437 ms response |
| f06 | TIMEOUT; outcome and usage unknown | **22,037 ms unavailable elapsed** |
| f07–f12 | Not attempted | Not measured |

State is **insufficient_data**: five measured exact matches, one unavailable,
six unattempted, zero held-out cases measured. Accepted-response p95 is 7,936 ms;
the timeout is excluded from that metric, not treated as a fast or successful
response. The twelve-case fixture gate did **not** pass. This small synthetic
result does not establish broader accuracy; **AT17 remains BLOCKED** and
human_reviewed remains false. Results are not pooled with the original pilot.

Every call had one attempt and one 128-output-token reservation. All start gaps
exceeded 60 seconds. The interrupted session left an approximately eighteen-hour
gap between f02 and f03; this was the same frozen experiment resumed without tuning.
Application charge was $0; external provider billing was not independently checked.
Unknown quota/usage from f06 is preserved. The next-case button is disabled.

## What the timing evidence establishes

The lost failure elapsed-time defect is verified and fixed in an actual failure:
f06 now retains 22,037 ms in the ledger, UI and report. Job creation to call
admission was 7.149 seconds, followed by 22.073 seconds from call start to
settlement. The first interval includes dispatch/preparation and must not be
reported as measured queue time alone or combined with response latency.

Available sanitized transport events cover **f01 and f02 only (2/6 attempts)**.
For those two calls, TCP/TLS/send completed by 123 ms and 60 ms respectively;
response headers arrived at 1,832 ms and 980 ms. Most elapsed time in these two
calls was response waiting. Client observations cannot separate provider compute
from network transit.

Transport events for f03–f06 were not recovered from the inspected local logs
after service restart, although their durable call results and elapsed times are
present. Consequently the exact stage/cause of f06's timeout, and the earlier
pilot's slowness, remain **unresolved**. Neither provider-side delay nor local
contention has been established as the cause. This logging coverage gap is an
explicit diagnostic limitation; no speculative request change or additional live
experiment was used to conceal it. Future authorized diagnostics should verify
event capture after restart before inference, using mocked/disabled providers first.

## Closeout and preservation — 29 October 2026

Documentation closeout resumed after the tool interruption. No additional model
calls were authorized or made during closeout. The existing local services were
restarted for read-only UI verification with their saved scoped configuration.
The saved f06 run opened with its usable rules-only checklist, and the pilot still
displayed the timeout, disabled f07 and insufficient-data summary. No console
errors or warnings were observed. A fresh read-only snapshot verified normal 0019
and all seven ledger/access tables unchanged since the stop: zero additional calls.
[Closeout receipt](../../../verification/sprint12_1/repair/closeout.json).

[Preservation receipt](../../../verification/sprint12_1/repair/preservation.json)
confirms all 144 protected file hashes match, including frozen migrations, private
configuration, prior evidence and the additional tooling. Existing memberships,
project/guided grants and historical call/reservation/pilot rows are unchanged.
Calls and reservations increased only from six to twelve; the second pilot is the
single authorized repair experiment. Normal schema remains 0019. No ledger reset,
access expansion, commit, PR, push, deployment or Sprint 13 work occurred.

The software repair is locally validated. Live fixture acceptance remains unmet;
broad model quality is unverified. Preserve both stopped experiments. Any later
experiment requires separate authorization and must retain the same honest
distinction between software checks, synthetic selection evidence and real outcomes.

[Actual downloaded report](../../../verification/sprint12_1/repair/live-pilot-report.json) ·
[Call/quota and timing receipt](../../../verification/sprint12_1/repair/live-evidence.json) ·
[Evidence index](../../../verification/sprint12_1/repair/README.md).
