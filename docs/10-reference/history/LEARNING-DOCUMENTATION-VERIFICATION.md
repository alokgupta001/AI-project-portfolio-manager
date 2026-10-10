# Verification of the simple AI-PPM learning guide

Reviewed on **9 October 2026** against Git **`9056440`**. Start with [the roadmap](../../02-learning/00-getting-started/README.md).

## Why the earlier guide needed rewriting

The earlier 31-chapter set had useful source facts, formulas and inventories. Its learning entry repeatedly used the same abstract What/Why/Internal/Removal language. Request traces put many unrelated checks in a single paragraph. Readers had to recognize advanced terms before understanding one request. Several chapters also used the older `ef196c9` snapshot and said hosted CI was unverified, despite a later recorded successful run and transaction fix.

The rewrite starts with the problem and a complete project save. It separates form state, request handling, validation, permission, SQL and commit; uses small real excerpts; and derives scores with numbers. It keeps the database dictionary, API inventory, code/test index, source specifications, technical contracts, decision records, Word handbooks and dated sprint evidence. Thirty old chapter URLs now link to replacement topics, so existing links remain valid. There are fourteen primary learning chapters and thirty interview questions.

## Checks actually run for this rewrite

Command, from repository root:

```powershell
.venv/Scripts/python.exe -B docs/learning/verify_learning_docs.py
```

Observed result:

- PASS: fourteen primary chapters and thirty interview questions.
- PASS: 753 local links across 50 checked documents; code fences balanced.
- PASS: explicit source paths, key backend/frontend symbols and function-scope transaction boundary.
- PASS: importing current routes produces the committed OpenAPI contract, with 50 operations. App startup/lifespan was not run.
- PASS: database dictionary covers all 54 application tables in imported metadata; six migration files end at `0006_command_center`.
- PASS: tracked changes are documentation only, including README; seven preserved source/prompt hashes match the original manifest.

The checker is a documentation helper under `docs/learning`. It does not start services, open a database connection, apply migrations or run backend/browser/worker acceptance. Local link checks prove destinations exist; source-symbol checks are not a substitute for reviewing the explanation. The source review also compared the project insert/retry path, login/context checks, published-answer handling, scoring arithmetic, capacity and command formulas with their actual files.

## Coverage of the attached request

| Requested topic | Rewritten location |
| --- | --- |
| Existing-document diagnosis and simple learning order | This report; [00](../../02-learning/00-getting-started/README.md) |
| Business problem, users, current features and architecture | [01](../../02-learning/01-project-foundations/PROJECT_OVERVIEW.md) |
| Eleven-step implemented feature with response and UI update | [02](../../02-learning/02-backend/REQUEST_LIFECYCLE.md) |
| React, Next.js, TypeScript and actual transport | [03](../../02-learning/03-frontend/FRONTEND_GUIDE.md) |
| Python/FastAPI, Pydantic, SQLAlchemy, transactions and errors | [04](../../02-learning/02-backend/BACKEND_GUIDE.md) |
| PostgreSQL, key tables, relationships, constraints and Alembic | [05](../../02-learning/04-database/DATABASE_GUIDE.md); preserved dictionary |
| Login, authorization, organization access and real RLS | [06](../../02-learning/05-security/AUTHENTICATION_AND_AUTHORIZATION.md) |
| Delivery, financial history, resources, assessments, evidence, risks and dashboards | [07](../../02-learning/01-project-foundations/FEATURE_WORKFLOWS.md) |
| Question/dimension weights, coverage, score storage, capacity and health formulas | [08](../../02-learning/06-ai-and-analytics/SCORING_AND_DASHBOARDS.md) |
| Honest implemented/partial/infrastructure/planned AI; Redis/Celery | [09](../../02-learning/06-ai-and-analytics/AI_AND_JOBS.md) |
| Sprint objectives, prior state, changes, files, migrations, verification and learning | [10](../../02-learning/01-project-foundations/SPRINT_HISTORY.md) |
| Navigation, real walkthroughs, endpoint/table/field/metric/AI changes and testing | [11](../../02-learning/07-testing-and-debugging/DEVELOPER_GUIDE.md) |
| Interview scripts and 25–40 implementation-specific questions | [12](../../02-learning/01-project-foundations/INTERVIEW_PREPARATION.md): thirty questions |
| Complete/partial/planned boundaries, Docker, CI and verification limits | [13](../../02-learning/08-deployment-and-operations/OPERATIONS_AND_LIMITS.md) |

## Historical application evidence, not a new test run

[The Sprint 07 CI correction record](../../04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md) records the response-before-commit race, fix `14f1eea`, 55 local backend tests, migration lifecycle/drift, two transaction regression cases and isolated assessment browser acceptance. It also records successful hosted run 37754868462 confirmed on 9 October 2026. This rewrite uses that reliable recorded result; it does not claim independent live verification of GitHub or a fresh application test run.

Earlier sprint checks remain dated evidence. No AI inference, cloud production release, production-scale load test, off-host recovery exercise or comprehensive security/accessibility certification is asserted.

## Maintenance

Use the documentation checker above after editing the primary chapters. The older authored generators encode the previous guide; review their output before use and do not overwrite the rewritten chapters with that snapshot. `documentation-manifest.json` records hashes of the current top-level Markdown documents and this helper; it is a content snapshot, not application acceptance.
