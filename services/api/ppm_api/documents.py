"""Versioned source library, live scoped keyword retrieval, and controlled retention."""

import asyncio
import base64
import binascii
import hashlib
import re
from datetime import timedelta
from typing import Any
from uuid import UUID, uuid4

import jwt
import sqlalchemy as sa
from fastapi import APIRouter, Query, Request, Response
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import run_in_threadpool

from ppm_api import document_tables as T
from ppm_api import job_tables as J
from ppm_api.assessment import evidence_access, oid
from ppm_api.assessment import get as assessment_get
from ppm_api.delivery import DomainError, can_edit, fail, lock
from ppm_api.delivery import get as delivery_get
from ppm_api.document_parser import (
    MAX_BYTES,
    PARSER_VERSION,
    IntakeError,
    isolated_extract,
    scan,
    validate,
)
from ppm_api.document_schemas import (
    Accepted,
    ChunkView,
    DocumentPage,
    DocumentView,
    DownloadTicket,
    EvidenceLink,
    EvidenceReference,
    Governance,
    JobStatus,
    OrphanPage,
    OrphanPurge,
    Result,
    Retrieval,
    Upload,
)
from ppm_api.identity import Auth, Principal, context, limited, now, record
from ppm_api.identity_tables import memberships, sessions, users
from ppm_api.jobs import stage
from ppm_api.storage import LocalObjectStore

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


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


@router.get("/retention/orphans", response_model=OrphanPage)
async def orphan_preview(request: Request, p: Auth) -> dict:
    return {"keys": await orphan_keys(p, request)}


@router.post("/retention/orphans/purge", response_model=Result)
async def orphan_purge(body: OrphanPurge, request: Request, p: Auth) -> dict:
    await lock(p, request)
    candidates = set(await orphan_keys(p, request))
    if not set(body.keys) <= candidates:
        fail(409, "Orphan eligibility changed; preview cleanup again")
    for key in set(body.keys):
        await run_in_threadpool(request.app.state.storage.delete, key)
    await record(p.conn, request, p.user["id"], oid(p), "document.orphans_purged")
    return {"status": "purged"}


async def document(p: Principal, id_: UUID, deleted: bool = False) -> dict:
    row = (
        (
            await p.conn.execute(
                sa.select(T.documents).where(
                    T.documents.c.id == id_, T.documents.c.organization_id == oid(p)
                )
            )
        )
        .mappings()
        .first()
    )
    if not row or (row["deleted_at"] and not deleted):
        fail(404, "Source unavailable")
    if row["project_id"]:
        await delivery_get(p, "projects", row["project_id"], True)
    return dict(row)


async def version(p: Principal, id_: UUID, deleted: bool = False) -> tuple[dict, dict]:
    row = (
        (await p.conn.execute(sa.select(T.versions).where(T.versions.c.id == id_)))
        .mappings()
        .first()
    )
    if not row:
        fail(404, "Source unavailable")
    return dict(row), await document(p, row["document_id"], deleted)


async def writable(p: Principal, d: dict) -> None:
    if p.role == "Viewer" or (
        p.role != "Admin" and (not d["project_id"] or not await can_edit(p, d["project_id"]))
    ):
        fail(
            403, "Document changes require project edit scope; organization policies require Admin"
        )


def revision(request: Request, d: dict) -> None:
    value = request.headers.get("if-match")
    if value is None:
        fail(428, "Reload the document before editing")
    if value != str(d["revision"]):
        fail(412, "Document changed; reload before editing")


async def view(p: Principal, d: dict) -> dict:
    versions = [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(T.versions)
                .where(T.versions.c.document_id == d["id"])
                .order_by(T.versions.c.number.desc())
                .limit(100)
            )
        ).mappings()
    ]
    policy = d["policy"]
    label = None
    if policy:
        today = now().date().isoformat()
        label = policy["state"]
        if label == "current" and policy["effective_date"] > today:
            label = "not yet effective"
        elif label == "current" and policy["review_date"] < today:
            label = "review overdue"
    manage = p.role == "Admin" or (
        p.role == "Project Manager" and bool(d["project_id"]) and await can_edit(p, d["project_id"])
    )
    return d | {"versions": versions, "policy_label": label, "can_manage": manage}


@router.get("", response_model=DocumentPage)
async def library(
    p: Auth,
    q: str = Query(default="", max_length=160),
    project_id: UUID | None = None,
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0, le=100000),
    deleted: bool = False,
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


@router.get("/search", response_model=Retrieval)
async def search(
    p: Auth,
    q: str = Query(min_length=1, max_length=160),
    project_id: UUID | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> dict:
    # RLS filters sources before ranking. Only the latest version is an active index.
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


@router.get("/{id_}", response_model=DocumentView)
async def detail(id_: UUID, p: Auth) -> dict:
    return await view(p, await document(p, id_))


async def enqueue(p: Principal, request: Request, v: dict, key: str, fingerprint: str) -> UUID:
    rejected = v["status"] == "quarantined"
    row = dict(
        id=uuid4(),
        organization_id=oid(p),
        integration_id=None,
        document_version_id=v["id"],
        actor_id=p.user["id"],
        session_id=p.session["id"],
        key=key,
        request_hash=fingerprint,
        config={"kind": "document-v1"},
        input={},
        status="failed" if rejected else "queued",
        attempt=0,
        position=0,
        accepted=0,
        errors=[{"code": v["diagnostic"]}] if rejected else [],
        cancel_requested=False,
        lease_token=None,
        heartbeat_at=None,
        lease_until=None,
        available_at=now(),
        created_at=now(),
        updated_at=now(),
        sequence=0,
    )
    await p.conn.execute(J.jobs.insert().values(**row))
    event = uuid4()
    await p.conn.execute(
        J.outbox.insert().values(
            id=event,
            organization_id=oid(p),
            job_id=row["id"],
            dispatched_at=now() if rejected else None,
            envelope=dict(
                event_id=str(event),
                event_type="document.quarantined" if rejected else "document.processing_requested",
                schema_version=1,
                organization_id=str(oid(p)),
                aggregate_type="job",
                aggregate_id=str(row["id"]),
                aggregate_version=1,
                occurred_at=now().isoformat(),
                actor_id=str(p.user["id"]),
                correlation_id=request.state.request_id,
                causation_id=None,
                payload={"stage": "quarantined" if rejected else "queued"},
            ),
        )
    )
    await stage(p.conn, row, "quarantined" if rejected else "queued")
    await record(p.conn, request, p.user["id"], oid(p), "document.processing_requested", v["id"])
    return row["id"]


def request_identity(request: Request, body: Any) -> tuple[str, str]:
    try:
        key = str(UUID(request.headers.get("idempotency-key", "")))
    except ValueError:
        fail(428, "A UUID Idempotency-Key is required")
    canonical = str(request.url.path) + str(jsonable_encoder(body))
    return key, hashlib.sha256(canonical.encode()).hexdigest()


async def replay(p: Principal, key: str, fingerprint: str) -> dict | None:
    row = (
        (
            await p.conn.execute(
                sa.select(J.jobs).where(
                    J.jobs.c.organization_id == oid(p),
                    J.jobs.c.actor_id == p.user["id"],
                    J.jobs.c.key == key,
                )
            )
        )
        .mappings()
        .first()
    )
    if not row:
        return None
    if row["request_hash"] != fingerprint or row["document_version_id"] is None:
        fail(409, "Idempotency key already used for different input")
    v, d = await version(p, row["document_version_id"])
    await writable(p, d)
    return dict(document=await view(p, d), version_id=v["id"], job_id=row["id"], duplicate=True)


@router.post("", response_model=Accepted, status_code=202)
async def upload(body: Upload, request: Request, p: Auth) -> dict:
    await lock(p, request)
    if p.role == "Viewer":
        fail(403, "Viewer cannot upload sources")
    key, fingerprint = request_identity(request, body.model_dump(mode="json"))
    prior = await replay(p, key, fingerprint)
    if prior:
        return prior
    await limited(request, "document-upload", str(oid(p)) + str(p.user["id"]), 10)
    if body.document_id:
        d = await document(p, body.document_id)
        await writable(p, d)
        revision(request, d)
        if (body.project_id, body.category, body.title) != (
            d["project_id"],
            d["category"],
            d["title"],
        ):
            fail(409, "New versions must preserve document scope, category and title")
    else:
        if not body.project_id and body.category != "policy":
            fail(422, "Project evidence requires a project")
        if body.project_id:
            await delivery_get(p, "projects", body.project_id, True)
        d = dict(
            id=uuid4(),
            organization_id=oid(p),
            project_id=body.project_id,
            title=body.title.strip(),
            category=body.category,
            revision=1,
            created_at=now(),
            deleted_at=None,
            legal_hold=False,
            retain_until=now() + timedelta(days=30),
            policy=None,
        )
        if not d["title"]:
            fail(422, "Document title is required")
        await writable(p, d)
        await p.conn.execute(T.documents.insert().values(**d))
    try:
        data = base64.b64decode(body.content_base64, validate=True)
    except (ValueError, binascii.Error):
        fail(422, "Invalid base64 source")
    if not 0 < len(data) <= MAX_BYTES:
        fail(413, "Source must be 1 byte to 8 MiB")
    digest = hashlib.sha256(data).hexdigest()
    old = (
        (
            await p.conn.execute(
                sa.select(T.versions).where(
                    T.versions.c.document_id == d["id"], T.versions.c.sha256 == digest
                )
            )
        )
        .mappings()
        .first()
    )
    if old:
        return dict(document=await view(p, d), version_id=old["id"], job_id=None, duplicate=True)
    count = int(
        await p.conn.scalar(
            sa.select(sa.func.count())
            .select_from(T.versions)
            .where(T.versions.c.document_id == d["id"])
        )
        or 0
    )
    if count >= 100:
        fail(409, "Document version limit reached")
    id_ = uuid4()
    object_key = f"{oid(p)}/documents/{d['id']}/{id_}"
    await run_in_threadpool(request.app.state.storage.put, object_key, data)
    v = dict(
        id=id_,
        organization_id=oid(p),
        document_id=d["id"],
        number=count + 1,
        filename=body.filename,
        size=len(data),
        sha256=digest,
        object_key=object_key,
        uploaded_by=p.user["id"],
        created_at=now(),
        status="queued",
        diagnostic=None,
        scanner=None,
        parser_version=PARSER_VERSION,
    )
    try:
        await run_in_threadpool(validate, data, body.filename)
    except IntakeError as exc:
        v.update(status="quarantined", diagnostic=str(exc))
    await p.conn.execute(T.versions.insert().values(**v))
    if body.document_id:
        d["revision"] += 1
        await p.conn.execute(
            T.documents.update().where(T.documents.c.id == d["id"]).values(revision=d["revision"])
        )
    job_id = await enqueue(p, request, v, key, fingerprint)
    return dict(document=await view(p, d), version_id=id_, job_id=job_id)


@router.get("/versions/{id_}/preview", response_model=list[ChunkView])
async def preview(
    id_: UUID,
    p: Auth,
    offset: int = Query(default=0, ge=0, le=5000),
    limit: int = Query(default=25, ge=1, le=100),
) -> list[dict]:
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


@router.get("/citations/{id_}", response_model=ChunkView)
async def citation(id_: UUID, p: Auth) -> dict:
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


@router.post("/versions/{id_}/download-ticket", response_model=DownloadTicket)
async def ticket(id_: UUID, request: Request, p: Auth) -> dict:
    await lock(p, request)
    v, _ = await version(p, id_)
    if v["status"] != "ready":
        fail(409, "Only released sources can be downloaded")
    expires = now() + timedelta(seconds=60)
    token = jwt.encode(
        dict(
            iss="ppm-documents",
            aud="download",
            exp=expires,
            sub=str(p.user["id"]),
            sid=str(p.session["id"]),
            org=str(oid(p)),
            version=str(id_),
            sha256=v["sha256"],
        ),
        request.app.state.settings.jwt_secret.get_secret_value(),
        algorithm="HS256",
    )
    return dict(token=token, expires_at=expires)


@router.get("/versions/{id_}/download")
async def download(
    id_: UUID, request: Request, p: Auth, token: str = Query(max_length=2000)
) -> Response:
    v, _ = await version(p, id_)
    try:
        claims = jwt.decode(
            token,
            request.app.state.settings.jwt_secret.get_secret_value(),
            algorithms=["HS256"],
            issuer="ppm-documents",
            audience="download",
            options={"require": ["exp", "sub", "sid", "org", "version", "sha256"]},
        )
        expected = dict(
            sub=str(p.user["id"]),
            sid=str(p.session["id"]),
            org=str(oid(p)),
            version=str(id_),
            sha256=v["sha256"],
        )
        if v["status"] != "ready" or any(claims[k] != value for k, value in expected.items()):
            raise ValueError
    except (jwt.InvalidTokenError, ValueError, KeyError):
        fail(403, "Download authorization expired or changed")
    data = await run_in_threadpool(request.app.state.storage.get, v["object_key"])
    if hashlib.sha256(data).hexdigest() != v["sha256"]:
        fail(409, "Source integrity check failed")
    return Response(
        data,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{v["filename"]}"',
            "Content-Security-Policy": "sandbox",
        },
    )


@router.get("/versions/{id_}/job", response_model=JobStatus)
async def job_status(id_: UUID, p: Auth) -> dict:
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


@router.post("/versions/{id_}/reprocess", response_model=Accepted, status_code=202)
async def reprocess(id_: UUID, request: Request, p: Auth) -> dict:
    await lock(p, request)
    v, d = await version(p, id_)
    await writable(p, d)
    key, fingerprint = request_identity(request, {})
    old = await replay(p, key, fingerprint)
    if old:
        return old
    revision(request, d)
    if v["status"] in {"queued", "processing", "purged"}:
        fail(409, "Source is already processing or unavailable")
    await p.conn.execute(T.chunks.delete().where(T.chunks.c.version_id == id_))
    await p.conn.execute(
        T.versions.update()
        .where(T.versions.c.id == id_)
        .values(status="queued", diagnostic=None, scanner=None)
    )
    d["revision"] += 1
    await p.conn.execute(
        T.documents.update().where(T.documents.c.id == d["id"]).values(revision=d["revision"])
    )
    job_id = await enqueue(
        p, request, v | {"status": "queued", "diagnostic": None}, key, fingerprint
    )
    return dict(document=await view(p, d), version_id=id_, job_id=job_id)


@router.post("/versions/{id_}/cancel", response_model=Result)
async def cancel(id_: UUID, request: Request, p: Auth) -> dict:
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


@router.patch("/{id_}/governance", response_model=DocumentView)
async def governance(id_: UUID, body: Governance, request: Request, p: Auth) -> dict:
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


@router.delete("/{id_}", response_model=Result)
async def delete(id_: UUID, request: Request, p: Auth) -> dict:
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


@router.post("/{id_}/purge", response_model=Result)
async def purge(id_: UUID, request: Request, p: Auth) -> dict:
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


@router.post("/versions/{id_}/assessment-link", response_model=Result)
async def link(id_: UUID, body: EvidenceLink, request: Request, p: Auth) -> dict:
    from ppm_api.assessment_tables import evidence_attachments

    await lock(p, request)
    v, d = await version(p, id_)
    await writable(p, d)
    revision(request, d)
    attachment = await assessment_get(p, evidence_attachments, body.attachment_id)
    from ppm_api.assessment_tables import assessments

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


@router.get("/versions/{id_}/assessment-links", response_model=list[EvidenceReference])
async def evidence_references(id_: UUID, p: Auth) -> list[dict]:
    from ppm_api.assessment_tables import assessments, evidence_attachments

    await version(p, id_)
    result = []
    rows = (
        await p.conn.execute(
            sa.select(evidence_attachments.c.id.label("attachment_id"), assessments)
            .select_from(
                T.links.join(
                    evidence_attachments, T.links.c.attachment_id == evidence_attachments.c.id
                ).join(assessments, assessments.c.id == evidence_attachments.c.assessment_id)
            )
            .where(T.links.c.version_id == id_)
            .order_by(evidence_attachments.c.id)
            .limit(100)
        )
    ).mappings()
    for row in rows:
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
    return result


async def document_worker(engine: Any, id_: UUID, tenant: UUID, actor: UUID, settings: Any) -> bool:
    """Shared job/outbox/dispatcher with a bounded parser outside database transactions."""
    token = uuid4()

    async def principal(conn: Any) -> tuple[Principal | None, dict | None, bool]:
        ref = (
            (
                await conn.execute(
                    sa.text("SELECT * FROM public.ppm_document_job(:id,:org,:actor)"),
                    {"id": id_, "org": tenant, "actor": actor},
                )
            )
            .mappings()
            .first()
        )
        if not ref:
            return None, None, False
        if not ref["authorized"]:
            return None, None, True
        await context(conn, actor, tenant)
        role = await conn.scalar(
            sa.select(memberships.c.role).where(
                memberships.c.organization_id == tenant,
                memberships.c.user_id == actor,
                memberships.c.active,
            )
        )
        await context(conn, actor, tenant, role)
        user = (await conn.execute(sa.select(users).where(users.c.id == actor))).mappings().one()
        session = (
            (await conn.execute(sa.select(sessions).where(sessions.c.id == ref["session_id"])))
            .mappings()
            .one()
        )
        row = (
            (await conn.execute(sa.select(J.jobs).where(J.jobs.c.id == id_).with_for_update()))
            .mappings()
            .first()
        )
        return Principal(conn, user, session, role), dict(row) if row else None, True

    async with engine.begin() as conn:
        p, job, handled = await principal(conn)
        if not p or not job or job["status"] in {"succeeded", "failed", "cancelled"}:
            return handled
        if job["status"] == "running" and job["lease_until"] and job["lease_until"] > now():
            return True
        v, _ = await version(p, job["document_version_id"])
        if job["cancel_requested"] or job["attempt"] >= 3:
            await conn.execute(J.jobs.update().where(J.jobs.c.id == id_).values(status="cancelled"))
            await conn.execute(
                T.versions.update().where(T.versions.c.id == v["id"]).values(status="cancelled")
            )
            return True
        await conn.execute(
            J.jobs.update()
            .where(J.jobs.c.id == id_)
            .values(
                status="running",
                attempt=job["attempt"] + 1,
                lease_token=token,
                lease_until=now() + timedelta(seconds=120),
            )
        )
        await conn.execute(
            T.versions.update().where(T.versions.c.id == v["id"]).values(status="processing")
        )
        await conn.execute(
            J.outbox.update().where(J.outbox.c.job_id == id_).values(dispatched_at=now())
        )
        await stage(conn, job, "scanning_source")
    diagnostic = None
    scanner = None
    output: list[dict] = []
    try:
        store = LocalObjectStore(settings.storage_root)
        data = await asyncio.to_thread(store.get, v["object_key"])
        if hashlib.sha256(data).hexdigest() != v["sha256"]:
            raise IntakeError("INTEGRITY_FAILED")
        await asyncio.to_thread(validate, data, v["filename"])
        scanner = await asyncio.to_thread(
            scan, data, settings.document_scanner_host, settings.document_scanner_port
        )
        output = await asyncio.to_thread(isolated_extract, data, v["filename"])
    except IntakeError as exc:
        diagnostic = str(exc)
    except Exception:
        diagnostic = "PROCESSING_FAILED"
    async with engine.begin() as conn:
        p, job, _ = await principal(conn)
        if not p or not job or job["lease_token"] != token or job["status"] != "running":
            return True
        # Permission, tombstone, session, lease and cancellation are rechecked before effects.
        await conn.execute(T.chunks.delete().where(T.chunks.c.version_id == v["id"]))
        if not diagnostic:
            for c in output:
                await conn.execute(
                    T.chunks.insert().values(
                        id=uuid4(), organization_id=tenant, version_id=v["id"], **c
                    )
                )
        await conn.execute(
            T.versions.update()
            .where(T.versions.c.id == v["id"])
            .values(
                status="quarantined" if diagnostic else "ready",
                diagnostic=diagnostic,
                scanner=scanner,
                parser_version=PARSER_VERSION,
            )
        )
        await conn.execute(
            J.jobs.update()
            .where(J.jobs.c.id == id_)
            .values(
                status="failed" if diagnostic else "succeeded",
                lease_until=None,
                accepted=len(output) if not diagnostic else 0,
                errors=[{"code": diagnostic}] if diagnostic else [],
            )
        )
        await stage(conn, job, "quarantined" if diagnostic else "source_ready")
    return True
