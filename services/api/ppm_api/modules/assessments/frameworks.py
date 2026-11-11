"""Framework authoring, immutable versions, examples and response loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import Request

from ppm_api.modules.assessments import tables as T
from ppm_api.modules.assessments.access import can_edit, get, oid
from ppm_api.modules.assessments.mutations import revision
from ppm_api.modules.assessments.schemas import FrameworkInput
from ppm_api.modules.assessments.validation import validate_definition
from ppm_api.modules.delivery.service import fail
from ppm_api.modules.identity.service import Principal, now

EXAMPLE_FRAMEWORKS = json.loads(
    Path(__file__).with_name("examples.json").read_text(encoding="utf-8")
)


async def fw_view(p: Principal, row: Any) -> Any:
    ver = await p.conn.scalar(
        sa.select(sa.func.max(T.framework_versions.c.version)).where(
            T.framework_versions.c.framework_id == row["id"]
        )
    )
    return dict(
        **row["definition"],
        id=row["id"],
        revision=row["revision"],
        published_version=ver,
        can_edit=await can_edit(p, row["id"]),
    )


async def list_frameworks(p: Principal, offset: int, limit: int) -> Any:
    rows = (
        await p.conn.execute(
            sa.select(T.frameworks)
            .order_by(T.frameworks.c.created_at, T.frameworks.c.id)
            .offset(offset)
            .limit(limit)
        )
    ).mappings()
    return [await fw_view(p, r) for r in rows]


async def create_framework(payload: FrameworkInput, p: Principal) -> Any:
    row = (
        (
            await p.conn.execute(
                T.frameworks.insert()
                .values(
                    id=uuid4(),
                    organization_id=oid(p),
                    created_at=now(),
                    revision=1,
                    definition=payload.model_dump(mode="json"),
                )
                .returning(T.frameworks)
            )
        )
        .mappings()
        .one()
    )
    return await fw_view(p, row)


async def edit_framework(
    framework_id: UUID, payload: FrameworkInput, request: Request, p: Principal
) -> Any:
    old = await get(p, T.frameworks, framework_id)
    revision(request, old)
    row = (
        (
            await p.conn.execute(
                T.frameworks.update()
                .where(T.frameworks.c.id == framework_id)
                .values(revision=old["revision"] + 1, definition=payload.model_dump(mode="json"))
                .returning(T.frameworks)
            )
        )
        .mappings()
        .one()
    )
    return await fw_view(p, row)


async def publish_framework(framework_id: UUID, request: Request, p: Principal) -> Any:
    fw = await get(p, T.frameworks, framework_id)
    revision(request, fw)
    if fw["definition"]["archived"]:
        fail(409, "Archived frameworks cannot be published")
    validate_definition(fw["definition"])
    ver = await p.conn.scalar(
        sa.select(sa.func.coalesce(sa.func.max(T.framework_versions.c.version), 0)).where(
            T.framework_versions.c.framework_id == framework_id
        )
    )
    row = (
        (
            await p.conn.execute(
                T.framework_versions.insert()
                .values(
                    id=uuid4(),
                    organization_id=oid(p),
                    created_at=now(),
                    framework_id=framework_id,
                    version=ver + 1,
                    snapshot=fw["definition"],
                    published_by=p.user["id"],
                )
                .returning(T.framework_versions)
            )
        )
        .mappings()
        .one()
    )
    await p.conn.execute(
        T.frameworks.update()
        .where(T.frameworks.c.id == framework_id)
        .values(revision=fw["revision"] + 1)
    )
    return dict(row)


async def list_framework_versions(framework_id: UUID, p: Principal) -> Any:
    await get(p, T.frameworks, framework_id)
    return [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(T.framework_versions)
                .where(T.framework_versions.c.framework_id == framework_id)
                .order_by(T.framework_versions.c.version.desc())
            )
        ).mappings()
    ]


async def seed_examples(p: Principal) -> Any:
    out = []
    for original in EXAMPLE_FRAMEWORKS:
        data = json.loads(json.dumps(original))
        for d in data["dimensions"]:
            for q in d["questions"]:
                q["rubric_levels"] = q.pop("levels", [])
        payload = FrameworkInput.model_validate(data)
        old = (
            (
                await p.conn.execute(
                    sa.select(T.frameworks).where(
                        T.frameworks.c.definition["name"].astext == payload.name
                    )
                )
            )
            .mappings()
            .first()
        )
        if old is None:
            old = (
                (
                    await p.conn.execute(
                        T.frameworks.insert()
                        .values(
                            id=uuid4(),
                            organization_id=oid(p),
                            created_at=now(),
                            revision=1,
                            definition=payload.model_dump(mode="json"),
                        )
                        .returning(T.frameworks)
                    )
                )
                .mappings()
                .one()
            )
        out.append(await fw_view(p, old))
    return out
