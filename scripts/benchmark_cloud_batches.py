"""Compare compact role batches on synthetic calibration inputs, preserving all history.

Dry-run by default. A separately bound repair phase permits at most six additional
calls per provider; it never renews the original authorization or qualifies a model.
"""

import argparse
import asyncio
import hashlib
import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from time import perf_counter
from uuid import UUID, uuid4

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from ppm_api.agent_batch import (  # noqa: E402
    batch_prompt,
    compact_payload,
    compact_schema,
    obj,
    validate_batch,
)
from ppm_api.agent_prompts import ROLE_PROVIDERS  # noqa: E402
from ppm_api.agent_registry import BY_AGENT  # noqa: E402
from ppm_api.ai_provider import gemini_block_reason  # noqa: E402
from ppm_api.model_adapters import NativeAdapter  # noqa: E402
from ppm_api.model_contracts import ExecutionPermit, ModelFailure, ModelRequest  # noqa: E402
from ppm_api.model_registry import ModelPolicy, canonical, digest  # noqa: E402

from scripts.benchmark_agent_runtime import (  # noqa: E402
    CLOUD_CORPUS,
    CORPUS,
    PRIVATE,
    fixture_context,
    load_corpus,
    save_ledger,
    write_new,
)
from scripts.benchmark_cloud_specialists import (  # noqa: E402
    check_admission,
    legacy_gemini_calls,
    retained_history,
)
from scripts.check_provider_setup import read_keys  # noqa: E402
from scripts.prepare_cloud_acceptance import approval, prepare_authorization  # noqa: E402
from scripts.prepare_cloud_specialists import gemini_settings  # noqa: E402

PROVIDERS = ("groq", "gemini", "puter")


def strategy_hash() -> str:
    return digest(
        [
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in (
                "services/api/ppm_api/agent_batch.py",
                "services/api/ppm_api/agent_context.py",
                "services/api/ppm_api/agent_prompts.py",
                "services/api/ppm_api/agent_validation.py",
                "services/api/ppm_api/model_adapters.py",
                "services/api/ppm_api/model_contracts.py",
                "services/api/ppm_api/model_router.py",
                "services/api/ppm_api/agent_registry.py",
                "services/api/ppm_api/agent_runtime.py",
            )
        ]
    )


def fixture_batch(cases: list) -> tuple[dict, dict]:
    if not 1 <= len(cases) <= 3 or len({c["agent"] for c in cases}) != len(cases):
        raise ValueError("One to three distinct roles required")
    members, contexts, payloads, schemas, evidence = [], {}, {}, {}, {}
    categories = set()
    for case in cases:
        node, context = fixture_context(case)
        role = case["agent"]
        if len(cases) > 1 and any(s["kind"] == "answer" for s in context["evidence"].values()):
            raise ValueError("Private assessment answers cannot be batched across roles")
        members.append(node)
        contexts[role] = context
        payloads[role] = compact_payload(context)
        schemas[role] = compact_schema(node, context)
        evidence.update({role + ":" + k: s for k, s in context["evidence"].items()})
        categories.update(context["categories"])
    node = dict(key="calibration-batch", agent=cases[0]["agent"], mode="batch", members=members)
    schema, payload = obj(schemas), canonical(payloads)
    return node, dict(
        schema=schema,
        payload=payload,
        members=contexts,
        evidence=evidence,
        categories=sorted(categories),
        input_tokens=len(payload.encode()) + len(json.dumps(schema).encode()),
    )


def prepare_phase(provider: str, folder: Path = PRIVATE) -> dict:
    """One explicit repair allocation after the user's 'fix all those issues'; no reset."""
    path = folder / (provider + "-repair-authorization.json")
    original = folder / (provider + "-specialist-authorization.json")
    rows = json.loads((folder / (provider + "-specialist-ledger.json")).read_bytes())
    if any(r["state"] == "unknown" for r in rows):
        raise ModelFailure("OUTCOME_UNKNOWN")
    binding = json.loads(original.read_bytes())
    if path.exists():
        record = json.loads(path.read_bytes())
        if (
            record["original_authorization_sha256"]
            != hashlib.sha256(original.read_bytes()).hexdigest()
        ):
            raise ValueError("Original authorization changed")
        return record
    record = binding | dict(
        schema_version="cloud-repair-authorization-v1",
        original_authorization_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
        prior_calls=len(rows),
        max_additional_calls=6,
        max_calls=len(rows) + 6,
        authorized_at=datetime.now(UTC).isoformat(),
        basis=(
            "User instructed: fix all those issues. Bounded synthetic cross-provider comparison; "
            "no paid training, activation or counter reset."
        ),
    )
    write_new(path, record)
    return record


async def run(
    provider: str,
    ids: list[str],
    execute: bool,
    folder: Path = PRIVATE,
    transport=None,
    external_calls=None,
    acceptance_review: Path | None = None,
    corpus_path: Path = CORPUS,
) -> dict:
    corpus, corpus_hash = load_corpus(corpus_path)
    acceptance = acceptance_review is not None
    if acceptance:
        approval(acceptance_review, corpus_hash, strategy_hash())
    cases = [next(c for c in corpus["cases"] if c["id"] == cid) for cid in ids]
    if (
        len(set(ids)) != len(ids)
        or any(c["split"] != "calibration" for c in cases)
        and not acceptance
    ):
        raise ValueError("Only named calibration cases permitted in this repair phase")
    if acceptance and any(ROLE_PROVIDERS[c["agent"]] != provider for c in cases):
        raise ValueError("Acceptance uses assigned roles only")
    node, context = fixture_batch(cases)
    prompt = batch_prompt(node)
    policy = ModelPolicy.model_validate_json((folder / "policy.json").read_bytes())
    profile = next(p for p in policy.profiles if p.id == provider + "-candidate")
    if acceptance and not {BY_AGENT[c["agent"]].task_class for c in cases} <= set(
        profile.assigned_task_classes
    ):
        raise ValueError("Acceptance role assignment changed")
    original_path = folder / (provider + "-specialist-authorization.json")
    original = json.loads(original_path.read_bytes())
    record = json.loads(
        (
            folder
            / (
                provider
                + ("-acceptance-authorization.json" if acceptance else "-repair-authorization.json")
            )
        ).read_bytes()
    )
    additional = 36 if acceptance else 6
    if acceptance and (
        record.get("strategy_sha256") != strategy_hash()
        or record.get("label_approval_sha256")
        != hashlib.sha256(acceptance_review.read_bytes()).hexdigest()
    ):
        raise ValueError("Approval or strategy changed")
    settings = gemini_settings()
    keys = read_keys(folder.parent / "ai-v2.env")
    keys["PPM_AI_API_KEY"] = settings.ai_api_key.get_secret_value()
    key = keys.get(profile.credential_ref, "")
    if provider == "gemini" and gemini_block_reason(settings):
        raise ModelFailure("SPENDING_NOT_AUTHORIZED")
    if not all(
        (
            provider in PROVIDERS,
            profile.provider == provider,
            not profile.enabled,
            profile.benchmark_only,
            not profile.qualified_task_classes,
            not profile.allowed_tenants,
            not profile.allowed_projects,
            profile.billing_class == "verified_free",
            profile.free_tier_confirmed,
            bool(key),
            profile.credential_sha256 == hashlib.sha256(key.encode()).hexdigest(),
            record.get("schema_version")
            == (
                "cloud-acceptance-authorization-v1"
                if acceptance
                else "cloud-repair-authorization-v1"
            ),
            record.get("original_authorization_sha256")
            == hashlib.sha256(original_path.read_bytes()).hexdigest(),
            record.get("max_additional_calls") == additional,
            type(record.get("prior_calls")) is int,
            record.get("max_calls") == record.get("prior_calls", -100) + additional,
            0 <= record.get("prior_calls", -1) <= original["max_calls"] + (6 if acceptance else 0),
            all(
                record.get(k) == original.get(k)
                for k in (
                    "provider",
                    "model",
                    "account_scope",
                    "key_sha256",
                    "synthetic_only",
                    "free_tier_confirmed",
                    "max_spend_usd",
                )
            ),
            record.get("provider") == provider,
            record.get("model") == profile.model,
            record.get("account_scope") == profile.quota_scope,
            record.get("key_sha256") == profile.credential_sha256,
            record.get("corpus_sha256") == corpus_hash,
            record.get("synthetic_only") is True,
            record.get("calibration_only") is (not acceptance),
            record.get("free_tier_confirmed") is True,
            record.get("max_spend_usd") == "0",
            profile.max_output_tokens == 512,
            profile.concurrency == 1,
            profile.requests_per_minute == 1,
            profile.requests_per_day <= 20,
            profile.tokens_per_minute <= 8000,
        )
    ):
        raise ModelFailure("SPENDING_NOT_AUTHORIZED")
    reserved = context["input_tokens"] + len(prompt.encode()) + 512
    if reserved + 256 > profile.context_tokens:
        raise ModelFailure("CONTEXT_LIMIT")
    report = dict(
        schema_version="cloud-batch-calibration-v1",
        provider=provider,
        model=profile.model,
        corpus_sha256=corpus_hash,
        strategy_sha256=strategy_hash(),
        policy_sha256=policy.policy_hash,
        selected_cases=ids,
        prompt_sha256=digest(prompt),
        request_sha256=digest([prompt, context["payload"], context["schema"]]),
        max_output_tokens=512,
        context_tokens=profile.context_tokens,
        qualified_classes=[],
        profile_activated=False,
        weight_training=False,
        independent_semantic_review="pending",
        label_approval_sha256=record.get("label_approval_sha256"),
        attempts=[],
        status="prepared_no_requests",
    )
    if not execute:
        return report
    os.environ[profile.credential_ref] = key
    lock = folder / (provider + "-specialist.lock")
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    ledger_path = folder / (provider + "-specialist-ledger.json")
    try:
        rows = json.loads(ledger_path.read_bytes())
        if len(rows) < record["prior_calls"]:
            raise ValueError("History shrank")
        history = retained_history(provider, folder, datetime.now(UTC))
        roots = [
            digest([profile.quota_scope, profile.model, c["agent"], c["sources"], c.get("rubric")])
            for c in cases
        ]
        used = (
            (external_calls() if external_calls else legacy_gemini_calls())
            if provider == "gemini"
            else 0
        )
        for root in roots:
            check_admission(profile, record, rows, history, root, reserved, used, datetime.now(UTC))
        aid = uuid4()
        receipt = dict(attempt_id=str(aid), cases=ids, request_sha256=report["request_sha256"])
        report["attempts"].append(receipt)
        row = dict(
            attempt_id=str(aid),
            roots=roots,
            cases=ids,
            state="unknown",
            phase="acceptance-v1" if acceptance else "repair-v1",
            admitted_at=datetime.now(UTC).isoformat(),
            reserved_tokens=reserved,
            corpus_sha256=corpus_hash,
            strategy_sha256=strategy_hash(),
            label_approval_sha256=record.get("label_approval_sha256"),
            model=profile.model,
        )
        rows.append(row)
        receipt["admitted_at"] = row["admitted_at"]
        save_ledger(ledger_path, rows)
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
            BY_AGENT[cases[0]["agent"]].task_class,
            tuple(context["categories"]),
            profile.context_tokens,
            512,
            tuple(BY_AGENT[c["agent"]].task_class for c in cases[1:]),
        )

        def checkpoint(value: dict) -> None:
            path = folder / ("cloud-native-" + str(aid) + ".json")
            write_new(path, value)
            receipt["native_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()

        adapter = NativeAdapter(settings, profile, transport, checkpoint_response=checkpoint)
        try:
            async with httpx.AsyncClient(
                transport=transport, timeout=22, follow_redirects=False, trust_env=False
            ) as client:
                start = perf_counter()
                async with asyncio.timeout(22):
                    if provider == "groq":
                        result = await adapter.cloud_chat(client, request, adapter.origin(), start)
                    elif provider == "puter":
                        result = await adapter.puter_chat(client, request, start)
                    else:
                        result = await adapter.gemini_chat(client, request, start)
            row["state"] = "completed"
            path = folder / ("cloud-candidate-" + str(aid) + ".json")
            write_new(path, result.model_dump(mode="json"))
            receipt.update(
                candidate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                usage=result.usage.model_dump(),
                latency_ms=result.latency_ms,
                completion=result.completion,
                reported_model_id=result.reported_model_id,
            )
            if result.completion != "complete":
                raise ModelFailure(
                    "TRUNCATED" if result.completion == "incomplete" else "REFUSED", "completed"
                )
            if result.usage.output_tokens is not None and result.usage.output_tokens > 512:
                raise ModelFailure("INVALID_OUTPUT", "completed")
            checked = validate_batch(node, context, json.loads(result.text))
            receipt["roles"] = {
                role: dict(
                    outcome=r["outcome"],
                    hard_validation=r["validation"]["outcome"],
                    finding_count=len(r["findings"]),
                )
                for role, r in checked["members"].items()
            }
            report["status"] = "completed_pending_review"
        except ModelFailure as error:
            row["state"] = error.certainty
            receipt["code"] = error.code
            if error.retry_after:
                row["blocked_until"] = (
                    datetime.now(UTC) + timedelta(seconds=error.retry_after)
                ).isoformat()
            report["status"] = "stopped_on_failure"
        except (ValueError, KeyError, TypeError, IndexError):
            row["state"] = "completed"
            receipt["code"] = "INVALID_OUTPUT"
            report["status"] = "stopped_on_failure"
        except (httpx.ConnectError, httpx.ConnectTimeout):
            row["state"] = "not_sent"
            receipt["code"] = "UNAVAILABLE"
            report["status"] = "stopped_on_failure"
        except (httpx.HTTPError, TimeoutError):
            receipt["code"] = "OUTCOME_UNKNOWN"
            report["status"] = "stopped_on_unknown"
        finally:
            save_ledger(ledger_path, rows)
    finally:
        lock.unlink()
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--provider", choices=PROVIDERS, required=True)
    p.add_argument("--case-id", nargs="+")
    p.add_argument("--prepare-phase", action="store_true")
    p.add_argument("--acceptance", action="store_true")
    p.add_argument("--label-approval", type=Path)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise SystemExit("BLOCKED existing receipt")
    try:
        if args.prepare_phase:
            if args.execute:
                raise ValueError("Preparation cannot send a request")
            if args.acceptance:
                _, corpus_hash = load_corpus(CLOUD_CORPUS)
                record = prepare_authorization(
                    args.provider, args.label_approval, corpus_hash, strategy_hash()
                )
            else:
                record = prepare_phase(args.provider)
            report = dict(
                status="repair_phase_prepared",
                provider=args.provider,
                prior_calls=record["prior_calls"],
                additional_calls=record["max_additional_calls"],
                model_requests=0,
            )
        else:
            if args.acceptance and args.label_approval is None:
                raise ValueError("Independent approval required")
            report = asyncio.run(
                run(
                    args.provider,
                    args.case_id or [],
                    args.execute,
                    acceptance_review=args.label_approval if args.acceptance else None,
                    corpus_path=CLOUD_CORPUS if args.acceptance else CORPUS,
                )
            )
        write_new(args.output, report)
        print(json.dumps(report, indent=2))
    except Exception:
        raise SystemExit("BLOCKED batch calibration; private details withheld") from None


if __name__ == "__main__":
    main()
