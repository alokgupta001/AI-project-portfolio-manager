"""Command-center reconciliation, closure history and adversarial access checks."""

from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api.command import combined, workdays
from ppm_api.identity import context, now
from ppm_api.ppm_tables import TABLES
from sqlalchemy.exc import DBAPIError
from test_delivery import change, create, setup
from test_identity import identity as identity
from test_identity import login, send


def test_rule_arithmetic_and_calendar():
    assert combined(Decimal(10), Decimal(10), Decimal(20)) == Decimal("12.5")
    assert combined(None, Decimal(0), Decimal(0)) is None
    calendar = dict.fromkeys(("monday", "tuesday", "wednesday", "thursday", "friday"), 8)
    calendar.update(saturday=0, sunday=0, holidays="2026-10-05,2026-10-06")
    assert workdays(date(2026, 10, 2), date(2026, 10, 7), calendar) == 1
    assert workdays(date(2026, 10, 7), date(2026, 10, 2), calendar) == -1


@pytest.mark.integration
async def test_complete_health_capacity_thresholds_and_currency_scope(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    pid = project["id"]
    project = (await change(c, project, status="active", forecast_end_date="2026-11-08")).json()
    base = await create(c, "baselines", project_id=pid, description="October plan")
    cal = await create(
        c,
        "calendars",
        timezone="Asia/Kolkata",
        monday="8",
        tuesday="8",
        wednesday="8",
        thursday="8",
        friday="8",
        saturday="0",
        sunday="0",
        holidays="",
    )
    await create(c, "budget_lines", project_id=pid, amount="100000", currency="INR", approved=True)
    await create(
        c,
        "metric_plans",
        project_id=pid,
        baseline_id=base["id"],
        calendar_id=cal["id"],
        forecast_cost="110000",
    )
    r = await create(c, "resources")
    start = (now().date() - timedelta(days=100)).isoformat()
    end = (now().date() + timedelta(days=100)).isoformat()
    await create(
        c,
        "availability",
        resource_id=r["id"],
        calendar_id=cal["id"],
        start_date=start,
        end_date=end,
    )
    await create(
        c,
        "allocations",
        resource_id=r["id"],
        project_id=pid,
        hours_per_day="10",
        start_date=start,
        end_date=end,
    )
    usd = await create(c, "projects", portfolio_id=portfolio["id"], currency="USD")
    await create(
        c, "budget_lines", project_id=usd["id"], amount="100", currency="USD", approved=True
    )
    counts = []

    def count_queries(conn, cursor, statement, parameters, context, executemany):
        counts.append(statement.split()[0])

    sa.event.listen(app.state.engine.sync_engine, "before_cursor_execute", count_queries)
    try:
        result = await snap(c)
    finally:
        sa.event.remove(app.state.engine.sync_engine, "before_cursor_execute", count_queries)
    print(
        f"COMMAND_BASELINE projects=2 resources=1 statements={len(counts)} "
        f"compute_ms={result['compute_ms']}"
    )
    first = next(p for p in result["projects"] if p["id"] == pid)
    values = {m["key"]: m for m in first["metrics"]}
    assert Decimal(values["capacity_risk"]["value"]) == 25
    assert abs(Decimal(values["risk"]["value"]) - (Decimal(200) / 21 + Decimal("9.75"))) < Decimal(
        ".00001"
    )
    assert Decimal(values["health"]["coverage_percent"]) == 100
    assert first["computed_health"] == "Green"
    assert Decimal(metric(result, "INR_budget")["value"]) == 100000
    assert Decimal(metric(result, "USD_budget")["value"]) == 100
    resource = result["resources"][0]["summary"]
    assert Decimal(resource["planned_percent"]) == 125
    assert resource["actual_percent"] is None
    policy = await create(c, "metric_policies", amber="10", red="15", stale_days=2)
    assert (
        next(p for p in (await snap(c))["projects"] if p["id"] == pid)["computed_health"] == "Red"
    )
    assert (await change(c, policy, amber="20", red="10")).status_code == 422
    await create(c, "grants", project_id=pid, user_id=str(ids["pm"]), access="read")
    await login(c, emails, "pm", ids["a"])
    limited = await snap(c)
    assert len(limited["projects"]) == 1
    assert metric(limited, "risk", True)["value"] is None
    assert limited["resources"][0]["summary"]["planned_percent"] is None


async def snap(c, portfolio=None, start="2026-10-01", end="2026-11-01"):
    result = await c.get(
        "/api/v1/command/snapshot",
        params={"start": start, "end": end, **({"portfolio_id": portfolio} if portfolio else {})},
    )
    assert result.status_code == 200, result.text
    return result.json()


def metric(snapshot, key, project=False):
    rows = snapshot["projects"][0]["metrics"] if project else snapshot["totals"]
    return next(r for r in rows if r["key"] == key)


@pytest.mark.integration
async def test_command_reconciliation_discrepancy_history_filters(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    project = (
        await change(
            c,
            project,
            status="active",
            ledger_complete=True,
            reported_health="Green",
            forecast_end_date="2026-11-08",
        )
    ).json()
    pid = project["id"]
    await create(c, "budget_lines", project_id=pid, amount="100000", currency="INR", approved=True)
    await create(
        c, "expenditures", project_id=pid, amount="25000", currency="INR", spent_on="2026-10-05"
    )
    await create(
        c, "expenditures", project_id=pid, amount="5000", currency="INR", spent_on="2026-09-05"
    )
    await create(
        c,
        "milestones",
        name="Critical overdue release",
        project_id=pid,
        due_date=(now().date() - timedelta(days=2)).isoformat(),
        critical=True,
    )
    baseline = await create(c, "baselines", project_id=pid, description="Approved schedule")
    cal = await create(
        c,
        "calendars",
        timezone="Asia/Kolkata",
        monday="8",
        tuesday="8",
        wednesday="8",
        thursday="8",
        friday="8",
        saturday="0",
        sunday="0",
        holidays="",
    )
    await create(
        c,
        "metric_plans",
        project_id=pid,
        baseline_id=baseline["id"],
        calendar_id=cal["id"],
        forecast_cost="110000",
    )
    benefit = await create(
        c,
        "benefits",
        project_id=pid,
        unit="hours saved",
        target="100",
        realized="20",
        period_start="2026-10-01",
        period_end="2026-11-01",
    )
    risk = await create(
        c, "risks", project_id=pid, severity=5, likelihood=4, review_on="2026-10-20"
    )
    assert (await change(c, risk, status="mitigating")).status_code == 422
    risk = (
        await change(
            c, risk, status="mitigating", owner_id=str(ids["pm"]), mitigation="Replan release"
        )
    ).json()
    assert (await change(c, risk, status="closed")).status_code == 422
    risk = (await change(c, risk, status="closed", resolution="Mitigation verified")).json()
    assert (await change(c, risk, status="open")).status_code == 409
    assert (await change(c, risk, description="stale revision")).status_code == 200
    assert (await change(c, risk, description="lost edit")).status_code == 412
    team = await create(c, "teams")
    sprint = await create(
        c,
        "sprints",
        project_id=pid,
        team_id=team["id"],
        start_date="2026-10-01",
        end_date="2026-10-15",
    )
    work = await create(c, "work_items", project_id=pid, sprint_id=sprint["id"], points="8")
    for status in ("ready", "in_progress", "done"):
        work = (await change(c, work, status=status)).json()
    sprint = (await change(c, sprint, status="active")).json()
    sprint = (await change(c, sprint, status="closed")).json()
    assert (await change(c, sprint, end_date="2026-10-16")).status_code == 409
    # Later edits to completed work must not rewrite accepted velocity.
    assert (await change(c, work, points="13")).status_code == 200
    result = await snap(c, portfolio["id"])
    assert metric(result, "alignment", True)["coverage_percent"] == "0"
    assert result["projects"][0]["discrepancy"]
    assert metric(result, "health", True)["value"] is None  # no staffing source
    assert Decimal(metric(result, "financial_risk", True)["value"]) == 10
    assert Decimal(metric(result, "INR_spend")["value"]) == 30000
    assert Decimal(metric(result, "INR_period_spend")["value"]) == 25000
    assert Decimal(metric(result, "INR_usage")["value"]) == 30
    assert Decimal(result["velocity"][0]["points"]) == 8
    summary = (await c.get("/api/v1/delivery/project-summary/" + pid)).json()
    assert Decimal(summary["money"][0]["recorded_spend"]) == Decimal(
        metric(result, "INR_spend")["value"]
    )
    assert any(r["id"] == benefit["id"] for r in result["records"])
    period = await snap(c, start="2026-10-10", end="2026-10-14")
    assert period["velocity"] == []
    assert not any(r["data"]["kind"] == "benefits" for r in period["records"])
    assert Decimal(metric(period, "INR_period_spend")["value"]) == 0
    async with owner.begin() as conn:
        await conn.execute(
            TABLES["projects"]
            .update()
            .where(TABLES["projects"].c.id == UUID(pid))
            .values(updated_at=now() - timedelta(days=30))
        )
    assert metric(await snap(c), "health", True)["freshness"] == "stale"
    # App-role SQL cannot rewrite closure history, even as tenant Admin.
    with pytest.raises(DBAPIError):
        async with app.state.engine.begin() as conn:
            await context(conn, ids["admin"], ids["a"], "Admin")
            await conn.execute(TABLES["sprint_closures"].update().values(points=999))


@pytest.mark.integration
async def test_command_scopes_personal_views_rls_csrf_and_replay(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    risk = await create(
        c, "risks", project_id=project["id"], severity=3, likelihood=2, review_on="2026-10-12"
    )
    personal = await create(
        c,
        "saved_views",
        user_id=str(ids["admin"]),
        start_date="2026-10-01",
        end_date="2026-11-01",
        portfolio_id=portfolio["id"],
    )
    await login(c, emails, "viewer", ids["a"])
    assert (await snap(c))["projects"] == []
    assert (await c.get("/api/v1/delivery/saved_views")).json()["items"] == []
    assert (await c.get("/api/v1/delivery/saved_views/" + personal["id"])).status_code == 404
    own = await create(
        c, "saved_views", user_id=str(ids["viewer"]), start_date="2026-10-01", end_date="2026-11-01"
    )
    assert (await change(c, own, archived=True)).status_code == 200
    assert (
        await send(
            c,
            "POST",
            "/delivery/saved_views",
            headers={"idempotency-key": str(uuid4())},
            json={**own["data"], "archived": False, "user_id": str(ids["admin"])},
        )
    ).status_code == 403
    assert (
        await send(
            c,
            "POST",
            "/delivery/risks",
            headers={"idempotency-key": str(uuid4())},
            json=risk["data"],
        )
    ).status_code == 403
    await login(c, emails, "admin", ids["a"])
    grant = await create(
        c, "grants", user_id=str(ids["pm"]), project_id=project["id"], access="edit"
    )
    await login(c, emails, "pm", ids["a"])
    key = str(uuid4())
    r = await send(
        c, "POST", "/delivery/risks", headers={"idempotency-key": key}, json=risk["data"]
    )
    assert r.status_code == 201
    assert (
        await send(
            c, "POST", "/delivery/risks", headers={"idempotency-key": key}, json=risk["data"]
        )
    ).json()["id"] == r.json()["id"]
    assert (
        await send(
            c,
            "POST",
            "/delivery/risks",
            headers={"idempotency-key": key},
            json=risk["data"] | {"severity": 4},
        )
    ).status_code == 409
    assert len((await snap(c))["projects"]) == 1
    assert (await c.post("/api/v1/delivery/risks", json=risk["data"])).status_code == 403
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["b"], "Viewer")
        for kind in (
            "risks",
            "saved_views",
            "metric_plans",
            "benefits",
            "sprint_closures",
            "metric_policies",
        ):
            assert not (await conn.execute(sa.select(TABLES[kind]))).first()
    await login(c, emails, "admin", ids["a"])
    assert (await change(c, grant, archived=True)).status_code == 200
    await login(c, emails, "pm", ids["a"])
    assert (
        await send(
            c, "POST", "/delivery/risks", headers={"idempotency-key": key}, json=risk["data"]
        )
    ).status_code == 404
    assert (await snap(c))["projects"] == []
    assert (
        await c.get(
            "/api/v1/command/snapshot",
            params={"start": "2026-10-01", "end": "2026-11-01", "portfolio_id": portfolio["id"]},
        )
    ).status_code == 404
    assert (
        await c.get("/api/v1/command/snapshot", params={"start": "2026-11-01", "end": "2026-10-01"})
    ).status_code == 422
