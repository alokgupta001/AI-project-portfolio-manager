"""HTTP adapters; business operations belong to the feature service."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter

from ppm_api.modules.capacity import service as _operations
from ppm_api.modules.capacity.schemas import CapacityView, SnapshotView, TeamCapacityView
from ppm_api.modules.identity.service import Auth

router = APIRouter(prefix="/api/v1/capacity", tags=["Capacity"])


@router.get("/resources/{rid}", response_model=CapacityView)
async def resource_summary(
    rid: UUID, start: date, end: date, p: Auth, project_id: UUID | None = None
) -> dict:
    return await _operations.resource_summary(
        rid=rid, start=start, end=end, p=p, project_id=project_id
    )


@router.get("/snapshots/{id_}", response_model=SnapshotView)
async def saved_snapshot(id_: UUID, p: Auth) -> dict:
    return await _operations.saved_snapshot(id_=id_, p=p)


@router.get("/teams/{tid}", response_model=TeamCapacityView)
async def team_summary(tid: UUID, start: date, end: date, p: Auth) -> dict:
    return await _operations.team_summary(tid=tid, start=start, end=end, p=p)
