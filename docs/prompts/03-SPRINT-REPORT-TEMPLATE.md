# Sprint implementation report template

The implementing assistant must create a separate report after every prompt or sub-sprint. This is the explanatory document for the product owner, reviewer, and future developer. Fill it with observed facts after implementation; do not fill future sprints with imagined accomplishments.

Copy this template to `docs/sprints/SPRINT-NN-REPORT.md`.

```markdown
# Sprint NN implementation report

## Status and scope
Date, sprint name, status (complete / partial / blocked), repository revision
when available, dirty-worktree note, requirement IDs, and source sections.
State exactly which acceptance criteria passed and which remain open.

## What was built
Describe user-visible capabilities and the roles that can use them. Identify
working UI routes, API operations, background jobs, and persisted entities.
Separate complete capabilities from demos, disabled features, and placeholders.

## Why it was built
Explain the business problem, connection to enterprise PPM, and how this sprint
enables later modules. Reference approved requirements rather than inventing
benefits. Explain important tradeoffs and link to architecture decisions.

## How it works
Describe a concrete input-to-output flow: user action, authorization, validation,
API/service, database or queue, AI/ML step if present, and resulting UI state.
Include a small sequence/data diagram where it helps. Define formulas and units.
Explain failure paths, retries, idempotency, and recovery in plain language.

## How to use and demonstrate it
List prerequisites and exact setup/run commands. Provide a short role-specific
walkthrough with labeled demo data, expected results and screenshot references.
List configuration variable names and where to obtain credentials, never values.

## Implementation record
List important changed files with their purpose. Record schema changes,
migration identifiers, API/event changes, configuration, dependencies, and
feature flags. Explain tenant, role, accessibility and audit implications.

## Verification evidence
| Acceptance criterion | Check or command | Result | Evidence path |
| --- | --- | --- | --- |
| Fill with actual criterion | Actual execution | Pass / fail / not run | Artifact |

Record environment, fixtures and test scope. Include affected regression tests
and negative permission cases. For UI work include responsive/keyboard checks.
For AI/ML include dataset version, evaluation results, failure examples and
limitations. A plausible model response is not evidence of general accuracy.

## Operational and security behavior
Describe logs, metrics, alerts, external calls, cost limits, data handling,
retention, and recovery steps introduced or changed by this sprint.

## Remaining work and decisions
List defects, impact, workaround, owner or next sprint, and blockers. Distinguish
accepted tradeoffs from unfinished required behavior. Link decision records.

## Next sprint readiness
State whether the next sprint's dependencies are verified. Link the matching
handoff and coverage matrix. Provide the next sprint ID and short rationale.
```

## Standalone documentation prompt

```text
Create or repair the implementation report for Sprint [NN] using this template.
Inspect the actual diff, code, migrations and test artifacts. Explain what was
built, why and how at a level a product owner can follow, with technical links
for the next developer. Do not infer completion from a plan or previous summary.
If evidence is missing, mark it unverified and list the verification needed.
Update the handoff separately; do not replace technical continuity with prose.
```
