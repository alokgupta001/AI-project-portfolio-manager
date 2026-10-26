"""Bounded adapters. Credentials are resolved only by workers; redirects are denied."""

import asyncio
import csv
import hashlib
import io
import ipaddress
import json
import os
import re
import socket
from datetime import UTC, datetime
from typing import Any, Literal
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ppm_api.ppm_schemas import SprintInput, WorkInput


class ConnectorConfig(BaseModel):
    source_namespace: str = Field(
        default="manual", min_length=1, max_length=80, pattern=r"^[A-Za-z0-9_.-]+$"
    )
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=160)
    provider: Literal["csv", "github", "jira"]
    mode: Literal["fixture", "live"] = "fixture"
    project_id: UUID
    resource: str = Field(default="", max_length=160)
    jira_project: str = Field(default="", pattern=r"^[A-Z0-9_]*$")
    board_id: int | None = Field(default=None, gt=0)
    team_id: UUID | None = None
    entity: Literal["issues", "pulls", "sprints"] = "issues"
    secret_ref: str = Field(default="", max_length=80, pattern=r"^(PPM_CONNECTOR_[A-Z0-9_]+)?$")
    webhook_secret_ref: str = Field(
        default="", max_length=80, pattern=r"^(PPM_CONNECTOR_[A-Z0-9_]+)?$"
    )
    mapping: dict[str, str] = Field(
        default_factory=lambda: {
            "external_id": "id",
            "name": "name",
            "source_updated_at": "updated_at",
            "status": "status",
        },
        max_length=12,
    )
    status_map: dict[str, str] = Field(default_factory=dict, max_length=30)

    @field_validator("mapping")
    @classmethod
    def mapping_allowlist(cls, value: dict[str, str]) -> dict[str, str]:
        if not set(value) <= {
            "external_id",
            "name",
            "source_updated_at",
            "status",
            "points",
            "priority",
            "work_type",
            "start_date",
            "end_date",
            "due_date",
        }:
            raise ValueError("Unsupported target field")
        if not {"external_id", "name", "source_updated_at"} <= set(value):
            raise ValueError("Identity, title and source timestamp are required")
        if any(not re.fullmatch(r"[A-Za-z0-9_.]{1,100}", p) for p in value.values()):
            raise ValueError("Invalid field path")
        paths = set(value.values())
        if any(child.startswith(parent + ".") for parent in paths for child in paths):
            raise ValueError("Mapped field paths must not overlap a scalar and its nested fields")
        return value

    @model_validator(mode="after")
    def target(self) -> "ConnectorConfig":
        if self.provider == "github" and not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", self.resource
        ):
            raise ValueError("Use owner/repository")
        if self.provider == "jira" and not re.fullmatch(
            r"[a-z0-9][a-z0-9-]*\.atlassian\.net", self.resource
        ):
            raise ValueError("Only Jira Cloud tenant hosts are supported")
        if self.entity == "sprints" and (
            self.provider != "jira" or not self.team_id or not self.board_id
        ):
            raise ValueError("Jira sprints require board and local team")
        if self.provider == "github" and self.entity == "sprints":
            raise ValueError("Unsupported GitHub entity")
        if self.mode == "live" and (self.provider == "csv" or not self.secret_ref):
            raise ValueError("Live connectors require a secret reference")
        return self


class ImportInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    csv_text: str | None = Field(default=None, max_length=500000)
    records: list[dict[str, Any]] | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def bounded(self) -> "ImportInput":
        if self.csv_text is not None and self.records is not None:
            raise ValueError("Select one source")
        if len(json.dumps(self.model_dump()).encode()) > 600000:
            raise ValueError("Input exceeds bounded batch")
        return self


def fingerprint(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def project_rows(config: ConnectorConfig, batch: list[dict]) -> list[dict]:
    """Persist only mapped fields, never incidental notes, credentials or provider metadata."""
    result = []
    for item in batch:
        projected: dict[str, Any] = {}
        for path in config.mapping.values():
            source: Any = item
            target = projected
            parts = path.split(".")
            for part in parts[:-1]:
                source = source.get(part, {}) if isinstance(source, dict) else {}
                target = target.setdefault(part, {})
            value = source.get(parts[-1]) if isinstance(source, dict) else None
            # Unsupported complex values become invalid rows rather than retained private objects.
            target[parts[-1]] = value if isinstance(value, (str, int, float, bool)) else None
        result.append(projected)
    return result


def rows(config: ConnectorConfig, body: ImportInput) -> list[dict]:
    if config.mode == "live":
        if body.csv_text is not None or body.records is not None:
            raise ValueError("Live sync cannot accept fixture records")
        return []
    if config.provider == "csv":
        if body.csv_text is None or "\x00" in body.csv_text:
            raise ValueError("CSV text is required")
        reader = csv.DictReader(io.StringIO(body.csv_text))
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("CSV headers must be unique")
        result: list[dict] = []
        for row in reader:
            if len(result) >= 500 or None in row or any(v is None for v in row.values()):
                raise ValueError("CSV exceeds 500 rows or has inconsistent columns")
            result.append(row)
        return result
    if body.records is None:
        raise ValueError("Fixture records are required")
    return body.records


def normalize(
    config: ConnectorConfig, row: dict
) -> tuple[str, datetime | None, WorkInput | SprintInput]:
    mapped: dict[str, Any] = {}
    for key, path in config.mapping.items():
        current: Any = row
        for segment in path.split("."):
            current = current.get(segment) if isinstance(current, dict) else None
        if current not in (None, ""):
            mapped[key] = current
    external = str(mapped.pop("external_id", ""))
    if not external or len(external) > 160:
        raise ValueError("Source identity is required")
    stamp_value = mapped.pop("source_updated_at", "")
    if not stamp_value and config.provider == "jira" and config.entity == "sprints":
        # Jira sprint DTOs do not expose a modification timestamp. Observation is separate.
        stamp = None
    else:
        stamp = datetime.fromisoformat(str(stamp_value).replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError("Source timestamp must include timezone")
        stamp = stamp.astimezone(UTC)
    # Provider text is data; it never supplies organization, grants, owners or URLs.
    state = str(mapped.pop("status", ""))
    mapped["project_id"] = config.project_id
    for field in ("start_date", "end_date", "due_date"):
        if isinstance(mapped.get(field), str) and "T" in mapped[field]:
            mapped[field] = datetime.fromisoformat(mapped[field].replace("Z", "+00:00")).date()
    if config.entity == "sprints":
        mapped["team_id"] = config.team_id
        mapped["status"] = config.status_map.get(state, state or "planned")
        return external, stamp, SprintInput(**mapped)
    mapped["status"] = config.status_map.get(state, state or "backlog")
    return external, stamp, WorkInput(**mapped)


class Retryable(Exception):
    def __init__(self, delay: int = 0):
        self.delay = min(max(delay, 0), 300)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> None:
        raise ValueError("Connector redirects are disabled")


def fetch_page(
    config: ConnectorConfig, cursor: str | None, page: int, token: str | None = None
) -> tuple[list[dict], str | None]:
    """One bounded request; caller persists each page before fetching the next."""
    secret = os.environ.get(config.secret_ref, "")
    if not secret:
        raise ValueError("Connector credential is not configured")
    if config.provider == "github":
        host = "api.github.com"
        params: dict[str, Any] = {
            "state": "all",
            "per_page": 100,
            "page": page,
            "sort": "updated",
            "direction": "asc",
        }
        if cursor and config.entity == "issues":
            params["since"] = cursor
        path = f"/repos/{config.resource}/{config.entity}?" + urlencode(params)
        auth = "Bearer " + secret
    else:
        host = config.resource
        auth = "Basic " + secret  # operator-provided base64(email:API token)
        if config.entity == "sprints":
            path = f"/rest/agile/1.0/board/{config.board_id}/sprint?" + urlencode(
                {"maxResults": 100, "startAt": (page - 1) * 100}
            )
        else:
            jql = f'project = "{config.jira_project}"'
            if cursor:
                dt = datetime.fromisoformat(cursor.replace("Z", "+00:00"))
                jql += ' AND updated >= "' + dt.strftime("%Y-%m-%d %H:%M") + '"'
            params = {
                "jql": jql + " ORDER BY updated ASC",
                "maxResults": 100,
                "fields": "summary,status,updated",
            }
            if token:
                params["nextPageToken"] = token
            path = "/rest/api/3/search/jql?" + urlencode(params)
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError("Connector host must resolve publicly")
    req = Request(
        "https://" + host + path,
        headers={
            "Authorization": auth,
            "Accept": "application/json",
            "User-Agent": "Enterprise-PPM/1",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with build_opener(NoRedirect()).open(req, timeout=8) as response:
            data = response.read(2000001)
        if len(data) > 2000000:
            raise ValueError("Connector page is too large")
        value = json.loads(data)
    except HTTPError as exc:
        if (
            exc.code in (429, 502, 503, 504)
            or exc.code == 403
            and exc.headers.get("X-RateLimit-Remaining") == "0"
        ):
            delay = exc.headers.get("Retry-After", "30")
            raise Retryable(int(delay) if delay.isdigit() else 30) from None
        raise ValueError("Connector authentication or request failed") from None
    except (TimeoutError, OSError):
        raise Retryable() from None
    if config.provider == "github":
        if not isinstance(value, list):
            raise ValueError("Invalid connector response")
        # GitHub issues endpoint includes PRs: those belong to the separate PR adapter.
        return [r for r in value if config.entity != "issues" or "pull_request" not in r], str(
            page + 1
        ) if len(value) == 100 else None
    return value.get("values" if config.entity == "sprints" else "issues", []), (
        str(page + 1)
        if config.entity == "sprints" and not value.get("isLast", True)
        else value.get("nextPageToken")
    )


async def remote_page(
    config: ConnectorConfig, cursor: str | None, page: int, token: str | None
) -> tuple[list[dict], str | None]:
    return await asyncio.to_thread(fetch_page, config, cursor, page, token)
