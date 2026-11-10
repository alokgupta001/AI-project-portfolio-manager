"""Document intake, private downloads and reprocessing."""

import base64
import binascii
import hashlib
from datetime import timedelta
from uuid import UUID, uuid4

import jwt
import sqlalchemy as sa
from fastapi import Request, Response
from starlette.concurrency import run_in_threadpool

from ppm_api.modules.assessments.access import oid
from ppm_api.modules.delivery.service import fail, lock
from ppm_api.modules.delivery.service import get as delivery_get
from ppm_api.modules.documents import tables as T
from ppm_api.modules.documents.access import document, version, writable
from ppm_api.modules.documents.mutations import request_identity, revision
from ppm_api.modules.documents.parser import MAX_BYTES, PARSER_VERSION, IntakeError, validate
from ppm_api.modules.documents.schemas import Upload
from ppm_api.modules.documents.service import enqueue, replay, view
from ppm_api.modules.identity.service import Principal, limited, now


async def upload(body: Upload, request: Request, p: Principal) -> dict:
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


async def ticket(id_: UUID, request: Request, p: Principal) -> dict:
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


async def download(id_: UUID, request: Request, p: Principal, token: str) -> Response:
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


async def reprocess(id_: UUID, request: Request, p: Principal) -> dict:
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
