# Follow up handoff document template

The implementing assistant must update this record after every sprint and before a context reset. It carries the exact state needed by the next prompt. Keep the latest record concise enough to read in full; link detailed histories and evidence.

Copy this template to `docs/handoffs/SPRINT-NN-HANDOFF.md`, then update `docs/handoffs/LATEST.md` to contain the latest handoff or an unambiguous link to it.

```markdown
# Sprint NN technical handoff

## Verified checkpoint
Sprint and status:
Date:
Branch and commit if available:
Uncommitted changes and ownership:
Last verified runtime environment:
Matching implementation report:
Completed requirement IDs:
Open or partially complete requirement IDs:

## Read these files first
List exact repository-relative paths to the master prompt, source scope matrix,
relevant ADRs, domain model, OpenAPI/client contracts, metric definitions,
latest migration, key implementations and test evidence. Explain each briefly.

## Current implementation
List working modules, routes, services, jobs and enabled feature flags.
List mocked providers and disabled or experimental features separately.
Summarize shared entities and ownership; do not duplicate the whole schema.

## Contracts the next prompt must preserve
Tenant/role enforcement:
API and event versions:
Authentication/session flow:
Database migration head:
Risk/maturity/KPI formulas and versions:
AI output schemas and provider interface:
Storage, vector and graph ownership:
Design tokens and shared components:
Document any planned deprecation and consumer migration path.

## Reproduce the current state
Exact install, environment bootstrap, migration, seed, run and test commands:
Required services and local ports:
Configuration names and secret provisioning instructions without values:
Known deterministic fixture identifiers:
Last executed commands, outcomes and evidence paths:
Tests not run and why:

## Data and migration state
Latest applied migration and expected schema:
Backfills complete or pending:
Seed/demo data boundaries:
Recovery or rollback constraints:
Vector/graph index version and rebuild status if applicable:

## Known issues and unresolved choices
For each issue: reproducible trigger, observed behavior, expected behavior,
impact, affected files, evidence, workaround and next action. Link rather than
copy large logs. Record source conflicts and who must resolve them.

## Next sprint instructions
Next sprint ID and objective:
Verified prerequisites:
Prerequisites still blocked:
Files/modules likely to change:
Required acceptance checks:
Specific compatibility risks and protections:
Scope boundaries:

## Copy ready next prompt
Continue Sprint [NN+1] using docs/prompts/MASTER.md and its ordered sprint prompt.
Read this handoff and its linked source/contract files first. Verify the actual
repository checkpoint and resolve listed prerequisite failures. Preserve the
recorded contracts. Implement the sprint, execute its acceptance checks, create
its implementation report, and update the handoff and requirement coverage.
```

## Context recovery prompt

```text
Recover the project state before writing new features. Read LATEST.md, the
latest sprint report, coverage, ADRs, contracts, git status and migrations.
Compare claims with actual code and available test artifacts. List discrepancies
and recreate missing continuity information from the repository without inventing
history. Mark anything unverified. Update the handoff, then proceed with the next
sprint only if its prerequisites are satisfied.
```
