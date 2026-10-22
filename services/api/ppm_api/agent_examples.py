"""Original positive format examples, drawn only from the authored training split."""

EXAMPLES = {
    "agile_coach": {
        "evidence": {
            "e1": {
                "length": 73,
                "text": "The team selected sprint work without agreeing a shared sprint objective.",
            }
        },
        "output": {
            "covered": ["e1"],
            "findings": [
                {
                    "advice": "Agree a sprint objective and inspect work against it.",
                    "claim": "An unclear objective makes sprint work harder to align.",
                    "epistemic": "interpretation",
                    "kind": "risk",
                    "predicate": "practice_gap",
                    "severity": "medium",
                    "signal": "adverse",
                    "spans": [{"e": "e1", "end": 73, "start": 0}],
                    "subject": "s1",
                }
            ],
            "gaps": [],
            "matches": [],
            "mode": "findings",
            "narrative": [],
            "outcome": "supported",
            "section": "training_agile_coach_supported",
        },
    },
    "executive": {
        "evidence": {
            "e1": {
                "length": 61,
                "text": "The selected release remains blocked pending security review.",
            }
        },
        "output": {
            "covered": ["f1"],
            "findings": [],
            "gaps": [],
            "matches": [],
            "mode": "synthesis",
            "narrative": [
                {
                    "advice": "Keep readiness conditional on the recorded review outcome.",
                    "basis": ["f1"],
                    "claim": "The unresolved release condition "
                    "warrants a scoped readiness decision.",
                    "epistemic": "interpretation",
                    "spans": [{"e": "e1", "end": 61, "start": 0}],
                }
            ],
            "outcome": "supported",
            "section": "training_executive_supported",
        },
    },
    "financial": {
        "evidence": {
            "e1": {
                "length": 58,
                "text": "Unapproved scope changes are increasing supplier invoices.",
            }
        },
        "output": {
            "covered": ["e1"],
            "findings": [
                {
                    "advice": "Review pending changes against the approved cost baseline.",
                    "claim": "Cost pressure warrants reviewing scope authorization.",
                    "epistemic": "interpretation",
                    "kind": "risk",
                    "predicate": "risk_present",
                    "severity": "medium",
                    "signal": "adverse",
                    "spans": [{"e": "e1", "end": 58, "start": 0}],
                    "subject": "s1",
                }
            ],
            "gaps": [],
            "matches": [],
            "mode": "findings",
            "narrative": [],
            "outcome": "supported",
            "section": "training_financial_supported",
        },
    },
    "governance": {
        "evidence": {
            "e1": {
                "length": 71,
                "text": "The release review record has no approval from the designated reviewer.",
            }
        },
        "output": {
            "covered": ["e1"],
            "findings": [
                {
                    "advice": "Obtain the required review before "
                    "treating the control as satisfied.",
                    "claim": "The missing review leaves an approval control gap.",
                    "epistemic": "interpretation",
                    "kind": "compliance_gap",
                    "predicate": "policy_gap",
                    "severity": "medium",
                    "signal": "adverse",
                    "spans": [{"e": "e1", "end": 71, "start": 0}],
                    "subject": "s1",
                }
            ],
            "gaps": [],
            "matches": [],
            "mode": "findings",
            "narrative": [],
            "outcome": "supported",
            "section": "training_governance_supported",
        },
    },
    "pmo": {
        "evidence": {
            "e1": {
                "length": 78,
                "text": "The shared supplier interface decision is unresolved "
                "across the selected work.",
            }
        },
        "output": {
            "covered": ["f1"],
            "findings": [],
            "gaps": [],
            "matches": [],
            "mode": "synthesis",
            "narrative": [
                {
                    "advice": "Coordinate the interface decision within the selected scope.",
                    "basis": ["f1"],
                    "claim": "The shared dependency warrants coordinated escalation.",
                    "epistemic": "interpretation",
                    "spans": [{"e": "e1", "end": 78, "start": 0}],
                }
            ],
            "outcome": "supported",
            "section": "training_pmo_supported",
        },
    },
    "resource": {
        "evidence": {"e1": {"length": 20, "text": "Capacity risk is 25."}},
        "output": {
            "covered": ["e1"],
            "findings": [
                {
                    "advice": "Review aggregate commitments before accepting additional work.",
                    "claim": "The aggregate capacity signal warrants a commitment review.",
                    "epistemic": "interpretation",
                    "kind": "risk",
                    "predicate": "capacity_exceeded",
                    "severity": "medium",
                    "signal": "adverse",
                    "spans": [{"e": "e1", "end": 20, "start": 0}],
                    "subject": "s1",
                }
            ],
            "gaps": [],
            "matches": [],
            "mode": "findings",
            "narrative": [],
            "outcome": "supported",
            "section": "training_resource_supported",
        },
    },
    "risk": {
        "evidence": {
            "e1": {
                "length": 74,
                "text": "The test environment is unavailable and release "
                "validation cannot proceed.",
            }
        },
        "output": {
            "covered": ["e1"],
            "findings": [
                {
                    "advice": "Resolve the environment blocker before judging release readiness.",
                    "claim": "Release readiness remains dependent on restoring validation.",
                    "epistemic": "interpretation",
                    "kind": "risk",
                    "predicate": "delivery_blocked",
                    "severity": "medium",
                    "signal": "adverse",
                    "spans": [{"e": "e1", "end": 74, "start": 0}],
                    "subject": "s1",
                }
            ],
            "gaps": [],
            "matches": [],
            "mode": "findings",
            "narrative": [],
            "outcome": "supported",
            "section": "training_risk_supported",
        },
    },
    "schedule": {
        "evidence": {
            "e1": {
                "length": 64,
                "text": "Integration cannot start until the interface contract is agreed.",
            }
        },
        "output": {
            "covered": ["e1"],
            "findings": [
                {
                    "advice": "Coordinate the interface decision before scheduling integration.",
                    "claim": "The unresolved interface threatens the delivery sequence.",
                    "epistemic": "interpretation",
                    "kind": "risk",
                    "predicate": "dependency_unresolved",
                    "severity": "medium",
                    "signal": "adverse",
                    "spans": [{"e": "e1", "end": 64, "start": 0}],
                    "subject": "s1",
                }
            ],
            "gaps": [],
            "matches": [],
            "mode": "findings",
            "narrative": [],
            "outcome": "supported",
            "section": "training_schedule_supported",
        },
    },
    "sentiment": {
        "evidence": {"e1": {"length": 24, "text": "Team blocker count is 6."}},
        "output": {
            "covered": ["b1"],
            "findings": [],
            "gaps": [],
            "matches": [],
            "mode": "synthesis",
            "narrative": [
                {
                    "advice": "Review shared impediments without "
                    "attributing emotions to individuals.",
                    "basis": ["b1"],
                    "claim": "The aggregate blocker signal warrants a "
                    "team-level impediment review.",
                    "epistemic": "interpretation",
                    "spans": [{"e": "e1", "end": 24, "start": 0}],
                }
            ],
            "outcome": "supported",
            "section": "training_sentiment_supported",
        },
    },
}
