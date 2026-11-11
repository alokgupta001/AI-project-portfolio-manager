"""Permission-filtered discovery, first-use progress and personal work surfaces."""

import asyncio
import hashlib
import json
from collections.abc import AsyncGenerator
from contextlib import aclosing
from datetime import date, timedelta
from typing import Any, cast
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import Request
from fastapi.responses import StreamingResponse
from sqlalchemy.dialects.postgresql import insert

from ppm_api.modules.assessments import tables as A
from ppm_api.modules.delivery import service as delivery
from ppm_api.modules.identity.service import Principal, now, principal
from ppm_api.modules.identity.tables import memberships, organizations
from ppm_api.modules.workspace.schemas import PreferenceInput, SearchKind
from ppm_api.modules.workspace.tables import notifications, preferences
from ppm_api.shared.table_registry import TABLES


def term(value: str) -> str:
    return "%" + value.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"


def destination(kind: str, row: Any) -> str:
    if kind == "assessments":
        return "/assessments?assessment=" + str(row["id"])
    if kind == "projects":
        return "/projects/" + str(row["id"])
    return "/projects/" + str(row["project_id"]) + "?kind=" + kind + "&record=" + str(row["id"])


async def records(
    p: Principal, q: str, kind: SearchKind | None, personal: bool, offset: int, limit: int
) -> dict:
    selections = []
    for k in [kind] if kind else ["projects", "work_items", "risks", "assessments"]:
        t = A.assessments if k == "assessments" else TABLES[k]
        filters = [
            t.c.organization_id == p.session["organization_id"],
            t.c.name.ilike(term(q), escape="\\"),
        ]
        if k != "assessments":
            filters.append(~t.c.archived)
            if k != "projects":
                filters.append(
                    sa.exists(
                        sa.select(TABLES["projects"].c.id).where(
                            TABLES["projects"].c.id == t.c.project_id,
                            ~TABLES["projects"].c.archived,
                        )
                    )
                )
        if personal:
            if k == "assessments":
                filters += [
                    sa.or_(t.c.assigned_to == p.user["id"], t.c.reviewer_id == p.user["id"]),
                    t.c.status != "completed",
                ]
            else:
                filters.append(t.c.owner_id == p.user["id"])
                filters.append(t.c.status.notin_(["done", "closed", "completed", "cancelled"]))
        project = (
            t.c.project_id
            if "project_id" in t.c
            else (t.c.id if k == "projects" else sa.literal(None, type_=sa.Uuid))
        )
        due = (
            t.c.due_date
            if "due_date" in t.c
            else (t.c.review_on if k == "risks" else sa.literal(None, type_=sa.Date))
        )
        selections.append(
            sa.select(
                t.c.id,
                t.c.name,
                t.c.organization_id,
                sa.literal(k).label("kind"),
                project.label("project_id"),
                due.label("due_date"),
            ).where(*filters)
        )
    union = sa.union_all(*selections).subquery()
    total = await p.conn.scalar(sa.select(sa.func.count()).select_from(union))
    rows = (
        await p.conn.execute(
            sa.select(union)
            .order_by(
                union.c.due_date.asc().nulls_last(),
                sa.func.lower(union.c.name),
                union.c.kind,
                union.c.id,
            )
            .offset(offset)
            .limit(limit)
        )
    ).mappings()
    return dict(
        items=[dict(r) | {"href": destination(r["kind"], r)} for r in rows],
        total=total,
        offset=offset,
        limit=limit,
    )


async def search(
    p: Principal, q: str = "", kind: SearchKind | None = None, offset: int = 0, limit: int = 25
) -> dict:
    return await records(p, q, kind, False, offset, limit)


async def my_work(p: Principal, offset: int = 0, limit: int = 25) -> dict:
    return await records(p, "", None, True, offset, limit)


async def setup(p: Principal) -> dict:
    org = await p.conn.scalar(
        sa.select(organizations.c.name).where(organizations.c.id == p.session["organization_id"])
    )
    steps = [
        {
            "label": "Organization name",
            "href": "/account#organization-profile",
            "complete": bool(org),
            "admin": True,
        }
    ]
    if p.role == "Admin":
        count = await p.conn.scalar(
            sa.select(sa.func.count())
            .select_from(memberships)
            .where(
                memberships.c.organization_id == p.session["organization_id"], memberships.c.active
            )
        )
        steps.append(
            {
                "label": "Invite a colleague",
                "href": "/account#members",
                "complete": (count or 0) > 1,
                "admin": True,
            }
        )
    for label, t, href in [
        ("Set timezone and currency", TABLES["settings"], "/organization"),
        ("Create a portfolio", TABLES["portfolios"], "/portfolios"),
        ("Create a project", TABLES["projects"], "/projects"),
        ("Create a resource profile", TABLES["resources"], "/resources"),
        ("Assign an assessment", A.assessments, "/assessments"),
    ]:
        count = await p.conn.scalar(
            sa.select(sa.func.count())
            .select_from(t)
            .where(t.c.organization_id == p.session["organization_id"])
        )
        steps.append(
            {"label": label, "href": href, "complete": count > 0, "admin": href == "/organization"}
        )
    return {"steps": [s for s in steps if p.role == "Admin" or not s["admin"]], "as_of": now()}


async def comparison(p: Principal, framework_version_id: UUID, start: date, end: date) -> dict:
    if end < start or (end - start).days > 3660:
        delivery.fail(422, "Use an ordered comparison period of at most ten years")
    a = A.assessments
    score = sa.cast(a.c.results["overall_score"].as_string(), sa.Numeric)
    departments = TABLES["departments"]
    rows = (
        await p.conn.execute(
            sa.select(
                a.c.department_id,
                departments.c.name,
                sa.func.count().label("count"),
                sa.func.count(score).label("scored_count"),
                sa.func.avg(score).label("score"),
            )
            .outerjoin(departments, departments.c.id == a.c.department_id)
            .where(
                a.c.organization_id == p.session["organization_id"],
                a.c.framework_version_id == framework_version_id,
                a.c.status == "completed",
                a.c.department_id.is_not(None),
                sa.cast(a.c.created_at, sa.Date) >= start,
                sa.cast(a.c.created_at, sa.Date) <= end,
            )
            .group_by(a.c.department_id, departments.c.name)
            .order_by(departments.c.name, a.c.department_id)
        )
    ).mappings()
    out = [dict(r) | {"score": str(r["score"]) if r["score"] is not None else None} for r in rows]
    return {
        "items": out,
        "count": sum(v["count"] for v in out),
        "start": start,
        "end": end,
        "framework_version_id": framework_version_id,
        "coverage": "All permitted completed departmental records created in this UTC period",
    }


async def notify(
    conn: Any, org: UUID, user: UUID | None, kind: str, target: UUID, key: str
) -> None:
    if user:
        await conn.execute(
            insert(notifications)
            .values(
                id=uuid4(),
                organization_id=org,
                user_id=user,
                kind=kind,
                target_id=target,
                event_key=key,
                created_at=now(),
                read=False,
            )
            .on_conflict_do_nothing()
        )


async def eligible_notification(p: Principal, n: Any) -> dict | None:
    if n["kind"] == "jobs":
        from ppm_api.modules.integrations.jobs import get_job

        job = await get_job(p, n["target_id"])
        return {"name": "Import " + job["status"], "href": "/integrations"}
    t = A.assessments if n["kind"] == "assessments" else TABLES[n["kind"]]
    visible = (
        (
            await p.conn.execute(
                sa.select(t).where(
                    t.c.id == n["target_id"], t.c.organization_id == p.session["organization_id"]
                )
            )
        )
        .mappings()
        .first()
    )
    if not visible or ("archived" in visible and visible["archived"]):
        return None
    if n["kind"] == "assessments":
        if p.user["id"] not in [visible["assigned_to"], visible["reviewer_id"]]:
            return None
    elif visible["owner_id"] != p.user["id"]:
        return None
    if "project_id" in visible:
        await delivery.get(p, "projects", visible["project_id"])
    return {"name": visible["name"], "href": destination(n["kind"], visible)}


async def feed(p: Principal, offset: int = 0, limit: int = 25) -> dict:
    enabled = await p.conn.scalar(
        sa.select(preferences.c.enabled).where(
            preferences.c.organization_id == p.session["organization_id"],
            preferences.c.user_id == p.user["id"],
        )
    )
    from ppm_api.modules.integrations.tables import jobs

    permitted = []
    for kind in ["work_items", "risks", "assessments", "jobs"]:
        t = A.assessments if kind == "assessments" else (jobs if kind == "jobs" else TABLES[kind])
        rules = [
            t.c.id == notifications.c.target_id,
            t.c.organization_id == p.session["organization_id"],
        ]
        if kind == "assessments":
            rules.append(sa.or_(t.c.assigned_to == p.user["id"], t.c.reviewer_id == p.user["id"]))
        elif kind == "jobs":
            rules.append(t.c.actor_id == p.user["id"])
        else:
            rules += [
                ~t.c.archived,
                t.c.owner_id == p.user["id"],
                sa.exists(
                    sa.select(TABLES["projects"].c.id).where(
                        TABLES["projects"].c.id == t.c.project_id, ~TABLES["projects"].c.archived
                    )
                ),
            ]
        permitted.append(
            sa.and_(notifications.c.kind == kind, sa.exists(sa.select(t.c.id).where(*rules)))
        )
    where = [notifications.c.created_at >= now() - timedelta(days=30), sa.or_(*permitted)]
    items = []
    total = 0
    if enabled is not False:
        total = (
            await p.conn.scalar(sa.select(sa.func.count()).select_from(notifications).where(*where))
            or 0
        )
        rows = (
            await p.conn.execute(
                sa.select(notifications)
                .where(*where)
                .order_by(notifications.c.created_at.desc(), notifications.c.id)
                .offset(offset)
                .limit(limit)
            )
        ).mappings()
        for n in rows:
            try:
                item = await eligible_notification(p, n)
            except delivery.DomainError:
                item = None
            if item:
                items.append(
                    item | {"id": n["id"], "read": n["read"], "created_at": n["created_at"]}
                )
    return {"items": items, "total": total, "enabled": enabled is not False, "retention_days": 30}


async def preference(body: PreferenceInput, p: Principal) -> dict:
    await p.conn.execute(
        insert(preferences)
        .values(
            organization_id=p.session["organization_id"], user_id=p.user["id"], enabled=body.enabled
        )
        .on_conflict_do_update(
            index_elements=["organization_id", "user_id"], set_={"enabled": body.enabled}
        )
    )
    return body.model_dump()


async def mark_read(id_: UUID, p: Principal) -> dict:
    n = (
        (
            await p.conn.execute(
                sa.select(notifications).where(
                    notifications.c.id == id_,
                    notifications.c.created_at >= now() - timedelta(days=30),
                )
            )
        )
        .mappings()
        .first()
    )
    if not n or not await eligible_notification(p, n):
        delivery.fail(404, "Notification is unavailable")
    await p.conn.execute(notifications.update().where(notifications.c.id == id_).values(read=True))
    return {"read": True}


async def freshness(p: Principal) -> str:
    parts = []
    # RLS-filtered aggregates emit no names, IDs, counts or private workforce data.
    for k in [
        "projects",
        "work_items",
        "milestones",
        "risks",
        "budget_lines",
        "expenditures",
        "resources",
        "allocations",
        "time_off",
        "availability",
    ]:
        t = TABLES[k]
        row = (
            await p.conn.execute(
                sa.select(sa.func.count(), sa.func.sum(t.c.revision), sa.func.max(t.c.updated_at))
            )
        ).one()
        parts.append(str(row))
    row = (
        await p.conn.execute(sa.select(sa.func.count(), sa.func.sum(A.assessments.c.revision)))
    ).one()
    parts.append(str(row))
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


async def stream(request: Request, p: Principal) -> StreamingResponse:
    await freshness(p)

    async def generate() -> AsyncGenerator[str, None]:
        last = request.headers.get("last-event-id", "")
        ticks = 0
        while not await request.is_disconnected():
            try:
                async with aclosing(
                    cast(AsyncGenerator[Principal, None], principal(request))
                ) as auth:
                    async for live in auth:
                        current = await freshness(live)
            except Exception:
                yield "event: access_revoked\ndata: {}\n\n"
                return
            if current != last:
                last = current
                yield (
                    f"id: {current}\nevent: changed\ndata: "
                    + json.dumps({"version": "workspace-v1", "as_of": now().isoformat()})
                    + "\n\n"
                )
            if ticks % 15 == 0:
                yield ": heartbeat\n\n"
            ticks += 1
            await asyncio.sleep(1)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
    )
