"""HTTP adapters; business operations belong to the feature service."""

from uuid import UUID

from fastapi import APIRouter, Query, Request
from fastapi.responses import StreamingResponse

from ppm_api.modules.ai import service as _operations
from ppm_api.modules.ai.schemas import (
    AIBudgetInput,
    AIDiagnostics,
    AIEvaluation,
    AIOperations,
    AIProviderStatus,
    AIRunInput,
    AIRunView,
)
from ppm_api.modules.identity.service import Auth
from ppm_api.modules.integrations.schemas import StageView

router = APIRouter(prefix="/api/v1/ai", tags=["AI runtime"])


@router.get("/status", response_model=AIProviderStatus)
async def status(request: Request, p: Auth) -> dict:
    """Return the configured AI provider status without exposing credentials."""
    return await _operations.status(request=request, p=p)


@router.get("/runs", response_model=list[AIRunView])
async def listing(
    p: Auth, project_id: UUID | None = None, offset: int = Query(default=0, ge=0, le=10000)
) -> list[dict]:
    """List visible AI runs in a bounded page, optionally scoped to a project."""
    return await _operations.listing(p=p, project_id=project_id, offset=offset)


@router.get("/runs/{id_}", response_model=AIRunView)
async def detail(id_: UUID, p: Auth) -> dict:
    """Return a run after current tenant, project and private evidence checks."""
    return await _operations.detail(id_=id_, p=p)


@router.get("/evaluation", response_model=AIEvaluation)
async def evaluation(p: Auth) -> dict:
    """Run the deterministic offline evaluation suite for an administrator."""
    return await _operations.evaluation(p=p)


@router.get("/operations", response_model=AIOperations)
async def operations(request: Request, p: Auth) -> dict:
    """Return tenant budget, circuit and provider operations data for an administrator."""
    return await _operations.operations(request=request, p=p)


@router.patch("/budget", response_model=AIOperations)
async def configure(body: AIBudgetInput, request: Request, p: Auth) -> dict:
    """Update the tenant budget within the operator limit using optimistic concurrency."""
    return await _operations.configure(body=body, request=request, p=p)


@router.post("/runs", response_model=AIRunView, status_code=202)
async def create(body: AIRunInput, request: Request, p: Auth) -> dict:
    """Queue an idempotent authorized run after reserving its budget and frozen inputs."""
    return await _operations.create(body=body, request=request, p=p)


@router.post("/runs/{id_}/cancel", response_model=AIRunView)
async def cancel(id_: UUID, request: Request, p: Auth) -> dict:
    """Cancel a visible run with revision checks and settle its remaining reservation."""
    return await _operations.cancel(id_=id_, request=request, p=p)


@router.get("/runs/{id_}/events", response_class=StreamingResponse)
async def progress(id_: UUID, request: Request, p: Auth) -> StreamingResponse:
    """Stream bounded run progress while repeatedly checking the caller's authority."""
    return await _operations.progress(id_=id_, request=request, p=p)


@router.get("/runs/{id_}/stages", response_model=list[StageView])
async def stages(id_: UUID, p: Auth) -> list[dict]:
    """Return the visible run's ordered durable stage history."""
    return await _operations.stages(id_=id_, p=p)


@router.get("/runs/{id_}/diagnostics", response_model=AIDiagnostics)
async def diagnostics(id_: UUID, p: Auth) -> dict:
    """Expose sanitized run diagnostics to an authorized administrator."""
    return await _operations.diagnostics(id_=id_, p=p)
