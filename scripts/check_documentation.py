"""Check local Markdown targets, anchors and retained Sprint 09/10 coverage."""

import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)")


def without_fences(content: str) -> str:
    return re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1[^\n]*$", "", content)


def anchors(content: str) -> set[str]:
    result = set(re.findall(r'<(?:a|[a-z]+)[^>]+(?:id|name)="([^"]+)"', content))
    counts: Counter[str] = Counter()
    for heading in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*#*\s*$", without_fences(content)):
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        count = counts[slug]
        counts[slug] += 1
        result.add(slug + (f"-{count}" if count else ""))
    return result


def main() -> None:
    files = [ROOT / "README.md", ROOT / "ANTIGRAVITY.md", *sorted((ROOT / "docs").rglob("*.md"))]
    errors = []
    references = 0
    cache: dict[Path, set[str]] = {}
    for path in files:
        content = without_fences(path.read_text(encoding="utf-8-sig"))
        for match in LINK.finditer(content):
            link = match[1].strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith("/"):
                continue
            references += 1
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing {link}")
            elif parsed.fragment and target.suffix.lower() == ".md":
                if target not in cache:
                    cache[target] = anchors(target.read_text(encoding="utf-8-sig"))
                if unquote(parsed.fragment) not in cache[target]:
                    errors.append(f"{path.relative_to(ROOT)}: missing anchor {link}")
    for topic in (
        "03-sprints/completed",
        "02-learning/sprint-based",
        "04-testing/sprint-based",
        "05-demos/sprint-based",
    ):
        if not (ROOT / "docs" / topic / "sprint-09/README.md").is_file():
            errors.append(f"Missing Sprint 09 README in {topic}")
    for topic in (
        "03-sprints/completed",
        "02-learning/sprint-based",
        "04-testing/sprint-based",
        "05-demos/sprint-based",
    ):
        if not (ROOT / "docs" / topic / "sprint-10/README.md").is_file():
            errors.append(f"Missing Sprint 10 README in {topic}")
    for name in (
        "contracts/ai.md",
        "architecture/adr/016-budgeted-ai-runtime.md",
        "02-learning/06-ai-and-analytics/AI_GATEWAY.md",
        "07-setup-and-deployment/AI-RUNTIME.md",
        "04-testing/sprint-based/sprint-10/DOCUMENTATION_CHECKS.md",
    ):
        if not (ROOT / "docs" / name).is_file():
            errors.append(f"Missing Sprint 10 artifact {name}")
    sprint10 = (ROOT / "docs/03-sprints/completed/sprint-10/SPRINT_REPORT.md").read_text(
        encoding="utf-8"
    )
    current_sprint10 = sprint10.split("## Historical 15 October record", 1)[0]
    if not all(
        term in current_sprint10 for term in ("Gemini", "$0", "VERIFIED", "OPEN", "Stop before 11")
    ):
        errors.append(
            "Sprint 10 must distinguish verified Gemini smoke, open quality gates "
            "and Sprint 11 boundary"
        )
    if (ROOT / "docs/03-sprints/planned/sprint-10/README.md").exists():
        errors.append("Duplicate planned Sprint 10 home")
    catalogue = (ROOT / "docs/00-overview/FEATURE_CATALOGUE.md").read_text(encoding="utf-8")
    mapping = (ROOT / "docs/09-planning/FEATURE_DOCUMENT_MAPPING.md").read_text(encoding="utf-8")
    coverage = (ROOT / "docs/requirements/coverage.md").read_text(encoding="utf-8")
    expected_ids = set(re.findall(r"(?m)^\| ((?:P|F|N|E|T)-\d{3})[ |]", coverage))
    for label, content in (("catalogue", catalogue), ("mapping", mapping)):
        ids = re.findall(r"(?m)^\| ((?:P|F|N|E|T)-\d{3})[ |]", content)
        gaps = re.findall(r"(?m)^\| (G-\d{3})[ |]", content)
        if len(ids) != 156 or len(set(ids)) != 156 or len(gaps) != 36 or len(set(gaps)) != 36:
            errors.append(f"{label}: expected unique 156 requirements and 36 gaps")
        if set(ids) != expected_ids:
            errors.append(f"{label}: requirement IDs differ from canonical coverage")
    for identifier in ("F-065", "F-068", "F-069", "F-073"):
        row = next(row for row in catalogue.splitlines() if row.startswith(f"| {identifier} |"))
        if "IMPLEMENTED AND VERIFIED LOCALLY" not in row:
            errors.append(f"catalogue: stale status for {identifier}")
    for identifier in ("F-066", "F-067", "F-074"):
        row = next(row for row in catalogue.splitlines() if row.startswith(f"| {identifier} |"))
        if "PARTIALLY IMPLEMENTED" not in row:
            errors.append(f"catalogue: semantic boundary lost for {identifier}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(files)} Markdown files; {references} local links/anchors; zero missing")
    print("PASS: catalogue/mapping each retain 156 requirements and 36 gaps")
    print("PASS: Sprint 09 hubs and accepted/partial requirement status boundaries")
    print("PASS: Sprint 10 hubs, verified-smoke/open-quality distinction and Sprint 11 boundary")
    print("External URLs, plain-text paths and archived Word layout are outside this check")


if __name__ == "__main__":
    main()
