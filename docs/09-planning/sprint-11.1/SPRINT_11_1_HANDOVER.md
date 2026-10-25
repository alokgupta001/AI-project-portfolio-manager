# Handover to GPT-6.1 Sol

**Current disposition — 25 October 2026:** Sprint 11/11.1 is complete for the
local guided-sample scope; Sprint 12 local foundations are ready to start, not yet
implemented. Broad AI accuracy **AT17 remains BLOCKED**. Normal schema is 0016;
Gemini/Puter/Groq guided access covers the two approved projects with shared
50/day provider ceilings. See [the closeout](../../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md) and
[reconciled plan](../LOCAL_SAMPLE_PLAN_UPDATE.md) for evidence, current scope and the Sprint 12 prompt.
This supersedes older runtime/rollout/stop statements below; dated test results
and original full-product acceptance requirements remain unchanged.

Planning date 17 October 2026. Source inspected: `d0ebe32e691a3d63166ced669450911c63151127`. The subsequent implementation request has arrived. Resume from the [implementation handoff](../../03-sprints/active/sprint-11.1/HANDOFF.md) and tracker; the planning instructions below describe the original starting checkpoint. Do not advance Sprint 12 automatically.

## Read in this order

1. Current repository instructions and `docs/handoffs/LATEST.md`, then this document and [index](README.md).
2. [Discovery](SPRINT_11_1_DISCOVERY.md) and [fresh verification](../../verification/sprint11_1/README.md); inspect diff since source baseline.
3. [Architecture](SPRINT_11_1_ARCHITECTURE.md) and [decisions](SPRINT_11_1_DECISION_LOG.md).
4. [Technical contracts](SPRINT_11_1_TECHNICAL_CONTRACTS.md), [catalog](SPRINT_11_1_AGENT_CATALOG.md), [routing](SPRINT_11_1_PROVIDER_ROUTING.md), [orchestration](SPRINT_11_1_ORCHESTRATION.md), [validation](SPRINT_11_1_VALIDATION_RECOVERY.md).
5. [Implementation guide](SPRINT_11_1_IMPLEMENTATION_GUIDE.md), [test plan](SPRINT_11_1_TEST_PLAN.md), [tracker](SPRINT_11_1_TASK_TRACKER.md), [traceability](SPRINT_11_1_TRACEABILITY.md), setup/risks/sources as relevant.

Authority: schema definitions in technical contracts; state/call/time bounds in orchestration; policy authorization in routing; acceptance in validation/test plan. If they conflict, document and reconcile before coding affected behavior. User instructions supersede historical stop points and this blueprint, but do not infer permission for live spend or normal data mutation.

## Selected design

Extend existing FastAPI/PostgreSQL/Celery modular monolith with deterministic bounded DAG and task/section checkpoints. Preserve financial, schedule, sentiment, risk, resource, governance, agile_coach, pmo, executive IDs. All nine roles combine deterministic services with optional qualified AI reasoning. Python owns calculations/scoring/privacy/reconciliation; models may interpret domain evidence, synthesize portfolio implications and produce executive explanations. Sentiment retains its permitted aggregate-only support boundary. Validator is layered deterministic checks plus optional semantic critique.

Hybrid-role revision, ADR 11.1-11, supersedes the initial permanent role split. Implement each role's interpretation handler/task class and triggers, `analysis_mode`, ordered requested_agents, separate base/semantic coverage, synthesis basis aliases and reserved PMO/Executive slots. Do not hardcode inference to risk/governance/agile. At most three initial sections may be drawn from any eligible roles; requesting all nine interpretations may still produce partial work under the unchanged caps. A Python fallback cannot be labeled completed requested AI interpretation.

Providers are independent of business capabilities. Local Ollama is an inference runtime under a single shared host slot. Hybrid routes filter authority, egress, zero-spend tier, capability, quality, context, quota and health before ranking. Gemini existing binding remains; second provider is optional and disabled until specifically qualified. No paid fallback. Persist requirements/evidence/config hashes and validated sections; never replay unknown external outcomes silently after worker crash.

## Decisions not to silently change

- Four admitted attempts/run, two/logical section, 512 output tokens/attempt, 90 s run deadline, 24 nodes, one local generation. No reset through child task or implicit new run.
- Existing metric/scoring rules, privacy/group-five suppression, session/project/assessment/RLS boundaries, independent append-only human review and original/suggested/approved score separation.
- Immutable existing migrations/old results/review keys; new additive successor, default-off v2. Normal historical runtime 0012 versus source 0014 must be checked, never guessed.
- Non-expiring credential-bound Gemini confirmation preserved; new billing/model/account events invalidate eligibility; cloud disabled by default and no zero-price fiction.
- Untrusted documents/model output cannot authorize tools, scope, money, mutations or provider selection. No thought text in events/logs.
- Valid spans are not semantic proof; disagreement and unknown data stay visible. No full-assessment success from partial question coverage.
- All nine roles support on-demand interpretation; call eligibility depends on evidence, goal, qualification and policy. Preserve distinct baseline/semantic outcomes and coverage. Metrics-only work makes no model calls; requested synthesis receives a planned slot or explicit deferral.

Configurable: model digest, qualified per-task routing priority, endpoint profile, measured memory envelope, quota caps/data-egress policies and optional embedding/Groq enablement. Changing invariant limits requires evidence and documented decision, not a hidden recovery workaround.

## First implementation task and baseline

**T01**: establish current Git/source/migration/runtime preservation baseline and isolated test environment. Fresh planning tests: 148 offline passed, one skipped, 108 excluded; focused AI set 85 passed overlaps. Source inventories and generated contracts matched during planning. Full DB/browser tests and model benchmarks were not executed here. Existing normal containers reported healthy, which does not establish current source deployment.

Inspect `.env`/secrets only through safe configuration checks without printing values. Do not bootstrap, rebuild normal services, run normal migrations, call provider smoke or regenerate credentials merely to start. C1/C4 are safe immediate checks; future C2/C3 require disposable fixtures. Read preservation scripts before executing them. Actual source head may have advanced; record that fact rather than overwriting other work.

## Tracker and context-loss protocol

At task start set IN_PROGRESS with selected slice and current source hash. Before stopping write modified files, checks/results, unresolved failure and exact next command in tracker/receipt. IMPLEMENTED means code exists; VERIFIED means acceptance observed. Save failed attempts too. No model quality VERIFIED based only on mocks. No production claim based on local tests.

On resume read tracker, latest task receipt, relevant contracts and Git diff. Continue the next unfinished step; do not repeat entire discovery or already-passing unchanged tests. If a source contradiction is found, stop affected edits, record evidence path/symbol/test and proposed correction under a new decision-log entry, update dependent contract/task/test rows, then continue unaffected work. Do not blindly implement an invalid blueprint or casually redesign the whole runtime.

## Remaining qualification decisions

Actual local model latency/quality/memory/digest, Ollama installation and Docker reachability, normal DB revision, account-specific free-tier quotas and egress approval, optional embedding dimensions/quality and second-provider model selection. Defaults are fail-closed/local keyword/deterministic mode. Core orchestration and schemas are specified; these are bounded operational qualification gates. [Risks](SPRINT_11_1_RISKS.md) provides evidence needed and revisit conditions.

Next owner outcome: implement T01–T14 incrementally, keep the application runnable with v2 off until integration gates pass, and hand back observed verification plus explicit unverified external/hardware gates. Do not mark deployment or later sprints complete.
