"""HTTP adapters; business operations belong to the feature service."""

from uuid import UUID

from fastapi import APIRouter, Request

from ppm_api.modules.identity.service import Auth
from ppm_api.modules.selection import service as _operations
from ppm_api.modules.selection.schemas import AutomatedReview, LabelReview, PilotInput, PilotView

router = APIRouter(prefix="/api/v1/agents/selection-pilots", tags=["Financial selection pilot"])


@router.get("", response_model=list[PilotView])
async def listing(project_id: UUID, request: Request, p: Auth) -> list[dict]:
    """List ten recent authorized pilots, reconstructing measurements without inference."""
    return await _operations.listing(project_id=project_id, request=request, p=p)


@router.post("", response_model=PilotView, status_code=201)
async def create(body: PilotInput, request: Request, p: Auth) -> dict:
    """Prepare an idempotent frozen fixture protocol; make no model call or label approval."""
    return await _operations.create(body=body, request=request, p=p)


@router.get("/{id_}", response_model=PilotView)
async def detail(id_: UUID, request: Request, p: Auth) -> dict:
    """Recheck current access and return a downloadable pilot report without inference."""
    return await _operations.detail(id_=id_, request=request, p=p)


@router.post("/{id_}/label-review", response_model=PilotView)
async def approve(id_: UUID, body: LabelReview, request: Request, p: Auth) -> dict:
    """Freeze a different authorized human's review of every bound fixture label."""
    return await _operations.approve(id_=id_, body=body, request=request, p=p)


@router.post("/{id_}/automated-review", response_model=PilotView)
async def automated_review(id_: UUID, body: AutomatedReview, request: Request, p: Auth) -> dict:
    """Record a scoped machine audit with human_reviewed=false; preserve all human gates."""
    return await _operations.automated_review(id_=id_, body=body, request=request, p=p)


@router.post("/{id_}/cases/{case_id}", response_model=PilotView, status_code=202)
async def measure(id_: UUID, case_id: str, request: Request, p: Auth) -> dict:
    """Queue one ordered fixture through normal AI admission; retain duplicate/failed runs."""
    return await _operations.measure(id_=id_, case_id=case_id, request=request, p=p)
