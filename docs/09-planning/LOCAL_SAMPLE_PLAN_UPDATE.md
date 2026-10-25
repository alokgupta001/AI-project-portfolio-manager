# Current local-sample plan

25 October 2026. This is the current local implementation direction. It reconciles
the original blueprint with the owner's supplied APIs, limited RAM and request
for a usable sample. Original full-product requirements are retained, not marked
complete by a reduced demo. See [Sprint 11/11.1 closeout](../10-reference/SPRINT-11-LOCAL-CLOSEOUT.md).

| Earlier direction/checkpoint | Current disposition |
| --- | --- |
| Ollama alongside the application | Stopped; insufficient RAM and no qualifying project-format results; optional future capability |
| Broad specialist-generated reasoning | Unqualified; guided mode uses Python facts/actions and bounded API selection with deterministic fallback |
| Train or fine-tune supplied models | No weight training performed; no verified free supported path; dataset/prompt work does not count as training |
| Provider exploration | Use supplied Gemini, Puter and Groq across nine roles; no additional key required |
| Normal schema 0012, rollout blocked | Local additive rollout through 0016; broad semantic activation remains blocked |
| Admin-only analysis | Explicit scoped guided grants for four named users, without changing business roles |
| Synthetic demo only | Synthetic demo plus approved Customer Onboarding Portal bounded observations |
| Ten requests per provider/day | Fifty per rolling 24 hours, shared; same pacing, concurrency, $0 policy and retained usage history |
| Stop before Sprint 12 | Sprint 11/11.1 local sample complete; Sprint 12 local foundations ready to start, not yet implemented |

Gemini handles financial/schedule/resource; Puter handles risk/governance/agile_coach;
Groq handles sentiment/team support/pmo/executive. One guided role/run uses at most
one 128-token request; all nine manual checklists work without an API response.
Current details: [scope](../limitations/API_DATA_SCOPE.md), [access](../limitations/USER_ACCESS.md),
[quota evidence](../limitations/QUOTA_REVIEW.md), [local usage](../limitations/TRY_IT_NOW.md).

## Sequence and acceptance

1. Sprint 11/11.1: local guided scope complete. AT17 and unrestricted model quality
   remain blocked; no independent human production acceptance is claimed.
2. Sprint 12: implement connector authority/conflicts, dated datasets with genuine
   label provenance, and reproducible small baseline pipelines. Deliver a usable
   local import-to-model-card journey. See [the implementation plan](sprint-12/LOCAL_IMPLEMENTATION_PLAN.md).
3. Sprint 13: consider forecast eligibility/serving only with the necessary data
   and evaluation evidence. A pipeline demo cannot promote an unqualified model.
4. Later sprints retain the [original roadmap](FUTURE_SPRINT_ROADMAP.md). Deployment
   work is tracked separately in [future deployment points](../limitations/FUTURE_DEPLOYMENT_POINTS.md).

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
changes must be forward-only after verifying the actual current head (0016 at
this handoff). Preserve uncommitted implementation and unrelated artifacts.

This update changes documentation and next-sprint planning only; it does not
implement Sprint 12, deploy production, change provider billing or expand data scope.
