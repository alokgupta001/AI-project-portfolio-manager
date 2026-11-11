"""Tenant-scoped assessment access, named responsibilities and live write checks."""

from __future__ import annotations

from typing import Any
from uuid import UUID

import sqlalchemy as sa
from fastapi import Request

from ppm_api.modules.assessments import tables as T
from ppm_api.modules.delivery.service import fail
from ppm_api.modules.identity.service import Principal


def oid(p: Principal) -> Any:
    return p.session["organization_id"]


async def get(p: Principal, table: Any, id_: Any) -> Any:
    row = (
        (
            await p.conn.execute(
                sa.select(table).where(table.c.id == id_, table.c.organization_id == oid(p))
            )
        )
        .mappings()
        .first()
    )
    if row is None:
        fail(404, "Record not found or access restricted")
    return row


async def grant(p: Principal, field: Any, id_: Any) -> Any:
    return bool(
        await p.conn.scalar(
            sa.select(T.assessment_access.c.id)
            .where(
                T.assessment_access.c.organization_id == oid(p),
                T.assessment_access.c.user_id == p.user["id"],
                T.assessment_access.c[field] == id_,
                T.assessment_access.c.active,
            )
            .limit(1)
        )
    )


async def can_edit(p: Principal, id_: Any) -> Any:
    return p.role == "Admin" or (
        p.role == "Project Manager" and await grant(p, "framework_id", id_)
    )


def eligible(p: Principal) -> Any:
    if p.role not in ("Admin", "Project Manager"):
        fail(403, "An eligible assessment role is required")


def respondent(p: Principal, a: Any) -> Any:
    eligible(p)
    if p.user["id"] != a["assigned_to"]:
        fail(403, "Only the assigned respondent can answer or submit")


def reviewer(p: Principal, a: Any) -> Any:
    eligible(p)
    if p.user["id"] != a["reviewer_id"] or p.user["id"] in (a["assigned_to"], a["submitted_by"]):
        fail(403, "Only the assigned independent reviewer can review")


def evidence_access(p: Principal, a: Any) -> Any:
    if p.role != "Admin" and (
        p.role != "Project Manager" or p.user["id"] not in (a["assigned_to"], a["reviewer_id"])
    ):
        fail(403, "Result access does not grant access to private answers or evidence")


async def command_access(p: Principal, request: Request) -> Any:
    """Recheck live scope even on idempotent replays."""
    eligible(p)
    path = request.url.path
    params = request.path_params
    if "assessment_id" in params:
        a = await get(p, T.assessments, UUID(str(params["assessment_id"])))
        if path.endswith("/review") or path.endswith("/release"):
            reviewer(p, a)
        else:
            respondent(p, a)
    elif "framework_id" in params:
        fid = UUID(str(params["framework_id"]))
        await get(p, T.frameworks, fid)
        if not await can_edit(p, fid) or (path.endswith("/publish") and p.role != "Admin"):
            fail(403, "Framework edit/publish access required")
    elif p.role != "Admin":
        fail(403, "Administration requires Admin")
