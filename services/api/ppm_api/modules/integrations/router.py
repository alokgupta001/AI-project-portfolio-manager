"""HTTP adapters; business operations belong to the feature service."""

from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from ppm_api.modules.identity.service import Auth
from ppm_api.modules.integrations import jobs as _operations
from ppm_api.modules.integrations.ingestion import (
    ConnectorConfig,
    ImportInput,
)
from ppm_api.modules.integrations.schemas import (
    EnabledInput,
    IntegrationView,
    JobView,
    Preview,
    SourceView,
    StageView,
)

router = APIRouter(prefix="/api/v1/integrations", tags=["Integrations and jobs"])


@router.get("/{id_}/sources", response_model=list[SourceView])
async def source_evidence(id_: UUID, p: Auth) -> list[dict]:
    return await _operations.source_evidence(id_=id_, p=p)


@router.get("", response_model=list[IntegrationView])
async def list_integrations(p: Auth) -> list[dict]:
    return await _operations.list_integrations(p=p)


@router.post("", response_model=IntegrationView, status_code=201)
async def create_integration(body: ConnectorConfig, request: Request, p: Auth) -> dict:
    return await _operations.create_integration(body=body, request=request, p=p)


@router.patch("/{id_}", response_model=IntegrationView)
async def enable_integration(id_: UUID, body: EnabledInput, request: Request, p: Auth) -> dict:
    return await _operations.enable_integration(id_=id_, body=body, request=request, p=p)


@router.post("/{id_}/preview", response_model=Preview)
async def preview(id_: UUID, body: ImportInput, request: Request, p: Auth) -> dict:
    return await _operations.preview(id_=id_, body=body, request=request, p=p)


@router.post("/{id_}/sync", response_model=JobView, status_code=202)
async def sync(id_: UUID, body: ImportInput, request: Request, p: Auth) -> dict:
    return await _operations.sync(id_=id_, body=body, request=request, p=p)


@router.post("/{id_}/webhook", response_model=JobView, status_code=202)
async def webhook(id_: UUID, body: ImportInput, request: Request, p: Auth) -> dict:
    """Authenticated signed gateway intake; never an unauthenticated provider endpoint."""
    return await _operations.webhook(id_=id_, body=body, request=request, p=p)


@router.get("/activity/jobs", response_model=list[JobView])
async def activity(p: Auth) -> list[dict]:
    return await _operations.activity(p=p)


@router.get("/activity/jobs/{id_}", response_model=JobView)
async def job_detail(id_: UUID, p: Auth) -> dict:
    return await _operations.job_detail(id_=id_, p=p)


@router.get("/activity/jobs/{id_}/stages", response_model=list[StageView])
async def stage_history(id_: UUID, p: Auth) -> list[dict]:
    return await _operations.stage_history(id_=id_, p=p)


@router.post("/activity/jobs/{id_}/cancel", response_model=JobView)
async def cancel(id_: UUID, request: Request, p: Auth) -> dict:
    return await _operations.cancel(id_=id_, request=request, p=p)


@router.get("/activity/jobs/{id_}/events", response_class=StreamingResponse)
async def stream(id_: UUID, request: Request, p: Auth) -> StreamingResponse:
    return await _operations.stream(id_=id_, request=request, p=p)


@router.post("/hooks/github/{id_}", response_model=JobView, status_code=202)
async def github_hook(id_: UUID, request: Request) -> dict:
    return await _operations.github_hook(id_=id_, request=request)
