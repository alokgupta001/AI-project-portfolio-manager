"""Capacity acceptance against real PostgreSQL RLS and existing identity controls."""

import asyncio
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from ppm_api.identity import context
from ppm_api.ppm_tables import TABLES, audit
from sqlalchemy.exc import DBAPIError
from test_delivery import change, create, setup
from test_identity import identity as identity
from test_identity import login, send

pytestmark = pytest.mark.integration


async def calendar(c, hours="4", **extra):
    return await create(
        c,
        "calendars",
        timezone="America/New_York",
        holidays="2026-03-10",
        **dict.fromkeys(("monday", "tuesday", "wednesday", "thursday", "friday"), hours),
        saturday="0",
        sunday="0",
        **extra,
    )


async def fixture(identity):
    c, app, owner, ids, emails, portfolio, project = await setup(identity)
    resource = await create(c, "resources", name="Independent resource")
    cal = await calendar(c)
    await create(
        c,
        "availability",
        resource_id=resource["id"],
        calendar_id=cal["id"],
        start_date="2026-01-01",
        end_date="2027-01-01",
    )
    second = await create(c, "projects", portfolio_id=portfolio["id"], currency="INR")
    return c, app, owner, ids, emails, project, second, resource, cal


async def summary(c, resource, start="2026-03-09", end="2026-03-16", **params):
    r = await c.get(
        "/api/v1/capacity/resources/" + resource["id"], params=dict(start=start, end=end, **params)
    )
    assert r.status_code == 200, r.text
    return r.json()


async def allocation(c, resource, project, hours="3", **extra):
    return await create(
        c,
        "allocations",
        resource_id=resource["id"],
        project_id=project["id"],
        start_date="2026-03-09",
        end_date="2026-03-23",
        hours_per_day=hours,
        **extra,
    )


async def test_split_capacity_leave_holiday_zero_and_snapshot_history(identity):
    c, app, owner, ids, emails, project, second, resource, cal = await fixture(identity)
    a = await allocation(c, resource, project)
    await allocation(c, resource, second)
    await create(
        c,
        "time_off",
        resource_id=resource["id"],
        start_date="2026-03-11",
        end_date="2026-03-13",
        hours_per_day="4",
    )
    await create(c, "milestones", project_id=project["id"], due_date="2026-03-12")
    s = await summary(c, resource)
    assert Decimal(s["available_hours"]) == 8
    assert Decimal(s["allocated_hours"]) == 30
    assert Decimal(s["excess_hours"]) == 22
    assert sum(Decimal(w["allocated_hours"]) for w in s["weeks"]) == 30
    assert sum(Decimal(w["excess_hours"]) for w in s["weeks"]) == 22
    assert Decimal(s["planned_percent"]) == 375
    assert s["days"][1]["planned_percent"] is None
    assert Decimal(s["days"][1]["excess_hours"]) == 6
    assert s["actual_percent"] is None and not s["effort_complete"]
    # End is exclusive: Friday has capacity again after the two-day leave.
    assert Decimal(s["days"][4]["available_hours"]) == 4
    snap = await create(
        c,
        "capacity_snapshots",
        resource_id=resource["id"],
        start_date="2026-03-09",
        end_date="2026-03-16",
    )
    before = (await c.get("/api/v1/capacity/snapshots/" + snap["id"])).json()
    assert before["snapshot"]["contract"] == "capacity-snapshot-v1"
    assert not before["snapshot"]["sources"]["effort"]
    assert (await change(c, a, hours_per_day="2")).status_code == 200
    assert (await c.get("/api/v1/capacity/snapshots/" + snap["id"])).json() == before
    assert (await change(c, cal, monday="8")).status_code == 409
    assert (await change(c, snap, name="rewrite")).status_code == 409
    history = (await c.get("/api/v1/delivery/history/allocations/" + a["id"])).json()
    assert len(history) == 2 and Decimal(history[0]["before"]["hours_per_day"]) == 3
    missing = await create(c, "resources")
    assert (await summary(c, missing))["available_hours"] is None


async def test_dst_local_dates_and_part_time_boundary_validation(identity):
    c, app, owner, ids, emails, project, second, resource, cal = await fixture(identity)
    # Calendar dates keep scheduled hours over US spring-forward and fall-back weekends.
    spring = await summary(c, resource, "2026-03-06", "2026-03-10")
    autumn = await summary(c, resource, "2026-10-30", "2026-11-03")
    assert Decimal(spring["available_hours"]) == Decimal(autumn["available_hours"]) == 8
    assert len(spring["days"]) == len(autumn["days"]) == 4
    assert all(d["timezone"] == "America/New_York" for d in spring["days"])
    r = await send(
        c,
        "POST",
        "/delivery/availability",
        headers={"idempotency-key": str(uuid4())},
        json=dict(
            kind="availability",
            name="Overlap",
            resource_id=resource["id"],
            calendar_id=cal["id"],
            start_date="2026-03-01",
            end_date="2026-04-01",
        ),
    )
    assert r.status_code == 409
    for end in ("2026-03-09", "2026-03-08", "2028-01-01"):
        assert (
            await c.get(
                "/api/v1/capacity/resources/" + resource["id"],
                params=dict(start="2026-03-09", end=end),
            )
        ).status_code == 422


async def test_resource_manager_scope_viewer_hidden_projects_and_live_revoke(identity):
    c, app, owner, ids, emails, project, second, resource, cal = await fixture(identity)
    a = await allocation(c, resource, project)
    await allocation(c, resource, second)
    await create(c, "grants", project_id=project["id"], user_id=str(ids["pm"]), access="edit")
    grant = await create(
        c, "resource_access", resource_id=resource["id"], user_id=str(ids["pm"]), manage=True
    )
    await login(c, emails, "pm", ids["a"])
    s = await summary(c, resource)
    async with app.state.engine.begin() as conn:
        await context(conn, ids["pm"], ids["a"], "Project Manager")
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(
                    TABLES["resources"]
                    .update()
                    .where(TABLES["resources"].c.id == UUID(resource["id"]))
                    .values(archived=True)
                )
    assert s["scope"] == "visible_projects_only" and s["planned_percent"] is None
    assert s["excess_hours"] is None and Decimal(s["allocated_hours"]) == 15
    assert second["id"] not in str(s)
    assert (await change(c, resource, archived=True)).status_code == 403
    assert (await change(c, a, hours_per_day="2")).status_code == 200
    r = await send(
        c,
        "POST",
        "/delivery/allocations",
        headers={"idempotency-key": str(uuid4())},
        json=a["data"] | dict(project_id=second["id"]),
    )
    assert r.status_code in (403, 404)
    await login(c, emails, "admin", ids["a"])
    assert (await change(c, grant, archived=True)).status_code == 200
    await login(c, emails, "pm", ids["a"])
    latest = (await c.get("/api/v1/delivery/allocations/" + a["id"])).json()
    assert (await change(c, latest, hours_per_day="1")).status_code == 403
    await login(c, emails, "viewer", ids["a"])
    r = await send(
        c,
        "POST",
        "/delivery/allocations",
        headers={"idempotency-key": str(uuid4())},
        json=a["data"],
    )
    assert r.status_code == 403
    await login(c, emails, "other", ids["b"])
    assert (await c.get("/api/v1/delivery/resources/" + resource["id"])).status_code == 404
    assert (
        await c.get(
            "/api/v1/capacity/resources/" + resource["id"],
            params=dict(start="2026-03-09", end="2026-03-16"),
        )
    ).status_code == 404
    await create(c, "settings", timezone="Asia/Kolkata", currency="INR")
    forged = await send(
        c,
        "POST",
        "/delivery/availability",
        headers={"idempotency-key": str(uuid4())},
        json=dict(
            kind="availability",
            name="forged",
            resource_id=resource["id"],
            calendar_id=cal["id"],
            start_date="2026-01-01",
            end_date="2027-01-01",
        ),
    )
    assert forged.status_code == 404


async def test_sensitive_effort_completeness_and_audit_revocation(identity):
    c, app, owner, ids, emails, project, second, resource, cal = await fixture(identity)
    payload = dict(
        kind="effort",
        name="Timesheet",
        resource_id=resource["id"],
        project_id=project["id"],
        worked_on="2026-03-09",
        hours="4",
        overtime_hours="1",
    )
    assert (
        await send(
            c, "POST", "/delivery/effort", headers={"idempotency-key": str(uuid4())}, json=payload
        )
    ).status_code == 403
    grant = await create(
        c, "resource_access", resource_id=resource["id"], user_id=str(ids["admin"]), effort=True
    )
    effort = await create(c, "effort", **{k: v for k, v in payload.items() if k != "kind"})
    s = await summary(c, resource, "2026-03-09", "2026-03-10")
    assert s["actual_percent"] is None and Decimal(s["actual_hours"]) == 4
    coverage = await create(
        c, "effort_coverage", resource_id=resource["id"], worked_on="2026-03-09", complete=True
    )
    assert (
        Decimal((await summary(c, resource, "2026-03-09", "2026-03-10"))["actual_percent"]) == 100
    )
    assert (await change(c, effort, hours="3")).status_code == 200
    assert not (await summary(c, resource, "2026-03-09", "2026-03-10"))["effort_complete"]
    assert (await change(c, coverage, complete=True)).status_code == 412
    assert (await change(c, grant, effort=False)).status_code == 200
    assert (await c.get("/api/v1/delivery/effort/" + effort["id"])).status_code == 404
    assert (await c.get("/api/v1/delivery/history/effort/" + effort["id"])).status_code == 404
    # Direct SQL through the non-bypass application role must also hide sensitive audit.
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        assert not (await conn.execute(sa.select(audit).where(audit.c.resource == "effort"))).all()


async def test_allocation_concurrency_retry_and_database_isolation(identity):
    c, app, owner, ids, emails, project, second, resource, cal = await fixture(identity)
    a = await allocation(c, resource, project)
    results = await asyncio.gather(change(c, a, hours_per_day="2"), change(c, a, hours_per_day="1"))
    assert sorted(r.status_code for r in results) == [200, 412]
    key = {"idempotency-key": str(uuid4())}
    one = await send(c, "POST", "/delivery/allocations", headers=key, json=a["data"])
    two = await send(c, "POST", "/delivery/allocations", headers=key, json=a["data"])
    assert one.status_code == two.status_code == 201 and one.json()["id"] == two.json()["id"]
    mismatch = await send(
        c, "POST", "/delivery/allocations", headers=key, json=a["data"] | {"hours_per_day": "1"}
    )
    assert mismatch.status_code == 409
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        role = (
            await conn.execute(
                sa.text("SELECT rolsuper,rolbypassrls FROM pg_roles WHERE rolname=current_user")
            )
        ).one()
        assert not role.rolsuper and not role.rolbypassrls
        assert await conn.scalar(sa.select(sa.func.count()).select_from(TABLES["resources"])) == 1
    async with app.state.engine.begin() as conn:
        assert await conn.scalar(sa.select(sa.func.count()).select_from(TABLES["resources"])) == 0
        await context(conn, ids["other"], ids["b"], "Admin")
        assert await conn.scalar(sa.select(sa.func.count()).select_from(TABLES["resources"])) == 0
    async with app.state.engine.begin() as conn:
        await context(conn, ids["admin"], ids["a"], "Admin")
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(TABLES["calendars"].update().values(monday=8))
    # Cross-tenant insert is blocked independently of API validation.
    async with app.state.engine.begin() as conn:
        await context(conn, ids["other"], ids["b"], "Admin")
        with pytest.raises(DBAPIError):
            async with conn.begin_nested():
                await conn.execute(
                    TABLES["resources"]
                    .insert()
                    .values(
                        id=uuid4(),
                        organization_id=ids["a"],
                        name="forged",
                        description="",
                        revision=1,
                        archived=False,
                        created_at=sa.func.now(),
                        updated_at=sa.func.now(),
                    )
                )


async def test_team_privacy_skills_and_sustained_overload(identity):
    c, app, owner, ids, emails, project, second, resource, cal = await fixture(identity)
    team = await create(c, "teams", name="Support team")
    params = dict(start="2026-03-09", end="2026-03-23")
    for n in range(5):
        r = resource if n == 0 else await create(c, "resources", name=f"Resource {n}")
        if n:
            await create(
                c,
                "availability",
                resource_id=r["id"],
                calendar_id=cal["id"],
                start_date="2026-01-01",
                end_date="2027-01-01",
            )
        await create(
            c,
            "resource_teams",
            resource_id=r["id"],
            team_id=team["id"],
            start_date="2026-01-01",
            end_date="2027-01-01",
        )
        await allocation(c, r, project, "5")
        await create(
            c, "resource_access", resource_id=r["id"], user_id=str(ids["admin"]), effort=True
        )
        await create(
            c,
            "effort",
            resource_id=r["id"],
            project_id=project["id"],
            worked_on="2026-03-09",
            hours="5",
            overtime_hours="1",
        )
        await create(
            c, "effort_coverage", resource_id=r["id"], worked_on="2026-03-09", complete=True
        )
        response = (await c.get("/api/v1/capacity/teams/" + team["id"], params=params)).json()
        if n < 4:
            assert response["status"] == "suppressed" and response["planned_percent"] is None
    assert response["status"] == "available" and response["sustained_overload"] is True
    assert response["overtime_warning"] is None
    assert Decimal(response["allocated_hours"]) == 250
    assert Decimal(response["available_hours"]) == 180
    complete_day = (
        await c.get(
            "/api/v1/capacity/teams/" + team["id"],
            params=dict(start="2026-03-09", end="2026-03-10"),
        )
    ).json()
    assert complete_day["overtime_warning"] is True
    assert Decimal(complete_day["actual_percent"]) == 125
    assert complete_day["sustained_overload"] is None
    await create(c, "resource_skills", resource_id=resource["id"], skill="Python")
    filtered = (await c.get("/api/v1/delivery/resources", params={"skill": "python"})).json()
    assert filtered["total"] == 1 and filtered["items"][0]["id"] == resource["id"]
