# Explain the project in an interview

[Learning roadmap](../00-getting-started/README.md) · Next: [current status and limits](../08-deployment-and-operations/OPERATIONS_AND_LIMITS.md)

Use these notes after understanding the request flow and calculations. Default role: **backend engineering**. These scripts describe the project, not verified individual authorship. Replace statements about your contribution only with work you can substantiate.

## A 30-second introduction

“AI-PPM helps an organization manage project plans, spending, staffing and assessments. The current version has a Next.js frontend, FastAPI backend and PostgreSQL database. The backend checks live user permissions, saves changes with history and calculates explainable scores and dashboards. AI retrieval and agents are planned; the current calculations use fixed formulas.”

## A two-minute explanation

“The problem is that a reported project status may not match its underlying facts. AI-PPM stores project dates, budgets, spending, allocations and assessment answers so users can inspect those facts together.

When someone saves a project, a React form sends JSON through a Next.js proxy to FastAPI. FastAPI validates the data and checks a signed access cookie against a live database session and organization membership. The project code checks the user's role and portfolio grant, verifies referenced records, then uses SQLAlchemy Core to execute SQL through asyncpg.

PostgreSQL applies constraints and row policies. The project, audit history and retry receipt commit together before the success response is sent. The UI then reloads its list. An edit includes the loaded revision, so an old form cannot silently overwrite a newer save.

Capacity compares calendar hours with leave and allocations. Assessment scoring uses frozen questions, weights and independent human review. The command center combines schedule, financial and staffing risk with fixed weights; missing required inputs produce Unknown. Human-reported health remains separate.

The repository includes real database and browser tests, and records a successful hosted CI run after a transaction-order fix. That evidence supports the tested checkpoint, not production readiness. Durable business jobs, RAG, agents and cloud release are future work.”

## A detailed backend flow to practice

Open `RecordEditor.save`, `delivery.create`, `delivery.write`, `identity.principal` and `ppm_tables.py`. Explain [the eleven project-creation steps](../02-backend/REQUEST_LIFECYCLE.md) aloud. Pause at INSERT and explain why it is not committed yet. Then explain how `scope="function"` prevents a response being sent before commit and how a failed audit rolls back the project too.

For a follow-up, trace an edit: the form sends revision 4; one caller commits revision 5; another caller with 4 receives 412 and retains unsaved fields. Explain both the organization lock and expected revision predicate rather than saying “transactions make it safe.”

## Thirty useful questions with answers

1. **What does the application solve?** It brings project plans, spending, staffing and assessment facts together. Users can inspect why a displayed metric differs from a reported status. See `command.snapshot` and its source drawer.

2. **What is your role?** Backend engineering is the safe description. Explain the backend work you can demonstrate; broad Git checkpoints do not prove that you individually authored every feature.

3. **What does FastAPI do?** It maps HTTP requests to Python functions and handles parsing/dependencies/responses. Project-specific rules remain in functions such as `delivery.write`. See `main.create_app` and `delivery.detail`.

4. **What does Pydantic do?** It checks API data. `ProjectInput.dates` rejects invalid date relationships, while UUID/status fields restrict input values. It does not decide whether the portfolio is accessible.

5. **How do React and Next.js differ here?** React renders interactive components from state. Next.js supplies route pages and the API proxy. See `RecordEditor`, `projects/page.tsx` and `proxy`.

6. **Why use TypeScript/generated contracts?** They help catch frontend/backend shape disagreements during development. `createApiClient<paths>` uses types generated from backend OpenAPI. Types do not validate runtime JSON.

7. **Does this app use a controller/service/repository chain?** Its routes and domain helpers live in Python modules. `delivery.create` calls `write` and SQL directly through Core. There is no repository class to invent in the explanation.

8. **How does Python become a database query?** Core builds a statement; SQLAlchemy compiles it for PostgreSQL with bound parameters; asyncpg sends it; PostgreSQL applies rules and returns rows. See `delivery.get`.

9. **Is SQLAlchemy used like Hibernate?** Most domain paths use explicit Core statements and `AsyncConnection`, not a managed ORM Session. Changing a returned dictionary does not save it. `FoundationState` is the limited mapped-model example.

10. **What is a connection pool?** It reuses database connections across requests. `make_engine` configures five pooled and five overflow connections; transaction-local tenant settings clear before reuse.

11. **What makes a project create atomic?** Project, audit, receipt and any creator grant use the same transaction connection. All commit or roll back together. This does not include filesystem writes.

12. **Why was commit timing fixed?** A successful upload response could trigger a read before the transaction committed. `Auth` now has function scope, which ends the transaction before sending success. See `SPRINT-07-CI-FIX.md` and commit-order tests.

13. **How do you prevent a lost edit?** The UI sends `If-Match` with its revision. `write` checks current revision, and UPDATE includes the expected revision. Stale means 412; missing means 428.

14. **What prevents duplicate creates?** A scoped command key and payload fingerprint in `ppm_requests`. Same-command retries read the target after rechecking authority; conflicting reuse gives 409.

15. **Why lock the organization?** Participating writes and membership edits share cross-record rules. `delivery.lock` serializes them and rechecks authority after waiting. The tradeoff is reduced concurrency within an organization.

16. **How does login work?** `login` checks bcrypt credentials and verified membership, creates a live session/refresh hash, commits and sets cookies. Later requests verify the token and session again.

17. **Why keep sessions if JWTs are signed?** A signature proves the token was issued correctly; the live session enables revocation and organization-switch checks. See `principal`.

18. **What happens if refresh credentials are replayed?** `refresh` revokes the session and commits the revocation before returning denial. Raising inside the transaction too early would roll that security change back.

19. **How are authentication and authorization different?** `principal` identifies the user. `authorize`/`can_edit` check role and grants for the action. Assigned respondents/reviewers and private effort have additional rules.

20. **What does CSRF protection do here?** Middleware checks exact Origin and cookie/header token match. Protected write requests also check the session digest. It helps prevent another website submitting changes with browser cookies.

21. **How is another organization's data protected?** Session-derived organization scope, application checks, composite foreign keys and database row policies reinforce the boundary. `context` sets transaction-local values; queries use `ppm_app`.

22. **Why test RLS with the app role?** An owner query does not exercise the same restrictions. Cross-tenant and pooled-connection integration cases verify the runtime boundary, not only a Python filter.

23. **Why use composite foreign keys?** A referenced ID must belong to the correct organization and sometimes project/portfolio. A valid foreign-tenant ID alone must not satisfy the relationship.

24. **What does Alembic add?** Ordered changes for existing databases. A table declaration alone cannot upgrade stored structure. Add new migrations; preserve applied versions and test lifecycle only on the guarded test database.

25. **How is an assessment score calculated?** `compute_scores` normalizes numeric answers, calculates a question-weighted dimension average, then applies dimension weights. Text affects completion/coverage, not the numeric average. Use the 87.5 example.

26. **Why freeze framework versions?** New questions/weights must not silently change old results. Assignments reference a published snapshot, and completed comparisons require matching versions.

27. **How is dashboard health calculated?** `combined` uses 40% schedule, 35% finance and 25% capacity risk; health is 100 minus risk. Any missing component means Unknown. Risk points are not a failure probability.

28. **What do Redis and Celery currently do?** Redis holds login attempt counts and task broker/results. Celery runs `foundation.database_checkpoint`. Durable business jobs and account email use the implemented database outbox; a running worker alone does not establish an AI workflow.

29. **What AI can you demonstrate?** No running LLM/RAG/agent path in this checkpoint. I can demonstrate deterministic scoring and analytics, and explain the future integration boundaries. The roadmap is separate from current source.

30. **What are the main limitations and evidence?** Coarse locks, bounded selectors/snapshots, development Gmail delivery with recorded acceptance, narrow text evidence and no production deployment. Recorded CI passed after the commit-order fix. A documentation review, a past CI run and production certification are distinct claims.

For deeper answers, use [database relationships](../04-database/DATABASE_GUIDE.md), [permission code](../05-security/AUTHENTICATION_AND_AUTHORIZATION.md) and [formulas](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md). Do not memorize library names without following their actual calls.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Knowledge checks: Why is fixture connector success different from real-provider acceptance? Why must notification counts recheck target permission? Why does server pagination not remove command snapshot bounds? Why is SMTP acceptance different from inbox arrival? Why can the original 8.1 plan still be historical while local implementation is verified? Cite the owning functions/tests and current report; do not claim that a dirty tree has a hosted CI checkpoint or that deterministic scores are AI predictions.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

Explain the observed setup failure: STARTTLS passed, Gmail returned 535, private boolean comparisons found an incomplete App Password, and correcting/reloading it produced authentication 235. Distinguish SMTP acceptance from human-confirmed receipt in Inbox/Spam. Explain why invitation verification creates membership but sign-in creates a session, and why promoting a Viewer to PM still requires work grants. Read [account email and role access](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md) and its linked evidence before making claims.
