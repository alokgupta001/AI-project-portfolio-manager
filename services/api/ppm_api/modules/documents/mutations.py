"""Document revision preconditions and shared idempotency fingerprints."""

import hashlib
from typing import Any
from uuid import UUID

from fastapi import Request
from fastapi.encoders import jsonable_encoder

from ppm_api.modules.delivery.service import fail


def revision(request: Request, d: dict) -> None:
    value = request.headers.get("if-match")
    if value is None:
        fail(428, "Reload the document before editing")
    if value != str(d["revision"]):
        fail(412, "Document changed; reload before editing")


def request_identity(request: Request, body: Any) -> tuple[str, str]:
    try:
        key = str(UUID(request.headers.get("idempotency-key", "")))
    except ValueError:
        fail(428, "A UUID Idempotency-Key is required")
    canonical = str(request.url.path) + str(jsonable_encoder(body))
    return key, hashlib.sha256(canonical.encode()).hexdigest()
