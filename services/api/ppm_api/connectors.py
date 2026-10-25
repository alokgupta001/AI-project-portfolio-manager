"""Organization-approved connector authority and version-checked source review."""

from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Any, Literal, cast
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from ppm_api import delivery
from ppm_api.identity import Auth, Principal, context, now
from ppm_api.ingestion import ConnectorConfig, ImportInput, fingerprint
from ppm_api.job_tables import integrations, sources
from ppm_api.ml_tables import conflicts, principals

router = APIRouter(prefix="/api/v1/integrations", tags=["Connector authority and conflicts"])


class AuthorityInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    active: bool = True
    interval_minutes: int = Field(default=0, ge=0, le=10080)
    secret_ref: str = Field(default="", max_length=80, pattern=r"^(PPM_CONNECTOR_[A-Z0-9_]+)?$")
    webhook_secret_ref: str = Field(
        default="", max_length=80, pattern=r"^(PPM_CONNECTOR_[A-Z0-9_]+)?$"
    )


class AuthorityView(BaseModel):
    id: UUID
    integration_id: UUID
    active: bool
    generation: int
    revision: int
    interval_minutes: int
    next_due: datetime
    updated_at: datetime


class ConflictView(BaseModel):
    id: UUID
    source_id: UUID
    project_id: UUID
    revision: int
    status: str
    candidate: dict
    local: dict
    source_updated_at: datetime | None
    source_observed_at: datetime
    fingerprint: str


class Resolution(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: Literal["keep_local", "accept_source"]
    local_revision: int
    source_fingerprint: str


@router.get("/{id_}/authority", response_model=AuthorityView | None)
async def authority(id_: UUID, p: Auth) -> dict | None:
    from ppm_api.jobs import get_integration

    await get_integration(p, id_)
    row = (
        (await p.conn.execute(sa.select(principals).where(principals.c.integration_id == id_)))
        .mappings()
        .first()
    )
    return dict(row) if row else None


@router.put("/{id_}/authority", response_model=AuthorityView)
async def approve(id_: UUID, body: AuthorityInput, request: Request, p: Auth) -> dict:
    """Each rotation fences queued work; secrets themselves never travel through this API."""
    from ppm_api.jobs import admin_write, get_integration, secret_scope

    await admin_write(p, request)
    integration = await get_integration(p, id_)
    old = await authority(id_, p)
    if request.headers.get("if-match") != str(old["revision"] if old else 0):
        delivery.fail(412, "Reload connector authority before approval or rotation")
    config = ConnectorConfig(
        **(
            integration["config"]
            | {"secret_ref": body.secret_ref, "webhook_secret_ref": body.webhook_secret_ref}
        )
    )
    secret_scope(config, p.session["organization_id"])
    if body.interval_minutes and config.mode != "live":
        delivery.fail(422, "Scheduled polling requires a live connector; fixtures use manual sync")
    row = dict(
        id=old["id"] if old else uuid4(),
        organization_id=p.session["organization_id"],
        integration_id=id_,
        active=body.active,
        generation=old["generation"] + 1 if old else 1,
        revision=old["revision"] + 1 if old else 1,
        interval_minutes=body.interval_minutes,
        next_due=now() + timedelta(minutes=max(body.interval_minutes, 1)),
        approved_by=p.user["id"],
        updated_at=now(),
    )
    if old:
        await p.conn.execute(principals.update().where(principals.c.id == old["id"]).values(**row))
    else:
        await p.conn.execute(principals.insert().values(**row))
    await p.conn.execute(
        integrations.update()
        .where(integrations.c.id == id_)
        .values(
            config=config.model_dump(mode="json"),
            revision=integration["revision"] + 1,
            updated_at=now(),
        )
    )
    await delivery.audit_change(p, request, "connector_authority", row, old)
    return row


async def connector_principal(
    conn: Any, oid: UUID, uid: UUID, integration_id: UUID
) -> Principal | None:
    """Attribution is retained; effective authority is the narrow connector grant."""
    await context(conn, uid, oid, "Connector")  # type: ignore[arg-type]
    await conn.execute(
        sa.text("SELECT set_config('ppm.connector_id',:id,true)"),  # type: ignore[attr-defined]
        {"id": str(integration_id)},
    )
    ref = (
        (
            await conn.execute(
                sa.text(  # type: ignore[attr-defined]
                    "SELECT * FROM public.ppm_connector_reference(:id)"
                ),
                {"id": integration_id},
            )
        )
        .mappings()
        .first()
    )
    if not ref:
        return None
    return Principal(
        conn,
        {"id": ref["actor_id"]},  # type: ignore[arg-type]
        {"id": ref["session_id"], "organization_id": oid},
        "Connector",
        integration_id,
    )


async def recheck(p: Principal) -> None:
    """Serialize revocation against each transactional source effect."""
    await p.conn.execute(
        sa.text("SELECT pg_advisory_xact_lock(hashtextextended(:org,2))"),
        {"org": str(p.session["organization_id"])},
    )
    if not await p.conn.scalar(
        sa.text("SELECT count(*) FROM public.ppm_connector_reference(:id)"), {"id": p.connector_id}
    ):
        delivery.fail(403, "Connector authority revoked")


def logical_key(config: ConnectorConfig, external: str) -> str:
    """Connection IDs and creator sessions do not define external record identity."""
    return fingerprint(
        [
            config.provider,
            config.mode,
            config.resource.lower(),
            config.jira_project,
            config.board_id if config.entity == "sprints" else None,
            config.entity,
            config.source_namespace if config.provider == "csv" else None,
            external,
        ]
    )


async def record_conflict(
    p: Principal,
    prior: dict,
    job: dict,
    payload: dict,
    stamp: datetime | None,
    observed: datetime,
    digest: str,
) -> None:
    """Replace a pending candidate only with the newest observed source version."""
    current = await delivery.get(p, prior["target_kind"], prior["target_id"])
    old = (
        (await p.conn.execute(sa.select(conflicts).where(conflicts.c.source_id == prior["id"])))
        .mappings()
        .first()
    )
    if old and old["status"] == "pending":
        if stamp and old["source_updated_at"] and stamp < old["source_updated_at"]:
            return
        if not stamp and observed < old["source_observed_at"]:
            return
        if (
            digest == old["fingerprint"]
            and stamp == old["source_updated_at"]
            and current["revision"] == old["local"]["revision"]
        ):
            return
    row = dict(
        id=old["id"] if old else uuid4(),
        organization_id=prior["organization_id"],
        source_id=prior["id"],
        project_id=prior["project_id"],
        status="pending",
        revision=old["revision"] + 1 if old else 1,
        candidate=payload,
        local=delivery.encode(dict(current)),
        source_updated_at=stamp,
        source_observed_at=observed,
        fingerprint=digest,
        job_id=job["id"],
    )
    if old:
        await p.conn.execute(conflicts.update().where(conflicts.c.id == old["id"]).values(**row))
    else:
        await p.conn.execute(conflicts.insert().values(**row))


@router.get("/{id_}/conflicts", response_model=list[ConflictView])
async def review(id_: UUID, p: Auth) -> list[dict]:
    from ppm_api.jobs import get_integration

    integration = await get_integration(p, id_)
    result = [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(conflicts)
                .where(conflicts.c.project_id == integration["project_id"])
                .order_by(conflicts.c.id)
                .limit(100)
            )
        ).mappings()
    ]
    for row in result:
        source = (
            (await p.conn.execute(sa.select(sources).where(sources.c.id == row["source_id"])))
            .mappings()
            .one()
        )
        current = await delivery.get(p, source["target_kind"], source["target_id"])
        row["local"] = delivery.encode(dict(current))
    return result


@router.post("/{id_}/conflicts/{conflict_id}/resolve", response_model=ConflictView)
async def resolve(
    id_: UUID, conflict_id: UUID, body: Resolution, request: Request, p: Auth
) -> dict:
    from ppm_api.jobs import admin_write, get_integration

    await admin_write(p, request)
    integration = await get_integration(p, id_)
    row = (
        (
            await p.conn.execute(
                sa.select(conflicts)
                .where(
                    conflicts.c.id == conflict_id,
                    conflicts.c.project_id == integration["project_id"],
                )
                .with_for_update()
            )
        )
        .mappings()
        .first()
    )
    if not row:
        delivery.fail(404, "Conflict unavailable")
    if (
        request.headers.get("if-match") != str(row["revision"])
        or row["status"] != "pending"
        or row["fingerprint"] != body.source_fingerprint
    ):
        delivery.fail(412, "Source candidate changed; reload conflict")
    source = (
        (await p.conn.execute(sa.select(sources).where(sources.c.id == row["source_id"])))
        .mappings()
        .one()
    )
    current = await delivery.get(p, source["target_kind"], source["target_id"])
    if body.local_revision != current["revision"]:
        delivery.fail(
            412, "Local record changed; inspect the latest project record before resolving"
        )
    if body.decision == "accept_source":
        payload = delivery.adapter.validate_python(row["candidate"])
        current = await delivery.write(
            p,
            request,
            payload.kind,
            payload,
            source["target_id"],
            current["revision"],
            "Reviewed source conflict",
            source_history_complete=False,
        )
    await p.conn.execute(
        sources.update()
        .where(sources.c.id == source["id"])
        .values(
            fingerprint=row["fingerprint"],
            source_updated_at=row["source_updated_at"],
            source_observed_at=row["source_observed_at"],
            job_id=row["job_id"],
            target_revision=current["revision"],
        )
    )
    after = dict(row) | {"status": body.decision, "revision": row["revision"] + 1}
    await p.conn.execute(
        conflicts.update()
        .where(conflicts.c.id == conflict_id)
        .values(status=after["status"], revision=after["revision"])
    )
    await delivery.audit_change(p, request, "source_conflicts", after, dict(row))
    return after


async def schedule_connectors(engine: Any) -> None:
    """Existing beat dispatch polls approved live connections; no extra service is needed."""
    from ppm_api.jobs import enqueue, get_integration

    async with engine.begin() as conn:  # type: ignore[attr-defined]
        due = list(
            (await conn.execute(sa.text("SELECT * FROM public.ppm_due_connectors()"))).mappings()
        )
    for ref in due:
        async with engine.begin() as conn:  # type: ignore[attr-defined]
            p = await connector_principal(
                conn, ref["organization_id"], ref["actor_id"], ref["integration_id"]
            )
            if not p:
                continue
            await recheck(p)
            authority_row = (
                (
                    await conn.execute(
                        sa.select(principals)
                        .where(principals.c.integration_id == p.connector_id)
                        .with_for_update()
                    )
                )
                .mappings()
                .one()
            )
            if authority_row["next_due"] > now():
                continue
            integration = await get_integration(p, ref["integration_id"])
            request = cast(Request, SimpleNamespace(state=SimpleNamespace(request_id=str(uuid4()))))
            await enqueue(
                p,
                request,
                integration,
                ImportInput(),
                f"schedule:{p.connector_id}:{authority_row['next_due'].isoformat()}",
            )
            await conn.execute(
                principals.update()
                .where(principals.c.id == authority_row["id"])
                .values(next_due=now() + timedelta(minutes=authority_row["interval_minutes"]))
            )
