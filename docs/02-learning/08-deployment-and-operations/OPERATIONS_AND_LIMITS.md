# Current status, setup and verification limits

[Learning roadmap](../00-getting-started/README.md)

Current verification: **9 October 2026**, Git base **`9056440`** plus preserved uncommitted Sprint 08/8.1 changes, with migration chain ending **`0008_pilot_completion`**. Sprint 8.1 is implemented locally with open parent acceptance. See [fresh verification results](../../04-testing/SPRINT_VERIFICATION_REPORT.md); older acceptance records retain their historical scope.

## Complete slices, partial features and plans

| Status | Scope | Current source / how to inspect |
| --- | --- | --- |
| Implemented within stated limits | Identity, delivery, capacity, versioned assessments, four command-center views, risk/benefit records and saved filters | Owning API modules, frontend components and tests described in chapters 2–8 |
| Implemented diagnostic | Celery database checkpoint, readiness, generated contracts, CI definition | `services/worker/ppm_worker/app.py`, `main.py`, `scripts/contracts.mjs`, `.github/workflows/ci.yml` |
| Partial against broad product requirements | Evidence intake/review and activation/reset delivery | Narrow UTF-8 text plus manual release; local-preview alternative plus verified development Gmail signup/invitation/recovery; no general document/scanning pipeline |
| Browser administration | Scoped assessment access | `assessment.set_access` and browser Framework/Assessment Access panels now exist |
| Implemented within local bounds | Durable jobs/outbox, CSV and labelled Jira/GitHub fixtures, live progress/SSE | Sprint 08 report and jobs contract; real provider authentication and deployed webhooks remain unverified |
| Planned | Retrieval, AI gateway/agents, predictive models/copilot and cloud release | Roadmap and decision records; no complete current user flow |
| Not established | Production readiness, real-world throughput, full accessibility/security certification, off-host recovery | Existing local/CI checks do not prove these outcomes |

Implementation means a connected code path exists and has the recorded acceptance described here. It does not mean every broad requirement or future sprint is complete.

## Practical limits you will encounter

The command snapshot bounds input to 200 projects, 100 assigned resources and 5,000 rows per loaded source kind. Selected date ranges are 1–366 days. Sprint 8.1 selectors now page/search on the server; snapshot input limits remain. A list or chart should not be treated as unlimited enterprise data.

Cooperating writes and snapshots serialize by organization. This favors straightforward cross-record checks, but can limit throughput. The small historical two-project/one-resource measurement is not a production performance guarantee.

Dashboard dates filter selected facts; they do not reconstruct all historical state. Source age can be stale even after reload. Missing inputs remain Unknown, and insufficient resource scope prevents whole-resource claims.

Evidence is plain text, manually released. File bytes and database metadata are not one atomic transaction; orphan cleanup/retention is not automated. App-role append-only history is not tamper-proof against the migration owner.

Current deployment settings target local/test/demo. Development Gmail SMTP account delivery is verified. No live cloud release, passkey rollout or scheduled business-report pipeline is established. Old source requirements or gallery illustrations should not be read as implemented features.

## Docker: running these components together

**What?** Docker packages a process and its dependencies in a container. Docker Compose starts related containers from one file. **Why here?** Web, API, PostgreSQL, Redis and the Linux worker need a consistent local environment. **Where?** `compose.yaml`, `infra/api.Dockerfile`, `infra/web.Dockerfile`, `compose.demo.yaml` and `compose.identity-test.yaml`.

**Real example:** Compose runs `postgres`, `redis`, `migrate`, `api`, `worker`, `web`, plus a profile-gated `test` service. The existing startup command is:

```powershell
docker compose up --build -d --wait
```

`up` starts the configured services; `--build` builds application images; `-d` runs them in the background; `--wait` waits for their health/start conditions. Use [local setup](../../07-setup-and-deployment/LOCAL-DEVELOPMENT.md) for prerequisites and [identity setup](../../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md) for activation. This rewrite does not rerun bootstrap or start a new stack.

**Internally:** PostgreSQL health precedes the migration service; successful migration and Redis health precede API startup; worker and web wait for API readiness. The worker and web are siblings, not a chain where web waits for a task result. Named volumes `postgres_data`, `redis_data` and `objects` preserve data/bytes across normal restarts.

Normal host ports are web 3000, API 8000, PostgreSQL 15432 and Redis 16379, bound to loopback. Inside containers, service names such as `api` and `postgres` refer to the Compose network. `API_ORIGIN=http://api:8000` belongs to the web server's proxy; it is not the browser's direct address.

**If something goes wrong:** wrong migration head, failed Redis or unavailable storage can make readiness fail. Inspect service status and the documented diagnostic routes. Removing volumes deletes persisted data; it is not a routine restart. Keep normal/demo/test environments and their origins separate.

Remember:

- Use the existing setup guides and ignored local settings; never paste secrets into learning notes.
- Containers provide the local runtime; volumes preserve its data.
- Migrations run as owner; ordinary requests run as the restricted app role.
- Test lifecycle resets belong only to the guarded disposable database.

## Tests and recorded evidence

Backend tests cover input, identity/session/CSRF, RLS, revisions/retries, delivery, capacity, assessment and command arithmetic. Playwright scenarios exercise real browser workflows, including targeted responsive/accessibility checks. The guarded backend runner checks migration lifecycle and drift; worker/persistence scripts test their specific round trips.

The old Sprint 07 records include 53 backend tests plus later focused command cases and separately recorded browser acceptance. A subsequent [CI correction record](../../04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md) supersedes old claims that hosted CI had not run: it records 55 local backend tests and successful hosted run **37754868462**, confirmed 9 October 2026. This guide relies on that repository evidence and does not claim to have independently queried the live hosted run.

CI runs on push/pull request through `.github/workflows/ci.yml`: locked dependency installation → static/contracts/source checks → isolated stack/backend/worker → browser/persistence → artifact upload/cleanup. It has no production deployment job. A past dependency audit does not establish current vulnerability status.

For checks actually run during this rewrite, see [documentation verification](../../10-reference/history/LEARNING-DOCUMENTATION-VERIFICATION.md). No application test pass is inferred from a file existing, and no normal database mutation is necessary to verify Markdown links and source references.

## Keeping the guide current

After a code change, follow its UI-to-database path and update the corresponding chapter. Keep the learning roadmap short. Preserve source specifications, technical contracts, dated evidence and detailed inventories as references.

Existing `docs/learning` generators encode older authored chapters. Do not rerun them over this guide without reviewing the output: old snapshots contain outdated commit/CI wording and dense explanations. Prefer editing the source-reviewed chapters and checking links. Regenerate detailed inventories only when needed and verify their results against the current source.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Current local setup includes migration 0008, a mail adapter and pilot controls. Development Gmail account delivery is verified; production delivery, current hosted CI and regenerated archived Word visual QA remain separate gates. Read CURRENT_STATUS for current scope and the original sprint reports for what was verified at each date. Legacy Word files/generators are retained and are not automatically the current canonical guide.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

Development Gmail SMTP is now verified for signup, existing-account Viewer acceptance and recovery. Infrastructure configuration remains an operator task; members use only website/email. Changing `.env` requires service recreation, not just restart, to load new environment values. Isolated tests retain local delivery. Follow [Gmail SMTP setup](../../07-setup-and-deployment/GMAIL-SMTP-SETUP.md) for exact keys and safe diagnostics; [the email report](../../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) does not certify production, other providers or every live lifecycle variant.
