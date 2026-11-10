"""HTTP adapters; business operations belong to the feature service."""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Header, Request, Response

from ppm_api.modules.identity import service as _operations
from ppm_api.modules.identity.schemas import (
    AccountView,
    AuditsView,
    CompleteChallenge,
    Credentials,
    CsrfResponse,
    EmailInput,
    InviteInput,
    MemberInput,
    MembersView,
    MemberView,
    Message,
    OrganizationProfileInput,
    ProfileInput,
    RegistrationInput,
    SessionsView,
    SwitchInput,
)
from ppm_api.modules.identity.service import AccountAuth, Auth

router = APIRouter(prefix="/api/v1", tags=["Identity"])


@router.get("/auth/csrf", response_model=CsrfResponse)
async def csrf(request: Request, response: Response) -> dict[str, str]:
    return await _operations.csrf(request=request, response=response)


@router.post("/auth/login", response_model=AccountView)
async def login(body: Credentials, request: Request, response: Response) -> dict[str, Any]:
    return await _operations.login(body=body, request=request, response=response)


@router.post("/auth/refresh", response_model=Message)
async def refresh(request: Request, response: Response) -> dict[str, str]:
    return await _operations.refresh(request=request, response=response)


@router.get("/auth/me", response_model=AccountView)
async def me(p: AccountAuth) -> dict[str, Any]:
    return await _operations.me(p=p)


@router.patch("/auth/profile", response_model=Message)
async def profile(body: ProfileInput, request: Request, p: AccountAuth) -> dict[str, str]:
    return await _operations.profile(body=body, request=request, p=p)


@router.post("/auth/switch", response_model=AccountView)
async def switch(
    body: SwitchInput, request: Request, response: Response, p: AccountAuth
) -> dict[str, Any]:
    return await _operations.switch(body=body, request=request, response=response, p=p)


@router.post("/auth/logout", response_model=Message)
async def logout(request: Request, response: Response, p: AccountAuth) -> dict[str, str]:
    return await _operations.logout(request=request, response=response, p=p)


@router.get("/auth/sessions", response_model=SessionsView)
async def list_sessions(p: AccountAuth) -> dict[str, Any]:
    return await _operations.list_sessions(p=p)


@router.delete("/auth/sessions/{session_id}", response_model=Message)
async def revoke(session_id: UUID, request: Request, p: AccountAuth) -> dict[str, str]:
    return await _operations.revoke(session_id=session_id, request=request, p=p)


@router.post("/auth/reset-request", response_model=Message)
async def reset_request(body: EmailInput, request: Request) -> dict[str, str]:
    return await _operations.reset_request(body=body, request=request)


@router.post("/auth/complete", response_model=Message)
async def complete(body: CompleteChallenge, request: Request) -> dict[str, str]:
    return await _operations.complete(body=body, request=request)


@router.get("/organization/members", response_model=MembersView)
async def member_list(p: Auth, after: UUID | None = None) -> dict[str, Any]:
    return await _operations.member_list(p=p, after=after)


@router.post("/organization/invitations", response_model=Message, status_code=201)
async def invite(body: InviteInput, request: Request, p: Auth) -> dict[str, str]:
    return await _operations.invite(body=body, request=request, p=p)


@router.patch("/organization/members/{user_id}", response_model=MemberView)
async def change_member(
    user_id: UUID,
    body: MemberInput,
    request: Request,
    p: Auth,
    if_match: Annotated[str | None, Header()] = None,
) -> dict[str, Any]:
    return await _operations.change_member(
        user_id=user_id, body=body, request=request, p=p, if_match=if_match
    )


@router.get("/organization/audit", response_model=AuditsView)
async def audit_list(p: Auth, after: UUID | None = None) -> dict[str, Any]:
    return await _operations.audit_list(p=p, after=after)


@router.post("/auth/register", response_model=Message)
async def register(body: RegistrationInput, request: Request) -> dict[str, str]:
    return await _operations.register(body=body, request=request)


@router.get("/organization/profile", response_model=dict)
async def organization_profile(p: Auth) -> dict:
    return await _operations.organization_profile(p=p)


@router.patch("/organization/profile", response_model=Message)
async def edit_organization(
    body: OrganizationProfileInput,
    request: Request,
    p: Auth,
    if_match: Annotated[int | None, Header()] = None,
) -> dict:
    return await _operations.edit_organization(body=body, request=request, p=p, if_match=if_match)


@router.get("/organization/invitations", response_model=list[dict])
async def invitation_list(p: Auth) -> list[dict]:
    return await _operations.invitation_list(p=p)


@router.post("/organization/invitations/{invitation_id}/{operation}", response_model=Message)
async def invitation_action(invitation_id: UUID, operation: str, request: Request, p: Auth) -> dict:
    return await _operations.invitation_action(
        invitation_id=invitation_id, operation=operation, request=request, p=p
    )
