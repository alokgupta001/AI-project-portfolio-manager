"""Private assessment evidence intake, storage, preview and reviewer release."""

from __future__ import annotations

import base64
import hashlib
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import Request, Response
from starlette.concurrency import run_in_threadpool

from ppm_api.modules.assessments import tables as T
from ppm_api.modules.assessments.access import evidence_access, get, oid
from ppm_api.modules.assessments.mutations import revision
from ppm_api.modules.assessments.schemas import ActionInput, EvidenceInput
from ppm_api.modules.assessments.service import bump, event
from ppm_api.modules.assessments.validation import questions
from ppm_api.modules.delivery.service import fail
from ppm_api.modules.identity.service import Principal, now
from ppm_api.storage import LocalObjectStore


async def list_evidence(assessment_id: UUID, p: Principal) -> Any:
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


async def upload_evidence(
    assessment_id: UUID, payload: EvidenceInput, request: Request, p: Principal
) -> Any:
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


async def download_evidence(
    assessment_id: UUID, evidence_id: UUID, request: Request, p: Principal
) -> Any:
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


async def delete_evidence(
    assessment_id: UUID, evidence_id: UUID, request: Request, p: Principal
) -> Any:
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


async def preview_evidence(
    assessment_id: UUID, evidence_id: UUID, request: Request, p: Principal
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


async def release_evidence(
    assessment_id: UUID, evidence_id: UUID, payload: ActionInput, request: Request, p: Principal
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
