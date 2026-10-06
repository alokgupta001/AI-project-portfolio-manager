# Sprint 00 technical handoff

## Verified checkpoint

Date: 2026-10-05. Sprint: 00. Status: planning complete. Workspace: `C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm`. Git branch `main`, no commits or remote. Project files are uncommitted, created during this task. Do not treat the original prompt pack in the parent folder as application code.

Completed requirements: P-001–P-005 planning deliverables. Functional, nonfunctional and enhancement implementation rows remain Planned; alternative technology/source-passage rows marked Resolved in plan are not implemented features. See [report](../sprints/SPRINT-00-REPORT.md) and [checks](../verification/SPRINT-00-CHECKS.md).

## Read these files first

1. [Master entry](../prompts/MASTER.md) and [ordered prompts](../prompts/02-ORDERED-SPRINT-PROMPTS.md): execution rules and Sprint 01 scope.
2. [Source index](../source/INDEX.md), original files and extract: source authority and exact heading map.
3. [Coverage](../requirements/coverage.md), [decisions](../requirements/decisions-and-assumptions.md), [roadmap](../requirements/roadmap.md): requirements and proposed assumptions.
4. [Architecture](../architecture/overview.md), [data model](../architecture/data-model.md), [ADRs](../architecture/adr/README.md): module ownership and tradeoffs.
5. [Permissions](../contracts/permissions.md), [API/events](../contracts/api-events.md), [metrics](../contracts/metrics.md), [quality plan](../requirements/quality-plan.md): shared invariants.

## Current implementation

Working modules/routes/services/jobs: none. Mock providers: none. Enabled feature flags: none. Runtime dependencies/locks/Docker/CI: not created. Source extraction used built-in ZIP/XML reading; this is documentation processing, not application code. The only executable file is the Sprint 00 documentation verification script.

## Contracts to preserve

- Global user identity with organization memberships and scoped project grants. RLS plus app checks; non-bypass application DB role.
- Versioned `/api/v1`, generated frontend types, decimal strings/currency, UTC instants and explicit date/calendar semantics.
- Short-lived JWT plus server-side session/membership revocation; browser secure cookies/CSRF controls.
- Single future Alembic chain; current migration head is **none**.
- Shared `metrics-v1-proposed` and `risk-rule-v1` definitions; proposed thresholds need product review. Never substitute risk scores for probabilities.
- Typed provider/retrieval/tool interfaces and evidence-bearing outputs; AI cannot directly execute material changes.
- PostgreSQL authority; object metadata with access control; pgvector and Neo4j derived indexes.
- Shared accessible enterprise tokens/components start in Sprint 03; do not separately reinvent module designs.

No deprecation/migration is active. Architecture ADRs are proposed, not owner-approved; use them as reversible engineering defaults unless the user steers otherwise.

## Reproduce current state

From the project root in PowerShell:

```powershell
./docs/verification/check-sprint-00.ps1
git status --short --branch
```

Evidence: [source preservation manifest](../source/source-manifest.json), [verification results](../verification/SPRINT-00-CHECKS.md). Required services/ports: none yet. Configuration/secrets: none. Fixture identifiers: none. Tests not run: all application/database/browser/provider/model checks, because implementation is absent. The documentation verifier checks files, hashes, sequence, IDs and links only.

## Data and migration state

No database/schema, migration, seed, backfill, vector index or graph exists. No production data imported. Originals and prompts are preserved in source/prompts; source copies should remain unchanged. Recovery is a normal file/Git history concern at this stage; no database rollback has been tested.

## Known issues and decisions

No unresolved workspace-copy failure. Local Git has no commit yet, so no immutable code checkpoint hash is available. Runtime tool availability and version compatibility are unverified. Production budget/region/provider/retention/model labels remain later-stage decisions.

The source prompts have forward dependency ambiguities addressed in architecture: Sprint 09 semantic extraction uses the Sprint 10 gateway and receives final integration acceptance in Sprint 11; never introduce an ad-hoc competing provider stack. Sprint 06 review history must survive Sprint 15 workflow integration. These are planning clarifications, not code fixes already applied.

## Next sprint instructions

Sprint 01 objective: local reproducible web/API/worker foundation with runtime config, dependency locks, initial migration chain, generated contracts, health/readiness, Docker Compose and CI. Scope is foundation only, not full authentication/domain modules.

Verified prerequisites: both specifications, complete prompt set, module/data/permission/metric contracts and traceability. No owner decision prevents a local reversible foundation. Inspect actual tool availability and verify supported compatible versions from official sources before installs. Use proposed ports 3000 web, 8000 API, 5432 PostgreSQL, 6379 Redis only after checking local conflicts; document actual chosen values. Object storage adapter ports are to be selected with runtime choice.

Expected areas: `apps/web`, `services/api`, `services/worker`, `packages/contracts`, `infra`, `tests`, root runtime files and updated docs. Required checks: fresh setup, service readiness, database round-trip, migrations, frontend load, reproducible API client generation and relevant CI commands. Avoid premature domain-table creation and external paid provisioning.

## Copy ready next prompt

```text
Execute Sprint 01 only in the enterprise-ppm workspace.
Read docs/prompts/MASTER.md and Sprint 01 in the ordered prompt file.
Read docs/handoffs/LATEST.md, the Sprint 00 report, coverage, decisions,
architecture and shared contracts, then verify the actual workspace state.

Use the proposed architecture as the local development baseline. Verify runtime
availability and supported compatible versions, then implement Sprint 01's
reproducible web/API/worker foundation. Preserve the source originals and contracts.
Do not provision paid cloud services or implement later domain modules.

Run the foundation acceptance checks and record actual results and limitations.
Create the Sprint 01 report and technical handoff; update LATEST, coverage and
changelog. Stop after Sprint 01.
```
