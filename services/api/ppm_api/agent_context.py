"""Role-scoped evidence packing. Accepted dependencies never grant new authority."""

import json

from ppm_api.agent_validation import PREDICATES
from ppm_api.model_contracts import ModelFailure, SectionOutput
from ppm_api.model_registry import canonical


def section_schema(mode: str) -> dict:
    """Restrict section output to the selected mode and reachable schema definitions."""
    schema = SectionOutput.model_json_schema()
    chosen = {"findings": "findings", "rubric": "matches", "synthesis": "narrative"}[mode]
    for name in ("findings", "matches", "narrative"):
        if name != chosen:
            schema["properties"][name] = {"type": "array", "maxItems": 0, "items": {}}
    definitions = schema.get("$defs", {})
    needed: set[str] = set()

    def visit(value: object) -> None:
        """Remove schema titles and collect transitively referenced definitions."""
        if isinstance(value, dict):
            value.pop("title", None)
            if "$ref" in value:
                key = str(value["$ref"]).split("/")[-1]
                if key not in needed:
                    needed.add(key)
                    visit(definitions[key])
            for key, child in list(value.items()):
                if key != "$defs":
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(schema)
    schema["$defs"] = {key: definitions[key] for key in sorted(needed)}
    return schema


def pack(
    snapshot: dict,
    node: dict,
    current: dict,
    basis: list[dict],
    unresolved: list[str] | None = None,
) -> dict:
    """Bind current authorized evidence and dependency aliases to a bounded role request."""
    agent, mode = node["agent"], node["mode"]
    old = {s["source"]: s for s in snapshot["sources"]}
    selected = []
    for sid in node["source_ids"]:
        source = current.get(sid)
        if source and sid in old and source["sha256"] == old[sid]["sha256"]:
            if agent in source["permitted_agents"]:
                selected.append(source)
    if agent == "sentiment":
        selected = [s for s in selected if s["kind"] == "group" and s["source"] == "group:blockers"]
    aliases: dict[str, dict] = {}
    subjects: dict[str, dict] = {}
    questions: dict[str, dict] = {}
    bases: dict[str, dict] = {}
    if mode == "findings" and not set(node["required_ids"]) <= {s["source"] for s in selected}:
        raise ModelFailure("AUTHORITY_REVOKED")
    if mode == "rubric":
        from ppm_api.assessment import questions as framework_questions

        all_questions = framework_questions(snapshot["framework"])
        for qid in node["required_ids"]:
            if qid in all_questions:
                questions[f"q{len(questions) + 1}"] = dict(id=qid, rubric=all_questions[qid])
        selected = [
            s
            for s in selected
            if s["source"] in {"answer:" + q["id"] for q in questions.values()}
            or s["kind"] == "document"
        ]
    elif mode == "findings":
        # Required text plus immutable numerical context; no unrelated raw project records.
        selected = [
            s for s in selected if s["source"] in node["required_ids"] or s["kind"] == "metric"
        ]
    if mode == "synthesis" and agent in ("pmo", "executive"):
        selected = []
        if agent == "executive":
            basis = sorted(basis, key=lambda item: "pmo" not in item.get("agents", []))
        for item in basis[:2]:
            refs = item.get("spans", [])
            permitted = []
            for ref in refs:
                source = current.get(ref["source"])
                if (
                    not source
                    or ref["source"] not in old
                    or source["sha256"] != old[ref["source"]]["sha256"]
                ):
                    break
                # Explicit derived allowance: currently authorized project/portfolio facts or
                # approved document windows only. Private answers/notes are never inherited.
                if source["kind"] not in ("metric", "document", "record", "group"):
                    break
                permitted.append(source)
            else:
                if permitted:
                    bases[f"f{len(bases) + 1}"] = item
                    selected.extend(permitted)
    for source in selected:
        if any(s["source"] == source["source"] for s in aliases.values()):
            continue
        aliases[f"e{len(aliases) + 1}"] = source
    if agent == "sentiment" and aliases:
        bases["b1"] = dict(
            key="group:blockers",
            spans=[dict(source=s["source"], start=0, end=len(s["text"])) for s in aliases.values()],
        )
    subjects["s1"] = dict(agent=agent, scope="selected authorized project")
    required_aliases = (
        list(questions)
        if mode == "rubric"
        else list(bases)
        if mode == "synthesis"
        else [k for k, s in aliases.items() if s["source"] in node["required_ids"]]
    )
    payload = dict(
        section=node["key"],
        mode=mode,
        required=required_aliases,
        evidence={k: dict(text=s["text"], length=len(s["text"])) for k, s in aliases.items()},
        subjects=subjects,
        questions=questions,
        basis={
            k: {
                f: v
                for f, v in item.items()
                if f in ("key", "kind", "signal", "severity", "title", "improvement", "spans")
            }
            for k, item in bases.items()
        },
    )
    if not aliases:
        raise ModelFailure("CONFIGURATION")
    if agent in ("pmo", "executive"):
        payload["unresolved_interpretations"] = unresolved or []
        payload["scope_limit"] = (
            "Only these cited basis items are inspected; no whole-portfolio assurance."
        )
    schema = section_schema(mode)
    # Give constrained decoders the same identity boundaries as the hard gate.
    # A subject alias (s1) is not an evidence/coverage alias (e1). These are
    # Python-owned identifiers, never a semantic choice delegated to the model.
    schema["properties"]["section"] = dict(type="string", const=node["key"])
    schema["properties"]["mode"] = dict(type="string", const=mode)
    coverage_aliases = required_aliases
    schema["properties"]["covered"]["items"] = dict(type="string", enum=coverage_aliases)
    definitions = schema["$defs"]
    if "SectionGap" in definitions:
        definitions["SectionGap"]["properties"]["item"] = dict(type="string", enum=coverage_aliases)
    if "CompactSpan" in definitions:
        definitions["CompactSpan"]["properties"]["e"] = dict(type="string", enum=list(aliases))
    if "SectionFinding" in definitions:
        definitions["SectionFinding"]["properties"]["subject"] = dict(
            type="string", enum=list(subjects)
        )
        definitions["SectionFinding"]["properties"]["predicate"] = dict(
            type="string", enum=sorted(PREDICATES.get(agent, set()))
        )
        if agent in ("financial", "resource"):
            # Canonical quantities stay in Python's baseline. Restrict decoding,
            # rather than editing or accepting an unsupported numeric statement.
            for field in ("claim", "advice"):
                definitions["SectionFinding"]["properties"][field]["pattern"] = r"^[^0-9]*$"
            primary = [key for key in required_aliases if key in aliases]
            if primary:
                definitions["CompactSpan"]["properties"]["e"] = dict(type="string", enum=primary)
    if "SectionMatch" in definitions and questions:
        definitions["SectionMatch"]["properties"]["question"] = dict(
            type="string", enum=list(questions)
        )
    if "NarrativeItem" in definitions and bases:
        definitions["NarrativeItem"]["properties"]["basis"]["items"] = dict(
            type="string", enum=list(bases)
        )
    # Whole-source packing: if it cannot fit, the runtime reports a gap, never a fake summary.
    return dict(
        payload=canonical(payload),
        schema=schema,
        evidence=aliases,
        subjects=subjects,
        questions=questions,
        basis=bases,
        required_aliases=required_aliases,
        categories=sorted({s.get("category", s["kind"]) for s in aliases.values()}),
        input_tokens=len(canonical(payload).encode()) + len(json.dumps(schema).encode()),
    )
