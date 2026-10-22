"""Check an operator's measured benchmark report offline; never activate a model."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "services/api"))

from ppm_api.model_qualification import CloudQualificationReport, QualificationReport  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        raw = args.report.read_bytes()
        if len(raw) > 64000:
            raise ValueError
        data = json.loads(raw)
        report = (
            CloudQualificationReport
            if data.get("schema_version") == "cloud-qualification-v1"
            else QualificationReport
        ).model_validate(data)
        qualified = report.qualified_classes()
    except Exception:
        raise SystemExit("BLOCKED invalid or unavailable measurement report") from None
    print("Measured classes passing configured gates: " + (", ".join(qualified) or "none"))
    print(
        "No profile was changed. Operator must verify report provenance before explicit promotion."
    )
    if not qualified:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
