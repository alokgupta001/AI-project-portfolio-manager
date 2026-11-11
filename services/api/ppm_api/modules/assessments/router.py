"""Versioned assessment workflows with scoped access and deterministic scoring."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Query, Request
from fastapi.routing import APIRoute

from ppm_api.modules.assessments import evidence as assessment_evidence
from ppm_api.modules.assessments import frameworks as assessment_frameworks
from ppm_api.modules.assessments import service as assessment_service
from ppm_api.modules.assessments.mutations import mutation
from ppm_api.modules.assessments.schemas import (
    AccessInput,
    ActionInput,
    AnswerBatchInput,
    AssessmentDetail,
    AssessmentRecord,
    AssignmentInput,
    EventRecord,
    EvidenceInput,
    EvidenceRecord,
    FrameworkInput,
    FrameworkRecord,
    ReviewInput,
    VersionRecord,
)
from ppm_api.modules.delivery.service import fail
from ppm_api.modules.identity.service import Auth


class BoundedRoute(APIRoute):
    def get_route_handler(self) -> Any:
        original = super().get_route_handler()

        async def bounded(request: Request) -> Any:
            if request.method not in ("GET", "HEAD", "OPTIONS"):
                chunks = []
                size = 0
                async for chunk in request.stream():
                    size += len(chunk)
                    if size > 2097152:
                        fail(413, "Assessment request exceeds 2 MiB")
                    chunks.append(chunk)
                request._body = b"".join(chunks)
            return await original(request)

        return bounded


router = APIRouter(prefix="/api/v1/assessment", tags=["Assessment"], route_class=BoundedRoute)


@router.get("/frameworks", response_model=list[FrameworkRecord])
async def list_frameworks(
    p: Auth, offset: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100)
) -> Any:
    return await assessment_frameworks.list_frameworks(p=p, offset=offset, limit=limit)


@router.post("/frameworks", response_model=FrameworkRecord, status_code=201)
@mutation
async def create_framework(payload: FrameworkInput, request: Request, p: Auth) -> Any:
    return await assessment_frameworks.create_framework(payload=payload, p=p)


@router.put("/frameworks/{framework_id}", response_model=FrameworkRecord)
@mutation
async def edit_framework(
    framework_id: UUID, payload: FrameworkInput, request: Request, p: Auth
) -> Any:
    return await assessment_frameworks.edit_framework(
        framework_id=framework_id, payload=payload, request=request, p=p
    )


@router.post("/frameworks/{framework_id}/publish", response_model=VersionRecord, status_code=201)
@mutation
async def publish_framework(
    framework_id: UUID, payload: ActionInput, request: Request, p: Auth
) -> Any:
    return await assessment_frameworks.publish_framework(
        framework_id=framework_id, request=request, p=p
    )


@router.get("/frameworks/{framework_id}/versions", response_model=list[VersionRecord])
async def versions(framework_id: UUID, p: Auth) -> Any:
    return await assessment_frameworks.list_framework_versions(framework_id=framework_id, p=p)


@router.post("/seed-examples", response_model=list[FrameworkRecord], status_code=201)
@mutation
async def seed_examples(request: Request, p: Auth) -> Any:
    return await assessment_frameworks.seed_examples(p=p)


@router.post("/access", response_model=AccessInput)
@mutation
async def set_access(payload: AccessInput, request: Request, p: Auth) -> Any:
    return await assessment_service.set_access_grant(payload=payload, p=p)


@router.post("/assessments", response_model=AssessmentRecord, status_code=201)
@mutation
async def assign(payload: AssignmentInput, request: Request, p: Auth) -> Any:
    return await assessment_service.assign_assessment(payload=payload, p=p)


@router.get("/assessments", response_model=list[AssessmentRecord])
async def list_assessments(
    p: Auth,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    framework_version_id: UUID | None = None,
    q: str = Query("", max_length=160),
) -> Any:
    return await assessment_service.list_assessments(
        p=p, offset=offset, limit=limit, framework_version_id=framework_version_id, q=q
    )


@router.get("/assessments/{assessment_id}", response_model=AssessmentDetail)
async def detail(assessment_id: UUID, p: Auth) -> Any:
    return await assessment_service.get_assessment(assessment_id=assessment_id, p=p)


@router.put("/assessments/{assessment_id}/answers", response_model=AssessmentDetail)
@mutation
async def save_answers(
    assessment_id: UUID, payload: AnswerBatchInput, request: Request, p: Auth
) -> Any:
    return await assessment_service.save_answers(
        assessment_id=assessment_id, payload=payload, request=request, p=p
    )


@router.post("/assessments/{assessment_id}/submit", response_model=AssessmentRecord)
@mutation
async def submit(assessment_id: UUID, payload: ActionInput, request: Request, p: Auth) -> Any:
    return await assessment_service.submit_assessment(
        assessment_id=assessment_id, payload=payload, request=request, p=p
    )


@router.post("/assessments/{assessment_id}/review", response_model=AssessmentRecord)
@mutation
async def review(assessment_id: UUID, payload: ReviewInput, request: Request, p: Auth) -> Any:
    return await assessment_service.review_assessment(
        assessment_id=assessment_id, payload=payload, request=request, p=p
    )


@router.get("/assessments/{assessment_id}/events", response_model=list[EventRecord])
async def history(assessment_id: UUID, p: Auth) -> Any:
    return await assessment_service.list_assessment_events(assessment_id=assessment_id, p=p)


@router.get("/assessments/{assessment_id}/evidence", response_model=list[EvidenceRecord])
async def evidence_list(assessment_id: UUID, p: Auth) -> Any:
    return await assessment_evidence.list_evidence(assessment_id=assessment_id, p=p)


@router.post(
    "/assessments/{assessment_id}/evidence", response_model=EvidenceRecord, status_code=201
)
@mutation
async def upload(assessment_id: UUID, payload: EvidenceInput, request: Request, p: Auth) -> Any:
    return await assessment_evidence.upload_evidence(
        assessment_id=assessment_id, payload=payload, request=request, p=p
    )


@router.get("/assessments/{assessment_id}/evidence/{evidence_id}")
async def download(assessment_id: UUID, evidence_id: UUID, request: Request, p: Auth) -> Any:
    return await assessment_evidence.download_evidence(
        assessment_id=assessment_id, evidence_id=evidence_id, request=request, p=p
    )


@router.delete("/assessments/{assessment_id}/evidence/{evidence_id}", response_model=ActionInput)
@mutation
async def delete_evidence(assessment_id: UUID, evidence_id: UUID, request: Request, p: Auth) -> Any:
    return await assessment_evidence.delete_evidence(
        assessment_id=assessment_id, evidence_id=evidence_id, request=request, p=p
    )


@router.get(
    "/assessments/{assessment_id}/evidence/{evidence_id}/preview", response_model=dict[str, str]
)
async def preview_evidence(
    assessment_id: UUID, evidence_id: UUID, request: Request, p: Auth
) -> dict:
    return await assessment_evidence.preview_evidence(
        assessment_id=assessment_id, evidence_id=evidence_id, request=request, p=p
    )


@router.post(
    "/assessments/{assessment_id}/evidence/{evidence_id}/release", response_model=EvidenceRecord
)
@mutation
async def release_evidence(
    assessment_id: UUID, evidence_id: UUID, payload: ActionInput, request: Request, p: Auth
) -> dict:
    return await assessment_evidence.release_evidence(
        assessment_id=assessment_id, evidence_id=evidence_id, payload=payload, request=request, p=p
    )


@router.get("/access", response_model=list[dict])
async def access_list(
    p: Auth, framework_id: UUID | None = None, assessment_id: UUID | None = None
) -> Any:
    return await assessment_service.list_access_grants(
        p=p, framework_id=framework_id, assessment_id=assessment_id
    )
