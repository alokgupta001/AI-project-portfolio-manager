"""Fenced document-source processing on the existing durable-job dispatcher."""

import asyncio
import hashlib
from datetime import timedelta
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa

from ppm_api.modules.documents import tables as T
from ppm_api.modules.documents.access import version
from ppm_api.modules.documents.parser import (
    PARSER_VERSION,
    IntakeError,
    isolated_extract,
    scan,
    validate,
)
from ppm_api.modules.identity.service import Principal, context, now
from ppm_api.modules.identity.tables import memberships, sessions, users
from ppm_api.modules.integrations import tables as J
from ppm_api.modules.integrations.jobs import stage
from ppm_api.storage import LocalObjectStore


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
