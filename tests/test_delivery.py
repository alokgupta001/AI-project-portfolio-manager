"""Sprint 04 end-to-end domain persistence against real restricted PostgreSQL roles."""

import asyncio
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api.identity import context
from ppm_api.ppm_tables import TABLES, audit
from test_identity import identity as identity
from test_identity import login, send

pytestmark = pytest.mark.integration


async def create(c, kind, **values):
    result = await send(
        c,
        "POST",
        "/delivery/" + kind,
        headers={"idempotency-key": str(uuid4())},
        json={"kind": kind, "name": kind + " fixture", **values},
    )
    assert result.status_code == 201, result.text
    return result.json()


async def change(c, row, **values):
    return await send(
        c,
        "PATCH",
        f"/delivery/{row['data']['kind']}/{row['id']}",
        headers={"if-match": str(row["revision"])},
        json=row["data"] | values,
    )


async def setup(identity):
    c, app, owner, ids, emails = identity
    await login(c, emails, org=ids["a"])
    await create(c, "settings", timezone="Asia/Kolkata", currency="INR")
    portfolio = await create(c, "portfolios", name="Platform portfolio")
    project = await create(
        c,
        "projects",
        portfolio_id=portfolio["id"],
        currency="INR",
        start_date="2026-10-01",
        target_end_date="2026-11-01",
    )
    return c, app, owner, ids, emails, portfolio, project


async def test_hierarchy_delivery_money_and_baseline(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    department = await create(c, "departments", owner_id=str(ids["pm"]))
    team = await create(c, "teams", department_id=department["id"])
    await create(
        c, "team_members", team_id=team["id"], user_id=str(ids["pm"]), start_date="2026-10-01"
    )
    goal = await create(c, "goals", name="Improve delivery")
    await create(
        c,
        "alignments",
        portfolio_id=portfolio["id"],
        goal_id=goal["id"],
        weight="1",
        contribution=".8",
    )
    await create(
        c,
        "alignments",
        project_id=project["id"],
        goal_id=goal["id"],
        weight="1",
        contribution=".75",
    )
    program = await create(c, "programs", portfolio_id=portfolio["id"])
    r = await change(
        c,
        project,
        program_id=program["id"],
        team_id=team["id"],
        department_id=department["id"],
        status="active",
        ledger_complete=True,
    )
    assert r.status_code == 200, r.text
    project = r.json()
    sprint = await create(
        c,
        "sprints",
        project_id=project["id"],
        team_id=team["id"],
        start_date="2026-10-01",
        end_date="2026-10-14",
    )
    work = await create(
        c,
        "work_items",
        project_id=project["id"],
        sprint_id=sprint["id"],
        due_date="2026-10-10",
        points="3.50",
    )
    assert (await change(c, work, status="ready")).status_code == 200
    await create(c, "milestones", project_id=project["id"], due_date="2026-11-01", critical=True)
    await create(
        c,
        "blockers",
        project_id=project["id"],
        work_item_id=work["id"],
        description="Awaiting approval",
    )
    await create(c, "budget_lines", project_id=project["id"], amount="1000.10", currency="INR")
    spend = await create(
        c,
        "expenditures",
        project_id=project["id"],
        amount="300.03",
        currency="INR",
        spent_on="2026-10-05",
    )
    await create(
        c,
        "expenditures",
        project_id=project["id"],
        amount="-300.03",
        currency="INR",
        spent_on="2026-10-06",
        reversal_of=spend["id"],
    )
    await create(
        c,
        "expenditures",
        project_id=project["id"],
        amount="250.01",
        currency="INR",
        spent_on="2026-10-06",
    )
    await create(c, "baselines", project_id=project["id"], description="Approved initial plan")
    r = await change(c, project, forecast_end_date="2026-11-15")
    assert r.status_code == 200
    await create(c, "baselines", project_id=project["id"], description="Forecast reviewed")
    summary = (await c.get("/api/v1/delivery/project-summary/" + project["id"])).json()
    assert summary["money"][0]["approved_budget"] == "1000.10"
    assert summary["money"][0]["recorded_spend"] == "250.01"
    assert Decimal(summary["alignment_percent"]) == 75
    assert summary["computed_health"] is None
    assert summary["baselines"][1]["snapshot"]["project"]["forecast_end_date"] is None
    assert summary["baselines"][0]["snapshot"]["project"]["forecast_end_date"] == "2026-11-15"
    assert summary["baselines"][1]["snapshot"]["items"]["budget_lines"][0]["amount"] == "1000.10"
    assert (await change(c, r.json(), archived=True)).status_code == 200
    async with owner.connect() as conn:
        assert (
            await conn.scalar(
                sa.select(sa.func.count())
                .select_from(audit)
                .where(audit.c.organization_id == ids["a"])
            )
            >= 15
        )


async def test_scope_grants_and_live_revocation(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    hidden = await create(
        c, "projects", portfolio_id=portfolio["id"], currency="INR", name="Hidden"
    )
    read = await create(
        c, "grants", user_id=str(ids["viewer"]), project_id=project["id"], access="read"
    )
    await create(c, "grants", user_id=str(ids["pm"]), project_id=project["id"], access="edit")
    await login(c, emails, "viewer", ids["a"])
    listing = (await c.get("/api/v1/delivery/projects")).json()
    assert [r["id"] for r in listing["items"]] == [project["id"]]
    assert (await c.get("/api/v1/delivery/projects/" + hidden["id"])).status_code == 404
    assert (await change(c, project, name="Forbidden")).status_code == 403
    await login(c, emails, "pm", ids["a"])
    assert (await change(c, project, name="Permitted")).status_code == 200
    assert (await change(c, hidden, name="Forbidden")).status_code == 404
    current = (await c.get("/api/v1/delivery/projects/" + project["id"])).json()
    assert (await change(c, current, archived=True)).status_code == 403
    await login(c, emails, org=ids["a"])
    assert (await change(c, read, archived=True)).status_code == 200
    await login(c, emails, "viewer", ids["a"])
    assert (await c.get("/api/v1/delivery/projects/" + project["id"])).status_code == 404


async def test_idempotency_versions_dates_and_cross_tenant(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    key = str(uuid4())
    body = {"kind": "goals", "name": "Idempotent goal"}
    first = await send(c, "POST", "/delivery/goals", headers={"idempotency-key": key}, json=body)
    second = await send(c, "POST", "/delivery/goals", headers={"idempotency-key": key}, json=body)
    assert (
        first.status_code == second.status_code == 201 and first.json()["id"] == second.json()["id"]
    )
    assert (
        await send(
            c,
            "POST",
            "/delivery/goals",
            headers={"idempotency-key": key},
            json=body | {"name": "Changed"},
        )
    ).status_code == 409
    assert (await change(c, project, target_end_date="2026-09-01")).status_code == 422
    assert (await change(c, project, name="First")).status_code == 200
    assert (await change(c, project, name="Stale")).status_code == 412
    assert (
        await send(c, "PATCH", "/delivery/projects/" + project["id"], json=project["data"])
    ).status_code == 428
    assert (
        await send(
            c,
            "POST",
            "/delivery/goals",
            headers={"idempotency-key": str(uuid4()), "x-organization-id": str(ids["b"])},
            json=body,
        )
    ).status_code == 409
    await login(c, emails, "other", ids["b"])
    await create(c, "settings", timezone="UTC", currency="USD")
    bad = await send(
        c,
        "POST",
        "/delivery/projects",
        headers={"idempotency-key": str(uuid4())},
        json={
            "kind": "projects",
            "name": "Bad parent",
            "portfolio_id": portfolio["id"],
            "currency": "USD",
        },
    )
    assert bad.status_code == 404


async def test_dependencies_cycle_and_same_project_references(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    other = await create(c, "projects", portfolio_id=portfolio["id"], currency="INR")
    a = await create(c, "work_items", project_id=project["id"])
    b = await create(c, "work_items", project_id=project["id"])
    await create(
        c,
        "dependencies",
        project_id=project["id"],
        target_project_id=project["id"],
        source_work_item_id=a["id"],
        target_work_item_id=b["id"],
    )
    for data in [
        {
            "project_id": project["id"],
            "target_project_id": project["id"],
            "source_work_item_id": b["id"],
            "target_work_item_id": a["id"],
        },
        {
            "project_id": other["id"],
            "target_project_id": project["id"],
            "source_work_item_id": a["id"],
        },
    ]:
        r = await send(
            c,
            "POST",
            "/delivery/dependencies",
            headers={"idempotency-key": str(uuid4())},
            json={"kind": "dependencies", "name": "Bad edge", **data},
        )
        assert r.status_code in (409, 422), r.text
    await create(c, "dependencies", project_id=project["id"], target_project_id=other["id"])
    r = await send(
        c,
        "POST",
        "/delivery/dependencies",
        headers={"idempotency-key": str(uuid4())},
        json={
            "kind": "dependencies",
            "name": "Cycle",
            "project_id": other["id"],
            "target_project_id": project["id"],
        },
    )
    assert r.status_code == 409


async def test_money_immutability_and_program_constraints(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    second = await create(c, "portfolios")
    program = await create(c, "programs", portfolio_id=second["id"])
    assert (await change(c, project, program_id=program["id"])).status_code == 422
    for values in [
        {"amount": "10.001", "currency": "INR"},
        {"amount": "10", "currency": "USD"},
        {"amount": "-1", "currency": "INR"},
    ]:
        r = await send(
            c,
            "POST",
            "/delivery/budget_lines",
            headers={"idempotency-key": str(uuid4())},
            json={"kind": "budget_lines", "name": "Invalid", "project_id": project["id"], **values},
        )
        assert r.status_code == 422, r.text
    expense = await create(
        c,
        "expenditures",
        project_id=project["id"],
        amount="1.01",
        currency="INR",
        spent_on="2026-10-01",
    )
    assert (await change(c, expense, amount="2.02")).status_code == 409
    baseline = await create(c, "baselines", project_id=project["id"], description="Approved")
    assert (await change(c, baseline, description="Overwrite")).status_code == 409
    summary = (await c.get("/api/v1/delivery/project-summary/" + project["id"])).json()
    assert (
        summary["money"][0]["usage_percent"] is None and not summary["money"][0]["ledger_complete"]
    )


async def test_real_rls_missing_context_and_foreign_keys(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    async with app.state.engine.begin() as conn:
        assert not await conn.scalar(sa.select(TABLES["projects"].c.id))
        await context(conn, ids["viewer"], ids["a"], "Viewer")
        assert not await conn.scalar(sa.select(TABLES["projects"].c.id))
        await context(conn, ids["admin"], ids["a"], "Admin")
        assert await conn.scalar(sa.select(TABLES["projects"].c.id))
        flags = (
            await conn.execute(
                sa.text("SELECT rolsuper,rolbypassrls FROM pg_roles WHERE rolname=current_user")
            )
        ).one()
        assert not any(flags)
    async with app.state.engine.begin() as conn:
        assert not await conn.scalar(sa.select(TABLES["projects"].c.id))


async def test_pm_portfolio_creation_and_concurrent_revision(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    await create(c, "grants", user_id=str(ids["pm"]), portfolio_id=portfolio["id"], access="manage")
    await login(c, emails, "pm", ids["a"])
    own = await create(c, "projects", portfolio_id=portfolio["id"], currency="INR")
    assert (await c.get("/api/v1/delivery/project-summary/" + own["id"])).json()["can_manage"]
    results = await asyncio.gather(
        change(c, own, name="Concurrent A"), change(c, own, name="Concurrent B")
    )
    assert sorted(r.status_code for r in results) == [200, 412]


async def test_currency_groups_and_scoped_portfolio_totals(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    usd = await create(c, "projects", portfolio_id=portfolio["id"], currency="USD")
    await create(c, "budget_lines", project_id=project["id"], amount="100.01", currency="INR")
    await create(c, "budget_lines", project_id=usd["id"], amount="200.02", currency="USD")
    result = (await c.get("/api/v1/delivery/portfolio-summary/" + portfolio["id"])).json()
    assert {x["currency"]: x["approved_budget"] for x in result["money"]} == {
        "INR": "100.01",
        "USD": "200.02",
    }
    await create(c, "grants", user_id=str(ids["viewer"]), project_id=project["id"], access="read")
    await login(c, emails, "viewer", ids["a"])
    result = (await c.get("/api/v1/delivery/portfolio-summary/" + portfolio["id"])).json()
    assert result["visible_projects"] == 1 and [x["currency"] for x in result["money"]] == ["INR"]


async def test_database_rejects_foreign_parent_and_ledger_mutation(identity):
    from sqlalchemy.exc import DBAPIError

    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    expense = await create(
        c,
        "expenditures",
        project_id=project["id"],
        amount="2.01",
        currency="INR",
        spent_on="2026-10-01",
    )
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(
                    TABLES["expenditures"]
                    .update()
                    .where(TABLES["expenditures"].c.id == UUID(expense["id"]))
                    .values(amount=Decimal(3))
                )
        original = dict(
            (
                await conn.execute(
                    sa.select(TABLES["projects"]).where(
                        TABLES["projects"].c.id == UUID(project["id"])
                    )
                )
            )
            .mappings()
            .one()
        )
        original.update(id=uuid4(), organization_id=ids["b"], created_by=ids["other"])
        await context(conn, ids["other"], ids["b"], "Admin")
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(TABLES["projects"].insert().values(**original))


async def test_seed_refuses_non_demo_database(identity):
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "scripts/seed_delivery_demo.py"], capture_output=True, text=True
    )
    assert (
        result.returncode != 0
        and "Refusing business fixture writes outside demo/ppm_demo" in result.stderr
    )
