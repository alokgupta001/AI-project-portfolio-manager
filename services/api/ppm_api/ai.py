"""Budgeted, fenced evidence runtime. Domain agents and automatic edits are out of scope."""

import asyncio
import json
from dataclasses import dataclass
from datetime import timedelta
from decimal import ROUND_UP, Decimal
from time import perf_counter
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import APIRouter, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ppm_api import ai_provider as P
from ppm_api import ai_tables as T
from ppm_api import delivery, documents
from ppm_api import document_tables as D
from ppm_api import job_tables as J
from ppm_api.ai_retrieval import (
    SourceTool,
    authorize_tool,
    cosine,
    digest,
    evaluate,
    index_chunks,
    keyword,
    merge,
    snapshot,
    validate_snapshot,
)
from ppm_api.ai_schemas import (
    GRAPH_VERSION,
    PROMPT_VERSION,
    SCHEMA_VERSION,
    TOOL_VERSION,
    AIBudgetInput,
    AIDiagnostics,
    AIEvaluation,
    AIOperations,
    AIOutput,
    AIProviderStatus,
    AIRunInput,
    AIRunView,
)
from ppm_api.config import Settings
from ppm_api.document_retrieval import EmbeddingRequest
from ppm_api.identity import Auth, Principal, now, record
from ppm_api.jobs import TERMINAL, StageView, stage, worker_principal

router = APIRouter(prefix="/api/v1/ai", tags=["AI runtime"])
VERSIONS = dict(
    prompt_version=PROMPT_VERSION,
    schema_version=SCHEMA_VERSION,
    tool_version=TOOL_VERSION,
    graph_version=GRAPH_VERSION,
)
ZERO = Decimal("0")


def oid(p: Principal) -> UUID:
    return p.session["organization_id"]


def admin(p: Principal) -> None:
    if p.role != "Admin":
        delivery.fail(403, "AI operations require Admin")


def call_cap(settings: Settings) -> Decimal:
    if settings.ai_provider == "gemini":
        return ZERO
    # UTF-8 bytes bound tokens conservatively. Input <= 110k bytes; output <= 512 tokens.
    return (
        (
            120000 * max(settings.ai_input_usd_per_million, settings.ai_embedding_usd_per_million)
            + 512 * settings.ai_output_usd_per_million
        )
        / 1000000
    ).quantize(Decimal("0.000001"), rounding=ROUND_UP)


def provider_status(settings: Settings) -> dict:
    active = P.enabled(settings)
    return dict(
        provider=settings.ai_provider,
        enabled=active,
        reason=(
            "FREE_TIER_OPERATOR_CONFIRMED"
            if active and settings.ai_provider == "gemini"
            else "CONFIGURED_NOT_VERIFIED"
            if active
            else P.gemini_block_reason(settings)
            if settings.ai_provider == "gemini"
            else "PROVIDER_DISABLED"
        ),
        completion_model=settings.ai_completion_model or None,
        embedding_model=settings.ai_embedding_model or None,
    )


@router.get("/status", response_model=AIProviderStatus)
async def status(request: Request, p: Auth) -> dict:
    return provider_status(request.app.state.settings)


async def budget(p: Principal, create: bool = False) -> dict:
    row = (
        (
            await p.conn.execute(
                sa.select(T.budgets).where(T.budgets.c.organization_id == oid(p)).with_for_update()
            )
        )
        .mappings()
        .first()
    )
    if row:
        return dict(row)
    values = dict(
        id=uuid4(),
        organization_id=oid(p),
        limit_usd=ZERO,
        spent_usd=ZERO,
        reserved_usd=ZERO,
        concurrency=1,
        revision=1,
        failures=0,
        circuit_until=None,
    )
    if create:
        await p.conn.execute(T.budgets.insert().values(**values))
    return values


async def access(p: Principal, id_: UUID) -> tuple[dict, dict]:
    # One statement observes the run and its job at the same PostgreSQL snapshot.
    # Separate READ COMMITTED reads could pair old evidence with a new terminal job,
    # causing a polling client to stop before receiving the final diagnostic/result.
    pair = (
        await p.conn.execute(
            sa.select(T.runs, J.jobs)
            .join(J.jobs, J.jobs.c.ai_run_id == T.runs.c.id)
            .where(T.runs.c.id == id_)
        )
    ).first()
    if not pair:
        delivery.fail(404, "Run unavailable")
    row = {c.name: pair._mapping[c] for c in T.runs.c}
    job = {c.name: pair._mapping[c] for c in J.jobs.c}
    if row["snapshot"]["operation"] == "agents":
        from ppm_api.agents import get_analysis

        await get_analysis(p, id_)
    await delivery.get(p, "projects", row["project_id"], True)
    return row, job


async def view(p: Principal, run: dict, job: dict) -> dict:
    evidence = []
    limitations = list(run["limitations"])
    # No saved provider text is served. Every excerpt is resolved from current authorized bytes.
    try:
        rows = await validate_snapshot(p, run["result"])
        evidence = [
            dict(
                chunk_id=r["id"],
                version_id=r["version_id"],
                sha256=r["sha256"],
                text_sha256=digest(r["text"]),
                location=r["location"],
                quote=r["text"],
            )
            for r in rows
        ]
    except (delivery.DomainError, P.ProviderError):
        limitations.append("EVIDENCE_UNAVAILABLE: retrieve the current permitted sources")
    call_rows = list(
        (
            await p.conn.execute(
                sa.select(T.calls)
                .where(T.calls.c.run_id == run["id"])
                .order_by(T.calls.c.operation, T.calls.c.attempt)
            )
        ).mappings()
    )

    def tokens(field: str) -> int | None:
        return (
            sum(r[field] for r in call_rows)
            if call_rows and all(r[field] is not None for r in call_rows)
            else None
        )

    return dict(
        id=run["id"],
        organization_id=run["organization_id"],
        input_snapshot_id=run["id"],
        project_id=run["project_id"],
        operation=run["snapshot"]["operation"],
        status=job["status"],
        created_at=run["created_at"],
        generated_at=job["updated_at"] if job["status"] in TERMINAL else None,
        answer_status=(
            "not_requested"
            if job["status"] not in TERMINAL
            else "indexed"
            if run["snapshot"]["operation"] == "index" and job["status"] == "succeeded"
            else "unavailable"
            if not evidence
            else "source_fallback"
            if run["diagnostic"]
            else "supported"
        ),
        **{k: run["versions"][k] for k in VERSIONS},
        provider=run["versions"]["provider"],
        model=run["versions"].get("completion_model"),
        diagnostic=run["diagnostic"],
        limitations=limitations,
        evidence=evidence,
        retrieval=run["retrieval"],
        reserved_usd=ZERO if run["settled"] else run["reservation"],
        charged_usd=run["charged_usd"],
        input_tokens=tokens("input_tokens"),
        output_tokens=tokens("output_tokens"),
        latency_ms=sum(r["latency_ms"] for r in call_rows),
        sequence=job["sequence"],
        revision=job["sequence"],
    )


@router.get("/runs", response_model=list[AIRunView])
async def listing(
    p: Auth, project_id: UUID | None = None, offset: int = Query(default=0, ge=0, le=10000)
) -> list[dict]:
    query = (
        sa.select(T.runs).order_by(T.runs.c.created_at.desc(), T.runs.c.id).offset(offset).limit(25)
    )
    if project_id:
        await delivery.get(p, "projects", project_id, True)
        query = query.where(T.runs.c.project_id == project_id)
    rows = list((await p.conn.execute(query)).mappings())
    return [await view(p, *await access(p, row["id"])) for row in rows]


@router.get("/runs/{id_}", response_model=AIRunView)
async def detail(id_: UUID, p: Auth) -> dict:
    return await view(p, *await access(p, id_))


@router.get("/evaluation", response_model=AIEvaluation)
async def evaluation(p: Auth) -> dict:
    from ppm_api.ai_evaluation import run_evaluation

    admin(p)
    return run_evaluation()


@router.get("/operations", response_model=AIOperations)
async def operations(request: Request, p: Auth) -> dict:
    admin(p)
    b = await budget(p)
    return {
        k: b[k]
        for k in (
            "limit_usd",
            "spent_usd",
            "reserved_usd",
            "concurrency",
            "revision",
            "failures",
            "circuit_until",
        )
    } | dict(
        provider=provider_status(request.app.state.settings),
        deployment_limit_usd=request.app.state.settings.ai_spend_limit_usd,
        runs=await listing(p, None, 0),
    )


@router.patch("/budget", response_model=AIOperations)
async def configure(body: AIBudgetInput, request: Request, p: Auth) -> dict:
    await delivery.lock(p, request)
    admin(p)
    b = await budget(p, True)
    if request.headers.get("if-match") is None:
        delivery.fail(428, "Reload the AI budget before editing")
    if request.headers.get("if-match") != str(b["revision"]):
        delivery.fail(412, "Budget changed; reload before editing")
    if body.limit_usd > request.app.state.settings.ai_spend_limit_usd:
        delivery.fail(422, "Budget exceeds the operator-authorized deployment limit")
    if body.limit_usd < b["spent_usd"] + b["reserved_usd"]:
        delivery.fail(409, "Budget cannot be below spent and reserved usage")
    await p.conn.execute(
        T.budgets.update()
        .where(T.budgets.c.id == b["id"])
        .values(limit_usd=body.limit_usd, concurrency=body.concurrency, revision=b["revision"] + 1)
    )
    await record(p.conn, request, p.user["id"], oid(p), "ai.budget_changed", b["id"])
    return await operations(request, p)


@router.post("/runs", response_model=AIRunView, status_code=202)
async def create(body: AIRunInput, request: Request, p: Auth) -> dict:
    await delivery.lock(p, request)
    admin(p)  # PM has no explicit costly-analysis grant in the current permission model.
    await delivery.get(p, "projects", body.project_id, True)
    if (
        (body.operation == "query" and (not body.query.strip() or body.version_id))
        or (body.operation == "index" and (not body.version_id or body.query))
        or (body.operation != "agents" and (body.version_ids or body.assessment_id))
        or (body.operation == "agents" and (body.query or body.version_id))
    ):
        delivery.fail(422, "Choose a query or one ready source version to index")
    # Preserve Sprint 10 request hashes for query/index replays after additive fields.
    identity_body = (
        body.model_dump(exclude={"version_ids", "assessment_id"})
        if body.operation != "agents"
        else body
    )
    key, fingerprint = documents.request_identity(request, identity_body)
    if body.operation == "agents":
        from ppm_api.agents import private_access

        await private_access(p, body.assessment_id)
    previous = (
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
    if previous:
        if previous["request_hash"] != fingerprint or not previous["ai_run_id"]:
            delivery.fail(409, "Idempotency key has a different request")
        return await detail(previous["ai_run_id"], p)
    analysis_snapshot = None
    if body.operation == "agents":
        from ppm_api.agents import capture

        analysis_snapshot = await capture(p, body)
    refs = []
    if body.version_id:
        _, rows = await index_chunks(p, body.project_id, body.version_id)
        refs = [snapshot(row) for row in rows]
    config = request.app.state.settings
    b = await budget(p, True)
    active = await p.conn.scalar(
        sa.select(sa.func.count())
        .select_from(T.runs)
        .where(T.runs.c.organization_id == oid(p), ~T.runs.c.settled)
    )
    if active >= b["concurrency"]:
        delivery.fail(429, "AI concurrency limit reached; wait or cancel the active run")
    reservation = call_cap(config) * 4 if P.enabled(config) else ZERO
    if config.ai_provider != "gemini" and b["spent_usd"] + b["reserved_usd"] + reservation > min(
        b["limit_usd"], config.ai_spend_limit_usd
    ):
        delivery.fail(429, "AI budget exhausted; keyword search remains available")
    run_id = uuid4()
    versions = VERSIONS | dict(
        provider=config.ai_provider if P.enabled(config) else "disabled",
        completion_model=config.ai_completion_model or None,
        embedding_model=config.ai_embedding_model or None,
        call_cap_usd=str(call_cap(config)),
        prompt_sha256=digest(P.SYSTEM_PROMPT),
        schema_sha256=digest(json.dumps(AIOutput.model_json_schema(), sort_keys=True)),
        tool_sha256=digest(json.dumps(SourceTool.model_json_schema(), sort_keys=True)),
        dimensions=256,
        max_completion_tokens=512,
        input_usd_per_million=str(config.ai_input_usd_per_million),
        output_usd_per_million=str(config.ai_output_usd_per_million),
        embedding_usd_per_million=str(config.ai_embedding_usd_per_million),
        provider_policy=P.policy_snapshot(config),
    )
    run = dict(
        id=run_id,
        organization_id=oid(p),
        project_id=body.project_id,
        actor_id=p.user["id"],
        session_id=p.session["id"],
        snapshot=body.model_dump(mode="json"),
        input_sha256=fingerprint,
        versions=versions,
        evidence=refs,
        result=[],
        diagnostic=None,
        limitations=[],
        retrieval="none",
        reservation=reservation,
        charged_usd=ZERO,
        settled=False,
        deadline=now() + timedelta(seconds=90),
        created_at=now(),
    )
    await p.conn.execute(T.runs.insert().values(**run))
    if analysis_snapshot is not None:
        from ppm_api import agent_tables

        await p.conn.execute(
            agent_tables.analyses.insert().values(
                id=run_id,
                run_id=run_id,
                organization_id=oid(p),
                project_id=body.project_id,
                assessment_id=body.assessment_id,
                actor_id=p.user["id"],
                snapshot=analysis_snapshot,
                output=None,
            )
        )
    await p.conn.execute(
        T.budgets.update()
        .where(T.budgets.c.id == b["id"])
        .values(reserved_usd=b["reserved_usd"] + reservation)
    )
    job = dict(
        id=uuid4(),
        organization_id=oid(p),
        integration_id=None,
        document_version_id=None,
        ai_run_id=run_id,
        actor_id=p.user["id"],
        session_id=p.session["id"],
        key=key,
        request_hash=fingerprint,
        config={"kind": "ai-v1"},
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
    await p.conn.execute(J.jobs.insert().values(**job))
    event_id = uuid4()
    await p.conn.execute(
        J.outbox.insert().values(
            id=event_id,
            organization_id=oid(p),
            job_id=job["id"],
            dispatched_at=None,
            envelope=dict(
                event_id=str(event_id),
                event_type="ai.requested",
                schema_version=1,
                organization_id=str(oid(p)),
                aggregate_type="ai_run",
                aggregate_id=str(run_id),
                aggregate_version=1,
                occurred_at=now().isoformat(),
                actor_id=str(p.user["id"]),
                correlation_id=request.state.request_id,
                causation_id=None,
                payload={"stage": "queued"},
            ),
        )
    )
    await stage(p.conn, job, "queued")
    await record(p.conn, request, p.user["id"], oid(p), "ai.requested", run_id)
    return await view(p, run, job)


@router.post("/runs/{id_}/cancel", response_model=AIRunView)
async def cancel(id_: UUID, request: Request, p: Auth) -> dict:
    await delivery.lock(p, request)
    admin(p)
    run, job = await access(p, id_)
    if request.headers.get("if-match") is None:
        delivery.fail(428, "Reload the run before cancellation")
    if request.headers.get("if-match") != str(job["sequence"]):
        delivery.fail(412, "Run changed; reload before cancellation")
    if job["status"] not in TERMINAL:
        await p.conn.execute(
            J.jobs.update().where(J.jobs.c.id == job["id"]).values(cancel_requested=True)
        )
        await p.conn.execute(
            sa.text("SELECT * FROM public.ppm_ai_job(:id,:org,:actor)"),
            {"id": job["id"], "org": oid(p), "actor": job["actor_id"]},
        )
        await stage(p.conn, job, "cancelled")
        await record(p.conn, request, p.user["id"], oid(p), "ai.cancelled", id_)
    return await detail(id_, p)


@router.get("/runs/{id_}/events", response_class=StreamingResponse)
async def progress(id_: UUID, request: Request, p: Auth) -> StreamingResponse:
    from ppm_api.jobs import stream

    _, job = await access(p, id_)
    return await stream(job["id"], request, p)


@router.get("/runs/{id_}/stages", response_model=list[StageView])
async def stages(id_: UUID, p: Auth) -> list[dict]:
    _, job = await access(p, id_)
    return [
        dict(row)
        for row in (
            await p.conn.execute(
                sa.select(J.events)
                .where(J.events.c.job_id == job["id"])
                .order_by(J.events.c.sequence)
                .limit(100)
            )
        ).mappings()
    ]


@router.get("/runs/{id_}/diagnostics", response_model=AIDiagnostics)
async def diagnostics(id_: UUID, p: Auth) -> dict:
    admin(p)
    run, job = await access(p, id_)
    calls = list(
        (
            await p.conn.execute(
                sa.select(T.calls)
                .where(T.calls.c.run_id == id_)
                .order_by(T.calls.c.operation, T.calls.c.attempt)
            )
        ).mappings()
    )
    # No query, source text, raw provider body, API key, object key or private reasoning.
    return dict(
        run=await view(p, run, job),
        input_sha256=run["input_sha256"],
        **{k: run["versions"][k] for k in VERSIONS},
        evidence_snapshot=run["evidence"],
        calls=[
            {
                k: c[k]
                for k in (
                    "id",
                    "operation",
                    "attempt",
                    "status",
                    "code",
                    "charged_usd",
                    "input_tokens",
                    "output_tokens",
                    "latency_ms",
                )
            }
            for c in calls
        ],
    )


async def worker_context(
    conn: Any, job_id: UUID, tenant: UUID, actor: UUID
) -> tuple[Principal | None, dict | None, dict | None]:
    ref = (
        (
            await conn.execute(
                sa.text("SELECT * FROM public.ppm_ai_job(:id,:org,:actor)"),
                {"id": job_id, "org": tenant, "actor": actor},
            )
        )
        .mappings()
        .first()
    )
    if not ref:
        return None, None, None
    if not ref["authorized"]:
        return None, {}, {}
    p = await worker_principal(conn, tenant, actor, ref["session_id"])
    if not p:
        return None, {}, {}
    run, job = await access(p, ref["run_id"])
    return p, run, job


async def settle(
    p: Principal,
    run: dict,
    job: dict,
    status: str,
    code: str | None,
    result: list[dict],
    refs: list[dict],
    retrieval: str,
    limitations: list[str],
) -> None:
    if run["settled"]:
        return
    b = await budget(p)
    await p.conn.execute(
        T.budgets.update()
        .where(T.budgets.c.id == b["id"])
        .values(
            reserved_usd=b["reserved_usd"] - run["reservation"],
            spent_usd=b["spent_usd"] + run["charged_usd"],
        )
    )
    await p.conn.execute(
        T.runs.update()
        .where(T.runs.c.id == run["id"])
        .values(
            settled=True,
            diagnostic=code,
            result=result,
            evidence=refs,
            retrieval=retrieval,
            limitations=limitations,
        )
    )
    await p.conn.execute(
        J.jobs.update()
        .where(J.jobs.c.id == job["id"])
        .values(
            status=status,
            lease_until=None,
            accepted=len(result),
            errors=[{"code": code}] if code else [],
        )
    )
    await stage(p.conn, job, status)


@dataclass
class Branch:
    name: str
    rows: list[dict]
    code: str | None = None


class Runtime:
    def __init__(
        self,
        engine: Any,
        job_id: UUID,
        tenant: UUID,
        actor: UUID,
        settings: Settings,
        adapter: P.Provider,
        token: UUID,
    ):
        self.engine, self.job_id, self.tenant, self.actor = engine, job_id, tenant, actor
        self.settings, self.adapter, self.token = settings, adapter, token

    async def state(self, conn: Any) -> tuple[Principal, dict, dict]:
        p, run, job = await worker_context(conn, self.job_id, self.tenant, self.actor)
        if (
            not p
            or not run
            or not job
            or run["settled"]
            or job["status"] != "running"
            or job["lease_token"] != self.token
        ):
            raise P.ProviderError("RUN_CANCELLED")
        if job["lease_until"] <= now() or run["deadline"] <= now():
            raise P.ProviderError("DEADLINE_EXCEEDED")
        return p, run, job

    async def call(
        self,
        operation: str,
        texts: list[str],
        query: str = "",
        rows: list[dict] | None = None,
        output_schema: type[BaseModel] = AIOutput,
    ) -> P.ProviderResult:
        p: Principal | None
        run: dict | None
        job: dict | None
        for attempt in range(1, 3):
            call_id = uuid4()
            async with self.engine.begin() as conn:
                p, run, job = await self.state(conn)
                # Frozen model/rate settings: changed configuration cannot replay old paid work.
                if (
                    run["versions"]["provider"]
                    != (self.settings.ai_provider if P.enabled(self.settings) else "disabled")
                    or run["versions"].get("provider_policy", {})
                    != P.policy_snapshot(self.settings)
                    or run["versions"].get("completion_model")
                    != (self.settings.ai_completion_model or None)
                    or run["versions"].get("embedding_model")
                    != (self.settings.ai_embedding_model or None)
                    or run["versions"]["call_cap_usd"] != str(call_cap(self.settings))
                    or run["versions"]["prompt_sha256"] != digest(P.SYSTEM_PROMPT)
                ):
                    raise P.ProviderError("CONFIGURATION_CHANGED")
                b = await budget(p)
                if b["circuit_until"] and b["circuit_until"] > now():
                    raise P.ProviderError("CIRCUIT_OPEN")
                if not P.enabled(self.settings) or self.adapter.name == "disabled":
                    raise P.ProviderError("PROVIDER_DISABLED")
                if operation != "completion" and not self.settings.ai_embedding_model:
                    raise P.ProviderError("EMBEDDINGS_DISABLED")
                if self.settings.ai_provider == "gemini":
                    # Locking the tenant budget serializes attempt admission across workers.
                    # A zero-dollar ledger alone cannot bound request counts.
                    attempts = await conn.scalar(
                        sa.select(sa.func.count())
                        .select_from(T.calls)
                        .where(T.calls.c.run_id == run["id"])
                    )
                    recent = await conn.scalar(
                        sa.select(sa.func.count())
                        .select_from(T.calls)
                        .join(T.runs, T.runs.c.id == T.calls.c.run_id)
                        .where(
                            T.calls.c.organization_id == self.tenant,
                            T.runs.c.created_at >= now() - timedelta(hours=24),
                            T.runs.c.versions["provider"].astext == "gemini",
                        )
                    )
                    if attempts >= 4 or recent >= self.settings.ai_gemini_daily_call_limit:
                        raise P.ProviderError("FREE_TIER_CALL_LIMIT")
                cap = Decimal(run["versions"]["call_cap_usd"])
                if run["charged_usd"] + cap > run["reservation"]:
                    raise P.ProviderError("BUDGET_EXHAUSTED")
                if sum(len(text.encode()) for text in texts) > 100000:
                    raise P.ProviderError("PROVIDER_INPUT_LIMIT")
                # Persist conservative charge BEFORE the request. Ambiguous outcomes retain it.
                await conn.execute(
                    T.runs.update()
                    .where(T.runs.c.id == run["id"])
                    .values(charged_usd=run["charged_usd"] + cap)
                )
                await conn.execute(
                    T.calls.insert().values(
                        id=call_id,
                        organization_id=self.tenant,
                        run_id=run["id"],
                        operation=operation,
                        attempt=attempt,
                        status="unknown",
                        code="CALL_OUTCOME_UNKNOWN",
                        charged_usd=cap,
                        input_tokens=None,
                        output_tokens=None,
                        latency_ms=0,
                    )
                )
                await stage(conn, job, "embedding" if operation != "completion" else "completion")
            start = perf_counter()
            error = None
            result = None
            try:
                result = await asyncio.wait_for(
                    self.adapter.complete(
                        query, [{"chunk_id": str(r["id"]), "text": r["text"]} for r in rows or []]
                    )
                    if operation == "completion"
                    else self.adapter.embed(texts),
                    timeout=(
                        P.GEMINI_COMPLETION_TIMEOUT_SECONDS
                        if self.settings.ai_provider == "gemini" and operation == "completion"
                        else P.CALL_TIMEOUT_SECONDS
                    ),
                )
                if operation == "completion":
                    result.value = output_schema.model_validate(result.value)
                else:
                    result.value = P.vectors(result.value, len(texts))
                for value in (result.input_tokens, result.output_tokens):
                    if value is not None and (
                        isinstance(value, bool) or not isinstance(value, int) or value < 0
                    ):
                        raise P.ProviderError("PROVIDER_MALFORMED")
            except P.ProviderError as exc:
                error = exc
            except TimeoutError:
                error = P.ProviderError("PROVIDER_TIMEOUT", True)
            except Exception:
                error = P.ProviderError("PROVIDER_MALFORMED")
            elapsed = int((perf_counter() - start) * 1000)
            async with self.engine.begin() as conn:
                # Accounting is safe even after cancellation/revocation: precharge already persists.
                p, run, job = await worker_context(conn, self.job_id, self.tenant, self.actor)
                if not p or not run or not job:
                    raise P.ProviderError("RUN_CANCELLED")
                b = await budget(p)
                failures = b["failures"] + 1 if error else 0
                await conn.execute(
                    T.budgets.update()
                    .where(T.budgets.c.id == b["id"])
                    .values(
                        failures=failures,
                        circuit_until=now() + timedelta(seconds=30) if failures >= 3 else None,
                    )
                )
                await conn.execute(
                    T.calls.update()
                    .where(T.calls.c.id == call_id)
                    .values(
                        status="failed" if error else "succeeded",
                        code=error.code if error else None,
                        input_tokens=result.input_tokens if result and not error else None,
                        output_tokens=result.output_tokens if result and not error else None,
                        latency_ms=elapsed,
                    )
                )
                fenced = run["settled"] or job["lease_token"] != self.token
            if fenced:
                raise P.ProviderError("RUN_CANCELLED")
            if not error and result:
                return result
            if error and (not error.retryable or attempt == 2):
                raise error
            await asyncio.sleep(0.05 * attempt)
        raise P.ProviderError("PROVIDER_FAILED")

    async def keyword_branch(self, project: UUID, query: str) -> Branch:
        try:
            async with self.engine.begin() as conn:
                p, _, _ = await self.state(conn)
                return Branch("keyword", await keyword(p, project, query))
        except (P.ProviderError, delivery.DomainError):
            return Branch("keyword", [], "KEYWORD_UNAVAILABLE")

    async def hybrid_branch(self, project: UUID, query: str) -> Branch:
        try:
            response = await self.call("query_embedding", [query])
            async with self.engine.begin() as conn:
                p, _, _ = await self.state(conn)
                await authorize_tool(p, SourceTool(tool="hybrid", project_id=project), project)
                rows = list(
                    (
                        await conn.execute(
                            sa.select(
                                D.chunks,
                                D.versions.c.sha256,
                                T.embeddings.c.vector,
                                T.embeddings.c.text_sha256,
                            )
                            .select_from(T.embeddings)
                            .join(D.chunks, D.chunks.c.id == T.embeddings.c.chunk_id)
                            .join(D.versions, D.versions.c.id == D.chunks.c.version_id)
                            .join(D.documents, D.documents.c.id == D.versions.c.document_id)
                            .where(
                                D.documents.c.project_id == project,
                                T.embeddings.c.model == self.settings.ai_embedding_model,
                                T.embeddings.c.chunk_version == "locations-1200-v1",
                            )
                            .order_by(D.chunks.c.id)
                            .limit(201)
                        )
                    ).mappings()
                )
                if len(rows) > 200:
                    raise P.ProviderError("HYBRID_CANDIDATE_LIMIT")
                valid = [dict(r) for r in rows if digest(r["text"]) == r["text_sha256"]]
                valid.sort(key=lambda r: (-cosine(response.value[0], r["vector"]), str(r["id"])))
                return Branch("hybrid", valid[:5], None if valid else "EMBEDDINGS_UNAVAILABLE")
        except P.ProviderError as exc:
            return Branch("hybrid", [], exc.code)
        except Exception:
            return Branch("hybrid", [], "HYBRID_UNAVAILABLE")

    async def index(self, request: EmbeddingRequest) -> None:
        # Implements Sprint 09 EmbeddingBackend.index; source identity is independently verified.
        async with self.engine.begin() as conn:
            p, run, _ = await self.state(conn)
            expected, rows = await index_chunks(p, run["project_id"], request.version_id)
            if expected != request:
                raise P.ProviderError("EMBEDDING_SCOPE_INVALID")
            await validate_snapshot(p, run["evidence"])
        response = await self.call("source_embedding", [r["text"] for r in rows])
        async with self.engine.begin() as conn:
            p, run, _ = await self.state(conn)
            await validate_snapshot(p, run["evidence"])
            for row, vector in zip(rows, response.value, strict=True):
                await conn.execute(
                    T.embeddings.delete().where(T.embeddings.c.chunk_id == row["id"])
                )
                await conn.execute(
                    T.embeddings.insert().values(
                        id=uuid4(),
                        organization_id=self.tenant,
                        chunk_id=row["id"],
                        source_sha256=request.sha256,
                        text_sha256=digest(row["text"]),
                        model=self.settings.ai_embedding_model,
                        chunk_version=request.chunk_version,
                        vector=vector,
                        run_id=run["id"],
                    )
                )


async def ai_worker(engine: Any, id_: UUID, tenant: UUID, actor: UUID, settings: Settings) -> bool:
    p: Principal | None
    job: dict | None
    current: dict | None
    token = uuid4()
    async with engine.begin() as conn:
        p, run, job = await worker_context(conn, id_, tenant, actor)
        if run is None:
            return False
        if not p or not run or not job or run["settled"] or job["status"] in TERMINAL:
            return True
        if job["status"] == "running" and job["lease_until"] and job["lease_until"] > now():
            return True
        if job["attempt"]:
            # A worker crash has an ambiguous external outcome; never silently spend again.
            await settle(
                p,
                run,
                job,
                "failed",
                "CALL_OUTCOME_UNKNOWN",
                [],
                run["evidence"],
                "none",
                ["Worker interrupted; inspect the retained attempt before a new run"],
            )
            return True
        await conn.execute(
            J.jobs.update()
            .where(J.jobs.c.id == id_)
            .values(
                status="running",
                attempt=1,
                lease_token=token,
                lease_until=now() + timedelta(seconds=75),
            )
        )
        await conn.execute(
            J.outbox.update().where(J.outbox.c.job_id == id_).values(dispatched_at=now())
        )
        await stage(conn, job, "validating_sources")
    runtime = Runtime(engine, id_, tenant, actor, settings, P.provider(settings), token)
    result, refs, code, limitations, retrieval = [], [], None, [], "none"
    agent_output = None
    final_status = "succeeded"
    try:
        if run["snapshot"]["operation"] == "agents":
            from ppm_api.agents import execute

            agent_output, code = await execute(runtime, run)
            if code or any(s["status"] != "supported" for s in agent_output["agents"]):
                final_status = "partially_succeeded"
            limitations.append(
                "Specialists propose review candidates only; real model quality UNVERIFIED/BLOCKED"
            )
        elif run["snapshot"]["operation"] == "index":
            async with engine.begin() as conn:
                p, current, _ = await runtime.state(conn)
                request, _ = await index_chunks(
                    p, current["project_id"], UUID(current["snapshot"]["version_id"])
                )
            await runtime.index(request)
            limitations.append(
                "Rebuildable 256-dimension projection; real retrieval quality is unverified"
            )
        else:
            project, query = run["project_id"], run["snapshot"]["query"]
            branches = await asyncio.gather(
                runtime.keyword_branch(project, query), runtime.hybrid_branch(project, query)
            )
            rows = merge(branches[0].rows, branches[1].rows)
            retrieval = "hybrid" if branches[1].rows else "keyword"
            refs = [snapshot(row) for row in rows]
            limitations = [b.code for b in branches if b.code]
            if not rows:
                code, final_status = "EVIDENCE_UNAVAILABLE", "partially_succeeded"
                limitations.append("No permitted matching source evidence; no answer is available")
            else:
                # Reauthorize references immediately before sending source text to any provider.
                async with engine.begin() as conn:
                    p, _, job = await runtime.state(conn)
                    await validate_snapshot(p, refs)
                    await conn.execute(
                        T.runs.update().where(T.runs.c.id == run["id"]).values(evidence=refs)
                    )
                    await stage(conn, job, "retrieving_evidence")
                try:
                    if settings.ai_provider == "gemini" and branches[1].code in {
                        "PROVIDER_QUOTA",
                        "FREE_TIER_CALL_LIMIT",
                    }:
                        raise P.ProviderError(branches[1].code)
                    response = await runtime.call(
                        "completion", [r["text"] for r in rows], query, rows
                    )
                    result = evaluate(response.value, rows)
                    if response.value.status == "unavailable":
                        limitations.append("Provider abstained; no supported answer is available")
                        final_status = "partially_succeeded"
                except P.ProviderError as exc:
                    code, final_status = exc.code, "partially_succeeded"
                    # Keyword/source fallback is explicit, never a fabricated model answer.
                    result = refs
                    limitations.append("Source excerpts only; AI answer unavailable")
                if limitations:
                    final_status = "partially_succeeded"
            limitations.append(
                "Extractive evidence preview only; no agents, semantic findings or plan edits"
            )
    except P.ProviderError as exc:
        code, final_status = exc.code, "failed"
        result = []
    except delivery.DomainError:
        code, final_status = "EVIDENCE_UNAVAILABLE", "failed"
        result = []
    except Exception:
        code, final_status = "RUN_FAILED", "failed"
        result = []
    async with engine.begin() as conn:
        p, current, job = await worker_context(conn, id_, tenant, actor)
        if (
            not p
            or not current
            or not job
            or current["settled"]
            or job["lease_token"] != token
            or job["lease_until"] <= now()
        ):
            return True
        try:
            await validate_snapshot(p, result)
            if agent_output is not None:
                from ppm_api.agents import publish

                await publish(p, current, agent_output)
        except (delivery.DomainError, P.ProviderError):
            result, code, final_status = [], "EVIDENCE_UNAVAILABLE", "failed"
        await settle(
            p,
            current,
            job,
            final_status,
            code,
            result,
            refs or current["evidence"],
            retrieval,
            limitations
            + (
                ["USD charge is a conservative reservation, not an invoice"]
                if current["charged_usd"]
                else []
            ),
        )
    return True
