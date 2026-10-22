"""Validate and export authored prompt examples. Does not train/upload model weights."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "services/api")]

from ppm_api.agent_prompts import cloud_prompt  # noqa: E402
from ppm_api.agent_registry import BY_AGENT  # noqa: E402
from ppm_api.agent_validation import validate_section  # noqa: E402
from ppm_api.model_contracts import SectionOutput  # noqa: E402
from ppm_api.model_registry import canonical, digest  # noqa: E402

from scripts.benchmark_agent_runtime import fixture_context  # noqa: E402

DATA = ROOT / "tests/fixtures/agent_v2_training.json"


def examples() -> tuple[list[dict], dict]:
    corpus = json.loads(DATA.read_bytes())
    refs = {r["id"] for r in corpus["references"] if r.get("admitted") is not False}
    if corpus["schema_version"] != "agent-training-examples-v1":
        raise ValueError("Unknown training example format")
    cases = corpus["cases"]
    if len({c["id"] for c in cases}) != len(cases):
        raise ValueError("Duplicate training ID")
    counts = {agent: 0 for agent in BY_AGENT}
    result = []
    for case in cases:
        if case["split"] != "training" or not set(case["reference_ids"]) <= refs:
            raise ValueError("Training/evaluation or provenance mismatch")
        if case["task_class"] != BY_AGENT[case["agent"]].task_class:
            raise ValueError("Incorrect training role")
        node, context = fixture_context(case)
        output = SectionOutput.model_validate(case["expected_output"])
        validate_section(node, context, output)
        counts[case["agent"]] += 1
        result.append(
            dict(
                id=case["id"],
                agent=case["agent"],
                label_status=case["label_status"],
                reference_ids=case["reference_ids"],
                messages=[
                    dict(role="system", content=cloud_prompt(case["agent"], node["mode"])),
                    dict(role="user", content=context["payload"]),
                    dict(role="assistant", content=canonical(case["expected_output"])),
                ],
            )
        )
    if any(count != 4 for count in counts.values()):
        raise ValueError("Four authored examples per role required")
    return result, dict(
        schema_version="training-example-validation-v1",
        examples=len(result),
        role_counts=counts,
        corpus_sha256=digest(corpus),
        hard_output_checks="passed",
        labels_independently_reviewed=False,
        model_weights_trained=False,
        model_requests=0,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows, report = examples()
    if args.output:
        if not args.output.resolve().is_relative_to((ROOT / "artifacts/local").resolve()):
            raise SystemExit("Private export path required")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            for row in rows:
                stream.write(canonical(row) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
