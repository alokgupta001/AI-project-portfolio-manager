"""Document lifecycle, governance, evidence links and controlled retention."""

import re
from datetime import timedelta
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import Request
from starlette.concurrency import run_in_threadpool

from ppm_api.modules.assessments.access import evidence_access, oid
from ppm_api.modules.assessments.access import get as assessment_get
from ppm_api.modules.delivery.service import fail, lock
from ppm_api.modules.documents import tables as T
from ppm_api.modules.documents.access import document, version, writable
from ppm_api.modules.documents.mutations import revision
from ppm_api.modules.documents.schemas import EvidenceLink, Governance, OrphanPurge
from ppm_api.modules.documents.service import view
from ppm_api.modules.identity.service import Principal, now, record
from ppm_api.modules.identity.tables import memberships, users
from ppm_api.modules.integrations import tables as J


async def orphan_keys(p: Principal, request: Request) -> list[str]:
    if p.role != "Admin":
        fail(403, "Orphan retention requires Admin")
    # Retention must include hidden archived projects, not just the readable library.
    # This narrow function rechecks live Admin membership and returns keys/holds only.
    references = list(
        (
            await p.conn.execute(sa.text("SELECT * FROM public.ppm_source_retention_refs()"))
        ).mappings()
    )
    referenced = {row["object_key"] for row in references if row["object_key"]}
    held = {str(row["document_id"]) for row in references if row["legal_hold"]}
    store = request.app.state.storage
    tenant = str(oid(p))
    cutoff = (now() - timedelta(days=30)).timestamp()

    def candidates() -> list[str]:
        folder = store._path(tenant + "/documents")
        result = []
        for index, file in enumerate(folder.glob("*/*")):
            if index >= 10000:
                break
            key = file.relative_to(store.root).as_posix()
            if (
                file.is_symlink()
                or file.parent.is_symlink()
                or not file.is_file()
                or not re.fullmatch(tenant + r"/documents/[a-f0-9-]{36}/[a-f0-9-]{36}", key)
            ):
                continue
            if (
                key not in referenced
                and file.parent.name not in held
                and file.stat().st_mtime < cutoff
            ):
                result.append(key)
            if len(result) == 100:
                break
        return result

    return await run_in_threadpool(candidates)


async def orphan_preview(request: Request, p: Principal) -> dict:
    return {"keys": await orphan_keys(p, request)}


async def orphan_purge(body: OrphanPurge, request: Request, p: Principal) -> dict:
    await lock(p, request)
    candidates = set(await orphan_keys(p, request))
    if not set(body.keys) <= candidates:
        fail(409, "Orphan eligibility changed; preview cleanup again")
    for key in set(body.keys):
        await run_in_threadpool(request.app.state.storage.delete, key)
    await record(p.conn, request, p.user["id"], oid(p), "document.orphans_purged")
    return {"status": "purged"}


async def cancel(id_: UUID, request: Request, p: Principal) -> dict:
    await lock(p, request)
    v, d = await version(p, id_)
    await writable(p, d)
    revision(request, d)
    await p.conn.execute(
        J.jobs.update()
        .where(
            J.jobs.c.document_version_id == id_,
            J.jobs.c.status.in_(["queued", "running", "retry_wait"]),
        )
        .values(status="cancelled", cancel_requested=True)
    )
    if v["status"] in {"queued", "processing"}:
        await p.conn.execute(
            T.versions.update().where(T.versions.c.id == id_).values(status="cancelled")
        )
    await record(p.conn, request, p.user["id"], oid(p), "document.processing_cancelled", id_)
    return {"status": "cancelled"}


async def governance(id_: UUID, body: Governance, request: Request, p: Principal) -> dict:
    await lock(p, request)
    if p.role != "Admin":
        fail(403, "Policy and retention administration requires Admin")
    d = await document(p, id_, True)
    revision(request, d)
    if body.policy:
        v, _ = await version(p, body.policy.version_id, bool(d["deleted_at"]))
        if d["category"] != "policy" or v["document_id"] != id_ or v["status"] != "ready":
            fail(422, "Policy must reference a ready version of this policy document")
        if not await p.conn.scalar(
            sa.select(memberships.c.user_id)
            .join(users, users.c.id == memberships.c.user_id)
            .where(
                memberships.c.organization_id == oid(p),
                memberships.c.user_id == body.policy.owner_id,
                memberships.c.active,
                users.c.active,
                users.c.verified,
            )
        ):
            fail(422, "Policy owner must be an active organization member")
    values = body.model_dump(mode="python") | {
        "policy": body.policy.model_dump(mode="json") if body.policy else None,
        "revision": d["revision"] + 1,
    }
    await p.conn.execute(T.documents.update().where(T.documents.c.id == id_).values(**values))
    await record(p.conn, request, p.user["id"], oid(p), "document.governance_changed", id_)
    return await view(p, d | values)


async def delete(id_: UUID, request: Request, p: Principal) -> dict:
    await lock(p, request)
    d = await document(p, id_)
    await writable(p, d)
    revision(request, d)
    await p.conn.execute(
        T.documents.update()
        .where(T.documents.c.id == id_)
        .values(deleted_at=now(), revision=d["revision"] + 1)
    )
    # Objects remain retained; every read and signed capability revalidates the tombstone.
    await record(p.conn, request, p.user["id"], oid(p), "document.deleted", id_)
    return {"status": "deleted"}


async def purge(id_: UUID, request: Request, p: Principal) -> dict:
    await lock(p, request)
    if p.role != "Admin":
        fail(403, "Purge requires Admin")
    d = await document(p, id_, True)
    revision(request, d)
    if not d["deleted_at"] or d["legal_hold"] or d["retain_until"] > now():
        fail(409, "Purge requires a deleted source, expired retention and no legal hold")
    rows = list(
        (
            await p.conn.execute(sa.select(T.versions).where(T.versions.c.document_id == id_))
        ).mappings()
    )
    # Physical deletion is repeatable. Keep a metadata tombstone even on a storage failure.
    for v in rows:
        await run_in_threadpool(request.app.state.storage.delete, v["object_key"])
    await p.conn.execute(sa.text("SELECT public.ppm_purge_document(:id)"), {"id": id_})
    await record(p.conn, request, p.user["id"], oid(p), "document.purged", id_)
    return {"status": "purged"}


async def link(id_: UUID, body: EvidenceLink, request: Request, p: Principal) -> dict:
    from ppm_api.modules.assessments.tables import evidence_attachments

    await lock(p, request)
    v, d = await version(p, id_)
    await writable(p, d)
    revision(request, d)
    attachment = await assessment_get(p, evidence_attachments, body.attachment_id)
    from ppm_api.modules.assessments.tables import assessments

    a = await assessment_get(p, assessments, attachment["assessment_id"])
    evidence_access(p, a)
    if not attachment["released"] or v["status"] != "ready" or attachment["sha256"] != v["sha256"]:
        fail(
            409,
            "Only identical released attachment bytes can be linked; "
            "assessment scores remain immutable",
        )
    from sqlalchemy.dialects.postgresql import insert

    await p.conn.execute(
        insert(T.links)
        .values(
            id=uuid4(), organization_id=oid(p), version_id=id_, attachment_id=body.attachment_id
        )
        .on_conflict_do_nothing()
    )
    await record(p.conn, request, p.user["id"], oid(p), "document.assessment_linked", id_)
    return {"status": "linked"}
