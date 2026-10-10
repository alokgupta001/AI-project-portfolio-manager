# Enterprise PPM Intelligence and Transformation Platform

[Canonical documentation index](docs/README.md) · [Current scope and open gates](docs/00-overview/CURRENT_STATUS.md) · [Documentation tracker](docs/09-planning/DOCUMENTATION_UPDATE_TRACKER.md)


Sprint 8.1 is implemented locally at migration `0008_pilot_completion`. Eight tasks are accepted locally; real SMTP inbox verification, hosted CI and Word-guide visual QA remain open. Start with the [current user guide](docs/03-sprints/active/sprint-8.1/SPRINT_8_1_USER_GUIDE.md), [report](docs/03-sprints/active/sprint-8.1/SPRINT_REPORT.md) and [latest handoff](docs/handoffs/LATEST.md). The Sprint 08 details below remain historical implementation context.

Sprint 08 adds durable imports, integrations and live job progress to the portfolio
command center and delivery/resource/assessment workspace.
Source specifications are preserved. AI and cloud deployment remain planned.

## Start here

Learning the project? Begin with [the simple learning roadmap](docs/02-learning/00-getting-started/README.md), then follow [one complete project save](docs/02-learning/02-backend/REQUEST_LIFECYCLE.md). The guide uses current source, small examples and explicit implementation limits.

Continuing in Antigravity? Use [the token-efficient agent entry point](ANTIGRAVITY.md)
and its copy-ready prompt. Current checkpoint remains in the latest handoff.

1. Follow [identity setup and first-admin activation](docs/07-setup-and-deployment/IDENTITY-DEVELOPMENT.md), then open the [command center](http://localhost:3000/command-center) or [integrations](http://localhost:3000/integrations). Read the [Sprint 08 report](docs/03-sprints/completed/sprint-08/SPRINT_REPORT.md) and [current verification](docs/04-testing/SPRINT_VERIFICATION_REPORT.md).
2. Review the [decision register](docs/requirements/decisions-and-assumptions.md), especially scope interpretations, deployment, data handling, and budget-dependent choices.
3. Use the [roadmap](docs/requirements/roadmap.md) and [coverage matrix](docs/requirements/coverage.md) to follow the implementation sequence.
4. Before a separately authorized Sprint 09, read the [latest handoff](docs/handoffs/LATEST.md) and follow its continuation instructions.

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

Sprint 08 is implemented at migration `0007_durable_jobs`, within its documented local connector bounds. Real Jira/GitHub authentication remains unverified without operator credentials. The transaction fix makes authenticated commits finish before success responses. [Recorded CI acceptance](docs/04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md) concerns the earlier Sprint 07 checkpoint; current local results are in the [verification report](docs/04-testing/SPRINT_VERIFICATION_REPORT.md). The [isolated business demo](docs/05-demos/sprint-based/sprint-04/DEMO-DEVELOPMENT.md) uses port 3002 with its own activation. See [current limitations](docs/02-learning/08-deployment-and-operations/OPERATIONS_AND_LIMITS.md) before treating this checkpoint as production-ready.

Workspace: http://localhost:3000 · Component gallery: `/design-system` (sign-in required) · Operator diagnostics: `/system`. See the [frontend contract](docs/contracts/frontend.md) for reusable components.


## 10 October 2026 follow-up: account and website workflow repair

The separate [repair and walkthrough execution report](docs/04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) records migration `0009_account_repair`, account/membership separation, organization profile/name controls, calendar navigation, shared business errors, the verified scoped Hement grant correction, guarded training data and current tests. Earlier sprint evidence remains historical. Global production identity administration, live-provider acceptance, general document intake and AI remain PLANNED or unverified according to their existing gates; this follow-up does not close those gates.
