"""Export synthetic labels separately from measured candidates for the nominated reviewer."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from scripts.benchmark_agent_runtime import (  # noqa: E402
    CLOUD_CORPUS,
    CORPUS,
    PRIVATE,
    load_corpus,
    write_new,
)
from scripts.benchmark_cloud_batches import strategy_hash  # noqa: E402
from scripts.score_agent_benchmark import review_template  # noqa: E402


def prepare(folder: Path) -> dict:
    """Export separate labels, historical candidates and unapproved review templates."""
    corpus, corpus_hash = load_corpus(CLOUD_CORPUS)
    folder.mkdir(parents=True, exist_ok=True)
    write_new(folder / "labels.json", corpus)
    template = review_template(corpus, corpus_hash)
    template["schema_version"] = "cloud-review-v1"
    template["strategy_sha256"] = strategy_hash()
    template["provider"] = None
    template["label_approval_sha256"] = None
    template["label_review"] = dict(
        id=None,
        reviewer=None,
        independent=False,
        approved_at=None,
        reviewed_before_held_out_inference=False,
    )
    template["instructions"] = (
        "Review labels.json before opening candidates.json. Record independent "
        "label approval before any held-out inference. Then use one copy of this template per "
        "provider, bind exact report/candidate hashes and rate claims, relevance, omissions and "
        "abstention. Historical calibration and multiple prompt versions do not qualify a model. "
        "Do not fill correct counts from hard-check success or another model's agreement."
    )
    write_new(folder / "review-template.json", template)
    write_new(
        folder / "label-approval-template.json",
        {key: template[key] for key in ("corpus_sha256", "strategy_sha256", "label_review")},
    )
    historical, _ = load_corpus(CORPUS)
    write_new(folder / "calibration-inputs.json", historical)
    candidates = []
    for path in sorted(
        (ROOT / "docs/verification/sprint11_1/implementation").glob("*-repair-*.json")
    ):
        report = json.loads(path.read_bytes())
        if report.get("schema_version") != "cloud-batch-calibration-v1":
            continue
        for attempt in report["attempts"]:
            item = dict(
                report=path.name,
                report_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                provider=report["provider"],
                model=report["model"],
                cases=attempt["cases"],
                prompt_sha256=report["prompt_sha256"],
                attempt=attempt,
                output=None,
            )
            if attempt.get("candidate_sha256"):
                candidate = PRIVATE / ("cloud-candidate-" + attempt["attempt_id"] + ".json")
                if (
                    hashlib.sha256(candidate.read_bytes()).hexdigest()
                    != attempt["candidate_sha256"]
                ):
                    raise ValueError("Candidate changed")
                value = json.loads(candidate.read_bytes())
                item["output"] = json.loads(value["text"])
            candidates.append(item)
    write_new(
        folder / "candidates.json",
        dict(status="calibration_only_unreviewed", candidates=candidates),
    )
    return dict(
        cases=len(corpus["cases"]),
        held_out=sum(c["split"] == "held_out" for c in corpus["cases"]),
        measured_requests=len(candidates),
        independent_label_approval=False,
        model_requests=0,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.output)))
    except Exception:
        raise SystemExit("BLOCKED review export; existing files retained") from None
