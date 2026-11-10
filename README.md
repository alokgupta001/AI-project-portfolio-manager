# AI Project Portfolio Manager

AI-PPM brings portfolio/project records, resource capacity, maturity assessments,
document evidence and controlled AI review into one application.

Start with the [project map](docs/01-architecture/PROJECT_MAP.md). It explains the
folders, each backend feature and the path a request or background job follows.

```text
apps/web/                 Next.js pages, components and API proxy
services/api/ppm_api/     API startup and shared infrastructure
  modules/               Features: HTTP adapters, operations, schemas and tables
  shared/                Common record contracts and explicit table registration
services/worker/         Celery task entrypoints and scheduling
packages/contracts/      Generated API schema/types and typed client
infra/                   Container definitions and database initialization
config/                  Checked-in configuration examples
tests/                   Backend, browser and tooling regressions
scripts/                 Development, verification and operator tools
docs/                    Architecture, setup, contracts, guides and evidence
artifacts/               Generated reports, fixtures and private local outputs
```

## Understand the code

- [Backend feature map](services/api/ppm_api/modules/README.md): what each feature owns.
- [Current architecture](docs/01-architecture/SYSTEM_ARCHITECTURE.md): processes, data and authority.
- [Documentation index](docs/README.md): setup, user guides and technical references.
- [API entrypoint](services/api/ppm_api/main.py) and [worker guide](services/worker/README.md).

The backend is a modular monolith: feature packages share one API deployment and
database; the worker runs background jobs. Feature folders make ownership clear
within this existing architecture. All feature HTTP handlers are thin adapters;
operations and table definitions have explicit owners.

## Run and verify

Use the [local setup guide](docs/07-setup-and-deployment/LOCAL-DEVELOPMENT.md) for
the configured runtime. Existing installations retain their private configuration,
databases and objects. Run `npm run check` for the existing offline quality gate;
the setup guide explains isolated database/browser checks.

[Structure verification](docs/04-testing/BACKEND_STRUCTURE_STEP_32.md) records actual
checks and limitations. The [latest handoff](docs/handoffs/LATEST.md) records current
authorization and operational state. Schema remains **0020**; live-model quality,
production deployment and successor-sprint work retain their existing gates.

Earlier dated README checkpoints are preserved in the
[history](docs/10-reference/history/PROJECT_README_BEFORE_STRUCTURE_CLEANUP.md).
