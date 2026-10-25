# Named-user guided access and shared quotas

24 October 2026. The operator requested access for Alok Gupta, Hement, Blaze and
Ashu, then clarified **both** the shared synthetic demo and their existing projects.
This supersedes the earlier demo-only account-access scope; raw text and broader
semantic interpretation remain outside the guided API payload.

Deployed and verified locally on schema **0016_guided_project_access**. Active grants:

| User | Shared synthetic demo | Existing Customer Onboarding Portal project |
| --- | --- | --- |
| Alok Gupta | Demo-only Admin | Guided review; retains Project Manager role |
| Hement | Demo-only Admin | Guided review; retains Project Manager role |
| Blaze | Demo-only Admin | Guided review; retains Viewer role |
| Ashu | Demo-only Admin | Guided review; retains existing Admin role |

Sign in with each user's existing credentials at `http://localhost:3000/agents`.
Select **Guided Review Demo · synthetic** and **Demo project** for the approved
Gemini/Puter/Groq demo. Select **Northstar Invitation Test 2026-10-10** and
**Customer Onboarding Portal** for guided review with the same three providers.

**Project cloud scope approved and activated.** The user explicitly approved
Customer Onboarding Portal, Gemini/Puter/Groq and the bounded observation payload.
The earlier approval block is resolved. Only this project's tenant/project scope
was added to the private policy and egress rules; shared caps remain unchanged.
All nine role routes and all four user grants passed local checks. Raw documents,
unrelated projects and broad semantic tasks remain blocked. No model call was made
for activation, and quota history, failure counts and quarantine state are unchanged.

The new guided grant permits read-only analysis of structured project observations.
It does not grant project editing, membership administration, budget changes,
document analysis, assessment access, unrestricted specialist analysis or additional
project visibility. Revoking the guided grant, source grant, membership or session
stops worker authority. A guided user can cancel their own permitted run.

An additive 0016 migration introduces owner-managed project/user grants and limited
row policies. Existing 0001–0015 migration files remain unchanged. Other worker
types still require their original authority. Role promotion is confined to the
synthetic demo, as explicitly described in the approval question.

## Why the account limit exists

The initial ten-request daily limit was a conservative application pilot setting, not a
universal Gemini, Puter or Groq provider limit. One account means one shared provider
account/API-key scope, not an application login. All four users and all nine roles
share those same three account allowances across the demo and existing project.
Adding users, organizations or role profiles does not create more free capacity.

The current application caps each provider account at **50 requests per rolling
24 hours**, one per minute and one concurrent request. This limits accidental use
of the free allowance while $0 remains the operating constraint. Exhaustion leaves
the rules-only checklist available. Reopening saved results uses no model request.
The cap was raised after the subsequent account-specific checks described below;
it does not guarantee billing behavior at the provider account itself.

The subsequent [50/day review](QUOTA_REVIEW.md) verified Gemini's actual 500/day
free quota and Puter's 962.41 remaining monthly credits. The 50/day ceiling is now
active for all three accounts. Puter capacity still depends on token use and other
account activity; exhausting its allowance triggers the existing checklist fallback.

## Validation and preservation

- Full backend run: 510 passed, one skipped, one readiness failure caused by an
  outdated schema constant. After updating the constant and contracts, all five
  targeted integration/access tests passed against a freshly built image.
- Migration upgrade/downgrade/re-upgrade and schema drift checks passed. All three
  browser journeys passed, including a Project Manager guided run, accessibility
  and mobile overflow checks. Permission tests cover Viewer and Project Manager,
  revocation, cancellation and blocked budget/document/unrestricted analysis access.
- Static checks passed. Normal API, worker, dispatcher and web are healthy.
- Before granting access, all 76 established table counts/hashes matched the backup;
  all five object files and 25 frozen input/migration hashes were preserved.
- App-role database checks verified each of the four grants and demo memberships.
  Existing memberships were compared before/after and are unchanged. No email was
  sent, password changed, or additional live model request made.

Private receipts are in `artifacts/local/guided-access/`. Existing live API receipts
remain in [LIVE_API_VERIFICATION](LIVE_API_VERIFICATION.md). These checks do not
close the broad semantic accuracy gate or start Sprint 12.
