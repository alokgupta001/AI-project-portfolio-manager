"""HTTP adapters; business operations belong to the feature service."""

from uuid import UUID

from fastapi import APIRouter, Request

from ppm_api.modules.identity.service import Auth
from ppm_api.modules.integrations import connectors as _operations
from ppm_api.modules.integrations.schemas import (
    AuthorityInput,
    AuthorityView,
    ConflictView,
    Resolution,
)

router = APIRouter(prefix="/api/v1/integrations", tags=["Connector authority and conflicts"])


@router.get("/{id_}/authority", response_model=AuthorityView | None)
async def authority(id_: UUID, p: Auth) -> dict | None:
    return await _operations.authority(id_=id_, p=p)


@router.put("/{id_}/authority", response_model=AuthorityView)
async def approve(id_: UUID, body: AuthorityInput, request: Request, p: Auth) -> dict:
    """Each rotation fences queued work; secrets themselves never travel through this API."""
    return await _operations.approve(id_=id_, body=body, request=request, p=p)


@router.get("/{id_}/conflicts", response_model=list[ConflictView])
async def review(id_: UUID, p: Auth) -> list[dict]:
    return await _operations.review(id_=id_, p=p)


@router.post("/{id_}/conflicts/{conflict_id}/resolve", response_model=ConflictView)
async def resolve(
    id_: UUID, conflict_id: UUID, body: Resolution, request: Request, p: Auth
) -> dict:
    return await _operations.resolve(
        id_=id_, conflict_id=conflict_id, body=body, request=request, p=p
    )
