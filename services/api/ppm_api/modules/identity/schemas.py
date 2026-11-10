from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator

Role = Literal["Admin", "Project Manager", "Viewer"]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Credentials(Input):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class EmailInput(Input):
    email: EmailStr


def nonblank(value: str) -> str:
    if not value.strip():
        raise ValueError("Use a nonempty name")
    return value.strip()


class RegistrationInput(EmailInput):
    organization_name: str = Field(min_length=1, max_length=120)
    normalize_name = field_validator("organization_name")(nonblank)


class OrganizationProfileInput(Input):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    industry: str | None = Field(default=None, max_length=120)
    website: HttpUrl | None = Field(default=None, max_length=500)
    normalize_name = field_validator("name")(nonblank)


class CompleteChallenge(Input):
    token: str = Field(min_length=32, max_length=128)
    password: str = Field(min_length=12, max_length=72)
    name: str = Field(min_length=1, max_length=120)

    @field_validator("password")
    @classmethod
    def password_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 UTF-8 bytes")
        return value


class ProfileInput(Input):
    name: str = Field(min_length=1, max_length=120)


class SwitchInput(Input):
    organization_id: UUID


class InviteInput(EmailInput):
    role: Role


class MemberInput(Input):
    role: Role
    active: bool


class Message(BaseModel):
    message: str


class CsrfResponse(BaseModel):
    csrf_token: str


class OrganizationView(BaseModel):
    id: UUID
    name: str
    role: Role


class AccountView(BaseModel):
    id: UUID
    email: str
    name: str
    organization_id: UUID | None
    role: Role | None
    organizations: list[OrganizationView]


class MemberView(BaseModel):
    user_id: UUID
    email: str
    name: str
    role: Role
    active: bool
    revision: int


class MembersView(BaseModel):
    items: list[MemberView]
    next_cursor: str | None = None
    as_of: datetime


class SessionView(BaseModel):
    id: UUID
    created_at: datetime
    expires_at: datetime
    current: bool


class SessionsView(BaseModel):
    items: list[SessionView]


class AuditView(BaseModel):
    id: UUID
    action: str
    actor_id: UUID
    target_id: UUID | None
    created_at: datetime
    request_id: UUID


class AuditsView(BaseModel):
    items: list[AuditView]
    next_cursor: str | None = None
    as_of: datetime
