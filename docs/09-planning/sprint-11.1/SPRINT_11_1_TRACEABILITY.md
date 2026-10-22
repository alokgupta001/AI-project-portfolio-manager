# Problem → requirement → component → task → acceptance traceability

R IDs are local to this blueprint and supplement the canonical 156-requirement coverage; they do not replace or close that register. Existing F IDs retain their historical acceptance limits.

| ID / problem | Business or technical requirement | Component / decision | Authoritative document | Implementation | Acceptance |
| --- | --- | --- | --- | --- | --- |
| R01 documentation/code mismatch | Repository-specific truth and observed baseline; no invented existing functionality | Discovery, preservation / 01 | DISCOVERY, PLAN | T01,T14 | AT19,AT20 + fresh C1/C4 |
| R02 nine roles share one prompt | Preserve F-040–049 with distinct scope, deterministic services and on-demand AI paths across all nine roles | Registry, goal-aware planner / 02,11 | AGENT_CATALOG, ORCHESTRATION | T02,T07,T09 | AT01 per role,AT02,AT12 |
| R03 domain coupled to provider | Model-independent contracts/config, eligibility before ranking; multiple providers possible | Adapters, registry/router / 03 | PROVIDER_ROUTING, TECHNICAL_CONTRACTS | T02,T04,T05,T06,T13 | AT03,AT04,AT18 |
| R04 key/zero price mistaken for authorization | Default zero spend, provider/account quota scope, no paid fallback or key evasion | Admission/policy ledger / 06 | PROVIDER_ROUTING, SETUP | T03,T04,T06,T13 | AT05,AT03,AT04 |
| R05 shared output/context limits | Preserve requirements under truncation/overflow/large documents without silent limit increases | Context planner, sections / 04 | ORCHESTRATION, VALIDATION_RECOVERY | T04,T07,T10 | AT02,AT04,AT11 |
| R06 persisted run not resumable tasks | Durable section checkpoints, valid transitions, idempotent results and partial success | Tasks, run lease, DB truth / 01,08 | ORCHESTRATION, TECHNICAL_CONTRACTS | T03,T08 | AT06,AT07,AT12 |
| R07 unbounded/ambiguous recovery risk | Bounded retry/fallback/cancel/restart, no repeated unknown spend | Recovery manager / 04,08 | ORCHESTRATION, VALIDATION_RECOVERY | T08,T10 | AT07,AT08,AT11 |
| R08 exact citation mistaken for truth | F-023–025/070–072; deterministic math, semantic review, contradictions and uncertainty | Validator/evaluator/reconciler / 05 | VALIDATION_RECOVERY, AGENT_CATALOG | T02,T09,T10,T12 | AT10,AT12,AT13,AT17 |
| R09 durable/LLM tools may widen access | Organization/project/source/private-assessment isolation, privacy and untrusted text | Evidence/live authority/RLS / 08 | TECHNICAL_CONTRACTS, AGENT_CATALOG | T03,T07,T08,T11 | AT09,AT08,AT14 |
| R10 16 GB hardware constraint | Useful local-only mode, one model/slot, configurable measured small-model profile | Ollama/resource gate / 07 | SETUP, TEST_PLAN | T05,T12,T13 | AT15,AT17,AT18 |
| R11 capability duplication and overreach | Preserve specialist reasoning with canonical calculations; avoid fake causal/sentiment/optimization claims or permanently excluding six roles from AI | Nine hybrid roles, distinct task classes / 02,09,11 | AGENT_CATALOG, RISKS | T02,T07,T09,T12 | AT01,AT02,AT10,AT12,AT13,AT17 |
| R12 changes may break frontend/history | Stable routes/status/replay, independent review and immutable original scores | Compatibility facade/UI / 08 | TECHNICAL_CONTRACTS | T01,T02,T09,T11,T14 | AT16,AT19 |
| R13 simpler alternatives not evaluated | Maintainable student-scale architecture with rationale and traceable decisions | Native bounded DAG / 01–09 | DECISION_LOG | T01,T14 (design review dependency) | AT20/manual alternative matrix |
| R14 opaque execution and private logs | Safe task stages/routes, separate baseline versus AI coverage, no falsely complete deferred interpretation | Events/API/frontend / 01,05,11 | ORCHESTRATION, TECHNICAL_CONTRACTS | T08,T11 | AT12,AT14,AT16 |
| R15 model/free-tier suitability unknown | Separate mocked, local and real authorized-free test modes; no paid smoke | Qualification and policy / 06,07 | TEST_PLAN, SOURCES, SETUP | T12,T13 | AT17,AT18,AT05 |
| R16 context loss and speculative handoff | Fifteen requested artifacts, explicit task status/order, conflict/resumption guide | Documentation package / 09 | IMPLEMENTATION_GUIDE, TRACKER, HANDOVER | T01,T14 | AT20, local link checks |

Document column abbreviations expand to `SPRINT_11_1_<NAME>.md` in this folder; TRACKER is `TASK_TRACKER`. All critical requirements have task and test ownership. Every T01–T14 task maps to at least one row; optional provider/index work is justified by R03/R10/R15, not infrastructure for its own sake.

## User request section coverage

| User section | Blueprint coverage |
| --- | --- |
| 1–4 context, alternatives, discovery | PLAN, DISCOVERY, DECISION_LOG; R01/R10/R13 |
| 5–6 components/nine contracts | ARCHITECTURE, AGENT_CATALOG; R02/R11 |
| 7–8 provider contract/routing | PROVIDER_ROUTING, TECHNICAL_CONTRACTS; R03/R04 |
| 9–10 quantifier/recovery | VALIDATION_RECOVERY; R05/R07/R08 |
| 11 execution lifecycle | ORCHESTRATION; R06/R07 |
| 12 hardware | SETUP, TEST_PLAN, SOURCES; R10/R15 |
| 13 zero spend | PROVIDER_ROUTING, SETUP; R04/R15 |
| 14 security | catalog common contract, routing eligibility, technical RLS, AT09; R09 |
| 15–18 artifacts/precision/traceability/context | README, all technical contracts, IMPLEMENTATION_GUIDE, TRACEABILITY, HANDOVER; R16 |
| 19–21 scope/acceptance/handover | PLAN, TRACKER, HANDOVER, verification evidence; R01/R12/R16 |
