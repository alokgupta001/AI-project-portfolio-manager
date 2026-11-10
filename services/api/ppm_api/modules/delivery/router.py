"""HTTP adapters; business operations belong to the feature service."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, Query, Request

from ppm_api.modules.delivery import service as _operations
from ppm_api.modules.delivery.schemas import (
    HistoryView,
    Input,
    PageView,
    PersonView,
    PortfolioSummary,
    RecordView,
    SummaryView,
)
from ppm_api.modules.delivery.service import LiteralSort
from ppm_api.modules.identity.service import Auth
from ppm_api.shared.record_schemas import Kind

router = APIRouter(prefix="/api/v1/delivery", tags=["Delivery"])


@router.get("/people", response_model=list[PersonView])
async def people(
    p: Auth,
    q: str = Query(default="", max_length=160),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[dict]:
    return await _operations.people(p=p, q=q, offset=offset, limit=limit)


@router.get("/history/{kind}/{id_}", response_model=list[HistoryView])
async def history(kind: Kind, id_: UUID, p: Auth) -> list[dict]:
    return await _operations.history(kind=kind, id_=id_, p=p)


@router.get("/portfolio-summary/{id_}", response_model=PortfolioSummary)
async def portfolio_summary(id_: UUID, p: Auth) -> dict:
    return await _operations.portfolio_summary(id_=id_, p=p)


@router.get("/project-summary/{id_}", response_model=SummaryView)
async def summary(id_: UUID, p: Auth) -> dict:
    return await _operations.summary(id_=id_, p=p)


@router.get("/{kind}", response_model=PageView)
async def listing(
    kind: Kind,
    p: Auth,
    q: str = Query(default="", max_length=160),
    project_id: UUID | None = None,
    portfolio_id: UUID | None = None,
    resource_id: UUID | None = None,
    skill: str = Query(default="", max_length=80),
    archived: bool = False,
    status: str | None = None,
    industry: str | None = Query(None, max_length=30),
    sort: LiteralSort = "name",
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> dict:
    return await _operations.listing(
        kind=kind,
        p=p,
        q=q,
        project_id=project_id,
        portfolio_id=portfolio_id,
        resource_id=resource_id,
        skill=skill,
        archived=archived,
        status=status,
        industry=industry,
        sort=sort,
        offset=offset,
        limit=limit,
    )


@router.get("/{kind}/{id_}", response_model=RecordView)
async def detail(kind: Kind, id_: UUID, p: Auth) -> dict:
    return await _operations.detail(kind=kind, id_=id_, p=p)


@router.post("/{kind}", response_model=RecordView, status_code=201)
async def create(
    kind: Kind,
    payload: Input,
    request: Request,
    p: Auth,
    idempotency_key: Annotated[UUID, Header()],
) -> dict:
    return await _operations.create(
        kind=kind, payload=payload, request=request, p=p, idempotency_key=idempotency_key
    )


@router.patch("/{kind}/{id_}", response_model=RecordView)
async def update(
    kind: Kind,
    id_: UUID,
    payload: Input,
    request: Request,
    p: Auth,
    if_match: Annotated[int | None, Header()] = None,
    x_change_reason: Annotated[str, Header(max_length=1000)] = "",
) -> dict:
    return await _operations.update(
        kind=kind,
        id_=id_,
        payload=payload,
        request=request,
        p=p,
        if_match=if_match,
        x_change_reason=x_change_reason,
    )
