"""Bounded operator calibration on frozen synthetic inputs; never activates a provider.

This is a transport/format calibration, not semantic qualification or production SQL
admission. Original probe history is retained and counted. No automatic retries,
new run IDs to reset case limits, paid fallbacks, tenant input or held-out cases.
"""

import argparse
import asyncio
import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from time import perf_counter
from uuid import UUID, uuid4

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from ppm_api.agent_prompts import ROLE_PROVIDERS, cloud_prompt  # noqa: E402
from ppm_api.agent_registry import BY_AGENT  # noqa: E402
from ppm_api.agent_validation import validate_section  # noqa: E402
from ppm_api.ai_provider import gemini_block_reason  # noqa: E402
from ppm_api.model_adapters import NativeAdapter  # noqa: E402
from ppm_api.model_contracts import (  # noqa: E402
    ExecutionPermit,
    ModelFailure,
    ModelRequest,
    SectionOutput,
)
from ppm_api.model_registry import ModelPolicy, digest  # noqa: E402

from scripts.benchmark_agent_runtime import (  # noqa: E402
    CORPUS,
    PRIVATE,
    fixture_context,
    load_corpus,
    save_ledger,
    write_new,
)
from scripts.check_provider_setup import read_keys  # noqa: E402
from scripts.prepare_cloud_specialists import gemini_settings  # noqa: E402


def legacy_gemini_calls() -> int:
    """Count legacy Gemini usage so calibration cannot bypass its account cap."""
    query = (
        "SELECT count(*) FROM ai_calls c JOIN ai_runs r ON r.id=c.run_id "
        "WHERE r.created_at > now()-interval '24 hours 90 seconds' "
        "AND r.versions->>'provider'='gemini'"
    )
    raw = subprocess.check_output(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "postgres",
            "psql",
            "-U",
            "postgres",
            "-d",
            "ppm_local",
            "-Atc",
            query,
        ],
        cwd=ROOT,
        timeout=15,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return int(raw.strip())


def retained_history(provider: str, folder: Path, now: datetime) -> list[dict]:
    """Load prior provider attempts, including failures and ambiguous outcomes."""
    rows: list[dict] = []
    if provider == "groq":
        path = folder / "groq-smoke-ledger.json"
        if path.exists():
            rows = json.loads(path.read_bytes())
    if provider == "gemini":
        # Direct historical smokes did not use normal app SQL. Count every distinct
        # receipt conservatively, including failed probes; never erase old evidence.
        seen = set()
        for path in (ROOT / "docs/verification").glob("gemini-*smoke*.json"):
            receipt = json.loads(path.read_bytes())
            stamp = receipt.get("checked_at")
            if not stamp or stamp in seen:
                continue
            seen.add(stamp)
            if datetime.fromisoformat(stamp) > now - timedelta(days=1):
                rows += [
                    dict(admitted_at=stamp, state="completed", reserved_tokens=8192)
                    for _ in range(receipt.get("requests", 2))
                ]
    return rows


def check_admission(
    profile,
    record: dict,
    rows: list,
    history: list,
    root: str,
    reserved: int,
    external_calls: int,
    now: datetime,
) -> None:
    """Reject calls exceeding the authorization, account or logical-case limits."""
    if any(r["state"] == "unknown" for r in rows + history):
        raise ModelFailure("OUTCOME_UNKNOWN")
    if (
        len(rows) >= record["max_calls"]
        or sum(r.get("root") == root or root in r.get("roots", []) for r in rows) >= 2
    ):
        raise ModelFailure("QUOTA_EXHAUSTED")
    recent = [
        r
        for r in rows + history
        if datetime.fromisoformat(r["admitted_at"]) > now - timedelta(days=1)
    ]
    if len(recent) + external_calls >= profile.requests_per_day:
        raise ModelFailure("QUOTA_EXHAUSTED")
    minute = [
        r for r in recent if datetime.fromisoformat(r["admitted_at"]) > now - timedelta(minutes=1)
    ]
    if (
        len(minute) >= profile.requests_per_minute
        or sum(r["reserved_tokens"] for r in minute) + reserved > profile.tokens_per_minute
    ):
        raise ModelFailure("QUOTA_EXHAUSTED")
    if any(
        r.get("blocked_until") and datetime.fromisoformat(r["blocked_until"]) > now
        for r in rows + history
    ):
        raise ModelFailure("QUOTA_EXHAUSTED")


async def run(
    provider: str,
    case_ids: list[str],
    execute: bool,
    folder: Path = PRIVATE,
    transport=None,
    external_calls=None,
) -> dict:
    """Run authorized synthetic specialist calibration without qualifying profiles."""
    corpus, corpus_hash = load_corpus(CORPUS)
    cases = [next(c for c in corpus["cases"] if c["id"] == cid) for cid in case_ids]
    if not 1 <= len(cases) <= 3 or len(set(case_ids)) != len(case_ids):
        raise ValueError("One to three named calibration cases required")
    if any(
        c["split"] != "calibration" or ROLE_PROVIDERS.get(c["agent"]) != provider for c in cases
    ):
        raise ValueError("Only assigned roles and calibration cases are permitted")
    policy = ModelPolicy.model_validate_json((folder / "policy.json").read_bytes())
    profile = next(p for p in policy.profiles if p.id == provider + "-candidate")
    record = json.loads((folder / (provider + "-specialist-authorization.json")).read_bytes())
    keys = read_keys(folder.parent / "ai-v2.env")
    settings = gemini_settings()
    if provider == "gemini" and gemini_block_reason(settings):
        raise ModelFailure("SPENDING_NOT_AUTHORIZED")
    keys["PPM_AI_API_KEY"] = settings.ai_api_key.get_secret_value()
    key = keys.get(profile.credential_ref, "")
    if not all(
        (
            profile.provider == provider,
            not profile.enabled,
            profile.benchmark_only,
            not profile.qualified_task_classes,
            not profile.allowed_tenants,
            not profile.allowed_projects,
            profile.billing_class == "verified_free",
            profile.free_tier_confirmed,
            record.get("provider") == provider,
            record.get("model") == profile.model,
            record.get("account_scope") == profile.quota_scope,
            bool(key),
            record.get("key_sha256")
            == profile.credential_sha256
            == hashlib.sha256(key.encode()).hexdigest(),
            record.get("corpus_sha256") == corpus_hash,
            record.get("synthetic_only") is True,
            record.get("calibration_only") is True,
            record.get("free_tier_confirmed") is True,
            record.get("max_spend_usd") == "0",
            type(record.get("max_calls")) is int and 1 <= record["max_calls"] <= 9,
            all(BY_AGENT[c["agent"]].task_class in profile.assigned_task_classes for c in cases),
            profile.max_output_tokens == 512,
            profile.concurrency == 1,
            profile.requests_per_day <= 20,
            profile.requests_per_minute == 1,
            profile.tokens_per_minute <= 8000,
        )
    ):
        raise ModelFailure("SPENDING_NOT_AUTHORIZED")
    prepared = [
        (
            c,
            *fixture_context(c),
            cloud_prompt(
                c["agent"],
                "rubric"
                if c.get("rubric")
                else "synthesis"
                if c["agent"] in ("sentiment", "pmo", "executive")
                else "findings",
            ),
        )
        for c in cases
    ]
    for _, _, context, prompt in prepared:
        if context["input_tokens"] + len(prompt.encode()) + 512 + 256 > profile.context_tokens:
            raise ModelFailure("CONTEXT_LIMIT")
    report = dict(
        schema_version="cloud-specialist-calibration-v1",
        provider=provider,
        model=profile.model,
        corpus_sha256=corpus_hash,
        selected_cases=case_ids,
        qualified_classes=[],
        profile_activated=False,
        weight_training=False,
        max_output_tokens=512,
        independent_semantic_review="pending",
        attempts=[],
        limits=dict(
            attempts_per_case=2,
            attempts_per_batch=3,
            batch_seconds=90,
            attempt_seconds=22,
            authorization_calls=record["max_calls"],
        ),
        status="prepared_no_requests",
    )
    if not execute:
        return report
    lock = folder / (provider + "-specialist.lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    ledger_path = folder / (provider + "-specialist-ledger.json")
    try:
        rows = json.loads(ledger_path.read_bytes()) if ledger_path.exists() else []
        history = retained_history(provider, folder, datetime.now(UTC))
        os.environ[profile.credential_ref] = key
        adapter = NativeAdapter(settings, profile, transport)
        began = perf_counter()
        async with httpx.AsyncClient(
            transport=transport,
            timeout=22,
            follow_redirects=False,
            trust_env=False,
            limits=httpx.Limits(max_connections=1),
        ) as client:
            for case, node, context, prompt in prepared:
                if perf_counter() - began > 67:
                    report["status"] = "deadline_stopped"
                    break
                # Case counter excludes prompt/report/corpus filenames so refinements
                # cannot reset the two-attempt limit for the same logical evidence.
                root = digest(
                    [
                        profile.quota_scope,
                        profile.model,
                        case["agent"],
                        case["sources"],
                        case.get("rubric"),
                    ]
                )
                reserved = context["input_tokens"] + len(prompt.encode()) + 512
                used = (
                    (external_calls() if external_calls else legacy_gemini_calls())
                    if provider == "gemini"
                    else 0
                )
                try:
                    check_admission(
                        profile, record, rows, history, root, reserved, used, datetime.now(UTC)
                    )
                except ModelFailure as error:
                    report.update(status="blocked_admission", code=error.code)
                    break
                aid = uuid4()
                request = ModelRequest(
                    ExecutionPermit(
                        aid,
                        provider,
                        profile.model,
                        policy.policy_hash,
                        datetime.now(UTC) + timedelta(seconds=22),
                    ),
                    prompt,
                    context["payload"],
                    context["schema"],
                    22,
                    UUID(int=1),
                    UUID(int=2),
                    BY_AGENT[case["agent"]].task_class,
                    tuple(context["categories"]),
                    profile.context_tokens,
                    512,
                )
                row = dict(
                    attempt_id=str(aid),
                    root=root,
                    case=case["id"],
                    state="unknown",
                    admitted_at=datetime.now(UTC).isoformat(),
                    reserved_tokens=reserved,
                )
                rows.append(row)
                save_ledger(ledger_path, rows)
                receipt = dict(
                    case=case["id"],
                    agent=case["agent"],
                    attempt_id=str(aid),
                    prompt_sha256=digest(prompt),
                    request_sha256=digest([prompt, context["payload"], context["schema"]]),
                )
                report["attempts"].append(receipt)
                raw_candidate = folder / ("cloud-native-" + str(aid) + ".json")

                def checkpoint(value: dict, target=raw_candidate, item=receipt) -> None:
                    """Save the calibration report after each durable attempt transition."""
                    write_new(target, value)
                    item["native_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()

                adapter.checkpoint_response = checkpoint
                try:
                    start = perf_counter()
                    async with asyncio.timeout(22):
                        if provider == "groq":
                            result = await adapter.cloud_chat(
                                client, request, adapter.origin(), start
                            )
                        elif provider == "puter":
                            result = await adapter.puter_chat(client, request, start)
                        else:
                            result = await adapter.gemini_chat(client, request, start)
                    row["state"] = "completed"
                    candidate = folder / ("cloud-candidate-" + str(aid) + ".json")
                    write_new(candidate, result.model_dump(mode="json"))
                    receipt.update(
                        candidate_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),
                        completion=result.completion,
                        usage=result.usage.model_dump(),
                        latency_ms=result.latency_ms,
                    )
                    if result.usage.output_tokens is not None and result.usage.output_tokens > 512:
                        raise ModelFailure("INVALID_OUTPUT", "completed")
                    if result.completion != "complete":
                        raise ModelFailure(
                            "TRUNCATED" if result.completion == "incomplete" else "REFUSED",
                            "completed",
                        )
                    receipt["validation_stage"] = "section_schema"
                    output = SectionOutput.model_validate_json(result.text)
                    receipt["validation_stage"] = "evidence_hard_checks"
                    checked = validate_section(node, context, output)
                    receipt.update(
                        hard_validation=checked["validation"]["outcome"],
                        finding_count=len(checked["findings"]),
                        semantic_review="pending",
                        validation_stage="finished",
                    )
                except ModelFailure as error:
                    row["state"] = error.certainty
                    receipt["code"] = error.code
                    if error.retry_after:
                        row["blocked_until"] = (
                            datetime.now(UTC) + timedelta(seconds=error.retry_after)
                        ).isoformat()
                    report["status"] = "stopped_on_failure"
                    break
                except (httpx.ConnectError, httpx.ConnectTimeout):
                    row["state"] = "not_sent"
                    receipt["code"] = "UNAVAILABLE"
                    report["status"] = "stopped_on_failure"
                    break
                except (httpx.HTTPError, TimeoutError):
                    receipt["code"] = "OUTCOME_UNKNOWN"
                    report["status"] = "stopped_on_unknown"
                    break
                except (ValueError, KeyError, TypeError, IndexError):
                    row["state"] = "completed"
                    receipt["code"] = "INVALID_OUTPUT"
                    report["status"] = "stopped_on_failure"
                    break
                finally:
                    save_ledger(ledger_path, rows)
            else:
                report["status"] = "completed_pending_review"
    finally:
        lock.unlink()
    return report


def main() -> None:
    """Parse specialist calibration options and retain a sanitized execution receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, choices=["groq", "gemini", "puter"])
    parser.add_argument("--case-id", nargs="+", required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("BLOCKED existing output; no request sent")
    try:
        report = asyncio.run(run(args.provider, args.case_id, args.execute))
        write_new(args.output, report)
        print(json.dumps(report, indent=2))
    except Exception:
        raise SystemExit("BLOCKED calibration; private details withheld") from None


if __name__ == "__main__":
    main()
