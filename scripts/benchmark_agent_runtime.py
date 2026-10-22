"""Bounded synthetic local benchmark. Dry-run by default; never promotes a profile.

Labels are excluded from requests. Draft labels and decoder/span checks alone never
establish semantic quality. Review the frozen corpus independently before running
held-out cases. Outputs and attempted case counters survive interrupted invocations.
"""

import argparse
import asyncio
import ctypes
import hashlib
import json
import math
import os
import platform
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from time import perf_counter
from uuid import UUID, uuid4

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from ppm_api.agent_context import pack  # noqa: E402
from ppm_api.agent_planner import PROMPT  # noqa: E402
from ppm_api.agent_registry import BY_AGENT  # noqa: E402
from ppm_api.agent_validation import validate_section  # noqa: E402
from ppm_api.config import Settings  # noqa: E402
from ppm_api.local_model_readiness import readiness, windows_memory  # noqa: E402
from ppm_api.model_adapters import NativeAdapter  # noqa: E402
from ppm_api.model_contracts import (  # noqa: E402
    ExecutionPermit,
    ModelFailure,
    ModelRequest,
    SectionOutput,
)
from ppm_api.model_registry import ModelPolicy, canonical, digest  # noqa: E402

CORPUS = ROOT / "tests/fixtures/agent_v2_quality.json"
CLOUD_CORPUS = ROOT / "tests/fixtures/agent_v2_cloud_quality.json"
PRIVATE = ROOT / "artifacts/local/ai-v2"
MODES = {"sentiment": "synthesis", "pmo": "synthesis", "executive": "synthesis"}


def load_corpus(path: Path) -> tuple[dict, str]:
    if (
        path.resolve() not in {CORPUS.resolve(), CLOUD_CORPUS.resolve()}
        or path.stat().st_size > 500000
    ):
        raise ValueError("Only the bundled synthetic corpus is accepted")
    raw = path.read_bytes()
    corpus = json.loads(raw)
    cases = corpus["cases"]
    if corpus["schema_version"] != "agent-quality-corpus-v1" or len(cases) != 108:
        raise ValueError("Incomplete corpus")
    if len({c["id"] for c in cases}) != len(cases):
        raise ValueError("Duplicate case")
    for agent, capability in BY_AGENT.items():
        rows = [c for c in cases if c["agent"] == agent]
        if len(rows) != 12 or sum(c["split"] == "held_out" for c in rows) != 6:
            raise ValueError("Missing class or held-out coverage")
        if any(c["task_class"] != capability.task_class for c in rows):
            raise ValueError("Task class mismatch")
    return corpus, hashlib.sha256(raw).hexdigest()


def fixture_context(case: dict) -> tuple[dict, dict]:
    agent, case_id = case["agent"], case["id"]
    mode = "rubric" if case.get("rubric") else MODES.get(agent, "findings")
    sources = []
    for i, entry in enumerate(case["sources"]):
        text = entry["text"]
        sources.append(
            dict(
                source="answer:" + case["rubric"]["id"]
                if mode == "rubric" and i == 0
                else "group:blockers"
                if agent == "sentiment"
                else f"fixture:{case_id}:{i}",
                kind="answer"
                if mode == "rubric" and i == 0
                else "group"
                if agent == "sentiment"
                else entry.get("kind", "document"),
                category="group:blockers" if agent == "sentiment" else entry["category"],
                text=text,
                sha256=hashlib.sha256(text.encode()).hexdigest(),
                permitted_agents=[agent],
                **({"metric": entry["metric"]} if "metric" in entry else {}),
            )
        )
    basis = [
        dict(
            key="baseline-" + case_id,
            kind="blocker",
            signal="uncertain",
            severity="medium",
            title=case["baseline"]["summary"],
            improvement="Inspect the authorized evidence and retain unresolved limitations.",
            spans=[dict(source=s["source"], start=0, end=len(s["text"])) for s in sources],
        )
    ]
    node = dict(
        key=case_id,
        agent=agent,
        mode=mode,
        source_ids=[s["source"] for s in sources],
        required_ids=[case["rubric"]["id"]]
        if mode == "rubric"
        else ["baseline-" + case_id]
        if mode == "synthesis"
        else [sources[0]["source"]],
    )
    context = pack(
        dict(
            sources=sources,
            framework=dict(dimensions=[dict(questions=[case["rubric"]])])
            if mode == "rubric"
            else None,
        ),
        node,
        {s["source"]: s for s in sources},
        basis,
        case["baseline"].get("unresolved", []),
    )
    return node, context


def ollama_process_ids(processes: list[tuple[int, int, str]]) -> set[int]:
    """Include model runners by ancestry; current Windows runners can have other names."""
    selected = {
        pid
        for pid, _, name in processes
        if name.lower() in {"ollama.exe", "ollama_llama_server.exe"}
    }
    while True:
        expanded = selected | {pid for pid, parent, _ in processes if parent in selected}
        if expanded == selected:
            return selected
        selected = expanded


def ollama_rss_mb() -> int:
    """Sum current Ollama process working sets on Windows, including runner children."""
    if platform.system() != "Windows":
        raise OSError("Windows host process measurement required")
    from ctypes import wintypes

    class ProcessEntry(ctypes.Structure):
        _fields_ = [
            ("size", wintypes.DWORD),
            ("usage", wintypes.DWORD),
            ("pid", wintypes.DWORD),
            ("heap", ctypes.c_size_t),
            ("module", wintypes.DWORD),
            ("threads", wintypes.DWORD),
            ("parent", wintypes.DWORD),
            ("priority", wintypes.LONG),
            ("flags", wintypes.DWORD),
            ("exe", wintypes.WCHAR * 260),
        ]

    class Counters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("faults", wintypes.DWORD)] + [
            (n, ctypes.c_size_t)
            for n in (
                "peak",
                "working",
                "paged_peak",
                "paged",
                "nonpaged_peak",
                "nonpaged",
                "page",
                "page_peak",
            )
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
    kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    psapi.GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(Counters),
        wintypes.DWORD,
    ]
    snapshot = kernel.CreateToolhelp32Snapshot(2, 0)
    if snapshot == wintypes.HANDLE(-1).value:
        raise OSError("Process inventory unavailable")
    entry = ProcessEntry()
    entry.size = ctypes.sizeof(entry)
    processes = []
    try:
        ok = kernel.Process32FirstW(snapshot, ctypes.byref(entry))
        while ok:
            processes.append((int(entry.pid), int(entry.parent), str(entry.exe)))
            ok = kernel.Process32NextW(snapshot, ctypes.byref(entry))
    finally:
        kernel.CloseHandle(snapshot)
    pids = ollama_process_ids(processes)
    if not pids:
        raise OSError("Ollama process not found")
    total, found = 0, False
    for pid in pids:
        handle = kernel.OpenProcess(0x410, False, pid)
        if not handle:
            if ctypes.get_last_error() == 87:  # A short-lived child exited after inventory.
                continue
            raise OSError("Ollama process memory unavailable")
        try:
            counters = Counters()
            counters.cb = ctypes.sizeof(counters)
            if not psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
                raise OSError("Ollama working set unavailable")
            total += counters.working
            found = True
        finally:
            kernel.CloseHandle(handle)
    if not found:
        raise OSError("Ollama working set unavailable")
    return math.ceil(total / 1048576)


def write_new(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def save_ledger(path: Path, rows: list) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


async def run(
    cases: list[dict],
    corpus_hash: str,
    profile,
    folder: Path,
    execute: bool,
    context_tokens: int,
    max_output: int,
    warm_repeats: int,
    transport: httpx.AsyncBaseTransport | None = None,
    keep_alive: int = 60,
) -> dict:
    if keep_alive not in (0, 60):
        raise ValueError("Bounded model residency required")
    if keep_alive == 0 and warm_repeats:
        raise ValueError("Warm measurements require retained model residency")
    prepared = [(c, *fixture_context(c)) for c in cases]
    if len(prepared) + warm_repeats > 30:
        raise ValueError("Thirty calls per explicit invocation maximum")
    for _, _, context in prepared:
        if context["input_tokens"] + len(PROMPT.encode()) + max_output + 256 > context_tokens:
            raise ModelFailure("CONTEXT_LIMIT")
    report = dict(
        schema_version="agent-benchmark-v1",
        mode="local-only",
        model=profile.model,
        model_digest=profile.installed_digest,
        corpus_sha256=corpus_hash,
        prompt_sha256=hashlib.sha256(PROMPT.encode()).hexdigest(),
        context_tokens=context_tokens,
        output_tokens=max_output,
        selected_cases=[c["id"] for c in cases],
        maximum_calls=len(prepared) + warm_repeats,
        warm_repeats_requested=warm_repeats,
        keep_alive_seconds=keep_alive,
        profile_activated=False,
        qualified_classes=[],
        independent_semantic_review="pending",
        attempts=[],
        status="prepared_no_requests",
        limits=dict(attempt_seconds=22, run_seconds=90, attempts_per_run=4, attempts_per_root=2),
    )
    if not execute:
        return report
    folder.mkdir(parents=True, exist_ok=True)
    lock = folder / "local-benchmark.lock"
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    ledger_path = folder / "local-benchmark-ledger.json"
    try:
        ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else []
        if any(r["state"] == "unknown" for r in ledger):
            raise ModelFailure("OUTCOME_UNKNOWN")
        observed = readiness(profile.model, reservation_mb=profile.memory_reservation_mb)
        report["readiness"] = observed
        if observed["blocked"] or observed["model_digest"] != profile.installed_digest:
            report["status"] = "blocked_preflight"
            return report
        hardware = dict(observed["hardware"])
        hardware["memory"] = dict(total_mb=observed["hardware"]["memory"]["total_mb"])
        hardware.update(
            cpu=platform.processor(),
            logical_cpus=os.cpu_count(),
            ollama_version=observed.get("ollama_version"),
            model_details=observed.get("model_details"),
        )
        report["hardware"] = hardware
        report["hardware_record_sha256"] = digest(hardware)
        settings = Settings(
            app_env="test",
            database_url="postgresql+asyncpg://unused:unused@127.0.0.1:9/ppm_test",
            redis_url="redis://127.0.0.1:9/1",
            storage_root=folder / "synthetic-only",
            jwt_secret="synthetic-benchmark-no-live-authority",
            ai_ollama_enabled=True,
            ai_ollama_keep_alive=keep_alive,
        )
        adapter = NativeAdapter(settings, profile, transport)
        queue = [(c, n, x, False) for c, n, x in prepared]
        if warm_repeats:
            c, n, x = prepared[0]
            queue += [(c, n, x, True) for _ in range(warm_repeats)]
        async with httpx.AsyncClient(
            transport=transport,
            timeout=22,
            follow_redirects=False,
            trust_env=False,
            limits=httpx.Limits(max_connections=1),
        ) as client:
            # Cold is observed, never forced by unloading someone else's model.
            running = await adapter.read(client, "GET", adapter.origin() + "/api/ps")
            cold = not running.get("models")
            for case, node, context, repeat in queue:
                running = await adapter.read(client, "GET", adapter.origin() + "/api/ps")
                if any(m.get("name") != profile.model for m in running.get("models", [])):
                    report["status"] = "other_model_resident"
                    break
                cold = not running.get("models")
                tags = await adapter.read(client, "GET", adapter.origin() + "/api/tags")
                if not any(
                    t.get("name") == profile.model and t.get("digest") == profile.installed_digest
                    for t in tags.get("models", [])
                ):
                    report["status"] = "model_digest_changed"
                    break
                root = digest(
                    [
                        corpus_hash,
                        profile.installed_digest,
                        case["id"],
                        context_tokens,
                        max_output,
                        "warm" if repeat else "quality",
                    ]
                )
                prior = sum(r["root"] == root for r in ledger)
                # Warm timing is a separate explicit measurement, not a retry or quality vote.
                if not repeat and prior >= 2:
                    report["status"] = "logical_attempt_limit"
                    break
                sample = windows_memory()
                required_mb = 2048 + (profile.memory_reservation_mb if cold else 0)
                if sample["available_mb"] < required_mb:
                    report["status"] = "memory_stopped"
                    break
                # Each fixture is one explicit synthetic analysis. No repair/retry is automatic.
                attempt_id, started = uuid4(), perf_counter()
                row = dict(
                    attempt_id=str(attempt_id),
                    root=root,
                    state="unknown",
                    admitted_at=datetime.now(UTC).isoformat(),
                )
                ledger.append(row)
                save_ledger(ledger_path, ledger)
                receipt = dict(
                    case=case["id"],
                    task_class=case["task_class"],
                    split=case["split"],
                    attempt_id=str(attempt_id),
                    timing_only=repeat,
                    cold=cold,
                    samples=[],
                )
                report["attempts"].append(receipt)

                async def monitor(receipt: dict = receipt) -> None:
                    while True:
                        memory = windows_memory()
                        receipt["samples"].append(
                            dict(available_mb=memory["available_mb"], ollama_rss_mb=ollama_rss_mb())
                        )
                        if memory["available_mb"] < 2048:
                            raise ModelFailure("LOCAL_RESOURCE", "unknown")
                        await asyncio.sleep(0.1)

                watcher = asyncio.create_task(monitor())
                request = ModelRequest(
                    ExecutionPermit(
                        attempt_id,
                        "ollama",
                        profile.model,
                        digest(profile.model_dump()),
                        datetime.now(UTC) + timedelta(seconds=22),
                    ),
                    PROMPT,
                    context["payload"],
                    context["schema"],
                    22,
                    UUID(int=1),
                    UUID(int=2),
                    BY_AGENT[case["agent"]].task_class,
                    (),
                    context_tokens,
                    max_output,
                )
                body = dict(
                    model=profile.model,
                    stream=False,
                    think=False,
                    keep_alive=settings.ai_ollama_keep_alive,
                    format=request.schema,
                    messages=[
                        dict(role="system", content=request.system),
                        dict(role="user", content=request.payload),
                    ],
                    options=dict(num_ctx=context_tokens, num_predict=max_output, temperature=0),
                )
                generation = asyncio.create_task(
                    adapter.read(client, "POST", adapter.origin() + "/api/chat", body)
                )
                try:
                    async with asyncio.timeout(22):
                        done, _ = await asyncio.wait(
                            [generation, watcher], return_when=asyncio.FIRST_COMPLETED
                        )
                        if watcher in done:
                            await watcher
                        data = await generation
                    row["state"] = "completed"
                    result = adapter.ollama_result(
                        request, data, int((perf_counter() - started) * 1000)
                    )
                    candidate = folder / (str(attempt_id) + ".json")
                    write_new(candidate, result.model_dump(mode="json"))
                    receipt.update(
                        candidate_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),
                        completion=result.completion,
                        usage=result.usage.model_dump(),
                        latency_ms=result.latency_ms,
                        load_ms=result.load_ms,
                        generation_ns=data.get("eval_duration"),
                    )
                    if (
                        result.usage.output_tokens is not None
                        and result.usage.output_tokens > max_output
                    ):
                        raise ModelFailure("INVALID_OUTPUT", "completed")
                    if result.completion != "complete":
                        raise ModelFailure("TRUNCATED", "completed")
                    output = SectionOutput.model_validate_json(result.text)
                    checked = validate_section(node, context, output)
                    receipt["hard_validation"] = checked["validation"]["outcome"]
                    receipt["semantic_review"] = "pending"
                    receipt["baseline_sha256"] = digest(case["baseline"])
                except ModelFailure as error:
                    row["state"] = error.certainty
                    receipt["code"] = error.code
                    report["status"] = "stopped_on_failure"
                    break
                except (httpx.HTTPError, TimeoutError, OSError):
                    receipt["code"] = "OUTCOME_UNKNOWN"
                    report["status"] = "stopped_on_unknown"
                    break
                except (ValueError, KeyError, TypeError):
                    row["state"] = "completed"
                    receipt["code"] = "INVALID_OUTPUT"
                    report["status"] = "stopped_on_failure"
                    break
                finally:
                    generation.cancel()
                    watcher.cancel()
                    await asyncio.gather(generation, watcher, return_exceptions=True)
                    receipt["end_to_end_seconds"] = round(perf_counter() - started, 4)
                    save_ledger(ledger_path, ledger)
            else:
                report["status"] = "completed_pending_review"
    finally:
        lock.unlink()
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["local-only"], default="local-only")
    parser.add_argument("--cases", type=Path, default=CORPUS)
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--case-id", nargs="+")
    parser.add_argument("--context", type=int, choices=[2048, 4096], default=4096)
    parser.add_argument("--max-output", type=int, choices=[256, 512], default=512)
    parser.add_argument("--concurrency", type=int, choices=[1], default=1)
    parser.add_argument("--max-calls", type=int, default=3)
    parser.add_argument("--warm-repeats", type=int, choices=range(6), default=0)
    parser.add_argument("--keep-alive", type=int, choices=[0, 60], default=60)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("BLOCKED output exists; no request sent")
    try:
        corpus, corpus_hash = load_corpus(args.cases)
        if not 1 <= args.max_calls <= 30 or args.warm_repeats >= args.max_calls:
            raise ValueError("Invalid explicit call budget")
        selected = (
            args.case_id or [c["id"] for c in corpus["cases"]][: args.max_calls - args.warm_repeats]
        )
        if len(set(selected)) != len(selected):
            raise ValueError("Duplicate selection")
        by_id = {c["id"]: c for c in corpus["cases"]}
        cases = [by_id[k] for k in selected]
        if len(cases) + args.warm_repeats > args.max_calls:
            raise ValueError("Selection exceeds explicit call budget")
        policy = ModelPolicy.model_validate_json((PRIVATE / "policy.json").read_bytes())
        profile = next(
            p for p in policy.profiles if p.provider == "ollama" and p.model == args.model
        )
        if any(p.enabled for p in policy.profiles if p.provider == "ollama"):
            raise ValueError("Production local profiles must be disabled while benchmarking")
        if not profile.benchmark_only or not profile.installed_digest:
            raise ValueError("Disabled installed benchmark profile required")
        report = asyncio.run(
            run(
                cases,
                corpus_hash,
                profile,
                PRIVATE,
                args.execute,
                args.context,
                args.max_output,
                args.warm_repeats,
                keep_alive=args.keep_alive,
            )
        )
        write_new(args.output, report)
        print(canonical(report))
        if args.execute and report["status"] != "completed_pending_review":
            raise SystemExit(1)
    except (
        ModelFailure,
        httpx.HTTPError,
        TimeoutError,
        OSError,
        ValueError,
        KeyError,
        StopIteration,
    ):
        raise SystemExit(
            "BLOCKED benchmark configuration, resource, or durable admission gate"
        ) from None


if __name__ == "__main__":
    main()
