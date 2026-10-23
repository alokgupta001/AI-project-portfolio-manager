"""Deterministic hard gates. A valid citation is identity evidence, not semantic proof."""

import re
import unicodedata
from decimal import Decimal

from ppm_api.model_contracts import ModelFailure, SectionOutput
from ppm_api.model_registry import digest

PREDICATES = {
    "financial": {"budget_overrun", "risk_present", "no_adverse_evidence"},
    "schedule": {"schedule_late", "dependency_unresolved", "delivery_blocked", "risk_present"},
    "risk": {"risk_present", "delivery_blocked", "dependency_unresolved"},
    "resource": {"capacity_exceeded", "risk_present"},
    "governance": {"policy_gap", "rubric_gap", "practice_gap", "no_adverse_evidence"},
    "agile_coach": {"practice_gap", "delivery_blocked", "risk_present"},
}


def numbers(text: str) -> set[Decimal]:
    """Extract normalized numerical tokens used to reject unsupported quantities."""
    return {Decimal(n) for n in re.findall(r"(?<![a-zA-Z])[-+]?\d+(?:\.\d+)?", text)}


def validate_section(node: dict, context: dict, output: SectionOutput) -> dict:
    """Check role scope, aliases, spans, quantities and coverage before acceptance."""
    if output.section != node["key"] or output.mode != node["mode"]:
        raise ModelFailure("INVALID_OUTPUT", "completed")
    known = set(context["evidence"]) | set(context["questions"]) | set(context["basis"])
    declared = set(output.covered) | {g.item for g in output.gaps}
    if not declared <= known or not declared <= set(context["required_aliases"]):
        raise ModelFailure("INVALID_OUTPUT", "completed")
    allowed_numbers = set()
    for source in context["evidence"].values():
        allowed_numbers |= numbers(source["text"])
    findings, matches = [], []

    def spans(refs: list) -> list[dict]:
        """Resolve evidence aliases and reject out-of-range or unauthorized spans."""
        result = []
        for ref in refs:
            source = context["evidence"].get(ref.e)
            if not source or not 0 <= ref.start < ref.end <= len(source["text"]):
                raise ModelFailure("INVALID_OUTPUT", "completed")
            result.append(dict(source=source["source"], start=ref.start, end=ref.end))
        return result

    def item(claim: str, advice: str, refs: list, **extra: object) -> dict:
        """Validate a finding's role predicate, source support and numerical claims."""
        if not (numbers(claim) | numbers(advice)) <= allowed_numbers:
            raise ModelFailure("INVALID_OUTPUT", "completed")
        # Equal digits elsewhere cannot prove matching units, periods or causality.
        # Numerical prose must be an exact cited statement; the canonical baseline
        # carries calculated quantities. Free interpretation can refer to it in words.
        quoted = [
            context["evidence"][r.e]["text"][r.start : r.end]
            for r in refs
            if r.e in context["evidence"]
        ]
        if any(
            numbers(text) and not any(text in quote for quote in quoted) for text in (claim, advice)
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        return dict(
            title=claim,
            improvement=advice,
            spans=spans(refs),
            confidence=None,
            agents=[node["agent"]],
            discrepancy=False,
            conflicts=[],
            semantic_status="unreviewed",
            **extra,
        )

    for finding in output.findings:
        if node["agent"] in ("financial", "resource") and (
            any(c.isdigit() for text in (finding.claim, finding.advice) for c in text)
            or not {r.e for r in finding.spans} <= set(context["required_aliases"])
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        if finding.subject not in context["subjects"] or finding.predicate not in PREDICATES.get(
            node["agent"], set()
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        if finding.predicate == "no_adverse_evidence" and finding.signal == "adverse":
            raise ModelFailure("INVALID_OUTPUT", "completed")
        metric_keys = {
            "budget_overrun": {"usage", "variance", "financial_risk"},
            "schedule_late": {"schedule_risk", "critical"},
            "capacity_exceeded": {"capacity_risk"},
            "risk_present": {
                "risk",
                "critical",
                "financial_risk",
                "schedule_risk",
                "capacity_risk",
            },
        }.get(finding.predicate, set())
        if finding.predicate == "no_adverse_evidence" and node["agent"] == "financial":
            metric_keys = {"usage", "variance", "financial_risk"}
        adverse_metric = any(
            s.get("metric", {}).get("key") in metric_keys
            and s["metric"]["value"] is not None
            and Decimal(str(s["metric"]["value"])) > (100 if s["metric"]["key"] == "usage" else 0)
            for s in context["evidence"].values()
        )
        if finding.signal == "clear" and adverse_metric:
            raise ModelFailure("INVALID_OUTPUT", "completed")
        value = item(
            finding.claim,
            finding.advice,
            finding.spans,
            kind=finding.kind,
            signal=finding.signal,
            severity=finding.severity,
            epistemic=finding.epistemic,
            predicate=finding.predicate,
            basis=[],
        )
        value["key"] = digest(
            [
                "claim-v2",
                context["subjects"][finding.subject]["scope"],
                finding.predicate,
                finding.signal,
                " ".join(unicodedata.normalize("NFC", finding.claim).split()),
                sorted(value["spans"], key=lambda s: (s["source"], s["start"], s["end"])),
                sorted(s["sha256"] for s in context["evidence"].values()),
            ]
        )[:32]
        findings.append(value)
    seen = set()
    for match in output.matches:
        question = context["questions"].get(match.question)
        if not question or match.question in seen:
            raise ModelFailure("INVALID_OUTPUT", "completed")
        seen.add(match.question)
        q = question["rubric"]
        levels = (
            [0, 1] if q["answer_type"] == "boolean" else [v["level"] for v in q["rubric_levels"]]
        )
        refs = spans(match.spans)
        if match.level not in levels or not any(
            s["source"] == "answer:" + question["id"] for s in refs
        ):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        matches.append(
            dict(question_id=question["id"], level=match.level, spans=refs, confidence="0")
        )
    for narrative in output.narrative:
        if any(key not in context["basis"] for key in narrative.basis):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        bases = [context["basis"][key] for key in narrative.basis]
        allowed_sources = {s["source"] for b in bases for s in b["spans"]}
        refs = spans(narrative.spans)
        if not all(s["source"] in allowed_sources for s in refs):
            raise ModelFailure("INVALID_OUTPUT", "completed")
        value = item(
            narrative.claim,
            narrative.advice,
            narrative.spans,
            kind=bases[0].get("kind", "blocker"),
            signal="uncertain",
            severity=bases[0].get("severity", "low"),
            epistemic=narrative.epistemic,
            predicate="practice_gap",
            basis=[b["key"] for b in bases],
        )
        value["key"] = digest([node["agent"], value["title"], value["spans"], value["basis"]])[:32]
        findings.append(value)
    required = set(context["required_aliases"])
    covered = set(output.covered) & required
    if output.outcome == "supported":
        cited = (
            {r.e for f in output.findings for r in f.spans}
            | {r.e for m in output.matches for r in m.spans}
            | {r.e for n in output.narrative for r in n.spans}
        )
        if output.mode == "findings" and not covered <= cited:
            raise ModelFailure("INVALID_OUTPUT", "completed")
        if output.mode == "rubric" and not covered <= seen:
            raise ModelFailure("INVALID_OUTPUT", "completed")
        if output.mode == "synthesis" and not covered <= {
            b for n in output.narrative for b in n.basis
        }:
            raise ModelFailure("INVALID_OUTPUT", "completed")
    complete = bool(required) and covered == required and not output.gaps
    return dict(
        findings=findings,
        matches=matches,
        covered_ids=node["required_ids"] if complete else [],
        validation=dict(
            outcome="validated" if complete else "partially_validated",
            hard_checks="passed",
            semantic_status="unreviewed",
            required_aliases=sorted(required),
            covered_aliases=sorted(covered),
            limitations=["Citations prove identity; interpretation remains provisional"],
        ),
        outcome=output.outcome,
    )


def reconcile(items: list[dict]) -> list[dict]:
    """Merge equivalent findings while retaining unresolved interpretation conflicts."""
    merged: dict[str, dict] = {}
    for raw in items:
        value = dict(raw)
        key = value["key"]
        if key in merged:
            merged[key]["agents"] = sorted(set(merged[key]["agents"] + value["agents"]))
        else:
            merged[key] = value
    for key, item in merged.items():
        item["conflicts"] = [
            other_key
            for other_key, other in merged.items()
            if key != other_key
            and other.get("predicate") == item.get("predicate")
            and {other["signal"], item["signal"]} == {"adverse", "clear"}
            and any(a == b for a in item["spans"] for b in other["spans"])
        ]
        item["discrepancy"] |= bool(item["conflicts"])
    return sorted(
        merged.values(), key=lambda v: ({"high": 0, "medium": 1, "low": 2}[v["severity"]], v["key"])
    )
