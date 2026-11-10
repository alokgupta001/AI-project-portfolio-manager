# Enterprise PPM Intelligence and Transformation Platform

## 30 October 2026 — ordinary guided cloud timeout

[Approved timeout follow-up](docs/03-sprints/active/sprint-12.1/TIMEOUT_FOLLOWUP.md): new ordinary cloud guided reviews can wait up to **60 seconds**, recorded per run. Normal schema is **0020** after a forward-only migration; all 83 table hashes matched. Existing fixture pilots retain **22 seconds**, the **20-second gate**, and their stopped results. Legacy runs retain their original limit. Shared quotas, $0 policy and access remain unchanged; **AT17 stays BLOCKED**. No new model call, PR, push, deployment or Sprint 13 work.

Validation: 580 full-suite passes plus two corrected test assertions verified in a **28-pass focused rerun** (overlapping); one skip. Migration lifecycle/drift, static/contracts and **two browser journeys** passed. See the linked report for exact evidence and limitations. Earlier dated sections below are historical.

## 28 October 2026 — Sprint 12.1 timing repair

[Current repair report](docs/03-sprints/active/sprint-12.1/REPAIR_FOLLOWUP.md) supersedes the operational checkpoint below. Failed calls retain elapsed timing; UI/downloads distinguish unavailable time from accepted-response p95. Separate repair pilot `3f0f3a7f`: **insufficient_data**, 5/12 measured, 5 exact matches, 1 unavailable, 0/6 reserved measured; accepted-case p95 7936 ms. Original ce874a14 history remains unchanged; experiments are not combined. Automated audit records **human_reviewed=false**. Broad **AT17 remains BLOCKED**.

Fresh validation: **566 backend passed, 1 skipped**, one inherited warning; disposable migration lifecycle/drift, two browser journeys, static/contracts and tooling checks passed. Normal schema remains frozen **0019**. Provider configuration, explicit grants, shared limits and $0 policy are preserved. No commit, PR, push, deployment or Sprint 13 work. The single repair experiment is complete under its gate/stop rule; do not start another without authorization.

## Earlier dated checkpoint (historical)

**Sprint 12.1 — [Current API financial selection pilot](docs/03-sprints/active/sprint-12.1/README.md)**
provides a usable `/agents` fixture experiment using the existing Gemini route and
shared ledger. The owner-approved automated audit checked 12/12 fixed labels with
human review false. Two real cases were attempted: f01 matched in 21.437 seconds;
f02 timed out, stopping the pilot. The saved report is **insufficient_data**,
with 10 unattempted and zero held-out measured cases. No fixture or broad AT17 pass.
[Actual record](docs/03-sprints/active/sprint-12.1/RUN_RECORD.md) ·
[User guide](docs/limitations/FINANCIAL_SELECTION_PILOT.md).

Normal schema remains **0019**. Fresh validation: 562 backend passed/one skipped,
disposable lifecycle/drift and two pilot browser journeys passed. Access, provider
scopes, shared ceilings and original artifacts are preserved. The one-pilot
automated option defaults off; other pilots retain the distinct-person review.
No new publication, training, serving or Sprint 13 work.

Sprint 12 closed for the bounded local sample at schema **0018**. The
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
Never reset normal data or edit applied 0001–0019 migrations. Default web/API ports
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
