# Cloud specialist calibration results

17 October 2026. Synthetic calibration only; no model is qualified or activated.

26 requests: Groq 9, Gemini 9, Puter 8. All outcomes known; original three Groq probes and exhausted local case retained.

Each role has a supported response under the current prompt that passed hard checks. This is not independently measured accuracy. Of nine absence cases, seven passed hard checks without findings; financial/resource were rejected. An absence result with gaps does not mean semantic coverage completed.

| Role | Provider | Case | Output tokens | Latency ms | Receipt |
| --- | --- | --- | --- | --- | --- |
| resource | groq | resource_03 | 209 | 888 | [receipt](implementation/cloud-groq-resource-v2.json) |
| financial | groq | financial_03 | 171 | 679 | [receipt](implementation/cloud-groq-financial-v3.json) |
| schedule | groq | schedule_03 | 169 | 738 | [receipt](implementation/cloud-groq-schedule-v2.json) |
| agile_coach | gemini | agile_coach_03 | 210 | 2235 | [receipt](implementation/cloud-gemini-agile-v2.json) |
| governance | gemini | governance_03 | 213 | 1899 | [receipt](implementation/cloud-gemini-governance-v2-measured.json) |
| risk | gemini | risk_03 | 109 | 2134 | [receipt](implementation/cloud-gemini-risk-v2.json) |
| executive | puter | executive_03 | 103 | 2170 | [receipt](implementation/cloud-puter-executive-v2.json) |
| sentiment | puter | sentiment_03 | 100 | 2032 | [receipt](implementation/cloud-puter-team-v2.json) |
| pmo | puter | pmo_03 | 114 | 2258 | [receipt](implementation/cloud-puter-pmo-v2.json) |

## Retained failed attempts

| Provider | Case | Result | Receipt |
| --- | --- | --- | --- |
| gemini | governance_01 | INVALID_OUTPUT | [receipt](implementation/cloud-gemini-governance-v2.json) |
| groq | financial_07 | INVALID_OUTPUT | [receipt](implementation/cloud-groq-financial-absent.json) |
| groq | financial_03 | INVALID_OUTPUT | [receipt](implementation/cloud-groq-financial-v2-measured.json) |
| groq | resource_07 | INVALID_OUTPUT | [receipt](implementation/cloud-groq-resource-absent.json) |
| puter | pmo_01 | INVALID_OUTPUT | [receipt](implementation/cloud-puter-pmo-measured.json) |
| puter | sentiment_01 | INVALID_OUTPUT | [receipt](implementation/cloud-puter-team-first.json) |

## Candidate review packet

These are original synthetic inputs and model outputs for review. No ratings or reviewer identity are invented. Correct spans do not prove semantic support. Compare implications, advice relevance, missing evidence and canonical values before any acceptance decision.

### resource

Synthetic evidence:

```json
[
  {
    "text": "{\"computed_health\":\"Amber\",\"facts\":[],\"freshness\":\"fresh\",\"key\":\"capacity_risk\",\"label\":\"Capacity risk\",\"reported_health\":\"Amber\",\"source_updated_at\":null,\"status\":\"available\",\"unit\":\"exceptions\",\"value\":\"3\"}",
    "category": "metric:capacity_risk",
    "kind": "metric",
    "metric": {
      "key": "capacity_risk",
      "value": "3"
    }
  }
]
```

Model output:

```json
{
  "covered": [
    "e1"
  ],
  "findings": [
    {
      "advice": "Reassess current project commitments to ensure capacity limits are not exceeded.",
      "claim": "The capacity risk signal indicates that the project is approaching its capacity threshold.",
      "epistemic": "interpretation",
      "kind": "risk",
      "predicate": "risk_present",
      "severity": "medium",
      "signal": "adverse",
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 208
        }
      ],
      "subject": "s1"
    }
  ],
  "gaps": [],
  "matches": [],
  "mode": "findings",
  "narrative": [],
  "outcome": "supported",
  "section": "resource_03"
}
```

### financial

Synthetic evidence:

```json
[
  {
    "text": "Expedited shipping is drawing down the remaining procurement allowance.",
    "category": "document:project"
  },
  {
    "text": "Budget usage is 110 percent.",
    "category": "metric:usage",
    "kind": "metric",
    "metric": {
      "key": "usage",
      "value": "110"
    }
  }
]
```

Model output:

```json
{
  "covered": [
    "e1"
  ],
  "findings": [
    {
      "advice": "Reassess shipping schedules to preserve procurement budget.",
      "claim": "Expedited shipping is drawing down the remaining procurement allowance.",
      "epistemic": "interpretation",
      "kind": "risk",
      "predicate": "risk_present",
      "severity": "medium",
      "signal": "adverse",
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 71
        }
      ],
      "subject": "s1"
    }
  ],
  "gaps": [],
  "matches": [],
  "mode": "findings",
  "narrative": [],
  "outcome": "supported",
  "section": "financial_03"
}
```

### schedule

Synthetic evidence:

```json
[
  {
    "text": "A supplier delivery slip prevents the dependent installation from starting.",
    "category": "document:sprint_report"
  },
  {
    "text": "Canonical schedule risk is 1.",
    "category": "metric:schedule_risk",
    "kind": "metric",
    "metric": {
      "key": "schedule_risk",
      "value": "1"
    }
  }
]
```

Model output:

```json
{
  "covered": [
    "e1"
  ],
  "findings": [
    {
      "advice": "Address the supplier delivery slip issue before proceeding with the dependent installation.",
      "claim": "The supplier delivery slip prevents the dependent installation from starting.",
      "epistemic": "interpretation",
      "kind": "risk",
      "predicate": "dependency_unresolved",
      "severity": "medium",
      "signal": "adverse",
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 75
        }
      ],
      "subject": "s1"
    }
  ],
  "gaps": [],
  "matches": [],
  "mode": "findings",
  "narrative": [],
  "outcome": "supported",
  "section": "schedule_03"
}
```

### agile_coach

Synthetic evidence:

```json
[
  {
    "text": "The team starts new work while blocked work remains unreviewed.",
    "category": "document:sprint_report"
  }
]
```

Model output:

```json
{
  "section": "agile_coach_03",
  "mode": "findings",
  "outcome": "supported",
  "findings": [
    {
      "subject": "s1",
      "predicate": "practice_gap",
      "kind": "risk",
      "signal": "adverse",
      "severity": "medium",
      "claim": "The team starts new work while blocked work remains unreviewed.",
      "advice": "Review blocked work before starting new items.",
      "epistemic": "interpretation",
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 63
        }
      ]
    }
  ],
  "matches": [],
  "narrative": [],
  "covered": [
    "e1"
  ],
  "gaps": []
}
```

### governance

Synthetic evidence:

```json
[
  {
    "text": "The mandatory access review has no documented completion evidence.",
    "category": "document:policy"
  }
]
```

Model output:

```json
{
  "section": "governance_03",
  "mode": "findings",
  "outcome": "supported",
  "findings": [
    {
      "subject": "s1",
      "predicate": "policy_gap",
      "kind": "compliance_gap",
      "signal": "adverse",
      "severity": "medium",
      "claim": "The missing documented completion evidence leaves a control gap.",
      "advice": "Obtain the required evidence before treating the control as satisfied.",
      "epistemic": "interpretation",
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 66
        }
      ]
    }
  ],
  "matches": [],
  "narrative": [],
  "covered": [
    "e1"
  ],
  "gaps": []
}
```

### risk

Synthetic evidence:

```json
[
  {
    "text": "The production certificate is expiring and renewal ownership is unresolved.",
    "category": "document:project"
  }
]
```

Model output:

```json
{
  "section": "risk_03",
  "mode": "findings",
  "outcome": "supported",
  "findings": [
    {
      "subject": "s1",
      "predicate": "dependency_unresolved",
      "kind": "risk",
      "signal": "adverse",
      "severity": "medium",
      "claim": "The production certificate is expiring and renewal ownership is unresolved.",
      "advice": "Assign certificate renewal ownership to prevent expiration risks.",
      "epistemic": "interpretation",
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 75
        }
      ]
    }
  ],
  "matches": [],
  "narrative": [],
  "covered": [
    "e1"
  ],
  "gaps": []
}
```

### executive

Synthetic evidence:

```json
[
  {
    "text": "The selected delivery commitments rely on an unverified recovery capability.",
    "category": "metric:risk"
  }
]
```

Model output:

```json
{
  "section": "executive_03",
  "mode": "synthesis",
  "outcome": "supported",
  "findings": [],
  "matches": [],
  "narrative": [
    {
      "claim": "The unresolved delivery commitments relying on an unverified recovery capability warrant a scoped readiness decision.",
      "advice": "Inspect the authorized evidence and retain unresolved limitations.",
      "epistemic": "interpretation",
      "basis": [
        "f1"
      ],
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 76
        }
      ]
    }
  ],
  "covered": [
    "f1"
  ],
  "gaps": []
}
```

### sentiment

Synthetic evidence:

```json
[
  {
    "text": "Privacy-safe team delivery summary: 3 open project blockers. This is not emotional sentiment.",
    "category": "group:blockers"
  }
]
```

Model output:

```json
{
  "section": "sentiment_03",
  "mode": "synthesis",
  "outcome": "supported",
  "findings": [],
  "matches": [],
  "narrative": [
    {
      "claim": "The aggregate blocker signal warrants a team-level impediment review.",
      "advice": "Review shared impediments without attributing emotions to individuals.",
      "epistemic": "interpretation",
      "basis": [
        "b1"
      ],
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 93
        }
      ]
    }
  ],
  "covered": [
    "b1"
  ],
  "gaps": []
}
```

### pmo

Synthetic evidence:

```json
[
  {
    "text": "A procurement delay in Project Cedar blocks the shared rollout in Project Maple.",
    "category": "record:dependencies"
  }
]
```

Model output:

```json
{
  "section": "pmo_03",
  "mode": "synthesis",
  "outcome": "supported",
  "findings": [],
  "matches": [],
  "narrative": [
    {
      "claim": "The procurement delay in Project Cedar impacts the shared rollout in Project Maple within the selected scope.",
      "advice": "Address the procurement delay in Project Cedar to unblock the shared rollout in Project Maple.",
      "epistemic": "interpretation",
      "basis": [
        "f1"
      ],
      "spans": [
        {
          "e": "e1",
          "start": 0,
          "end": 80
        }
      ]
    }
  ],
  "covered": [
    "e1",
    "f1"
  ],
  "gaps": []
}
```
