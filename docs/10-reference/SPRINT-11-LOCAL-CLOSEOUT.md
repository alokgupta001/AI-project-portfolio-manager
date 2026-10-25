# Sprint 11 and 11.1 local-sample closeout

25 October 2026. **Complete for the implemented local guided-sample scope; ready
to start Sprint 12's local foundations.** This is a narrower disposition than full
original AI acceptance: broad semantic accuracy **AT17 remains BLOCKED**. Sprint
12 has not been implemented by this documentation update.

## Current delivered scope

| Area | Current state |
| --- | --- |
| Runtime | Local schema `0016_guided_project_access`; existing records and objects preserved |
| Guided review | Python owns calculations, observations and displayed actions; one optional API call selects at most two IDs from eight observations |
| Output/fallback | 128 output tokens, no retry; all nine manual checklists remain available when evidence or APIs are unavailable |
| Role assignments | Gemini: financial, schedule, resource. Puter: risk, governance, agile_coach. Groq: sentiment/team support, pmo, executive |
| Access | Alok Gupta, Hement, Blaze and Ashu have demo-only Admin plus scoped guided grants for Customer Onboarding Portal; existing business roles preserved |
| Cloud scope | Synthetic demo and Customer Onboarding Portal only, using the approved bounded observations; no raw documents, names, assessment answers or personal notes |
| Quotas | 50 requests per rolling 24 hours per provider account and tenant, shared across users/projects/roles; one/minute and one concurrent request |
| Local model/training | Ollama stopped; no weight training or fine-tuning performed |

Use [the local walkthrough](../limitations/TRY_IT_NOW.md). Saved result reopening
does not call a provider. The $0 policy remains; request caps do not independently
control external billing. Puter's monthly credit is token-dependent, so 50/day is
a ceiling rather than guaranteed sustained throughput. See [quota evidence](../limitations/QUOTA_REVIEW.md).

## Recorded validation, with its limits

The latest access checkpoint recorded **510 backend tests passed, one skipped and
one stale-schema readiness failure**. After correcting the constant/contracts,
all five targeted integration/access tests passed against a rebuilt image. This
is not a claim of a subsequent fully green backend run. Migration lifecycle/drift,
three browser journeys including accessibility/mobile checks, and static/contract
checks passed. See [access evidence](../limitations/USER_ACCESS.md).

Earlier approved synthetic runs succeeded once per Gemini/Puter/Groq; saved UI
results reopened without new calls. Access and quota changes used no additional
inference. See [live verification](../limitations/LIVE_API_VERIFICATION.md).
Before access grants, all 76 established table counts/hashes, five objects and
25 frozen input hashes matched; existing business memberships remained unchanged.

The implementation remains uncommitted on `sprint-11-1-review-closeout`, based on
`e3bf8a3`, with unrelated verification artifact changes preserved. This closeout
does not claim fresh hosted CI, a new PR, independent human acceptance or production
readiness. The documentation reconciliation itself adds no runtime test results.

## Carry-forward gates

Documentation validation on 25 October: 831 local Markdown file links across the
affected pages resolved; `git diff --check` passed; the preservation helper's
`check()` against `artifacts/local/guided-review/files-before.json` passed all 25
frozen configuration/source/prompt/migration hashes. No application tests were
rerun for this documentation-only change.

- Broad model reasoning/accuracy AT17 is blocked. The rejected output audit and
  original evaluation evidence remain unchanged. Guided selection usefulness is
  also not independently measured; format validity is not semantic accuracy.
- Limited RAM prevents the intended local Ollama deployment. The local sample
  requires no new provider, model training or paid capacity.
- Genuine historical labels and authorized live connector access must be checked
  during Sprint 12; fixtures cannot establish live integration or model quality.
- Production controls and release validation remain in [future deployment points](../limitations/FUTURE_DEPLOYMENT_POINTS.md)
  and the original full product release criteria.

The roadmap permits dependent work against verified interfaces or disabled
fallbacks. Sprint 12 can therefore build source history, connector authority,
datasets and baseline pipelines without relying on unqualified LLM outputs.
Failed access or integrity checks still block dependent work.

Read the [reconciled plan](../09-planning/LOCAL_SAMPLE_PLAN_UPDATE.md),
[Sprint 12 implementation plan](../09-planning/sprint-12/LOCAL_IMPLEMENTATION_PLAN.md)
and [copyable starting prompt](../09-planning/sprint-12/START_PROMPT.md).
