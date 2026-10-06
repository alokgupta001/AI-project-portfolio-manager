"""Resource staffing, reproducible daily metrics, and restricted workforce effort."""

from datetime import date, timedelta
from decimal import Decimal
from typing import Any
from uuid import UUID

import sqlalchemy as sa
from fastapi import APIRouter

from ppm_api.capacity_schemas import CapacityView, SnapshotView, TeamCapacityView
from ppm_api.delivery import can_edit, encode, fail, get
from ppm_api.identity import Auth, Principal, now
from ppm_api.ppm_tables import TABLES

router = APIRouter(prefix="/api/v1/capacity", tags=["Capacity"])
KINDS = {
    "resources",
    "calendars",
    "availability",
    "resource_teams",
    "resource_skills",
    "time_off",
    "allocations",
    "resource_access",
    "effort",
    "effort_coverage",
    "capacity_snapshots",
}
IMMUTABLE = {"calendars", "capacity_snapshots"}
SENSITIVE = {"effort", "effort_coverage"}
WEEK = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
ZERO = Decimal(0)


async def access(p: Principal, rid: UUID | None, capability: str) -> bool:
    t = TABLES["resource_access"]
    return bool(
        await p.conn.scalar(
            sa.select(t.c.id)
            .where(
                t.c.organization_id == p.session["organization_id"],
                t.c.user_id == p.user["id"],
                t.c.resource_id == rid,
                ~t.c.archived,
                t.c[capability],
            )
            .limit(1)
        )
    )


async def authorize(p: Principal, kind: str, d: dict, old: Any) -> None:
    rid = d.get("resource_id") or (old["id"] if old else None)
    if p.role == "Viewer":
        fail(403, "Viewer cannot change staffing")
    if kind in {"resource_access", "calendars", "capacity_snapshots"} or (
        kind == "resources" and not old
    ):
        if p.role != "Admin":
            fail(403, "Organization administration requires Admin")
    elif kind in SENSITIVE:
        if not await access(p, rid, "effort"):
            fail(403, "Explicit sensitive effort grant required")
    elif p.role != "Admin" and not await access(p, rid, "manage"):
        fail(403, "Resource manager grant required")
    if d.get("project_id"):
        if not await can_edit(p, d["project_id"]):
            fail(403, "Project edit grant required")
        await get(p, "projects", d["project_id"], True)
    if old:
        if kind == "resources" and old["archived"] != d["archived"] and p.role != "Admin":
            fail(403, "Resource archive requires full organization scope")
        for key in ("resource_id", "project_id", "user_id", "team_id"):
            if key in d and old[key] != d[key]:
                fail(409, "Scope is immutable; create a separate record")
    if rid and kind != "resources":
        await get(p, "resources", rid, True)


async def validate(p: Principal, kind: str, d: dict, id_: UUID) -> None:
    if kind in {"availability", "resource_teams"} and not d["archived"]:
        t = TABLES[kind]
        # One effective working calendar and one reporting team on each local date.
        if await p.conn.scalar(
            sa.select(t.c.id)
            .where(
                t.c.resource_id == d["resource_id"],
                ~t.c.archived,
                t.c.id != id_,
                t.c.start_date < d["end_date"],
                t.c.end_date > d["start_date"],
            )
            .limit(1)
        ):
            fail(409, "Effective resource periods overlap")
    if kind in SENSITIVE and not d["archived"]:
        # An attestation covers the whole resource, so only full-scope Admin can mark complete.
        if kind == "effort_coverage" and d["complete"] and p.role != "Admin":
            fail(403, "Full resource scope required to attest completeness")
        if kind == "effort":
            t = TABLES["effort"]
            total = await p.conn.scalar(
                sa.select(sa.func.coalesce(sa.func.sum(t.c.hours), 0)).where(
                    t.c.resource_id == d["resource_id"],
                    t.c.worked_on == d["worked_on"],
                    ~t.c.archived,
                    t.c.id != id_,
                )
            )
            if p.role == "Admin" and total + d["hours"] > 24:
                fail(422, "Daily recorded effort exceeds 24 hours")


async def rows(p: Principal, kind: str, rid: UUID) -> list[dict]:
    t = TABLES[kind]
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(t)
                .where(
                    t.c.organization_id == p.session["organization_id"],
                    t.c.resource_id == rid,
                    ~t.c.archived,
                )
                .order_by(t.c.id)
            )
        ).mappings()
    ]


def ratio(hours: Decimal | None, available: Decimal | None) -> Decimal | None:
    return (
        (100 * hours / available).quantize(Decimal(".01"))
        if available and hours is not None
        else None
    )


def in_period(row: dict, day: date) -> bool:
    return row["start_date"] <= day < row["end_date"]


def calculate(start: date, end: date, sources: dict, full: bool, sensitive: bool) -> list[dict]:
    result = []
    day = start
    calendars = {r["id"]: r for r in sources["calendars"]}
    while day < end:
        schedule = next((r for r in sources["availability"] if in_period(r, day)), None)
        calendar = calendars.get(schedule["calendar_id"]) if schedule else None
        nominal = Decimal(calendar[WEEK[day.weekday()]]) if calendar else None
        holiday = calendar and day.isoformat() in calendar["holidays"].split(",")
        leave = sum((r["hours_per_day"] for r in sources["time_off"] if in_period(r, day)), ZERO)
        available = (
            max(ZERO, (ZERO if holiday else nominal) - leave) if nominal is not None else None
        )
        # Planned hours apply on scheduled weekdays even during leave/holiday, exposing conflicts.
        # Without a calendar every date is counted conservatively, but capacity stays unknown.
        allocated = sum(
            (
                r["hours_per_day"]
                for r in sources["allocations"]
                if in_period(r, day) and (nominal is None or nominal > 0)
            ),
            ZERO,
        )
        effort = [r for r in sources["effort"] if r["worked_on"] == day]
        actual = sum((r["hours"] for r in effort), ZERO) if sensitive else None
        overtime = sum((r["overtime_hours"] for r in effort), ZERO) if sensitive else None
        complete = (
            sensitive
            and full
            and any(r["worked_on"] == day and r["complete"] for r in sources["effort_coverage"])
        )
        result.append(
            dict(
                day=day,
                timezone=calendar["timezone"] if calendar else None,
                calendar_id=calendar["id"] if calendar else None,
                available_hours=available,
                allocated_hours=allocated,
                excess_hours=max(ZERO, allocated - available)
                if full and available is not None
                else None,
                planned_percent=ratio(allocated, available) if full else None,
                actual_hours=actual,
                overtime_hours=overtime,
                actual_percent=ratio(actual, available) if complete else None,
                effort_complete=complete,
            )
        )
        day += timedelta(days=1)
    return result


def bounded(start: date, end: date) -> None:
    if not 0 < (end - start).days <= 366:
        fail(422, "Choose an interval of 1–366 days; end date is excluded")


async def sources_for(p: Principal, rid: UUID, sensitive: bool) -> dict:
    source = {}
    for kind in (
        "availability",
        "time_off",
        "allocations",
        "resource_teams",
        "resource_skills",
        "effort",
        "effort_coverage",
    ):
        source[kind] = await rows(p, kind, rid) if sensitive or kind not in SENSITIVE else []
    ids = [r["calendar_id"] for r in source["availability"]]
    t = TABLES["calendars"]
    source["calendars"] = [
        dict(r)
        for r in (
            await p.conn.execute(sa.select(t).where(t.c.id.in_(ids)).order_by(t.c.id))
        ).mappings()
    ]
    return source


async def summary(
    p: Principal, rid: UUID, start: date, end: date, project_id: UUID | None = None
) -> dict:
    bounded(start, end)
    resource = await get(p, "resources", rid)
    sensitive = p.role != "Viewer" and await access(p, rid, "effort")
    source = await sources_for(p, rid, sensitive)
    full = p.role == "Admin"
    if project_id:
        await get(p, "projects", project_id)
        source["allocations"] = [r for r in source["allocations"] if r["project_id"] == project_id]
        source["effort"] = [r for r in source["effort"] if r["project_id"] == project_id]
        full = False  # Project slice cannot establish whole-resource overload.
    days = calculate(start, end, source, full, sensitive)
    known = all(d["available_hours"] is not None for d in days)
    available = sum((d["available_hours"] for d in days), ZERO) if known else None
    allocated = sum((d["allocated_hours"] for d in days), ZERO)
    actual = sum((d["actual_hours"] for d in days), ZERO) if sensitive else None
    complete = all(d["effort_complete"] for d in days)
    grouped: dict[date, list] = {}
    for day in days:
        monday = day["day"] - timedelta(days=day["day"].weekday())
        grouped.setdefault(monday, []).append(day)
    weeks = []
    for monday, entries in grouped.items():
        capacity = (
            sum((d["available_hours"] for d in entries), ZERO)
            if all(d["available_hours"] is not None for d in entries)
            else None
        )
        planned = sum((d["allocated_hours"] for d in entries), ZERO)
        weeks.append(
            dict(
                start_date=max(start, monday),
                end_date=min(end, monday + timedelta(days=7)),
                available_hours=capacity,
                allocated_hours=planned,
                excess_hours=sum((d["excess_hours"] for d in entries), ZERO)
                if full and capacity is not None
                else None,
                planned_percent=ratio(planned, capacity) if full else None,
            )
        )
    return dict(
        resource_id=rid,
        resource_name=resource["name"],
        start_date=start,
        end_date=end,
        scope="full_resource" if full else "visible_projects_only",
        can_manage=p.role == "Admin"
        or (p.role == "Project Manager" and await access(p, rid, "manage")),
        can_effort=sensitive,
        days=days,
        weeks=weeks,
        available_hours=available,
        allocated_hours=allocated,
        excess_hours=sum((d["excess_hours"] for d in days), ZERO) if known and full else None,
        planned_percent=ratio(allocated, available) if full else None,
        actual_hours=actual,
        actual_percent=ratio(actual, available) if complete else None,
        effort_complete=complete,
        as_of=now(),
    )


async def snapshot(p: Principal, d: dict) -> dict:
    source = await sources_for(p, d["resource_id"], False)
    return encode(
        dict(
            contract="capacity-snapshot-v1",
            recorded_at=now(),
            start_date=d["start_date"],
            end_date=d["end_date"],
            resource=dict(await get(p, "resources", d["resource_id"])),
            sources=source,
            days=calculate(d["start_date"], d["end_date"], source, True, False),
            semantics=(
                "Local dates [start,end); scheduled decimal hours; no effort or future revisions"
            ),
        )
    )


@router.get("/resources/{rid}", response_model=CapacityView)
async def resource_summary(
    rid: UUID, start: date, end: date, p: Auth, project_id: UUID | None = None
) -> dict:
    return await summary(p, rid, start, end, project_id)


@router.get("/snapshots/{id_}", response_model=SnapshotView)
async def saved_snapshot(id_: UUID, p: Auth) -> dict:
    row = await get(p, "capacity_snapshots", id_)
    return dict(id=row["id"], created_at=row["created_at"], snapshot=row["snapshot"])


@router.get("/teams/{tid}", response_model=TeamCapacityView)
async def team_summary(tid: UUID, start: date, end: date, p: Auth) -> dict:
    bounded(start, end)
    await get(p, "teams", tid)
    t = TABLES["resource_teams"]
    memberships = [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(t).where(
                    t.c.team_id == tid,
                    ~t.c.archived,
                    t.c.start_date < end,
                    t.c.end_date > start,
                )
            )
        ).mappings()
    ]
    ids = sorted({r["resource_id"] for r in memberships})
    base = dict(team_id=tid, resource_count=len(ids), as_of=now())
    if p.role != "Admin":
        return base | dict(status="insufficient_scope")
    if len(ids) < 5:
        return base | dict(status="suppressed")
    results = [await summary(p, rid, start, end) for rid in ids]
    # Suppress if any selected day has a small cohort; no subtraction attacks via date filters.
    days = [
        d
        for r in results
        for d in r["days"]
        if any(m["resource_id"] == r["resource_id"] and in_period(m, d["day"]) for m in memberships)
    ]
    counts = {d["day"]: sum(x["day"] == d["day"] for x in days) for d in days}
    if len(counts) != (end - start).days or min(counts.values()) < 5:
        return base | dict(status="suppressed")
    if any(d["available_hours"] is None for d in days):
        return base | dict(status="incomplete_capacity")
    available = sum((d["available_hours"] for d in days), ZERO)
    allocated = sum((d["allocated_hours"] for d in days), ZERO)
    weeks: dict[date, list] = {}
    for d in days:
        monday = d["day"] - timedelta(days=d["day"].weekday())
        if start <= monday and monday + timedelta(days=7) <= end:
            weeks.setdefault(monday, []).append(d)
    overloaded = {
        w
        for w, ds in weeks.items()
        if sum(x["allocated_hours"] for x in ds) > sum(x["available_hours"] for x in ds)
    }
    complete = all(d["effort_complete"] for d in days)
    return base | dict(
        status="available",
        available_hours=available,
        allocated_hours=allocated,
        excess_hours=sum((d["excess_hours"] for d in days), ZERO),
        planned_percent=ratio(allocated, available),
        actual_percent=ratio(sum(d["actual_hours"] for d in days), available) if complete else None,
        sustained_overload=any(w + timedelta(days=7) in overloaded for w in overloaded)
        if len(weeks) >= 2
        else None,
        overtime_warning=sum(d["overtime_hours"] for d in days) > available / 10
        if complete
        else None,
    )
