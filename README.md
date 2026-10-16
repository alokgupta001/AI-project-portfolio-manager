# Enterprise PPM Intelligence and Transformation Platform

**Closeout — 16 October 2026: Sprints 8.1 and 10 are COMPLETED for their implemented development scope.** The reviewed application checkpoint `631c149` passed [hosted CI](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/38885041673), including regression, migration and browser checks. The current pilot Word guide is rendered and visually verified in the linked closeout evidence. Earlier blocked/active statements below describe their recorded checkpoints. Production deployment, broad real-model/agent quality and scale remain OPEN release/successor gates. Stop before 11. [Detailed closeout](docs/10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md).

Current checkpoint — 16 October 2026: Sprints 8.1 and 10 are COMPLETED for their implemented development scope at `0012_ai_runtime`. Reviewed application checkpoint `631c149` passed hosted CI; 201 backend tests and the document browser regression passed. A current pilot Word guide is rendered and visually verified. Gemini bounded completion/embedding smoke passed at maximum spend $0; confirmation does not expire daily. Production deployment, scale and broad agent/model quality remain OPEN release/successor gates. Sprint 11 is not started. Stop before 11.

[Canonical documentation index](docs/README.md) · [Current scope and open gates](docs/00-overview/CURRENT_STATUS.md) · [Documentation tracker](docs/09-planning/DOCUMENTATION_UPDATE_TRACKER.md)


Sprint 8.1 reached `0008_pilot_completion`; subsequent account repairs reached 0010 and Sprint 09 reached 0011. Development Gmail signup, Viewer invitation and recovery were verified on 10 October. The reviewed application checkpoint passed hosted CI; the current pilot Word guide has completed visual QA. Start with the [current user guide](docs/03-sprints/completed/sprint-8.1/SPRINT_8_1_USER_GUIDE.md), [report](docs/03-sprints/completed/sprint-8.1/SPRINT_REPORT.md) and [latest handoff](docs/handoffs/LATEST.md). The Sprint 08 details below remain historical implementation context.

Historical Sprint 08 contribution: durable imports, integrations and live job progress to the portfolio
command center and delivery/resource/assessment workspace.
Source specifications are preserved. Later document intake and the bounded Gemini evidence preview are implemented; semantic agents and cloud deployment remain planned.

## Start here

Learning the project? Begin with [the simple learning roadmap](docs/02-learning/00-getting-started/README.md), then follow [one complete project save](docs/02-learning/02-backend/REQUEST_LIFECYCLE.md). The guide uses current source, small examples and explicit implementation limits.

Continuing in Antigravity? Use [the token-efficient agent entry point](ANTIGRAVITY.md)
and its copy-ready prompt. Current checkpoint remains in the latest handoff.

1. Follow [identity setup and first-admin activation](docs/07-setup-and-deployment/IDENTITY-DEVELOPMENT.md), then open the [command center](http://localhost:3000/command-center) or [integrations](http://localhost:3000/integrations). Read the [Sprint 08 report](docs/03-sprints/completed/sprint-08/SPRINT_REPORT.md) and [current verification](docs/04-testing/SPRINT_VERIFICATION_REPORT.md).
2. Review the [decision register](docs/requirements/decisions-and-assumptions.md), especially scope interpretations, deployment, data handling, and budget-dependent choices.
3. Use the [roadmap](docs/requirements/roadmap.md) and [coverage matrix](docs/requirements/coverage.md) to follow the implementation sequence.
4. Before any separately authorized Sprint 11, read the [latest handoff](docs/handoffs/LATEST.md) and follow its continuation instructions.

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

The separate [repair and walkthrough execution report](docs/04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) records migration `0009_account_repair`, account/membership separation, organization profile/name controls, calendar navigation, shared business errors, the verified scoped Hement grant correction, guarded training data and current tests. Earlier sprint evidence remains historical. Global production identity administration, live connector acceptance and AI retain their gates; general document intake/OCR/keyword citations subsequently shipped locally in Sprint 09; this follow-up does not close those gates.
