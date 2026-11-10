"""HTTP adapters; business operations belong to the feature service."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Query, Request
from fastapi.responses import StreamingResponse

from ppm_api.modules.identity.service import Auth
from ppm_api.modules.workspace import service as _operations
from ppm_api.modules.workspace.schemas import PreferenceInput, SearchKind, SearchPage

router = APIRouter(prefix="/api/v1/workspace", tags=["Workspace"])


@router.get("/search", response_model=SearchPage)
async def search(
    p: Auth,
    q: str = Query("", max_length=160),
    kind: SearchKind | None = None,
    offset: int = Query(0, ge=0, le=100000),
    limit: int = Query(25, ge=1, le=100),
) -> dict:
    return await _operations.search(p=p, q=q, kind=kind, offset=offset, limit=limit)


@router.get("/my-work", response_model=SearchPage)
async def my_work(
    p: Auth, offset: int = Query(0, ge=0, le=100000), limit: int = Query(25, ge=1, le=100)
) -> dict:
    return await _operations.my_work(p=p, offset=offset, limit=limit)


@router.get("/setup", response_model=dict)
async def setup(p: Auth) -> dict:
    return await _operations.setup(p=p)


@router.get("/comparison", response_model=dict)
async def comparison(p: Auth, framework_version_id: UUID, start: date, end: date) -> dict:
    return await _operations.comparison(
        p=p, framework_version_id=framework_version_id, start=start, end=end
    )


@router.get("/notifications", response_model=dict)
async def feed(p: Auth, offset: int = Query(0, ge=0), limit: int = Query(25, ge=1, le=100)) -> dict:
    return await _operations.feed(p=p, offset=offset, limit=limit)


@router.put("/notification-preference", response_model=PreferenceInput)
async def preference(body: PreferenceInput, p: Auth) -> dict:
    return await _operations.preference(body=body, p=p)


@router.post("/notifications/{id_}/read", response_model=dict)
async def mark_read(id_: UUID, p: Auth) -> dict:
    return await _operations.mark_read(id_=id_, p=p)


@router.get("/events", response_class=StreamingResponse)
async def stream(request: Request, p: Auth) -> StreamingResponse:
    return await _operations.stream(request=request, p=p)
