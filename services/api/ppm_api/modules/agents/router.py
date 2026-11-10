"""HTTP adapters; business operations belong to the feature service."""

from uuid import UUID

from fastapi import APIRouter, Query, Request

from ppm_api.modules.agents import service as _operations
from ppm_api.modules.agents.schemas import (
    AgentDefinition,
    AnalysisInput,
    AnalysisSummary,
    AnalysisView,
    ReviewInput,
)
from ppm_api.modules.identity.service import Auth

router = APIRouter(prefix="/api/v1/agents", tags=["Specialists and recommendations"])


@router.get("/definitions", response_model=list[AgentDefinition])
async def definitions(request: Request, p: Auth) -> list[dict]:
    """List the available typed specialist definitions for the current runtime."""
    return await _operations.definitions(request=request, p=p)


@router.post("/runs", response_model=AnalysisView, status_code=202)
async def create(body: AnalysisInput, request: Request, p: Auth) -> dict:
    """Queue an authorized specialist analysis using the existing budget and job controls."""
    return await _operations.create(body=body, request=request, p=p)


@router.get("/runs", response_model=list[AnalysisSummary])
async def listing(p: Auth, offset: int = Query(0, ge=0, le=10000)) -> list[dict]:
    """List visible specialist analyses for the requested project and page."""
    return await _operations.listing(p=p, offset=offset)


@router.get("/runs/{id_}", response_model=AnalysisView)
async def detail(id_: UUID, p: Auth) -> dict:
    """Return an analysis with evidence filtered through current access checks."""
    return await _operations.detail(id_=id_, p=p)


@router.post("/runs/{id_}/reviews/{item_key}", response_model=AnalysisView)
async def review(id_: UUID, item_key: str, body: ReviewInput, request: Request, p: Auth) -> dict:
    """Record an authorized suggestion decision with revision and idempotency checks."""
    return await _operations.review(id_=id_, item_key=item_key, body=body, request=request, p=p)
