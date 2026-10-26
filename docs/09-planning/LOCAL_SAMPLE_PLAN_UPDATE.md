# Current local-sample plan

26 October 2026. This is the current local implementation direction, following the
[reviewed Sprint 12 closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md). It reconciles
the original blueprint with the owner's supplied APIs, limited RAM and request
for a usable sample. Original full-product requirements are retained, not marked
complete by a reduced demo. See [Sprint 11/11.1 closeout](../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md).

| Earlier direction/checkpoint | Current disposition |
| --- | --- |
| Ollama alongside the application | Stopped; insufficient RAM and no qualifying project-format results; optional future capability |
| Broad specialist-generated reasoning | Unqualified; guided mode uses Python facts/actions and bounded API selection with deterministic fallback |
| Train or fine-tune supplied models | No hosted LLM weight training; small local CPU baselines now run reproducibly. Dataset/prompt work is not LLM training and synthetic metrics do not qualify models |
| Provider exploration | Use supplied Gemini, Puter and Groq across nine roles; no additional key required |
| Normal schema 0012, rollout blocked | Local additive rollout through 0018; broad semantic/model-quality activation remains blocked |
| Admin-only analysis | Explicit scoped guided grants for four named users, without changing business roles |
| Synthetic demo only | Synthetic demo plus approved Customer Onboarding Portal bounded observations |
| Ten requests per provider/day | Fifty per rolling 24 hours, shared; same pacing, concurrency, $0 policy and retained usage history |
| Stop before Sprint 12 | Superseded by explicit Sprint 12 authorization; local sample accepted at 0018, reviewed/pushed on PR 7; full external/model gates open; stop before 13 |

Gemini handles financial/schedule/resource; Puter handles risk/governance/agile_coach;
Groq handles sentiment/team support/pmo/executive. One guided role/run uses at most
one 128-token request; all nine manual checklists work without an API response.
Current details: [scope](../limitations/API_DATA_SCOPE.md), [access](../limitations/USER_ACCESS.md),
[quota evidence](../limitations/QUOTA_REVIEW.md), [local usage](../limitations/TRY_IT_NOW.md).

## Sequence and acceptance

1. Sprint 11/11.1: local guided scope complete. AT17 and unrestricted model quality
   remain blocked; no independent human production acceptance is claimed.
2. Sprint 12: local connector authority/conflicts, outcome-provenance dataset contracts
   and small reproducible CPU pipelines are implemented. The import-to-model-card
   journey is accepted locally; genuine labels and live source comparison remain unavailable. See [the implementation plan](sprint-12/LOCAL_IMPLEMENTATION_PLAN.md).
3. Sprint 13: consider forecast eligibility/serving only with the necessary data
   and evaluation evidence. A pipeline demo cannot promote an unqualified model.
4. Later sprints retain the [original roadmap](FUTURE_SPRINT_ROADMAP.md). Deployment
   work is tracked separately in [future deployment points](../limitations/FUTURE_DEPLOYMENT_POINTS.md).

Current implementation: [Sprint 12 report](../03-sprints/completed/sprint-12/SPRINT_REPORT.md). The dated planning directions above are retained; local sample acceptance is complete with the retained live/model gates open.

Sprint 12 can depend on verified deterministic/source/job contracts. It must not
depend on an unqualified specialist or use its output as true outcome labels.
Absent live credentials or sufficient genuine labels can leave live integration
or model promotion BLOCKED while a clearly labeled local pipeline is accepted.
Access, source integrity and contract failures still block the affected work.
Full original acceptance requires the missing real evidence; this update does not
silently remove model, privacy, reliability or release requirements.

## Documentation authority

Use this plan, the closeout and `docs/limitations/` for current local behavior.
Dated earlier test reports, routing experiments and stop instructions describe
their checkpoints. Keep their failures and measurements as history. Original
`docs/source`, `docs/prompts` and applied migrations remain frozen. New schema
changes must be forward-only after verifying the actual current head (0018 at
this closeout). Preserve uncommitted implementation and unrelated artifacts.

The original 25 October update was planning-only; Sprint 12 implementation and review
are now complete for the local scope. This reconciliation does not deploy production,
change provider billing, expand data scope or authorize Sprint 13.
