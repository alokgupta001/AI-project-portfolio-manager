"""Portfolio/delivery commands with live scope, concurrency and auditable persistence."""

import hashlib
import json
from decimal import Decimal
from typing import Annotated, Any, Literal, NoReturn
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import APIRouter, Header, HTTPException, Query, Request
from fastapi.encoders import jsonable_encoder
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from ppm_api.identity import Auth, Principal, context, now
from ppm_api.identity_tables import memberships, sessions, users
from ppm_api.metric_math import alignment_score, budget_usage
from ppm_api.ppm_schemas import (
    HistoryView,
    Input,
    Kind,
    PageView,
    PersonView,
    PortfolioSummary,
    RecordView,
    SummaryView,
)
from ppm_api.ppm_tables import TABLES, audit, requests

LiteralSort = Literal["name", "updated"]

router = APIRouter(prefix="/api/v1/delivery", tags=["Delivery"])
adapter: TypeAdapter = TypeAdapter(Input)
IMMUTABLE = {"baselines", "expenditures", "status_updates"}
ORG_ADMIN = {
    "metric_policies",
    "settings",
    "departments",
    "teams",
    "team_members",
    "goals",
    "portfolios",
    "programs",
    "grants",
}


def encode(value: Any) -> Any:
    return jsonable_encoder(value, custom_encoder={Decimal: str})


class DomainError(HTTPException):
    """Only fixed, credential-free domain messages reach the UI."""


def fail(status: int, detail: str) -> NoReturn:
    raise DomainError(status, detail)


def view(kind: str, row: Any) -> dict[str, Any]:
    fields = adapter.validate_python(
        {
            "kind": kind,
            **{
                k: v
                for k, v in dict(row).items()
                if k
                not in {
                    "id",
                    "organization_id",
                    "revision",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "snapshot",
                    "version",
                }
            },
        }
    )
    return {
        k: row[k] for k in ["id", "organization_id", "revision", "created_at", "updated_at"]
    } | {"data": fields}


async def get(p: Principal, kind: str, id_: UUID, active: bool = False) -> Any:
    t = TABLES[kind]
    row = (
        (
            await p.conn.execute(
                sa.select(t).where(
                    t.c.id == id_, t.c.organization_id == p.session["organization_id"]
                )
            )
        )
        .mappings()
        .first()
    )
    if not row:
        fail(404, "Record not available")
    if active and row["archived"]:
        fail(409, "Referenced record is archived")
    return row


async def grant(p: Principal, field: str, id_: UUID, levels: tuple[str, ...]) -> bool:
    g = TABLES["grants"]
    return bool(
        await p.conn.scalar(
            sa.select(g.c.id)
            .where(
                g.c.organization_id == p.session["organization_id"],
                g.c.user_id == p.user["id"],
                g.c[field] == id_,
                g.c.access.in_(levels),
                ~g.c.archived,
            )
            .limit(1)
        )
    )


async def can_edit(p: Principal, id_: UUID, manage: bool = False) -> bool:
    return (
        p.role == "Admin"
        or p.role == "Project Manager"
        and await grant(p, "project_id", id_, ("manage",) if manage else ("edit", "manage"))
    )


async def lock(p: Principal, request: Request) -> None:
    oid = p.session["organization_id"]
    if request.headers.get("x-organization-id") != str(oid):
        fail(409, "Reload the active organization")
    # Same lock namespace as identity membership edits: recheck live authority after waiting.
    await p.conn.execute(
        sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org, 2))"), {"org": str(oid)}
    )
    role = await p.conn.scalar(
        sa.select(memberships.c.role).where(
            memberships.c.organization_id == oid,
            memberships.c.user_id == p.user["id"],
            memberships.c.active,
        )
    )
    session = (
        (await p.conn.execute(sa.select(sessions).where(sessions.c.id == p.session["id"])))
        .mappings()
        .one()
    )
    if (
        not role
        or session["revoked"]
        or session["expires_at"] <= now()
        or session["organization_id"] != oid
    ):
        fail(401, "Session is no longer active")
    p.role = str(role)
    await context(p.conn, p.user["id"], oid, str(role))


async def authorize(p: Principal, kind: str, data: dict, old: Any = None) -> None:
    from ppm_api import capacity

    if kind in capacity.KINDS:
        await capacity.authorize(p, kind, data, old)
        return
    if kind == "saved_views":
        if data["user_id"] != p.user["id"] or old and old["user_id"] != p.user["id"]:
            fail(403, "Saved views are personal")
        return
    if kind in ORG_ADMIN:
        if p.role != "Admin":
            fail(403, "Organization administration requires Admin")
    elif kind == "projects":
        if old:
            if not await can_edit(p, old["id"], data["archived"] != old["archived"]):
                fail(403, "Project grant required")
            if old["archived"] and data["archived"]:
                fail(409, "Restore this project before editing")
            if old["portfolio_id"] != data["portfolio_id"] and p.role != "Admin":
                fail(403, "Transfers require Admin")
        elif p.role != "Admin" and not (
            p.role == "Project Manager"
            and await grant(p, "portfolio_id", data["portfolio_id"], ("manage",))
        ):
            fail(403, "Portfolio manage grant required")
    elif kind == "alignments" and data.get("portfolio_id"):
        if p.role != "Admin":
            fail(403, "Portfolio alignment requires Admin")
    else:
        if not await can_edit(p, data["project_id"]):
            fail(403, "Project edit grant required")
        await get(p, "projects", data["project_id"], True)
    if old:
        for key in [
            "project_id",
            "user_id",
            "team_id" if kind == "team_members" else "",
            "portfolio_id" if kind in ("programs", "grants", "alignments") else "",
        ]:
            if key and key in data and data[key] != old[key]:
                fail(409, "Scope is immutable; create a new record instead")


async def refs(p: Principal, kind: str, d: dict) -> None:
    for field in ("owner_id", "user_id"):
        if d.get(field):
            valid = await p.conn.scalar(
                sa.select(memberships.c.user_id).where(
                    memberships.c.organization_id == p.session["organization_id"],
                    memberships.c.user_id == d[field],
                    memberships.c.active,
                )
            )
            if not valid:
                fail(422, "Owner/member must be an active organization member")
    mapping = {
        "baseline_id": "baselines",
        "resource_id": "resources",
        "calendar_id": "calendars",
        "portfolio_id": "portfolios",
        "program_id": "programs",
        "department_id": "departments",
        "team_id": "teams",
        "project_id": "projects",
        "target_project_id": "projects",
        "sprint_id": "sprints",
        "work_item_id": "work_items",
        "goal_id": "goals",
        "source_milestone_id": "milestones",
        "target_milestone_id": "milestones",
        "source_work_item_id": "work_items",
        "target_work_item_id": "work_items",
        "reversal_of": "expenditures",
    }
    for field, target in mapping.items():
        if not d.get(field):
            continue
        r = await get(p, target, d[field], True)
        if field == "program_id" and r["portfolio_id"] != d["portfolio_id"]:
            fail(422, "Program must belong to the selected portfolio")
        if target in ("sprints", "work_items", "milestones", "expenditures", "baselines"):
            expected = (
                d.get("target_project_id") if field.startswith("target_") else d.get("project_id")
            )
            if r["project_id"] != expected:
                fail(422, "Reference belongs to a different project")
    if kind in ("budget_lines", "expenditures"):
        proj = await get(p, "projects", d["project_id"], True)
        if d["currency"] != proj["currency"]:
            fail(422, "Currency must match the project; no implicit FX conversion")
    if kind == "expenditures":
        if d["reversal_of"]:
            original = await get(p, "expenditures", d["reversal_of"])
            if (
                original["reversal_of"]
                or d["amount"] != -original["amount"]
                or d["currency"] != original["currency"]
            ):
                fail(422, "Reversal must exactly negate the original entry")
        elif d["amount"] < 0:
            fail(422, "Negative expenditure requires an auditable reversal")
    if kind == "team_members":
        t = TABLES[kind]
        conditions = [
            t.c.team_id == d["team_id"],
            t.c.user_id == d["user_id"],
            ~t.c.archived,
            sa.or_(t.c.end_date.is_(None), t.c.end_date > d["start_date"]),
        ]
        if d.get("end_date"):
            conditions.append(t.c.start_date < d["end_date"])
        if d.get("_id"):
            conditions.append(t.c.id != d["_id"])
        if await p.conn.scalar(sa.select(t.c.id).where(*conditions).limit(1)):
            fail(409, "Team membership dates overlap")


async def cycle_check(p: Principal, d: dict, id_: UUID) -> None:
    if not await can_edit(p, d["target_project_id"]):
        fail(403, "Both dependency projects require edit access")
    t = TABLES["dependencies"]
    # Cross-project graph closure is checked at project level as well as node level.
    # RLS may hide edges involving other grants: fail closed unless caller can read all edges.
    # Organization Admin manages cross-project edges; scoped PMs can edit only intra-project edges.
    if d["project_id"] != d["target_project_id"] and p.role != "Admin":
        fail(403, "Cross-project dependency changes require Admin")
    rows = [
        dict(r)
        for r in (await p.conn.execute(sa.select(t).where(~t.c.archived, t.c.id != id_))).mappings()
    ] + [d]

    def endpoint(r: dict, target: bool) -> str:
        prefix = "target_" if target else "source_"
        return str(
            r.get(prefix + "milestone_id")
            or r.get(prefix + "work_item_id")
            or r["target_project_id" if target else "project_id"]
        )

    graphs: list[dict[str, set[str]]] = [{}, {}]
    for r in rows:
        a, b = endpoint(r, False), endpoint(r, True)
        graphs[0].setdefault(a, set()).add(b)
        if r["project_id"] != r["target_project_id"]:
            graphs[1].setdefault(str(r["project_id"]), set()).add(str(r["target_project_id"]))
    for graph in graphs:
        indegree = {node: 0 for a, bs in graph.items() for node in [a, *bs]}
        for bs in graph.values():
            for node in bs:
                indegree[node] += 1
        ready = [n for n, v in indegree.items() if v == 0]
        visited = 0
        while ready:
            a = ready.pop()
            visited += 1
            for b in graph.get(a, set()):
                indegree[b] -= 1
                if indegree[b] == 0:
                    ready.append(b)
        if visited != len(indegree):
            fail(409, "Schedule dependencies must be acyclic")


async def audit_change(
    p: Principal, request: Request, kind: str, row: Any, old: Any = None
) -> None:
    await p.conn.execute(
        audit.insert().values(
            id=uuid4(),
            organization_id=p.session["organization_id"],
            project_id=row.get("project_id") or (row["id"] if kind == "projects" else None),
            actor_id=p.user["id"],
            resource=kind,
            target_id=row["id"],
            before=encode(dict(old)) if old else None,
            after=encode(dict(row)),
            request_id=UUID(request.state.request_id),
            created_at=now(),
        )
    )


async def snapshot(p: Principal, pid: UUID) -> dict:
    project_row = await get(p, "projects", pid)
    result = {
        "project": encode(dict(project_row)),
        "calendar": {
            "timezone": await p.conn.scalar(sa.select(TABLES["settings"].c.timezone)),
            "week_start": "Monday",
            "version": "calendar-v1",
        },
        "items": {},
    }
    for kind in ["work_items", "milestones", "sprints", "budget_lines"]:
        t = TABLES[kind]
        result["items"][kind] = encode(
            [
                dict(r)
                for r in (
                    await p.conn.execute(
                        sa.select(t).where(t.c.project_id == pid, ~t.c.archived).order_by(t.c.id)
                    )
                ).mappings()
            ]
        )
    return result


async def archive_guard(p: Principal, kind: str, id_: UUID) -> None:
    if kind == "projects":
        return
    for t in TABLES.values():
        for fk in t.foreign_key_constraints:
            pairs = list(fk.elements)
            matching = [
                e for e in pairs if e.column.table.name == "ppm_" + kind and e.column.name == "id"
            ]
            for e in matching:
                if await p.conn.scalar(
                    sa.select(t.c.id)
                    .where(t.c[e.parent.name] == id_, ~t.c.archived, t.c.id != id_)
                    .limit(1)
                ):
                    fail(409, "Archive dependent active records first")


@router.get("/people", response_model=list[PersonView])
async def people(p: Auth, q: str = Query(default="", max_length=160)) -> list[dict]:
    rows = (
        await p.conn.execute(
            sa.select(users.c.id, users.c.name)
            .join(memberships, memberships.c.user_id == users.c.id)
            .where(
                memberships.c.organization_id == p.session["organization_id"],
                memberships.c.active,
                users.c.name.ilike("%" + q + "%"),
            )
            .order_by(users.c.name, users.c.id)
            .limit(100)
        )
    ).mappings()
    return [dict(r) for r in rows]


@router.get("/history/{kind}/{id_}", response_model=list[HistoryView])
async def history(kind: Kind, id_: UUID, p: Auth) -> list[dict]:
    await get(p, kind, id_)
    rows = (
        await p.conn.execute(
            sa.select(audit)
            .where(audit.c.resource == kind, audit.c.target_id == id_)
            .order_by(audit.c.created_at.desc())
            .limit(100)
        )
    ).mappings()
    return [dict(r) for r in rows]


@router.get("/portfolio-summary/{id_}", response_model=PortfolioSummary)
async def portfolio_summary(id_: UUID, p: Auth) -> dict:
    portfolio = await get(p, "portfolios", id_)
    t = TABLES["projects"]
    projects = list(
        (
            await p.conn.execute(sa.select(t.c.id).where(t.c.portfolio_id == id_, ~t.c.archived))
        ).scalars()
    )
    totals: dict[str, dict] = {}
    for pid in projects:
        item = (await summary(pid, p))["money"][0]
        currency = item["currency"]
        group = totals.setdefault(
            currency,
            dict(
                currency=currency,
                approved_budget=Decimal(0),
                recorded_spend=Decimal(0),
                usage_percent=None,
                ledger_complete=True,
            ),
        )
        group["approved_budget"] += item["approved_budget"]
        group["recorded_spend"] += item["recorded_spend"]
        group["ledger_complete"] &= item["ledger_complete"]
    for group in totals.values():
        if group["approved_budget"] and group["ledger_complete"]:
            group["usage_percent"] = budget_usage(
                group["recorded_spend"], group["approved_budget"], group["ledger_complete"]
            )
    return dict(
        portfolio=view("portfolios", portfolio),
        visible_projects=len(projects),
        money=list(totals.values()),
        as_of=now(),
    )


@router.get("/project-summary/{id_}", response_model=SummaryView)
async def summary(id_: UUID, p: Auth) -> dict:
    row = await get(p, "projects", id_)
    budget = TABLES["budget_lines"]
    expense = TABLES["expenditures"]
    align = TABLES["alignments"]
    base = TABLES["baselines"]
    work = TABLES["work_items"]
    amount = await p.conn.scalar(
        sa.select(sa.func.coalesce(sa.func.sum(budget.c.amount), 0)).where(
            budget.c.project_id == id_, ~budget.c.archived, budget.c.approved
        )
    )
    spent = await p.conn.scalar(
        sa.select(sa.func.coalesce(sa.func.sum(expense.c.amount), 0)).where(
            expense.c.project_id == id_
        )
    )
    goals = list(
        (
            await p.conn.execute(
                sa.select(align).where(align.c.project_id == id_, ~align.c.archived)
            )
        ).mappings()
    )
    complete = bool(goals) and sum(g["weight"] for g in goals) == Decimal(1)
    alignment = alignment_score(goals)
    counts: dict[str, int] = dict(
        (
            await p.conn.execute(
                sa.select(work.c.status, sa.func.count())
                .where(work.c.project_id == id_, ~work.c.archived)
                .group_by(work.c.status)
            )
        )
        .tuples()
        .all()
    )
    history = (
        await p.conn.execute(
            sa.select(base).where(base.c.project_id == id_).order_by(base.c.version.desc())
        )
    ).mappings()
    return dict(
        project=view("projects", row),
        can_edit=await can_edit(p, id_),
        can_manage=await can_edit(p, id_, True),
        money=[
            dict(
                currency=row["currency"],
                approved_budget=amount,
                recorded_spend=spent,
                usage_percent=budget_usage(
                    Decimal(str(spent or 0)), Decimal(str(amount or 0)), row["ledger_complete"]
                ),
                ledger_complete=row["ledger_complete"],
            )
        ],
        alignment_percent=alignment,
        alignment_complete=complete,
        computed_health=None,
        baselines=[
            dict(
                id=b["id"],
                version=b["version"],
                created_at=b["created_at"],
                reason=b["description"],
                snapshot=b["snapshot"],
            )
            for b in history
        ],
        work_counts=counts,
        as_of=now(),
    )


@router.get("/{kind}", response_model=PageView)
async def listing(
    kind: Kind,
    p: Auth,
    q: str = Query(default="", max_length=160),
    project_id: UUID | None = None,
    portfolio_id: UUID | None = None,
    resource_id: UUID | None = None,
    skill: str = Query(default="", max_length=80),
    archived: bool = False,
    status: str | None = None,
    sort: LiteralSort = "name",
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> dict:
    t = TABLES[kind]
    where = [t.c.organization_id == p.session["organization_id"], t.c.archived == archived]
    if skill:
        if kind != "resources":
            fail(422, "Skill filter requires resources")
        s = TABLES["resource_skills"]
        where.append(
            sa.exists(
                sa.select(s.c.id).where(
                    s.c.resource_id == t.c.id,
                    ~s.c.archived,
                    sa.func.lower(s.c.skill) == skill.strip().lower(),
                )
            )
        )
    if q:
        where.append(
            t.c.name.ilike(
                "%" + q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%",
                escape="\\",
            )
        )
    for key, value in [
        ("project_id", project_id),
        ("portfolio_id", portfolio_id),
        ("resource_id", resource_id),
        ("status", status),
    ]:
        if value is not None:
            if key not in t.c:
                fail(422, "Filter is not supported for this resource")
            where.append(t.c[key] == value)
    count = await p.conn.scalar(sa.select(sa.func.count()).select_from(t).where(*where))
    order = t.c.updated_at.desc() if sort == "updated" else t.c.name.asc()
    rows = (
        await p.conn.execute(
            sa.select(t).where(*where).order_by(order, t.c.id).offset(offset).limit(limit)
        )
    ).mappings()
    return dict(
        items=[view(kind, r) for r in rows], total=count, offset=offset, limit=limit, as_of=now()
    )


@router.get("/{kind}/{id_}", response_model=RecordView)
async def detail(kind: Kind, id_: UUID, p: Auth) -> dict:
    return view(kind, await get(p, kind, id_))


async def write(
    p: Principal,
    request: Request,
    kind: Kind,
    payload: Any,
    id_: UUID | None,
    version: int | None,
    reason: str,
) -> dict:
    from ppm_api import capacity

    if payload.kind != kind:
        fail(422, "Resource kind mismatch")
    await lock(p, request)
    old = await get(p, kind, id_) if id_ else None
    if old and (version is None or old["revision"] != version):
        fail(428 if version is None else 412, "Reload the current revision before saving")
    if old and kind in IMMUTABLE | capacity.IMMUTABLE:
        fail(409, "History/ledger entries are immutable; append a new baseline, status or reversal")
    d = payload.model_dump(exclude={"kind"})
    await authorize(p, kind, d, old)
    if kind == "settings" and d["archived"]:
        fail(409, "Organization configuration cannot be archived")
    if kind == "work_items" and old and old["status"] != d["status"]:
        transitions = {
            "backlog": {"ready"},
            "ready": {"backlog", "in_progress"},
            "in_progress": {"ready", "done"},
            "done": {"in_progress"},
        }
        if d["status"] not in transitions[old["status"]]:
            fail(409, "Invalid work status transition")
    if kind == "risks" and old and old["status"] != d["status"]:
        transitions = {
            "open": {"mitigating", "accepted", "closed"},
            "mitigating": {"open", "accepted", "closed"},
            "accepted": {"open", "closed"},
            "closed": {"open"},
        }
        if (
            d["status"] not in transitions[old["status"]]
            or old["status"] == "closed"
            and not reason.strip()
        ):
            fail(409, "Invalid risk transition; reopening requires a change reason")
    if kind == "sprints" and not old and d["status"] != "planned":
        fail(422, "Create a planned sprint before progressing its lifecycle")
    if kind == "sprints" and old and old["status"] == "closed":
        fail(409, "Closed sprint definition is immutable")
    if kind == "alignments" and not d["archived"]:
        t = TABLES["alignments"]
        same = [~t.c.archived, t.c.id != (id_ or UUID(int=0)), t.c.goal_id == d["goal_id"]]
        same.append(
            t.c.project_id == d["project_id"]
            if d["project_id"]
            else t.c.portfolio_id == d["portfolio_id"]
        )
        if await p.conn.scalar(sa.select(t.c.id).where(*same).limit(1)):
            fail(409, "Goal already linked; edit its existing weight")

    if kind != "settings" and not await p.conn.scalar(sa.select(TABLES["settings"].c.id)):
        fail(409, "Configure organization timezone and currency first")
    id_ = id_ or uuid4()
    if old and d["archived"] and not old["archived"]:
        await archive_guard(p, kind, id_)
    if d["archived"] and not old:
        fail(422, "New records cannot start archived")
    await refs(p, kind, d | {"_id": id_})
    if kind in capacity.KINDS:
        await capacity.validate(p, kind, d, id_)
    if kind == "capacity_snapshots":
        d["snapshot"] = await capacity.snapshot(p, d)
    if kind == "projects":
        transitions = {
            "draft": {"active", "cancelled"},
            "active": {"on_hold", "completed", "cancelled"},
            "on_hold": {"active", "cancelled"},
            "completed": {"active"},
            "cancelled": {"active"},
        }
        if old and d["status"] != old["status"]:
            if d["status"] not in transitions[old["status"]]:
                fail(409, "Invalid project status transition")
            if old["status"] in ("completed", "cancelled") and not reason.strip():
                fail(422, "Reopening requires a reason and new baseline")
        if old and old["currency"] != d["currency"]:
            for k in ("budget_lines", "expenditures"):
                if await p.conn.scalar(
                    sa.select(TABLES[k].c.id).where(TABLES[k].c.project_id == id_).limit(1)
                ):
                    fail(409, "Currency cannot change after financial records exist")
        if not old:
            d["created_by"] = p.user["id"]
    if (
        kind == "work_items"
        and old
        and old["status"] == "done"
        and d["status"] != "done"
        and not reason.strip()
    ):
        fail(422, "Reopening work requires a reason")
    if (
        kind == "sprints"
        and old
        and old["status"] != d["status"]
        and (old["status"], d["status"]) not in [("planned", "active"), ("active", "closed")]
    ):
        fail(409, "Invalid sprint transition")
    if kind == "dependencies" and not d["archived"]:
        await cycle_check(p, d, id_)
    if kind == "baselines":
        if not d["description"].strip():
            fail(422, "Baseline requires a reason")
        b = TABLES["baselines"]
        d["version"] = (
            int(
                (
                    await p.conn.scalar(
                        sa.select(sa.func.coalesce(sa.func.max(b.c.version), 0)).where(
                            b.c.project_id == d["project_id"]
                        )
                    )
                )
                or 0
            )
            + 1
        )
        d["snapshot"] = await snapshot(p, d["project_id"])
    t = TABLES[kind]
    stamp = now()
    d.update(updated_at=stamp, revision=old["revision"] + 1 if old else 1)
    if old:
        row = (
            (
                await p.conn.execute(
                    t.update()
                    .where(t.c.id == id_, t.c.revision == version)
                    .values(**d)
                    .returning(t)
                )
            )
            .mappings()
            .first()
        )
        if not row:
            fail(412, "Record changed; reload")
    else:
        d.update(id=id_, organization_id=p.session["organization_id"], created_at=stamp)
        row = (await p.conn.execute(t.insert().values(**d).returning(t))).mappings().one()
    await audit_change(p, request, kind, row, old)
    if kind == "sprints" and old and old["status"] != "closed" and d["status"] == "closed":
        work = TABLES["work_items"]
        items = list(
            (
                await p.conn.execute(
                    sa.select(work).where(work.c.sprint_id == id_, ~work.c.archived)
                )
            ).mappings()
        )
        completed = [w for w in items if w["status"] == "done"]
        await p.conn.execute(
            TABLES["sprint_closures"]
            .insert()
            .values(
                id=uuid4(),
                organization_id=p.session["organization_id"],
                project_id=d["project_id"],
                name=d["name"],
                description="Frozen at sprint closure; team-points-v1",
                revision=1,
                archived=False,
                created_at=stamp,
                updated_at=stamp,
                sprint_id=id_,
                team_id=d["team_id"],
                end_date=d["end_date"],
                points=sum((w["points"] or Decimal(0) for w in completed), Decimal(0)),
                complete=all(w["points"] is not None for w in completed),
                snapshot=encode(completed),
            )
        )
    if kind == "effort":
        coverage = TABLES["effort_coverage"]
        affected_dates = {d["worked_on"]}
        if old:
            affected_dates.add(old["worked_on"])
        for before in (
            (
                await p.conn.execute(
                    sa.select(coverage).where(
                        coverage.c.resource_id == d["resource_id"],
                        coverage.c.worked_on.in_(affected_dates),
                        coverage.c.complete,
                    )
                )
            )
            .mappings()
            .all()
        ):
            after = (
                (
                    await p.conn.execute(
                        coverage.update()
                        .where(coverage.c.id == before["id"])
                        .values(complete=False, revision=coverage.c.revision + 1, updated_at=stamp)
                        .returning(coverage)
                    )
                )
                .mappings()
                .one()
            )
            await audit_change(p, request, "effort_coverage", after, before)
    if kind == "projects" and not old and p.role != "Admin":
        g = TABLES["grants"]
        await p.conn.execute(
            g.insert().values(
                id=uuid4(),
                organization_id=p.session["organization_id"],
                name="Project creator",
                description="",
                revision=1,
                archived=False,
                created_at=stamp,
                updated_at=stamp,
                user_id=p.user["id"],
                project_id=id_,
                portfolio_id=None,
                access="manage",
            )
        )
    if kind == "status_updates":
        proj = TABLES["projects"]
        before = await get(p, "projects", d["project_id"])
        after = (
            (
                await p.conn.execute(
                    proj.update()
                    .where(proj.c.id == d["project_id"])
                    .values(
                        reported_health=d["reported_health"],
                        revision=proj.c.revision + 1,
                        updated_at=stamp,
                    )
                    .returning(proj)
                )
            )
            .mappings()
            .one()
        )
        await audit_change(p, request, "projects", after, before)
    if (
        kind == "projects"
        and old
        and old["status"] in ("completed", "cancelled")
        and d["status"] == "active"
    ):
        from ppm_api.ppm_schemas import BaselineInput

        await write(
            p,
            request,
            "baselines",
            BaselineInput(name="Reopened plan", description=reason, project_id=id_),
            None,
            None,
            "",
        )
    return view(kind, row)


@router.post("/{kind}", response_model=RecordView, status_code=201)
async def create(
    kind: Kind,
    payload: Input,
    request: Request,
    p: Auth,
    idempotency_key: Annotated[UUID, Header()],
) -> dict:
    await lock(p, request)
    fp = hashlib.sha256(
        json.dumps(payload.model_dump(mode="json"), sort_keys=True).encode()
    ).hexdigest()
    prior = (
        (
            await p.conn.execute(
                sa.select(requests).where(
                    requests.c.key == idempotency_key,
                    requests.c.organization_id == p.session["organization_id"],
                    requests.c.user_id == p.user["id"],
                )
            )
        )
        .mappings()
        .first()
    )
    if prior:
        if prior["resource"] != kind or prior["fingerprint"] != fp:
            fail(409, "Idempotency key already used for another command")
        replay = await get(p, kind, prior["target_id"])
        await authorize(p, kind, payload.model_dump(exclude={"kind"}), replay)
        return view(kind, replay)
    try:
        result = await write(p, request, kind, payload, None, None, "")
        await p.conn.execute(
            requests.insert().values(
                organization_id=p.session["organization_id"],
                user_id=p.user["id"],
                key=idempotency_key,
                fingerprint=fp,
                resource=kind,
                target_id=result["id"],
            )
        )
        return result
    except IntegrityError as e:
        raise HTTPException(409, "Conflicting record or invalid scoped reference") from e


@router.patch("/{kind}/{id_}", response_model=RecordView)
async def update(
    kind: Kind,
    id_: UUID,
    payload: Input,
    request: Request,
    p: Auth,
    if_match: Annotated[int | None, Header()] = None,
    x_change_reason: Annotated[str, Header(max_length=1000)] = "",
) -> dict:
    try:
        return await write(p, request, kind, payload, id_, if_match, x_change_reason)
    except IntegrityError as e:
        raise HTTPException(409, "Conflicting record or invalid scoped reference") from e
