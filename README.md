# Enterprise PPM Intelligence and Transformation Platform

Sprint 12 is complete for the bounded local sample at schema **0018**. The
[reviewed application closeout](docs/10-reference/SPRINT-12-LOCAL-CLOSEOUT.md)
records passing CI and CodeRabbit review for `f93a596`. Full live/model acceptance
remains open: **AT17 is BLOCKED**, live connector credentials and sufficient verified
outcome labels were unavailable. No production deployment or Sprint 13 work is claimed.

## Use the local sample

Open http://localhost:3000 with an existing activated account and select the intended
organization. Roles and explicit project grants remain authoritative.

- [User guide](docs/06-user-guides/USER_GUIDE.md): existing identity, portfolio,
  delivery, resource, assessment, document, guided AI and baseline journeys.
- [Sprint 12 walkthrough](docs/03-sprints/completed/sprint-12/USER_GUIDE.md): approve
  connector authority/review conflicts in `/integrations`, then import history,
  build a dataset and run/repeat/download a CPU model card in `/ml` as Admin.
- [Guided review](docs/limitations/TRY_IT_NOW.md): Gemini/Puter/Groq retain the
  approved data scopes and four-user access, shared 50/day per-provider ceilings,
  one/minute pacing and $0 policy. Ollama remains off.
- [Demo guide](docs/05-demos/CURRENT_DEMO_GUIDE.md): use clearly labelled synthetic
  fixtures. Their scores are pipeline evidence, never real-world model accuracy.

## Start or continue safely

Use `C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm` as the project root.
For an established installation, retain its private `.env`, Compose overlays, database,
objects and usage history. Follow [existing local setup](docs/07-setup-and-deployment/LOCAL-DEVELOPMENT.md)
and [the latest handoff](docs/handoffs/LATEST.md); bootstrap is for a fresh installation.
Never reset normal data or edit applied 0001–0018 migrations. Default web/API ports
are 3000/8000; the isolated browser project uses 3001/8001.

## Read, learn and verify

- [Documentation index](docs/README.md), [current status](docs/00-overview/CURRENT_STATUS.md)
  and [feature catalogue](docs/00-overview/FEATURE_CATALOGUE.md).
- [Plain-language Sprint 12 report](docs/11-plain-language-sprint-reports/completed/SPRINT-12.md)
  and [learning roadmap](docs/02-learning/00-getting-started/README.md).
- [Architecture](docs/01-architecture/SYSTEM_ARCHITECTURE.md),
  [actual API](docs/01-architecture/18-api-contracts.md),
  [schema](docs/01-architecture/DATABASE-DICTIONARY.md) and
  [local baseline contract](docs/contracts/ml.md).
- [Actual validation](docs/04-testing/sprint-based/sprint-12/TESTING_REPORT.md),
  [review fixes](docs/verification/sprint12/REVIEW_FIXES.md),
  [coverage](docs/requirements/coverage.md) and
  [documentation tracker](docs/09-planning/DOCUMENTATION_UPDATE_TRACKER.md).
- [Agent entry point](ANTIGRAVITY.md), [source index](docs/source/INDEX.md) and
  [decision register](docs/requirements/decisions-and-assumptions.md).

[PR 7](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/7) contains
the implementation and fixes. The 21 pre-existing verification artifact edits remain
local and preserved. Source/prompts, dated sprint evidence and archived Word snapshots
retain their original results. Current operator/user instructions are the maintained
Markdown guides. [Future deployment points](docs/limitations/FUTURE_DEPLOYMENT_POINTS.md)
record production work without requiring it for this local sample.
