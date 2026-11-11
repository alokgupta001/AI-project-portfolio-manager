"""Assessment write authorization, idempotent replay, revisions and audit recording."""

from __future__ import annotations

import hashlib
from functools import wraps
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from ppm_api.modules.assessments import tables as T
from ppm_api.modules.assessments.access import command_access, oid
from ppm_api.modules.delivery.service import fail, lock
from ppm_api.modules.identity.service import now, record


def mutation(fn: Any) -> Any:

    @wraps(fn)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        p, request = (kwargs["p"], kwargs["request"])
        await lock(p, request)
        await command_access(p, request)
        try:
            key = UUID(request.headers.get("idempotency-key", ""))
        except ValueError:
            fail(428, "A UUID Idempotency-Key is required")
        body = await request.body()
        fingerprint = hashlib.sha256(
            request.method.encode()
            + request.url.path.encode()
            + body
            + request.headers.get("if-match", "").encode()
        ).hexdigest()
        old = (
            (
                await p.conn.execute(
                    sa.select(T.assessment_requests).where(
                        T.assessment_requests.c.organization_id == oid(p),
                        T.assessment_requests.c.user_id == p.user["id"],
                        T.assessment_requests.c.key == key,
                    )
                )
            )
            .mappings()
            .first()
        )
        if old:
            if old["fingerprint"] != fingerprint:
                fail(409, "Idempotency key already used for a different request")
            return old["response"]
        try:
            result = await fn(*args, **kwargs)
        except ValidationError as exc:
            fail(422, str(exc.errors(include_input=False)))
        except IntegrityError:
            fail(409, "Conflicting record or invalid scoped reference")
        encoded = jsonable_encoder(result)
        await p.conn.execute(
            T.assessment_requests.insert().values(
                id=uuid4(),
                organization_id=oid(p),
                created_at=now(),
                user_id=p.user["id"],
                key=key,
                fingerprint=fingerprint,
                response=encoded,
            )
        )
        await record(p.conn, request, p.user["id"], oid(p), "assessment." + fn.__name__)
        return result

    return wrapped


def revision(request: Request, row: Any) -> Any:
    supplied = request.headers.get("if-match")
    if supplied is None:
        fail(428, "If-Match revision is required")
    if supplied != str(row["revision"]):
        fail(412, "This record changed. Reload before saving")
