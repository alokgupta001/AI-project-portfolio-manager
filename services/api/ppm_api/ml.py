"""Local history → versioned dataset → durable CPU baseline → reviewable model card."""

import asyncio
from datetime import UTC, datetime, timedelta
from random import Random
from typing import Any
from uuid import UUID, uuid4, uuid5

import sqlalchemy as sa
from fastapi import APIRouter, Request

from ppm_api import delivery
from ppm_api.identity import Auth, Principal, now
from ppm_api.ingestion import fingerprint
from ppm_api.job_tables import jobs, outbox
from ppm_api.ml_pipeline import build_dataset, evaluate
from ppm_api.ml_schemas import (
    TARGETS,
    DatasetInput,
    DatasetView,
    HistoryInput,
    MLHistoryView,
    RunInput,
    RunView,
    Target,
)
from ppm_api.ml_tables import datasets, histories, runs

router = APIRouter(prefix="/api/v1/ml", tags=["Local datasets and baselines"])


def admin(p: Principal) -> None:
    """Aggregate history and experiments are limited to organization administrators."""
    if p.role != "Admin":
        delivery.fail(403, "History and baseline research requires Admin")


async def get(p: Principal, table: sa.Table, id_: UUID) -> dict:
    admin(p)
    row = (await p.conn.execute(sa.select(table).where(table.c.id == id_))).mappings().first()
    if not row:
        delivery.fail(404, "Research record unavailable")
    await delivery.get(p, "projects", row["project_id"], True)
    return dict(row)


async def active_dataset(p: Principal, id_: UUID) -> dict:
    row = await get(p, datasets, id_)
    history = await get(p, histories, row["history_id"])
    if history["withdrawn"]:
        delivery.fail(409, "Source history withdrawn; rebuild from authorized history")
    return row


async def access_run(p: Principal, id_: UUID) -> dict:
    row = await get(p, runs, id_)
    await active_dataset(p, row["dataset_id"])
    return row


def request_id(p: Principal, request: Request, operation: str) -> UUID:
    key = request.headers.get("idempotency-key", "")
    if not 1 <= len(key) <= 100:
        delivery.fail(428, "Idempotency key required")
    return uuid5(p.session["organization_id"], f"{p.user['id']}:{operation}:{key}")


def fixture(project_id: UUID, target: Target = "delay") -> dict:
    """A fixed seed creates separate demonstrator lineage, never real outcome evidence."""
    random = Random(12)
    records = []
    for index in range(90):
        observed = datetime(2025, (1, 5, 9)[index // 30], index % 28 + 1, tzinfo=UTC)
        bugs = random.randint(0, 20)
        days = random.randint(5, 18)
        outcome = observed + timedelta(days=days)
        records.append(
            dict(
                entity_id=f"fixture-{index:03}",
                entity_kind="team" if target == "sentiment" else "project",
                observed_at=observed.isoformat(),
                feature_asof=observed.isoformat(),
                features=dict(
                    velocity=random.randint(10, 50),
                    bugs=bugs,
                    scope_change=random.randint(-3, 12),
                    spend_ratio=round(random.random(), 3),
                    dependencies=random.randint(0, 10),
                    allocation_percent=None if index % 7 == 0 else random.randint(30, 100),
                ),
                outcome=dict(
                    target=target,
                    kind="synthetic",
                    evidence_ref=f"fixture:outcome-{index:03}",
                    occurred_at=outcome.isoformat(),
                    available_at=(outcome + timedelta(days=1)).isoformat(),
                    baseline_known_at=observed.isoformat(),
                    planned_finish=(observed + timedelta(days=7)).date().isoformat(),
                    actual_finish=outcome.date().isoformat(),
                    budget=10000,
                    actual_spend=9000 + bugs * 200,
                    disposition="missed_commitment" if bugs > 10 else "accepted",
                    adverse_category=int(bugs > 10),
                    adjudication="independent_outcome_review",
                    survey_mean=1.5 if bugs > 10 else 3.5,
                    respondents=8,
                    consent=True,
                ),
            )
        )
    return dict(
        history=dict(
            project_id=str(project_id),
            name=f"Synthetic {target} history",
            origin="In-repository seeded numeric fixture v1; seed 12",
            lineage="synthetic",
            license="CC0-1.0",
            authorized=True,
            label_declaration="synthetic-fixture",
            records=records,
        ),
        dataset=dict(
            target=target,
            horizon_days=30,
            train_end="2025-03-01T00:00:00Z",
            validation_end="2025-07-01T00:00:00Z",
            cutoff="2025-12-31T00:00:00Z",
        ),
    )


@router.get("/template", response_model=dict)
async def template(project_id: UUID, p: Auth, target: Target = "delay") -> dict:
    admin(p)
    await delivery.get(p, "projects", project_id, True)
    return fixture(project_id, target) | {"targets": TARGETS}


@router.get("/histories", response_model=list[MLHistoryView])
async def history_list(p: Auth) -> list[dict]:
    admin(p)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(histories).order_by(histories.c.created_at.desc()).limit(100)
            )
        ).mappings()
    ]


@router.post("/histories", response_model=MLHistoryView, status_code=201)
async def import_history(body: HistoryInput, request: Request, p: Auth) -> dict:
    from ppm_api.jobs import admin_write
    from ppm_api.ml_pipeline import label

    await admin_write(p, request)
    await delivery.get(p, "projects", body.project_id, True)
    if any(
        r.observed_at > now() or r.outcome and r.outcome.available_at > now() for r in body.records
    ):
        delivery.fail(422, "Future history cannot be imported as observed evidence")
    try:
        for r in body.records:
            if r.outcome:
                label(r)
    except ValueError as exc:
        delivery.fail(422, str(exc))
    id_ = request_id(p, request, "history")
    serialized = body.model_dump(mode="json")
    digest = fingerprint(serialized)
    old = (
        (await p.conn.execute(sa.select(histories).where(histories.c.id == id_))).mappings().first()
    )
    if old:
        if old["digest"] != digest:
            delivery.fail(409, "Idempotency key has different input")
        return dict(old)
    version = 1 + int(
        (
            await p.conn.scalar(
                sa.select(sa.func.coalesce(sa.func.max(histories.c.version), 0)).where(
                    histories.c.project_id == body.project_id, histories.c.name == body.name
                )
            )
        )
        or 0
    )
    row = dict(
        id=id_,
        organization_id=p.session["organization_id"],
        project_id=body.project_id,
        name=body.name,
        version=int(version or 1),
        digest=digest,
        withdrawn=False,
        created_at=now(),
        records=serialized.pop("records"),
        manifest=serialized
        | {
            "schema_version": 1,
            "imported_at": now().isoformat(),
            "label_verification": "synthetic"
            if body.lineage == "synthetic"
            else "organization-attested; not independently verified",
            "record_count": len(body.records),
        },
    )
    await p.conn.execute(histories.insert().values(**row))
    await delivery.audit_change(
        p, request, "ml_histories", {k: v for k, v in row.items() if k != "records"}, None
    )
    return row


@router.post("/histories/{id_}/withdraw", response_model=MLHistoryView)
async def withdraw(id_: UUID, request: Request, p: Auth) -> dict:
    from ppm_api.jobs import admin_write

    await admin_write(p, request)
    row = await get(p, histories, id_)
    if not row["withdrawn"]:
        await p.conn.execute(histories.update().where(histories.c.id == id_).values(withdrawn=True))
        await delivery.audit_change(
            p, request, "ml_history_withdrawal", {"id": id_, "withdrawn": True}, row
        )
    return row | {"withdrawn": True}


@router.get("/datasets", response_model=list[DatasetView])
async def dataset_list(p: Auth) -> list[dict]:
    admin(p)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(datasets).order_by(datasets.c.created_at.desc()).limit(100)
            )
        ).mappings()
    ]


@router.post("/datasets", response_model=DatasetView, status_code=201)
async def create_dataset(body: DatasetInput, request: Request, p: Auth) -> dict:
    from ppm_api.jobs import admin_write

    await admin_write(p, request)
    history = await get(p, histories, body.history_id)
    if history["withdrawn"]:
        delivery.fail(409, "Source history withdrawn")
    id_ = request_id(p, request, "dataset")
    metadata = {k: v for k, v in history["manifest"].items() if k in HistoryInput.model_fields}
    source = HistoryInput(**(metadata | {"records": history["records"]}))
    try:
        manifest, records = build_dataset(source, body)
    except ValueError as exc:
        delivery.fail(422, str(exc))
    manifest |= dict(
        history_id=str(body.history_id),
        history_version=history["version"],
        history_hash=history["digest"],
        spec=body.model_dump(mode="json"),
    )
    digest = fingerprint([manifest, records])
    old = (await p.conn.execute(sa.select(datasets).where(datasets.c.id == id_))).mappings().first()
    if old:
        if old["digest"] != digest:
            delivery.fail(409, "Idempotency key has different input")
        return dict(old)
    row = dict(
        id=id_,
        organization_id=p.session["organization_id"],
        project_id=history["project_id"],
        history_id=body.history_id,
        digest=digest,
        manifest=manifest,
        records=records,
        created_at=now(),
    )
    await p.conn.execute(datasets.insert().values(**row))
    await delivery.audit_change(
        p, request, "ml_datasets", {k: v for k, v in row.items() if k != "records"}, None
    )
    return row


@router.get("/datasets/{id_}", response_model=DatasetView)
async def dataset_detail(id_: UUID, p: Auth) -> dict:
    return await active_dataset(p, id_)


@router.get("/runs", response_model=list[RunView])
async def run_list(p: Auth) -> list[dict]:
    admin(p)
    # Recheck withdrawal on list as well as artifact delivery.
    query = (
        sa.select(runs)
        .join(datasets, runs.c.dataset_id == datasets.c.id)
        .join(histories, datasets.c.history_id == histories.c.id)
        .where(~histories.c.withdrawn)
    )
    return [
        dict(r)
        for r in (
            await p.conn.execute(query.order_by(runs.c.created_at.desc()).limit(100))
        ).mappings()
    ]


@router.post("/runs", response_model=RunView, status_code=202)
async def train(body: RunInput, request: Request, p: Auth) -> dict:
    from ppm_api.jobs import admin_write, stage

    await admin_write(p, request)
    dataset = await active_dataset(p, body.dataset_id)
    id_ = request_id(p, request, "baseline")
    old = (await p.conn.execute(sa.select(runs).where(runs.c.id == id_))).mappings().first()
    if old:
        if old["dataset_id"] != body.dataset_id:
            delivery.fail(409, "Idempotency key has different input")
        return dict(old)
    pending = await p.conn.scalar(
        sa.select(sa.func.count())
        .select_from(jobs)
        .where(
            jobs.c.ml_run_id.is_not(None), jobs.c.status.in_(["queued", "running", "retry_wait"])
        )
    )
    if (pending or 0) >= 3:
        delivery.fail(429, "At most three local baseline jobs may be pending")
    row = dict(
        id=id_,
        organization_id=p.session["organization_id"],
        project_id=dataset["project_id"],
        dataset_id=body.dataset_id,
        actor_id=p.user["id"],
        status="queued",
        card={},
        artifacts={},
        created_at=now(),
    )
    await p.conn.execute(runs.insert().values(**row))
    job = dict(
        id=uuid4(),
        organization_id=p.session["organization_id"],
        integration_id=None,
        ml_run_id=id_,
        actor_id=p.user["id"],
        session_id=p.session["id"],
        key=f"ml:{id_}",
        request_hash=fingerprint(str(body.dataset_id)),
        config={},
        input={},
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
    await p.conn.execute(jobs.insert().values(**job))
    await p.conn.execute(
        outbox.insert().values(
            id=uuid4(),
            organization_id=row["organization_id"],
            job_id=job["id"],
            envelope={
                "event_type": "ml.baseline.requested",
                "schema_version": 1,
                "aggregate_id": str(job["id"]),
            },
            dispatched_at=None,
        )
    )
    await stage(p.conn, job, "queued")
    await delivery.audit_change(p, request, "ml_runs", row, None)
    return row


@router.get("/runs/{id_}", response_model=RunView)
async def run_detail(id_: UUID, p: Auth) -> dict:
    return await access_run(p, id_)


@router.get("/runs/{id_}/artifacts", response_model=dict)
async def artifacts(id_: UUID, p: Auth) -> dict:
    row = await access_run(p, id_)
    return {"run_id": str(id_), "model_card": row["card"], "artifacts": row["artifacts"]}


async def ml_worker(engine: Any, id_: UUID, oid: UUID, uid: UUID) -> bool:
    """Reuse durable dispatch and app-role/session gates; interrupted work rolls back safely."""
    from ppm_api.identity import context
    from ppm_api.jobs import TERMINAL, stage, worker_principal

    async with engine.begin() as conn:
        await context(conn, uid, oid, "")
        ref = (
            (await conn.execute(sa.text("SELECT * FROM public.ppm_ml_job(:id)"), {"id": id_}))
            .mappings()
            .first()
        )
        if not ref:
            return False
        if not ref["authorized"]:
            return True
        p = await worker_principal(conn, oid, uid, ref["session_id"])
        if not p:
            return True
        job = dict(
            (await conn.execute(sa.select(jobs).where(jobs.c.id == id_).with_for_update()))
            .mappings()
            .one()
        )
        if job["status"] in TERMINAL:
            return True
        try:
            run = await get(p, runs, ref["run_id"])
            if job["cancel_requested"]:
                await conn.execute(jobs.update().where(jobs.c.id == id_).values(status="cancelled"))
                await conn.execute(
                    runs.update().where(runs.c.id == run["id"]).values(status="cancelled")
                )
                await stage(conn, job, "cancelled")
                return True
            await stage(conn, job, "training_baseline")
            dataset = await active_dataset(p, run["dataset_id"])
            card, output = await asyncio.to_thread(
                evaluate, dataset["manifest"], dataset["records"], dataset["digest"]
            )
            previous = (
                await conn.execute(
                    sa.select(runs.c.card)
                    .where(
                        runs.c.dataset_id == run["dataset_id"],
                        runs.c.id != run["id"],
                        runs.c.status == "succeeded",
                    )
                    .order_by(runs.c.created_at.desc())
                    .limit(1)
                )
            ).scalar()
            card["repeat_matches_previous"] = (
                previous.get("result_hash") == card.get("result_hash")
                if previous and card.get("result_hash")
                else None
            )
            status = "insufficient_data" if card["reasons"] else "succeeded"
            await conn.execute(
                runs.update()
                .where(runs.c.id == run["id"])
                .values(status=status, card=card, artifacts=output)
            )
            await conn.execute(
                jobs.update()
                .where(jobs.c.id == id_)
                .values(status="succeeded", accepted=len(dataset["records"]), updated_at=now())
            )
            await stage(conn, job, "insufficient_data" if card["reasons"] else "completed")
        except delivery.DomainError:
            await conn.execute(
                runs.update()
                .where(runs.c.id == ref["run_id"])
                .values(
                    status="blocked",
                    card={"eligibility": "source_unavailable", "promotion": "BLOCKED"},
                )
            )
            await conn.execute(
                jobs.update().where(jobs.c.id == id_).values(status="cancelled", updated_at=now())
            )
            await stage(conn, job, "access_revoked")
        except Exception:
            await conn.execute(
                runs.update()
                .where(runs.c.id == ref["run_id"])
                .values(
                    status="failed",
                    card={
                        "eligibility": "evaluation_failed",
                        "promotion": "BLOCKED",
                        "error": "LOCAL_BASELINE_FAILED",
                    },
                )
            )
            await conn.execute(
                jobs.update()
                .where(jobs.c.id == id_)
                .values(
                    status="failed", updated_at=now(), errors=[{"code": "LOCAL_BASELINE_FAILED"}]
                )
            )
            await stage(conn, job, "failed")
        return True
