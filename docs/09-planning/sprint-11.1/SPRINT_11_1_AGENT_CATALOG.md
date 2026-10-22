# Nine capability contracts

These are proposed v2 hybrid specialist contracts retaining the existing `AGENTS` IDs. Every role combines deterministic services with an optional qualified AI interpretation path. A role can serve its numerical baseline without inference; a requested interpretation remains separate work. The common contract applies to **each** of the nine entries; each entry then specifies its unique behavior. No hidden tenth specialist or model coordinator is required. This catalog incorporates ADR 11.1-11.

## Common contract: applies to every capability

Input `CapabilityInput`: schema_version=`capability-input-v2`; run_id/task_id UUID; agent ID; immutable snapshot_hash; project_id; server-derived scope_digest; period start/end; ordered evidence_refs; dependency section IDs; section_id; required_item_ids. Organization/actor/session come from worker authority, never model input. Evidence contains source ID, source/version/text hashes, Unicode code-point start/end and permitted capability IDs. Server-generated short aliases map to immutable full refs; models cannot invent that map.

Output `CapabilityResult`: agent, section_id, outcome (`supported`, `no_findings`, `insufficient_evidence`), findings, rubric_matches, narrative, gaps and covered_item_ids; runtime supplies provenance/validation/timing fields. Unknown fields forbidden. Semantic responses use compact `SectionOutput` from technical contracts, then server expands into this result. Deterministic services return the expanded baseline directly. Record `base_outcome`, `semantic_outcome` and separate coverage. Semantic_outcome is not_requested, not_needed, completed, deferred, unavailable or failed. Baseline success cannot mark a requested interpretation completed. No_findings means no supported adverse finding in the stated inspected scope; it does not certify the whole project safe. An unavailable input is never a zero metric.

Each registry entry has `execution_policy='hybrid_on_demand'`, deterministic_handler, interpretation_handler, task_class, semantic_input_categories and interpretation trigger rules. All nine interpretation handlers are defined even if a profile is unqualified/disabled. Eligible providers for every interpretation: qualified local Ollama, explicitly authorized Gemini, or optional Groq after T13 qualification; routing/capability/egress/budget checks apply independently. No role is permanently bound to a provider. Shared Python services own canonical calculations, scoring, permissions and deterministic fallback. They do not replace missing semantic evidence.

Common task classes are financial_interpretation, schedule_interpretation, team_support_advice, risk_extraction, governance_interpretation, agile_advice, resource_interpretation, portfolio_synthesis and executive_synthesis. Qualification for one class does not qualify the others. Python can decide a metric-only or empty-context request needs no model; explicit meaningful interpretation without adequate input becomes unavailable, never a model-invented fact. Baseline numerical results and AI interpretations are presented separately.

Every finding uses an existing Kind, signal, ordinal severity, typed assertion, exact evidence spans and epistemic label (`deterministic`, `interpretation`, `hypothesis`). Advice is a bounded template or short plain text and cannot execute anything. Confidence from legacy output remains visibly uncalibrated; v2 does not ask models for confidence. Numeric metrics retain value/unit/currency/period and rule version. No invented percentage risk probabilities.

Tools are server-only `read_authorized_snapshot` and `cite_exact_span`; dependencies are read-only validated sections, not requests from another agent granting authority. LLM tool calling, arbitrary HTTP/SQL/filesystem access, notifications, approvals, score writes and plan writes are denied for every capability. All reads inherit live session/membership/project/assessment/source checks and RLS; no service-wide bypass. Reauthorize before inference, publication, read and acceptance. Cloud input additionally requires project/organization egress authorization.

Validation for every output: correct task/section/agent identity; completed transport; strict bounded fields; exact permitted live spans; canonical units/values; no unknown item IDs; completeness ledger; no duplicate section writes; no hidden business mutations. Raw source text is untrusted data. Failure codes distinguish source missing/stale/revoked, invalid shape, unsupported claim, timeout and resource/provider failure. Failed output is not published as a supported finding.

Recovery for deterministic stages in any role: retry only interrupted pure computation from unchanged authorized snapshot; no provider attempts. For interpretation stages in any role: two admitted attempts maximum per logical section including replacement/decomposition, four across run, no automatic chain of new runs; immutable accepted sections survive. The remaining recovery slot may repair **or** critique, never both after the cap. Provider fallback must pass the same capability and quality gates; original budget/deadline remain. See orchestration for exact counters and goal-aware selection across all nine roles.

Success: all required items either produce validated evidence-grounded results or explicit gaps; partial coverage never equals full analysis. Every capability must pass the existing four fixture families (supported, missing, contradictory, malicious) plus its tests below. Definition success is control/coverage correctness, not broad real-model quality certification.

## financial — financial exposure (F-046)

1. **ID/purpose:** `financial`; explain existing financial exceptions in the selected project/period.
2. **Responsibilities:** classify known over-budget/usage/financial-risk conditions using canonical metrics; optionally interpret cited cost drivers, reported explanations and mitigation options. Preserve currency and metric lineage; causal statements are hypotheses unless supported by explicit evidence.
3. **Non-responsibilities:** forecasting returns, recalculating formulas independently, inferring missing spend, changing budgets.
4. **Input/context:** CapabilityInput plus `metric:budget`, `metric:spend`, `metric:usage`, `metric:financial_risk` from `command.snapshot`; proposed semantic input is explicitly selected `document:project` cost explanations plus authorized project risk/blocker records. No raw unrelated portfolio accounts, invoices or invented connectors. New source-category allowlists are target changes in T07.
5. **Output/evidence:** zero to five baseline risk findings with metric refs; interpretation SectionOutput adds 0–2 cited financial risk explanations/advice items, with no rubric matches. Numeric assertions must match canonical metrics. Missing metrics/text create separate gaps.
6. **Execution/models/providers:** Python financial baseline plus optional financial_interpretation LLM; requires qualified financial-evidence reasoning, structured output and the common provider policy. Explicit financial investigation or relevant explanatory text with an adverse/disputed metric is a trigger; a numeric-only overview needs no call.
7. **Dependencies/tools/security:** snapshot only; common read-only permissions; currency-separated totals.
8. **Validation/failure/recovery:** compare original Decimal metric, unit, period and rule; stale/unknown values unavailable; explanations cite permitted text and cannot revise totals. Use common bounded interpretation recovery; failure preserves baseline and exposes missing interpretation.
9. **Length:** baseline at most five findings, title ≤120/advice ≤240 chars; interpretation ≤512 tokens and 0–2 items; combined DTO ≤16 KB.
10. **Acceptance/success:** AT01-F: usage 101 triggers the canonical exception with zero calls in metrics mode; missing spend unknown and INR/USD never summed. A cited rework explanation yields an interpretation with unchanged overrun; unrelated quote fails support; no eligible model leaves semantic_outcome unavailable/deferred. Reported Green discrepancy remains visible.

## schedule — schedule and dependency exposure (F-047)

1. **ID/purpose:** `schedule`; identify current timing exceptions against the existing baseline.
2. **Responsibilities:** expose canonical variance, schedule risk, overdue critical milestones and known dependency links; optionally interpret authorized status narratives and propose evidence-grounded response options.
3. **Non-responsibilities:** probabilistic forecasts, new causal links from text, changing dates or baselines.
4. **Input/context:** `metric:variance`, `metric:schedule_risk`, `metric:critical`, `record:dependencies`; baseline/version/calendar/period refs from owning services. Proposed semantic inputs include selected `document:project`, `document:sprint_report` and scoped blocker/dependency records; no hidden foreign-project data.
5. **Output/evidence:** ≤5 baseline timing findings; interpretation SectionOutput adds 0–2 schedule/dependency explanations and mitigations with exact spans. Missing baseline remains unknown.
6. **Execution/models/providers:** Python schedule baseline plus optional schedule_interpretation LLM under common provider policy. Trigger on explicit schedule investigation or an adverse/disputed timing condition accompanied by relevant narrative. No metric recomputation in the model.
7. **Dependencies/tools/security:** snapshot; canonical scoped dependency endpoints only; no hidden foreign-project IDs in output.
8. **Validation/failure/recovery:** compare canonical variance/direction/calendar; no duplicated schedule formula. Explanations need matching authorized spans, and proposed edges remain review candidates. Missing authority gives a gap; common bounded recovery preserves baseline.
9. **Length:** ≤16 KB expanded result; interpretation ≤512 tokens and 0–2 items per section.
10. **Acceptance/success:** AT01-S: late milestone survives model outage, baseline retained, negative variance not mislabeled overdue and cross-scope edge withheld. An approval-delay narrative supports a provisional explanation without altering dates; missing narrative never becomes a causal finding.

## sentiment — team delivery support signal (F-048)

1. **ID/purpose:** `sentiment` retained for API compatibility; UI label “Team support signal”.
2. **Responsibilities:** render privacy-safe open blocker aggregate and data sufficiency; optional model may explain the stated aggregate's limitations and suggest generic team-support review questions when explicitly requested.
3. **Non-responsibilities:** emotional sentiment, diagnosis, employee ranking, individual note interpretation; F-060 remains future work.
4. **Input/context:** only server-created `group:blockers`, minimum-five check and existing Admin-sensitive access rule. Raw notes/names never enter input.
5. **Output/evidence:** one baseline blocker summary/no_findings when count=0 and eligible; insufficient_evidence when suppressed. Optional synthesis-mode SectionOutput cites only the aggregate and labels advice as conditional; it cannot claim causes, emotional state or new team facts.
6. **Execution/models/providers:** Python privacy gate/template plus optional team_support_advice LLM under common provider policy. Current single blocker count does not automatically trigger AI. Explicit advice request can trigger a qualified bounded explanation; absent permitted aggregate blocks it. Future emotional/text sentiment is outside this input contract.
7. **Dependencies/tools/security:** snapshot privacy gate; no other capability can request an exception to suppression.
8. **Validation/failure/recovery:** count matches source; group<5 or lost grant suppresses baseline and model input. No raw notes, expanded retrieval or diagnosis in recovery. A generic advice item cannot be presented as an observed team condition; common bounded recovery.
9. **Length:** baseline ≤1 KB excluding refs; optional advice section ≤512 tokens/0–2 narrative items.
10. **Acceptance/success:** AT01-N: sizes 4/5, revocation, no raw notes/names in prompts/logs; zero count differs from unknown. Count-only auto mode makes zero calls; explicit qualified advice preserves privacy and cannot infer morale. Suppression prevents a model request entirely.

## risk — evidence-based risk extraction (F-041/066/067/070/071)

1. **ID/purpose:** `risk`; extract a small set of reviewable risks, blockers and proposed dependencies from selected evidence.
2. **Responsibilities:** interpret authorized project text/records; preserve contradictions; label causal associations as hypotheses.
3. **Non-responsibilities:** redefine metric risk scores, approve risks, prove causation, train forecasts, issue action requests.
4. **Input/context:** `metric:risk`, `record:risks`, `record:blockers`, `document:project`; explicit selected chunk/item manifest. Other-project context excluded.
5. **Output/evidence:** `SectionOutput` with 0–2 risk/blocker/dependency candidates, subject alias, predicate, brief claim/advice and 1–2 exact spans each. Causal hypothesis requires supporting source reference and label; no numerical predicted impact.
6. **Execution/models/providers:** deterministic existing metric fallback plus optional risk_extraction LLM; requires structured output, qualified extraction and no tool dependence. Common provider eligibility applies; optional Groq activation is T13.
7. **Dependencies/tools/security:** snapshot; no need to wait on other semantic worker. Read/cite only, project egress checked.
8. **Validation/failure/recovery:** exact citation plus semantic support status; fabricated subject/edge rejected. Missing text leaves deterministic fallback and declared semantic gap. Common bounded repair; smaller one-finding section on truncation.
9. **Length:** 512 token hard maximum, two findings target, concise claim/advice ≤160 chars each; no guarantee two always fit.
10. **Acceptance/success:** AT01-R/AT13: cited hidden risk under Green preserved, unrelated quote does not substantiate claim, opposite accounts retained, injected “edit plan” never acts. Success produces review candidates with honest coverage.

## resource — aggregate capacity interpretation (F-045)

1. **ID/purpose:** `resource`; explain capacity exceptions and review options.
2. **Responsibilities:** show existing capacity-risk condition and scope; optionally interpret authorized aggregate constraints and project-level blocker narratives to propose reviewable staffing or sequencing options.
3. **Non-responsibilities:** individual productivity ranking, optimization, allocation writes or access to private effort notes.
4. **Input/context:** existing `metric:capacity_risk`, period/unit/freshness; richer aggregates only if exposed by an authorized capacity API. Proposed semantic inputs are selected project/sprint report windows after server-side privacy filtering; no raw-person queries, individual effort notes or hidden-project totals.
5. **Output/evidence:** ≤5 baseline risk findings; interpretation SectionOutput adds 0–2 cited capacity constraint explanations or conditional staffing/sequencing suggestions, without a claimed optimal plan.
6. **Execution/models/providers:** Python capacity baseline plus optional resource_interpretation LLM under common provider policy. Explicit resource investigation or a capacity exception with permitted explanatory context is a trigger; numbers-only overview needs no call.
7. **Dependencies/tools/security:** snapshot and existing capacity privacy/suppression; no cross-project permission inheritance.
8. **Validation/failure/recovery:** canonical metric, no hidden totals, stale/partial data qualified; narrative must cite approved filtered input. No staffing optimization or named-person inference; common bounded recovery retains baseline.
9. **Length:** ≤16 KB expanded DTO; interpretation ≤512 tokens/0–2 items per section.
10. **Acceptance/success:** AT01-C: overload accurate, missing availability unknown, grant removal hides protected content. A permitted project-level skill bottleneck explanation can yield conditional advice with unchanged capacity figures; raw workforce notes never enter context. Allocation/effort tables remain unchanged.

## governance — policy gaps and rubric interpretation (F-042/023–025/072)

1. **ID/purpose:** `governance`; interpret answers/text against explicit published rubric and selected policy.
2. **Responsibilities:** sole owner of semantic rubric matches, supported policy gaps and missing-evidence requirements.
3. **Non-responsibilities:** legal certification, automatic score approval, rewriting rubric/answers or independent numerical scoring.
4. **Input/context:** `document:policy`, `assessment:answer`, `assessment:rubric`; exact framework version, assessment revision, selected numeric-question IDs, relevant text plus required rubric levels.
5. **Output/evidence:** rubric mode returns 0–2 matches with question alias, exact level and answer-text span plus optional policy span; policy mode returns 0–2 compliance_gap/maturity_evidence findings. A section uses one mode, not both.
6. **Execution/models/providers:** optional governance_interpretation LLM plus deterministic `assessment.compute_scores`; requires qualified rubric interpretation and structured output under common provider policy.
7. **Dependencies/tools/security:** snapshot; private assessment authority in addition to project scope. Agile cannot supply alternate matches.
8. **Validation/failure/recovery:** question/level must exist; supporting answer text must belong to that question or explicit rubric-linked evidence, not merely another answer in its dimension. All required numeric questions must have supported matches before a suggested dimension score exists. Reuse published weights. Changed assessment revision invalidates all assessment-derived results. Common bounded recovery.
9. **Length:** ≤512 tokens, ≤2 matches/section; unprocessed question manifest remains visible, no fabricated completion for a 50-question assessment.
10. **Acceptance/success:** AT01-G/AT10: invalid level and duplicate matches rejected, wrong-question support rejected, missing match yields null suggested score, original score unchanged; independent read-granted reviewer can review. Scores, evidence and uncertainty remain distinct.

## agile_coach — practice recommendations (F-043/025)

1. **ID/purpose:** `agile_coach`; propose evidence-grounded process improvements.
2. **Responsibilities:** interpret sprint records/reports and assessment gaps; propose one or two actionable review suggestions.
3. **Non-responsibilities:** compare raw story points across teams, recompute rubric matches/scores, infer developer performance or change sprints.
4. **Input/context:** `record:sprints`, `document:sprint_report`, permitted `assessment:answer`/`assessment:rubric`; optional validated governance gaps if already available, never a required extra model call.
5. **Output/evidence:** ≤2 maturity_evidence/blocker candidates with bounded practice advice and exact spans; unsupported techniques omitted.
6. **Execution/models/providers:** optional agile_advice LLM plus deterministic delivery/practice baseline; qualified advice relevance plus structured output under common provider policy, independently ranked.
7. **Dependencies/tools/security:** snapshot; optional accepted governance section, no hard dependency, to avoid unnecessary serial delay.
8. **Validation/failure/recovery:** each advice item tied to cited practice gap, no new numeric targets asserted as facts; common bounded repair, unavailable when text cannot support interpretation.
9. **Length:** 512 tokens maximum, ≤160 chars/claim and advice.
10. **Acceptance/success:** AT01-A: retrospective evidence produces reviewable advice, cross-team points not ranked, missing sprint text abstains, malicious report ignored. Useful suggestions preserve original data.

## pmo — authorized portfolio roll-up (F-040/049)

1. **ID/purpose:** `pmo`; aggregate validated findings over the explicitly visible portfolio subset.
2. **Responsibilities:** consume deterministic reconciliation/coverage; optionally synthesize cross-domain implications, dependencies and review priorities over the authorized portfolio subset.
3. **Non-responsibilities:** re-read unrestricted project data, independently regenerate risk findings, claim whole-portfolio coverage from a subset.
4. **Input/context:** snapshot's authorized PMO portfolio metrics/dependencies plus validated terminal outcomes of financial/schedule/sentiment/risk/resource/governance/agile; dependency refs reauthorized.
5. **Output/evidence:** baseline reconciled refs/conflicts/coverage/unavailable IDs and canonical per-currency aggregates. Optional synthesis-mode SectionOutput adds 0–2 interpretation/advice items with upstream finding refs and original source spans. No new uncited facts or revised totals.
6. **Execution/models/providers:** Python reconciliation/roll-up plus optional portfolio_synthesis LLM under common provider policy. Trigger on portfolio analysis request or multiple supported cross-domain findings needing interpretation; a simple exact roll-up needs no model.
7. **Dependencies/tools/security:** terminal outcome descriptors for all seven upstream domains, including failed/deferred or explicitly skipped/unrequested; no wait for an unplanned task. Visible-source intersection cannot widen scope.
8. **Validation/failure/recovery:** stable identity and canonical coverage remain Python-owned. Model synthesis must reference accepted upstream items and authorized original evidence; disagreement and unavailable dependencies cannot be erased. Common bounded semantic recovery; baseline survives failure.
9. **Length:** baseline ≤100 refs/≤64 KB before pagination; each synthesis section ≤512 tokens/0–2 items.
10. **Acceptance/success:** AT01-P/AT12: distinct issues/conflicts/missing projects retained. Portfolio synthesis connects a cited cost issue and dependency delay without adding hidden projects or changing numbers; insufficient upstream evidence abstains. Failed/deferred synthesis is separate from successful roll-up.

## executive — concise final briefing (F-044)

1. **ID/purpose:** `executive`; render a concise decision-support view from PMO output.
2. **Responsibilities:** retain a deterministic briefing skeleton; optionally produce concise audience-specific explanations and priority rationales from validated PMO/domain findings, preserving original metrics, conflicts and gaps.
3. **Non-responsibilities:** unsupported new factual claims, vote-based certainty, new scores/forecasts, automatic approvals or suppression of adverse evidence. Priority rationale is provisional interpretation, not a new authoritative risk score.
4. **Input/context:** validated PMO roll-up and authorized canonical health/usage metrics; selected project/portfolio coverage label.
5. **Output/evidence:** baseline top-five refs plus mandatory conflicts/gaps, timestamp and review caveat. Optional synthesis-mode SectionOutput contributes 0–2 cited briefing paragraphs/priority rationales, referencing upstream findings and original evidence. Material conflicts/gaps are appended by Python even if the model omits them.
6. **Execution/models/providers:** Python briefing skeleton/number and citation checks plus optional executive_synthesis LLM under common provider policy. Explicit executive briefing or substantive conflicting/prioritized findings can trigger AI; model failure preserves a clearly labeled baseline briefing.
7. **Dependencies/tools/security:** PMO terminal; all underlying source refs checked again at read/accept time; original data text escaped.
8. **Validation/failure/recovery:** every factual number/claim traces to accepted item and original permitted evidence. Interpretations preserve upstream uncertainty; no rounding changes, omitted conflicts or unsupported priority facts. Common bounded recovery; required synthesis without a slot is deferred, not completed by its template.
9. **Length:** assembled briefing target ≤500 words/≤16 KB with paginated mandatory lists; each model section ≤512 tokens/0–2 narrative items. Assembly can exceed one call's token budget.
10. **Acceptance/success:** AT01-X: disagreement/partial coverage remain visible, values unchanged, names escaped, review independent. A briefing request can select executive_synthesis even when risk/governance/agile are not selected for model calls; fallback has distinct semantic status and is not claimed as completed AI synthesis.

The grouped entries above plus common fields cover purpose, boundaries, input/output, context/evidence, execution/capabilities/providers, dependency/tools, validation/failure/recovery, length/security, tests and success for every ID. Model qualification is per semantic task class, not “one best model for all agents”.
