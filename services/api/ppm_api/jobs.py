"""Durable ingestion, transactional outbox and permission-rechecked progress."""

import asyncio
import hashlib
import hmac
import json
import os
import random
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import aclosing
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ppm_api import delivery
from ppm_api.identity import Auth, Principal, context, now, principal
from ppm_api.identity_tables import memberships, sessions, users
from ppm_api.ingestion import (
    ConnectorConfig,
    ImportInput,
    Retryable,
    fingerprint,
    normalize,
    project_rows,
    remote_page,
    rows,
)
from ppm_api.job_tables import events, integrations, jobs, outbox, sources

router = APIRouter(prefix="/api/v1/integrations", tags=["Integrations and jobs"])
TERMINAL = {"succeeded", "partially_succeeded", "failed", "cancelled"}


class IntegrationView(BaseModel):
    id: UUID
    config: ConnectorConfig
    revision: int
    enabled: bool
    cursor: str | None
    updated_at: datetime


class StageView(BaseModel):
    id: UUID
    sequence: int
    stage: str
    occurred_at: datetime


class JobView(BaseModel):
    id: UUID
    integration_id: UUID
    status: str
    attempt: int
    position: int
    accepted: int
    errors: list[dict[str, Any]]
    cancel_requested: bool
    heartbeat_at: datetime | None
    created_at: datetime
    updated_at: datetime
    sequence: int


class Preview(BaseModel):
    valid: int
    errors: list[dict[str, Any]]
    examples: list[dict[str, Any]]


class EnabledInput(BaseModel):
    enabled: bool


class SourceView(BaseModel):
    external_id: str
    source_updated_at: datetime | None
    source_observed_at: datetime
    target_id: UUID
    target_kind: str
    target_revision: int
    job_id: UUID


@router.get("/{id_}/sources", response_model=list[SourceView])
async def source_evidence(id_: UUID, p: Auth) -> list[dict]:
    await get_integration(p, id_)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(sources)
                .where(sources.c.integration_id == id_)
                .order_by(sources.c.external_id)
                .limit(100)
            )
        ).mappings()
    ]


async def get_integration(p: Principal, id_: UUID) -> dict:
    row = (
        (await p.conn.execute(sa.select(integrations).where(integrations.c.id == id_)))
        .mappings()
        .first()
    )
    if not row:
        delivery.fail(404, "Integration not available")
    await delivery.get(p, "projects", row["project_id"], True)
    return dict(row)


async def get_job(p: Principal, id_: UUID, locked: bool = False) -> dict:
    query = sa.select(jobs).where(jobs.c.id == id_)
    row = (await p.conn.execute(query.with_for_update() if locked else query)).mappings().first()
    if not row:
        delivery.fail(404, "Job not available")
    if row["ai_run_id"]:
        from ppm_api.ai import access

        await access(p, row["ai_run_id"])
    else:
        await get_integration(p, row["integration_id"])
    return dict(row)


async def admin_write(p: Principal, request: Request) -> None:
    await delivery.lock(p, request)
    if p.role != "Admin":
        delivery.fail(403, "Integration management requires Admin")


def secret_scope(config: ConnectorConfig, organization_id: UUID) -> None:
    prefix = f"PPM_CONNECTOR_{organization_id.hex.upper()}_{config.provider.upper()}_"
    for reference in (config.secret_ref, config.webhook_secret_ref):
        if reference and not reference.startswith(prefix):
            delivery.fail(
                422, "Secret references must use the current organization and provider prefix"
            )


async def stage(conn: Any, row: dict, code: str) -> None:
    seq = row["sequence"] + 1
    await conn.execute(
        events.insert().values(
            id=uuid4(),
            organization_id=row["organization_id"],
            job_id=row["id"],
            sequence=seq,
            stage=code,
            occurred_at=now(),
        )
    )
    await conn.execute(
        jobs.update().where(jobs.c.id == row["id"]).values(sequence=seq, updated_at=now())
    )
    row["sequence"] = seq
    if code in {"succeeded", "partially_succeeded", "failed", "cancelled"}:
        from ppm_api.pilot import notify

        await notify(
            conn, row["organization_id"], row["actor_id"], "jobs", row["id"], f"{row['id']}:{code}"
        )


@router.get("", response_model=list[IntegrationView])
async def list_integrations(p: Auth) -> list[dict]:
    return [
        dict(r)
        for r in (
            await p.conn.execute(sa.select(integrations).order_by(integrations.c.id).limit(100))
        ).mappings()
    ]


@router.post("", response_model=IntegrationView, status_code=201)
async def create_integration(body: ConnectorConfig, request: Request, p: Auth) -> dict:
    await admin_write(p, request)
    secret_scope(body, p.session["organization_id"])
    await delivery.get(p, "projects", body.project_id, True)
    if body.team_id:
        await delivery.get(p, "teams", body.team_id, True)
    key = request.headers.get("idempotency-key", "")
    if not 1 <= len(key) <= 100:
        delivery.fail(428, "Idempotency key is required")
    # Stable ID for a retried create; conflicts compare the complete canonical configuration.
    from uuid import uuid5

    id_ = uuid5(p.session["organization_id"], str(p.user["id"]) + ":integration:" + key)
    old = (
        (await p.conn.execute(sa.select(integrations).where(integrations.c.id == id_)))
        .mappings()
        .first()
    )
    config = body.model_dump(mode="json")
    if old:
        if old["config"] != config:
            delivery.fail(409, "Idempotency key has different input")
        return dict(old)
    row = dict(
        id=id_,
        organization_id=p.session["organization_id"],
        project_id=body.project_id,
        config=config,
        actor_id=p.user["id"],
        session_id=p.session["id"],
        revision=1,
        enabled=True,
        cursor=None,
        updated_at=now(),
    )
    await p.conn.execute(integrations.insert().values(**row))
    await delivery.audit_change(p, request, "integrations", row, None)
    return row


@router.patch("/{id_}", response_model=IntegrationView)
async def enable_integration(id_: UUID, body: EnabledInput, request: Request, p: Auth) -> dict:
    await admin_write(p, request)
    row = await get_integration(p, id_)
    if request.headers.get("if-match") != str(row["revision"]):
        delivery.fail(
            428 if "if-match" not in request.headers else 412, "Reload the current revision"
        )
    after = row | dict(
        enabled=body.enabled,
        revision=row["revision"] + 1,
        updated_at=now(),
        actor_id=p.user["id"],
        session_id=p.session["id"],
    )
    await p.conn.execute(
        integrations.update()
        .where(integrations.c.id == id_)
        .values(
            enabled=after["enabled"],
            revision=after["revision"],
            updated_at=after["updated_at"],
            actor_id=after["actor_id"],
            session_id=after["session_id"],
        )
    )
    await delivery.audit_change(p, request, "integrations", after, row)
    return after


@router.post("/{id_}/preview", response_model=Preview)
async def preview(id_: UUID, body: ImportInput, request: Request, p: Auth) -> dict:
    await admin_write(p, request)
    config = ConnectorConfig(**(await get_integration(p, id_))["config"])
    if config.mode == "live":
        delivery.fail(409, "Live data is fetched only by durable sync jobs")
    try:
        batch = project_rows(config, rows(config, body))
    except ValueError:
        delivery.fail(422, "Invalid or oversized source batch")
    valid = 0
    errors: list[dict[str, Any]] = []
    examples: list[dict[str, Any]] = []
    for index, item in enumerate(batch):
        try:
            external, stamp, payload = normalize(config, item)
            valid += 1
            if len(examples) < 5:
                examples.append(
                    dict(
                        external_id=external,
                        source_updated_at=stamp.isoformat() if stamp else None,
                        data=payload.model_dump(mode="json"),
                    )
                )
        except (ValueError, TypeError):
            errors.append(dict(row=index + 1, code="INVALID_SOURCE_ROW"))
    return dict(valid=valid, errors=errors, examples=examples)


async def enqueue(
    p: Principal,
    request: Request,
    integration: dict,
    body: ImportInput,
    key: str,
    source_hash: str | None = None,
) -> dict:
    if not integration["enabled"]:
        delivery.fail(409, "Integration is disabled")
    if not 1 <= len(key) <= 160:
        delivery.fail(428, "Idempotency key is required")
    config = ConnectorConfig(**integration["config"])
    secret_scope(config, p.session["organization_id"])
    try:
        batch = project_rows(config, rows(config, body))
    except ValueError:
        delivery.fail(422, "Invalid or oversized source batch")
    digest = fingerprint(dict(integration_id=str(integration["id"]), body=body.model_dump()))
    digest = fingerprint([digest, source_hash]) if source_hash else digest
    existing = (
        (
            await p.conn.execute(
                sa.select(jobs).where(
                    jobs.c.organization_id == p.session["organization_id"],
                    jobs.c.actor_id == p.user["id"],
                    jobs.c.key == key,
                )
            )
        )
        .mappings()
        .first()
    )
    if existing:
        if existing["request_hash"] != digest:
            delivery.fail(409, "Idempotency key has different input")
        return dict(existing)
    row = dict(
        id=uuid4(),
        organization_id=p.session["organization_id"],
        integration_id=integration["id"],
        actor_id=p.user["id"],
        session_id=p.session["id"],
        key=key,
        request_hash=digest,
        config=integration["config"],
        input=dict(
            rows=batch,
            fetched=config.mode != "live",
            page=1,
            token=None,
            next_token=None,
            cursor=integration["cursor"],
            watermark=integration["cursor"],
            observed_at=now().isoformat(),
        ),
        status="queued",
        attempt=0,
        position=0,
        accepted=0,
        errors=[],
        cancel_requested=False,
        lease_token=None,
        heartbeat_at=None,
        lease_until=None,
        available_at=now(),
        created_at=now(),
        updated_at=now(),
        sequence=0,
    )
    await p.conn.execute(jobs.insert().values(**row))
    event_id = uuid4()
    envelope = dict(
        event_id=str(event_id),
        event_type="ingestion.requested",
        schema_version=1,
        organization_id=str(row["organization_id"]),
        aggregate_type="job",
        aggregate_id=str(row["id"]),
        aggregate_version=1,
        occurred_at=now().isoformat(),
        actor_id=str(row["actor_id"]),
        correlation_id=request.state.request_id,
        causation_id=None,
        payload={"stage": "queued"},
    )
    await p.conn.execute(
        outbox.insert().values(
            id=event_id,
            organization_id=row["organization_id"],
            job_id=row["id"],
            envelope=envelope,
            dispatched_at=None,
        )
    )
    await stage(p.conn, row, "queued")
    await delivery.audit_change(
        p, request, "jobs", {k: v for k, v in row.items() if k not in {"input", "config"}}, None
    )
    return row


@router.post("/{id_}/sync", response_model=JobView, status_code=202)
async def sync(id_: UUID, body: ImportInput, request: Request, p: Auth) -> dict:
    await admin_write(p, request)
    return await enqueue(
        p, request, await get_integration(p, id_), body, request.headers.get("idempotency-key", "")
    )


@router.post("/{id_}/webhook", response_model=JobView, status_code=202)
async def webhook(id_: UUID, body: ImportInput, request: Request, p: Auth) -> dict:
    """Authenticated signed gateway intake; never an unauthenticated provider endpoint."""
    await admin_write(p, request)
    integration = await get_integration(p, id_)
    config = ConnectorConfig(**integration["config"])
    secret = os.environ.get(config.webhook_secret_ref, "")
    raw = await request.body()
    signature = request.headers.get("x-hub-signature-256", "")
    delivery_id = request.headers.get("x-github-delivery", "")
    if not secret or not hmac.compare_digest(
        "sha256=" + hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest(), signature
    ):
        delivery.fail(403, "Webhook verification failed")
    if not 1 <= len(delivery_id) <= 100:
        delivery.fail(422, "Webhook delivery identity is required")
    # Identity remains retained with the job; a changed body with a replayed ID conflicts.
    return await enqueue(p, request, integration, body, "webhook:" + str(id_) + ":" + delivery_id)


@router.get("/activity/jobs", response_model=list[JobView])
async def activity(p: Auth) -> list[dict]:
    result = []
    for r in (
        await p.conn.execute(
            sa.select(jobs).order_by(jobs.c.created_at.desc(), jobs.c.id).limit(100)
        )
    ).mappings():
        try:
            await get_integration(p, r["integration_id"])
            result.append(dict(r))
        except delivery.DomainError:
            pass
    return result


@router.get("/activity/jobs/{id_}", response_model=JobView)
async def job_detail(id_: UUID, p: Auth) -> dict:
    return await get_job(p, id_)


@router.get("/activity/jobs/{id_}/stages", response_model=list[StageView])
async def stage_history(id_: UUID, p: Auth) -> list[dict]:
    await get_job(p, id_)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(events)
                .where(events.c.job_id == id_, events.c.occurred_at >= now() - timedelta(hours=24))
                .order_by(events.c.sequence.desc())
                .limit(100)
            )
        ).mappings()
    ]


@router.post("/activity/jobs/{id_}/cancel", response_model=JobView)
async def cancel(id_: UUID, request: Request, p: Auth) -> dict:
    await admin_write(p, request)
    row = await get_job(p, id_, True)
    if row["status"] not in TERMINAL and not row["cancel_requested"]:
        await p.conn.execute(jobs.update().where(jobs.c.id == id_).values(cancel_requested=True))
        row["cancel_requested"] = True
        await stage(p.conn, row, "cancellation_requested")
        await delivery.audit_change(p, request, "jobs", row | {"input": {}, "config": {}}, None)
    return row


async def event_batch(request: Request, id_: UUID, after: int) -> tuple[dict, list[dict]]:
    # A fresh transaction per poll; no connection stays pinned for an SSE subscription.
    async with aclosing(
        cast(AsyncGenerator[Principal, None], principal(request))
    ) as authentication:
        async for p in authentication:
            row = await get_job(p, id_)
            values = (
                await p.conn.execute(
                    sa.select(events)
                    .where(
                        events.c.job_id == id_,
                        events.c.sequence > after,
                        events.c.occurred_at >= now() - timedelta(hours=24),
                    )
                    .order_by(events.c.sequence)
                    .limit(100)
                )
            ).mappings()
            return row, [dict(v) for v in values]
    delivery.fail(401, "Session is no longer active")


@router.get("/activity/jobs/{id_}/events", response_class=StreamingResponse)
async def stream(id_: UUID, request: Request, p: Auth) -> StreamingResponse:
    await get_job(p, id_)
    try:
        after = int(request.headers.get("last-event-id", request.query_params.get("after", "0")))
        if after < 0:
            raise ValueError
    except ValueError:
        delivery.fail(422, "Invalid progress cursor")

    async def generate() -> AsyncIterator[str]:
        nonlocal after
        heartbeat = 0
        while not await request.is_disconnected():
            try:
                row, batch = await event_batch(request, id_, after)
            except delivery.DomainError:
                yield "event: access_revoked\ndata: {}\n\n"
                return
            except Exception:
                yield "event: access_revoked\ndata: {}\n\n"
                return
            if (
                after > row["sequence"]
                or (batch and batch[0]["sequence"] > after + 1)
                or (not batch and after < row["sequence"])
            ):
                yield 'event: resync_required\ndata: {"reason":"cursor_not_retained"}\n\n'
                return
            for event in batch:
                after = event["sequence"]
                yield (
                    f"id: {after}\nevent: stage\ndata: "
                    + json.dumps(StageView(**event).model_dump(mode="json"))
                    + "\n\n"
                )
            if row["status"] in TERMINAL and after >= row["sequence"]:
                return
            if heartbeat % 15 == 0:
                yield ": heartbeat\n\n"
            heartbeat += 1
            await asyncio.sleep(1)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-store"},
    )


async def worker_principal(conn: Any, oid: UUID, uid: UUID, sid: UUID) -> Principal | None:
    await context(conn, uid, oid, "")
    role = await conn.scalar(
        sa.select(memberships.c.role).where(
            memberships.c.organization_id == oid, memberships.c.user_id == uid, memberships.c.active
        )
    )
    session = (
        (
            await conn.execute(
                sa.select(sessions).where(sessions.c.id == sid, sessions.c.user_id == uid)
            )
        )
        .mappings()
        .first()
    )
    user = (await conn.execute(sa.select(users).where(users.c.id == uid))).mappings().first()
    if (
        role != "Admin"
        or not user
        or not user["verified"]
        or not user["active"]
        or not session
        or session["revoked"]
        or session["expires_at"] <= now()
        or session["organization_id"] != oid
    ):
        return None
    await context(conn, uid, oid, "Admin")
    return Principal(conn, user, session, "Admin")


async def worker_transaction(
    conn: Any, oid: UUID, uid: UUID, id_: UUID
) -> tuple[Principal | None, dict | None]:
    if await conn.scalar(sa.text("SELECT public.ppm_cancel_unauthorized_job(:id)"), {"id": id_}):
        return None, None
    # Serialize with membership/grant/domain edits, then recheck current authority.
    await conn.execute(
        sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org,2))"), {"org": str(oid)}
    )
    # Tenant context alone permits only identifier-scoped owner reads. No role assumed yet.
    await context(conn, uid, oid, "")
    sid = await conn.scalar(sa.text("SELECT public.ppm_job_session(:id)"), {"id": id_})
    if not sid:
        return None, None
    p = await worker_principal(conn, oid, uid, sid)
    if not p:
        return None, None
    row = (
        (
            await conn.execute(
                sa.select(jobs).where(jobs.c.id == id_, jobs.c.actor_id == uid).with_for_update()
            )
        )
        .mappings()
        .first()
    )
    if not row:
        return None, None
    return p, dict(row)


async def apply_source(p: Principal, row: dict, item: dict) -> None:
    config = ConnectorConfig(**row["config"])
    external, stamp, payload = normalize(config, item)
    digest = fingerprint(payload.model_dump(mode="json"))
    prior = (
        (
            await p.conn.execute(
                sa.select(sources).where(
                    sources.c.integration_id == row["integration_id"],
                    sources.c.external_id == external,
                )
            )
        )
        .mappings()
        .first()
    )
    observed_at = datetime.fromisoformat(row["input"]["observed_at"])
    if prior and (
        (stamp and prior["source_updated_at"] and stamp < prior["source_updated_at"])
        or (not stamp and observed_at < prior["source_observed_at"])
    ):
        return
    if prior and stamp and stamp == prior["source_updated_at"]:
        if digest != prior["fingerprint"]:
            raise ValueError("Source version collision")
        return
    if prior and digest == prior["fingerprint"]:
        await p.conn.execute(
            sources.update()
            .where(sources.c.id == prior["id"])
            .values(source_updated_at=stamp, source_observed_at=observed_at, job_id=row["id"])
        )
        return
    # Never overwrite local edits. Existing domain lifecycle and revision gates are reused.
    request = SimpleNamespace(
        headers={"x-organization-id": str(row["organization_id"])},
        state=SimpleNamespace(request_id=str(row["id"])),
    )
    target_id = prior["target_id"] if prior else None
    version = prior["target_revision"] if prior else None
    # Imported sprint lifecycle uses existing transitions; frozen points remain unknown.
    if payload.kind == "sprints":
        current = (await delivery.get(p, "sprints", target_id))["status"] if target_id else None
        states = ["planned", "active", "closed"]
        if current == "closed" and payload.status != "closed":
            raise ValueError("Closed sprint source cannot be reopened")
        path = (["planned"] if current is None else []) + states[
            states.index(current or "planned") + 1 : states.index(payload.status) + 1
        ]
        if not path:
            path = [payload.status]
        for state in path:
            target = await delivery.write(
                p,
                cast(Request, request),
                payload.kind,
                payload.model_copy(update={"status": state}),
                target_id,
                version,
                "Imported source lifecycle; historical point coverage unknown",
                source_history_complete=False,
            )
            target_id, version = UUID(str(target["id"])), target["revision"]
    else:
        target = await delivery.write(
            p,
            cast(Request, request),
            payload.kind,
            payload,
            target_id,
            version,
            "Imported source update",
        )
    values = dict(
        source_updated_at=stamp,
        source_observed_at=observed_at,
        fingerprint=digest,
        target_id=UUID(str(target["id"])),
        project_id=config.project_id,
        work_item_id=UUID(str(target["id"])) if payload.kind == "work_items" else None,
        sprint_id=UUID(str(target["id"])) if payload.kind == "sprints" else None,
        target_kind=payload.kind,
        target_revision=target["revision"],
        job_id=row["id"],
    )
    if prior:
        await p.conn.execute(sources.update().where(sources.c.id == prior["id"]).values(**values))
    else:
        await p.conn.execute(
            sources.insert().values(
                id=uuid4(),
                organization_id=row["organization_id"],
                integration_id=row["integration_id"],
                external_id=external,
                **values,
            )
        )


async def run_job(
    engine: Any, id_: UUID, oid: UUID, uid: UUID, stop_after: int | None = None
) -> None:
    """Each source effect + provenance + checkpoint commits atomically; leases fence old tasks."""
    from ppm_api.ai import ai_worker
    from ppm_api.config import load_settings
    from ppm_api.documents import document_worker

    if await ai_worker(engine, id_, oid, uid, load_settings()):
        return

    if await document_worker(engine, id_, oid, uid, load_settings()):
        return
    token = uuid4()
    async with engine.begin() as conn:
        p, row = await worker_transaction(conn, oid, uid, id_)
        if not row or not p or row["status"] in TERMINAL or row["available_at"] > now():
            return
        if row["status"] == "running" and row["lease_until"] > now():
            return
        if row["attempt"] >= 5:
            await conn.execute(
                jobs.update()
                .where(jobs.c.id == id_)
                .values(
                    status="failed",
                    lease_until=None,
                    errors=row["errors"] + [{"code": "ATTEMPTS_EXHAUSTED"}],
                )
            )
            await stage(conn, row, "dead_letter")
            return
        await conn.execute(
            jobs.update()
            .where(jobs.c.id == id_)
            .values(
                status="running",
                attempt=row["attempt"] + 1,
                lease_token=token,
                lease_until=now() + timedelta(seconds=45),
                heartbeat_at=now(),
            )
        )
        await conn.execute(
            outbox.update().where(outbox.c.job_id == id_).values(dispatched_at=now())
        )
        await stage(conn, row, "validating_sources")
    processed = 0
    while True:
        async with engine.begin() as conn:
            p, row = await worker_transaction(conn, oid, uid, id_)
            if not p or not row or row["lease_token"] != token or row["status"] != "running":
                return
            integration = await get_integration(p, row["integration_id"])
            if row["cancel_requested"] or not integration["enabled"]:
                await conn.execute(
                    jobs.update()
                    .where(jobs.c.id == id_)
                    .values(status="cancelled", lease_until=None)
                )
                await stage(conn, row, "cancelled")
                return
            data = row["input"]
            if not data["fetched"]:
                config = ConnectorConfig(**row["config"])
                try:
                    batch, next_token = await remote_page(
                        config, data["cursor"], data["page"], data["token"]
                    )
                    if len(batch) > 100 or len(json.dumps(batch).encode()) > 2000000:
                        raise ValueError("Page limit")
                    data = data | dict(
                        rows=project_rows(config, batch),
                        fetched=True,
                        next_token=next_token,
                        observed_at=now().isoformat(),
                    )
                    await conn.execute(
                        jobs.update()
                        .where(jobs.c.id == id_)
                        .values(
                            input=data,
                            position=0,
                            heartbeat_at=now(),
                            lease_until=now() + timedelta(seconds=45),
                        )
                    )
                    continue
                except Retryable as exc:
                    delay = max(exc.delay, min(300, 2 ** row["attempt"] * 5 + random.randint(0, 5)))
                    await conn.execute(
                        jobs.update()
                        .where(jobs.c.id == id_)
                        .values(
                            status="retry_wait",
                            lease_until=None,
                            available_at=now() + timedelta(seconds=delay),
                        )
                    )
                    await stage(conn, row, "retry_wait")
                    return
                except Exception:
                    await conn.execute(
                        jobs.update()
                        .where(jobs.c.id == id_)
                        .values(
                            status="failed",
                            lease_until=None,
                            errors=row["errors"] + [{"code": "CONNECTOR_REQUEST_FAILED"}],
                        )
                    )
                    await stage(conn, row, "dead_letter")
                    return
            if row["position"] >= len(data["rows"]):
                if data["next_token"]:
                    if data["page"] >= 20:
                        await conn.execute(
                            jobs.update()
                            .where(jobs.c.id == id_)
                            .values(
                                status="failed",
                                lease_until=None,
                                errors=row["errors"] + [{"code": "PAGE_LIMIT"}],
                            )
                        )
                        await stage(conn, row, "dead_letter")
                        return
                    await conn.execute(
                        jobs.update()
                        .where(jobs.c.id == id_)
                        .values(
                            input=data
                            | dict(
                                rows=[],
                                fetched=False,
                                page=data["page"] + 1,
                                token=data["next_token"],
                                next_token=None,
                            ),
                            position=0,
                        )
                    )
                    continue
                status = "partially_succeeded" if row["errors"] else "succeeded"
                await conn.execute(
                    jobs.update().where(jobs.c.id == id_).values(status=status, lease_until=None)
                )
                # Partial jobs replay from the old watermark. Advance only for a wholly valid sync.
                if not row["errors"] and data["watermark"]:
                    current = integration["cursor"]
                    watermark = max(current, data["watermark"]) if current else data["watermark"]
                    await conn.execute(
                        integrations.update()
                        .where(integrations.c.id == integration["id"])
                        .values(cursor=watermark, updated_at=now())
                    )
                await stage(conn, row, "degraded" if row["errors"] else "completed")
                return
            item = data["rows"][row["position"]]
            accepted, errors = row["accepted"], row["errors"]
            try:
                async with conn.begin_nested():
                    await apply_source(p, row, item)
                accepted += 1
                _, stamp, _ = normalize(ConnectorConfig(**row["config"]), item)
                source_time = stamp.isoformat() if stamp else None
                data = data | dict(
                    watermark=max(data["watermark"], source_time)
                    if data["watermark"] and source_time
                    else source_time or data["watermark"]
                )
            except (ValueError, TypeError, delivery.DomainError) as exc:
                code = (
                    "LOCAL_REVISION_CONFLICT"
                    if isinstance(exc, delivery.DomainError) and exc.status_code == 412
                    else "INVALID_SOURCE_ROW"
                )
                errors = errors + [dict(page=data["page"], row=row["position"] + 1, code=code)]
            await conn.execute(
                jobs.update()
                .where(jobs.c.id == id_)
                .values(
                    position=row["position"] + 1,
                    accepted=accepted,
                    errors=errors,
                    input=data,
                    heartbeat_at=now(),
                    lease_until=now() + timedelta(seconds=45),
                )
            )
            await stage(conn, row, "source_processed")
        processed += 1
        if stop_after is not None and processed >= stop_after:
            return  # deterministic crash boundary used only by tests


@router.post("/hooks/github/{id_}", response_model=JobView, status_code=202)
async def github_hook(id_: UUID, request: Request) -> dict:
    # Signature is the sole CSRF exception; authorization still uses a live delegated session.
    raw = bytearray()
    async for chunk in request.stream():
        raw.extend(chunk)
        if len(raw) > 600000:
            delivery.fail(413, "Webhook batch is too large")
    async with request.app.state.engine.begin() as conn:
        ref = (
            (
                await conn.execute(
                    sa.text("SELECT * FROM public.ppm_webhook_reference(:id)"), {"id": id_}
                )
            )
            .mappings()
            .first()
        )
        secret = os.environ.get(ref["secret_ref"], "") if ref else ""
        signature = request.headers.get("x-hub-signature-256", "")
        expected = "sha256=" + hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
        if not secret or not hmac.compare_digest(expected, signature):
            delivery.fail(403, "Webhook verification failed")
        await conn.execute(
            sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org,2))"),
            {"org": str(ref["organization_id"])},
        )
        p = await worker_principal(conn, ref["organization_id"], ref["actor_id"], ref["session_id"])
        if not p:
            delivery.fail(403, "Webhook authority is no longer active")
        integration = await get_integration(p, id_)
        config = ConnectorConfig(**integration["config"])
        try:
            payload = json.loads(raw)
            if payload["repository"]["full_name"].lower() != config.resource.lower():
                raise ValueError
            expected_event = "pull_request" if config.entity == "pulls" else "issues"
            if request.headers.get("x-github-event") != expected_event:
                raise ValueError
            record = payload["pull_request" if config.entity == "pulls" else "issue"]
            body = ImportInput() if config.mode == "live" else ImportInput(records=[record])
        except (ValueError, KeyError, TypeError):
            delivery.fail(422, "Unsupported webhook payload")
        delivery_id = request.headers.get("x-github-delivery", "")
        if not 1 <= len(delivery_id) <= 100:
            delivery.fail(422, "Webhook delivery identity is required")
        return await enqueue(
            p,
            request,
            integration,
            body,
            "github:" + str(id_) + ":" + delivery_id,
            hashlib.sha256(raw).hexdigest(),
        )
