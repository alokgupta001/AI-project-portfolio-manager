"""HTTP adapters; business operations belong to the feature service."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Request

import ppm_api.modules.command.tables  # noqa: F401 — worker callers also need the metric registry
from ppm_api.modules.command import service as _operations
from ppm_api.modules.command.schemas import CommandSnapshot
from ppm_api.modules.identity.service import Auth

router = APIRouter(prefix="/api/v1/command", tags=["Command center"])


@router.get("/snapshot", response_model=CommandSnapshot)
async def snapshot(
    start: date, end: date, request: Request, p: Auth, portfolio_id: UUID | None = None
) -> dict:
    return await _operations.snapshot(
        start=start, end=end, request=request, p=p, portfolio_id=portfolio_id
    )
