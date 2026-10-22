"""Read-only structure checks plus a receipt for the planning documentation.

This checks documentation, not the proposed application's implementation.
"""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/09-planning/sprint-11.1"
NAMES = [
    "PLAN", "DISCOVERY", "ARCHITECTURE", "DECISION_LOG", "AGENT_CATALOG",
    "PROVIDER_ROUTING", "ORCHESTRATION", "VALIDATION_RECOVERY",
    "TECHNICAL_CONTRACTS", "IMPLEMENTATION_GUIDE", "TEST_PLAN", "SETUP",
    "RISKS", "TASK_TRACKER", "HANDOVER", "TRACEABILITY", "SOURCES",
]
expected = {"README.md", *(f"SPRINT_11_1_{name}.md" for name in NAMES)}
assert {p.name for p in PACK.glob("*.md")} == expected
documents = {p.name: p.read_text(encoding="utf-8") for p in sorted(PACK.glob("*.md"))}
for name, text in documents.items():
    assert text.startswith("# "), name
    assert text.count("```") % 2 == 0, name
    assert "pipeline_jobs" not in text, name
    assert "\ufffd" not in text, name

catalog = documents["SPRINT_11_1_AGENT_CATALOG.md"]
agents = re.findall(r"^## ([a-z_]+) —", catalog, re.M)
assert agents == ["financial", "schedule", "sentiment", "risk", "resource",
                  "governance", "agile_coach", "pmo", "executive"]
catalog_blocks = re.split(r"^## [a-z_]+ —", catalog, flags=re.M)[1:]
for block in catalog_blocks:
    assert len(re.findall(r"^\d+\. \*\*", block, re.M)) == 10
    execution = re.search(r"^6\. \*\*Execution/models/providers:\*\* (.+)$", block, re.M)
    assert execution and "LLM" in execution[1], "Every role needs an optional AI path"
assert "execution_policy='hybrid_on_demand'" in catalog
classes = [
    "financial_interpretation", "schedule_interpretation", "team_support_advice",
    "risk_extraction", "resource_interpretation", "governance_interpretation",
    "agile_advice", "portfolio_synthesis", "executive_synthesis",
]
for task_class in classes:
    assert task_class in catalog
    assert task_class in documents["SPRINT_11_1_PROVIDER_ROUTING.md"]

orchestration = documents["SPRINT_11_1_ORCHESTRATION.md"]
contracts = documents["SPRINT_11_1_TECHNICAL_CONTRACTS.md"]
assert "### Interpretation selection and priority" in orchestration
assert "Explicit financial/schedule/resource investigation" in orchestration
assert "Executive alone" in orchestration
assert "semantic_deferred_ids" in contracts
assert "resolved_context_manifest" in contracts
assert "ADR 11.1-11" in documents["SPRINT_11_1_HANDOVER.md"]
stale_role_rules = [
    "use six deterministic capabilities and three conditional semantic workers",
    "six deterministic methods, three semantic workers",
    "Python deterministic service; no model or provider eligible",
    "deterministic reconciliation; no provider",
    "Python template renderer; no provider",
    "Six deterministic roles make zero network calls",
]
for name, content in documents.items():
    for stale in stale_role_rules:
        assert stale not in content, (name, stale)

guide = documents["SPRINT_11_1_IMPLEMENTATION_GUIDE.md"]
tasks = re.findall(r"^## (T\d{2}) —", guide, re.M)
assert tasks == [f"T{i:02}" for i in range(1, 15)]
tracker = documents["SPRINT_11_1_TASK_TRACKER.md"]
trace = documents["SPRINT_11_1_TRACEABILITY.md"]
testplan = documents["SPRINT_11_1_TEST_PLAN.md"]
tests = re.findall(r"^\| (AT\d{2}) \|", testplan, re.M)
assert tests == [f"AT{i:02}" for i in range(1, 21)]
requirements = re.findall(r"^\| (R\d{2}) ", trace, re.M)
assert requirements == [f"R{i:02}" for i in range(1, 17)]
for task in tasks:
    assert re.search(rf"^\| {task} \| (NOT_STARTED|IN_PROGRESS|BLOCKED|IMPLEMENTED|VERIFIED)", tracker, re.M), task
    assert task in trace, task
for name, content in documents.items():
    for test in re.findall(r"\bAT\d{2}\b", content):
        assert test in tests, (name, test)
    for task in re.findall(r"\bT\d{2}\b", content):
        assert task in tasks, (name, task)

receipt = {
    "date": "2026-10-17",
    "scope": "documentation structure; not implementation verification",
    "source_baseline": "d0ebe32e691a3d63166ced669450911c63151127",
    "planning_revision": "hybrid-roles-adr-11.1-11",
    "documents": [{"file": name, "bytes": len(text.encode()),
                   "sha256": hashlib.sha256(text.encode()).hexdigest(),
                   "headings": re.findall(r"^#{1,3} (.+)$", text, re.M)}
                  for name, text in documents.items()],
    "capabilities": agents,
    "interpretation_task_classes": classes,
    "implementation_tasks": tasks,
    "acceptance_tests": tests,
    "requirements": requirements,
    "result": "PASS",
}
(Path(__file__).parent / "blueprint-audit.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"PASS: read {len(documents)} documents; 15 requested artifacts plus index/traceability/sources")
print("PASS: nine contracts, 14 tracked implementation tasks, 16 requirements, 20 acceptance IDs")
print("PASS: fences, local IDs, required files and known table-name consistency")
print("PASS: all nine optional AI paths/classes, synthesis/coverage contracts and no stale fixed-role rules")
print("Semantic consistency requires the separate human/model re-read checklist; this is not runtime testing.")
