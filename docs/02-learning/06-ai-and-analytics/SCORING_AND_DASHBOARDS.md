# Where scores and dashboard numbers come from

[Learning roadmap](../00-getting-started/README.md) Â· Next: [AI status](AI_AND_JOBS.md)

## Assessment scores: first follow the stored answer

Answers live in `ppm_answers`, tied to `assessment_id` and `question_id`. The definition lives in the assessment's frozen `ppm_framework_versions.snapshot`. `assessment.scoring` loads those inputs and passes them to [`compute_scores`](../../../services/api/ppm_api/assessment.py), along with valid human adjustments.

A dimension is a group of questions, such as one area in an example framework. Each dimension has an overall weight. Each question also has a positive weight within that dimension. Publication requires dimension weights to total exactly 1 and at least one numeric question per dimension.

The algorithm handles one question at a time:

1. Find its saved answer using the question UUID.
2. Check that the value matches the published question. A missing required answer adds a note.
3. Convert boolean `"true"` to 1 and `"false"` to 0.
4. For a rubric answer, convert its numeric level to `(value - minimum level) / (maximum level - minimum level)`. A rubric is the published list of allowed levels and labels. Numeric values, rather than list position, determine normalization.
5. Count text answers for answer coverage and required completion, but exclude them from numerical scoring.
6. If the reviewer supplied an allowed numeric adjustment, replace the normalized value with `reviewer_score / 100` while retaining the raw answer.
7. Add weight Ã— normalized value to the numerator and answered numeric weight to the denominator.

Actual arithmetic excerpt:

```python
numerator += w * norm
denominator += w
score = (100 * numerator / denominator).quantize(Decimal("0.0001")) if denominator else None
```

The first line accumulates weighted answer value. The second accumulates only answered numeric weights. The third turns the weighted average into a 0â€“100 score, rounded to four decimal places. `None` means no computable score, rather than a score of zero.

## Work a real test example by hand

`tests/test_assessment.py:test_weighting_unknown_and_coverage` uses a boolean with weight 3 and a rubric with weight 1 on levels 0â€“2.

If the boolean is true and rubric answer is 1, their normalized values are 1 and 0.5. The dimension score is:

```text
100 Ã— (3 Ã— 1 + 1 Ã— 0.5) / (3 + 1) = 87.5
```

If the reviewer changes the rubric score to 0, the dimension becomes `100 Ã— (3 Ã— 1 + 1 Ã— 0) / 4 = 75`. The original rubric answer is still stored.

For several dimensions, the overall score is the sum of dimension weight Ã— dimension score. For example, if valid scores are 80 and 60 with weights 0.75 and 0.25, the formula gives 75. This second example illustrates the actual formula; it is not a claimed saved assessment fixture.

If any dimension cannot be scored or the dimension weights do not total 1, overall is null. Optional unanswered numeric questions are excluded from the answered denominator. A draft can show a provisional score while a required answer is missing, but `finalize_check` prevents submission/completion.

## Score is different from coverage

Answer coverage is **valid answered question weight / all question weight Ã— 100**, including text weights. Evidence coverage is **questions with nonblank evidence narrative or released attachment / all questions Ã— 100**. They use different denominators.

In the two-question test above, both answers mean answer coverage 100%. Evidence only for the boolean means evidence coverage 50%. If only the weight-1 rubric is answered, its provisional score is 50, answer coverage is 25%, and the missing required boolean blocks submission. Evidence does not add score points or prove a claim true.

`submit` and `review` store computed results in `ppm_assessments.results`. The UI displays overall/dimension scores in bars and tables. Later publication produces another version, so old answers retain their old weights and rubrics. No overall named maturity-band classifier or AI assessment interpretation is implemented.

## Capacity: where the hours come from

`capacity.calculate` reads availability periods, immutable calendars, holidays, leave and active allocations. Date ranges use `[start,end)`: include the start date and exclude the end. It calculates each local date first, then totals days/weeks.

```text
available = max(0, nominal scheduled hours - leave hours)
holiday available = 0 before subtracting leave
allocated = sum active allocation hours_per_day on scheduled weekdays
daily excess = max(0, allocated - available)
planned utilization = 100 Ã— allocated / available
```

Five four-hour weekdays give 20 available hours. Two three-hour allocations per day give 30 allocated hours: 150% planned utilization and 10 excess hours. Two full leave days reduce availability to 12, while planned work remains 30: 250% and 18 excess hours. This illustrates `calculate` using its actual daily rules.

Allocation remains counted on otherwise scheduled days during holidays/leave, exposing conflicts. A normal weekday with zero scheduled hours does not count planned hours. Missing calendars leave availability unknown and count allocation dates conservatively. Excess is summed per day, so spare capacity on Tuesday cannot cancel overload on Monday.

The percentage requires full-resource scope and a nonzero known denominator. Actual utilization additionally requires private effort access and complete effort coverage across the period. Team overload requires consecutive full overloaded weeks, at least two; overtime warnings require complete effort and overtime greater than available/10. Those are rules in `team_summary`, not AI predictions.

## Dashboard: follow one snapshot

`CommandCenter.refresh` requests `/api/v1/command/snapshot`. `command.snapshot` obtains the organization timezone/policy and visible projects, then loads associated source facts under row policies. It also calculates capacity for the selected range and next 28 local days. The same response supports all four dashboard views.

Selected dates filter period facts. They do not turn today's mutable database into an exact historical database snapshot.

### Money and alignment

- Approved budget sums nonarchived approved `ppm_budget_lines.amount`.
- Spend sums signed `ppm_expenditures.amount`, including reversals. Period spend additionally filters `spent_on` within `[start,end)`.
- `metric_math.budget_usage` returns `100 Ã— spend / budget`, rounded to two decimals, only with nonzero budget and complete ledger. Budget 1000/spend 400 gives 40%; incomplete ledger gives null.
- `metric_math.alignment_score` returns `100 Ã— Î£(weight Ã— contribution)` only when active goal weights total exactly 1. It is stored alignment data, not an AI judgment.

Money remains grouped by currency. Benefits fully contained in the selected interval show target/realized values with their units; unlike units are not added together or prorated.

### Project health, one component at a time

`workdays` counts signed scheduled working dates in `(target,finish]`, excluding holidays according to the selected frozen calendar. The metric plan chooses a baseline. The finish is actual where available, otherwise forecast. Positive finish variance means late.

Schedule risk is `100 Ã— max(0, finish variance) / max(1, baseline working duration)`, limited to 0â€“100. It needs target/finish/calendar and baseline duration.

Financial risk is `100 Ã— (forecast_cost - approved budget) / approved budget`, limited to 0â€“100. It needs a positive approved budget and a `ppm_metric_plans.forecast_cost`. It is not simply the spent percentage.

Capacity risk is `100 Ã— total daily excess / total available hours`, limited to 0â€“100, for assigned resources in the next 28 local days. It requires nonzero known capacity and full-resource scope. Hidden workload is not assumed to be zero.

Actual `command.combined`:

```python
if schedule is None or financial is None or staffing is None:
    return None
return schedule * Decimal(".4") + financial * Decimal(".35") + staffing * Decimal(".25")
```

The missing-input branch keeps the result unknown. The return line applies 40% schedule, 35% financial and 25% capacity. Weights are not redistributed around missing components.

The accepted test fixture has five late working days over a 21-working-day duration, financial risk 10 and capacity risk 25:

```text
schedule = 100 Ã— 5 / 21 â‰ˆ 23.80952
risk = 0.4 Ã— 23.80952 + 0.35 Ã— 10 + 0.25 Ã— 25 â‰ˆ 19.27381
evidence health = 100 - risk â‰ˆ 80.72619
```

Default category thresholds are Amber at risk 30 and Red at risk 60; below Amber is Green. Admin may change validated policy. These risk points are a rule-based signal, not a probability of failure.

Human `reported_health` stays separate. A discrepancy appears when the computed category is worse than a known reported category, or reported Green has an overdue critical milestone. Therefore an overdue gate can flag a discrepancy even when composite health is Unknown.

### Other displayed numbers

`delivery.summary` counts work by status and supplies project budget/alignment information. Its `computed_health` is empty; command-center health comes from `command.snapshot`.

Milestone variance compares frozen baseline due date with actual/current planned date using the calendar. Overdue critical gates count critical milestones with no actual date and due date before today.

Velocity reads `ppm_sprint_closures` for closed sprints in the period. `delivery.write` froze completed work-item points when the sprint closed; later changes do not rewrite that velocity. Old closed sprints without a complete closure stay unknown.

Portfolio evidence health equally averages covered active/on_hold projects. Coverage reports how many eligible projects contributed; unknown projects do not silently become healthy. Worst covered health is the minimum available active-project health. Alignment averages covered visible projects.

### Source age and evidence

Metrics include value, unit, contributing facts, period, coverage, source update time and computation time. Source freshness uses the oldest contributing update and a default seven-day threshold. Reloading does not make old source facts fresh. Old but stable baselines may conservatively make a metric stale.

To verify a number, inspect the snapshot response and source drawer, find its metric key in `command.py`, then follow the source IDs. Read `tests/test_command.py` and `tests/test_capacity.py` for missing data, mixed currencies and visibility cases. This chapter confirms source formulas; it does not report newly run calculation or browser tests.


## Source-reviewed Sprint 8.1 update — 9 October 2026

`pilot.comparison` selects completed departmental assessments for one framework version and an ordered UTC creation period of at most ten years. It computes count/scored_count/average from the full permitted cohort, independent of display pagination, and preserves null scores. `pilot.stream` polls committed RLS-visible revision aggregates; `apps/web/components/live-workspace.ts` coalesces notices/refetches. No names or values are broadcast. A refetch does not make old source data fresh, change formulas or reconstruct historical snapshots. Debug version, period, missing scores and scope; compare independently with `test_pilot.py` and retain snapshot bounds.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

The verified email invitation gave an existing account Viewer membership in another organization; it did not automatically share completed assessment results. An Admin must grant result access through the completed assessment Access panel. Viewer result access shares scores, not private answers or evidence. Organization switching and explicit grants determine the visible cohort, while deterministic score/health formulas remain unchanged. See the [website role/access exercise](../../06-user-guides/MEMBERS_ROLES_AND_ACCESS.md).


## Calendar setup used by the walkthrough

[`capacity.tsx`](../../../apps/web/components/capacity.tsx) exposes Working calendars directly in Resource planning. A calendar is an immutable schedule version: timezone, seven daily hour values and holiday dates. Save a new version and reference it from a dated availability interval; changing a schedule does not rewrite old capacity inputs. [`capacity.py`](../../../services/api/ppm_api/capacity.py) computes from calendar, availability, time off and allocations. Missing coverage remains Unknown. Sensitive actual effort still needs its own grant, including for Admin.

The prepared Northstar records use Asia/Kolkata, weekdays of eight hours and weekends of zero. The walkthrough closes a sprint with ten completed points and reviews the supplied answers independently. Deterministic scores and saved-change notices are current behavior; Broad document intake/OCR/keyword citations are now locally verified in Sprint 09; AI analysis remains PLANNED and never rewrites saved assessment scores. [Current repair evidence](../../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) distinguishes browser verification from external-provider acceptance.
