"""Check every prior sprint's canonical documentation and retained acceptance boundaries."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []
    artifacts = 0
    sprint_ids = [f"{number:02d}" for number in range(11)] + ["8.1"]
    for sprint_id in sprint_ids:
        state = "completed"
        home = ROOT / f"docs/03-sprints/{state}/sprint-{sprint_id}"
        required = [home / name for name in ("README.md", "SPRINT_REPORT.md", "HANDOFF.md")]
        required.extend(
            ROOT / f"docs/{topic}/sprint-based/sprint-{sprint_id}/README.md"
            for topic in ("02-learning", "04-testing", "05-demos")
        )
        plain_state = "completed"
        required.append(
            ROOT / f"docs/11-plain-language-sprint-reports/{plain_state}/SPRINT-{sprint_id}.md"
        )
        if sprint_id == "8.1":
            required.extend(
                home / name for name in ("SPRINT_8_1_USER_GUIDE.md", "SPRINT_8_1_USER_GUIDE.docx")
            )
            required.extend(
                ROOT / f"docs/04-testing/sprint-based/sprint-8.1/PPM-81-{task:03d}.md"
                for task in range(1, 11)
            )
        else:
            required.append(
                ROOT / f"docs/04-testing/sprint-based/sprint-{sprint_id}/TESTING_REPORT.md"
            )
        for path in required:
            artifacts += 1
            if not path.is_file() or not path.stat().st_size:
                errors.append(
                    "Missing or empty prior-sprint artifact: " + str(path.relative_to(ROOT))
                )
            elif path.suffix == ".md" and not path.read_text(encoding="utf-8-sig").strip():
                errors.append("Empty Markdown artifact: " + str(path.relative_to(ROOT)))
        for other in {"active", "planned", "completed"} - {state}:
            if (ROOT / f"docs/03-sprints/{other}/sprint-{sprint_id}/README.md").exists():
                errors.append(f"Duplicate canonical sprint home: {sprint_id} ({other})")
    current_docs = (
        "README.md",
        "ANTIGRAVITY.md",
        "docs/README.md",
        "docs/00-overview/CURRENT_STATUS.md",
        "docs/09-planning/README.md",
        "docs/03-sprints/completed/sprint-10/README.md",
    )
    stale = ("real provider BLOCKED", "mocks/fallback only", "Sprints 10–23 remain planned")
    for relative in current_docs:
        text = (ROOT / relative).read_text(encoding="utf-8-sig").split("## Historical", 1)[0]
        if any(term.lower() in text.lower() for term in stale):
            errors.append("Stale current provider/sprint availability in " + relative)
    guide = (ROOT / "docs/07-setup-and-deployment/GEMINI-FREE-TIER.md").read_text(encoding="utf-8")
    if "does not expire" not in guide or "$0" not in guide:
        errors.append("Gemini guide must document non-expiring confirmation and $0 authorization")
    if not (ROOT / "docs/10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md").is_file():
        errors.append("Missing prior-sprint documentation closure")
    for relative in (
        "docs/10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md",
        "docs/09-planning/RELEASE-ACCEPTANCE-REGISTER.md",
        "docs/verification/sprint-8.1-10-closeout.json",
    ):
        if not (ROOT / relative).is_file():
            errors.append("Missing sprint closeout evidence: " + relative)
    for sprint_id in ("8.1", "10"):
        text = (ROOT / f"docs/03-sprints/completed/sprint-{sprint_id}/README.md").read_text(
            encoding="utf-8"
        )
        if "COMPLETED" not in text:
            errors.append("Completed sprint lacks explicit disposition: " + sprint_id)
        if (
            ROOT / f"docs/11-plain-language-sprint-reports/in-progress/SPRINT-{sprint_id}.md"
        ).exists():
            errors.append("Stale in-progress ordinary-language sprint report: " + sprint_id)
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"PASS: {len(sprint_ids)} prior sprint packages; {artifacts} required artifacts; "
        "canonical homes unique."
    )
    print("PASS: current provider status, no daily expiry, $0 scope and historical boundaries.")


if __name__ == "__main__":
    main()
