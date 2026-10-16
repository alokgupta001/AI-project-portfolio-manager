"""Authorized current-state metrics with explicit period facts and missing inputs."""

from datetime import date, datetime, timedelta
from decimal import Decimal
from time import perf_counter
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

import sqlalchemy as sa
from fastapi import APIRouter, Request

import ppm_api.command_tables  # noqa: F401 — worker callers also need the metric registry
from ppm_api import capacity, delivery
from ppm_api.command_schemas import CommandSnapshot
from ppm_api.identity import Auth, now
from ppm_api.metric_math import alignment_score, budget_usage
from ppm_api.ppm_tables import TABLES

router = APIRouter(prefix="/api/v1/command", tags=["Command center"])
ZERO = Decimal(0)
HUNDRED = Decimal(100)
DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def workdays(start: date, end: date, calendar: dict) -> int:
    """Signed scheduled working dates in (start,end], using an immutable calendar."""
    if end < start:
        return -workdays(end, start, calendar)
    if (end - start).days > 36600:
        delivery.fail(422, "Schedule range exceeds 100 years")
    holidays = set(calendar["holidays"].split(","))
    return sum(
        calendar[DAYS[(start + timedelta(days=i)).weekday()]] > 0
        and (start + timedelta(days=i)).isoformat() not in holidays
        for i in range(1, (end - start).days + 1)
    )


def combined(
    schedule: Decimal | None, financial: Decimal | None, staffing: Decimal | None
) -> Decimal | None:
    if schedule is None or financial is None or staffing is None:
        return None
    return schedule * Decimal(".4") + financial * Decimal(".35") + staffing * Decimal(".25")


def clamped(value: Decimal) -> Decimal:
    return max(ZERO, min(HUNDRED, value))


@router.get("/snapshot", response_model=CommandSnapshot)
async def snapshot(
    start: date, end: date, request: Request, p: Auth, portfolio_id: UUID | None = None
) -> dict:
    began = perf_counter()
    capacity.bounded(start, end)
    # All delivery/identity mutations use this lock; source facts remain mutually consistent.
    await delivery.lock(p, request)
    stamp = now()
    if portfolio_id:
        await delivery.get(p, "portfolios", portfolio_id, True)

    async def load(kind: str, *where: Any) -> list[dict]:
        t = TABLES[kind]
        values = [
            dict(r)
            for r in (
                await p.conn.execute(
                    sa.select(t)
                    .where(
                        t.c.organization_id == p.session["organization_id"],
                        ~t.c.archived,
                        *where,
                    )
                    .order_by(t.c.id)
                    .limit(5001)
                )
            ).mappings()
        ]
        if len(values) > 5000:
            delivery.fail(422, "Snapshot exceeds 5000 source rows; narrow the portfolio filter")
        return values

    settings = await load("settings")
    timezone = settings[0]["timezone"] if settings else "UTC"
    today = stamp.astimezone(ZoneInfo(timezone)).date()
    policy = await load("metric_policies")
    amber, red, stale_days = (
        (policy[0]["amber"], policy[0]["red"], policy[0]["stale_days"])
        if policy
        else (Decimal(30), Decimal(60), 7)
    )
    projects = await load(
        "projects", *([TABLES["projects"].c.portfolio_id == portfolio_id] if portfolio_id else [])
    )
    if len(projects) > 200:
        delivery.fail(422, "Snapshot exceeds 200 projects; select a smaller portfolio")
    ids = [r["id"] for r in projects]
    sources = {}
    for kind in (
        "budget_lines",
        "expenditures",
        "alignments",
        "baselines",
        "milestones",
        "blockers",
        "dependencies",
        "risks",
        "benefits",
        "metric_plans",
        "sprints",
        "sprint_closures",
        "allocations",
    ):
        sources[kind] = await load(kind, TABLES[kind].c.project_id.in_(ids))
    calendars = {r["id"]: r for r in await load("calendars")}

    def freshness(updated: datetime | None) -> str:
        return (
            "missing"
            if updated is None
            else "stale"
            if stamp - updated > timedelta(days=stale_days)
            else "fresh"
        )

    def fact(kind: str, row: dict, detail: str) -> dict:
        return dict(
            id=row["id"], kind=kind, name=row["name"], detail=detail, updated_at=row["updated_at"]
        )

    def metric(
        key: str,
        label: str,
        value: Decimal | int | None,
        unit: str,
        period: str,
        source: str,
        rows: list[dict],
        explanation: str = "",
        coverage: Decimal = HUNDRED,
        partial: bool = False,
    ) -> dict:
        updated = min((r["updated_at"] for r in rows), default=None)
        return dict(
            key=key,
            label=label,
            value=value,
            unit=unit,
            period=period,
            source=source,
            source_updated_at=updated,
            freshness=freshness(updated),
            status="unknown" if value is None else "partial" if partial else "available",
            coverage_percent=ZERO if value is None and coverage == HUNDRED else coverage,
            explanation=explanation,
            facts=rows,
        )

    current = f"Current snapshot {today}; not a historical reconstruction"
    period = f"{start} to {end} (end excluded)"
    resource_ids = sorted(
        {
            r["resource_id"]
            for r in sources["allocations"]
            if r["start_date"] < max(end, today + timedelta(days=28))
            and r["end_date"] > min(start, today)
        }
    )
    if len(resource_ids) > 100:
        delivery.fail(422, "Snapshot exceeds 100 assigned resources; narrow the portfolio filter")
    resource_results, future_capacity = [], {}
    capacity_facts: dict[UUID, list[dict]] = {}
    for rid in resource_ids:
        result = await capacity.summary(p, rid, start, end)
        future_capacity[rid] = await capacity.summary(p, rid, today, today + timedelta(days=28))
        # Capacity is whole-resource only for Admin; never infer full utilization from hidden work.
        inputs = await capacity.sources_for(p, rid, False)
        capacity_facts[rid] = [
            fact(kind, r, f"Capacity source for resource {rid}")
            for kind, rows in inputs.items()
            for r in rows
        ]
        updated = min((r["updated_at"] for rows in inputs.values() for r in rows), default=None)
        resource_results.append(
            dict(summary=result, source_updated_at=updated, freshness=freshness(updated))
        )
    output, records, velocities = [], [], []
    currency_totals: dict[str, dict] = {}
    for project in projects:
        pid = project["id"]
        src = {k: [r for r in rows if r["project_id"] == pid] for k, rows in sources.items()}
        pf = fact("projects", project, "Current project declaration")
        metrics = []
        budget = sum((r["amount"] for r in src["budget_lines"] if r["approved"]), ZERO)
        spent = sum((r["amount"] for r in src["expenditures"]), ZERO)
        in_period = sum(
            (r["amount"] for r in src["expenditures"] if start <= r["spent_on"] < end), ZERO
        )
        money_facts = (
            [
                fact("budget_lines", r, f"Approved {r['amount']} {r['currency']}")
                for r in src["budget_lines"]
                if r["approved"]
            ]
            + [
                fact("expenditures", r, f"{r['spent_on']}: {r['amount']} {r['currency']}")
                for r in src["expenditures"]
            ]
            + [pf]
        )
        complete = project["ledger_complete"]
        usage = budget_usage(spent, budget, complete)
        metrics += [
            metric(
                "budget",
                "Approved budget",
                budget,
                project["currency"],
                current,
                "Approved budget lines",
                money_facts,
            ),
            metric(
                "spend",
                "Recorded spend",
                spent,
                project["currency"],
                current,
                "Expenditure including reversals",
                money_facts,
                "Ledger incomplete" if not complete else "Ledger declared complete",
                partial=not complete,
            ),
            metric(
                "period_spend",
                "Period recorded spend",
                in_period,
                project["currency"],
                period,
                "Expenditure spent_on",
                money_facts,
                partial=not complete,
            ),
            metric(
                "usage",
                "Budget use",
                usage,
                "%",
                current,
                "Recorded spend / approved budget",
                money_facts,
                "Unknown when ledger incomplete or budget zero",
            ),
        ]
        ct = currency_totals.setdefault(
            project["currency"], dict(budget=ZERO, spent=ZERO, period=ZERO, complete=True, facts=[])
        )
        ct["budget"] += budget
        ct["spent"] += spent
        ct["period"] += in_period
        ct["complete"] &= complete
        ct["facts"] += money_facts
        aligns = src["alignments"]
        alignment = alignment_score(aligns)
        metrics.append(
            metric(
                "alignment",
                "Strategic alignment",
                alignment,
                "%",
                current,
                "Declared goal weights and contribution",
                [
                    fact("alignments", r, f"Weight {r['weight']}; contribution {r['contribution']}")
                    for r in aligns
                ],
                "Unknown unless weights total 1",
            )
        )
        plans = src["metric_plans"]
        plan = plans[0] if plans else None
        baseline = next(
            (r for r in src["baselines"] if plan and r["id"] == plan["baseline_id"]), None
        )
        calendar = calendars.get(plan["calendar_id"]) if plan else None
        baseline_project = baseline["snapshot"].get("project", {}) if baseline else {}
        target = baseline_project.get("target_end_date")
        beginning = baseline_project.get("start_date")
        finish = (
            project["actual_end_date"]
            if project["status"] == "completed"
            else project["forecast_end_date"]
        )
        variance = (
            workdays(date.fromisoformat(target), finish, calendar)
            if target and finish and calendar
            else None
        )
        duration = (
            workdays(date.fromisoformat(beginning), date.fromisoformat(target), calendar)
            if beginning and target and calendar
            else None
        )
        schedule = (
            clamped(Decimal(max(0, variance)) / max(1, duration) * 100)
            if variance is not None and duration is not None
            else None
        )
        financial = (
            clamped((plan["forecast_cost"] - budget) / budget * 100)
            if plan and plan["forecast_cost"] is not None and budget > 0
            else None
        )
        assigned = {
            r["resource_id"]
            for r in src["allocations"]
            if r["start_date"] < today + timedelta(days=28) and r["end_date"] > today
        }
        futures = [future_capacity[rid] for rid in assigned]
        capacity_known = bool(futures) and all(
            r["scope"] == "full_resource"
            and r["available_hours"] is not None
            and r["excess_hours"] is not None
            for r in futures
        )
        available = sum((r["available_hours"] for r in futures), ZERO) if capacity_known else None
        staffing = (
            clamped(sum((r["excess_hours"] for r in futures), ZERO) / available * 100)
            if available
            else None
        )
        risk = combined(schedule, financial, staffing)
        health = (
            "Unknown"
            if risk is None
            else "Red"
            if risk >= red
            else "Amber"
            if risk >= amber
            else "Green"
        )
        evidence = (
            [pf]
            + (
                [
                    fact(
                        "metric_plans",
                        plan,
                        f"Forecast cost {plan['forecast_cost']}; calendar {plan['calendar_id']}",
                    )
                ]
                if plan
                else []
            )
            + (
                [fact("baselines", baseline, f"Frozen baseline finish {target}")]
                if baseline
                else []
            )
        )
        overdue = [
            r
            for r in src["milestones"]
            if r["critical"] and not r["actual_date"] and r["due_date"] < today
        ]
        evidence += [
            fact("milestones", r, f"Critical milestone overdue since {r['due_date']}")
            for r in overdue
        ]
        evidence += [
            fact(
                "allocations",
                r,
                f"{r['hours_per_day']} hours per scheduled day; resource {r['resource_id']}",
            )
            for r in src["allocations"]
            if r["resource_id"] in assigned
        ]
        evidence += [f for rid in assigned for f in capacity_facts[rid]]
        evidence += money_facts
        if calendar:
            evidence.append(
                fact("calendars", calendar, "Immutable schedule calendar with holidays")
            )
        # Milestone variance compares actual/current planned finish to the frozen baseline.
        frozen_milestones = (
            baseline["snapshot"].get("items", {}).get("milestones", []) if baseline else []
        )
        for milestone in src["milestones"]:
            original = next((m for m in frozen_milestones if m["id"] == str(milestone["id"])), None)
            delta = (
                workdays(
                    date.fromisoformat(original["due_date"]),
                    milestone["actual_date"] or milestone["due_date"],
                    calendar,
                )
                if original and calendar
                else None
            )
            metrics.append(
                metric(
                    "milestone_" + str(milestone["id"]),
                    milestone["name"] + " variance",
                    delta,
                    "working days",
                    current,
                    "Frozen milestone baseline and actual/current planned date",
                    [
                        fact(
                            "milestones",
                            milestone,
                            (
                                f"Baseline {original['due_date'] if original else 'missing'}; "
                                f"actual {milestone['actual_date']}; "
                                f"planned {milestone['due_date']}"
                            ),
                        )
                    ],
                    "Positive is late; planned variance until actual completion",
                    HUNDRED if delta is not None else ZERO,
                )
            )
        coverage = Decimal(sum(v is not None for v in (schedule, financial, staffing))) / 3 * 100
        for key, label, value, unit, explanation in (
            (
                "variance",
                "Finish variance",
                variance,
                "working days",
                "Actual/forecast minus frozen baseline, immutable calendar; positive is late",
            ),
            (
                "schedule_risk",
                "Schedule component",
                schedule,
                "risk points",
                "Positive delay / baseline working duration, capped 100",
            ),
            (
                "financial_risk",
                "Financial component",
                financial,
                "risk points",
                "Positive forecast overrun / approved budget, capped 100",
            ),
            (
                "capacity_risk",
                "Capacity component",
                staffing,
                "risk points",
                (
                    f"Excess / capacity, {today} to {today + timedelta(days=28)}; "
                    "unknown with insufficient scope"
                ),
            ),
            (
                "risk",
                "Deterministic risk",
                risk,
                "risk points",
                "risk-rule-v1: 40% schedule + 35% financial + 25% capacity; not a probability",
            ),
            (
                "health",
                "Evidence health",
                HUNDRED - risk if risk is not None else None,
                "health points",
                "100 minus risk; higher is healthier; all three inputs required",
            ),
            (
                "critical",
                "Overdue critical milestones",
                Decimal(len(overdue)),
                "milestones",
                "Open critical milestones with due date before today",
            ),
        ):
            metrics.append(
                metric(
                    key,
                    label,
                    value,
                    unit,
                    current,
                    "Versioned plan, delivery and capacity-v1",
                    evidence,
                    explanation,
                    coverage
                    if key in ("risk", "health")
                    else HUNDRED
                    if value is not None
                    else ZERO,
                )
            )
        order = {"Unknown": -1, "Green": 0, "Amber": 1, "Red": 2}
        discrepancy = project["reported_health"] != "Unknown" and (
            order[health] > order[project["reported_health"]]
            or project["reported_health"] == "Green"
            and bool(overdue)
        )
        output.append(
            dict(
                id=pid,
                name=project["name"],
                portfolio_id=project["portfolio_id"],
                reported_health=project["reported_health"],
                computed_health=health,
                discrepancy=discrepancy,
                metrics=metrics,
                can_edit=await delivery.can_edit(p, pid),
            )
        )
        for kind in ("risks", "benefits", "blockers", "dependencies", "milestones"):
            rows = src[kind]
            if kind == "benefits":
                rows = [r for r in rows if r["period_start"] >= start and r["period_end"] <= end]
            records += [delivery.view(kind, r) for r in rows]
        for sprint in src["sprints"]:
            if sprint["status"] == "closed" and start <= sprint["end_date"] < end:
                closure = next(
                    (r for r in src["sprint_closures"] if r["sprint_id"] == sprint["id"]), None
                )
                velocities.append(
                    dict(
                        sprint_id=sprint["id"],
                        project_id=pid,
                        team_id=sprint["team_id"],
                        name=sprint["name"],
                        end_date=sprint["end_date"],
                        points=closure["points"] if closure and closure["complete"] else None,
                        recorded_points=closure["points"] if closure else ZERO,
                        source_updated_at=closure["created_at"] if closure else None,
                        freshness="frozen" if closure else "missing",
                    )
                )
    totals = []
    for currency, ct in sorted(currency_totals.items()):
        for key, label, value, unit in (
            ("budget", "Approved budget", ct["budget"], currency),
            ("spend", "Recorded spend", ct["spent"], currency),
            ("period_spend", "Period recorded spend", ct["period"], currency),
            (
                "usage",
                "Budget use",
                budget_usage(ct["spent"], ct["budget"], ct["complete"]),
                "%",
            ),
        ):
            totals.append(
                metric(
                    f"{currency}_{key}",
                    f"{currency} {label}",
                    value,
                    unit,
                    period if key == "period_spend" else current,
                    "Authorized project ledger totals",
                    ct["facts"],
                    "No FX conversion; current authorized scope",
                    partial=not ct["complete"],
                )
            )
    for key, label in (
        ("health", "Portfolio evidence health"),
        ("alignment", "Portfolio strategic alignment"),
    ):
        active_ids = {r["id"] for r in projects if r["status"] in ("active", "on_hold")}
        eligible = [r for r in output if key != "health" or r["id"] in active_ids]
        ms = [
            m for r in eligible for m in r["metrics"] if m["key"] == key and m["value"] is not None
        ]
        totals.append(
            metric(
                key,
                label,
                sum((m["value"] for m in ms), ZERO) / len(ms) if ms else None,
                "health points" if key == "health" else "%",
                current,
                "Equal-weight mean of covered projects",
                [f for m in ms for f in m["facts"]],
                f"{len(ms)}/{len(eligible)} eligible projects covered",
                Decimal(len(ms)) / len(eligible) * 100 if eligible else ZERO,
                len(ms) < len(eligible),
            )
        )
    active_health = [
        m
        for r in output
        if any(pj["id"] == r["id"] and pj["status"] in ("active", "on_hold") for pj in projects)
        for m in r["metrics"]
        if m["key"] == "health" and m["value"] is not None
    ]
    worst = min(active_health, key=lambda m: m["value"]) if active_health else None
    totals.append(
        metric(
            "worst_health",
            "Worst covered project health",
            worst["value"] if worst else None,
            "health points",
            current,
            "Lowest covered active-project health",
            worst["facts"] if worst else [],
            "Unknown projects excluded and remain unknown",
            HUNDRED if worst else ZERO,
        )
    )
    team_ids = {r["team_id"] for r in projects if r["team_id"]}
    teams = []
    for tid in sorted(team_ids):
        team = await delivery.get(p, "teams", tid)
        teams.append(
            dict(name=team["name"], summary=await capacity.team_summary(tid, start, end, p))
        )
    return dict(
        computed_at=stamp,
        start=start,
        end=end,
        timezone=timezone,
        portfolio_id=portfolio_id,
        policy_revision=policy[0]["revision"] if policy else 0,
        amber=amber,
        red=red,
        stale_days=stale_days,
        projects=output,
        totals=totals,
        records=records,
        velocity=velocities,
        resources=resource_results,
        teams=teams,
        limitations=[
            (
                "Current facts with selected-period spend, benefits, closed sprints and "
                "capacity; no historical reconstruction."
            ),
            (
                "Benefits included only when their full recorded period fits the filter; no "
                "prorating or combining unlike units."
            ),
            (
                "Capacity includes all authorized work for resources assigned to selected "
                "projects; team signals are whole-team and suppress cohorts under five."
            ),
            (
                "Source freshness uses the oldest contributing record; recomputation never "
                "refreshes source facts."
            ),
            (
                "Closed sprints predating closure snapshots remain unknown. No AI "
                "predictions or automated escalation."
            ),
        ],
        compute_ms=round((perf_counter() - began) * 1000, 2),
    )
