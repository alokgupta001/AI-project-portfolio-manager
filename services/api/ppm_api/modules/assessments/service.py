"""Assessment workflows, grants, history and shared data operations."""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import Request
from fastapi.encoders import jsonable_encoder

from ppm_api.modules.assessments import tables as T
from ppm_api.modules.assessments.access import evidence_access, get, oid
from ppm_api.modules.assessments.mutations import revision
from ppm_api.modules.assessments.schemas import (
    AccessInput,
    ActionInput,
    AnswerBatchInput,
    AnswerRecord,
    AssignmentInput,
    ReviewInput,
)
from ppm_api.modules.assessments.scoring import compute_scores
from ppm_api.modules.assessments.validation import questions, valid_answer
from ppm_api.modules.delivery.service import fail
from ppm_api.modules.identity.service import Principal, now
from ppm_api.modules.identity.tables import memberships, users
from ppm_api.shared.table_registry import TABLES


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


async def finalize_check(p: Principal, a: Any) -> Any:
    data = await scoring(p, a)
    if data["notes"] or data["overall_score"] is None:
        fail(422, "Complete required answers and all scoring dimensions first")
    return data


async def assign_assessment(payload: AssignmentInput, p: Principal) -> Any:
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
    from ppm_api.modules.workspace.service import notify

    for user in [row["assigned_to"], row["reviewer_id"]]:
        await notify(p.conn, oid(p), user, "assessments", row["id"], f"{row['id']}:assigned")
    return await a_view(p, row)


async def list_assessments(
    p: Principal, offset: int, limit: int, framework_version_id: UUID | None, q: str
) -> Any:
    from ppm_api.modules.workspace.service import term

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


async def get_assessment(assessment_id: UUID, p: Principal) -> Any:
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


async def save_answers(
    assessment_id: UUID, payload: AnswerBatchInput, request: Request, p: Principal
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
    return await get_assessment(assessment_id, p)


async def submit_assessment(
    assessment_id: UUID, payload: ActionInput, request: Request, p: Principal
) -> Any:
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
    from ppm_api.modules.workspace.service import notify

    await notify(
        p.conn,
        oid(p),
        a["reviewer_id"],
        "assessments",
        assessment_id,
        f"{assessment_id}:{a['revision']}:review",
    )
    return await a_view(p, row)


async def review_assessment(
    assessment_id: UUID, payload: ReviewInput, request: Request, p: Principal
) -> Any:
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


async def set_access_grant(payload: AccessInput, p: Principal) -> Any:
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


async def list_assessment_events(assessment_id: UUID, p: Principal) -> Any:
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


async def list_access_grants(
    p: Principal, framework_id: UUID | None = None, assessment_id: UUID | None = None
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
