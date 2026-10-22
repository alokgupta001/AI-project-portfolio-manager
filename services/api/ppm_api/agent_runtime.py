"""Checkpointed hybrid execution over existing runs, fenced jobs and live authority."""

import asyncio
import json
from contextlib import suppress
from datetime import timedelta
from typing import Any
from uuid import UUID, uuid4, uuid5

import sqlalchemy as sa

from ppm_api import agent_engine as E
from ppm_api import agent_task_tables as T
from ppm_api import ai_tables as A
from ppm_api import job_tables as J
from ppm_api.agent_batch import batch_prompt, pack_batch, validate_batch
from ppm_api.agent_context import pack, section_schema
from ppm_api.agent_critique import PROMPT as REVIEW_PROMPT
from ppm_api.agent_critique import Critique, pack_review, validate_review
from ppm_api.agent_planner import PROMPT
from ppm_api.agent_prompts import cloud_prompt
from ppm_api.agent_recovery import recovery
from ppm_api.agent_schemas import AGENTS
from ppm_api.agent_validation import reconcile, validate_section
from ppm_api.identity import now
from ppm_api.jobs import stage
from ppm_api.model_adapters import NativeAdapter
from ppm_api.model_contracts import (
    CapabilityDetail,
    ExecutionPermit,
    ModelFailure,
    ModelRequest,
    SectionOutput,
)
from ppm_api.model_registry import canonical, digest, load_policy
from ppm_api.model_router import RouteRequirements, candidates

TERMINAL = {"SUCCEEDED", "FAILED", "BLOCKED", "SKIPPED", "CANCELLED"}
MAX_BOUND_CONTEXT_BYTES = 80000


async def initialize(conn: Any, run: dict, snapshot: dict) -> None:
    """Persist the run's frozen plan as durable tasks under its existing transaction."""
    plan = snapshot["hybrid_plan"]
    ids = {node["key"]: uuid5(run["id"], node["key"]) for node in plan["nodes"]}
    for node in plan["nodes"]:
        await conn.execute(
            T.tasks.insert().values(
                id=ids[node["key"]],
                organization_id=run["organization_id"],
                run_id=run["id"],
                task_key=node["key"],
                agent=node["agent"],
                kind=node["kind"],
                logical_section_id=node["key"],
                section_id=node["key"],
                dependencies=[str(ids[k]) for k in node["dependencies"]],
                input_manifest=node,
                input_hash=digest(node),
                schema_hash=digest(
                    Critique.model_json_schema()
                    if node["kind"] == "evaluator"
                    else ["compact-batch-v1", SectionOutput.model_json_schema()]
                    if node["mode"] == "batch"
                    else section_schema(node["mode"])
                ),
                prompt_hash=digest(
                    REVIEW_PROMPT
                    if node["kind"] == "evaluator"
                    else batch_prompt(node)
                    if node["mode"] == "batch"
                    else cloud_prompt(node["agent"], node["mode"])
                    if run["versions"].get("cloud_specialist_prompts")
                    and node["kind"] == "semantic"
                    else PROMPT
                ),
                policy_hash=run["versions"]["model_policy_hash"],
                state="WAITING" if node["dependencies"] else "READY",
                required=node.get("required", True),
                revision=1,
                attempt_count=0,
                created_at=now(),
                updated_at=now(),
            )
        )


async def task_update(runtime: Any, task_id: UUID, **values: Any) -> dict:
    """Fence a durable task update through the current worker authority and lease."""
    async with runtime.engine.begin() as conn:
        await runtime.state(conn)
        row = dict(
            (
                await conn.execute(
                    sa.select(T.tasks).where(T.tasks.c.id == task_id).with_for_update()
                )
            )
            .mappings()
            .one()
        )
        await conn.execute(
            T.tasks.update()
            .where(T.tasks.c.id == task_id, T.tasks.c.revision == row["revision"])
            .values(revision=row["revision"] + 1, updated_at=now(), **values)
        )
        return row | values | {"revision": row["revision"] + 1}


async def commit_section(runtime: Any, task: dict, result: dict) -> None:
    # Canonical metric helpers return Decimal. Persist their exact string value
    # through the same JSON boundary as legacy analysis publication.
    """Commit a validated section only while its task and worker remain authorized."""
    result = json.loads(canonical(result))
    task = await task_update(runtime, task["id"], state="VALIDATING")
    async with runtime.engine.begin() as conn:
        _, run, job = await runtime.state(conn)
        await conn.execute(
            T.sections.insert().values(
                id=uuid5(task["id"], "result"),
                organization_id=runtime.tenant,
                run_id=run["id"],
                task_id=task["id"],
                section_id=task["section_id"],
                logical_section_id=task["logical_section_id"],
                result=result,
                validation=result.get("validation", {"hard_checks": "passed"}),
                content_sha256=digest(result),
                schema_version="capability-result-v2",
                created_at=now(),
            )
        )
        await conn.execute(
            T.tasks.update()
            .where(T.tasks.c.id == task["id"], T.tasks.c.revision == task["revision"])
            .values(
                state="SUCCEEDED",
                outcome=result.get("outcome", "supported"),
                revision=task["revision"] + 1,
                updated_at=now(),
                candidate_payload=None,
            )
        )
        await stage(conn, job, task["agent"] + "_checkpoint")


def baseline(snapshot: dict, agent: str, prior: list[dict], current: dict) -> dict:
    """Compute canonical role findings from currently permitted snapshot evidence."""
    items = [
        f
        for f in E.deterministic(snapshot)
        if f["agent"] == agent and all(s["source"] in current for s in f["spans"])
    ]
    findings = E.aggregate(items)
    for finding in findings:
        finding.update(
            epistemic="deterministic",
            semantic_status="not_assessed",
            basis=[],
            predicate="risk_present",
        )
    own = [
        s
        for s in snapshot["sources"]
        if s["kind"] in ("metric", "group")
        and agent in s["permitted_agents"]
        and s["source"] in current
    ]
    return dict(
        findings=findings,
        matches=[],
        base_covered_ids=[s["source"] for s in own],
        outcome="supported"
        if findings or (agent in ("pmo", "executive") and prior)
        else "no_findings"
        if own
        else "insufficient_evidence",
        validation={"hard_checks": "passed", "method": "deterministic"},
    )


async def heartbeat(runtime: Any, stop: asyncio.Event) -> None:
    """Renew the worker lease until stopped, checking run authority each time."""
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=10)
        except TimeoutError:
            async with runtime.engine.begin() as conn:
                _, run, _ = await runtime.state(conn)
                await conn.execute(
                    J.jobs.update()
                    .where(J.jobs.c.id == runtime.job_id, J.jobs.c.lease_token == runtime.token)
                    .values(
                        heartbeat_at=now(),
                        lease_until=min(now() + timedelta(seconds=30), run["deadline"]),
                    )
                )


def batch_window_delay(
    rows: list, profile: Any, instant: Any, deadline: Any, timeout: float
) -> float:
    """Wait within this run for its own previous admission; never manufacture another run."""
    stamps = [
        r["started_at"] for r in rows if r["provider_id"] == profile.provider and r["started_at"]
    ]
    if profile.requests_per_minute != 1 or not stamps:
        return 0
    ready = max(stamps) + timedelta(seconds=61)
    delay = max(0.0, (ready - instant).total_seconds())
    if delay and ready + timedelta(seconds=timeout) >= deadline:
        raise ModelFailure("DEADLINE_EXCEEDED")
    return delay


async def complete_task(runtime: Any, task: dict, node: dict, context: dict, policy: Any) -> dict:
    """Admit, execute and settle bounded model attempts; propagate worker cancellation."""
    from ppm_api.agent_registry import BY_AGENT

    spec = BY_AGENT[node["agent"]]
    review = node["kind"] == "evaluator"
    task_class = "semantic_review" if review else spec.task_class
    additional_classes = tuple(BY_AGENT[m["agent"]].task_class for m in node.get("members", [])[1:])
    base_system = (
        REVIEW_PROMPT
        if review
        else batch_prompt(node)
        if node["mode"] == "batch"
        else (
            cloud_prompt(node["agent"], node["mode"])
            if runtime.settings.ai_execution_mode == "hybrid" and runtime.settings.ai_cloud_enabled
            else PROMPT
        )
    )
    system = base_system
    if task["prompt_hash"] != digest(base_system):
        raise ModelFailure("CONFIGURATION")
    schema = context["schema"]
    output_limit = runtime.settings.ai_max_output_tokens
    excluded: set[str] = set()
    for _ in range(2):
        async with runtime.engine.begin() as conn:
            _, run, _ = await runtime.state(conn)
            rows = (
                (await conn.execute(sa.select(A.calls).where(A.calls.c.run_id == run["id"])))
                .mappings()
                .all()
            )
        if (
            len(rows) >= runtime.settings.ai_max_attempts_per_run
            or task["attempt_count"] >= runtime.settings.ai_max_attempts_per_section
        ):
            raise ModelFailure("QUOTA_EXHAUSTED")
        options, reasons = candidates(
            policy,
            RouteRequirements(
                runtime.tenant,
                run["project_id"],
                task_class,
                context["input_tokens"] + len(system.encode()),
                output_tokens=output_limit,
                categories=tuple(context["categories"]),
                additional_task_classes=additional_classes,
            ),
            runtime.settings,
        )
        options = [p for p in options if p.id not in excluded]
        if not options:
            raise ModelFailure(
                "CONTEXT_LIMIT" if "CONTEXT_LIMIT" in reasons.values() else "UNAVAILABLE"
            )
        admitted = None
        for profile in options:
            aid = uuid4()
            timeout = min(runtime.settings.ai_local_completion_timeout_seconds, 22)
            if node["mode"] == "batch":
                while delay := batch_window_delay(rows, profile, now(), run["deadline"], timeout):
                    await asyncio.sleep(min(delay, 5))
                    async with runtime.engine.begin() as conn:
                        _, run, _ = await runtime.state(conn)
            async with runtime.engine.begin() as conn:
                _, run, _ = await runtime.state(conn)
                admission = await conn.scalar(
                    sa.text(
                        "SELECT public.ppm_model_admit(:run,:task,:scope,:model,:policy,"
                        ":lease,:attempt,:input,:output,:timeout)"
                    ),
                    dict(
                        run=run["id"],
                        task=task["id"],
                        scope=profile.quota_scope,
                        model=profile.model,
                        policy=policy.policy_hash,
                        lease=runtime.token,
                        attempt=aid,
                        input=context["input_tokens"] + len(system.encode()),
                        output=output_limit,
                        timeout=timeout,
                    ),
                )
                if "code" not in admission:
                    await conn.execute(
                        A.calls.update()
                        .where(A.calls.c.id == aid)
                        .values(
                            request_hash=digest(
                                dict(
                                    system=system,
                                    payload=context["payload"],
                                    schema=schema,
                                    model=profile.model,
                                    output_limit=output_limit,
                                    num_ctx=profile.context_tokens,
                                )
                            ),
                        )
                    )
                    admitted = (profile, aid, run, timeout)
                    break
        if admitted is None:
            raise ModelFailure("QUOTA_EXHAUSTED")
        profile, aid, run, timeout = admitted
        permit = ExecutionPermit(
            aid,
            profile.provider,
            profile.model,
            policy.policy_hash,
            min(run["deadline"], now() + timedelta(seconds=timeout)),
        )
        response, failure = None, None
        cancellation: asyncio.CancelledError | None = None
        output: SectionOutput | Critique | dict | None = None
        result: dict | None = None
        try:
            response = await NativeAdapter(runtime.settings, profile).execute(
                ModelRequest(
                    permit,
                    system,
                    context["payload"],
                    schema,
                    timeout,
                    runtime.tenant,
                    run["project_id"],
                    task_class,
                    tuple(context["categories"]),
                    num_ctx=profile.context_tokens,
                    max_output_tokens=output_limit,
                    additional_task_classes=additional_classes,
                )
            )
            if response.completion != "complete":
                raise ModelFailure(
                    "TRUNCATED" if response.completion == "incomplete" else "REFUSED", "completed"
                )
            if review:
                output = Critique.model_validate_json(response.text)
                result = validate_review(context, output)
                result["review_model"] = dict(provider=profile.provider, model=profile.model)
            elif node["mode"] == "batch":
                wire = json.loads(response.text)
                result = validate_batch(node, context, wire)
                output = wire
            else:
                output = SectionOutput.model_validate_json(response.text)
                result = validate_section(node, context, output)
        except ModelFailure as exc:
            failure = exc
        except (ValueError, KeyError, TypeError, IndexError):
            failure = ModelFailure("INVALID_OUTPUT", "completed")
        except asyncio.CancelledError as exc:
            failure = ModelFailure("CANCELLED", "unknown")
            cancellation = exc
        except Exception:
            failure = ModelFailure("UNKNOWN", "unknown")
        try:
            async with runtime.engine.begin() as conn:
                # Reestablish context even when cancellation/revocation prevents publication.
                from ppm_api.ai import worker_context

                await worker_context(conn, runtime.job_id, runtime.tenant, runtime.actor)
                usage = response.usage if response else None
                category = (
                    "unknown"
                    if failure and failure.certainty == "unknown"
                    else "failed"
                    if failure
                    else "complete"
                )
                await conn.execute(
                    sa.text("SELECT public.ppm_model_settle(:id,:category,:code,:i,:o,:cooldown)"),
                    dict(
                        id=aid,
                        category=category,
                        code=failure.code if failure else None,
                        i=usage.input_tokens if usage else None,
                        o=(usage.output_tokens + (usage.reasoning_tokens or 0))
                        if usage and usage.output_tokens is not None
                        else None,
                        cooldown=failure.retry_after if failure else None,
                    ),
                )
                await conn.execute(
                    A.calls.update()
                    .where(A.calls.c.id == aid)
                    .values(
                        status="succeeded" if category == "complete" else category,
                        code=failure.code if failure else None,
                        completed_at=now(),
                        finish_category=response.completion if response else "unknown",
                        input_tokens=usage.input_tokens if usage else None,
                        output_tokens=usage.output_tokens if usage else None,
                        reasoning_tokens=usage.reasoning_tokens if usage else None,
                        usage_source=usage.source if usage else "unknown",
                        send_state="returned" if response else "unknown",
                        native_reason=response.native_finish_reason if response else None,
                        latency_ms=response.latency_ms if response else 0,
                        response_hash=digest(response.text) if response else None,
                    )
                )
        finally:
            if cancellation is not None:
                raise cancellation
        if not failure and output is not None and result is not None:
            candidate = output if isinstance(output, dict) else output.model_dump(mode="json")
            await task_update(
                runtime,
                task["id"],
                candidate_payload=candidate,
                candidate_hash=digest(candidate),
                candidate_attempt_id=aid,
                state="VALIDATING",
            )
            return result
        if failure is None:
            failure = ModelFailure("UNKNOWN", "unknown")
        remaining = (run["deadline"] - now()).total_seconds()
        task = await task_update(runtime, task["id"], state="RETRY_WAIT", diagnostic=failure.code)
        action = recovery(failure, task["attempt_count"], len(rows) + 1, remaining)
        if action == "stop":
            raise failure
        if action == "fallback":
            excluded.add(profile.id)
        if action == "repair":
            # A fresh bounded replacement, never concatenated partial JSON.
            system = base_system + (
                " Replacement after " + failure.code + ". One item; "
                "remaining required aliases are unprocessed gaps."
            )
            from copy import deepcopy

            schema = deepcopy(context["schema"])
            for name in ("findings", "matches", "narrative", "decisions"):
                prop = schema.get("properties", {}).get(name)
                if prop and prop.get("maxItems", 0):
                    prop["maxItems"] = 1
        await task_update(runtime, task["id"], state="READY")
    raise ModelFailure("INVALID_OUTPUT", "completed")


async def execute(runtime: Any, run: dict) -> tuple[dict, str | None]:
    """Resume the frozen DAG and assemble authorized committed results within run limits."""
    from ppm_api.agents import current_sources, get_analysis

    policy = load_policy(runtime.settings)
    if run["versions"]["model_policy_hash"] != policy.policy_hash:
        raise ModelFailure("CONFIGURATION")
    if bool(run["versions"].get("cloud_specialist_prompts")) != bool(
        runtime.settings.ai_execution_mode == "hybrid" and runtime.settings.ai_cloud_enabled
    ):
        raise ModelFailure("CONFIGURATION")
    async with runtime.engine.begin() as conn:
        p, _, _ = await runtime.state(conn)
        analysis = await get_analysis(p, run["id"])
    snapshot, stop = analysis["snapshot"], asyncio.Event()
    pulse = asyncio.create_task(heartbeat(runtime, stop))
    try:
        for node in snapshot["hybrid_plan"]["nodes"]:
            async with runtime.engine.begin() as conn:
                p, _, _ = await runtime.state(conn)
                task = dict(
                    (
                        await conn.execute(
                            sa.select(T.tasks).where(
                                T.tasks.c.run_id == run["id"], T.tasks.c.task_key == node["key"]
                            )
                        )
                    )
                    .mappings()
                    .one()
                )
                stored = list(
                    (
                        await conn.execute(
                            sa.select(T.sections).where(T.sections.c.run_id == run["id"])
                        )
                    ).mappings()
                )
                all_tasks = list(
                    (
                        await conn.execute(sa.select(T.tasks).where(T.tasks.c.run_id == run["id"]))
                    ).mappings()
                )
                live = await current_sources(p, analysis, run)
            if task["state"] in TERMINAL:
                continue
            accepted = live_sections(snapshot, stored, tasks=all_tasks, current=live)
            prior, _ = reviewed_findings(accepted, live)
            try:
                if task["state"] == "RUNNING" and task["attempt_count"]:
                    async with runtime.engine.begin() as conn:
                        await runtime.state(conn)
                        unknown = (
                            (
                                await conn.execute(
                                    sa.select(A.calls).where(
                                        A.calls.c.task_id == task["id"],
                                        A.calls.c.status == "unknown",
                                    )
                                )
                            )
                            .mappings()
                            .all()
                        )
                        for call in unknown:
                            await conn.execute(
                                sa.text(
                                    "SELECT public.ppm_model_settle(:id,'unknown',"
                                    "'OUTCOME_UNKNOWN',NULL,NULL)"
                                ),
                                {"id": call["id"]},
                            )
                    raise ModelFailure("OUTCOME_UNKNOWN", "unknown")
                if task["state"] in ("WAITING", "RETRY_WAIT"):
                    task = await task_update(runtime, task["id"], state="READY")
                if node["kind"] == "deterministic":
                    if task["state"] != "VALIDATING":
                        task = await task_update(runtime, task["id"], state="RUNNING")
                    result = baseline(snapshot, node["agent"], prior, live)
                else:
                    context = (
                        pack_review(prior, live)
                        if node["kind"] == "evaluator"
                        else pack_batch(
                            snapshot,
                            node,
                            live,
                            prior,
                            {i for s in accepted for i in s["result"].get("covered_ids", [])},
                        )
                        if node["mode"] == "batch"
                        else pack(
                            snapshot,
                            node,
                            live,
                            prior,
                            [
                                d["agent"]
                                for d in snapshot["hybrid_plan"]["details"]
                                if d["agent"] != node["agent"]
                                and d["semantic_required_ids"]
                                and not set(d["semantic_required_ids"])
                                <= {i for s in accepted for i in s["result"].get("covered_ids", [])}
                            ],
                        )
                    )
                    if task["bound_at"] is None:
                        # Spaced JSON plus a margin stays below PostgreSQL's 90 KB bound.
                        if (
                            len(json.dumps(context, ensure_ascii=False, default=str).encode())
                            > MAX_BOUND_CONTEXT_BYTES
                        ):
                            raise ModelFailure("CONTEXT_LIMIT")
                        task = await task_update(
                            runtime,
                            task["id"],
                            resolved_context_manifest=context,
                            resolved_input_hash=digest(context),
                            bound_at=now(),
                        )
                    elif task["resolved_input_hash"] != digest(context):
                        raise ModelFailure("AUTHORITY_REVOKED")
                    if task["candidate_payload"] is not None:
                        result = (
                            validate_review(
                                context, Critique.model_validate(task["candidate_payload"])
                            )
                            if node["kind"] == "evaluator"
                            else validate_batch(node, context, task["candidate_payload"])
                            if node["mode"] == "batch"
                            else validate_section(
                                node,
                                context,
                                SectionOutput.model_validate(task["candidate_payload"]),
                            )
                        )
                    else:
                        result = await complete_task(runtime, task, node, context, policy)
                await commit_section(runtime, task, result)
            except ModelFailure as exc:
                async with runtime.engine.begin() as conn:
                    await runtime.state(conn)
                    actual = dict(
                        (await conn.execute(sa.select(T.tasks).where(T.tasks.c.id == task["id"])))
                        .mappings()
                        .one()
                    )
                if actual["state"] not in TERMINAL:
                    await task_update(runtime, task["id"], state="BLOCKED", diagnostic=exc.code)
        async with runtime.engine.begin() as conn:
            p, _, _ = await runtime.state(conn)
            stored = list(
                (
                    await conn.execute(
                        sa.select(T.sections).where(T.sections.c.run_id == run["id"])
                    )
                ).mappings()
            )
            tasks = list(
                (
                    await conn.execute(sa.select(T.tasks).where(T.tasks.c.run_id == run["id"]))
                ).mappings()
            )
            current = await current_sources(p, analysis, run)
        return assemble(snapshot, stored, tasks, current), None
    finally:
        stop.set()
        pulse.cancel()
        with suppress(asyncio.CancelledError, Exception):
            await pulse


def live_sections(snapshot: dict, sections: list, tasks: list | None, current: dict) -> list:
    """Filter committed sections by current sources, hashes and dependency authority."""
    original = {s["source"]: s for s in snapshot["sources"]}
    valid: list[dict] = []
    for section in sections:
        task: dict = next((t for t in tasks or [] if t["id"] == section["task_id"]), {})
        refs = (task.get("resolved_context_manifest") or {}).get("evidence", {})
        result = section["result"]
        ids = {
            s["source"]
            for f in result.get("findings", []) + result.get("matches", [])
            for s in f["spans"]
        }
        ids.update(s["source"] for s in refs.values())
        if all(
            sid in current and sid in original and current[sid]["sha256"] == original[sid]["sha256"]
            for sid in ids
        ):
            base = result.get("base_covered_ids")
            if base is not None:
                section = dict(section) | {
                    "result": result
                    | {
                        "base_covered_ids": [
                            sid
                            for sid in base
                            if sid in current
                            and sid in original
                            and current[sid]["sha256"] == original[sid]["sha256"]
                        ]
                    }
                }
            if "members" in result:
                valid.extend(
                    dict(section) | dict(agent=role, section_id=role + "-01", result=member)
                    for role, member in result["members"].items()
                )
            else:
                valid.append(section)
    return valid


def reviewed_findings(sections: list, current: dict) -> tuple[list, set]:
    """Apply bounded critique decisions and withdraw unsupported dependent findings."""
    decisions = {
        d["key"]: d["disposition"] for s in sections for d in s["result"].get("decisions", [])
    }
    withdrawn = {
        key
        for key, status in decisions.items()
        if status in ("contradicted", "insufficient_evidence")
    }
    findings = reconcile(
        [
            f
            for s in sections
            for f in s["result"]["findings"]
            if all(r["source"] in current for r in f["spans"])
        ]
    )
    for _ in range(24):
        dependent = {f["key"] for f in findings if set(f.get("basis", [])) & withdrawn}
        if dependent <= withdrawn:
            break
        withdrawn |= dependent
    for finding in findings:
        if finding["key"] in decisions:
            finding["semantic_status"] = (
                "model_review_only" if decisions[finding["key"]] == "supported" else "unreviewed"
            )
    return [f for f in findings if f["key"] not in withdrawn], withdrawn


def assemble(snapshot: dict, sections: list, tasks: list, current: dict) -> dict:
    """Report actual baseline and semantic coverage, including partial or failed outcomes."""
    plan = snapshot["hybrid_plan"]
    sections = live_sections(snapshot, sections, tasks, current)
    findings, withdrawn = reviewed_findings(sections, current)
    matches = [
        m
        for s in sections
        for m in s["result"].get("matches", [])
        if all(r["source"] in current for r in m["spans"])
    ]
    details, states = [], []
    for agent in AGENTS:
        descriptor = next(
            (d for d in plan["details"] if d["agent"] == agent),
            dict(
                agent=agent,
                semantic_outcome="not_requested",
                interpretation_reason="none",
                semantic_required_ids=[],
                semantic_covered_ids=[],
                semantic_deferred_ids=[],
            ),
        )
        detail = dict(descriptor)
        own = [
            s
            for s in sections
            if s.get("agent", next((t["agent"] for t in tasks if t["id"] == s["task_id"]), None))
            == agent
        ]
        base: dict = next((s["result"] for s in own if s["section_id"].endswith("-base")), {})
        base_required = [
            s["source"]
            for s in snapshot["sources"]
            if s["fresh"]
            and s["kind"] in ("metric", "group")
            and agent in s["permitted_agents"]
            and any(t["agent"] == agent and t["kind"] == "deterministic" for t in tasks)
        ]
        covered = [
            i
            for s in own
            if not any(f["key"] in withdrawn for f in s["result"].get("findings", []))
            for i in s["result"].get("covered_ids", [])
        ]
        required = detail["semantic_required_ids"]
        detail.update(
            base_outcome=base.get("outcome", "insufficient_evidence")
            if base.get("base_covered_ids")
            else "insufficient_evidence",
            base_covered_ids=base.get("base_covered_ids", []),
            base_required_ids=base_required,
            semantic_covered_ids=covered,
            semantic_deferred_ids=[i for i in required if i not in covered],
            execution_method="hybrid" if covered else "deterministic",
        )
        if required:
            failed = next(
                (
                    t
                    for t in tasks
                    if (
                        t["agent"] == agent
                        or any(
                            m["agent"] == agent
                            for m in t.get("input_manifest", {}).get("members", [])
                        )
                    )
                    and t["kind"] == "semantic"
                    and t["state"] == "BLOCKED"
                ),
                None,
            )
            detail["semantic_outcome"] = (
                "completed"
                if set(required) <= set(covered)
                else "unavailable"
                if failed
                else "deferred"
            )
            detail["code"] = failed["diagnostic"] if failed else None
        details.append(CapabilityDetail.model_validate(detail).model_dump(mode="json"))
        states.append(
            dict(
                agent=agent,
                status="supported"
                if detail["semantic_outcome"] == "completed"
                else "fallback"
                if any(agent in f["agents"] for f in findings)
                else "unavailable",
                code=detail.get("code"),
            )
        )
    partial = any(
        d["semantic_required_ids"] and d["semantic_outcome"] != "completed" for d in details
    ) or any(f["conflicts"] for f in findings)
    base_gaps = [
        d["agent"] for d in details if set(d["base_required_ids"]) - set(d["base_covered_ids"])
    ]
    partial |= bool(base_gaps)
    useful = bool(findings or matches) or any(d["base_covered_ids"] for d in details)
    blocked = [
        "Requested AI interpretation is incomplete: " + d["agent"]
        for d in details
        if d["semantic_required_ids"] and d["semantic_outcome"] != "completed"
    ]
    if any(f["conflicts"] for f in findings):
        blocked.append("Conflicting interpretations require human review")
    if withdrawn:
        blocked.append("Unsupported interpretations and dependent summaries were withheld")
    if base_gaps:
        blocked.append("Baseline evidence is incomplete: " + ", ".join(base_gaps))
    suggestions = E.semantic_suggestions(snapshot, matches, current)
    for suggestion in suggestions:
        suggestion["confidence"] = None
    return dict(
        agents=states,
        findings=findings,
        suggestions=suggestions,
        semantic_status="hybrid_partial" if partial else "hybrid_complete",
        runtime_version="v2",
        analysis_mode=plan["mode"],
        capability_details=details,
        completion_status="failed"
        if not useful
        else "partially_succeeded"
        if partial
        else "succeeded",
        blocked=blocked,
        validation_summary={
            "hard_checks": "passed",
            "semantic_quality": "UNVERIFIED/BLOCKED",
            "withdrawn_items": len(withdrawn),
            "critique": "model_review_only"
            if any(s["result"].get("decisions") for s in sections)
            else "not_assessed",
        },
        task_summary=[
            {
                k: t[k]
                for k in ("id", "task_key", "agent", "kind", "state", "diagnostic", "attempt_count")
            }
            for t in tasks
        ],
    )
