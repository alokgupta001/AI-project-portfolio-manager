"""Nine business roles. Python owns facts/control; interpretation is selected on demand."""

from dataclasses import dataclass

from ppm_api.model_contracts import AgentId, SectionMode, TaskClass


@dataclass(frozen=True)
class Capability:
    agent: AgentId
    task_class: TaskClass
    categories: tuple[str, ...]
    modes: tuple[SectionMode, ...] = ("findings",)
    execution_policy: str = "hybrid_on_demand"
    deterministic_handler: str = "canonical_baseline"
    interpretation_handler: str = "validated_section"


REGISTRY = (
    Capability(
        "financial",
        "financial_interpretation",
        (
            "metric:budget",
            "metric:spend",
            "metric:usage",
            "metric:financial_risk",
            "document:project",
            "record:risks",
            "record:blockers",
        ),
    ),
    Capability(
        "schedule",
        "schedule_interpretation",
        (
            "metric:variance",
            "metric:schedule_risk",
            "metric:critical",
            "record:dependencies",
            "record:blockers",
            "document:project",
            "document:sprint_report",
        ),
    ),
    Capability("sentiment", "team_support_advice", ("group:blockers",), ("synthesis",)),
    Capability(
        "risk",
        "risk_extraction",
        (
            "metric:risk",
            "record:risks",
            "record:blockers",
            "document:project",
        ),
    ),
    Capability("resource", "resource_interpretation", ("metric:capacity_risk",)),
    Capability(
        "governance",
        "governance_interpretation",
        (
            "document:policy",
            "assessment:answer",
            "assessment:rubric",
        ),
        ("findings", "rubric"),
    ),
    Capability(
        "agile_coach",
        "agile_advice",
        (
            "record:sprints",
            "document:sprint_report",
            "assessment:answer",
            "assessment:rubric",
        ),
    ),
    Capability(
        "pmo",
        "portfolio_synthesis",
        (
            "metric:risk",
            "metric:critical",
            "metric:financial_risk",
            "record:dependencies",
        ),
        ("synthesis",),
    ),
    Capability(
        "executive",
        "executive_synthesis",
        (
            "metric:risk",
            "metric:health",
            "metric:critical",
            "metric:usage",
        ),
        ("synthesis",),
    ),
)
BY_AGENT = {entry.agent: entry for entry in REGISTRY}
DOMAIN = tuple(entry.agent for entry in REGISTRY[:7])
SYNTHESIS = ("pmo", "executive")


def definitions() -> list[dict]:
    return [
        dict(
            agent=c.agent,
            inputs=list(c.categories),
            tools=["read_authorized_snapshot", "cite_exact_span"],
            timeout_seconds=22,
            fallback="Canonical baseline; requested interpretation remains separate",
            output_schema="SectionOutput",
            execution_policy=c.execution_policy,
            task_class=c.task_class,
            modes=list(c.modes),
        )
        for c in REGISTRY
    ]
