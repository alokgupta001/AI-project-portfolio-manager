"""Scoped document library, keyword search and source reads."""

from typing import Any
from uuid import UUID

import sqlalchemy as sa

from ppm_api.errors import DomainError
from ppm_api.modules.assessments.access import evidence_access
from ppm_api.modules.delivery.service import fail
from ppm_api.modules.documents import tables as T
from ppm_api.modules.documents.access import document, version
from ppm_api.modules.documents.service import view
from ppm_api.modules.identity.service import Principal, now
from ppm_api.modules.integrations import tables as J


async def library(
    p: Principal, q: str, project_id: UUID | None, limit: int, offset: int, deleted: bool
) -> dict:
    if deleted and p.role != "Admin":
        fail(403, "Deleted-source retention requires Admin")
    filters: list[Any] = [
        T.documents.c.deleted_at.is_not(None) if deleted else T.documents.c.deleted_at.is_(None)
    ]
    if q:
        filters.append(T.documents.c.title.icontains(q, autoescape=True))
    if project_id:
        filters.append(T.documents.c.project_id == project_id)
    query = sa.select(T.documents).where(*filters)
    total = await p.conn.scalar(sa.select(sa.func.count()).select_from(query.subquery()))
    rows = (
        await p.conn.execute(
            query.order_by(T.documents.c.created_at.desc(), T.documents.c.id)
            .offset(offset)
            .limit(limit)
        )
    ).mappings()
    return dict(items=[await view(p, dict(r)) for r in rows], total=total, as_of=now())


async def search(p: Principal, q: str, project_id: UUID | None, limit: int) -> dict:
    latest = (
        sa.select(sa.func.max(T.versions.c.number))
        .where(T.versions.c.document_id == T.documents.c.id)
        .correlate(T.documents)
        .scalar_subquery()
    )
    vector = sa.func.to_tsvector(sa.literal_column("'simple'"), T.chunks.c.text)
    terms = sa.func.plainto_tsquery(sa.literal_column("'simple'"), q)
    query = (
        sa.select(
            T.chunks,
            T.documents.c.title,
            T.documents.c.id.label("document_id"),
            T.versions.c.number.label("version_number"),
            T.versions.c.sha256,
            sa.func.ts_rank_cd(vector, terms).label("score"),
        )
        .join(T.versions, T.versions.c.id == T.chunks.c.version_id)
        .join(T.documents, T.documents.c.id == T.versions.c.document_id)
        .where(
            T.documents.c.deleted_at.is_(None),
            T.versions.c.status == "ready",
            T.versions.c.number == latest,
            vector.op("@@")(terms),
        )
    )
    if project_id:
        query = query.where(T.documents.c.project_id == project_id)
    rows = (
        await p.conn.execute(query.order_by(sa.desc("score"), T.chunks.c.id).limit(limit))
    ).mappings()
    return {"items": [dict(r) for r in rows]}


async def detail(id_: UUID, p: Principal) -> dict:
    return await view(p, await document(p, id_))


async def preview(id_: UUID, p: Principal, offset: int, limit: int) -> list[dict]:
    v, _ = await version(p, id_)
    if v["status"] != "ready":
        fail(409, "Source is not ready; quarantined or failed content cannot be previewed")
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(T.chunks)
                .where(T.chunks.c.version_id == id_)
                .order_by(T.chunks.c.ordinal)
                .offset(offset)
                .limit(limit)
            )
        ).mappings()
    ]


async def citation(id_: UUID, p: Principal) -> dict:
    c = (await p.conn.execute(sa.select(T.chunks).where(T.chunks.c.id == id_))).mappings().first()
    if not c:
        fail(404, "Citation unavailable")
    v, d = await version(p, c["version_id"])
    latest = await p.conn.scalar(
        sa.select(sa.func.max(T.versions.c.number)).where(T.versions.c.document_id == d["id"])
    )
    if v["status"] != "ready" or v["number"] != latest:
        fail(409, "Citation is stale; retrieve the current source version")
    return dict(c)


async def job_status(id_: UUID, p: Principal) -> dict:
    await version(p, id_)
    row = (
        (
            await p.conn.execute(
                sa.select(J.jobs)
                .where(J.jobs.c.document_version_id == id_)
                .order_by(J.jobs.c.created_at.desc(), J.jobs.c.id)
                .limit(1)
            )
        )
        .mappings()
        .first()
    )
    if not row:
        fail(404, "Processing diagnostics require the uploader or Admin")
    stages = list(
        (
            await p.conn.execute(
                sa.select(J.events.c.stage)
                .where(J.events.c.job_id == row["id"])
                .order_by(J.events.c.sequence)
            )
        ).scalars()
    )
    return dict(row) | {"stages": stages}


async def evidence_references(id_: UUID, p: Principal) -> list[dict]:
    from ppm_api.modules.assessments.tables import assessments, evidence_attachments

    await version(p, id_)
    result: list[dict] = []
    query = (
        sa.select(evidence_attachments.c.id.label("attachment_id"), assessments)
        .select_from(
            T.links.join(
                evidence_attachments, T.links.c.attachment_id == evidence_attachments.c.id
            ).join(assessments, assessments.c.id == evidence_attachments.c.assessment_id)
        )
        .where(T.links.c.version_id == id_)
        .order_by(evidence_attachments.c.id)
    )
    after: UUID | None = None
    while len(result) < 100:
        page = query.limit(100)
        if after is not None:
            page = page.where(evidence_attachments.c.id > after)
        rows = (await p.conn.execute(page)).mappings().all()
        if not rows:
            break
        for row in rows:
            after = row["attachment_id"]
            try:
                evidence_access(p, row)
            except DomainError:
                continue
            result.append(
                dict(
                    attachment_id=row["attachment_id"],
                    assessment_id=row["id"],
                    assessment_name=row["name"],
                )
            )
            if len(result) == 100:
                break
        if len(rows) < 100:
            break
    return result
