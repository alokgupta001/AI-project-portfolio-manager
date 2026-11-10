# Try the limited guided review

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](../03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](../03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

For the new measured experiment, follow the [financial selection pilot](FINANCIAL_SELECTION_PILOT.md)
in `/agents`: prepare 12 synthetic cases, obtain a second person's label review,
then measure one case at a time using the existing Gemini quota ledger. Preparing
and reading require no model call; AT17 remains BLOCKED.

## Sprint 12 local lab

Open `/ml` as Admin in the existing synthetic demo organization. Load a synthetic numeric example, import an immutable history version, build an as-of dataset, run/repeat the CPU baseline and inspect/download its model card. [Full user steps](../03-sprints/completed/sprint-12/USER_GUIDE.md). `/integrations` now owns connector approval, rotation/revocation and source conflict review. No new AI keys, Ollama or services are needed. Real history without genuine outcomes yields insufficient_data; synthetic metrics are not real accuracy.

**Current purpose: local sample use.** The 50/day provider ceilings are active.
Production preparation is recorded separately in
[Future deployment points](FUTURE_DEPLOYMENT_POINTS.md) for later; continue using
the local sample with the existing account, scope and checklist controls.

The local entry point is **http://localhost:3000/agents**. On 24 October 2026 the
normal local services are healthy and schema 0016 is installed. After explicit
synthetic-demo approval, **all three live API tests succeeded**: financial through
Gemini, agile coaching through Puter, and executive through Groq. Their saved
results are available now. [Exact verification](LIVE_API_VERIFICATION.md).

**Alok Gupta, Hement, Blaze and Ashu can use their existing logins.** Each has
demo-only Admin membership and guided access to Customer Onboarding Portal while
retaining their existing organization role. Its specific data-scope approval is
now received and applied: bounded requests to Gemini/Puter/Groq are enabled.
See [access, validation and shared quotas](USER_ACCESS.md).

1. Sign in with your existing Admin, or use the separate synthetic demo login stored
   privately in `artifacts/local/guided-review/demo-login.json`. The demo is ready;
   use organization **Guided Review Demo · synthetic**, project **Demo project**.
2. Open **Agents & recommendations** and select an analysis project.
3. Select **Guided review · limited, one API call** and one role.
4. Run the analysis. Read the guided checklist and the canonical evidence/coverage.
5. Expand **Review actions for all nine roles**. These remain available without API access.
6. Reopen the saved run to check persistence. Refreshing it makes no new model call.

**Rules-only checklist** means no accepted API selection was used. The code beside
it explains missing evidence, disabled configuration, quota, timeout or invalid output.
**API selection completed** means IDs were validated against this run's observations;
it does not mean unrestricted reasoning or production accuracy was approved.

Choose financial, agile_coach or executive to exercise Gemini, Puter or Groq respectively.
Cloud access is enabled for the synthetic demo and Customer Onboarding Portal. Other projects retain
rules-only checklists. The app caps each provider at one request/minute and 50/day;
one request per provider was used in this verification. The synthetic
demo includes recorded overspend and an overdue milestone. It has no five-person team
or assessed rubric, so team/governance evidence can correctly remain unavailable.
The recorded risk alone does not establish the composite risk metric: the risk
guided role correctly reports `EVIDENCE_UNAVAILABLE` until sufficient inputs exist.
The agile role can use the demo sprint's recorded status without inferring team quality.

To restart the approved demo configuration from the repository directory:

```powershell
docker compose -f compose.yaml -f compose.guided.yaml -f artifacts/local/guided-review/cloud.compose.yaml up -d --wait api worker dispatcher web
```

To turn cloud calls off while keeping the checklists available, use the checked-in
local-only configuration:

```powershell
docker compose -f compose.yaml -f compose.guided.yaml up -d --wait api worker dispatcher web
```

The second command runs existing additive migrations, enables guided checklists and
keeps cloud calls off. Do not start the old benchmark scripts alongside the live pilot.
The original normal data and earlier evaluation artifacts are preserved. Backups
and verification receipts are private under `artifacts/local/guided-review/`.

Verification: 509 backend tests passed, one skipped; migration lifecycle/drift,
two browser journeys, three responsive widths, axe checks, lint, formatting,
types, contracts and source-preservation checks passed. These are local checks,
not hosted CI or full semantic accuracy acceptance. Three real local demo runs
used zero provider calls and recorded $0. A subsequent actual localhost browser
check passed demo login, guided selection, persisted agile sprint observation,
all nine checklists and logout. The original 70-table comparison found
67 tables identical and three identity tables with one added login row each;
every original identity row was then verified against the private database backup.
All five original object files and 25 frozen configuration/source/migration files
matched their captured hashes before adding the synthetic demo.

See [the exact API data scope](API_DATA_SCOPE.md) and
[all current limits](LIMITS_AND_FUTURE_SOLUTIONS.md).
