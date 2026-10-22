"""Read-only specialists on the existing AI ledger, jobs, metrics and evidence authority."""

import json
from datetime import date, timedelta
from typing import Any
from uuid import UUID, uuid4

import sqlalchemy as sa
from fastapi import APIRouter, Query, Request
from fastapi.encoders import jsonable_encoder

from ppm_api import agent_engine as E
from ppm_api import agent_tables as T
from ppm_api import ai, assessment, command, delivery, documents
from ppm_api import assessment_tables as A
from ppm_api.agent_schemas import (
    AGENTS,
    PROMPT,
    RULE,
    AgentBatch,
    AgentDefinition,
    AnalysisInput,
    AnalysisSummary,
    AnalysisView,
    ReviewInput,
    ReviewView,
)
from ppm_api.ai_provider import ProviderError
from ppm_api.ai_retrieval import digest, index_chunks
from ppm_api.ai_schemas import AIRunInput
from ppm_api.identity import Auth, Principal, now, record
from ppm_api.jobs import TERMINAL, stage

router = APIRouter(prefix="/api/v1/agents", tags=["Specialists and recommendations"])


def internal_request(p: Principal) -> Request:
    return Request({"type": "http", "headers": [(b"x-organization-id", str(ai.oid(p)).encode())]})


async def private_access(p: Principal, aid: UUID | None) -> dict | None:
    if not aid:
        return None
    row = dict(await assessment.get(p, A.assessments, aid))
    assessment.evidence_access(p, row)
    return row


async def capture(p: Principal, body: AIRunInput, period: dict | None = None) -> dict:
    project = await delivery.get(p, "projects", body.project_id, True)
    a = await private_access(p, body.assessment_id)
    start = date.fromisoformat(period["start"]) if period else now().date()
    end = date.fromisoformat(period["end"]) if period else start + timedelta(days=28)
    metrics = await command.snapshot(start, end, internal_request(p), p, project["portfolio_id"])
    sources = []

    def add(
        key: str,
        kind: str,
        category: str,
        text: str,
        version: str,
        location: str,
        fresh: bool = True,
        **extra: Any,
    ) -> None:
        from ppm_api.agent_registry import REGISTRY

        allowed = (
            [c.agent for c in REGISTRY if category in c.categories]
            if body.uses_v2()
            else [agent for agent in AGENTS if category in E.INPUTS[agent]]
        )
        if allowed and len(text) <= 20000:
            sources.append(
                dict(
                    source=key,
                    kind=kind,
                    text=text,
                    version=version,
                    sha256=digest(text + version),
                    location=location,
                    fresh=fresh,
                    permitted_agents=allowed,
                    **({"category": category} if body.uses_v2() else {}),
                    **extra,
                )
            )

    for row in metrics["projects"]:
        # PMO/Executive may synthesize only the currently permitted portfolio subset.
        for m in row["metrics"]:
            if row["id"] != body.project_id and m["key"] not in {
                "risk",
                "critical",
                "financial_risk",
                "health",
                "usage",
            }:
                continue
            content = {
                k: m[k]
                for k in (
                    "key",
                    "label",
                    "value",
                    "unit",
                    "status",
                    "freshness",
                    "source_updated_at",
                )
            }
            content["reported_health"] = row["reported_health"]
            content["computed_health"] = row["computed_health"]
            content["facts"] = [
                dict(id=str(f["id"]), kind=f["kind"], updated_at=str(f["updated_at"]))
                for f in m["facts"]
            ]
            add(
                f"metric:{row['id']}:{m['key']}",
                "metric",
                "metric:" + m["key"],
                E.canonical(content),
                f"command-v1/risk-rule-v1/policy-{metrics['policy_revision']}",
                f"Project {row['id']} / {m['label']} ({m['unit']})",
                m["freshness"] == "fresh" and m["value"] is not None,
                metric=dict(
                    key=m["key"], value=str(m["value"]) if m["value"] is not None else None
                ),
                discrepancy=row["discrepancy"],
            )
            if (
                row["id"] != body.project_id
                and sources
                and sources[-1]["source"] == f"metric:{row['id']}:{m['key']}"
            ):
                sources[-1]["permitted_agents"] = [
                    x for x in sources[-1]["permitted_agents"] if x in ("pmo", "executive")
                ]
    for row in metrics["records"]:
        data = jsonable_encoder(row["data"])
        if str(data.get("project_id")) == str(body.project_id):
            add(
                "record:" + str(row["id"]),
                "record",
                "record:" + data["kind"],
                E.canonical(data),
                str(row["revision"]),
                f"{data['kind']} / {row['id']}",
                (now() - row["updated_at"]).days <= metrics["stale_days"],
            )
    # Sprint records are read through existing RLS and delivery policy, never raw workforce notes.
    t = delivery.TABLES["sprints"]
    sprint_rows = list(
        (
            await p.conn.execute(
                sa.select(t).where(t.c.project_id == body.project_id, ~t.c.archived).limit(51)
            )
        ).mappings()
    )
    if len(sprint_rows) > 50:
        delivery.fail(422, "Narrow analysis to at most 50 current sprints")
    for row in sprint_rows:
        add(
            "record:" + str(row["id"]),
            "record",
            "record:sprints",
            E.canonical(jsonable_encoder(delivery.view("sprints", row)["data"])),
            str(row["revision"]),
            f"Sprint {row['id']}",
            (now() - row["updated_at"]).days <= metrics["stale_days"],
        )
    team = next(
        (r["summary"] for r in metrics["teams"] if r["summary"]["team_id"] == project["team_id"]),
        None,
    )
    if team and team["status"] == "available" and team["resource_count"] >= 5 and p.role == "Admin":
        data_rows = [jsonable_encoder(r["data"]) for r in metrics["records"]]
        count = sum(
            r["kind"] == "blockers"
            and r.get("status") == "open"
            and str(r.get("project_id")) == str(body.project_id)
            for r in data_rows
        )
        # Fixed aggregate text only. Names/raw notes never enter sentiment prompts or outputs.
        add(
            "group:blockers",
            "group",
            "group:blockers",
            f"Privacy-safe team delivery summary: {count} open project blockers. "
            "This is not emotional sentiment.",
            E.canonical({k: v for k, v in team.items() if k != "as_of"}),
            "Team delivery support signal (minimum group five)",
        )
    if len(set(body.version_ids)) != len(body.version_ids):
        delivery.fail(422, "Choose distinct source versions")
    for vid in body.version_ids:
        v, d = await documents.version(p, vid)
        if d["project_id"] not in (None, body.project_id):
            delivery.fail(404, "Source unavailable")
        # The project chunk helper excludes organization policy; resolve it directly.
        if d["project_id"]:
            _, chunks = await index_chunks(p, body.project_id, vid)
        else:
            from ppm_api import document_tables as D

            chunks = [
                dict(r)
                for r in (
                    await p.conn.execute(
                        sa.select(D.chunks)
                        .where(D.chunks.c.version_id == vid)
                        .order_by(D.chunks.c.ordinal)
                        .limit(21)
                    )
                ).mappings()
            ]
            if not 1 <= len(chunks) <= 20:
                delivery.fail(422, "Analysis sources require 1–20 chunks each")
        for chunk in chunks:
            await documents.citation(chunk["id"], p)
            category = (
                "document:policy"
                if d["category"] == "policy"
                else "document:sprint_report"
                if d["category"] == "sprint_report"
                else "document:project"
            )
            add(
                "chunk:" + str(chunk["id"]),
                "document",
                category,
                chunk["text"],
                v["sha256"] + "/" + str(v["id"]) + "/" + E.canonical(d["policy"]),
                chunk["location"],
            )
    framework, answers = None, {}
    if a:
        fw = await assessment.get(p, A.framework_versions, a["framework_version_id"])
        framework = fw["snapshot"]
        answers = {
            qid: {"value": r.get("value"), "evidence_text": r.get("evidence_text", "")}
            for qid, r in (await assessment.answer_map(p, a["id"])).items()
        }
        add(
            "rubric:" + str(fw["id"]),
            "rubric",
            "assessment:rubric",
            E.canonical(framework),
            str(fw["version"]),
            "Published assessment rubric",
        )
        for qid, r in answers.items():
            q = assessment.questions(framework)[qid]
            text = (r.get("value") or "") if q["answer_type"] == "text" else ""
            text += "\n" + r["evidence_text"]
            if text.strip():
                add(
                    "answer:" + qid,
                    "answer",
                    "assessment:answer",
                    text,
                    str(a["revision"]),
                    "Assessment question " + qid,
                )
    if sum(len(s["text"].encode()) for s in sources) > 70000:
        delivery.fail(422, "Analysis inputs exceed 70 KB; select fewer sources")
    snapshot = dict(
        start=start.isoformat(),
        end=end.isoformat(),
        sources=sources,
        framework=framework,
        answers=answers,
        assessment_revision=a["revision"] if a else None,
        framework_version_id=str(a["framework_version_id"]) if a else None,
        prompt_version=PROMPT,
        prompt_sha256=digest(E.SYSTEM_PROMPT),
        schema_sha256=digest(E.canonical(AgentBatch.model_json_schema())),
        rule_version=RULE,
    )
    if body.uses_v2():
        from ppm_api.agent_planner import PROMPT as HYBRID_PROMPT
        from ppm_api.agent_planner import build_plan
        from ppm_api.model_contracts import SectionOutput

        if body.question_ids and (
            not framework
            or not {str(q) for q in body.question_ids} <= set(assessment.questions(framework))
        ):
            delivery.fail(422, "Choose published assessment questions")
        snapshot.update(
            prompt_version="hybrid-specialists-v2",
            rule_version="hybrid-support-v2",
            prompt_sha256=digest(HYBRID_PROMPT),
            schema_sha256=digest(E.canonical(SectionOutput.model_json_schema())),
        )
        snapshot["hybrid_plan"] = build_plan(snapshot, body)
    if len(E.canonical(snapshot).encode()) > 90000:
        delivery.fail(422, "Complete analysis snapshot exceeds 90 KB")
    return snapshot


async def get_analysis(p: Principal, id_: UUID) -> dict:
    row = (
        (await p.conn.execute(sa.select(T.analyses).where(T.analyses.c.run_id == id_)))
        .mappings()
        .first()
    )
    if not row:
        delivery.fail(404, "Analysis unavailable")
    await delivery.get(p, "projects", row["project_id"], True)
    await private_access(p, row["assessment_id"])
    return dict(row)


async def current_sources(p: Principal, row: dict, run: dict) -> dict:
    try:
        selection = AIRunInput(**run["snapshot"])
        if selection.uses_v2():
            available = []
            for vid in selection.version_ids:
                try:
                    version, _ = await documents.version(p, vid)
                    if version["status"] == "ready":
                        available.append(vid)
                except delivery.DomainError:
                    continue
            selection = selection.model_copy(update={"version_ids": available})
        current = await capture(p, selection, row["snapshot"])
        old = {s["source"]: s for s in row["snapshot"]["sources"]}
        # Any assessment revision change invalidates semantic input, including numeric edits.
        changed_assessment = (
            current["assessment_revision"] != row["snapshot"]["assessment_revision"]
        )
        return {
            s["source"]: s
            for s in current["sources"]
            if s["source"] in old
            and s["sha256"] == old[s["source"]]["sha256"]
            and s["fresh"]
            and not (changed_assessment and s["kind"] in ("answer", "rubric"))
        }
    except (delivery.DomainError, ProviderError):
        return {}


async def can_review(p: Principal, row: dict) -> bool:
    if p.role == "Viewer" or p.user["id"] == row["actor_id"]:
        return False
    if row["assessment_id"]:
        a = await private_access(p, row["assessment_id"])
        return bool(
            a
            and p.user["id"] == a["reviewer_id"]
            and p.user["id"] not in (a["assigned_to"], a["submitted_by"])
        )
    return await delivery.can_edit(p, row["project_id"])


@router.get("/definitions", response_model=list[AgentDefinition])
async def definitions(request: Request, p: Auth) -> list[dict]:
    if request.app.state.settings.ai_runtime_v2_enabled:
        from ppm_api.agent_registry import definitions as hybrid_definitions

        return hybrid_definitions()
    return E.definitions()


@router.post("/runs", response_model=AnalysisView, status_code=202)
async def create(body: AnalysisInput, request: Request, p: Auth) -> dict:
    run = await ai.create(AIRunInput(**body.model_dump(), operation="agents"), request, p)
    return await detail(run["id"], p)


@router.get("/runs", response_model=list[AnalysisSummary])
async def listing(p: Auth, offset: int = Query(0, ge=0, le=10000)) -> list[dict]:
    # RLS filters current project/assessment scope. Listing never resolves source
    # text or saved review comments; those remain exclusive to the detail route.
    rows = (
        await p.conn.execute(
            sa.select(
                T.analyses.c.run_id,
                ai.T.runs.c.created_at,
                ai.J.jobs.c.status,
                sa.func.coalesce(
                    T.analyses.c.output["semantic_status"].astext, "unavailable"
                ).label("semantic_status"),
            )
            .join(ai.T.runs, ai.T.runs.c.id == T.analyses.c.run_id)
            .join(ai.J.jobs, ai.J.jobs.c.ai_run_id == ai.T.runs.c.id)
            .order_by(ai.T.runs.c.created_at.desc(), T.analyses.c.id)
            .offset(offset)
            .limit(25)
        )
    ).mappings()
    return [
        dict(
            run=dict(id=r["run_id"], status=r["status"], created_at=r["created_at"]),
            semantic_status=r["semantic_status"],
        )
        for r in rows
    ]


@router.get("/runs/{id_}", response_model=AnalysisView)
async def detail(id_: UUID, p: Auth) -> dict:
    row = await get_analysis(p, id_)
    run, job = await ai.access(p, id_)
    current = await current_sources(p, row, run)
    output = row["output"] or E.evaluate(row["snapshot"], None, "NOT_REQUESTED")
    if row["output"] and run["versions"].get("runtime_version") == "v2":
        from ppm_api import agent_task_tables as tasks
        from ppm_api.agent_runtime import assemble

        sections = list(
            (
                await p.conn.execute(
                    sa.select(tasks.sections).where(tasks.sections.c.run_id == id_)
                )
            ).mappings()
        )
        task_rows = list(
            (
                await p.conn.execute(sa.select(tasks.tasks).where(tasks.tasks.c.run_id == id_))
            ).mappings()
        )
        output = assemble(row["snapshot"], sections, task_rows, current)
    history = [
        dict(r)
        for r in (
            await p.conn.execute(
                sa.select(T.reviews)
                .where(T.reviews.c.analysis_id == row["id"])
                .order_by(T.reviews.c.item_key, T.reviews.c.revision)
            )
        ).mappings()
    ]

    def item(value: dict) -> dict:
        available = bool(value["spans"]) and all(s["source"] in current for s in value["spans"])
        reviews = [r for r in history if r["item_key"] == value["key"]]
        reviews = [
            {k: r[k] for k in ReviewView.model_fields}
            | (
                {}
                if available
                else {"reason": "Evidence unavailable; comment withheld", "approved_score": None}
            )
            for r in reviews
        ]
        return value | dict(
            available=available,
            spans=value["spans"] if available else [],
            review_revision=len(reviews),
            reviews=reviews,
        )

    findings = [item(value) for value in output["findings"]]
    suggestions = []
    for value in output["suggestions"]:
        s = item(value)
        latest = s["reviews"][-1] if s["reviews"] else None
        s["approved_score"] = (
            latest["approved_score"]
            if s["available"] and latest and latest["decision"] == "accepted"
            else None
        )
        if not s["available"]:
            s["suggested_score"], s["confidence"] = None, None
        suggestions.append(s)
    states = [dict(s) for s in output["agents"]]
    for state in states:
        if (
            output.get("runtime_version") != "v2"
            and state["status"] == "supported"
            and not any(f["available"] and state["agent"] in f["agents"] for f in findings)
        ):
            state.update(status="unavailable", code="EVIDENCE_UNAVAILABLE")
    missing = [s["agent"] for s in states if s["status"] != "supported"]
    if output.get("runtime_version") == "v2":
        missing = [
            d["agent"]
            for d in output["capability_details"]
            if d["semantic_outcome"] in ("deferred", "unavailable", "failed")
        ]
    routes = []
    if run["versions"].get("runtime_version") == "v2":
        calls = (
            await p.conn.execute(
                sa.select(ai.T.calls)
                .where(ai.T.calls.c.run_id == id_)
                .order_by(ai.T.calls.c.run_attempt_no)
            )
        ).mappings()
        routes = [
            {
                k: r[k]
                for k in (
                    "provider_id",
                    "model_id",
                    "run_attempt_no",
                    "finish_category",
                    "code",
                    "input_tokens",
                    "output_tokens",
                    "reasoning_tokens",
                    "usage_source",
                    "latency_ms",
                )
            }
            for r in calls
        ]
    return dict(
        route_summary=routes,
        blocked_reason="; ".join(output.get("blocked", [])) or None,
        **{
            k: output[k]
            for k in (
                "runtime_version",
                "analysis_mode",
                "capability_details",
                "task_summary",
                "validation_summary",
            )
            if k in output
        },
        briefing=[item(f) for f in output["findings"] if "executive" in f["agents"]][:20],
        run=await ai.view(p, run, job),
        prompt_version=row["snapshot"]["prompt_version"],
        rule_version=row["snapshot"]["rule_version"],
        framework_version_id=row["snapshot"]["framework_version_id"],
        assessment_id=row["assessment_id"],
        assessment_revision=row["snapshot"]["assessment_revision"],
        source_snapshot_sha256=digest(E.canonical(row["snapshot"])),
        semantic_status=output["semantic_status"],
        agents=states,
        missing_agents=missing,
        findings=findings,
        suggestions=suggestions,
        evidence=[
            {k: s[k] for k in ("source", "version", "sha256", "location", "text")}
            for s in current.values()
        ],
        stages=await ai.stages(id_, p),
        can_review=job["status"] in TERMINAL and await can_review(p, row),
        limitations=[
            "Accepted means reviewed only; no project or original assessment changes.",
            "Confidence is uncalibrated source support, separate from maturity (0–100).",
            "Sentiment uses a group blocker summary; no individual or emotional labels.",
            "PMO and Executive use the authorized portfolio subset; missing projects stay unknown.",
        ]
        + (
            ["STALE_OR_REVOKED_EVIDENCE: unsupported items are withheld"]
            if len(current) < len(row["snapshot"]["sources"])
            else []
        )
        + run["limitations"],
    )


@router.post("/runs/{id_}/reviews/{item_key}", response_model=AnalysisView)
async def review(id_: UUID, item_key: str, body: ReviewInput, request: Request, p: Auth) -> dict:
    await delivery.lock(p, request)
    row = await get_analysis(p, id_)
    if not await can_review(p, row):
        delivery.fail(403, "An independent authorized human reviewer is required")
    view = await detail(id_, p)
    if view["run"]["status"] not in TERMINAL:
        delivery.fail(409, "Wait for analysis to finish")
    values = view["findings"] + view["suggestions"]
    value = next((x for x in values if x["key"] == item_key), None)
    if not value:
        delivery.fail(404, "Review item unavailable")
    key, fingerprint = documents.request_identity(request, body)
    fingerprint = digest(f"{id_}/{item_key}/{fingerprint}")
    previous = (
        (
            await p.conn.execute(
                sa.select(T.reviews).where(
                    T.reviews.c.actor_id == p.user["id"], T.reviews.c.key == UUID(key)
                )
            )
        )
        .mappings()
        .first()
    )
    if previous:
        if previous["fingerprint"] != fingerprint:
            delivery.fail(409, "Idempotency key has a different review")
        return view
    if request.headers.get("if-match") is None:
        delivery.fail(428, "Reload the review item")
    if request.headers["if-match"] != str(value["review_revision"]):
        delivery.fail(412, "Review changed; reload")
    semantic = item_key.startswith("dimension-")
    if body.decision == "accepted" and (
        not value["available"] or semantic and value["suggested_score"] is None
    ):
        delivery.fail(409, "Current supported evidence is required for acceptance")
    if (not semantic or body.decision == "rejected") and body.approved_score is not None:
        delivery.fail(422, "Only accepted maturity suggestions may have an approved score")
    approved = (
        (body.approved_score if body.approved_score is not None else value["suggested_score"])
        if semantic and body.decision == "accepted"
        else None
    )
    await p.conn.execute(
        T.reviews.insert().values(
            id=uuid4(),
            organization_id=ai.oid(p),
            analysis_id=row["id"],
            item_key=item_key,
            actor_id=p.user["id"],
            **body.model_dump(exclude={"approved_score"}),
            approved_score=approved,
            revision=value["review_revision"] + 1,
            key=UUID(key),
            fingerprint=fingerprint,
            created_at=now(),
        )
    )
    await record(p.conn, request, p.user["id"], ai.oid(p), "agents." + body.decision, row["id"])
    return await detail(id_, p)


async def execute(runtime: ai.Runtime, run: dict) -> tuple[dict, str | None]:
    if run["versions"].get("runtime_version") == "v2":
        from ppm_api.agent_runtime import execute as hybrid_execute

        return await hybrid_execute(runtime, run)
    from ppm_api.agent_provider import AgentProvider

    async with runtime.engine.begin() as conn:
        p, current, job = await runtime.state(conn)
        row = await get_analysis(p, run["id"])
        if row["snapshot"]["prompt_sha256"] != digest(E.SYSTEM_PROMPT) or row["snapshot"].get(
            "schema_sha256"
        ) != digest(E.canonical(AgentBatch.model_json_schema())):
            raise ProviderError("CONFIGURATION_CHANGED")
        live = await current_sources(p, row, current)
        if any(s["source"] not in live for s in row["snapshot"]["sources"] if s["fresh"]):
            raise ProviderError("EVIDENCE_CHANGED")
        await stage(conn, job, "specialists_validating")
    runtime.adapter = AgentProvider(runtime.settings)
    code, output = None, None
    try:
        permitted = row["snapshot"] | {"sources": list(live.values())}
        response = await runtime.call(
            "completion",
            [E.canonical(permitted)],
            E.canonical(permitted),
            [],
            output_schema=AgentBatch,
        )
        output = response.value
    except ProviderError as exc:
        if exc.code in {"RUN_CANCELLED", "DEADLINE_EXCEEDED"}:
            raise
        code = exc.code
    result = E.evaluate(row["snapshot"], output, code)
    # Nine persistent safe stages; bounded local validation never starts another queue or call.
    async with runtime.engine.begin() as conn:
        _, _, job = await runtime.state(conn)
        for state in result["agents"]:
            await stage(conn, job, state["agent"] + "_" + state["status"])
    return result, code


async def publish(p: Principal, run: dict, output: dict) -> None:
    row = await get_analysis(p, run["id"])
    live = await current_sources(p, row, run)
    if output.get("runtime_version") != "v2" and any(
        s["source"] not in live for s in row["snapshot"]["sources"] if s["fresh"]
    ):
        raise ProviderError("EVIDENCE_CHANGED")
    await p.conn.execute(
        T.analyses.update()
        .where(T.analyses.c.id == row["id"])
        .values(output=json.loads(E.canonical(output)))
    )
