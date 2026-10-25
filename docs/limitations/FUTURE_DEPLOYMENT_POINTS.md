# Future deployment points — local sample first

## Sprint 12 deployment follow-up — open/deferred

Before deployment, move connector environment references into a chosen secret manager, test provider-side credential rotation/revocation and exact authorized live-source equality, and define connector approval/expiry ownership. Review immutable history/export retention, permanent withdrawal, erasure/backups and copies downloaded before withdrawal. Validate provenance and independent genuine outcome labels for each target. Establish production-sized CPU/memory limits, queue monitoring, model review and native MLflow tracking/import if required. XGBoost/text candidates need justified data/resources; no hosted fine-tuning is implied. Forecast promotion/serving is Sprint 13 and remains blocked. These items do not prevent the bounded local fixture/manual-import sample; no deployment is authorized.

**Decision recorded: 25 October 2026.** The owner is building and checking a local
sample now. Production preparation below is deferred until deployment is planned;
it is not additional work required to continue using the current local sample.
This file records future work, not completed production acceptance.

## Use now

- Run the app locally at `http://localhost:3000/agents` using the existing Compose
  setup and supplied Gemini, Puter and Groq accounts. Local hosting still sends
  the approved bounded observations to those external APIs.
- Keep the active **50 requests per rolling 24 hours per provider account**, shared
  across users and authorized projects. Keep one request/minute, one concurrent
  request, the 128-token guided output cap and the $0 operating policy.
- Alok, Hement, Blaze and Ashu can use the shared synthetic demo and guided review
  for Customer Onboarding Portal. Existing business roles remain unchanged.
- Each guided run uses at most one assigned provider. All nine role checklists
  remain usable when a provider is unavailable, returns invalid output or runs out
  of allowance. Saved results can be reopened without new model calls.
- Ollama remains off. No additional keys, paid plan, fine-tuning or production
  hosting setup is required for this sample.

The current configuration and measured allowance evidence are in
[QUOTA_REVIEW](QUOTA_REVIEW.md); startup instructions are in
[TRY_IT_NOW](TRY_IT_NOW.md). Keep current access and data protections enabled during
local use. Deferring deployment work does not authorize widening data access or
provider billing.

## Before exposing the app beyond local use

| Point | Work to do when deployment is planned | Evidence to record |
| --- | --- | --- |
| Hosting and configuration | Select the deployment target, expected users and budget. Create environment-specific configuration; review origins, cookies, TLS, ports, network access and database/service permissions. Do not expose the local Compose setup directly. | Named environment, reviewed configuration, HTTPS and readiness checks; authorization for the actual deployment. |
| Secrets and provider accounts | Move private local keys into the deployment's secret store. Establish key rotation and revocation, account ownership and separate development/production credentials where appropriate. Never bundle local env files, database dumps or receipts into an image or public repository. | Secret scan, deployed secret references, rotation/revocation exercise and account owner. |
| Quotas and fair use | Recheck provider quotas for the selected models and account tiers. Size daily/token/concurrency limits for real demand; introduce suitable per-user/tenant allocation without multiplying a shared account's allowance. Unify benchmark and application usage accounting. | Account quota snapshot, load assumptions, shared-ledger tests and exhaustion behavior. |
| Puter monthly credit | Add credit monitoring/reservation and useful low-balance alerts. Measure representative input/output sizes and include other account usage; do not assume the small demo's cost is a worst-case bound. | Monthly budget calculation, current price/allowance evidence, depletion/reconciliation tests and fallback demonstration. |
| Billing policy | Decide whether the deployed service must remain free-only or has an explicitly approved spend budget. Apply provider-side billing controls and app-side budgets; a request count or app `$0` flag alone cannot enforce an external account's billing settings. | Documented budget decision, account settings and tested budget-stop behavior. |
| Users and authorization | Replace sample membership assumptions with intended organization/project roles. Review demo-only Admin accounts, invitations, session lifecycle and guided grants. Verify revocation across queued work and result reads. | Cross-tenant Admin/PM/Viewer tests, negative permission tests and access review. |
| Data scope and privacy | Decide which deployed projects and categories may leave the host and for which providers. Review retention, deletion, logging and any provider data-processing requirements. Existing approvals cover only the two documented local project scopes. | Approved scope matrix, payload/log inspection and deletion/retention tests. |
| AI claims and acceptance | Keep guided selection clearly distinguished from broad reasoning. Before advertising unrestricted nine-agent reasoning, semantic scoring or forecasts, complete the corresponding evaluations and independent acceptance. AT17 remains open. | Frozen evaluation set/strategy, per-role results, abstention and source checks, reviewer decision. |
| Reliability and monitoring | Add deployment monitoring for API/worker health, queue age, provider failures, quota/credit exhaustion and resource use. Test timeout, cancellation, worker restart and duplicate-delivery behavior in the chosen environment. | Alert checks, outage/recovery exercises and measured service behavior. |
| Backup and migration | Arrange database/object backups, retention, secure storage and a restore procedure. Test forward migration from preserved data and rollback/recovery before rollout. | Restore to a separate environment, reconciled records/files and measured recovery time/data loss. |
| Capacity and performance | Size RAM/CPU/storage for the app and workers; test realistic users and data volumes. Reconsider local inference only if later hardware and quality measurements justify it. | Hardware profile, representative load results and agreed latency/capacity limits. |
| Release and handoff | Review the final branch/PR and hosted CI, run deployment-specific security/accessibility checks, prepare operator/user instructions and assign incident ownership. Distinguish a limited pilot release from the full product. | Exact revision, CI/test receipts, release checklist, rollback procedure and scope-specific acceptance. |

All deployment items above are **open/deferred**. Set an owner and target release
when deployment work starts; mark an item complete only with its linked evidence.
Do not treat this checklist as a request to deploy, purchase services, change
billing, rotate keys or start the next sprint now.

## Revisit in this order

1. Choose the release scope, hosting target, account owners and budget.
2. Verify provider capacity, monthly cost, permitted data and user access.
3. Configure the deployment, secrets, backups, monitoring and recovery procedures.
4. Run the required acceptance checks and a staged rollout with rollback available.

Broader feature work remains in the [future sprint roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md).
The [full product release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md)
remain authoritative for a full release. The detailed
[limitations register](LIMITS_AND_FUTURE_SOLUTIONS.md) preserves the unresolved
requirements; this file separates their deployment follow-up from today's local use.
