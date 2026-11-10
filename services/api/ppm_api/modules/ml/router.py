"""HTTP adapters; business operations belong to the feature service."""

from uuid import UUID

from fastapi import APIRouter, Request

from ppm_api.modules.identity.service import Auth
from ppm_api.modules.ml import service as _operations
from ppm_api.modules.ml.schemas import (
    DatasetInput,
    DatasetView,
    HistoryInput,
    MLHistoryView,
    RunInput,
    RunView,
    Target,
)

router = APIRouter(prefix="/api/v1/ml", tags=["Local datasets and baselines"])


@router.get("/template", response_model=dict)
async def template(project_id: UUID, p: Auth, target: Target = "delay") -> dict:
    return await _operations.template(project_id=project_id, p=p, target=target)


@router.get("/histories", response_model=list[MLHistoryView])
async def history_list(p: Auth) -> list[dict]:
    return await _operations.history_list(p=p)


@router.post("/histories", response_model=MLHistoryView, status_code=201)
async def import_history(body: HistoryInput, request: Request, p: Auth) -> dict:
    return await _operations.import_history(body=body, request=request, p=p)


@router.post("/histories/{id_}/withdraw", response_model=MLHistoryView)
async def withdraw(id_: UUID, request: Request, p: Auth) -> dict:
    return await _operations.withdraw(id_=id_, request=request, p=p)


@router.get("/datasets", response_model=list[DatasetView])
async def dataset_list(p: Auth) -> list[dict]:
    return await _operations.dataset_list(p=p)


@router.post("/datasets", response_model=DatasetView, status_code=201)
async def create_dataset(body: DatasetInput, request: Request, p: Auth) -> dict:
    return await _operations.create_dataset(body=body, request=request, p=p)


@router.get("/datasets/{id_}", response_model=DatasetView)
async def dataset_detail(id_: UUID, p: Auth) -> dict:
    return await _operations.dataset_detail(id_=id_, p=p)


@router.get("/runs", response_model=list[RunView])
async def run_list(p: Auth) -> list[dict]:
    return await _operations.run_list(p=p)


@router.post("/runs", response_model=RunView, status_code=202)
async def train(body: RunInput, request: Request, p: Auth) -> dict:
    return await _operations.train(body=body, request=request, p=p)


@router.get("/runs/{id_}", response_model=RunView)
async def run_detail(id_: UUID, p: Auth) -> dict:
    return await _operations.run_detail(id_=id_, p=p)


@router.get("/runs/{id_}/artifacts", response_model=dict)
async def artifacts(id_: UUID, p: Auth) -> dict:
    return await _operations.artifacts(id_=id_, p=p)
