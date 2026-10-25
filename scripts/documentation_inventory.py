"""Refresh source inventories without settings, application lifespan or database access."""

import argparse
import ast
import json
import sys
from pathlib import Path

from sqlalchemy.dialects import postgresql

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services/api"))

from ppm_api.database import Base  # noqa: E402
from ppm_api.main import create_app  # noqa: E402
from ppm_api.schemas import SCHEMA_REVISION  # noqa: E402


def cell(value: object) -> str:
    return str(value).replace("|", "&#124;").replace("\n", " ")


def inventories() -> dict[str, str]:
    schema = create_app().openapi()
    committed = json.loads((ROOT / "packages/contracts/openapi.json").read_text(encoding="utf-8"))
    if schema != committed:
        raise SystemExit("OpenAPI differs from committed contract; generate contracts first")
    api = [
        "# API reference — actual current routes",
        "",
        "Generated from `main.create_app().openapi()` without lifespan, settings secrets, "
        "database or provider access. Run `python scripts/documentation_inventory.py` to refresh "
        "or add `--check` for drift. The generated schema equals the committed OpenAPI.",
        "",
        "## Authentication, validation and errors",
        "",
        "Routes use live cookie/session/membership checks, organization RLS and owning-domain "
        "permissions. Mutations require CSRF/Origin except explicitly signed provider hooks. "
        "OpenAPI does not enumerate grants or privacy rules: read the "
        "[permission contract](../contracts/permissions.md) and "
        "[document contract](../contracts/documents.md). Ownership grants no access. "
        "`main.error_response` returns sanitized code/message/request_id/details. "
        "Revisions, idempotency, rate limits and dependency failures remain handler-specific.",
        "",
        "Document original downloads additionally need a 60-second signed ticket and current "
        "authenticated authority; source bytes are SHA-256 verified. See "
        "[the practical trace](../02-learning/06-ai-and-analytics/DOCUMENT_SOURCES.md).",
        "",
        "## Route inventory",
        "",
        "| Method and path | Actual handler | Parameters / validation | Request body | Responses |",
        "| --- | --- | --- | --- | --- |",
    ]
    operations = 0
    for path, item in sorted(schema["paths"].items()):
        for method, op in item.items():
            if method not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                continue
            operations += 1
            # FastAPI operationId includes the actual endpoint name before the path suffix.
            name = op["operationId"].split("_api_v1_", 1)[0]
            params = "; ".join(
                f"{p['name']} ({p['in']}{', required' if p.get('required') else ''}): "
                + json.dumps(p.get("schema", {}), ensure_ascii=False)
                for p in op.get("parameters", [])
            )
            body = "; ".join(
                f"{mime}: {json.dumps(content.get('schema', {}), ensure_ascii=False)}"
                for mime, content in op.get("requestBody", {}).get("content", {}).items()
            )
            responses = "; ".join(
                f"{code}: {json.dumps(response.get('content', {}), ensure_ascii=False)}"
                for code, response in op["responses"].items()
            )
            api.append(
                "| "
                + " | ".join(
                    cell(x)
                    for x in (
                        f"`{method.upper()} {path}`",
                        f"`{name}`",
                        params or "—",
                        body or "—",
                        responses,
                    )
                )
                + " |"
            )
    api.extend(["", f"**Inventory:** {operations} operations across {len(schema['paths'])} paths."])
    db = [
        "# Current source-derived database dictionary",
        "",
        "Generated from SQLAlchemy `Base.metadata` without a database connection; "
        "SQL types use the PostgreSQL dialect. Source chain "
        f"ends at `{SCHEMA_REVISION}`; the normal applied head and preservation evidence "
        "are independently recorded in the [latest handoff](../handoffs/LATEST.md). "
        "Run `python scripts/documentation_inventory.py --check` for drift. "
        "SQL-only RLS, triggers, privileges and security-definer functions require reading "
        "[the migrations](../../services/api/migrations/versions) and "
        "[document contract](../contracts/documents.md); "
        "metadata is not a complete policy inventory.",
        "",
        "## Important data flows",
        "",
        "Live organization membership → transaction-local principal/RLS → scoped domain facts. "
        "Published assessment history remains immutable. `source_documents` owns scope/retention; "
        "`source_versions` owns immutable byte identity and mutable processing status; "
        "`source_chunks` is replaceable derived text; "
        "`source_evidence_links` references separately "
        "authorized released attachments. `durable_jobs` references exactly one integration, "
        "document version, AI run or local ML run according to job kind. "
        "Connector principals, source conflicts, immutable histories/datasets and CPU "
        "run lineage follow the [local baseline contract](../contracts/ml.md). "
        "AI run provenance/budgets, "
        "attempt accounting and rebuildable vectors follow the [AI contract](../contracts/ai.md). "
        "Originals remain private objects; logical deletion "
        "revokes reads, guarded purge removes bytes/text/links but retains tombstones. "
        "`ai_embeddings` stores the bounded exact JSONB projection; no pgvector/ANN "
        "or semantic-finding table is activated.",
        "",
        f"**Inventory:** {len(Base.metadata.tables)} metadata tables "
        "(Alembic's runtime version table is separate).",
    ]
    for table in sorted(Base.metadata.tables.values(), key=lambda t: t.name):
        db.extend(
            [
                "",
                f"## {table.name}",
                "",
                "| Column | SQL type | Nullable | Primary key | Foreign reference |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for col in table.columns:
            db.append(
                "| "
                + " | ".join(
                    cell(x)
                    for x in (
                        f"`{col.name}`",
                        f"`{col.type.compile(dialect=postgresql.dialect())}`",
                        col.nullable,
                        col.primary_key,
                        ", ".join(sorted(fk.target_fullname for fk in col.foreign_keys)) or "—",
                    )
                )
                + " |"
            )
        db.append("")
        constraint_rows = []
        for constraint in table.constraints:
            expression = getattr(constraint, "sqltext", None)
            detail = (
                str(expression)
                if expression is not None
                else ", ".join(col.name for col in constraint.columns)
            )
            constraint_rows.append(
                f"- {type(constraint).__name__} ({constraint.name or 'unnamed'}): {cell(detail)}"
            )
        db.extend(sorted(constraint_rows))
        for index in sorted(table.indexes, key=lambda i: i.name or ""):
            db.append(
                f"- Index `{index.name}` (unique={index.unique}): "
                + cell(", ".join(str(e) for e in index.expressions))
            )
    code = [
        "# Current code and test navigation",
        "",
        "Source-derived AST inventory. Search symbols instead of relying on line numbers; a test "
        "definition is not an executed result. Run "
        "`python scripts/documentation_inventory.py --check` "
        "for drift. Actual results: "
        "[Sprint 10 checks](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md) and "
        "[Gemini follow-up](../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md).",
    ]
    paths = sorted(
        p
        for directory in ("services", "scripts", "tests")
        for p in (ROOT / directory).rglob("*.py")
        if "__pycache__" not in p.parts
    )
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        symbols = sorted(
            (
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            ),
            key=lambda n: n.lineno,
        )
        if not symbols:
            continue
        relative = path.relative_to(ROOT).as_posix()
        code.extend(["", f"## {relative}", "", f"[Source](../../{relative})", ""])
        code.extend(f"- `{node.name}` — line {node.lineno}" for node in symbols)
    return {
        "docs/01-architecture/18-api-contracts.md": "\n".join(api) + "\n",
        "docs/01-architecture/DATABASE-DICTIONARY.md": "\n".join(db) + "\n",
        "docs/10-reference/CODE-AND-TEST-INDEX.md": "\n".join(code) + "\n",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    mismatches = []
    for relative, content in inventories().items():
        path = ROOT / relative
        if args.check:
            if path.read_text(encoding="utf-8") != content:
                mismatches.append(relative)
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    if mismatches:
        raise SystemExit("Stale documentation inventories: " + ", ".join(mismatches))
    print("PASS: three source inventories " + ("match" if args.check else "refreshed"))


if __name__ == "__main__":
    main()
