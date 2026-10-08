# Versioned metric dictionary

Sprint 05 implements `capacity-v1` for M07–M10 and initial team support signals:
[exact local-date formulas, completeness and scope rules](capacity.md). Full-resource
utilization is never inferred from a caller's visible subset of project allocations.
These are deterministic staffing measures, not predictive/medical assessments.

Sprint 04 implements only the `delivery-v1` summary DTOs: [exact money/alignment rules](delivery.md). Budget usage is unknown for zero budget or incomplete ledger; alignment unknown unless weights total 1; computed health remains null. Planned formulas below are not implemented dashboard claims.

Version `metrics-v1-proposed`, Sprint 00. The source specifies metric categories but not equations. These proposed defaults are reproducible product rules, not empirically validated predictive models. Store definition/rule version with every snapshot; dashboards, reports, agents, simulations and exports call the same metric service.

## Shared period and unit conventions

UTC instants for storage; organization IANA timezone for displayed day/week/quarter boundaries. Timestamp periods are `[start, end)`; date-ranged allocations follow the same half-open convention. Baseline finish is a date interpreted at end of its local working day. Week starts Monday, quarters are calendar quarters unless a versioned fiscal calendar overrides. Business-day calculations use the project's immutable calendar version, including holidays and daily capacity. Snapshot all calendars used by scenarios.

Money uses decimal strings and currency. Portfolio monetary totals are per-currency unless an explicitly supplied dated FX conversion policy applies. Budget is approved budget as of the snapshot; commitments and actuals are distinct. Missing actuals are not zero unless the source is confirmed complete. Story points are meaningful only within the same team and estimation policy. Percentages have unit `%` on 0–100 scale; probabilities use unit `probability` on 0–1.

## Metric definitions

| ID | Definition and formula | Missing or special cases |
| --- | --- | --- |
| M01 Actual spend | Sum accepted expenditure amounts in period/project/currency; corrections are auditable reversals | Incomplete ledger shows partial coverage, not full total |
| M02 Budget usage | 100 × cumulative actual spend / current approved budget, same currency | Budget zero → undefined plus zero-budget flag; may exceed 100% |
| M03 Cost overrun | Forecast final cost minus approved budget; percent = 100 × difference / budget | Forecast absent → unknown; negative means forecast under budget |
| M04 Schedule variance | Working-day difference between baseline finish and actual finish if done, otherwise forecast finish; positive is late | No forecast → unknown forecast variance; overdue-unfinished flag calculated separately |
| M05 Milestone on-time rate | 100 × eligible completed milestones finished by baseline date / completed milestones with valid baseline | No completed eligible milestones → unknown; show count and open-overdue count separately |
| M06 Sprint velocity | Sum accepted completed points for a team's closed sprint using closure snapshot | Reopened/carryover work follows versioned team rule; no cross-team point ranking |
| M07 Available capacity | Sum scheduled working hours minus approved leave per resource/day | Clamp at zero; missing calendar → unavailable, not default full time |
| M08 Planned utilization | 100 × allocated hours / available capacity for selected interval | Zero capacity → undefined with over-allocation flag if allocated hours > 0; can exceed 100% |
| M09 Actual utilization | 100 × accepted actual effort hours / available capacity | Missing effort coverage makes value partial; not a productivity score |
| M10 Allocation excess | max(0, allocated hours − available capacity), aggregated without double-counting resources | Show source/destination scope limitations rather than leaking hidden project names |
| M11 Maturity dimension | 100 × sum(answer weight × normalized rubric score) / sum(answer weights); normalized score = (value − min)/(max − min) | Final requires all required answers; draft provisional uses answered denominator and explicit coverage; min=max invalid |
| M12 Overall maturity | Sum(dimension weight × approved dimension score), weights sum to 1 | Unapproved/incomplete dimensions → provisional or unknown; never silently renormalize final |
| M13 Strategic alignment | Project value = 100 × sum(goal weight × declared contribution); contribution 0–1, weights sum to 1 | Contributions are reviewed inputs, not AI facts; portfolio = equal-weight mean of covered project values with coverage |
| M14 Business value | Record target and realized benefit per KPI unit/time period; compare only same unit | No adding revenue, NPS and saved hours into one unexplained number |
| M15 Evidence coverage | 100 × valid available required evidence inputs / required evidence inputs for that metric rule | Quality/freshness shown separately; quantity does not prove truth |
| M16 Forecast delay | Predicted working days beyond baseline for a named target/horizon | Display calibrated intervals only when evaluated; no suitable model → labeled rule fallback/unknown |
| M17 Failure probability | P(project meets defined failure label by horizon), from eligible calibrated model | Failure definition and labeled observations required; risk score cannot substitute |
| M18 Delivery confidence | P(finish by approved baseline date), only from an eligible on-time model | Not 1 minus general failure probability unless outcome/horizon are exact complements |
| M19 Risk trend | Current comparable risk score minus prior score, percentage points | Different rule/input scope versions flagged as noncomparable |
| M20 SLA elapsed | Elapsed real or business-calendar minutes from start to terminal state, less explicitly permitted pauses | Workflow version defines clock and pauses; no hidden reset on reassignment |

M11 example: two required questions, weights 1 and 3, normalized scores 0.5 and 1 give `(1×0.5 + 3×1)/4 ×100 = 87.5`. If the second answer is missing, show provisional 50 with 25% weight coverage, not a final maturity score. Evidence coverage M15 counts inputs; assessment completeness uses weight coverage, explicitly labeled.

## Starter risk and health rule

Rule `risk-rule-v1` uses three operational components on 0–100: schedule, financial and capacity. Sentiment/governance findings are separate indicators initially and do not covertly change weights. All three required components must be available to publish the combined score; otherwise display `insufficient_data` and individual known components.

- Schedule component: clamp(100 × positive working-day delay / max(1, baseline duration working days), 0, 100). If no forecast exists, the component is unavailable; a separate overdue flag still appears.
- Financial component: clamp(100 × positive forecast cost overrun / approved budget, 0, 100); budget zero or missing forecast makes component unavailable.
- Capacity component: clamp(100 × aggregate excess hours / aggregate available hours, 0, 100) over the next four weeks for assigned resources, using full-resource allocations. If hidden allocations cannot be aggregated by policy, display insufficient scope. Zero capacity is unknown plus explicit overload flag.
- Combined risk = 0.40 × schedule + 0.35 × financial + 0.25 × capacity, rounded once at display to one decimal. Low `<30`, Medium `30–<60`, High `>=60`. These are illustrative operational thresholds needing product validation, not failure probabilities.
- Computed health = 100 − combined risk only for this rule. Green means risk `<30`, Amber `30–<60`, Red `>=60`. The health label includes rule version and coverage. Unknown risk means unknown health.
- Reported health remains the separately timestamped human Green/Amber/Red/Unknown. A discrepancy flag appears when computed severity exceeds reported severity, or when a missed critical milestone contradicts reported Green even if combined risk is unavailable. Show both the metric and the critical flag without silently overwriting reported status.

Worked rule fixture: 5-day delay / 50-day duration → schedule 10; forecast 110,000 / approved 100,000 → financial 10; excess 80 / capacity 400 → capacity 20. Combined risk 12.5, health 87.5, Low/Green. This demonstrates arithmetic only, not validation of sensitivity; critical missed milestones can still flag a reported-health discrepancy. The review must decide whether initial thresholds are useful before production.

Portfolio risk/health is an equal-weight mean of eligible active projects, with eligible/total counts and worst-project indicator. Do not silently weight by incomparable currencies or treat missing projects as healthy. Closed/cancelled projects are excluded from current active health but retained historically.

## Freshness alerts and privacy

Proposed initial freshness threshold is one configured source sync interval plus five minutes; manually updated facts instead use the organization's reporting cadence. Display event time, ingestion time and compute time. A stale source remains stale even if computation just ran.

Starter alert trigger: transition from below 60 to 60 or more, or increase of at least 15 risk points within 24 hours, same rule version and adequate coverage. One alert per project/rule/trigger window; proposed cooldown six hours. Recovery notification is optional and requires risk below 55 for two consecutive valid evaluations. Defaults are configurable policy proposals; outages and unknown values do not masquerade as recovery.

Team workload warning: planned utilization >100% for two consecutive weeks, or recorded overtime above 10% of available capacity. Sentiment is a separate trend with source limitations. Suppress sensitive aggregates for groups under five resources and exclude individual ranking/medical labels. Source lawfulness, workforce policy and production thresholds remain review items.

## Sprint 06 implemented maturity rules

M11/M12 now use the versioned [assessment contract](assessment.md). Decimal scoring uses exact published rubric levels, positive weights and dimension weights summing exactly to 1. Draft scores remain provisional; required text answers count toward completeness but not numeric scores. Answer coverage is weighted, evidence coverage counts questions with notes or independently released attachments, and both remain within 0–100. Completed results and original framework versions are preserved. Worked 87.5 → reviewer-adjusted 75 versus Operations 0 fixture and unknown cases are in the contract and Sprint 06 tests.

## Sprint 07 implemented dashboard metrics

[Command center contract](command-center.md) now implements shared M01/M02/M04/M06/M07–M10/M13–M15 and `risk-rule-v1` current-state health. Missing inputs, period filters, currency grouping, source freshness, frozen closure points and baseline-calendar choices are explicit. Proposed predictive metrics remain unimplemented.
