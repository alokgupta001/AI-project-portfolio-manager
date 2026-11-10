# Backend features

Each package has one business responsibility and a short guide to its files.
All 129 feature handlers are thin HTTP adapters. They call feature operations;
worker entrypoints also call those operations directly.

| Feature | Owns |
| --- | --- |
| [agents](agents/README.md) | Read-only specialists, bounded task graphs and independent analysis review |
| [ai](ai/README.md) | Evidence-grounded assistance, budgets and policy-controlled model execution |
| [assessments](assessments/README.md) | Maturity frameworks, assignments, private evidence, independent reviews and scoring |
| [capacity](capacity/README.md) | Workforce records, staffing eligibility, calendars, effort privacy and capacity |
| [command](command/README.md) | Evidence-backed current portfolio metrics and dashboard snapshots |
| [delivery](delivery/README.md) | Portfolio/project records, scoped changes, audit and optimistic concurrency |
| [documents](documents/README.md) | Versioned sources, extraction/OCR, scoped retrieval and controlled retention |
| [identity](identity/README.md) | Accounts, sessions, membership, live authorization and private account mail |
| [integrations](integrations/README.md) | Durable ingestion jobs, bounded adapters, connector authority and source conflicts |
| [ml](ml/README.md) | Versioned history/datasets, reproducible baselines and authorized ML artifacts |
| [selection](selection/README.md) | Explicitly scoped financial-selection fixture research and label review |
| [workspace](workspace/README.md) | Search, personal work, onboarding, cohort comparison and notification receipts |

[Shared record contracts and table registration](../shared/README.md) explain the
small common foundation. [main.py](../main.py) composes routers and application
resources. Feature services do not import HTTP routers. The deployment remains
the established API plus web and worker/dispatcher processes.
