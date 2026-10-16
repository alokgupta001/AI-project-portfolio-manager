"""Protected source tools and bounded exact hybrid ranking through the Sprint 09 seam."""

import hashlib
import math
from typing import Literal
from uuid import UUID

import sqlalchemy as sa

from ppm_api import document_tables as D
from ppm_api.ai_provider import ProviderError
from ppm_api.ai_schemas import AIOutput
from ppm_api.delivery import fail, get
from ppm_api.document_retrieval import EmbeddingRequest
from ppm_api.document_schemas import Strict
from ppm_api.documents import citation, search, version
from ppm_api.identity import Principal


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class SourceTool(Strict):
    tool: Literal["keyword", "hybrid", "index"]
    project_id: UUID


async def authorize_tool(p: Principal, tool: SourceTool, project_id: UUID) -> None:
    # Never accept model-selected scope or tool names. RLS remains the second boundary.
    if tool.project_id != project_id:
        fail(403, "Tool scope is immutable")
    await get(p, "projects", project_id, True)


def snapshot(row: dict, sha256: str | None = None) -> dict[str, str]:
    return dict(
        chunk_id=str(row["id"]),
        version_id=str(row["version_id"]),
        sha256=sha256 or row["sha256"],
        text_sha256=digest(row["text"]),
    )


async def keyword(p: Principal, project_id: UUID, query: str) -> list[dict]:
    await authorize_tool(p, SourceTool(tool="keyword", project_id=project_id), project_id)
    return (await search(p, query, project_id, 5))["items"]


async def validate_snapshot(p: Principal, refs: list[dict]) -> list[dict]:
    rows = []
    for ref in refs:
        chunk = await citation(UUID(ref["chunk_id"]), p)
        v, _ = await version(p, chunk["version_id"])
        if (
            str(chunk["version_id"]) != ref["version_id"]
            or v["sha256"] != ref["sha256"]
            or digest(chunk["text"]) != ref["text_sha256"]
        ):
            raise ProviderError("EVIDENCE_CHANGED")
        rows.append(chunk | {"sha256": v["sha256"]})
    return rows


async def index_chunks(
    p: Principal, project_id: UUID, id_: UUID
) -> tuple[EmbeddingRequest, list[dict]]:
    await authorize_tool(p, SourceTool(tool="index", project_id=project_id), project_id)
    v, d = await version(p, id_)
    if d["project_id"] != project_id:
        fail(404, "Source unavailable")
    rows = list(
        (
            await p.conn.execute(
                sa.select(D.chunks)
                .where(D.chunks.c.version_id == id_)
                .order_by(D.chunks.c.ordinal)
                .limit(21)
            )
        ).mappings()
    )
    if not rows or len(rows) > 20:
        fail(422, "Index requests require 1–20 chunks; larger sources remain keyword searchable")
    for row in rows:
        await citation(row["id"], p)
    request = EmbeddingRequest(
        organization_id=p.session["organization_id"],
        project_id=project_id,
        version_id=id_,
        sha256=v["sha256"],
        chunk_ids=[r["id"] for r in rows],
    )
    return request, [dict(row) | {"sha256": v["sha256"]} for row in rows]


def cosine(left: list[float], right: list[float]) -> float:
    denominator = math.sqrt(sum(v * v for v in left)) * math.sqrt(sum(v * v for v in right))
    return sum(a * b for a, b in zip(left, right, strict=True)) / denominator if denominator else 0


def merge(keyword_rows: list[dict], semantic_rows: list[dict]) -> list[dict]:
    # Reciprocal rank fusion: source scores of different units are never added directly.
    rows: dict[str, dict] = {}
    scores: dict[str, float] = {}
    for branch in (keyword_rows, semantic_rows):
        for rank, row in enumerate(branch, 1):
            key = str(row["id"])
            rows[key] = row
            scores[key] = scores.get(key, 0.0) + 1 / (60 + rank)
    return [rows[key] for key in sorted(rows, key=lambda key: (-scores[key], key))[:5]]


def evaluate(output: AIOutput, rows: list[dict]) -> list[dict[str, str]]:
    """Extractive support gate: the full current chunk is the only publishable statement."""
    if (output.status == "supported") != bool(output.excerpts):
        raise ProviderError("OUTPUT_UNSUPPORTED")
    known = {str(row["id"]): row for row in rows}
    seen = set()
    refs = []
    for excerpt in output.excerpts:
        key = str(excerpt.chunk_id)
        row = known.get(key)
        if not row or key in seen or excerpt.quote != row["text"]:
            # Includes every unsupported numerical assertion; no fuzzy text/number matching.
            raise ProviderError("OUTPUT_UNSUPPORTED")
        seen.add(key)
        refs.append(snapshot(row))
    return refs
