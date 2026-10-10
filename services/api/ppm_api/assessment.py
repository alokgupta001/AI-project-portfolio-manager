"""Versioned assessment workflows with scoped access and deterministic scoring."""

from __future__ import annotations

import base64
import hashlib
import json
from decimal import Decimal
from functools import wraps
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import APIRouter, Query, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.concurrency import run_in_threadpool

from ppm_api import assessment_tables as T
from ppm_api.assessment_schemas import (
    AccessInput,
    ActionInput,
    AnswerBatchInput,
    AnswerRecord,
    AssessmentDetail,
    AssessmentRecord,
    AssignmentInput,
    EventRecord,
    EvidenceInput,
    EvidenceRecord,
    FrameworkInput,
    FrameworkRecord,
    ReviewInput,
    VersionRecord,
)
from ppm_api.delivery import fail, lock
from ppm_api.identity import Auth, Principal, now, record
from ppm_api.identity_tables import memberships, users
from ppm_api.ppm_tables import TABLES
from ppm_api.storage import LocalObjectStore


class BoundedRoute(APIRoute):
    def get_route_handler(self) -> Any:
        original = super().get_route_handler()

        async def bounded(request: Request) -> Any:
            if request.method not in ("GET", "HEAD", "OPTIONS"):
                chunks = []
                size = 0
                async for chunk in request.stream():
                    size += len(chunk)
                    if size > 2097152:
                        fail(413, "Assessment request exceeds 2 MiB")
                    chunks.append(chunk)
                request._body = b"".join(chunks)
            return await original(request)

        return bounded


router = APIRouter(prefix="/api/v1/assessment", tags=["Assessment"], route_class=BoundedRoute)
EXAMPLE_FRAMEWORKS = json.loads(
    Path(__file__).with_name("assessment_examples.json").read_text(encoding="utf-8")
)


def oid(p: Principal) -> Any:
    return p.session["organization_id"]


async def get(p: Principal, table: Any, id_: Any) -> Any:
    row = (
        (
            await p.conn.execute(
                sa.select(table).where(table.c.id == id_, table.c.organization_id == oid(p))
            )
        )
        .mappings()
        .first()
    )
    if row is None:
        fail(404, "Record not found or access restricted")
    return row


async def grant(p: Principal, field: Any, id_: Any) -> Any:
    return bool(
        await p.conn.scalar(
            sa.select(T.assessment_access.c.id)
            .where(
                T.assessment_access.c.organization_id == oid(p),
                T.assessment_access.c.user_id == p.user["id"],
                T.assessment_access.c[field] == id_,
                T.assessment_access.c.active,
            )
            .limit(1)
        )
    )


async def can_edit(p: Principal, id_: Any) -> Any:
    return p.role == "Admin" or (
        p.role == "Project Manager" and await grant(p, "framework_id", id_)
    )


def eligible(p: Principal) -> Any:
    if p.role not in ("Admin", "Project Manager"):
        fail(403, "An eligible assessment role is required")


def respondent(p: Principal, a: Any) -> Any:
    eligible(p)
    if p.user["id"] != a["assigned_to"]:
        fail(403, "Only the assigned respondent can answer or submit")


def reviewer(p: Principal, a: Any) -> Any:
    eligible(p)
    if p.user["id"] != a["reviewer_id"] or p.user["id"] in (a["assigned_to"], a["submitted_by"]):
        fail(403, "Only the assigned independent reviewer can review")


def evidence_access(p: Principal, a: Any) -> Any:
    if p.role != "Admin" and (
        p.role != "Project Manager" or p.user["id"] not in (a["assigned_to"], a["reviewer_id"])
    ):
        fail(403, "Result access does not grant access to private answers or evidence")


async def command_access(p: Principal, request: Request) -> Any:
    """Recheck live scope even on idempotent replays."""
    eligible(p)
    path = request.url.path
    params = request.path_params
    if "assessment_id" in params:
        a = await get(p, T.assessments, UUID(str(params["assessment_id"])))
        if path.endswith("/review") or path.endswith("/release"):
            reviewer(p, a)
        else:
            respondent(p, a)
    elif "framework_id" in params:
        fid = UUID(str(params["framework_id"]))
        await get(p, T.frameworks, fid)
        if not await can_edit(p, fid) or (path.endswith("/publish") and p.role != "Admin"):
            fail(403, "Framework edit/publish access required")
    elif p.role != "Admin":
        fail(403, "Administration requires Admin")


def mutation(fn: Any) -> Any:

    @wraps(fn)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        p, request = (kwargs["p"], kwargs["request"])
        await lock(p, request)
        await command_access(p, request)
        try:
            key = UUID(request.headers.get("idempotency-key", ""))
        except ValueError:
            fail(428, "A UUID Idempotency-Key is required")
        body = await request.body()
        fingerprint = hashlib.sha256(
            request.method.encode()
            + request.url.path.encode()
            + body
            + request.headers.get("if-match", "").encode()
        ).hexdigest()
        old = (
            (
                await p.conn.execute(
                    sa.select(T.assessment_requests).where(
                        T.assessment_requests.c.organization_id == oid(p),
                        T.assessment_requests.c.user_id == p.user["id"],
                        T.assessment_requests.c.key == key,
                    )
                )
            )
            .mappings()
            .first()
        )
        if old:
            if old["fingerprint"] != fingerprint:
                fail(409, "Idempotency key already used for a different request")
            return old["response"]
        try:
            result = await fn(*args, **kwargs)
        except ValidationError as exc:
            fail(422, str(exc.errors(include_input=False)))
        except IntegrityError:
            fail(409, "Conflicting record or invalid scoped reference")
        encoded = jsonable_encoder(result)
        await p.conn.execute(
            T.assessment_requests.insert().values(
                id=uuid4(),
                organization_id=oid(p),
                created_at=now(),
                user_id=p.user["id"],
                key=key,
                fingerprint=fingerprint,
                response=encoded,
            )
        )
        await record(p.conn, request, p.user["id"], oid(p), "assessment." + fn.__name__)
        return result

    return wrapped


def revision(request: Request, row: Any) -> Any:
    supplied = request.headers.get("if-match")
    if supplied is None:
        fail(428, "If-Match revision is required")
    if supplied != str(row["revision"]):
        fail(412, "This record changed. Reload before saving")


async def bump(p: Principal, a: Any) -> Any:
    await p.conn.execute(
        T.assessments.update()
        .where(T.assessments.c.id == a["id"])
        .values(revision=a["revision"] + 1, results=None)
    )


async def event(p: Principal, aid: Any, name: Any, note: Any = "", details: Any = None) -> Any:
    await p.conn.execute(
        T.assessment_events.insert().values(
            id=uuid4(),
            organization_id=oid(p),
            created_at=now(),
            assessment_id=aid,
            actor_id=p.user["id"],
            event=name,
            note=note,
            details=jsonable_encoder(details or {}),
        )
    )


def questions(snapshot: Any) -> Any:
    return {str(q["id"]): q for d in snapshot["dimensions"] for q in d["questions"]}


def validate_definition(snapshot: Any) -> Any:
    dims = snapshot["dimensions"]
    if not dims or sum(Decimal(str(d["weight"])) for d in dims) != 1:
        fail(422, "Dimension weights must sum exactly to 1")
    for d in dims:
        if not any(q["answer_type"] != "text" for q in d["questions"]):
            fail(422, "Each dimension requires at least one numeric question")
        for q in d["questions"]:
            levels = [v["level"] for v in q.get("rubric_levels", [])]
            if q["answer_type"] == "rubric" and (
                len(levels) < 2 or len(set(levels)) != len(levels)
            ):
                fail(422, "Rubrics require at least two distinct levels")
            if q["answer_type"] != "rubric" and levels:
                fail(422, "Only rubric questions may define levels")


def _normalize_rubric(value: Any, minimum: Any, maximum: Any) -> Any:
    try:
        v = Decimal(str(value))
        if not v.is_finite() or v != int(v) or minimum >= maximum or (not minimum <= v <= maximum):
            return None
        return (v - minimum) / Decimal(maximum - minimum)
    except (ValueError, ArithmeticError):
        return None


def valid_answer(q: Any, value: Any) -> Any:
    if value is None or not str(value).strip():
        return False
    if q["answer_type"] == "text":
        return True
    if q["answer_type"] == "boolean":
        return value in ("true", "false")
    return str(value) in {str(v["level"]) for v in q["rubric_levels"]}


def compute_scores(snapshot: Any, answer_map: Any, reviewer_adjustments: Any = None) -> Any:
    notes = []
    results = {}
    overall = Decimal(0)
    unknown = False
    for d in snapshot.get("dimensions", []):
        numerator = denominator = answered_weight = Decimal(0)
        total_weight = sum((Decimal(str(q["weight"])) for q in d["questions"]), Decimal(0))
        answered = evidence = 0
        for q in d["questions"]:
            aid = str(q["id"])
            a = answer_map.get(aid, {})
            if a.get("evidence_text", "").strip() or a.get("has_attachment"):
                evidence += 1
            if not valid_answer(q, a.get("value")):
                if q.get("required", True):
                    notes.append(f"Required answer missing: {(q['name'] if 'name' in q else aid)}")
                continue
            w = Decimal(str(q["weight"]))
            answered_weight += w
            answered += 1
            if q["answer_type"] == "text":
                continue
            if q["answer_type"] == "boolean":
                norm = Decimal(1 if a["value"] == "true" else 0)
            else:
                levels = [lv["level"] for lv in q["rubric_levels"]]
                norm = _normalize_rubric(a["value"], min(levels), max(levels))
            if norm is None:
                continue
            if reviewer_adjustments and aid in reviewer_adjustments:
                norm = Decimal(str(reviewer_adjustments[aid])) / 100
            numerator += w * norm
            denominator += w
        score = (100 * numerator / denominator).quantize(Decimal("0.0001")) if denominator else None
        weight = Decimal(str(d["weight"]))
        if score is None:
            unknown = True
        else:
            overall += weight * score
        results[str(d["id"])] = dict(
            dimension_id=str(d["id"]),
            dimension_name=d["name"],
            score=score,
            weight=weight,
            answered_count=answered,
            total_required=sum(q.get("required", True) for q in d["questions"]),
            coverage_percent=(100 * answered_weight / total_weight).quantize(Decimal(".01"))
            if total_weight
            else Decimal(0),
            evidence_coverage_percent=(Decimal(100 * evidence) / len(d["questions"])).quantize(
                Decimal(".01")
            )
            if d["questions"]
            else Decimal(0),
        )
    if sum(Decimal(str(d["weight"])) for d in snapshot.get("dimensions", [])) != 1:
        unknown = True
    return (None if unknown or not results else overall.quantize(Decimal(".0001")), results, notes)


async def answer_map(p: Principal, aid: Any) -> Any:
    rows = (
        await p.conn.execute(sa.select(T.answers).where(T.answers.c.assessment_id == aid))
    ).mappings()
    out = {str(r["question_id"]): dict(r) for r in rows}
    evidence = (
        await p.conn.execute(
            sa.select(T.evidence_attachments.c.question_id).where(
                T.evidence_attachments.c.assessment_id == aid, T.evidence_attachments.c.released
            )
        )
    ).scalars()
    for qid in evidence:
        out.setdefault(str(qid), {})["has_attachment"] = True
    return out


async def scoring(p: Principal, a: Any) -> Any:
    v = await get(p, T.framework_versions, a["framework_version_id"])
    answers = await answer_map(p, a["id"])
    overrides = {
        q: r["reviewer_score"] for q, r in answers.items() if r.get("reviewer_score") is not None
    }
    score, dims, notes = compute_scores(v["snapshot"], answers, overrides)
    return dict(overall_score=score, dimension_scores=list(dims.values()), notes=notes)


async def fw_view(p: Principal, row: Any) -> Any:
    ver = await p.conn.scalar(
        sa.select(sa.func.max(T.framework_versions.c.version)).where(
            T.framework_versions.c.framework_id == row["id"]
        )
    )
    return dict(
        **row["definition"],
        id=row["id"],
        revision=row["revision"],
        published_version=ver,
        can_edit=await can_edit(p, row["id"]),
    )


async def a_view(p: Principal, a: Any) -> Any:
    v = await get(p, T.framework_versions, a["framework_version_id"])
    data = a["results"] or await scoring(p, a)
    return dict(
        id=a["id"],
        name=a["name"],
        framework_version_id=a["framework_version_id"],
        department_id=a["department_id"],
        team_id=a["team_id"],
        assigned_to=a["assigned_to"],
        reviewer_id=a["reviewer_id"],
        revision=a["revision"],
        status=a["status"],
        framework_name=v["snapshot"]["name"],
        framework_version=v["version"],
        overall_score=data["overall_score"],
        dimension_scores=data["dimension_scores"],
        provisional=a["status"] != "completed",
        can_read_evidence=p.role == "Admin"
        or (p.role == "Project Manager" and p.user["id"] in (a["assigned_to"], a["reviewer_id"])),
        can_answer=p.role in ("Admin", "Project Manager")
        and p.user["id"] == a["assigned_to"]
        and (a["status"] in ("draft", "returned")),
        can_review=p.role in ("Admin", "Project Manager")
        and p.user["id"] == a["reviewer_id"]
        and (a["status"] in ("submitted", "in_review")),
    )


@router.get("/frameworks", response_model=list[FrameworkRecord])
async def list_frameworks(
    p: Auth, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100)
) -> Any:
    rows = (
        await p.conn.execute(
            sa.select(T.frameworks)
            .order_by(T.frameworks.c.created_at, T.frameworks.c.id)
            .offset(offset)
            .limit(limit)
        )
    ).mappings()
    return [await fw_view(p, r) for r in rows]


@router.post("/frameworks", response_model=FrameworkRecord, status_code=201)
@mutation
async def create_framework(payload: FrameworkInput, request: Request, p: Auth) -> Any:
    row = (
        (
            await p.conn.execute(
                T.frameworks.insert()
                .values(
                    id=uuid4(),
                    organization_id=oid(p),
                    created_at=now(),
                    revision=1,
                    definition=payload.model_dump(mode="json"),
                )
                .returning(T.frameworks)
            )
        )
        .mappings()
        .one()
    )
    return await fw_view(p, row)


@router.put("/frameworks/{framework_id}", response_model=FrameworkRecord)
@mutation
async def edit_framework(
    framework_id: UUID, payload: FrameworkInput, request: Request, p: Auth
) -> Any:
    old = await get(p, T.frameworks, framework_id)
    revision(request, old)
    row = (
        (
            await p.conn.execute(
                T.frameworks.update()
                .where(T.frameworks.c.id == framework_id)
                .values(revision=old["revision"] + 1, definition=payload.model_dump(mode="json"))
                .returning(T.frameworks)
            )
        )
        .mappings()
        .one()
    )
    return await fw_view(p, row)


@router.post("/frameworks/{framework_id}/publish", response_model=VersionRecord, status_code=201)
@mutation
async def publish_framework(
    framework_id: UUID, payload: ActionInput, request: Request, p: Auth
) -> Any:
    fw = await get(p, T.frameworks, framework_id)
    revision(request, fw)
    if fw["definition"]["archived"]:
        fail(409, "Archived frameworks cannot be published")
    validate_definition(fw["definition"])
    ver = await p.conn.scalar(
        sa.select(sa.func.coalesce(sa.func.max(T.framework_versions.c.version), 0)).where(
            T.framework_versions.c.framework_id == framework_id
        )
    )
    row = (
        (
            await p.conn.execute(
                T.framework_versions.insert()
                .values(
                    id=uuid4(),
                    organization_id=oid(p),
                    created_at=now(),
                    framework_id=framework_id,
                    version=ver + 1,
                    snapshot=fw["definition"],
                    published_by=p.user["id"],
                )
                .returning(T.framework_versions)
            )
        )
        .mappings()
        .one()
    )
    await p.conn.execute(
        T.frameworks.update()
        .where(T.frameworks.c.id == framework_id)
        .values(revision=fw["revision"] + 1)
    )
    return dict(row)


@router.get("/frameworks/{framework_id}/versions", response_model=list[VersionRecord])
async def versions(framework_id: UUID, p: Auth) -> Any:
    await get(p, T.frameworks, framework_id)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(T.framework_versions)
                .where(T.framework_versions.c.framework_id == framework_id)
                .order_by(T.framework_versions.c.version.desc())
            )
        ).mappings()
    ]


@router.post("/seed-examples", response_model=list[FrameworkRecord], status_code=201)
@mutation
async def seed_examples(request: Request, p: Auth) -> Any:
    out = []
    for original in EXAMPLE_FRAMEWORKS:
        data = json.loads(json.dumps(original))
        for d in data["dimensions"]:
            for q in d["questions"]:
                q["rubric_levels"] = q.pop("levels", [])
        payload = FrameworkInput.model_validate(data)
        old = (
            (
                await p.conn.execute(
                    sa.select(T.frameworks).where(
                        T.frameworks.c.definition["name"].astext == payload.name
                    )
                )
            )
            .mappings()
            .first()
        )
        if old is None:
            old = (
                (
                    await p.conn.execute(
                        T.frameworks.insert()
                        .values(
                            id=uuid4(),
                            organization_id=oid(p),
                            created_at=now(),
                            revision=1,
                            definition=payload.model_dump(mode="json"),
                        )
                        .returning(T.frameworks)
                    )
                )
                .mappings()
                .one()
            )
        out.append(await fw_view(p, old))
    return out


@router.post("/access", response_model=AccessInput)
@mutation
async def set_access(payload: AccessInput, request: Request, p: Auth) -> Any:
    role = await p.conn.scalar(
        sa.select(memberships.c.role).where(
            memberships.c.organization_id == oid(p),
            memberships.c.user_id == payload.user_id,
            memberships.c.active,
        )
    )
    if not role or (payload.framework_id and role != "Project Manager"):
        fail(422, "Editors need an active PM role; result readers need active membership")
    field = "framework_id" if payload.framework_id else "assessment_id"
    target = getattr(payload, field)
    await get(p, T.frameworks if payload.framework_id else T.assessments, target)
    if payload.assessment_id:
        a = await get(p, T.assessments, target)
        if a["status"] != "completed":
            fail(409, "Result read grants require a completed assessment")
    await p.conn.execute(
        T.assessment_access.update()
        .where(
            T.assessment_access.c.user_id == payload.user_id, T.assessment_access.c[field] == target
        )
        .values(active=False)
    )
    await p.conn.execute(
        T.assessment_access.insert().values(
            id=uuid4(), organization_id=oid(p), created_at=now(), **payload.model_dump()
        )
    )
    return payload.model_dump()


@router.post("/assessments", response_model=AssessmentRecord, status_code=201)
@mutation
async def assign(payload: AssignmentInput, request: Request, p: Auth) -> Any:
    await get(p, T.framework_versions, payload.framework_version_id)
    for uid in (payload.assigned_to, payload.reviewer_id):
        role = await p.conn.scalar(
            sa.select(memberships.c.role).where(
                memberships.c.organization_id == oid(p),
                memberships.c.user_id == uid,
                memberships.c.active,
            )
        )
        if role not in ("Admin", "Project Manager"):
            fail(422, "Respondent and reviewer must be active eligible members")
    for field, kind in [("department_id", "departments"), ("team_id", "teams")]:
        target = getattr(payload, field)
        if target:
            scoped = await get(p, TABLES[kind], target)
            if scoped["archived"]:
                fail(422, "Scope is archived")
            if (
                kind == "teams"
                and payload.department_id
                and (scoped["department_id"] != payload.department_id)
            ):
                fail(422, "Team does not belong to the selected department")
    row = (
        (
            await p.conn.execute(
                T.assessments.insert()
                .values(
                    id=uuid4(),
                    organization_id=oid(p),
                    created_at=now(),
                    revision=1,
                    status="draft",
                    **payload.model_dump(),
                )
                .returning(T.assessments)
            )
        )
        .mappings()
        .one()
    )
    await event(p, row["id"], "assigned", details=payload.model_dump())
    from ppm_api.pilot import notify

    for user in [row["assigned_to"], row["reviewer_id"]]:
        await notify(p.conn, oid(p), user, "assessments", row["id"], f"{row['id']}:assigned")
    return await a_view(p, row)


@router.get("/assessments", response_model=list[AssessmentRecord])
async def list_assessments(
    p: Auth,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    framework_version_id: UUID | None = None,
    q: str = Query("", max_length=160),
) -> Any:
    from ppm_api.pilot import term

    query = sa.select(T.assessments).where(T.assessments.c.name.ilike(term(q), escape="\\"))
    if framework_version_id:
        query = query.where(T.assessments.c.framework_version_id == framework_version_id)
    rows = (
        await p.conn.execute(
            query.order_by(T.assessments.c.created_at.desc(), T.assessments.c.id)
            .offset(offset)
            .limit(limit)
        )
    ).mappings()
    return [await a_view(p, r) for r in rows]


@router.get("/assessments/{assessment_id}", response_model=AssessmentDetail)
async def detail(assessment_id: UUID, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    v = await get(p, T.framework_versions, a["framework_version_id"])
    data = a["results"] or await scoring(p, a)
    rows = await answer_map(p, assessment_id)
    return dict(
        assessment=await a_view(p, a),
        snapshot=v["snapshot"],
        answers=[{k: r[k] for k in AnswerRecord.model_fields} for r in rows.values() if "id" in r],
        notes=data["notes"],
    )


@router.put("/assessments/{assessment_id}/answers", response_model=AssessmentDetail)
@mutation
async def save_answers(
    assessment_id: UUID, payload: AnswerBatchInput, request: Request, p: Auth
) -> Any:
    a = await get(p, T.assessments, assessment_id)
    revision(request, a)
    if a["status"] not in ("draft", "returned"):
        fail(409, "Answers are editable only in draft or returned assessments")
    v = await get(p, T.framework_versions, a["framework_version_id"])
    qs = questions(v["snapshot"])
    seen = set()
    for answer in payload.items:
        q = qs.get(str(answer.question_id))
        if not q or answer.question_id in seen:
            fail(422, "Question must occur once and belong to the frozen framework")
        seen.add(answer.question_id)
        if answer.value and (not valid_answer(q, answer.value)):
            fail(422, "Answer does not match the published question or rubric")
        old = (
            (
                await p.conn.execute(
                    sa.select(T.answers).where(
                        T.answers.c.assessment_id == assessment_id,
                        T.answers.c.question_id == answer.question_id,
                    )
                )
            )
            .mappings()
            .first()
        )
        values = dict(**answer.model_dump(), reviewer_score=None, reviewer_note=None)
        if old:
            await p.conn.execute(
                T.answers.update().where(T.answers.c.id == old["id"]).values(**values)
            )
        else:
            await p.conn.execute(
                T.answers.insert().values(
                    id=uuid4(),
                    organization_id=oid(p),
                    created_at=now(),
                    assessment_id=assessment_id,
                    **values,
                )
            )
        await event(
            p,
            assessment_id,
            "answer_saved",
            details={"before": dict(old) if old else None, "after": values},
        )
    await p.conn.execute(
        T.assessments.update()
        .where(T.assessments.c.id == assessment_id)
        .values(results=None, revision=a["revision"] + 1)
    )
    return await detail(assessment_id, p)


async def finalize_check(p: Principal, a: Any) -> Any:
    data = await scoring(p, a)
    if data["notes"] or data["overall_score"] is None:
        fail(422, "Complete required answers and all scoring dimensions first")
    return data


@router.post("/assessments/{assessment_id}/submit", response_model=AssessmentRecord)
@mutation
async def submit(assessment_id: UUID, payload: ActionInput, request: Request, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    revision(request, a)
    if a["status"] not in ("draft", "returned"):
        fail(409, "Only draft or returned assessments can be submitted")
    data = await finalize_check(p, a)
    row = (
        (
            await p.conn.execute(
                T.assessments.update()
                .where(T.assessments.c.id == assessment_id)
                .values(
                    status="submitted",
                    submitted_by=p.user["id"],
                    results=jsonable_encoder(data),
                    revision=a["revision"] + 1,
                )
                .returning(T.assessments)
            )
        )
        .mappings()
        .one()
    )
    await event(p, assessment_id, "submitted", payload.note, data)
    from ppm_api.pilot import notify

    await notify(
        p.conn,
        oid(p),
        a["reviewer_id"],
        "assessments",
        assessment_id,
        f"{assessment_id}:{a['revision']}:review",
    )
    return await a_view(p, row)


@router.post("/assessments/{assessment_id}/review", response_model=AssessmentRecord)
@mutation
async def review(assessment_id: UUID, payload: ReviewInput, request: Request, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    revision(request, a)
    if a["status"] not in ("submitted", "in_review"):
        fail(409, "Review requires a submitted assessment")
    if payload.action == "start" and (a["status"] != "submitted" or payload.adjustments):
        fail(409, "Start review from submitted without adjustments")
    seen = set()
    for adj in payload.adjustments:
        answer = await get(p, T.answers, adj.answer_id)
        if answer["assessment_id"] != assessment_id or adj.answer_id in seen:
            fail(422, "Adjustment must target a unique answer in this assessment")
        seen.add(adj.answer_id)
        v = await get(p, T.framework_versions, a["framework_version_id"])
        q = questions(v["snapshot"])[str(answer["question_id"])]
        if q["answer_type"] == "text" or not valid_answer(q, answer["value"]):
            fail(422, "Only valid numeric answers can be adjusted")
        await p.conn.execute(
            T.answers.update()
            .where(T.answers.c.id == adj.answer_id, T.answers.c.assessment_id == assessment_id)
            .values(reviewer_score=adj.reviewer_score, reviewer_note=adj.reviewer_note)
        )
        await event(
            p,
            assessment_id,
            "score_adjusted",
            adj.reviewer_note,
            {"before": dict(answer), "after": adj.model_dump()},
        )
    if payload.action == "complete":
        quarantined = await p.conn.scalar(
            sa.select(sa.func.count())
            .select_from(T.evidence_attachments)
            .where(
                T.evidence_attachments.c.assessment_id == assessment_id,
                ~T.evidence_attachments.c.released,
            )
        )
        if quarantined:
            fail(409, "Review and release quarantined text evidence before completion")
    data = await finalize_check(p, a) if payload.action == "complete" else await scoring(p, a)
    status = {"start": "in_review", "return": "returned", "complete": "completed"}[payload.action]
    row = (
        (
            await p.conn.execute(
                T.assessments.update()
                .where(T.assessments.c.id == assessment_id)
                .values(status=status, results=jsonable_encoder(data), revision=a["revision"] + 1)
                .returning(T.assessments)
            )
        )
        .mappings()
        .one()
    )
    await event(p, assessment_id, status, payload.note, data)
    return await a_view(p, row)


@router.get("/assessments/{assessment_id}/events", response_model=list[EventRecord])
async def history(assessment_id: UUID, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    evidence_access(p, a)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(T.assessment_events)
                .where(T.assessment_events.c.assessment_id == assessment_id)
                .order_by(T.assessment_events.c.created_at, T.assessment_events.c.id)
            )
        ).mappings()
    ]


@router.get("/assessments/{assessment_id}/evidence", response_model=list[EvidenceRecord])
async def evidence_list(assessment_id: UUID, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    evidence_access(p, a)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(T.evidence_attachments)
                .where(T.evidence_attachments.c.assessment_id == assessment_id)
                .order_by(T.evidence_attachments.c.created_at)
            )
        ).mappings()
    ]


@router.post(
    "/assessments/{assessment_id}/evidence", response_model=EvidenceRecord, status_code=201
)
@mutation
async def upload(assessment_id: UUID, payload: EvidenceInput, request: Request, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    revision(request, a)
    if a["status"] not in ("draft", "returned"):
        fail(409, "Evidence is frozen after submission")
    v = await get(p, T.framework_versions, a["framework_version_id"])
    if str(payload.question_id) not in questions(v["snapshot"]):
        fail(422, "Question is not in the published framework")
    try:
        content = base64.b64decode(payload.content_base64, validate=True)
        text = content.decode("utf-8")
    except (ValueError, UnicodeError):
        fail(422, "Evidence must be base64-encoded UTF-8 plain text")
    if not 0 < len(content) <= 524288 or any(ord(c) < 32 and c not in "\n\r\t" for c in text):
        fail(422, "Evidence must be plain text between 1 byte and 512 KiB")
    if any(x in text.lower() for x in ("<script", "<html", "<?xml", "<!doctype", "x5o!p%@ap[4")):
        fail(422, "Active markup or test-malware signature is not accepted as plain text")
    count = await p.conn.scalar(
        sa.select(sa.func.count())
        .select_from(T.evidence_attachments)
        .where(T.evidence_attachments.c.assessment_id == assessment_id)
    )
    if (count or 0) >= 50:
        fail(422, "Maximum 50 evidence attachments per assessment")
    eid = uuid4()
    key = f"{oid(p)}/assessments/{assessment_id}/{eid}.txt"
    digest = hashlib.sha256(content).hexdigest()
    store = LocalObjectStore(request.app.state.settings.storage_root)
    await run_in_threadpool(store.put, key, content)
    row = (
        (
            await p.conn.execute(
                T.evidence_attachments.insert()
                .values(
                    id=eid,
                    organization_id=oid(p),
                    created_at=now(),
                    assessment_id=assessment_id,
                    question_id=payload.question_id,
                    file_name=payload.file_name,
                    file_size=len(content),
                    sha256=digest,
                    released=False,
                    storage_path=key,
                    uploaded_by=p.user["id"],
                )
                .returning(T.evidence_attachments)
            )
        )
        .mappings()
        .one()
    )
    await bump(p, a)
    await event(
        p,
        assessment_id,
        "evidence_added",
        details={"id": eid, "sha256": digest, "file_name": payload.file_name},
    )
    return dict(row)


@router.get("/assessments/{assessment_id}/evidence/{evidence_id}")
async def download(assessment_id: UUID, evidence_id: UUID, request: Request, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    evidence_access(p, a)
    row = await get(p, T.evidence_attachments, evidence_id)
    if row["assessment_id"] != assessment_id:
        fail(404, "Evidence not found")
    if not row["released"]:
        fail(409, "Evidence is quarantined until the independent reviewer releases it")
    store = LocalObjectStore(request.app.state.settings.storage_root)
    content = await run_in_threadpool(store.get, row["storage_path"])
    if hashlib.sha256(content).hexdigest() != row["sha256"]:
        fail(409, "Evidence integrity check failed")
    return Response(
        content,
        media_type="text/plain; charset=utf-8",
        headers={
            "Content-Disposition": f'''attachment; filename="{row["file_name"]}"''',
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.delete("/assessments/{assessment_id}/evidence/{evidence_id}", response_model=ActionInput)
@mutation
async def delete_evidence(assessment_id: UUID, evidence_id: UUID, request: Request, p: Auth) -> Any:
    a = await get(p, T.assessments, assessment_id)
    revision(request, a)
    if a["status"] not in ("draft", "returned"):
        fail(409, "Submitted evidence is retained with assessment history")
    row = await get(p, T.evidence_attachments, evidence_id)
    if row["assessment_id"] != assessment_id:
        fail(404, "Evidence not found")
    await p.conn.execute(
        T.evidence_attachments.delete().where(T.evidence_attachments.c.id == evidence_id)
    )
    await bump(p, a)
    await event(
        p, assessment_id, "evidence_removed", details={"id": evidence_id, "sha256": row["sha256"]}
    )
    return {"note": "Attachment removed from this draft"}


@router.get(
    "/assessments/{assessment_id}/evidence/{evidence_id}/preview", response_model=dict[str, str]
)
async def preview_evidence(
    assessment_id: UUID, evidence_id: UUID, request: Request, p: Auth
) -> dict:
    a = await get(p, T.assessments, assessment_id)
    evidence_access(p, a)
    row = await get(p, T.evidence_attachments, evidence_id)
    if row["assessment_id"] != assessment_id:
        fail(404, "Evidence not found")
    content = await run_in_threadpool(
        LocalObjectStore(request.app.state.settings.storage_root).get, row["storage_path"]
    )
    if hashlib.sha256(content).hexdigest() != row["sha256"]:
        fail(409, "Evidence integrity check failed")
    return {"note": content.decode("utf-8")}


@router.post(
    "/assessments/{assessment_id}/evidence/{evidence_id}/release", response_model=EvidenceRecord
)
@mutation
async def release_evidence(
    assessment_id: UUID, evidence_id: UUID, payload: ActionInput, request: Request, p: Auth
) -> dict:
    a = await get(p, T.assessments, assessment_id)
    revision(request, a)
    if a["status"] not in ("submitted", "in_review") or not payload.note.strip():
        fail(409, "Release requires independent review and a reason")
    row = await get(p, T.evidence_attachments, evidence_id)
    if row["assessment_id"] != assessment_id:
        fail(404, "Evidence not found")
    updated = (
        (
            await p.conn.execute(
                T.evidence_attachments.update()
                .where(T.evidence_attachments.c.id == evidence_id)
                .values(released=True)
                .returning(T.evidence_attachments)
            )
        )
        .mappings()
        .one()
    )
    await bump(p, a)
    await event(
        p,
        assessment_id,
        "evidence_released",
        payload.note,
        {"id": evidence_id, "sha256": row["sha256"]},
    )
    return dict(updated)


@router.get("/access", response_model=list[dict])
async def access_list(
    p: Auth, framework_id: UUID | None = None, assessment_id: UUID | None = None
) -> Any:
    if p.role != "Admin":
        fail(403, "Only Admin manages grants")
    if (framework_id is None) == (assessment_id is None):
        fail(422, "Choose one target")
    await get(p, T.frameworks if framework_id else T.assessments, framework_id or assessment_id)
    rows = (
        await p.conn.execute(
            sa.select(T.assessment_access, users.c.name)
            .join(users, users.c.id == T.assessment_access.c.user_id)
            .where(
                T.assessment_access.c.framework_id == framework_id
                if framework_id
                else T.assessment_access.c.assessment_id == assessment_id,
                T.assessment_access.c.active,
            )
            .order_by(T.assessment_access.c.id)
        )
    ).mappings()
    return [dict(r) for r in rows]
