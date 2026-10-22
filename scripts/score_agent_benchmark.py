"""Build a qualification report from measured runs and independent, bound human review.

This cannot approve labels, invent missing ratings, or activate a profile. Reviewers
must inspect the underlying evidence and advice; a citation alone is not support.
"""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from ppm_api.agent_validation import validate_section  # noqa: E402
from ppm_api.model_contracts import ModelResult, SectionOutput  # noqa: E402
from ppm_api.model_qualification import ClassMeasurement, QualificationReport  # noqa: E402

from scripts.benchmark_agent_runtime import (  # noqa: E402
    CORPUS,
    PRIVATE,
    fixture_context,
    load_corpus,
    write_new,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def review_template(corpus: dict, corpus_hash: str) -> dict:
    return dict(
        schema_version="benchmark-review-v1",
        corpus_sha256=corpus_hash,
        label_review=dict(
            id=None, reviewer=None, independent=False, reviewed_before_inference=False
        ),
        reports=[],
        instructions="Review labels before inference. For each chosen candidate inspect evidence, "
        "claim, advice relevance, omissions, conflicts and canonical values. "
        "Do not infer correctness from real spans or another model's agreement.",
        cases=[
            dict(
                case=c["id"],
                attempt_id=None,
                candidate_sha256=None,
                correct_claims=None,
                recalled_items=None,
                correct_abstention=None,
                canonical_preserved=None,
                supported_added_interpretations=None,
                citation_errors=None,
                unsupported_numbers=None,
                privacy_or_control_errors=None,
                advice_relevant=None,
                material_omissions=None,
                review_note=None,
            )
            for c in corpus["cases"]
        ],
    )


def score(
    corpus: dict, corpus_hash: str, review: dict, reports: list[dict], folder: Path = PRIVATE
) -> QualificationReport:
    label = review["label_review"]
    if (
        review["schema_version"] != "benchmark-review-v1"
        or review["corpus_sha256"] != corpus_hash
        or label["independent"] is not True
        or label["reviewed_before_inference"] is not True
        or not isinstance(label["id"], str)
        or not label["id"].strip()
        or not isinstance(label["reviewer"], str)
        or not label["reviewer"].strip()
    ):
        raise ValueError("Independent label review is missing")
    if not reports or any(r["schema_version"] != "agent-benchmark-v1" for r in reports):
        raise ValueError("Measured reports required")
    identities = {
        (
            r["model_digest"],
            r["corpus_sha256"],
            r["prompt_sha256"],
            r["context_tokens"],
            r["output_tokens"],
            r.get("hardware_record_sha256"),
        )
        for r in reports
    }
    if len(identities) != 1 or reports[0]["corpus_sha256"] != corpus_hash:
        raise ValueError("Cannot merge different models, prompts, corpora, hardware or profiles")
    attempts = {}
    all_attempts = []
    for report in reports:
        for row in report["attempts"]:
            if row.get("code"):
                raise ValueError("Failed attempts prevent operational qualification")
            if row["attempt_id"] in attempts:
                raise ValueError("Duplicate attempt across reports")
            attempts[row["attempt_id"]] = row
            all_attempts.append(row)
    by_case = {c["id"]: c for c in corpus["cases"]}
    rows = review["cases"]
    if len({r["case"] for r in rows}) != len(rows) or any(r["case"] not in by_case for r in rows):
        raise ValueError("Duplicate or unknown case review")
    grouped: dict[str, list[dict]] = {}
    seen = set()
    for rating in rows:
        if rating["attempt_id"] is None:
            continue
        case = by_case[rating["case"]]
        attempt = attempts[rating["attempt_id"]]
        if attempt["case"] != case["id"] or attempt["timing_only"] or attempt["attempt_id"] in seen:
            raise ValueError("Review is not bound to one quality candidate")
        seen.add(attempt["attempt_id"])
        candidate = folder / (str(attempt["attempt_id"]) + ".json")
        if (
            not candidate.resolve().is_relative_to(folder.resolve())
            or sha(candidate) != rating["candidate_sha256"]
            or sha(candidate) != attempt["candidate_sha256"]
        ):
            raise ValueError("Candidate fingerprint mismatch")
        result = ModelResult.model_validate_json(candidate.read_bytes())
        output = SectionOutput.model_validate_json(result.text)
        if result.completion != "complete" or str(result.attempt_id) != attempt["attempt_id"]:
            raise ValueError("Incomplete or mismatched candidate")
        node, context = fixture_context(case)
        validate_section(node, context, output)
        for name in (
            "correct_claims",
            "recalled_items",
            "supported_added_interpretations",
            "citation_errors",
            "unsupported_numbers",
            "privacy_or_control_errors",
            "material_omissions",
        ):
            if type(rating[name]) is not int or not 0 <= rating[name] <= 20:
                raise ValueError("Missing finite count")
        for name in ("correct_abstention", "canonical_preserved", "advice_relevant"):
            if type(rating[name]) is not bool:
                raise ValueError("Missing review decision")
        if not isinstance(rating["review_note"], str) or not rating["review_note"].strip():
            raise ValueError("Evidence review note required")
        emitted = len(output.findings) + len(output.matches) + len(output.narrative)
        if (
            rating["correct_claims"] > emitted
            or rating["recalled_items"] > case["labels"]["supported_items"]
            or rating["supported_added_interpretations"] > rating["correct_claims"]
            or (not rating["advice_relevant"] or rating["material_omissions"])
            and rating["correct_claims"]
        ):
            raise ValueError("Inconsistent review denominator or advice/omission judgment")
        if rating["correct_abstention"] and (emitted or output.outcome == "supported"):
            raise ValueError("Emitted claims are not an abstention")
        grouped.setdefault(case["task_class"], []).append(
            dict(
                case=case,
                rating=rating,
                emitted=emitted,
            )
        )
    measurements = []
    for task_class, rated in grouped.items():

        def total(key: str, rated: list = rated) -> int:
            return sum(r["rating"][key] for r in rated)

        measurements.append(
            ClassMeasurement(
                task_class=task_class,
                labeled_cases=len(rated),
                held_out_cases=sum(r["case"]["split"] == "held_out" for r in rated),
                supported_items=sum(r["case"]["labels"]["supported_items"] for r in rated),
                emitted_claims=sum(r["emitted"] for r in rated),
                correct_claims=total("correct_claims"),
                recalled_items=total("recalled_items"),
                abstention_cases=sum(r["case"]["labels"]["abstention_required"] for r in rated),
                correct_abstentions=sum(
                    r["rating"]["correct_abstention"] and r["case"]["labels"]["abstention_required"]
                    for r in rated
                ),
                canonical_checks=len(rated),
                canonical_preserved=total("canonical_preserved"),
                supported_added_interpretations=total("supported_added_interpretations"),
                citation_errors=total("citation_errors"),
                unsupported_numbers=total("unsupported_numbers"),
                privacy_or_control_errors=total("privacy_or_control_errors"),
            )
        )
    samples = [s for a in all_attempts for s in a.get("samples", [])]
    warm = [
        a["end_to_end_seconds"]
        for a in all_attempts
        if a["timing_only"] and not a["cold"] and not a.get("code")
    ]
    cold = [a["end_to_end_seconds"] for a in all_attempts if a["cold"]]
    if not warm or not cold or not samples:
        raise ValueError("Cold, warm and host measurements are required")
    # Resource failures are never removed by selecting only successful semantic candidates.
    warm.sort()
    first = reports[0]
    return QualificationReport(
        model_digest=first["model_digest"],
        hardware_record_sha256=first["hardware_record_sha256"],
        corpus_sha256=corpus_hash,
        independent_label_review_id=label["id"],
        context_tokens=first["context_tokens"],
        output_tokens=first["output_tokens"],
        warm_repeats=len(warm),
        p95_warm_seconds=warm[math.ceil(len(warm) * 0.95) - 1],
        cold_seconds=max(cold),
        minimum_host_headroom_mb=min(s["available_mb"] for s in samples),
        peak_model_mb=max(s["ollama_rss_mb"] for s in samples),
        out_of_memory_events=sum(a.get("code") == "LOCAL_RESOURCE" for a in all_attempts),
        maximum_simultaneous_generations=1,
        classes=measurements,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", action="store_true")
    parser.add_argument("--review", type=Path)
    parser.add_argument("--reports", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        corpus, corpus_hash = load_corpus(CORPUS)
        if args.template:
            write_new(args.output, review_template(corpus, corpus_hash))
            print("Draft review template written; no qualification or model call.")
            return
        review = json.loads(args.review.read_bytes())
        paths = args.reports or []
        if review["reports"] != [sha(p) for p in paths]:
            raise ValueError("Reviewed report fingerprints do not match")
        report = score(corpus, corpus_hash, review, [json.loads(p.read_bytes()) for p in paths])
        write_new(args.output, report.model_dump(mode="json"))
        print(
            "Classes passing measured gates: " + (", ".join(report.qualified_classes()) or "none")
        )
        print("No model profile was changed.")
    except Exception:
        raise SystemExit(
            "BLOCKED incomplete measurements or independent review; no promotion"
        ) from None


if __name__ == "__main__":
    main()
