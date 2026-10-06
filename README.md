# Enterprise PPM Intelligence and Transformation Platform

Sprint 05 adds resource profiles, working calendars, staffing, capacity/effort measures
and immutable allocation snapshots to the existing delivery workspace. Source specifications
are preserved. Assessments, AI and cloud deployment remain planned.

## Start here

Continuing in Antigravity? Use [the token-efficient agent entry point](ANTIGRAVITY.md)
and its copy-ready prompt. Current checkpoint remains in the latest handoff.

1. Follow [identity setup and first-admin activation](docs/IDENTITY-DEVELOPMENT.md), then open [resource planning](http://localhost:3000/resources). Read the [Sprint 05 report](docs/sprints/SPRINT-05-REPORT.md) and [actual checks](docs/verification/SPRINT-05-CHECKS.md).
2. Review the [decision register](docs/requirements/decisions-and-assumptions.md), especially scope interpretations, deployment, data handling, and budget-dependent choices.
3. Use the [roadmap](docs/requirements/roadmap.md) and [coverage matrix](docs/requirements/coverage.md) to follow the implementation sequence.
4. Before a separately authorized Sprint 06, read the [latest handoff](docs/handoffs/LATEST.md) and use its prepared next prompt.

## Documentation map

| Location | Purpose |
| --- | --- |
| [Source index](docs/source/INDEX.md) | Preserved originals, readable extract, hashes and exact heading references |
| [Master instruction](docs/prompts/MASTER.md) | Stable entry point to the master prompt |
| [Ordered prompts](docs/prompts/02-ORDERED-SPRINT-PROMPTS.md) | Sprint 00 through 23 implementation instructions |
| [Product scope](docs/requirements/product-scope.md) | Personas, terminology, journeys and navigation |
| [Architecture](docs/architecture/overview.md) | Components, ownership, inputs, outputs and failure behavior |
| [Data model](docs/architecture/data-model.md) | Entity relationships, invariants and ownership |
| [Decision records](docs/architecture/adr/README.md) | Technology decisions and alternatives |
| [Permissions](docs/contracts/permissions.md) | Roles, tenant boundaries and project visibility |
| [API and event contracts](docs/contracts/api-events.md) | Versioning, errors, jobs, concurrency and AI output envelopes |
| [Metric dictionary](docs/contracts/metrics.md) | Versioned formulas, periods, calendars and thresholds |
| [Quality plan](docs/requirements/quality-plan.md) | Acceptance evidence and measurable nonfunctional targets |

## Current setup

Open `C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm` as the project folder. Use Python 3.12 to run `scripts/bootstrap.py`, then `docker compose up --build -d --wait` with Docker's Linux engine running. The setup guide covers executable paths, frozen installs and test commands. Web/API ports are 3000/8000; database/broker host ports are 15432/16379. Configuration secrets remain in ignored `.env`.

Sprint 04 is complete locally. Start with `/organization` as Admin, then `/portfolios` and `/projects`. The normal local Demo tenant was preserved; [isolated business demo](docs/DEMO-DEVELOPMENT.md) runs on port 3002 with its own activation. Git has no commit or remote; hosted CI has not run. Sprint 05 requires separate authorization.

Workspace: http://localhost:3000 · Component gallery: `/design-system` (sign-in required) · Operator diagnostics: `/system`. See the [frontend contract](docs/contracts/frontend.md) for reusable components.
