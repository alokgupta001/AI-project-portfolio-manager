"""Document response loading, processing-job enqueueing and authorized replay."""

from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import Request

from ppm_api.modules.assessments.access import oid
from ppm_api.modules.delivery.service import can_edit, fail
from ppm_api.modules.documents import tables as T
from ppm_api.modules.documents.access import version, writable
from ppm_api.modules.identity.service import Principal, now, record
from ppm_api.modules.integrations import tables as J
from ppm_api.modules.integrations.jobs import stage


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
