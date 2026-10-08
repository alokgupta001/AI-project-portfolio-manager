import asyncio
import json
import logging
import secrets
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from time import perf_counter
from typing import Any
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy import select, text
from starlette.exceptions import HTTPException

import ppm_api.assessment_tables  # noqa: F401 — registers assessment tables into TABLES
import ppm_api.command_tables  # noqa: F401
from ppm_api.assessment import router as assessment_router
from ppm_api.capacity import router as capacity_router
from ppm_api.command import router as command_router
from ppm_api.config import Settings, load_settings
from ppm_api.database import FoundationState, make_engine
from ppm_api.delivery import DomainError
from ppm_api.delivery import router as delivery_router
from ppm_api.identity import router as identity_router
from ppm_api.schemas import (
    DependencyStatus,
    ErrorBody,
    ErrorDetail,
    ErrorResponse,
    FoundationResponse,
    HealthResponse,
    ReadyResponse,
)
from ppm_api.storage import LocalObjectStore

logger = logging.getLogger("ppm.requests")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


def error_response(
    request: Request, status: int, code: str, message: str, details: list[ErrorDetail] | None = None
) -> JSONResponse:
    body = ErrorResponse(
        error=ErrorBody(
            code=code, message=message, request_id=request.state.request_id, details=details or []
        )
    )
    return JSONResponse(status_code=status, content=body.model_dump())


def create_app(settings: Settings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        config = settings or load_settings()
        app.state.settings = config
        app.state.engine = make_engine(config)
        app.state.redis = Redis.from_url(
            config.redis_url.get_secret_value(),
            socket_timeout=config.dependency_timeout_seconds,
            socket_connect_timeout=config.dependency_timeout_seconds,
        )
        app.state.storage = LocalObjectStore(config.storage_root)
        try:
            yield
        finally:
            await app.state.redis.aclose()
            await app.state.engine.dispose()

    app = FastAPI(title="Enterprise PPM foundation", version="0.1.0", lifespan=lifespan)
    app.include_router(command_router)
    app.include_router(capacity_router)
    app.include_router(assessment_router)

    @app.middleware("http")
    async def request_context(request: Request, call_next: Callable[..., Awaitable[Any]]) -> Any:
        supplied = request.headers.get("x-request-id", "")
        try:
            request_id = str(UUID(supplied))
        except ValueError:
            request_id = str(uuid4())
        request.state.request_id = request_id
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            config = request.app.state.settings
            csrf_cookie = request.cookies.get("ppm_csrf", "")
            csrf_header = request.headers.get("x-csrf-token", "")
            if (
                request.headers.get("origin") != config.web_origin
                or len(csrf_cookie) < 32
                or not secrets.compare_digest(csrf_cookie, csrf_header)
            ):
                rejected = error_response(
                    request, 403, "CSRF_REJECTED", "Request verification failed."
                )
                rejected.headers["X-Request-ID"] = request_id
                rejected.headers["Cache-Control"] = "no-store"
                logger.info(
                    json.dumps(
                        {
                            "event": "csrf_rejected",
                            "request_id": request_id,
                            "method": request.method,
                            "status": 403,
                        }
                    )
                )
                return rejected
        started = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            # Do not log raw errors: drivers may include connection strings or credentials.
            response = error_response(request, 500, "INTERNAL_ERROR", "An internal error occurred.")
        response.headers["X-Request-ID"] = request_id
        response.headers["Cache-Control"] = "no-store"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        route = request.scope.get("route")
        logger.info(
            json.dumps(
                {
                    "event": "http_request",
                    "request_id": request_id,
                    "method": request.method,
                    "route": getattr(route, "path", "unmatched"),
                    "status": response.status_code,
                    "duration_ms": round((perf_counter() - started) * 1000, 2),
                }
            )
        )
        return response

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
        response = error_response(
            request,
            exc.status_code,
            "HTTP_ERROR",
            str(exc.detail) if isinstance(exc, DomainError) else "Request could not be completed.",
        )
        if exc.headers:
            response.headers.update(exc.headers)
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return error_response(
            request,
            422,
            "VALIDATION_ERROR",
            "Request validation failed.",
            [
                ErrorDetail(field=".".join(str(p) for p in e["loc"]), reason=e["type"])
                for e in exc.errors()
            ],
        )

    @app.get("/api/v1/health/live", response_model=HealthResponse, operation_id="getLiveness")
    async def live() -> HealthResponse:
        return HealthResponse()

    @app.get(
        "/api/v1/health/ready",
        response_model=ReadyResponse,
        responses={503: {"model": ReadyResponse}},
        operation_id="getReadiness",
    )
    async def ready(request: Request) -> JSONResponse:
        async def database_probe() -> None:
            async with request.app.state.engine.connect() as conn:
                result = await conn.execute(select(FoundationState.instance_id))
                if result.scalar_one_or_none() is None:
                    raise RuntimeError("Missing migration checkpoint")
                revision = await conn.scalar(text("SELECT version_num FROM alembic_version"))
                if revision != "0006_command_center":
                    raise RuntimeError("Schema revision mismatch")

        async def redis_probe() -> None:
            await request.app.state.redis.ping()

        async def storage_probe() -> None:
            if not await asyncio.to_thread(request.app.state.storage.ready):
                raise RuntimeError("Storage unavailable")

        async def probe(name: Any, action: Callable[[], Awaitable[None]]) -> DependencyStatus:
            try:
                await asyncio.wait_for(
                    action(), request.app.state.settings.dependency_timeout_seconds
                )
                return DependencyStatus(name=name, status="ready")
            except Exception:
                return DependencyStatus(name=name, status="unavailable")

        results = await asyncio.gather(
            probe("database", database_probe),
            probe("redis", redis_probe),
            probe("storage", storage_probe),
        )
        ok = all(r.status == "ready" for r in results)
        payload = ReadyResponse(status="ready" if ok else "not_ready", dependencies=list(results))
        return JSONResponse(status_code=200 if ok else 503, content=payload.model_dump())

    @app.get(
        "/api/v1/foundation",
        response_model=FoundationResponse,
        responses={503: {"model": ErrorResponse}},
        operation_id="getFoundation",
    )
    async def foundation(request: Request) -> Any:
        try:
            async with request.app.state.engine.connect() as conn:
                row = (await conn.execute(select(FoundationState))).mappings().one()
            return FoundationResponse(
                instance_id=row["instance_id"],
                initialized_at=row["created_at"],
                environment=request.app.state.settings.app_env,
            )
        except Exception:
            return error_response(request, 503, "DATABASE_UNAVAILABLE", "Database is not ready.")

    app.include_router(identity_router)
    app.include_router(delivery_router)
    return app


app = create_app()
