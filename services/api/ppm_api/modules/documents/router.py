"""Versioned source library, live scoped keyword retrieval, and controlled retention."""

from uuid import UUID

from fastapi import APIRouter, Query, Request, Response

from ppm_api.modules.documents import files as document_files
from ppm_api.modules.documents import lifecycle as document_lifecycle
from ppm_api.modules.documents import queries as document_queries
from ppm_api.modules.documents.schemas import (
    Accepted,
    ChunkView,
    DocumentPage,
    DocumentView,
    DownloadTicket,
    EvidenceLink,
    EvidenceReference,
    Governance,
    JobStatus,
    OrphanPage,
    OrphanPurge,
    Result,
    Retrieval,
    Upload,
)
from ppm_api.modules.identity.service import Auth

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


@router.get("/retention/orphans", response_model=OrphanPage)
async def orphan_preview(request: Request, p: Auth) -> dict:
    return await document_lifecycle.orphan_preview(request=request, p=p)


@router.post("/retention/orphans/purge", response_model=Result)
async def orphan_purge(body: OrphanPurge, request: Request, p: Auth) -> dict:
    return await document_lifecycle.orphan_purge(body=body, request=request, p=p)


@router.get("", response_model=DocumentPage)
async def library(
    p: Auth,
    q: str = Query(default="", max_length=160),
    project_id: UUID | None = None,
    limit: int = Query(default=25, ge=1, le=100),
    offset: int = Query(default=0, ge=0, le=100000),
    deleted: bool = False,
) -> dict:
    return await document_queries.library(
        p=p, q=q, project_id=project_id, limit=limit, offset=offset, deleted=deleted
    )


@router.get("/search", response_model=Retrieval)
async def search(
    p: Auth,
    q: str = Query(min_length=1, max_length=160),
    project_id: UUID | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> dict:
    # RLS filters sources before ranking. Only the latest version is an active index.
    return await document_queries.search(p=p, q=q, project_id=project_id, limit=limit)


@router.get("/{id_}", response_model=DocumentView)
async def detail(id_: UUID, p: Auth) -> dict:
    return await document_queries.detail(id_=id_, p=p)


@router.post("", response_model=Accepted, status_code=202)
async def upload(body: Upload, request: Request, p: Auth) -> dict:
    return await document_files.upload(body=body, request=request, p=p)


@router.get("/versions/{id_}/preview", response_model=list[ChunkView])
async def preview(
    id_: UUID,
    p: Auth,
    offset: int = Query(default=0, ge=0, le=5000),
    limit: int = Query(default=25, ge=1, le=100),
) -> list[dict]:
    return await document_queries.preview(id_=id_, p=p, offset=offset, limit=limit)


@router.get("/citations/{id_}", response_model=ChunkView)
async def citation(id_: UUID, p: Auth) -> dict:
    return await document_queries.citation(id_=id_, p=p)


@router.post("/versions/{id_}/download-ticket", response_model=DownloadTicket)
async def ticket(id_: UUID, request: Request, p: Auth) -> dict:
    return await document_files.ticket(id_=id_, request=request, p=p)


@router.get("/versions/{id_}/download")
async def download(
    id_: UUID, request: Request, p: Auth, token: str = Query(max_length=2000)
) -> Response:
    return await document_files.download(id_=id_, request=request, p=p, token=token)


@router.get("/versions/{id_}/job", response_model=JobStatus)
async def job_status(id_: UUID, p: Auth) -> dict:
    return await document_queries.job_status(id_=id_, p=p)


@router.post("/versions/{id_}/reprocess", response_model=Accepted, status_code=202)
async def reprocess(id_: UUID, request: Request, p: Auth) -> dict:
    return await document_files.reprocess(id_=id_, request=request, p=p)


@router.post("/versions/{id_}/cancel", response_model=Result)
async def cancel(id_: UUID, request: Request, p: Auth) -> dict:
    return await document_lifecycle.cancel(id_=id_, request=request, p=p)


@router.patch("/{id_}/governance", response_model=DocumentView)
async def governance(id_: UUID, body: Governance, request: Request, p: Auth) -> dict:
    return await document_lifecycle.governance(id_=id_, body=body, request=request, p=p)


@router.delete("/{id_}", response_model=Result)
async def delete(id_: UUID, request: Request, p: Auth) -> dict:
    return await document_lifecycle.delete(id_=id_, request=request, p=p)


@router.post("/{id_}/purge", response_model=Result)
async def purge(id_: UUID, request: Request, p: Auth) -> dict:
    return await document_lifecycle.purge(id_=id_, request=request, p=p)


@router.post("/versions/{id_}/assessment-link", response_model=Result)
async def link(id_: UUID, body: EvidenceLink, request: Request, p: Auth) -> dict:
    return await document_lifecycle.link(id_=id_, body=body, request=request, p=p)


@router.get("/versions/{id_}/assessment-links", response_model=list[EvidenceReference])
async def evidence_references(id_: UUID, p: Auth) -> list[dict]:
    return await document_queries.evidence_references(id_=id_, p=p)
