"""A provenance-checked fixture pilot using normal jobs, source checks and provider quotas."""

from datetime import timedelta
from uuid import UUID, uuid5

import sqlalchemy as sa
from fastapi import Request

from ppm_api.config import Settings
from ppm_api.modules.ai.registry import digest, load_policy
from ppm_api.modules.delivery import service as delivery
from ppm_api.modules.identity.service import Principal, now, record
from ppm_api.modules.selection.audit import audit
from ppm_api.modules.selection.protocol import PROMPT, fixture_sources, protocol, summarize
from ppm_api.modules.selection.schemas import (
    AutomatedReview,
    LabelReview,
    PilotInput,
)
from ppm_api.modules.selection.tables import pilots


def automated_allowed(settings: object, id_: UUID) -> bool:
    """Default deny; only the owner's one-ID local allowlist enables automated review."""
    return (
        isinstance(settings, Settings)
        and settings.app_env == "local"
        and id_ in settings.ai_fixture_automated_pilots
    )


async def scope(p: Principal, project_id: UUID) -> None:
    """Require an Admin and their existing explicit guided grant; create no new scope."""
    from ppm_api.modules.agents.guided_review import granted_projects

    if p.role != "Admin":
        delivery.fail(403, "Selection pilot requires Admin")
    await delivery.get(p, "projects", project_id, True)
    if project_id not in await granted_projects(p):
        delivery.fail(403, "Use an already approved guided project")


def binding(settings: object) -> dict:
    """Freeze policy, model, prompt and corpus without exposing key references or account IDs."""
    assert isinstance(settings, Settings)
    policy = load_policy(settings)
    profiles = [p for p in policy.profiles if p.provider == "gemini" and p.guided_selection_enabled]
    model = profiles[0].model if len(profiles) == 1 else None
    return dict(
        provider="gemini",
        model=model,
        policy_sha256=policy.policy_hash,
        corpus_sha256=protocol()["corpus_sha256"],
        strategy_sha256=digest(PROMPT),
        lineage="synthetic",
        output_tokens=128,
        max_calls=12,
        protocol=protocol(),
        guided_enabled=settings.ai_guided_enabled,
        runtime_enabled=settings.ai_runtime_v2_enabled,
        effective_output_tokens=min(128, settings.ai_max_output_tokens),
        measurement_version="attempt-elapsed-v2",
        timeout_seconds=min(settings.ai_local_completion_timeout_seconds, 22),
    )


async def get(p: Principal, id_: UUID, lock: bool = False) -> dict:
    """Resolve only a currently authorized pilot, optionally locking edits and case starts."""
    if p.role != "Admin":
        delivery.fail(403, "Selection pilot requires Admin")
    query = sa.select(pilots).where(pilots.c.id == id_)
    row = (await p.conn.execute(query.with_for_update() if lock else query)).mappings().first()
    if not row:
        delivery.fail(404, "Selection pilot unavailable")
    await scope(p, row["project_id"])
    return dict(row)


async def reviewed(p: Principal, row: dict) -> bool:
    """A removed reviewer or grant cannot authorize new measurements or retain a pass."""
    review = row["review"]
    if not review:
        return False
    if review.get("kind") == "automated_rule_audit":
        try:
            if (
                review.get("human_reviewed") is not False
                or review.get("pilot_id") != str(row["id"])
                or review.get("audit") != audit(row["binding"]["protocol"])
            ):
                return False
        except (ValueError, TypeError, KeyError):
            return False
    elif review.get("human_reviewed") is not True or review["actor_id"] == str(row["actor_id"]):
        return False
    return bool(
        await p.conn.scalar(
            sa.text(
                "SELECT public.ppm_guided_actor(:org,:actor,:project) AND EXISTS "
                "(SELECT 1 FROM memberships WHERE organization_id=:org AND user_id=:actor "
                "AND active AND role='Admin')"
            ),
            dict(
                org=row["organization_id"],
                actor=UUID(review["actor_id"]),
                project=row["project_id"],
            ),
        )
    )


async def view(p: Principal, row: dict, settings: object) -> dict:
    """Rebuild scores from immutable accepted API sections, never from manual fallback cards."""
    from ppm_api.modules.agents import task_tables as T
    from ppm_api.modules.ai import service as ai

    rows = []
    next_case_at = None
    for case in row["binding"]["protocol"]["cases"]:
        result = dict(
            id=case["id"],
            split=case["split"],
            expected=case["expected"],
            selected=[],
            status="not_started",
            run_id=row["case_runs"].get(case["id"]),
            correct=None,
            latency_ms=0,
            elapsed_ms=None,
            timing_kind="not_recorded",
            diagnostic=None,
        )
        if result["run_id"]:
            run, job = await ai.access(p, UUID(result["run_id"]))
            result["status"] = "pending"
            if job["status"] in ai.TERMINAL:
                sections = list(
                    (
                        await p.conn.execute(
                            sa.select(T.sections).where(T.sections.c.run_id == run["id"])
                        )
                    ).mappings()
                )
                accepted = next((s for s in sections if "guided_cards" in s["result"]), None)
                calls = list(
                    (
                        await p.conn.execute(
                            sa.select(ai.T.calls).where(ai.T.calls.c.run_id == run["id"])
                        )
                    ).mappings()
                )
                for call in calls:
                    if call["started_at"]:
                        due = call["started_at"] + timedelta(seconds=61)
                        next_case_at = max(next_case_at, due) if next_case_at else due
                valid = (
                    accepted is not None
                    and len(calls) == 1
                    and calls[0]["status"] == "succeeded"
                    and job["status"] in {"succeeded", "partially_succeeded"}
                    and calls[0]["provider_id"] == row["binding"]["provider"]
                    and calls[0]["model_id"] == row["binding"]["model"]
                )
                result["status"] = "measured" if valid else "unavailable"
                result["latency_ms"] = sum(c["latency_ms"] for c in calls)
                # Legacy failure zeros contain no timing evidence; never backfill history.
                if valid or (calls and all(c["latency_ms"] > 0 for c in calls)):
                    result["elapsed_ms"] = result["latency_ms"]
                    result["timing_kind"] = "accepted_response" if valid else "unavailable_attempt"
                result["diagnostic"] = run["diagnostic"] or next(
                    (c["code"] for c in calls if c["code"]), None
                )
                if valid:
                    assert accepted is not None
                    result["selected"] = [
                        c["source"].rsplit(":", 1)[-1] for c in accepted["result"]["guided_cards"]
                    ]
                    result["correct"] = set(result["selected"]) == set(case["expected"])
        rows.append(result)
    current = row["binding"] == binding(settings) and await reviewed(p, row)
    kind = row["review"].get("kind", "human") if row["review"] else None
    if kind == "automated_rule_audit":
        current = current and automated_allowed(settings, row["id"])
    summary = summarize(rows)
    human = bool(
        row["review"]
        and kind == "human"
        and row["review"].get("human_reviewed") is True
        and row["review"]["actor_id"] != str(row["actor_id"])
    )
    summary.update(label_review_kind=kind, independent_human_review=human)
    if not current:
        summary["state"] = "awaiting_label_review" if not row["review"] else "binding_changed"
    return dict(
        **{
            k: row[k]
            for k in ("id", "project_id", "actor_id", "created_at", "revision", "binding", "review")
        },
        protocol=row["binding"]["protocol"],
        cases=rows,
        summary=summary,
        binding_current=current,
        can_review=not row["review"] and p.user["id"] != row["actor_id"],
        next_case_at=next_case_at,
        can_automated_review=(
            not row["review"]
            and not row["case_runs"]
            and automated_allowed(settings, row["id"])
            and row["binding"] == binding(settings)
        ),
        review_kind=kind,
        human_reviewed=human,
    )


def revision(row: dict, request: Request) -> None:
    """Reject stale label approval instead of approving a different protocol revision."""
    if request.headers.get("if-match") != str(row["revision"]):
        delivery.fail(412, "Pilot changed; reload before continuing")


async def listing(project_id: UUID, request: Request, p: Principal) -> list[dict]:
    """List ten recent authorized pilots, reconstructing measurements without inference."""
    await scope(p, project_id)
    rows = (
        await p.conn.execute(
            sa.select(pilots)
            .where(pilots.c.project_id == project_id)
            .order_by(pilots.c.created_at.desc())
            .limit(10)
        )
    ).mappings()
    return [await view(p, dict(row), request.app.state.settings) for row in rows]


async def create(body: PilotInput, request: Request, p: Principal) -> dict:
    """Prepare an idempotent frozen fixture protocol; make no model call or label approval."""
    await delivery.lock(p, request)
    await scope(p, body.project_id)
    if not request.app.state.settings.ai_guided_enabled:
        delivery.fail(422, "Guided review is disabled")
    key = request.headers.get("idempotency-key", "")
    if not 1 <= len(key) <= 100:
        delivery.fail(428, "Idempotency key required")
    id_ = uuid5(p.session["organization_id"], f"selection:{p.user['id']}:{key}")
    row = (await p.conn.execute(sa.select(pilots).where(pilots.c.id == id_))).mappings().first()
    if row:
        if row["project_id"] != body.project_id:
            delivery.fail(409, "Idempotency key has a different project")
        return await view(p, dict(row), request.app.state.settings)
    item = dict(
        id=id_,
        organization_id=p.session["organization_id"],
        project_id=body.project_id,
        actor_id=p.user["id"],
        binding=binding(request.app.state.settings),
        review=None,
        case_runs={},
        created_at=now(),
        revision=1,
    )
    await p.conn.execute(pilots.insert().values(**item))
    await record(
        p.conn, request, p.user["id"], item["organization_id"], "selection_pilot.created", id_
    )
    return await view(p, item, request.app.state.settings)


async def detail(id_: UUID, request: Request, p: Principal) -> dict:
    """Recheck current access and return a downloadable pilot report without inference."""
    return await view(p, await get(p, id_), request.app.state.settings)


async def approve(id_: UUID, body: LabelReview, request: Request, p: Principal) -> dict:
    """Freeze a different authorized human's review of every bound fixture label."""
    await delivery.lock(p, request)
    row = await get(p, id_, True)
    if row["review"]:
        if row["review"]["actor_id"] == str(p.user["id"]) and row["review"][
            "input_sha256"
        ] == digest(body.model_dump()):
            return await view(p, row, request.app.state.settings)
        delivery.fail(409, "Label review is immutable; start a new pilot")
    revision(row, request)
    if p.user["id"] == row["actor_id"]:
        delivery.fail(403, "A second person must review all twelve fixture labels")
    expected = protocol()
    if (
        body.corpus_sha256 != expected["corpus_sha256"]
        or body.strategy_sha256 != expected["strategy_sha256"]
        or set(body.reviewed_case_ids) != {c["id"] for c in expected["cases"]}
        or row["binding"] != binding(request.app.state.settings)
    ):
        delivery.fail(409, "Review does not match the frozen protocol")
    row.update(
        review=dict(
            kind="human",
            actor_id=str(p.user["id"]),
            approved_at=now().isoformat(),
            reason=body.reason,
            input_sha256=digest(body.model_dump()),
            corpus_sha256=body.corpus_sha256,
            strategy_sha256=body.strategy_sha256,
            human_reviewed=True,
        ),
        revision=row["revision"] + 1,
    )
    await p.conn.execute(
        pilots.update()
        .where(pilots.c.id == id_)
        .values(review=row["review"], revision=row["revision"])
    )
    await record(
        p.conn,
        request,
        p.user["id"],
        row["organization_id"],
        "selection_pilot.labels_reviewed",
        id_,
    )
    return await view(p, row, request.app.state.settings)


async def automated_review(
    id_: UUID, body: AutomatedReview, request: Request, p: Principal
) -> dict:
    """Record a scoped machine audit with human_reviewed=false; preserve all human gates."""
    await delivery.lock(p, request)
    row = await get(p, id_, True)
    settings = request.app.state.settings
    if not automated_allowed(settings, id_):
        delivery.fail(403, "Automated fixture review is not authorized for this pilot")
    fingerprint = digest(body.model_dump())
    if row["review"]:
        if (
            row["review"].get("kind") == "automated_rule_audit"
            and row["review"].get("input_sha256") == fingerprint
        ):
            return await view(p, row, settings)
        delivery.fail(409, "Review is immutable")
    revision(row, request)
    if row["case_runs"] or row["binding"] != binding(settings):
        delivery.fail(409, "Audit must precede inference with an unchanged binding")
    if (
        body.corpus_sha256 != row["binding"]["corpus_sha256"]
        or body.strategy_sha256 != row["binding"]["strategy_sha256"]
    ):
        delivery.fail(409, "Audit request does not match the frozen protocol")
    try:
        checked = audit(row["binding"]["protocol"])
    except (ValueError, TypeError, KeyError):
        delivery.fail(409, "Only the original fixed synthetic protocol may use automated review")
    row.update(
        review=dict(
            kind="automated_rule_audit",
            actor_id=str(p.user["id"]),
            pilot_id=str(id_),
            checked_at=now().isoformat(),
            human_reviewed=False,
            audit=checked,
            input_sha256=fingerprint,
            corpus_sha256=body.corpus_sha256,
            strategy_sha256=body.strategy_sha256,
            reason=(
                "Owner-authorized automated arithmetic check of synthetic fixtures; "
                "no personal human review."
            ),
        ),
        revision=row["revision"] + 1,
    )
    await p.conn.execute(
        pilots.update()
        .where(pilots.c.id == id_)
        .values(review=row["review"], revision=row["revision"])
    )
    await record(
        p.conn,
        request,
        p.user["id"],
        row["organization_id"],
        "selection_pilot.automated_labels_checked",
        id_,
    )
    return await view(p, row, settings)


async def snapshot(p: Principal, body: object) -> dict:
    """Resolve only frozen fixtures after live project/grant/reviewer checks, also in workers."""
    from ppm_api.modules.agents.guided_review import Choice, plan
    from ppm_api.modules.ai.schemas import AIRunInput

    assert isinstance(body, AIRunInput) and body.guided_pilot_id
    row = await get(p, body.guided_pilot_id)
    if row["project_id"] != body.project_id or not await reviewed(p, row):
        delivery.fail(403, "Pilot needs a valid label check and current access")
    if row["binding"]["corpus_sha256"] != protocol()["corpus_sha256"] or row["binding"][
        "strategy_sha256"
    ] != digest(PROMPT):
        delivery.fail(409, "Pilot strategy changed; prepare a new reviewed pilot")
    if body.guided_case_id not in {c["id"] for c in protocol()["cases"]}:
        delivery.fail(422, "Unknown fixture case")
    assert body.guided_case_id is not None
    content: dict = dict(
        sources=fixture_sources(str(body.project_id), body.guided_case_id),
        framework=None,
        answers={},
        assessment_revision=None,
        prompt_version="financial-selection-fixtures-v1",
        rule_version="financial-selection-rule-v1",
        prompt_sha256=digest(PROMPT),
        schema_sha256=digest(Choice.model_json_schema()),
        framework_version_id=None,
        start=now().date().isoformat(),
        end=now().date().isoformat(),
        selection_pilot=dict(id=str(row["id"]), case=body.guided_case_id, binding=row["binding"]),
    )
    content["hybrid_plan"] = plan(content, "financial", str(body.project_id))
    if row["review"].get("kind") == "automated_rule_audit":
        content["selection_pilot"]["review_kind"] = "automated_rule_audit"
    return content


async def measure(id_: UUID, case_id: str, request: Request, p: Principal) -> dict:
    """Queue one ordered fixture through normal AI admission; retain duplicate/failed runs."""
    from ppm_api.modules.ai import service as ai
    from ppm_api.modules.ai.schemas import AIRunInput

    await delivery.lock(p, request)
    row = await get(p, id_, True)
    if case_id in row["case_runs"]:
        return await view(p, row, request.app.state.settings)
    revision(row, request)
    current = await view(p, row, request.app.state.settings)
    if not current["binding_current"]:
        delivery.fail(
            409, "Review the frozen labels before measurement; changed bindings need a new pilot"
        )
    if any(c["status"] in {"pending", "unavailable"} for c in current["cases"]):
        delivery.fail(
            409, "Wait for the active case; unavailable attempts stop this pilot without retry"
        )
    if current["next_case_at"] and now() < current["next_case_at"]:
        delivery.fail(
            429, "Wait at least one minute between provider requests; no new case was queued"
        )
    todo = next((c for c in current["cases"] if c["status"] == "not_started"), None)
    if not todo or todo["id"] != case_id:
        delivery.fail(409, "Measure cases in protocol order; calibration precedes held-out cases")
    # A case has one durable run. Normal jobs and SQL quota admission own every network attempt.
    body = AIRunInput(
        project_id=row["project_id"],
        operation="agents",
        runtime_version="v2",
        analysis_mode="guided",
        requested_agents=["financial"],
        guided_pilot_id=id_,
        guided_case_id=case_id,
    )
    request.state.selection_case = (id_, case_id)
    run = await ai.create(body, request, p)
    row.update(case_runs=row["case_runs"] | {case_id: str(run["id"])}, revision=row["revision"] + 1)
    await p.conn.execute(
        pilots.update()
        .where(pilots.c.id == id_)
        .values(case_runs=row["case_runs"], revision=row["revision"])
    )
    return await view(p, row, request.app.state.settings)
