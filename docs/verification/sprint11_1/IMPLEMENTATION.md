# Sprint 11.1 implementation verification

## Current three-provider follow-up

[Guide](../../03-sprints/active/sprint-11.1/CLOUD_SPECIALISTS.md),
[results/review packet](CLOUD_CALIBRATION_RESULTS.md),
[closeout](implementation/cloud-specialists-closeout.json) and
[65 fingerprints](implementation/cloud-specialists-source-fingerprints.json) are current.
26 real synthetic cloud calls: nine current-prompt supported roles pass hard checks;
seven/nine absence cases pass, financial/resource rejected. No held-out or independent
semantic qualification. Native Puter, separate assignment/qualification, role prompts/
examples, strict Gemini fields and prompt-resume fencing implemented. Ollama stopped.
36 original draft examples/export; no training/upload or paid endpoint.

[198 offline](implementation/cloud-specialists-units-closeout.txt),
[101 DB/provider](implementation/cloud-specialists-db-final.txt) and
[37 final prompt-fence DB](implementation/cloud-specialists-prompt-fence-db.txt) pass,
overlapping. [Full backend](implementation/cloud-specialists-backend.txt) lifecycle/
drift passed; 446 tests passed/three cloud context fixtures failed, corrected in final
scopes. No clean full-pass claim. Ruff 170 files, mypy 64 modules, contracts match;
no UI/browser change. [Preservation disposition](implementation/cloud-specialists-preservation-disposition.json)
retains the strict initial snapshot failure: 69 normal table hashes unchanged,
65 original refresh-token rows/session bindings retained, two added/one used flag
consumed. Five objects/24 frozen files unchanged. Normal 0012/HTTP 200; seven profiles
disabled, no tenant scopes, qualification, normal activation or scope sync. AT17 BLOCKED.
Earlier no-cloud/no-native-Puter entries below retain their historical scope.

17 October 2026. This is implementation evidence, separate from historical planning receipts. Source baseline `d0ebe32e691a3d63166ced669450911c63151127`; no commit or normal deployment. Three real fixed-synthetic Groq and four later authorized local Ollama requests are recorded below; application/DB test transports remain intercepted. Isolated DB tests target test/ppm_test, never normal data.

## Authorized small local model setup

[Setup/results](../../03-sprints/active/sprint-11.1/OLLAMA_SMALL.md) records the user's
explicit approval after the hardware discussion. Qwen3 0.6B and native `ppm-small`
preset are installed. Two basic JSON controls passed alongside the normal project;
the actual project risk case and existing one-item replacement both failed unchanged
hard validation. No model qualified, no held-out test ran and no cloud call occurred.
All four outcomes were known complete. Model unload and normal health HTTP 200 passed.

[Final closeout](implementation/qwen06-closeout.json) verifies 57 source fingerprints,
24 frozen files, five disabled profiles, unchanged original profiles and four retained
local admissions; source hashes are [recorded separately](implementation/qwen06-source-fingerprints.json).

Measured server+runner peak 1,138 MiB gives a 1,536 MiB small reservation after 25%
margin/upward rounding, plus unchanged 2,048 MiB headroom. The first control's 88 MiB
server-only sample is explicitly invalid for model-memory claims. Corrected sampler
follows descendants; later controls retain valid host/process measurements. The
benchmark now supports immediate unload while rejecting warm repeats with zero
residency and excluding cold timings from warm statistics. Final
[53 tests passed](implementation/qwen06-final-units.txt), 1.82 s. The launcher syntax
and installed model parameters passed; no runtime/UI/SQL change requires another
full backend/browser run for this operator-only follow-up. Keep failed candidates
and the exhausted two-attempt risk root. Earlier closeouts below are historical.

## Whole-sprint implementation follow-up

The remaining mandatory benchmark code now exists. See [actual workflow](../../03-sprints/active/sprint-11.1/BENCHMARK.md)
and ADR 11.1-14. The 108 synthetic cases cover nine classes, twelve per class/six held
out. Expected labels remain draft and excluded from requests. The local runner
retains attempt/unknown state, fixed call/context/output bounds, digest checks,
sampled host RAM/Ollama working sets and cold/warm/end-to-end telemetry. The separate
scorer binds independent review to report/candidate hashes and cannot activate a model.
Standalone report-checker imports were corrected to match its documented command.

| Check | Observed result | Receipt |
| --- | --- | --- |
| Corpus/control scope | 45 passed, including 36 role/control combinations and all-case context/label isolation | [focused](implementation/benchmark-units-final.txt) |
| Final benchmark/qualification scope | **51 passed**, 5.43 s; includes final residency/output-cap/resource changes and corpus aligned to actual resource/team inputs; synthetic/intercepted only | [final](implementation/benchmark-corpus-release.txt) |
| Full migration lifecycle/backend | All upgrade/downgrade/repeated head/drift checks passed; pytest **422 passed, six fixture errors**, 493.54 s, one inherited warning. All six errors were missing `config/model-policy.example.json` in the old test image. | [full run, retained failure](implementation/backend-completion.txt) |
| Packaged-image correction | Added only the public disabled policy example to the Docker image; build passed. All affected fixtures plus final benchmark/qualification scope: **58 passed**, 2.61 s | [build](implementation/benchmark-image-build.txt), [tests](implementation/benchmark-packaged-tests.txt) |
| Full browser regression | **18 passed**, 4.2 min; one deliberate skip for v2, which needs its separate overlay; identity, agents, AI, assessment, capacity, command, delivery, documents, integrations, pilot, shell and full walkthrough | [browser](implementation/browser-completion.txt) |
| Hybrid browser | **1 passed**, 28.1 s; metrics zero calls, explicit requested unavailable AI, ordered roles, separate coverage, keyboard and desktop/tablet/mobile axe | [hybrid](implementation/browser-hybrid-completion.txt) |
| Offline preparation | 108 cases prepared in four explicit groups, zero model/network calls; no fabricated review/ratings; current corpus supersedes the retained first draft | [group 1](benchmarks/current/prepared-1.json), [2](benchmarks/current/prepared-2.json), [3](benchmarks/current/prepared-3.json), [4](benchmarks/current/prepared-4.json), [review draft](benchmarks/current/independent-review-template.json) |
| Fresh normal preservation | Normal 0012, all 70 table counts/hashes, five original object hashes and 24 frozen files unchanged | [preservation](implementation/completion-preservation.txt) |

Counts overlap; **no uninterrupted 428-pass full run is claimed**. The six setup
errors were fixed by the image packaging change and all affected tests passed in the
rebuilt image. Existing full-suite passes remain evidence for unaffected behavior;
the final focused scopes cover subsequent benchmark-only refinements. No product
security, scoring or SQL behavior was weakened to pass tests.

Visual inspection of fresh desktop/mobile screenshots found the legacy specialist
table's default limitation label could claim cited support for an unavailable role.
The default now distinguishes supported results, canonical fallback and unavailable
interpretation. Web type/lint/format checks pass after this copy correction. The
full browser receipt above precedes that final copy-only change.

The final hybrid journey passed again after the label correction: **1 passed, 28.8 s**,
[receipt](implementation/browser-hybrid-release.txt). Desktop/mobile screenshots were
visually inspected and all three viewport captures retained privately with hashes.
The [completion closeout](implementation/completion-closeout.json) verifies 55 final
source/config/test/image fingerprints, 24 frozen files, current corpus/prepared hashes,
four disabled profiles and all three original Groq admissions. Ruff 164 files, mypy 62
modules and web type/lint/format/contracts pass. Normal loopback readiness returned
HTTP 200. No new live provider request or local generation occurred.

Local generation remains user-deferred. The previous measured insufficient RAM is
retained as a hardware blocker, without remeasuring or loading a model in this pass.
Independent label approval and real per-class quality/latency/memory remain absent.
AT17 is BLOCKED; no model is qualified. Optional cloud benchmark/native Puter driver/
embeddings remain disabled with documented disposition. Normal rollout stays outside
this implementation checkpoint, as the guide specifies. Earlier entries below are
historical checkpoints, including their statements that the runner did not yet exist.

## Current cloud credentials and decoder follow-up

[Provider status](../../03-sprints/active/sprint-11.1/CLOUD_PROVIDER_STATUS.md) is current. Groq/Puter/DeepInfra keys passed authenticated metadata GETs. DeepInfra returned balance suspension/no scoped credit/no payment method/no top-up; it received no inference request. User confirmed Puter Free with screenshot; no Puter AI call or paid-compatible route. User deferred local testing and has not supplied OpenRouter/Mistral credentials.

Groq's original three-request synthetic allowance was consumed: [configuration rejection](implementation/groq-synthetic-smoke.json), [complete but hard-rejected supported case](implementation/groq-synthetic-smoke-retry.json), [complete but hard-rejected missing case](implementation/groq-synthetic-missing.json). Missing case's saved private structure used `s1` for an evidence gap, while only `e1` was valid. Runtime decoder schemas now bind exact section/mode/aliases, with unchanged hard validators. Strict cloud empty arrays have typed unreachable items, and Groq suppresses returned reasoning with low effort for GPT-OSS. No post-fix real retest or successful class qualification is claimed.

[110 focused offline tests passed](implementation/cloud-credentials-units-final.txt), including setup privacy, fixed GET endpoints, durable smoke account/case/cooldown/unknown bounds and alias binding. Python static checks pass for 161 files/62 modules. Full corpus qualification, native Puter free-driver support and normal activation remain open. The synthetic operator probe is not production SQL admission or a full independent benchmark; reconcile its retained usage with account limits before activation.

[16 isolated DB regressions passed](implementation/runtime-cloud-schema-final.txt), 73.28 s, after decoder identity binding. This supersedes the earlier 16-case provider checkpoint for the context-schema change. No full-suite/browser rerun is claimed for unchanged legacy/UI scope.

[Final cloud closeout](implementation/cloud-closeout.json): 50 source fingerprints/24 frozen files match, four candidates disabled, all three Groq admissions retained. Ruff 161 files/mypy 62 modules and generated inventories/contracts pass; documentation audit checked 343 Markdown files/5122 links before these final receipt links. Normal revision remains 0012 and health HTTP 200. Existing normal data was not the target of any mutation in this follow-up.

## Prior provider/local setup checkpoint

User selected Groq, OpenRouter and Mistral AI and confirmed free-tier accounts. [Setup guide](../../03-sprints/active/sprint-11.1/PROVIDER_SETUP.md) records private key entry and all activation gates. New adapters preserve the existing limits, qualification, scope and shared SQL accounting. No actual cloud authentication or inference request occurred; the new key fields remain empty.

| Check | Observed result | Receipt |
| --- | --- | --- |
| Focused provider/hybrid/setup offline scope | **103 passed**, 3.46 s; synthetic keys/intercepted HTTP, no real model calls | [offline](implementation/unit-providers-setup-final.txt) |
| Final readiness refinement | **6 passed**, 0.22 s, after the installed-digest guard and standalone CLI adjustment; overlaps the 103-case scope | [readiness controls](implementation/readiness-release.txt) |
| V2 DB provider/runtime regression | **16 passed**, 101.69 s; real ppm_test SQL admission/daily exhaustion for three new providers plus prior runtime/fencing cases | [DB](implementation/runtime-providers-setup-final.txt) |
| Ollama installation | Official 0.40.5 WinGet install, installer hash verified; binary fingerprint recorded | [installation](implementation/ollama-installed.json) |
| Local model inventory/readiness | Qwen3 4B Q4_K_M installed digest; 1261 MiB host available vs 6144 MiB gate; exit 1 LOCAL_RESOURCE is expected; no inference | [fresh readiness](implementation/local-readiness-installed.json) |
| Native and Docker endpoint | Native version/empty residency and Docker API container → host.docker.internal:11434 version 0.40.5 passed; bound to loopback | [installation](implementation/ollama-installed.json) |
| Final static/integrity checks | Ruff 159 files, mypy 62 modules, contracts/inventories match; 48 source fingerprints and 24 frozen files match; four private candidates disabled; normal readiness HTTP 200 | [closeout](implementation/setup-closeout.json) |

The first new quota test had an outdated partial-success expectation when no useful canonical baseline survived. Corrected expected status to failed; no product behavior was weakened. Its failed receipt is retained. The normal database read confirms 0012. No migration/dependency/browser/UI change occurred in this follow-up. Existing full-suite/lifecycle/browser receipts below describe their earlier source checkpoint; the focused follow-up supersedes provider/setup behavior without claiming a fresh full-suite run.

## Earlier core verification

| Check | Observed result | Receipt |
| --- | --- | --- |
| Preservation and fresh pre-edit baseline | Private files/DB/object backup; 148 passed, one skipped, 108 excluded; contracts match | [baseline](implementation-baseline.md) |
| First isolated storage/lifecycle checkpoint | 272 passed; all lifecycle directions/repeated head/drift passed | [storage baseline](implementation/storage-baseline.txt) |
| First four v2 DB cases | 4 passed after correcting analysis-parent insertion before task RLS dependency reads | [focused integration](implementation/runtime-integration2.txt) |
| Final focused unit cases | **52 passed**; contracts, scoped context, truthful baseline coverage, canonical numeric contradiction gates, no ambiguous replay, critique withdrawal, intercepted Ollama/Gemini, explicit egress/legacy-dispatch isolation/daily ceiling and qualification arithmetic | [units](implementation/unit-account-final.txt) |
| Intermediate full backend | 305 passed; one inherited Starlette/httpx deprecation warning; lifecycle/drift passed | [checkpoint](implementation/backend-final1.txt) |
| Full backend checkpoint | **314 passed**, one inherited warning, 499.63 s; upgrade/downgrade/base/repeated-head/drift all passed. Final focused scopes below cover subsequent v2 hardening. | [full regression](implementation/backend-final.txt) |
| Final v2 integration | **13 passed**, 59.15 s; includes no-duplicate resume, strict repair, unknown quarantine, global host slot, cross-tenant task denial and cancel/lease/member/source fencing | [final runtime](implementation/runtime-release-final.txt) |
| V2 browser | **Passed**, 33.1 s; desktop/tablet/mobile axe, keyboard/table scrolling, zero-call metrics, explicit unavailable interpretation and final model/polling metadata; previous failures retained | [browser](implementation/browser-v2-final.txt) |
| Legacy specialist browser | Passed in 38.9 s; persistent independent review, source evidence, discrepancies/privacy and disabled-provider fallback | [legacy browser](implementation/browser-legacy.txt) |
| Web contracts/typecheck/lint/format | Passed | [web](implementation/static-web.txt) |
| Python ruff/format | Passed; mypy 61 modules passed | [static](implementation/ruff-final.txt), [mypy](implementation/mypy-final.txt) |
| npm vulnerability audit | 0 vulnerabilities after elevated read-only retry; sandbox DNS failed first | [audit](implementation/npm-audit-elevated.txt) |

Counts overlap and are not additive. The full-suite checkpoint preceded final v2-only hardening; the complete final 52-unit/13-integration scopes cover that final source, without repeating unchanged legacy tests. Failed/intermediate attempts remain evidence, not final acceptance. `backend-final2.txt` records an old development SQL signature in the disposable DB. `backend-final3.txt` was stopped after a concurrency-fixture initialization failure; the corrected case passed in the full/focused final scopes. Final focused failures retained a repair-context overflow (fixed with compact equivalent instructions, without raising limits) and an outdated partial-success expectation for a semantic-only unknown run. Such a run now fails when no canonical result survives. Stopped synthetic attempts were explicitly released by the test owner without removing quota history; no normal schema/data was involved.

## Real-model gate

Installed Ollama/model digest and private Docker reachability are recorded; user deferred local testing. Independent labels, broad inference measurements and class qualification remain missing. The three-request Groq probe is not the complete benchmark runner. T12 remains BLOCKED and the report checker never activates profiles. Current credential/account status is above; no model is qualified. Puter native free-driver support and local embeddings remain deferred/unverified. No broad accuracy claim follows from mocks, metadata or these rejected synthetic responses.

## Final preservation and fingerprints

PASS: normal remains 0012; all 70 established table counts/hashes, five original object keys/byte hashes and 24 frozen `.env`/source/prompt/migration hashes match the private pre-implementation checkpoint. See [preservation-after](implementation/preservation-after.txt) and [source fingerprints](implementation/source-fingerprints.json). Public receipts contain no raw source prompts, credentials, reasoning text or private backups.
