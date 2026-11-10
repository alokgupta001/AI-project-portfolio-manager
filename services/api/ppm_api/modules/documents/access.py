"""Tenant/project-scoped source lookup and document write eligibility."""

from uuid import UUID

import sqlalchemy as sa

from ppm_api.modules.assessments.access import oid
from ppm_api.modules.delivery.service import can_edit, fail
from ppm_api.modules.delivery.service import get as delivery_get
from ppm_api.modules.documents import tables as T
from ppm_api.modules.identity.service import Principal


async def document(p: Principal, id_: UUID, deleted: bool = False) -> dict:
    row = (
        (
            await p.conn.execute(
                sa.select(T.documents).where(
                    T.documents.c.id == id_, T.documents.c.organization_id == oid(p)
                )
            )
        )
        .mappings()
        .first()
    )
    if not row or (row["deleted_at"] and not deleted):
        fail(404, "Source unavailable")
    if row["project_id"]:
        await delivery_get(p, "projects", row["project_id"], True)
    return dict(row)


async def version(p: Principal, id_: UUID, deleted: bool = False) -> tuple[dict, dict]:
    row = (
        (await p.conn.execute(sa.select(T.versions).where(T.versions.c.id == id_)))
        .mappings()
        .first()
    )
    if not row:
        fail(404, "Source unavailable")
    return dict(row), await document(p, row["document_id"], deleted)


async def writable(p: Principal, d: dict) -> None:
    if p.role == "Viewer" or (
        p.role != "Admin" and (not d["project_id"] or not await can_edit(p, d["project_id"]))
    ):
        fail(
            403, "Document changes require project edit scope; organization policies require Admin"
        )
