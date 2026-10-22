"""Score bound cloud measurements and independent review; never activate a provider."""

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from ppm_api.agent_batch import batch_prompt, normalize, validate_batch  # noqa: E402
from ppm_api.agent_prompts import ROLE_PROVIDERS  # noqa: E402
from ppm_api.model_contracts import ModelResult  # noqa: E402
from ppm_api.model_qualification import ClassMeasurement, CloudQualificationReport  # noqa: E402
from ppm_api.model_registry import digest  # noqa: E402

from scripts.benchmark_agent_runtime import (  # noqa: E402
    CLOUD_CORPUS,
    PRIVATE,
    load_corpus,
    write_new,
)
from scripts.benchmark_cloud_batches import fixture_batch, strategy_hash  # noqa: E402
from scripts.prepare_cloud_acceptance import approval  # noqa: E402
from scripts.score_agent_benchmark import sha  # noqa: E402


def score(
    corpus: dict,
    corpus_hash: str,
    review: dict,
    reports: list[dict],
    folder: Path = PRIVATE,
    label_approval_path: Path | None = None,
) -> CloudQualificationReport:
    label = review["label_review"]
    if (
        review.get("schema_version") != "cloud-review-v1"
        or review.get("corpus_sha256") != corpus_hash
        or review.get("strategy_sha256") != strategy_hash()
        or label.get("independent") is not True
        or label.get("reviewed_before_held_out_inference") is not True
        or not isinstance(label.get("id"), str)
        or not label["id"].strip()
        or not isinstance(label.get("reviewer"), str)
        or not label["reviewer"].strip()
    ):
        raise ValueError("Independent label approval missing")
    if label_approval_path is None:
        raise ValueError("Bound label approval file required")
    frozen = approval(label_approval_path, corpus_hash, strategy_hash())
    if (
        frozen["label_review"] != label
        or sha(label_approval_path) != review["label_approval_sha256"]
    ):
        raise ValueError("Label approval binding changed")
    approved = datetime.fromisoformat(label["approved_at"])
    if approved.tzinfo is None or not reports:
        raise ValueError("Dated approval and measurements required")
    first = reports[0]
    provider = review["provider"]
    if provider not in set(ROLE_PROVIDERS.values()):
        raise ValueError("Unknown provider")
    by_case = {c["id"]: c for c in corpus["cases"]}
    attempts, latencies, reported_ids, shapes = {}, {}, set(), set()
    for report in reports:
        if any(
            report.get(k) != v
            for k, v in dict(
                schema_version="cloud-batch-calibration-v1",
                provider=provider,
                model=first["model"],
                corpus_sha256=corpus_hash,
                strategy_sha256=strategy_hash(),
                label_approval_sha256=review["label_approval_sha256"],
                max_output_tokens=first["max_output_tokens"],
                context_tokens=first["context_tokens"],
            ).items()
        ):
            raise ValueError("Mixed measurement strategy or identity")
        cases = [by_case[c] for c in report["selected_cases"]]
        if any(ROLE_PROVIDERS[c["agent"]] != provider for c in cases):
            raise ValueError("Cross-provider comparison cannot qualify an assigned runtime")
        node, ctx = fixture_batch(cases)
        if report["prompt_sha256"] != digest(batch_prompt(node)) or report[
            "request_sha256"
        ] != digest([batch_prompt(node), ctx["payload"], ctx["schema"]]):
            raise ValueError("Request binding changed")
        for attempt in report["attempts"]:
            aid = attempt["attempt_id"]
            if (
                aid in attempts
                or attempt.get("code")
                or attempt["cases"] != report["selected_cases"]
            ):
                raise ValueError("Duplicate, failed or mismatched measurement")
            if (
                any(c["split"] == "held_out" for c in cases)
                and datetime.fromisoformat(attempt["admitted_at"]) <= approved
            ):
                raise ValueError("Held-out inference predates label approval")
            path = folder / ("cloud-candidate-" + aid + ".json")
            if (
                not path.resolve().is_relative_to(folder.resolve())
                or sha(path) != attempt["candidate_sha256"]
            ):
                raise ValueError("Candidate fingerprint mismatch")
            result = ModelResult.model_validate_json(path.read_bytes())
            if (
                str(result.attempt_id) != aid
                or result.provider_id != provider
                or result.model_id != first["model"]
                or result.completion != "complete"
                or result.usage.output_tokens is None
                or result.usage.output_tokens + (result.usage.reasoning_tokens or 0) > 512
            ):
                raise ValueError("Unbounded or mismatched result")
            values = json.loads(result.text)
            validate_batch(node, ctx, values)
            attempts[aid] = (attempt, cases, node, ctx, values)
            latencies[aid] = result.latency_ms / 1000
            reported_ids.add(result.reported_model_id or result.model_id)
            shapes.add(tuple(sorted(c["agent"] for c in cases)))
    history = json.loads((folder / (provider + "-specialist-ledger.json")).read_bytes())
    bound = {
        row["attempt_id"]
        for row in history
        if row.get("phase") == "acceptance-v1"
        and row.get("corpus_sha256") == corpus_hash
        and row.get("strategy_sha256") == strategy_hash()
        and row.get("model") == first["model"]
        and row.get("label_approval_sha256") == review["label_approval_sha256"]
    }
    if not bound or set(attempts) != bound:
        raise ValueError("All bound acceptance attempts, including failures, must be supplied")
    grouped = {}
    seen = set()
    for row in review["cases"]:
        if row["attempt_id"] is None:
            continue
        cid = row["case"]
        if cid in seen:
            raise ValueError("Duplicate case")
        seen.add(cid)
        case = by_case[cid]
        attempt, cases, node, ctx, values = attempts[row["attempt_id"]]
        if cid not in attempt["cases"] or row["candidate_sha256"] != attempt["candidate_sha256"]:
            raise ValueError("Review not bound to candidate")
        member = next(m for m in node["members"] if m["agent"] == case["agent"])
        output = normalize(member, ctx["members"][case["agent"]], values[case["agent"]])
        for key in (
            "correct_claims",
            "recalled_items",
            "supported_added_interpretations",
            "citation_errors",
            "unsupported_numbers",
            "privacy_or_control_errors",
            "material_omissions",
        ):
            if type(row[key]) is not int or not 0 <= row[key] <= 20:
                raise ValueError("Missing finite reviewer count")
        for key in ("correct_abstention", "canonical_preserved", "advice_relevant"):
            if type(row[key]) is not bool:
                raise ValueError("Missing reviewer judgment")
        emitted = len(output.findings) + len(output.matches) + len(output.narrative)
        if (
            not isinstance(row["review_note"], str)
            or not row["review_note"].strip()
            or row["correct_claims"] > emitted
            or row["recalled_items"] > case["labels"]["supported_items"]
            or row["supported_added_interpretations"] > row["correct_claims"]
            or row["correct_claims"]
            and (not row["advice_relevant"] or row["material_omissions"])
            or row["correct_abstention"]
            and (emitted or output.outcome == "supported")
        ):
            raise ValueError("Inconsistent review")
        grouped.setdefault(case["task_class"], []).append((case, row, emitted))
    measurements = []
    for task_class, items in grouped.items():
        totals = {
            key: sum(r[key] for _, r, _ in items)
            for key in (
                "correct_claims",
                "recalled_items",
                "supported_added_interpretations",
                "citation_errors",
                "unsupported_numbers",
                "privacy_or_control_errors",
            )
        }
        measurements.append(
            ClassMeasurement(
                task_class=task_class,
                labeled_cases=len(items),
                held_out_cases=sum(c["split"] == "held_out" for c, _, _ in items),
                supported_items=sum(c["labels"]["supported_items"] for c, _, _ in items),
                emitted_claims=sum(n for _, _, n in items),
                abstention_cases=sum(c["labels"]["abstention_required"] for c, _, _ in items),
                correct_abstentions=sum(
                    c["labels"]["abstention_required"] and r["correct_abstention"]
                    for c, r, _ in items
                ),
                canonical_checks=len(items),
                canonical_preserved=sum(r["canonical_preserved"] for _, r, _ in items),
                **totals,
            )
        )
    groups = [
        ["financial", "schedule", "resource"],
        ["risk", "governance", "agile_coach"],
        ["sentiment", "pmo"],
        ["executive"],
    ]
    expected = [g for g in groups if all(ROLE_PROVIDERS[a] == provider for a in g)]
    times = sorted(latencies.values())
    if not times:
        raise ValueError("No measured calls")
    return CloudQualificationReport(
        provider=provider,
        model=first["model"],
        reported_model_ids=sorted(reported_ids),
        corpus_sha256=corpus_hash,
        strategy_sha256=strategy_hash(),
        independent_label_review_id=label["id"],
        measurement_reports=review["reports"],
        context_tokens=first["context_tokens"],
        output_tokens=first["max_output_tokens"],
        measured_calls=len(times),
        p95_seconds=times[math.ceil(0.95 * len(times)) - 1],
        failed_or_unknown_calls=0,
        observed_runtime_batches=[list(v) for v in sorted(shapes)],
        expected_runtime_batches=expected,
        classes=measurements,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--review", type=Path, required=True)
    p.add_argument("--reports", type=Path, nargs="+", required=True)
    p.add_argument("--label-approval", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        corpus, corpus_hash = load_corpus(CLOUD_CORPUS)
        review = json.loads(args.review.read_bytes())
        if review["reports"] != [sha(path) for path in args.reports]:
            raise ValueError("Reports changed")
        result = score(
            corpus,
            corpus_hash,
            review,
            [json.loads(p.read_bytes()) for p in args.reports],
            label_approval_path=args.label_approval,
        )
        write_new(args.output, result.model_dump(mode="json"))
        print("Classes passing gates: " + (", ".join(result.qualified_classes()) or "none"))
        print("No profile activated.")
    except Exception:
        raise SystemExit(
            "BLOCKED incomplete or unbound cloud review/measurements; no promotion"
        ) from None
