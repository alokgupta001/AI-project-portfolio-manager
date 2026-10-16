# Complete future sprint roadmap

Execution update, 16 October 2026: Sprint 09 is locally verified and Sprint 10 is implemented at `0012_ai_runtime`;
[current handoff](../03-sprints/active/sprint-10/HANDOFF.md) governs continuation.
Development Gmail and bounded Gemini free-tier smoke are verified; general model quality, CI/Word
and production gates remain open. Sprints 11–23 remain PLANNED; stop before 11. Proposed paths in later
sections remain plans. Historical planning-date statements below are retained as context.

**Execution update 2026-10-09:** Sprint 8.1 local implementation is recorded in the [report](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md); parent acceptance remains OPEN. The planning baseline below is historical. Future task scope and release criteria remain unchanged; no next sprint was started.

**Historical planning baseline (before Sprint 8.1 execution):** 9 October 2026. Documentation only; no feature work is authorized by this pack.** Sprint 08 is complete locally; Sprint 8.1 is proposed, not started. Numbers describe execution order, not dates or delivery promises. The frozen source specifications and original prompt pack remain intact. For future work, this pack supersedes the earlier gap review and the future sections of the original ordered prompts; those prompts remain historical scope evidence. Completed reports retain their original meaning.

Read the [audit](SPRINT_8_1_GAP_AUDIT.md), [Sprint 8.1 plan](SPRINT_8_1_PLAN.md), [future roadmap](FUTURE_SPRINT_ROADMAP.md), [traceability](FEATURE_GAP_TRACEABILITY.md), and [release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) together. A later implementation session must read the latest handoff and current working tree before using these plans.

## Preserved history and execution rules

Sprints 00–08 are history: requirements/architecture, foundation, identity, shell, delivery, capacity, assessments, command center, and durable jobs/imports. Reports and applied migration files are unchanged by this pack. Their local acceptance does not imply production or AI-complete status.

The original four phases are retained in concrete order: operational foundation (00–8.1); evidence/intelligence and forecasting (09–14); workflows and enterprise decision capabilities (15–20); communication, access hardening and release (21–23). All original future functional scope remains required for full product release. This roadmap supersedes future execution order in the preserved original prompt pack without changing its hash.

For each task: read source requirement acceptance and current module contracts; inspect latest tree; define interfaces before migrations; implement a vertical UI/API/data slice; run positive/negative/failure tests; record exact evidence; update report/handoff/coverage. Task IDs are unique across the pack. Paths marked proposed are not current implementation claims. Database ownership remains PostgreSQL; graph/vector/search are derived views with permission revalidation. Reuse jobs/outbox, metrics and role model.

Documentation acceptance follows [the shared sprint checklist](SPRINT_DOCUMENTATION_CHECKLIST.md). No sprint closes solely because code exists. Missing provider credentials may allow fixture acceptance of a slice, but the real-provider capability remains BLOCKED. A dependent sprint can start only against a verified interface or clearly disabled fallback, never invented results. Full release requires closing outstanding required environment/model acceptance.

## Sequence

| Sprint | Phase | Main user result | Entry prerequisites |
| --- | --- | --- | --- |
| 8.1 | Operational completion | Create/join organization and use complete core screens | Local 08; current evidence |
| 09 | Evidence and intelligence | Document evidence and governance foundation | 8.1; completed 08 |
| 10 | Evidence and intelligence | Shared AI gateway and evaluation | 09 keyword/source contracts; 08 jobs |
| 11 | Evidence and intelligence | Nine agents, semantic assessments and recommendations | 06,07,09,10 |
| 12 | Evidence and intelligence | Connector reliability and historical model foundations | 05,08,11; 8.1 metadata |
| 13 | Evidence and intelligence | Eligible forecasts and uncertainty views | 12; shared 07 metrics |
| 14 | Evidence and intelligence | Project-aware copilot and analytics | 09,10,11; 8.1 metadata; 13 forecast eligibility contract |
| 15 | Enterprise decisions | Approvals, reminders and assessment follow-through | 08,11; 14 draft contract; 8.1 inbox |
| 16 | Enterprise decisions | Transformation plans and decision tracking | 06,09,11,14,15 |
| 17 | Enterprise decisions | Time Machine resource and budget simulation | 05,07,13 eligibility contract,15 |
| 18 | Enterprise decisions | Knowledge graph and impact tracing | 04,05,09,11; 08 outbox |
| 19 | Enterprise decisions | Comparable internal benchmarks | 06,07,13 contracts; 8.1 metadata/paging |
| 20 | Enterprise decisions | Meeting intelligence and actions | 09,10,15 |
| 21 | Release completion | Reports, alerts and daily executive briefing | 08,11,13 contracts,15; shared 07 metrics |
| 22 | Release completion | Passkeys and all-surface account protection | 02 and all protected feature surfaces through 21 |
| 23 | Release completion | Integrated release, recovery and deployment | 8.1 and all 09–22 acceptance; all original requirement evidence |

## Sprint 8.1

The ten individually specified work packages and completion gate are in [SPRINT_8_1_PLAN.md](SPRINT_8_1_PLAN.md); they are part of this sequence, not an independent alternative backlog.

## Sprint 09 — Document evidence and governance foundation

**State:** implemented and verified locally on 15 October 2026 for the revised 09 slice; [report](../03-sprints/completed/sprint-09/SPRINT_REPORT.md) / [checks](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md). **Phase:** Evidence and intelligence. **Entry dependencies:** existing 8.1 interfaces and completed 08; earlier 8.1 parent CI/Word acceptance remains open. Original acceptance below is retained; 10/11 extensions remain planned.

**Goal / why now:** Users need safe reusable source documents before intelligence can make supported claims.

**User outcome:** Versioned library and evidence links; Keyword retrieval and semantic-ready contracts; Policy registry, retention and pilot recovery.

**Existing foundations:** evidence R plus A/J storage and jobs. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-09-001 — Versioned library and evidence links

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 8.1; completed 08.

**Change and user benefit:** PDF/DOCX/text, scanned PDF/images OCR and CSV/XLSX parsing; SRS/BRD/PRD/MOM/sprint report/risk log/charter/policy categories. Size/format bounds, malware quarantine, signed authorized downloads, processing jobs, hashes, versions, page/paragraph/sheet locations, confidence. Link assessment attachments to reusable documents without rewriting scores.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/documents.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/documents/` and `apps/web/components/documents.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `documents` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Text and scanned fixtures, Word/table fixtures, duplicates, corrupt/oversized files, malicious content, changed access and cancelled jobs; browser upload/progress/preview/source links.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-09-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-09-002 — Keyword retrieval and semantic-ready contracts

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 8.1; completed 08; PPM-09-001 interfaces.

**Change and user benefit:** Versioned chunking and a tenant/project-filtered keyword index; hybrid retrieval/embedding interface with semantic mode explicitly pending 10. Revalidate citations on read; label no semantic findings yet. Baseline retrieval evaluation on labeled fixtures.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/documents.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/documents/` and `apps/web/components/documents.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `documents` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Authorized expected source locations rank correctly; revoked/deleted sources never retrieve; changed version and reprocessing produce no duplicate active chunks; no fabricated citation.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-09-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-09-003 — Policy registry, retention and pilot recovery

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 8.1; completed 08; PPM-09-001 and PPM-09-002 interfaces/results.

**Change and user benefit:** Policy owner, applicability, version, effective/review dates and current/draft state; approvals integrated later in 15. Define quarantine/retention/legal-hold policy, safe orphan purge and derived-data invalidation. Snapshot and restore pilot database plus object files to isolated scratch targets with manifest comparison.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/documents.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/documents/` and `apps/web/components/documents.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `documents` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Admin scoped policy edit and PM read; expired/superseded policy labels; deletion revokes access immediately and purge respects holds; scratch restore reproduces counts/hashes and signed download access.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-09-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Parser/OCR availability, malware-scanner choice and real object storage may block live acceptance; fixture-only checks must be labeled.

**Exclusions:** No production semantic extraction or AI score; no general workflow engine; no destructive cleanup of existing evidence.

**Next-sprint entry:** 10 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 10 — Shared AI gateway and evaluation

**State:** local implementation and bounded Gemini free-tier completion/embedding smoke VERIFIED; broader model/retrieval quality and release acceptance OPEN. **Phase:** Evidence and intelligence. **Entry dependencies:** 09 keyword/source contracts; 08 jobs.

**Goal / why now:** One controlled runtime prevents separate agents from inventing facts, costs or authorization rules.

**User outcome:** Providers, embeddings and limits; Typed orchestration and protected tools; AI operations and evaluation gates.

**Existing foundations:** evidence R plus J durable run events and 09 sources. These already exist where identified in the audit; the source and evidence paths below are now implemented locally; bounded Gemini smoke passed; broader quality remains unverified.

### PPM-10-001 — Providers, embeddings and limits

**Status:** implemented and verified locally; bounded Gemini smoke passed; broader quality/scale unverified. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09 keyword/source contracts; 08 jobs.

**Change and user benefit:** One configured completion/embedding provider, disabled states and test doubles; version prompts/model/tool schemas, run input snapshots/evidence, redacted diagnostics, cost/token/latency tracking, per-tenant budgets/concurrency/deadlines/retry/circuit breaker. Activate budgeted hybrid retrieval through 09 interface.

| Implementation concern | Required work |
| --- | --- |
| Backend | Implemented module `services/api/ppm_api/ai.py` with scoped provider/retrieval/schema/evaluation modules; extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Implemented `apps/web/app/ai/` and `apps/web/components/ai.tsx` using the existing shell/transport. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `ai` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Configured provider smoke records actual results; fixtures separately cover quota/timeout/malformed JSON/embedding error; overspend bounded and citations revalidated after access change.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-10-001.md` (executed evidence is in the active Sprint 10 report), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-10-002 — Typed orchestration and protected tools

**Status:** accepted locally for typed tools, cancellation, replay, partial aggregation and authorized progress. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09 keyword/source contracts; 08 jobs; PPM-10-001 interfaces.

**Change and user benefit:** Bounded graph fan-out, cancellation/partial aggregation and independently authorized allowlisted tools. Retrieved text cannot choose arbitrary tools or scope. Emit observable progress, concise evidence/rationale, not private model reasoning.

| Implementation concern | Required work |
| --- | --- |
| Backend | Implemented module `services/api/ppm_api/ai.py` with scoped provider/retrieval/schema/evaluation modules; extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Implemented `apps/web/app/ai/` and `apps/web/components/ai.tsx` using the existing shell/transport. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `ai` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Injection/foreign ID/tool escalation fixtures rejected; cancellation/replay and one failed branch produce truthful states; no unauthorized mutation or SSE leak.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-10-002.md` (executed evidence is in the active Sprint 10 report), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-10-003 — AI operations and evaluation gates

**Status:** accepted locally for Admin operations, disabled UI and versioned validator gates. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09 keyword/source contracts; 08 jobs; PPM-10-001 and PPM-10-002 interfaces/results.

**Change and user benefit:** Admin usage/errors/provider console with budgets, run inspection and redacted evidence. Version evaluation fixtures for support, citations, completion and leakage. Establish agent release thresholds before 11 evaluation.

| Implementation concern | Required work |
| --- | --- |
| Backend | Implemented module `services/api/ppm_api/ai.py` with scoped provider/retrieval/schema/evaluation modules; extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Implemented `apps/web/app/ai/` and `apps/web/components/ai.tsx` using the existing shell/transport. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `ai` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Viewer/PM cannot access restricted diagnostics; deterministic harness reports counts/failures; any unsupported number fails evaluation; disabled/no-key UI usable.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-10-003.md` (executed evidence is in the active Sprint 10 report), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Provider access/cost and evaluation sample quality; absence of a real key blocks provider verification, not contract work.

**Exclusions:** No independent agent stacks or production-trained model claims; no automatic plan edits.

**Next-sprint entry:** 11 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 11 — Nine agents, semantic assessments and recommendations

**State:** proposed. **Phase:** Evidence and intelligence. **Entry dependencies:** 06,07,09,10.

**Goal / why now:** Managers need evidence-backed interpretation of their own records and a safe review step.

**User outcome:** All nine specialized agents; Suggested semantic maturity scores; Recommendation center and document findings.

**Existing foundations:** evidence R plus A/M rubric and metric services. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-11-001 — All nine specialized agents

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 06,07,09,10.

**Change and user benefit:** Financial, Schedule, Sentiment, Risk, Resource, Governance, Agile Coach, PMO and Executive. Explicit inputs/allowed tools/typed output/citations/timeout/fallback/evaluation for each. Reuse common metrics and policy registry; aggregate with deterministic conflict/duplicate rules and missing-agent indicators. Team sentiment only from permitted text at privacy-safe group size.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/agents.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/agents/` and `apps/web/components/agents.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `agents` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Each agent tested on supported/missing/contradictory/injected inputs; green-reported late project flagged with evidence; one failed agent gives partial status; no fabricated success or individual sentiment label.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-11-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-11-002 — Suggested semantic maturity scores

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 06,07,09,10; PPM-11-001 interfaces.

**Change and user benefit:** Evaluate free text against published rubric and cited document evidence. Store deterministic original, suggested and reviewer-approved scores separately, including model/prompt/framework versions and override reasons.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/agents.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/agents/` and `apps/web/components/agents.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `agents` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Known rubric fixtures and missing evidence; reviewer may reject suggestions; original scores/history unchanged; revoked sources withheld; no AI confidence presented as maturity percentage.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-11-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-11-003 — Recommendation center and document findings

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 06,07,09,10; PPM-11-001 and PPM-11-002 interfaces/results.

**Change and user benefit:** Extract candidate risks/blockers/dependencies/compliance gaps/maturity evidence; review queue with severity/confidence/evidence and accept/reject history. Accepted means reviewed, not applied. Until 15 use ordinary authorized manual forms for any conversion, with no generic auto-action.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/agents.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/agents/` and `apps/web/components/agents.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `agents` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Supported source spans visible; duplicate and contradictory recommendations merge transparently; accepted item does not silently edit a project; edited/revoked sources invalidate unsupported proposals.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-11-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Nine agents are a large parent sprint: implement/evaluate Financial/Schedule first, then others in recorded sub-slices; parent closes only after all nine pass.

**Exclusions:** No generic execution or self-approval; no private reasoning display; acceptance does not mean application.

**Next-sprint entry:** 12 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 12 — Connector reliability and historical model foundations

**State:** proposed. **Phase:** Evidence and intelligence. **Entry dependencies:** 05,08,11; 8.1 metadata.

**Goal / why now:** Models need legitimate dated observations and connectors that keep working when a user logs out.

**User outcome:** Unattended connectors and usable conflicts; As-of datasets and justified labels; Reproducible training and model cards.

**Existing foundations:** evidence R plus D/C/J source history and connectors. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-12-001 — Unattended connectors and usable conflicts

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 05,08,11; 8.1 metadata.

**Change and user benefit:** Narrow organization-approved connector principal/credential rotation/revocation, source identity deduplication and no inherited interactive-session authority. Add local/source diff resolution with source version checks. Extend mappings for work type/bug counts/scope change and authorized history, including justified public Git commit-log capture with source/license/rate limits and optional consented text fields; rate-limit/cursor/partial recovery semantics retained. Run authorized live Jira/GitHub smoke and controlled sync.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/ml.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/ml/` and `apps/web/components/ml.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `ml` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Creator session expiry does not halt permitted schedule; principal revocation stops it; two connections cannot duplicate the same logical record. Conflict preserves local edits until reviewed. Live imports match provider source; fixture success is not live acceptance.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-12-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-12-002 — As-of datasets and justified labels

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 05,08,11; 8.1 metadata; PPM-12-001 interfaces.

**Change and user benefit:** Define delay/overrun/risk/failure/sentiment targets, horizons, observation cutoff and operational failure definition. Capture historical velocity, bugs, scope, spend, dependencies, allocation and optional consented notes. Manifest origin/license/schema/label suitability/date/privacy for PROMISE/Jira/GitHub; isolated seeded Faker demos.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/ml.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/ml/` and `apps/web/components/ml.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `ml` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Reject future leakage and unsuitable dataset; temporal/entity split overlap zero; withdrawn text excluded; labels trace to actual outcomes, not recycled risk heuristic; synthetic records never enter real evaluation.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-12-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-12-003 — Reproducible training and model cards

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 05,08,11; 8.1 metadata; PPM-12-001 and PPM-12-002 interfaces/results.

**Change and user benefit:** Deterministic baselines, scikit-learn/pandas training commands, MLflow artifacts/hashes; compare XGBoost/Random Forest and DistilBERT where suitable. Assess other candidate models rather than promise every library. Report MAE, PR-AUC/recall/calibration/Brier with sample/imbalance context.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/ml.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/ml/` and `apps/web/components/ml.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `ml` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Repeat run reproducible within documented tolerance; clean dataset import and baseline comparison; cards show targets, limitations and missing-data behavior. Insufficient genuine labels means promotion BLOCKED, not invented accuracy.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-12-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Live credentials, data rights and sufficient history may be external blockers; pipeline and demo can close separately from production model eligibility.

**Exclusions:** No promoted forecasts before evidence; no unconsented note collection; no mandatory training of every candidate technology.

**Next-sprint entry:** 13 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 13 — Eligible forecasts and uncertainty views

**State:** proposed. **Phase:** Evidence and intelligence. **Entry dependencies:** 12; shared 07 metrics.

**Goal / why now:** Users must distinguish a forecast from the current transparent risk rules.

**User outcome:** Model eligibility and promotion; Inference history and feedback; Forecast dashboards and private trends.

**Existing foundations:** evidence R plus M common dashboard DTOs. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-13-001 — Model eligibility and promotion

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 12; shared 07 metrics.

**Change and user benefit:** Registry versions with predeclared dataset/evaluation/calibration/privacy criteria, approvals and rollback; record train/serve schema and model cards. Production promotion only from genuine eligible evidence.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/forecast.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/forecast/` and `apps/web/components/forecast.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `forecast` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Rejected/incompatible model cannot serve; promotion/rollback audited; held-out results satisfy target-specific preregistered thresholds; insufficient history shows BLOCKED with requirements.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-13-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-13-002 — Inference history and feedback

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 12; shared 07 metrics; PPM-13-001 interfaces.

**Change and user benefit:** Async batch prediction, bounded cached reads, feature parity/freshness/coverage, drift/outcome feedback and history. Delay days, budget overrun units, risk category and calibrated failure/delay probabilities only when justified.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/forecast.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/forecast/` and `apps/web/components/forecast.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `forecast` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Fixture reproducibility; stale/missing/incompatible features return honest states; two tenants isolated; latency measured on stated data/hardware; schema mismatch fails safely.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-13-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-13-003 — Forecast dashboards and private trends

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 12; shared 07 metrics; PPM-13-001 and PPM-13-002 interfaces/results.

**Change and user benefit:** Views for sprint/milestone/project/budget/portfolio; contribution explanations without causal claims; delivery confidence defined explicitly; sentiment/workload trends respect privacy minima. Extend existing metric contracts, not parallel formulas.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/forecast.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/forecast/` and `apps/web/components/forecast.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `forecast` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** No eligible model and low confidence readable; probabilities never fabricated from heuristic; browser detail/evidence and accessible tables agree with serving data; experiment labels visible.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-13-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Model readiness remains a separate gate; operational pilot can operate without models, full original release cannot hide their absence.

**Exclusions:** No accuracy or causal staffing promise from demos; deterministic fallbacks do not satisfy required model release evidence.

**Next-sprint entry:** 14 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 14 — Project-aware copilot and analytics

**State:** proposed. **Phase:** Evidence and intelligence. **Entry dependencies:** 09,10,11; 8.1 metadata; 13 forecast eligibility contract.

**Goal / why now:** Users should ask questions and receive answers that reconcile with stored facts.

**User outcome:** Scoped factual and evidence tools; Streaming conversation and citations; Draft decisions and saved analysis.

**Existing foundations:** evidence R plus D/M scoped facts. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-14-001 — Scoped factual and evidence tools

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09,10,11; 8.1 metadata; 13 forecast eligibility contract.

**Change and user benefit:** Allowlisted semantic query plans, row/query/joins/aggregation budgets, timeframe/currency rules; factual tools for metrics, RAG for documents. Project selection plus multi-project/portfolio questions, including fintech delay with overrun. 13 forecasts used only when eligible.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/copilot.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/copilot/` and `apps/web/components/copilot.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `copilot` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Deterministic expected answers for why delayed/high quarterly risk/fintech overrun; mixed currency rejected or separated; missing industry/date/forecast clarified; no raw arbitrary SQL.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-14-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-14-002 — Streaming conversation and citations

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09,10,11; 8.1 metadata; 13 forecast eligibility contract; PPM-14-001 interfaces.

**Change and user benefit:** Tenant/project-scoped history, correct follow-up context, result tables/charts, evidence source previews, feedback and supported ambiguity clarification. Revalidate access to earlier turns/cached answers.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/copilot.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/copilot/` and `apps/web/components/copilot.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `copilot` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Multi-turn context retains selected scope; membership removal redacts old answers/citations; prompt/query injection, timeout and oversized requests fail safely; zero cross-tenant leak.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-14-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-14-003 — Draft decisions and saved analysis

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09,10,11; 8.1 metadata; 13 forecast eligibility contract; PPM-14-001 and PPM-14-002 interfaces/results.

**Change and user benefit:** Save answers as evidence-linked decision drafts or saved views with versions; recommendation handoff. Add approved actions only through 15; maintain a stable draft contract for 16 decision log.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/copilot.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/copilot/` and `apps/web/components/copilot.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `copilot` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Saved result retains original sources and period; deleted source marked unavailable; proposed record change creates draft only; copy/reopen permitted view works.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-14-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Natural-language ambiguity and stale evidence; 16 now explicitly depends on 14 drafts, fixing old plan mismatch.

**Exclusions:** No unrestricted SQL/Cypher; no automatic approved actions before 15.

**Next-sprint entry:** 15 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 15 — Approvals, reminders and assessment follow-through

**State:** proposed. **Phase:** Enterprise decisions. **Entry dependencies:** 08,11; 14 draft contract; 8.1 inbox.

**Goal / why now:** Reviewed suggestions need safe accountable decisions and follow-up.

**User outcome:** Versioned workflows and applied actions; Assessment scheduling and repeat history; SLA clocks, reminders and policy approval.

**Existing foundations:** evidence R plus A/J review and events. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-15-001 — Versioned workflows and applied actions

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 08,11; 14 draft contract; 8.1 inbox.

**Change and user benefit:** Risk escalation, assessment review, recommendation and plan-change flows; ordered role/person approvers, reject/return/reassign, self-approval restrictions, version checks and typed allowlisted execution. Recheck authority when applying.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/workflows.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/workflows/` and `apps/web/components/workflows.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `workflows` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Concurrent approvers/stale source/removed approver/retry tested; one approved change applied once; Viewer cannot approve; execution failure visible and retry bounded.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-15-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-15-002 — Assessment scheduling and repeat history

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 08,11; 14 draft contract; 8.1 inbox; PPM-15-001 interfaces.

**Change and user benefit:** Due dates, authorized reassignment, repeat/clone assignment and compatible-version trend/export. Preserve published rubric/answers/history; separate current person from historic assessor. Integrate review workflows with original scoring rules.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/workflows.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/workflows/` and `apps/web/components/workflows.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `workflows` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Return/reassign/repeat journey; invalid transitions and incompatible version comparisons rejected; trend and export reconcile to fixed fixtures; past completed scores unchanged.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-15-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-15-003 — SLA clocks, reminders and policy approval

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 08,11; 14 draft contract; 8.1 inbox; PPM-15-001 and PPM-15-002 interfaces/results.

**Change and user benefit:** Business-calendar versus elapsed-time clocks, due reminders/milestone notifications, cooldown/dedup and durable restart-safe timers. In-app inbox/timeline with useful failure states; approve effective policy changes against 09 registry. External report channels integrated in 21.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/workflows.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/workflows/` and `apps/web/components/workflows.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `workflows` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Timezone/calendar boundary, overdue replay/restart and removed recipient; one due reminder per eligible event; published edits affect new instances unless explicit migration; policy approval history retained.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-15-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Calendar ambiguity and concurrent decisions; notifications must use fresh permissions and no sensitive content in external previews.

**Exclusions:** No mail/Slack reporting channel assumption; no anonymous approval or silent workflow-instance migration.

**Next-sprint entry:** 16 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 16 — Transformation plans and decision tracking

**State:** proposed. **Phase:** Enterprise decisions. **Entry dependencies:** 06,09,11,14,15.

**Goal / why now:** PMO and Agile improvements need owners, measurable outcomes and a record of why decisions were made.

**User outcome:** Six evidence-backed transformation outputs; Initiatives, timeline and KPI history; Decision log and approved project conversion.

**Existing foundations:** evidence R plus A/D goals and versioned plans. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-16-001 — Six evidence-backed transformation outputs

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 06,09,11,14,15.

**Change and user benefit:** PMO/Agile roadmaps covering process improvement, governance/reporting hierarchy, resource models, tooling, delivery optimization and KPI frameworks. Capture organization scale, goals, timeframe and constraints, not invented savings.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/transformation.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/transformation/` and `apps/web/components/transformation.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `transformation` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** 300-member example explains assumptions; each output traceable to assessment/policy/risk/capacity/goal evidence; missing or restricted inputs yield qualified drafts.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-16-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-16-002 — Initiatives, timeline and KPI history

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 06,09,11,14,15; PPM-16-001 interfaces.

**Change and user benefit:** Owner role, objective, dependency/priority, effort/cost assumptions, quarterly milestones, baseline/target/measurement/review cadence; versioned editor/comparison, expected versus observed benefits and cycle detection.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/transformation.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/transformation/` and `apps/web/components/transformation.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `transformation` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Cycle rejected; edited versions preserved; unsupported numeric benefit flagged; timeline and KPI fixtures reconcile; keyboard table alternative.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-16-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-16-003 — Decision log and approved project conversion

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 06,09,11,14,15; PPM-16-001 and PPM-16-002 interfaces/results.

**Change and user benefit:** Consume 14 drafts; alternatives/rationale/approver/follow-up outcome, linked evidence and initiative. 15 approval converts to new/existing projects atomically and idempotently.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/transformation.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/transformation/` and `apps/web/components/transformation.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `transformation` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Duplicate conversion creates one project; removed approver/stale initiative rejected; decision history readable only by permitted users; alternative and outcome preserved.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-16-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Poor baselines may prevent numerical benefit claims; never substitute invented organization staffing.

**Exclusions:** No generation directly creates live commitments; original six outputs are required, not optional.

**Next-sprint entry:** 17 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 17 — Time Machine resource and budget simulation

**State:** proposed. **Phase:** Enterprise decisions. **Entry dependencies:** 05,07,13 eligibility contract,15.

**Goal / why now:** Managers need to compare plans before changing live allocations or budgets.

**User outcome:** Immutable scenario baseline; Conserving calculations and comparisons; Approved application and rollback.

**Existing foundations:** evidence R plus C/D/M immutable snapshots and metrics. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-17-001 — Immutable scenario baseline

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 05,07,13 eligibility contract,15.

**Change and user benefit:** Snapshot source versions/calendars/capacity/dependencies/budgets/risk rules/eligible model versions. Typed resource transfer and budget cut, exact inputs plus sliders; saved scenarios/version history.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/scenarios.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/scenarios/` and `apps/web/components/scenarios.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `scenarios` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Move two backend resources and cut budget 25% fixtures; no-op same totals; invalid headcount/zero-budget edge cases explained; live baseline unchanged.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-17-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-17-002 — Conserving calculations and comparisons

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 05,07,13 eligibility contract,15; PPM-17-001 interfaces.

**Change and user benefit:** Skill/effective-date/funding/dependency constraints; before/after schedule/cost/utilization/risk/affected projects. Use deterministic rules first, eligible models only in range. Explain extrapolation and unavailable intervals.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/scenarios.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/scenarios/` and `apps/web/components/scenarios.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `scenarios` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Cross-project capacity conserved; repeated results reproducible; no shared-resource duplication; uncertainty/no-model UI truthful; chart and table reconcile.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-17-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-17-003 — Approved application and rollback

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 05,07,13 eligibility contract,15; PPM-17-001 and PPM-17-002 interfaces/results.

**Change and user benefit:** Require 15 approval, compare source versions, atomic idempotent domain updates and audit/apply history; reject stale baseline and restore failed transaction.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/scenarios.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/scenarios/` and `apps/web/components/scenarios.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `scenarios` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Stale scenario rejected; repeat approval applies once; midway failure changes nothing; removed user cannot apply; live totals equal selected approved change.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-17-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Complex dependencies make forecasts uncertain; bounded scenario size and assumptions must be visible.

**Exclusions:** No implied causal ML staffing effect; no edits during simulation.

**Next-sprint entry:** 18 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 18 — Knowledge graph and impact tracing

**State:** proposed. **Phase:** Enterprise decisions. **Entry dependencies:** 04,05,09,11; 08 outbox.

**Goal / why now:** Users need traceable relationships across goals, teams, skills, risks and dependencies.

**User outcome:** Authoritative-to-derived graph projection; Rebuild, reconciliation and bounded queries; Organization map and impact paths.

**Existing foundations:** evidence R plus D/C source relationships and J events. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-18-001 — Authoritative-to-derived graph projection

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 04,05,09,11; 08 outbox.

**Change and user benefit:** Neo4j projection of Portfolio→BusinessGoal, Project→Team, Team→Skill, Project→Risk, Risk→Dependency; tenant/source IDs/evidence/timestamps; inferred edges clearly distinct. PostgreSQL remains authority.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/graph.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/graph/` and `apps/web/components/graph.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `graph` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Typed edge fixtures match source records; no inferred edge modifies source; foreign-tenant endpoints rejected; source deletion tombstones derived edge.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-18-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-18-002 — Rebuild, reconciliation and bounded queries

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 04,05,09,11; 08 outbox; PPM-18-001 interfaces.

**Change and user benefit:** Idempotent outbox updates, lag metrics/delete propagation/full rebuild; parameterized allowlisted query service with permission recheck, depth/size bounds and graph-unavailable fallback.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/graph.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/graph/` and `apps/web/components/graph.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `graph` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Rebuild hash/count reconciliation; duplicate/out-of-order events, changed access/cycles/large graphs; no arbitrary Cypher; graph outage preserves project use.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-18-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-18-003 — Organization map and impact paths

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 04,05,09,11; 08 outbox; PPM-18-001 and PPM-18-002 interfaces/results.

**Change and user benefit:** Accessible map/dependency/impact-path UI with source drill-down/table alternative and hypothesis labels. Enable copilot graph tools only through protected service.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/graph.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/graph/` and `apps/web/components/graph.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `graph` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Keyboard/table journey and bounded traversals; restricted source never appears; path descriptions distinguish relationships from proven cause.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-18-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** New graph service increases operations burden; prepare restore/rebuild proof before release.

**Exclusions:** No second authoritative database; no unlimited traversal.

**Next-sprint entry:** 19 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 19 — Comparable internal benchmarks

**State:** proposed. **Phase:** Enterprise decisions. **Entry dependencies:** 06,07,13 contracts; 8.1 metadata/paging.

**Goal / why now:** Departments and portfolios need fair comparisons rather than misleading leaderboards.

**User outcome:** Cohorts and compatible measures; Aggregates, percentiles and trends; Comparison workspace.

**Existing foundations:** evidence R plus A/M comparison and metrics. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-19-001 — Cohorts and compatible measures

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 06,07,13 contracts; 8.1 metadata/paging.

**Change and user benefit:** Period/methodology/size/work type/currency/framework version cohorts; delivery reliability/schedule/budget/utilization/maturity formulas, sample counts/missingness and minimum sensitive group thresholds.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/benchmarks.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/benchmarks/` and `apps/web/components/benchmarks.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `benchmarks` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Mixed currencies/versions never silently merge; zero denominator/small cohort unavailable with reason; no cross-team raw story-point ranking.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-19-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-19-002 — Aggregates, percentiles and trends

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 06,07,13 contracts; 8.1 metadata/paging; PPM-19-001 interfaces.

**Change and user benefit:** Authorized reproducible median/percentile/trend service over full cohort, saved filters and evidence links; preserve rule/model distinction and same metric contracts.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/benchmarks.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/benchmarks/` and `apps/web/components/benchmarks.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `benchmarks` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Hand-calculated fixtures match; pagination cannot change totals; unauthorized samples suppressed; fixed-period rerun equal.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-19-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-19-003 — Comparison workspace

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 06,07,13 contracts; 8.1 metadata/paging; PPM-19-001 and PPM-19-002 interfaces/results.

**Change and user benefit:** Department/team/portfolio views, accessible charts/tables and filter/drill-down explanations. Reuse assessment comparison instead of building competing scores.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/benchmarks.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/benchmarks/` and `apps/web/components/benchmarks.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `benchmarks` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** User can select a cohort and understand why comparison unavailable; approved filter reopens; role/currency/version cases tested.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-19-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Sparse/incompatible data legitimately prevents a comparison; display reasons rather than zeros.

**Exclusions:** Cross-customer sharing is optional and excluded; no individual productivity ranking.

**Next-sprint entry:** 20 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 20 — Meeting intelligence and actions

**State:** proposed. **Phase:** Enterprise decisions. **Entry dependencies:** 09,10,15.

**Goal / why now:** Meeting outcomes should become reviewable minutes and actions with source evidence.

**User outcome:** Authorized transcript/audio processing; Minutes and supported candidates; Review and approved action conversion.

**Existing foundations:** evidence R plus J storage/jobs and 09 documents. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-20-001 — Authorized transcript/audio processing

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09,10,15.

**Change and user benefit:** Format/duration/size matrix, consent/authority, scoped access/retention, job cancellation/retry-safe chunks/cost limits; provider transcription with timestamps/uncertainty, edited transcript versions and user speaker labels.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/meetings.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/meetings/` and `apps/web/components/meetings.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `meetings` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Transcript and noisy multi-speaker audio fixtures; real provider smoke separately; invalid file/no key/cancel/delete/access cases; no biometric identification.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-20-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-20-002 — Minutes and supported candidates

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09,10,15; PPM-20-001 interfaces.

**Change and user benefit:** Generate MOM, decisions, actions/owners/due dates/blockers/risks/dependency candidates with timestamp/span references. Mark ambiguous owner/date for confirmation.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/meetings.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/meetings/` and `apps/web/components/meetings.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `meetings` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Contradictory dates, missing owners and malicious instructions flagged; source jump works; no invented commitments; edited transcript version retains provenance.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-20-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-20-003 — Review and approved action conversion

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 09,10,15; PPM-20-001 and PPM-20-002 interfaces/results.

**Change and user benefit:** Minutes editor and 15 approve/reject; convert approved actions to existing work and risks to register once, with source-version guards and deletion propagation.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/meetings.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/meetings/` and `apps/web/components/meetings.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `meetings` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Reprocessing cannot duplicate accepted action; removed approver/stale transcript rejected; deleted audio inaccessible; approved UI journey verified.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-20-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Audio consent, transcription quality/provider rights and sensitive retention require explicit configuration.

**Exclusions:** No live meeting recording or speaker biometrics; no action creation before approval.

**Next-sprint entry:** 21 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 21 — Reports, alerts and daily executive briefing

**State:** proposed. **Phase:** Release completion. **Entry dependencies:** 08,11,13 contracts,15; shared 07 metrics.

**Goal / why now:** Executives need portable summaries and reliable authorized delivery.

**User outcome:** Versioned reports and useful exports; Subscriptions, delivery and risk alerts; Daily audio and measured operations.

**Existing foundations:** evidence R plus M/J snapshot metrics and jobs. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-21-001 — Versioned reports and useful exports

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 08,11,13 contracts,15; shared 07 metrics.

**Change and user benefit:** Weekly executive snapshot/PDF/HTML plus justified CSV tables for assessments/metrics; date/currency/freshness/evidence/changes/risks/owners/decisions. Add simple manual snapshot download first, then schedule; preserve existing JSON.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/reports.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/reports/` and `apps/web/components/reports.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `reports` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Report/table totals match dashboard/source; PDF/HTML rendered and visually inspected; authorized download and revoked access tests; missing AI/model fields labeled.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-21-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-21-002 — Subscriptions, delivery and risk alerts

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 08,11,13 contracts,15; shared 07 metrics; PPM-21-001 interfaces.

**Change and user benefit:** Email/Slack config with Admin-authorized recipients, previews/test-to-self/preferences; timezone schedules, delivery audit, outbox retries/idempotency policy. Threshold/risk-spike alerts with prior/current evidence, cooldown/dedup/recovery/quiet hours.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/reports.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/reports/` and `apps/web/components/reports.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `reports` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Actual authorized test delivery separated from fixtures; timezone/provider outage/ambiguous timeout/unsubscribe/recipient revocation/repeated spike cases; no sensitive external preview leak.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-21-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-21-003 — Daily audio and measured operations

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 08,11,13 contracts,15; shared 07 metrics; PPM-21-001 and PPM-21-002 interfaces/results.

**Change and user benefit:** Approximately two-minute cited executive script and standard-voice TTS with transcript, text fallback/protected audio/retention. Monitor availability/delivery SLI and worker lag toward 99.9% target.

| Implementation concern | Required work |
| --- | --- |
| Backend | Proposed module `services/api/ppm_api/reports.py` (or a scoped package under that name); extend existing owning modules rather than duplicate their formulas/access. Workers use existing durable jobs. Add typed contracts for the changes named above. |
| Frontend | Proposed `apps/web/app/reports/` and `apps/web/components/reports.tsx`, or extend existing related screens. Build the specific upload/review/query/comparison/settings views described; include accessible tables, keyboard use and loading/empty/error states. |
| Database / migration | New `reports` domain records/versions only where the specified user behavior requires them, via new forward migrations after current head; tenant keys, scoped references, indexes and preservation/upgrade tests. Derived stores must be rebuildable; no edits to applied migrations. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Measure audio duration/alignment and source evidence; missing TTS provider yields text fallback with status; monitoring window reported, not invented uptime.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-21-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Delivery credentials, recipients and actual availability observation need external evidence.

**Exclusions:** No named-person voice cloning; no exactly-once external-delivery promise; identity email must already work.

**Next-sprint entry:** 22 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 22 — Passkeys and all-surface account protection

**State:** proposed. **Phase:** Release completion. **Entry dependencies:** 02 and all protected feature surfaces through 21.

**Goal / why now:** Users need safe account recovery and revocation across everything the product stores or sends.

**User outcome:** Passkeys and safe recovery; Account and tenant lifecycle settings; Full-surface isolation and retention sweep.

**Existing foundations:** evidence R plus I and all later domain access. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-22-001 — Passkeys and safe recovery

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 02 and all protected feature surfaces through 21.

**Change and user benefit:** Maintained WebAuthn library; recent-verification enrollment, login/list/name/revoke, multi-credential support; challenge/origin/RP/user-verification/ownership validation and safe password/passkey recovery.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend existing services/api/ppm_api/identity.py and its schemas plus the existing owning modules for revocation; proposed passkey adapter isolated from challenge/session authority. Audit/search export uses existing scoped history sources. |
| Frontend | Extend existing apps/web/app/account/identity-client.tsx and organization screens; proposed passkey/security-settings components under apps/web/components. Build enrollment/list/recovery/lifecycle/settings flows with accessible errors. |
| Database / migration | Forward migrations for owned passkey credentials and explicit lifecycle/settings state if needed. Reuse existing user/membership/session/audit records; do not introduce a second identity model. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Virtual-authenticator wrong-origin/replay/foreign/revoked/cancel cases; record available real-device checks separately; recovery never bypasses verification.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-22-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-22-002 — Account and tenant lifecycle settings

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 02 and all protected feature surfaces through 21; PPM-22-001 interfaces.

**Change and user benefit:** Safe email change, leaving organization, display/profile/session controls, last-Admin rule, scoped retention and AI provider settings. Restricted audit search/export with clear deletion/hold rules.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend existing services/api/ppm_api/identity.py and its schemas plus the existing owning modules for revocation; proposed passkey adapter isolated from challenge/session authority. Audit/search export uses existing scoped history sources. |
| Frontend | Extend existing apps/web/app/account/identity-client.tsx and organization screens; proposed passkey/security-settings components under apps/web/components. Build enrollment/list/recovery/lifecycle/settings flows with accessible errors. |
| Database / migration | Forward migrations for owned passkey credentials and explicit lifecycle/settings state if needed. Reuse existing user/membership/session/audit records; do not introduce a second identity model. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Last Admin cannot accidentally strand organization; changed email/session revocation correct; account deletion/retention does not rewrite immutable audit/score history; restricted export tested.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-22-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-22-003 — Full-surface isolation and retention sweep

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** Medium (relative effort, not a calendar estimate). **Dependencies:** 02 and all protected feature surfaces through 21; PPM-22-001 and PPM-22-002 interfaces/results.

**Change and user benefit:** Recheck membership/roles across sessions/SSE/downloads/search/RAG/graph/meetings/cached answers/queued mail and jobs; complete purge-derived-index/cache policy with scratch verification.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend existing services/api/ppm_api/identity.py and its schemas plus the existing owning modules for revocation; proposed passkey adapter isolated from challenge/session authority. Audit/search export uses existing scoped history sources. |
| Frontend | Extend existing apps/web/app/account/identity-client.tsx and organization screens; proposed passkey/security-settings components under apps/web/components. Build enrollment/list/recovery/lifecycle/settings flows with accessible errors. |
| Database / migration | Forward migrations for owned passkey credentials and explicit lifecycle/settings state if needed. Reuse existing user/membership/session/audit records; do not introduce a second identity model. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Two-tenant three-role negative matrix with existing open sessions; revoked user loses every surface; queued delivery rechecks recipients; held/removed source behavior tested.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-22-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Real browser/device coverage and retention decisions may require follow-up; report explicitly.

**Exclusions:** SSO/SCIM/custom roles are optional; passkeys remain required original scope.

**Next-sprint entry:** 23 consumes the specific interfaces and evidence above plus its separately listed dependencies. Failed source access, contract or integrity checks block dependent work; unavailable providers/models are represented as disabled, never as working results.

## Sprint 23 — Integrated release, recovery and deployment

**State:** proposed. **Phase:** Release completion. **Entry dependencies:** 8.1 and all 09–22 acceptance; all original requirement evidence.

**Goal / why now:** A release is a proven complete user journey and recoverable system, not a list of implemented pages.

**User outcome:** Integrated journeys and measured nonfunctional gates; Production configuration and recovery artifacts; Release evidence and handoff.

**Existing foundations:** evidence R plus R existing containers/CI/test harness. These already exist where identified in the audit; new domain paths below are proposed.

### PPM-23-001 — Integrated journeys and measured nonfunctional gates

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 8.1 and all 09–22 acceptance; all original requirement evidence.

**Change and user benefit:** Onboarding→projects/resources→assessment→documents/meetings→agents/forecasts/copilot→approval→transformation/scenario/graph/benchmark→reports/audio. All requirements dispositioned, two tenants/three roles, accessibility, dependency/secret/upload/rate-limit/security tests. Measured login/FCP/chart targets with stated p95/profile/load/query plans.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend existing services/api/ppm_api/config.py, health/configuration and existing deployment/test scripts only where release checks demonstrate a need. No new release API module is required. Production IaC under infra/terraform and infra/kubernetes is proposed; reuse existing images. |
| Frontend | Verify all existing/new user journeys and publish the user/admin/demo artifacts; make targeted fixes only for reproduced integration/usability defects. No new release screen or parallel application shell is required. |
| Database / migration | No new release-domain tables. Validate upgrade against stored data, backup/restore to scratch and rollback boundaries; any discovered schema repair requires a separate forward migration with preservation evidence. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Original full-scope traceability has no unresolved required feature; isolation/security/data tests pass. Evaluate sub-second login, FCP<2s and near-60fps honestly; report actual measurements and blockers.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-23-001.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-23-002 — Production configuration and recovery artifacts

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 8.1 and all 09–22 acceptance; all original requirement evidence; PPM-23-001 interfaces.

**Change and user benefit:** Extend current local/test/demo settings deliberately; reusable production images, AWS ECS/RDS/S3 Terraform/network/TLS/secrets/migration jobs/least privilege/observability/cost/CI rollback. Kubernetes profile reuses images. Back up and restore database+objects and rebuild graph/indexes to scratch; measure recovery and data-loss objectives.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend existing services/api/ppm_api/config.py, health/configuration and existing deployment/test scripts only where release checks demonstrate a need. No new release API module is required. Production IaC under infra/terraform and infra/kubernetes is proposed; reuse existing images. |
| Frontend | Verify all existing/new user journeys and publish the user/admin/demo artifacts; make targeted fixes only for reproduced integration/usability defects. No new release screen or parallel application shell is required. |
| Database / migration | No new release-domain tables. Validate upgrade against stored data, backup/restore to scratch and rollback boundaries; any discovered schema repair requires a separate forward migration with preservation evidence. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** IaC validates; production config fails closed; migration upgrade and rollback preserve checkpoints. Scratch restore reconciles data/files/projections; live cloud and K8s execution independently labeled if unavailable.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-23-002.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

### PPM-23-003 — Release evidence and handoff

**Status:** proposed, not implemented by this planning task. **Priority:** P1. **Complexity:** High (relative effort, not a calendar estimate). **Dependencies:** 8.1 and all 09–22 acceptance; all original requirement evidence; PPM-23-001 and PPM-23-002 interfaces/results.

**Change and user benefit:** Admin/user/incident/operations/backup/rollback guides, threat model/API docs/model-data cards, complete matrix, ten-minute demo, exact reviewed revision and hosted pipeline results. Declare pilot versus full-product decision and observed SLI/error budget.

| Implementation concern | Required work |
| --- | --- |
| Backend | Extend existing services/api/ppm_api/config.py, health/configuration and existing deployment/test scripts only where release checks demonstrate a need. No new release API module is required. Production IaC under infra/terraform and infra/kubernetes is proposed; reuse existing images. |
| Frontend | Verify all existing/new user journeys and publish the user/admin/demo artifacts; make targeted fixes only for reproduced integration/usability defects. No new release screen or parallel application shell is required. |
| Database / migration | No new release-domain tables. Validate upgrade against stored data, backup/restore to scratch and rollback boundaries; any discovered schema repair requires a separate forward migration with preservation evidence. |
| AI / data | Use only the provider/model operations named in this task; preserve evidence/version/cost and disabled states. Non-AI tasks require no model calls. No synthetic fixture is production accuracy evidence. |
| Security | Permission-filter before retrieval/aggregation; recheck at download/action/delivery. Validate bounded files/queries/tools, protect secrets, redact diagnostics and audit authorized transitions. |

**Acceptance:** Independent reviewer can repeat demo and find each acceptance artifact; release checklist signed with unresolved environment/model gates explicit; no production reliability claims from unit tests.

**Tests:** Run focused unit/API fixtures and the user journey described above, including two tenants, allowed/denied roles, missing data, stale source versions, retries and dependency failure. Record real external acceptance separately from deterministic doubles.

**Completion evidence:** record exact revision, relevant API/browser/negative-case results and screenshots or rendered output in `docs/verification/PPM-23-003.md` (**proposed**), linked from the sprint report. Include command, environment, fixture size, expected/actual result and external checks still blocked. A code path alone is not acceptance.

**Definition of done:** all three task acceptances pass for their claimed environment; module contracts and source requirement dispositions updated; user journey recorded; report/handoff states real versus fixture evidence and open blockers. Published scores/history and existing stored records are preserved. A blocked required real-provider or model criterion prevents full product acceptance even if its implementation slice is locally accepted.

**Risks:** Real labels, provider/cloud credentials and production observation may block full release; explicitly separate artifact readiness from deployed verification.

**Exclusions:** No cloud deployment without configured credentials/budget/authorization; no declaring full release while required advanced scope is missing.

**Next-sprint entry:** release decision must satisfy the full checklist; unfinished requirements require an explicit repair plan, not a silent scope reduction.

## Dependency resolutions and early gates

- 09 finishes safe documents, keyword retrieval and embedding/extraction contracts. 10 supplies shared budgeted embeddings and hybrid activation. 11 supplies reviewed semantic extraction and scoring. The original combined document-intelligence requirement closes only after all these stages, not at 09 keyword search.
- 14 uses the **13 forecast contract**, which may truthfully return no eligible model. Core factual chat depends on 09–11, while forecast answers require actual 13 eligibility. This removes conflicting unconditional versus optional dependencies without removing forecast scope.
- 11 records recommendation acceptance; 15 owns applied actions. 14 decisions are drafts; 16 owns final decision history and now explicitly depends on 14 and 15.
- 8.1 identity email and basic in-app events are independent of 21 reporting channels. 15 owns due dates/SLA/timed reminders, 21 external reporting/alerts/TTS. Shared adapter contracts prevent separate incompatible mail stacks.
- Metadata is added in 8.1; connector histories/consented notes in 12; normalized comparisons in 19. No later analytic example may assume absent historical fields are already present.
- Scratch restore starts before a real-data operational pilot in 8.1, database/object/index erasure and pilot restore expand in 09, full revocation in 22, measured deployment recovery in 23. No actual purge or restore of the normal database is authorized by this plan.

## Optional enhancements after required scope

| ID | Feature / benefit | Roles | Status | Complexity / dependencies | Decision |
| --- | --- | --- | --- | --- | --- |
| OPT-001 | Task comments/checklists for lightweight collaboration | PM, members | NOT IMPLEMENTED | Medium; delivery access and notification model | P3 optional; existing tasks/blockers first |
| OPT-002 | SSO/SCIM for larger enterprise account administration | Admin | NOT IMPLEMENTED | High; 22 and approved identity provider | Separate approved scope; does not replace passkeys |
| OPT-003 | Cross-customer anonymous benchmarks | Admin/executive | NOT IMPLEMENTED | High; 19, consent/aggregation/privacy design | Excluded from required release |
| OPT-004 | Radar visualization alongside existing score bars/table | PM/executive | NOT IMPLEMENTED | Low; assessment chart usability evidence | P3 only if it improves interpretation |
| OPT-005 | Extra provider/cloud/vector/model alternatives | Admin/operators | NOT IMPLEMENTED | Varies; existing adapter/ADR decisions | Add only when a concrete supported need exists |

Original graph, transformation, simulation, model pipeline/eligible forecasts, meetings, reporting audio and passkeys are **required full-product scope**, not optional rows.


## 10 October 2026 follow-up: account and website workflow repair

The separate [repair and walkthrough execution report](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) records migration `0009_account_repair`, account/membership separation, organization profile/name controls, calendar navigation, shared business errors, the verified scoped Hement grant correction, guarded training data and current tests. Earlier sprint evidence remains historical. Global production identity administration, live-provider acceptance, general document intake and AI remain PLANNED or unverified according to their existing gates; this follow-up does not close those gates.
