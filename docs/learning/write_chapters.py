"""Authored learning chapters for the inspected Sprint 07 workspace."""
from build_learning_docs import write, build_references, ROOT, DOCS

chapters = {
'00-project-overview': ('Project overview: learn the actual system', '''
The current AI-PPM is a locally implemented enterprise portfolio/project management system through Sprint 07. Its operational core combines identity, tenant-scoped delivery records, resource capacity, versioned maturity assessments and four deterministic dashboards. “AI” in the project name describes the wider roadmap; this checkpoint has no verified LLM, RAG, agent or predictive-model execution.

The business problem is that a reported Green project may conceal late milestones, incomplete financial records or overallocated people. This application stores the underlying facts and makes their scope, history and incompleteness visible. A dashboard number is useful only when a backend engineer can explain which authorized rows produced it.

```mermaid
flowchart TD
 U[User in browser] --> R[Next.js pages and React client components]
 R --> C[Identity transport and API clients]
 C --> P[Same-origin Next.js API proxy]
 P --> F[FastAPI middleware and routes]
 F --> A[Live identity and scoped authorization]
 A --> D[Domain functions and Pydantic contracts]
 D --> S[SQLAlchemy Core AsyncConnection]
 S --> DB[(PostgreSQL: facts, RLS, history)]
 F --> RED[(Redis: identity rate limiter)]
 W[Celery checkpoint worker] --> RED
 W --> DB
 D --> O[Local private evidence files]
```

Start with the [master guide](AI-PPM-MASTER-LEARNING-GUIDE.md), then follow one project create through [request lifecycle](04-request-lifecycle.md). Keep [API inventory](18-api-contracts.md) and [database dictionary](DATABASE-DICTIONARY.md) open alongside the narrative. Existing sprint reports, contracts and ADRs remain historical evidence; they are not silently rewritten to imply their old checkpoint is current. The two pre-existing Word handbooks in `docs/learning/` are preserved, but this source-reviewed Markdown set is the current learning entry point.

The backend is a modular monolith: routers and domain helpers live together in `services/api/ppm_api`, not separately deployed microservices. Next.js is a separate web process. PostgreSQL is the authority for identity and business facts. Redis is a shared rate-limit/broker/result service. The worker currently proves connectivity only. Private evidence bytes live in a filesystem volume while their metadata lives in PostgreSQL.

Your default contribution description is **Backend Engineering**. Say “Implemented in the project; individual ownership not verified” where ownership cannot be established. Two coarse Git commits do not establish who authored every feature. No claim that this chat built earlier sprints is required to explain their code accurately.

For learning, “implemented” means traceable source exists, not production certification. Historical acceptance records are labelled historical. This documentation task does not modify logic, schemas, dependencies, runtime configuration or user data.
'''),
'01-current-state': ('Current state and evidence boundaries', '''
**Latest completed local sprint: Sprint 07.** Four independent signals agree: `docs/handoffs/LATEST.md`, `docs/sprints/SPRINT-07-REPORT.md`, the six-file migration chain ending at `0006_command_center`, and Git `ef196c9` (“savepoint up to sprint 7”). `main.py.ready` explicitly expects that revision. Git also contains `f53d771`, the initial checkpoint through Sprint 05. There are not eight separate sprint commits.

The current source includes identity, delivery, capacity, assessments and command-center routes. Its API version still says `0.1.0` and the package description still mentions Sprint 01; neither is a reliable sprint detector. Likewise, the roadmap introduction still says only Sprint 00 is complete. Use source plus latest handoff, not those stale strings.

| Evidence level | What can be concluded |
|---|---|
| Current source and frozen migrations | Implemented structure, algorithms, guards and expected schema |
| Current tests | Intended checks and regression boundaries |
| Sprint 07 accepted transcripts | Prior local execution passed within recorded limits |
| This documentation verification | Source-derived inventory, contract equality and documentation integrity; see verification report |
| Production/cloud/hosted CI | Not verified from this workspace |

Historical acceptance reports 53 backend tests, followed by four command tests after the final coverage-display adjustment. Seven pre-existing browser scenarios passed in one invocation and the repaired command scenario passed separately. These are not described as a new all-green combined run. Earlier failing transcripts remain preserved.

No Sprint 08 durable job/outbox/SSE implementation was found. No AI provider calls, vector ingestion, embeddings, retrievers, LangChain agents or model serving were found in application source. Infrastructure can support future work without implementing that work.

Known local boundaries include first-100 selectors; 200-project/100-resource/5,000-source-row snapshot bounds; organization-serialized writes; no historical dashboard reconstruction; local-only challenge delivery; narrow plain-text evidence; and no automated orphan retention. Team metrics suppress small cohorts and scoped capacity refuses whole-resource claims.

Status vocabulary is exclusive per feature: IMPLEMENTED, PARTIALLY IMPLEMENTED, PLANNED, DOCUMENTATION ONLY, NOT VERIFIED. A planned item is labelled **Planned — not verified as implemented in the current workspace.** A proposed improvement in a learning exercise is not an implemented feature. See [feature matrix](26-feature-status.md).
'''),
'03-system-architecture': ('System architecture and every boundary', '''
The important architectural boundary is between a browser-controlled proposal and server-controlled authority. A project body may propose a portfolio and dates; it cannot choose the authenticated tenant, actor, revision increment or database role.

| Arrow | Data and format | Actual handler | Why it exists / effect of removal |
|---|---|---|---|
| User → React | DOM events and form values | `RecordEditor.save`, `IdentityClient`, `Assessments`, `CommandCenter` | Converts interaction to explicit commands; removal leaves no interactive workflow |
| React → client | Typed JS object, paths, query and headers | `packages/contracts/src/client.ts:createApiClient`; local assessment/command API wrappers | Central transport plus compile-time contracts; removal invites inconsistent headers/types |
| Client → browser HTTP | JSON body, cookies, CSRF and tenant preconditions | `identity-client.tsx:transport` | Coalesces refresh and injects context; removal breaks protected requests |
| HTTP → Next proxy | Same-origin `/api/v1/...` request | `app/api/v1/[...path]/route.ts:proxy` | Keeps browser endpoint same-origin and upstream fixed; direct calls would need a redesigned origin/cookie contract |
| Proxy → FastAPI | HTTP to `API_ORIGIN`, allowlisted headers, bounded text body | `proxy`, `main.py:create_app` | API process owns persistence; proxy imposes timeout and forwards Set-Cookie |
| Middleware → route | Request with UUID request ID | `main.py:request_context` | Unsafe-origin/CSRF check and safe error/log boundary; bypass removes those controls |
| Route → dependencies | Parsed parameters plus request | `identity.py:principal`, `Auth` | Produces live principal and transaction connection; JWT alone would lose immediate revocation |
| Dependency → PostgreSQL context | Parameter-bound SQL setting UUID/role strings | `identity.py:context` | Installs transaction-local RLS identity; absent settings deny tenant rows |
| Validated body → business logic | Pydantic model and Principal | `delivery.write`, assessment handlers, capacity helpers | Enforces scope, transitions, references and revisions beyond data types |
| Business logic → SQLAlchemy | Core expressions and bound values | `p.conn.execute`, `select`, `insert`, `update` | Builds parameterized SQL; removal requires equivalent SQL/driver handling |
| Driver → PostgreSQL | SQL plus typed parameters over asyncpg | `database.make_engine` | Applies constraints, policies and transaction effects |
| Rows → response | Row mappings → dict/Pydantic → JSON | `delivery.view`, response models | Hides non-contract columns and validates response shape |
| JSON → UI | Typed data, local React state | `onSaved`, loaders, `setSnapshot`, rerender | Refreshes visible truth; no automatic frontend database binding exists |

Dependency resolution and body parsing are framework steps, not a promise that every operation follows the exact linear order of an illustrative stack. Application middleware runs outside route handling; dependencies and validation must succeed before the endpoint body executes. Database work can occur inside dependencies.

The background path is separate: `scripts/smoke_worker.py` sends `foundation.database_checkpoint` via Celery → Redis `foundation` queue → Linux worker → fresh async engine → checkpoint SELECT → JSON result backend. No user-facing project write queues this task. Evidence upload is a synchronous API operation using a threadpool for filesystem IO, not a Celery job.

No implemented AI arrow belongs in this diagram. A later retrieval/provider/agent chain is a proposal in [AI architecture](21-ai-architecture.md). The current score calculation must remain explainable without an external model.
'''),
'04-request-lifecycle': ('Six complete request lifecycles', '''
Read these traces with `services/api/ppm_api` and `apps/web` open. All URLs below are real current routes. The [API inventory](18-api-contracts.md) links handler definitions and contracts; the [database dictionary](DATABASE-DICTIONARY.md) expands every referenced table.

## A. Login: credentials become a live session

1. `/login` selects `IdentityClient` login mode. The form prevents the browser's native submit; its handler gathers email/password and invokes the typed POST to `/api/v1/auth/login` through `action`, which sets busy/error state.
2. `transport` first obtains `/api/v1/auth/csrf` if needed. The API returns a random readable CSRF cookie/token. The transport puts it in `x-csrf-token`. Cookies travel with same-origin requests; access/refresh JWT secrets are not put in React state or localStorage.
3. Next `proxy` forwards the JSON, cookie, Origin and CSRF headers to its fixed API origin. FastAPI `request_context` requires exact configured Origin and matching CSRF cookie/header for this POST before the route runs.
4. `Credentials` validates input. `identity.login` lowercases email and calls `limited` for email and network-peer buckets. Redis atomically increments and sets a 600-second expiry. Unavailable limiter yields 503; excess yields 429.
5. `engine.begin()` opens a transaction. `SELECT identity_users ... WHERE email=:email FOR UPDATE` locks a matching identity. `password_matches` calls bcrypt in a thread; nonexistent identities use a dummy hash. Missing/incorrect/unverified accounts fail without exposing which condition applied.
6. `context(conn,user)` enables membership lookup. Login selects the first active organization ordered by UUID; it does not accept an arbitrary organization from the form. No active membership means denial.
7. It sets tenant context, inserts `identity_sessions` with seven-day expiry and CSRF digest, inserts a SHA256 hash of a random refresh credential, appends `session.login` audit and builds `AccountView` via `account`.
8. The transaction completes before login issues cookies. `access_cookie` signs HS256 claims with ten-minute expiry, user/session/org/issuer/audience/JTI. `cookie` sets Secure/HttpOnly/SameSite Strict for access and refresh. The response contains safe account data.
9. Proxy forwards individual Set-Cookie headers. The login UI follows its success path; protected loading calls `/auth/me` and stores the active organization. React rerenders the authenticated workspace.

On a future expired access request, `transport` coalesces refresh within that page, then retries a cloned request. Refresh rotates the stored token hash under session lock. Reusing an already consumed refresh revokes the session and commits that fact before returning 401. Across tabs there is no grace window.

## B. Create project: form → atomic facts/history/receipt

Prerequisites are an activated user, organization settings and an accessible portfolio. `RecordEditor` has local `values`, `busy`, `error` and one stable UUID `command` per editor instance. `save` builds a `ProjectInput` body with `kind: projects`; UUID references and date strings are submitted as JSON. It calls `client.POST('/api/v1/delivery/{kind}', ...)` with the command UUID as `Idempotency-Key`.

The common transport adds CSRF and `X-Organization-ID`. The proxy forwards these. Middleware validates unsafe request origin/CSRF. FastAPI parses the path Kind, UUID header and discriminated Input. `principal` validates the JWT and live session/membership, checks session-bound CSRF, opens the transaction and yields the connection plus identity. `ProjectInput.dates` rejects reversed dates or completed status without actual finish. Unknown extra fields such as a forged tenant fail validation.

`delivery.create` calls `lock`: compare organization header with session tenant, acquire `pg_advisory_xact_lock(hashtextextended(:org,2))`, recheck live membership/session after waiting, and reset RLS context to the live role. It fingerprints canonical payload JSON and looks for a receipt scoped to organization/user/key. A different payload/kind with the same key returns 409. An identical retry retrieves the target and rechecks current mutation authority; it does not blindly trust an old response.

For a new command, `write` verifies payload kind and authorization. Admin may create; a PM needs a portfolio manage grant. It requires organization settings, checks active referenced records and the program/portfolio relationship, and adds server-owned creator/UUID/tenant/revision 1/timestamps. SQLAlchemy executes an INSERT RETURNING on `ppm_projects`. PostgreSQL checks tenant RLS, composite references, allowed status and dates. For a PM-created project the same transaction adds the creator's manage grant.

`audit_change` inserts before=null and after=current row into `ppm_audit`, including actor and request ID. `create` adds `ppm_requests` fingerprint/target receipt. The yielding dependency owns transaction completion; failure unwinds the transaction. No caller separately commits project then audit. Response `RecordView` contains server fields and typed `data`; `view` explicitly omits internal fields from that data. `RecordEditor` calls `onSaved` and `onClose`; `Delivery` increments refresh and reloads scoped lists/summary. The displayed record is server-returned truth.

Approximate SQL (parameter syntax varies by driver):

```sql
INSERT INTO ppm_projects (id, organization_id, name, portfolio_id, revision, ...)
VALUES (:id, :tenant, :name, :portfolio, 1, ...) RETURNING *;
INSERT INTO ppm_audit (...) VALUES (...);
INSERT INTO ppm_requests (...) VALUES (...);
```

The three writes are atomic database effects. No external LLM, Redis cache write or background worker participates in project creation.

## C. Read project: identity + tenant + project visibility

`Delivery` loads detail/summary using GET `/api/v1/delivery/projects/{id_}` and/or `/project-summary/{id_}`. `principal` obtains tenant from signed claims verified against live session, not from a browser query field. `detail` calls `get`, which executes `SELECT ppm_projects WHERE id=:id AND organization_id=:tenant`. PostgreSQL's `tenant_read` additionally checks Admin, direct project grant or portfolio grant. A hidden ID yields the same unavailable 404 as an absent record.

Rows are `RowMapping` values, not a Hibernate entity graph. `view` validates domain values through the Input adapter, and `RecordView` serializes JSON. Summary separately aggregates approved budget, all ledger entries including reversals, alignment, work counts and baselines. React loaders update state. There is no ORM lazy load, shared session cache or Redis record cache in this trace. The delivery summary deliberately has `computed_health=None`; command-center health comes from its dedicated snapshot.

## D. Update project: prevent a lost edit

`RecordEditor.save` sends the complete current `ProjectInput` to PATCH `/delivery/projects/{id_}`, with `If-Match: row.revision` and optional `X-Change-Reason`. PATCH here is a full validated domain payload, not a partial dictionary merge. The same identity, CSRF, organization lock and post-lock authority checks apply.

`write` retrieves current row, rejects missing revision with 428 and stale revision with 412, then checks grants and state transitions. Portfolio transfers require Admin; archived projects must be restored before editing; currency cannot change once budget/expenditure exists. Reopening completed/cancelled projects needs a reason and appends a new baseline through the same write path.

The UPDATE includes both ID and expected revision and increments revision. `RETURNING` must return a row or 412 follows. Before/after audit is inserted in the same transaction. With two revision-4 edits, the first becomes revision 5; the second acquires the lock afterward, sees 5 and fails 412. The UI retains unsaved values and asks for reload; there is no silent last-writer-wins overwrite for shared project records.

## E. Assessment: publish → answer → review → complete

`Assessments` creates an editable `FrameworkInput`. Publishing calls `publish_framework`: validate dimensions/question definitions and exact dimension weight sum 1, then freeze a version snapshot. Assignment binds to that version and distinct eligible respondent/reviewer, optionally department/team. This is JSONB framework structure, not separate dimension/question SQL tables.

The respondent changes local answers; the `save` callback uses PUT `/assessment/assessments/{assessment_id}/answers` with revision and an idempotency key. The mutation decorator acquires the organization lock, rechecks role/assignment, validates command fingerprint and records the response. `save_answers` accepts draft/returned only, rejects foreign/duplicate question IDs and invalid published rubric values, writes answers, clears old reviewer adjustments/results and appends answer history. The UI debounces saving and preserves dirty state on errors.

POST `.../submit` calls `finalize_check`: required answers must be present and every dimension computable. `compute_scores` normalizes boolean/rubric answers, excludes text from numeric scoring, calculates weighted dimension/overall values, and reports separate answer/evidence coverage. Submission stores results, submitted actor and incremented revision. It is deterministic arithmetic; no AI scoring exists.

Reviewer POST `.../review` starts, returns or completes. Only the assigned independent reviewer may act. Numeric overrides are 0–100 and require notes; they preserve raw answers. Completion refuses quarantined attachments and incomplete scores. Published versions and events have no app-role update/delete privileges. Completed results are tied to their original version; comparison in UI requires the same version. Results render dimension bars and tables; a radar chart or semantic maturity classification must not be inferred. See [assessment algorithm](15-assessment-engine.md).

## F. Command center: authorized sources → explainable metrics

`CommandCenter.refresh` clears the prior snapshot/evidence, builds start/end/portfolio query and loads `/command/snapshot` plus portfolios and saved views. A request counter prevents an older response replacing a newer filter result. GET snapshot still requires the matching organization header because it calls `delivery.lock` to coordinate source consistency.

`command.snapshot` reads organization timezone/policy, authorized projects and source facts under RLS. It bounds rows, obtains capacity for selected dates and the next 28 local days, and uses shared money/alignment helpers. Baseline/calendar supply working-day schedule variance; forecast cost supplies financial risk; complete full-resource capacity supplies staffing risk. Missing any required risk component means Unknown. Weighted risk is not a probability. Human-reported health remains separate, and an overdue critical milestone can expose a Green discrepancy even when composite health is unknown.

`CommandSnapshot` includes metric value, unit, source facts, coverage, source freshness and computation time. Frontend Executive/Delivery/Risk/Resource views consume the same snapshot and open a source evidence drawer. JSON export performs a fresh authorized fetch. Selected dates filter period facts; they do not reconstruct all database history at a past instant. [Command-center chapter](16-command-center.md) derives each calculation.
'''),
'05-frontend': ('Frontend architecture and state', '''
The Next.js App Router lives in `apps/web/app`, with route files for `/`, `/system`, `/login`, `/account`, `/organization`, `/portfolios`, `/projects`, `/projects/[id]`, `/resources`, `/assessments` and `/command-center`. `app/layout.tsx` provides the root layout/styles. Route wrappers choose modes of the client `IdentityClient`; interactive domain components use `"use client"`. A page wrapper is not itself a business service.

`IdentityClient` owns account/session loading, sign-in forms, organization switching and shared transport. The transport fetches CSRF once, supplies organization/CSRF headers, and performs one coalesced refresh/retry on eligible 401s. HttpOnly credentials stay in cookies. Generated `components` types describe account/member/session/domain responses. The fixed Next proxy avoids browser-controlled upstream destinations and forwards individual cookie headers correctly.

`components/delivery.tsx` exports `Delivery`, `RecordEditor`, `RelatedName` and `ChangeDetails`. `delivery-fields.ts` describes per-kind form fields. `RecordEditor.save` converts form values, preserves intended empty strings where specified, sends a full discriminated payload, uses a stable create key or current revision, and calls parent refresh on success. Failed saves retain values. `Reference` searches bounded candidates; relationship labels replace unreadable raw IDs. Lists, boards and timelines reflect fetched pages, not an unlimited client-side dataset.

`Capacity` reuses delivery CRUD for resource records and calls specialized capacity endpoints for calculation. `Assessments` has a local typed fetch wrapper over shared transport, debounced answer autosave and explicit dirty/conflict handling. `CommandCenter` similarly uses typed response shapes and a request sequence guard; export reads a newly authorized DTO. Not every component calls the `openapi-fetch` client for every request: generated types and actual transport are related but distinct mechanisms.

State is local React `useState`/effects/callbacks/refs. No installed Redux, Zustand or React Query authority should be invented. Errors and busy/loading/empty states are explicit. Shared `ui.tsx` and `shell.tsx` supply reusable tables, dialogs, drawers, skeletons and navigation; native dialog behavior and CSS handle accessibility and presentation. Tailwind/PostCSS and custom CSS tokens support themes and responsive layouts. Charts are native bars/tables; a design-gallery illustration is not production analytics.

Click → handler → state/payload → transport → proxy → API → response → state setter → React rerender is the useful learning chain. React never writes PostgreSQL. Hiding an edit button is only UX: backend authorization still decides. Removing the shared transport would require every component to independently implement session refresh and CSRF. Removing generated types would remove compile-time drift protection, not change database validation.

Evidence: `apps/web/components/*.tsx`, `app/account/identity-client.tsx`, `packages/contracts/src/client.ts`, `app/api/v1/[...path]/route.ts`, and all `tests/browser/*.spec.ts`. Historical Sprint 03 and 07 browser checks establish targeted keyboard/responsive behavior, not universal accessibility certification.
'''),
'06-fastapi-backend': ('FastAPI, dependencies and Pydantic internally', '''
`main.py:create_app` constructs FastAPI, defines the lifespan and handlers, and includes command/capacity/assessment/identity/delivery routers. Module imports register assessment and command tables in shared metadata. `app = create_app()` creates the ASGI application without running its lifespan; this is why contract export can inspect routes without a database login.

At ASGI startup the lifespan loads validated `Settings`, creates an async SQLAlchemy engine, a Redis client and `LocalObjectStore`, then yields. Shutdown closes Redis and disposes the engine. Startup does not call `metadata.create_all`; Compose runs the migration service first. Engine construction does not prove database connectivity. `/health/ready` actually probes checkpoint/revision, Redis ping and writable object storage concurrently with timeouts; `/health/live` remains a cheap process check.

Middleware assigns/validates a UUID correlation ID, checks Origin and double-submit CSRF on unsafe methods, calls the route pipeline, then supplies no-store and safety headers and structured timing logs. Unexpected exceptions are sanitized rather than logging driver credentials. `RequestValidationError` becomes a 422 envelope containing location/reason; `HTTPException` becomes an envelope, with fixed `DomainError` messages allowed through.

Routers organize URL prefixes, not a Java controller/service/repository hierarchy. `delivery.router` has `/api/v1/delivery`; specialized routes precede generic `/{kind}`. FastAPI matches method/path, resolves annotations, parses parameters and dependency graphs, then invokes an async endpoint. A `UUID` path parameter is not a string the endpoint must manually parse. `Query(ge=...,le=...)` enforces bounds. Body `Input` uses a kind discriminator. `response_model` validates/serializes the returned object; it is not merely a documentation annotation.

`Auth = Annotated[Principal, Depends(principal)]` tells FastAPI to resolve a reusable dependency. `principal` is an async generator: before yield it authenticates, opens an `engine.begin()` transaction and sets context; the yielded object contains user/session/role/connection; cleanup exits the transaction context. Successful completion commits, exceptions roll back. Do not imagine an `AsyncSession` dependency or an `@Transactional` annotation that is absent. FastAPI manages dependency lifetime; application code manages transaction semantics within it.

Conceptually, `detail(kind,id_,p)` is four steps: framework validates Kind/UUID, resolves Auth, `get` queries with tenant/ID, `view` validates data and the framework serializes `RecordView`. Business checks belong in helpers such as `authorize`, `refs` and `write`; FastAPI does not know a completed project requires a new baseline when reopened.

Pydantic schemas approximate DTOs: request JSON becomes validated Python values; output becomes JSON-safe contract data. Differences from a plain Java DTO include executable runtime validators, automatic schema production and parsing/coercion rules. Python type hints alone do not provide those guarantees. `ProjectInput.dates` validates chronology and actual finish; `Common.extra=forbid` rejects extra attributes; Decimal/UUID/date contracts avoid ad hoc strings in domain logic. Database constraints remain necessary because Pydantic cannot serialize concurrent writers or protect alternate SQL callers.

The order of framework parsing and dependency evaluation should not be oversimplified: the endpoint runs only after their successful resolution, but a dependency can already execute SQL while preparing the request. Response serialization does not substitute for authorization. Removing Pydantic means manually replacing validation, serialization and contract generation; removing FastAPI means replacing routing/ASGI/dependency/exception plumbing while the domain rules still need to exist.
'''),
'07-database': ('PostgreSQL and the actual relational model', '''
The complete [database dictionary](DATABASE-DICTIONARY.md) lists every application table, all columns/types, primary and foreign keys, constraints, indexes, creating migration, consumers and model source. It is generated from current Python metadata without connecting to a database. `alembic_version` is Alembic-managed and is additional to these application models.

Compose initializes `ppm_local`, `ppm_test` and `ppm_demo`. The normal application uses the public schema with the restricted `ppm_app` role; migrations use `ppm_owner`. PostgreSQL does not have one schema per tenant. Organization UUID columns, composite foreign keys and RLS implement shared-table multitenancy. Global identity control-plane tables deliberately differ from tenant-owned business tables.

```mermaid
erDiagram
 organizations ||--o{ memberships : contains
 identity_users ||--o{ memberships : joins
 memberships ||--o{ identity_sessions : authorizes
 organizations ||--o{ ppm_portfolios : owns
 ppm_portfolios ||--o{ ppm_programs : groups
 ppm_portfolios ||--o{ ppm_projects : contains
 ppm_projects ||--o{ ppm_work_items : plans
 ppm_projects ||--o{ ppm_baselines : freezes
 ppm_projects ||--o{ ppm_expenditures : records
 ppm_resources ||--o{ ppm_allocations : assigned
 ppm_projects ||--o{ ppm_allocations : staffed
 ppm_calendars ||--o{ ppm_availability : schedules
 ppm_frameworks ||--o{ ppm_framework_versions : publishes
 ppm_framework_versions ||--o{ ppm_assessments : governs
 ppm_assessments ||--o{ ppm_answers : captures
 ppm_assessments ||--o{ ppm_evidence_attachments : supports
```

This conceptual diagram omits optionality and composite key details; the dictionary is authoritative for those. There are no standalone dimensions/questions tables: framework definitions and published snapshots contain their IDs/structure in JSONB. Answers refer to a question ID validated against the frozen framework by application logic, not by a question-table FK.

Most delivery tables share UUID ID, organization ID, human name/description, positive revision, archive flag and timezone-aware created/updated timestamps. `table()` creates a tenant-ID unique constraint and organization index. `ref()` often uses `(organization_id, reference_id)`; project-scoped children can use `(organization_id, project_id, reference_id)`. A valid foreign record ID alone cannot join a project to another tenant or attach a work item to a sprint in the wrong project.

Money uses `Numeric(18,2)` and Python Decimal; weight/score precision is separately declared. Currency is explicit; totals group by currency without FX conversion. Date-only staffing windows use local calendar dates; audit timestamps represent instants. UUID identity is not chronological order, so UUID cursor lists are bounded traversals rather than time ordering.

Read the dictionary's ON DELETE declarations: default NO ACTION is not automatic cascade deletion. Public delivery deletion is archive/restore, with `archive_guard` checking active dependents. Historical baselines, spend, status, sprint closures and audit records are appended; app-role privileges omit destructive operations on immutable tables. A migration owner is still powerful: this is application-role immutability, not cryptographic tamper-proof storage.

Indexes support tenant access and unique invariants, but existence of an index is not a query performance measurement. Command snapshots issue multiple scoped queries and bound their input. No production query-plan or 100x-scale guarantee follows from the schema. PostgreSQL provides atomic transactions and concurrency control; application locks/preconditions encode domain-specific consistency.
'''),
'08-sqlalchemy': ('SQLAlchemy Core: the database path actually used', '''
The primary persistence path is **SQLAlchemy Core + AsyncEngine + AsyncConnection + asyncpg**. `database.Base` and `FoundationState` use declarative mapping, but identity/delivery/capacity/assessment/command code mostly declares `sa.Table` objects and executes expressions against connections. There is no repository interface, ORM Session dependency, persistence context or first-level entity cache in these request paths.

`make_engine` configures `postgresql+asyncpg`, `pool_pre_ping=True`, pool size 5, max overflow 5 and the dependency connection timeout. An engine manages dialect/driver/pool behavior; it is not one connection. `engine.begin()` checks out a connection and opens a transaction. `p.conn` is that request's transaction connection. Pool return permits reuse after transaction completion; `set_config(...,true)` tenant settings are transaction-local and clear at commit/rollback.

```text
delivery.get / write
  → select(Table) / insert().values() / update().where().returning()
  → PostgreSQL dialect compiles SQL + separate bound parameters
  → asyncpg driver executes on checked-out connection
  → PostgreSQL evaluates RLS, constraints, SQL and locks
  → result rows
  → .mappings().first()/one()/all(), .scalar(), .scalars()
  → delivery.view / explicit dictionaries
  → Pydantic response model → JSON
```

For example, `get` selects one table with ID and tenant predicates; `summary` executes `sum(amount)` over approved budget rows. Approximate SQL is `SELECT coalesce(sum(amount),0) FROM ppm_budget_lines WHERE project_id=:pid AND NOT archived AND approved`. PostgreSQL additionally applies the table's RLS policy. Values are bound, not concatenated into SQL strings. The chosen table comes from an allowlisted Kind/TABLES mapping; parameter binding cannot itself make arbitrary identifiers safe.

`write` uses `INSERT ... RETURNING table` to obtain inserted values directly. Update predicates include expected revision and `RETURNING` distinguishes a successful change from a lost race. `mappings()` exposes named columns; `scalar()` obtains a single aggregate/checkpoint; `scalars()` extracts a column sequence. These do not create managed ORM entities that flush later.

| Familiar Hibernate/SQLAlchemy concept | Actual use here |
|---|---|
| Engine / connection pool | `make_engine`, reused async connections |
| Connection / transaction | `principal` or explicit `engine.begin` blocks |
| ORM model | FoundationState is mapped; domain tables are Core metadata |
| Session / AsyncSession | Not used by inspected domain request paths |
| flush | No unit-of-work flush; Core execute sends DML immediately within transaction |
| refresh | No ORM refresh; RETURNING or a SELECT obtains values |
| commit / rollback | Context-manager exit; not every execute commits |
| lazy/eager loading | No ORM relationship loaders; joins and helper SELECTs are explicit |
| identity map / first-level cache | No Session identity map in this path |
| relationship | ForeignKeyConstraint in database metadata plus explicit queries |

Immediate execute is not immediate durability: another transaction does not necessarily see uncommitted changes. An exception after project INSERT but before receipt completion rolls back the database writes. No explicit isolation level is configured in `make_engine`; PostgreSQL normally defaults to READ COMMITTED, but this is not proof of a live server setting. The organization advisory lock coordinates participating requests; it is not equivalent to global SERIALIZABLE isolation.

The current command snapshot's many explicit queries are understandable but can become expensive. Optimize with measured bulk queries/projections later, preserving scoped filtering and missing-data semantics. Removing SQLAlchemy would require equivalent bound SQL, result handling, dialect integration and metadata/migration coordination; it would not remove the need for PostgreSQL constraints or RLS.

Interview exercise: explain why a Python dictionary edited after a SELECT does not automatically update a row. Answer: this code has no managed Session unit of work; it must execute an explicit UPDATE.
'''),
'09-alembic-migrations': ('Alembic and schema evolution', '''
Alembic is the ordered database-change mechanism; PostgreSQL executes the resulting DDL. Editing a Python table definition alone does not update an existing database. `services/api/migrations/env.py` imports current metadata for drift checking and requires `PPM_MIGRATION_DATABASE_URL`; it creates an async migration engine with NullPool, calls synchronous Alembic through `run_sync`, and disposes it.

| Revision | Parent | Sprint | Change |
|---|---|---|---|
| `0001_foundation` | none | 01 | Singleton installation checkpoint |
| `0002_identity` | 0001 | 02 | Seven identity/organization/membership tables and tenant policies |
| `0003_delivery` | 0002 | 04 | Delivery hierarchy, history, scoped grants and retry receipts |
| `0004_capacity` | 0003 | 05 | Eleven capacity resources, sensitive scope and audit policy refinement |
| `0005_assessment` | 0004 | 06 | Eight assessment/version/answer/evidence/access/history tables |
| `0006_command_center` | 0005 | 07 | Risks, benefits, metric plans/policies, saved views, sprint closures |

Sprint 00 has no migration; Sprint 03 changes the shell without a database change. The detailed dictionary links each table to its creating migration. Migrations preserve their own historical metadata rather than importing mutable future table shapes. The latest `target_metadata` is for comparison, not a replacement for old migration definitions.

Fresh local setup runs the one-shot Compose `migrate` service: PostgreSQL healthy → migration owner connects → Alembic reads `alembic_version` → runs each missing `upgrade()` in dependency order → records head → API can pass readiness. On an existing Sprint 06 database only 0006 should apply. `main.py.ready` checks exactly that head, so a stale or unexpectedly advanced schema can fail readiness.

Adding a future entity should be Model → reviewed new migration → owner executes upgrade → database structure → updated schemas/routes/contracts/tests. Autogeneration may propose table changes but must not be assumed to generate correct RLS, grants, immutable privileges or data backfill. Review all tenant and project composite constraints explicitly. Do not edit an already applied migration to make development history look cleaner.

`downgrade()` reverses structure and may remove data. `scripts/test_backend.py` explicitly refuses its lifecycle exercise outside environment `test` and database `ppm_test`. It performs upgrade, downgrade base, upgrade, repeated upgrade, drift check and pytest. Those destructive lifecycle commands are test-only; this documentation task does not execute them on normal/demo databases. For user data, a rollback strategy requires backup/restore or reviewed forward repair, not casually dropping new tables.

Evidence: migration source, `infra/postgres/init.sh`, Compose migration dependencies, `scripts/test_backend.py`, and accepted Sprint 07 backend transcript. `alembic check` compares metadata structure but is not sufficient evidence that every security policy is correct; app-role negative tests cover that boundary.
'''),
'10-authentication': ('Authentication and credential lifecycle', '''
`identity.py` is the implemented identity service. Authentication answers who is calling; its result is a live `Principal`, not simply a decoded token. Global `identity_users`, `identity_sessions`, refresh-token hashes and challenge hashes support narrow server-owned lookups. They are deliberately not tenant-RLS tables; tenant membership and audit are.

There is no anonymous register-an-Admin route. `scripts/bootstrap_identity.py` is an operator path for initial organization/pending Admin, and activation/invitation challenges complete account setup. `issue_challenge` creates random one-use secrets, stores only SHA256 hashes in PostgreSQL and writes the delivery link to a private local mailbox. Reset expires after 30 minutes; activation/invitation after 24 hours. This is local delivery, not verified SMTP/email integration.

New passwords need at least 12 characters and at most 72 UTF-8 bytes. bcrypt cost 12 runs in a thread to avoid blocking the event loop. Verification uses stored hash or dummy hash for unknown accounts. Password reset/activation consume applicable challenges and revoke existing sessions. Invitation acceptance rechecks the inviter is still an active Admin, verifies an existing account's password, and cannot silently restore an existing removed membership.

Access JWTs are HS256, ten minutes, issuer `enterprise-ppm`, audience `ppm-web`, required sub/sid/org/iat/exp/jti. The secret is a validated SecretStr of at least 32 bytes. A fixed seven-day database session supplies revocation, selected tenant and CSRF binding. Access/refresh cookies are Secure, HttpOnly, SameSite Strict and path `/`; CSRF is readable. The local browser origin must match configured origin. Neither token goes into localStorage.

Each protected request decodes claims, queries session by sid/user, checks expiry/revocation/org equality, resolves active membership and verified user, then establishes transaction-local identity. Role is re-read from membership, not trusted from a stale JWT claim. Logout revokes the session and expires cookies. Session revocation is user-scoped; membership removal revokes sessions for that organization. Personal profile-name changes are last-write-wins, unlike revision-controlled shared records.

Refresh stores random credentials as digests, locks the session row, marks the old token used and inserts a replacement. If the old token is reused, the entire session is revoked. Code commits revocation before raising denial; raising inside the transaction would otherwise undo the security response. Concurrent refresh losers can revoke the session, so the client coalesces refresh in-page. This is strict replay detection, not transparent cross-tab synchronization.

Evidence: `identity.login`, `principal`, `refresh`, `complete`, `logout`, `revoke`, `password_hash`, `password_matches`; `identity_schemas.py`; `0002_identity`; `identity-client.tsx`; `tests/test_identity.py` cookie, replay, reset, invitation and session tests. The detailed login trace is in chapter 04. Removing live session checks would delay revocation until token expiry and lose the selected-organization validation.
'''),
'11-authorization-multitenancy': ('Authorization, tenant isolation and RLS', '''
Authentication establishes identity. Authorization decides the permitted action. Tenant isolation limits the organization's data. Project scope and sensitive-resource scope further narrow the rows and fields inside that tenant. A valid JWT does not imply permission to edit every project.

`principal` resolves claims against a live session, active organization membership and verified user. It calls `context` with user/org/role. The browser's `X-Organization-ID` is a stale-tab precondition, not an authority source. A tenant switch updates the session and token; old tabs must reload instead of sending writes into a newly selected organization.

For delivery writes `lock` serializes by organization, then re-reads session and membership after waiting. Admin controls organization configuration and grants. PM project creation needs portfolio manage; project edits need direct edit/manage; archive/restore needs manage. Viewer has no business-write capability, with the explicit personal saved-view exception. Resource effort requires a separate capability even for Admin. Assessment respondent/reviewer rules are assignment-specific; Admin cannot impersonate the assigned respondent simply by having a higher role.

PostgreSQL policies in migrations use `NULLIF(current_setting('ppm.organization_id',true),'')::uuid`, corresponding user setting and role setting. `context` binds values with `set_config(..., true)`: true means transaction-local. A reused connection cannot retain this transaction's tenant settings after commit/rollback. Missing settings do not match tenant rows. This defense only works when queries run as restricted `ppm_app`, not owner/superuser/BYPASSRLS.

`0003_delivery.upgrade` installs `tenant_read`, `tenant_insert` and permitted `tenant_update` policies. SELECT `USING` determines visible rows; INSERT `WITH CHECK` validates proposed rows; UPDATE applies visibility/allowed-row conditions and checks resulting scope. Project reads allow Admin or applicable project/portfolio grants. Child tables depend on visible project; dependencies require visibility of both endpoints. Application-level ID/tenant predicates and database policies therefore reinforce each other.

Not all tables use RLS: global identity credential/session tables require pre-authentication lookup, while organizations/memberships/identity_audit are policy-controlled. The code inspected uses ENABLE RLS and a separate non-owner runtime role; it does not claim FORCE RLS on all tables or that an owner cannot bypass policies. RLS trusts the server-set context; arbitrary SQL execution with the ability to set session variables remains a serious trust-boundary failure. It is defense in depth, not protection against a fully compromised application credential.

Composite tenant/project FKs stop cross-scope relationships independently of route checks. App-role grants separately deny UPDATE/DELETE on immutable history. `tests/test_identity.py:test_rls_pool_reuse_foreign_writes_and_composite_fk` and delivery/capacity/assessment/command direct-SQL tests exercise missing context, pooled reuse, foreign writes and hidden rows. A read query returning zero rows cannot by itself prove a record does not exist; the API intentionally treats hidden and absent records alike.

If application filtering were the only control, one missing predicate in an aggregation could leak totals. If RLS were the only control, allowed rows could still undergo invalid status transitions or stale revisions. Both layers are necessary for this implementation. New endpoints, exports and future workers must reuse live scope rather than trust a stored result or saved view as an access grant.
'''),
'12-security': ('Security mechanisms and their limits', '''
Each row is an implemented mechanism, tied to a concrete threat. This is code analysis, not a penetration-test certification.

| Threat / example attack | Protection | Code | Why it helps / boundary |
|---|---|---|---|
| Stolen password database | bcrypt cost 12, byte bounds | `identity.password_hash/password_matches` | Expensive salted verification; does not prevent weak/reused passwords |
| Forged/expired access cookie | Fixed HS256, issuer/audience/required claims | `principal` | Rejects invalid signatures/claims; live session adds revocation |
| Refresh credential replay | Hashed rotating tokens, locked session, revoke on replay | `refresh` | Replay cannot mint indefinitely; strict races can require re-login |
| Cross-site form submits mutation | Exact Origin, CSRF cookie/header, session digest | `request_context`, `principal` | Another origin cannot satisfy the normal browser request contract |
| Cross-tenant guessed UUID | Context RLS + scoped lookup + composite FK | migrations 0002–0006, `get` | Hidden reads and invalid foreign references blocked as app role |
| Viewer sends handcrafted PATCH | Live role/grants, post-lock recheck | `authorize`, `lock` | UI hiding is not relied upon |
| Brute-force login/reset | Atomic Redis fixed-window limiter | `limited` | Shared count/expiry and fail-closed 503; not a production edge policy |
| Duplicate create after timeout | Scoped key/fingerprint receipts | `create`, `mutation` | Same command does not duplicate database effect; auth rechecked |
| Stale browser overwrites new data | If-Match/revision predicate | `write`, `revision` | Returns 412/428; preserves newer state |
| Silent history/ledger rewriting | Append-only app privileges, reversals | migrations, `IMMUTABLE` | Application role cannot update/delete history; owner remains trusted |
| Path traversal through evidence key | Resolved root containment and generated keys | `LocalObjectStore._path`, `upload` | Rejects traversal; authorization still required before get |
| Active uploaded content | UTF-8 text/size/content bounds, quarantine/manual release | assessment upload/release/download | Narrow format and safe download; manual review is not antivirus |
| Credential exposure in error logs | Sanitized envelopes, fixed log fields, SecretStr | `main`, `config` | No raw driver exceptions/request bodies in normal logs |
| Proxy to attacker-supplied destination | Fixed API_ORIGIN, path segment allowlist | Next `proxy` | Browser cannot select arbitrary upstream; deployment config is trusted |

Unsafe request CSRF failures include request ID/no-store; normal responses add Referrer-Policy and nosniff. The proxy forwards selected response headers, so do not assume every API header automatically reaches the browser. No configured cross-origin CORS middleware is part of the current architecture; the same-origin proxy is the intended path.

Configuration uses `PPM_` environment names with secret values hidden from validation errors; bootstrap creates ignored local credentials. Git ignore is not a managed production secret store. Current settings allow local/test/demo only. Containers run application processes as non-root and bind published ports to loopback. Production TLS/IAM/rotation/backup operations are not established by these local controls.

Audit logs record business actions; application logs record request route/status/duration/request ID. A correlation ID is not authentication. RLS does not validate semantic content. SQL parameter binding does not replace authorization. Evidence SHA256 detects changed stored bytes, not truthfulness of the uploaded document. No cryptographic append-only audit chain, WAF, general anti-malware service or security certification is claimed.

Tests: `test_identity.py`, `test_delivery.py`, `test_capacity.py`, `test_assessment.py`, `test_command.py`, `test_config_storage.py` and safe-error tests in `test_api.py`. See [test inventory](CODE-AND-TEST-INDEX.md) for specific case names.
'''),
'13-delivery-module': ('PPM domain and delivery lifecycle', '''
Delivery is the authoritative system of record, not a projection owned by dashboards. `ppm_tables.py` defines shared table helpers and domain tables, `ppm_schemas.py` defines the discriminated payloads, and `delivery.py` owns reads/mutations/history/summary. `apps/web/components/delivery.tsx` and `delivery-fields.ts` expose those records through lists, project details, forms, work board and timeline.

| Entity group | Business purpose and relationships | Lifecycle / authority |
|---|---|---|
| Organization/User/Membership | Tenant, global identity, per-tenant role | Operator bootstrap, activation, membership revision/removal |
| Settings/Department/Team/Goal | Currency/timezone, organizational ownership and strategic objectives | Admin configuration; archive guarded |
| Portfolio/Program/Project | Investments → optional program → executable plan | Admin or scoped PM; project has reported health, dates and ledger completeness |
| Grants | Explicit project/portfolio scope | Admin manages; PM creator gets project manage grant |
| Sprint/Work item | Team timebox and individual delivery work | Planned→active→closed; backlog↔ready→in_progress→done with constrained reversals |
| Milestone/Blocker/Dependency | Gate, impediment, directed sequencing | Project edit; dependency graph acyclic; cross-project mutation Admin-only |
| Budget line/Expenditure | Approved plan and actual ledger | Decimal money, matching project currency, append-only exact reversals |
| Status update/Baseline | Human report and frozen plan evidence | Append-only; baseline version increments and requires reason |
| Alignment | Goal contribution weighted for project/portfolio | Complete only when active weights sum exactly 1 |
| Risk/Benefit/Metric plan | Risk register, outcomes, chosen calculation sources | Added in Sprint 07; same delivery mutation/audit infrastructure |

The [dictionary](DATABASE-DICTIONARY.md) provides model symbol, columns, migration and relationships for each entity. The [API inventory](18-api-contracts.md) maps every public kind to its schema and CRUD endpoints. Resource and assessment entities have their own chapters; no invented Repository or service class is needed to connect these pieces.

Projects transition draft→active/cancelled; active→on_hold/completed/cancelled; on_hold→active/cancelled; completed/cancelled→active with reason/new baseline. Completed input requires actual finish. Project currency becomes fixed once financial rows exist. Archiving preserves records, while archived parents cannot be casually referenced for new work. Reopening done work requires a reason. Closed sprint definitions cannot be edited; closure captures completed-point history.

`refs` verifies active membership owners, active referenced records, matching program/portfolio, matching child project and currency. `cycle_check` builds both node and project graphs and uses topological traversal: if visited count differs from node count, reject the cycle. Because scoped PMs may not see all edges, cross-project writes require Admin. This is a correctness response to incomplete graph visibility, not an AI scheduling algorithm.

Budget summary sums approved lines and all signed expenditure rows. `budget_usage` is unknown for zero budget/incomplete ledger. Reversal must exactly negate the original amount/currency, refer to the same project, and cannot reverse a reversal. A unique original reference prevents repeated reversal. There is no exchange-rate service or implicit conversion.

Baseline snapshot contains project, timezone/calendar metadata and active work/milestones/sprints/budget lines. It is historical evidence, not a replayable event-sourced system. Current facts remain mutable where allowed, and audit preserves before/after. `summary` counts work by status but leaves computed health empty; command-center rules add that capability later.

Evidence: migration `0003_delivery`, extensions 0004/0006, `tests/test_delivery.py`, `tests/browser/delivery.spec.ts`. Important regression examples include PM portfolio creation, concurrent revision rejection, dependency cycles, cross-tenant FK denial and immutable ledger updates.
'''),
'14-resource-capacity': ('Resource and capacity calculations', '''
Resources are independent workforce profiles; a resource need not be a login user and does not gain authority through staffing. Eleven capacity kinds are stored through delivery CRUD: resources, calendars, availability, resource_teams, resource_skills, time_off, allocations, resource_access, effort, effort_coverage and capacity_snapshots. `capacity.py` owns their authorization/validation and calculation; `Capacity` is the UI consumer.

The central algorithm is `calculate(start,end,sources,full,sensitive)`. Dates use `[start,end)` and are bounded to 1–366 days. For each local date it selects the effective availability period, looks up its immutable calendar, gets that weekday's Decimal nominal hours, and checks holiday membership. Recorded time-off subtracts hours; no separate leave-request/approval workflow is implemented. Missing calendar means unknown capacity, not zero. `TimeOffInput` forbids narrative medical reasons by requiring an empty description, and overtime is included within total recorded effort hours rather than added twice.

```text
available = max(0, (0 if holiday else nominal weekday hours) - leave hours)
allocated = sum(hours_per_day for active allocations on scheduled weekdays)
daily excess = max(0, allocated - available)  [full scope and known capacity only]
planned % = 100 × allocated / available     [full scope, nonzero capacity]
actual % = 100 × actual hours / available   [sensitive + full + complete coverage]
```

Planned hours remain counted on scheduled weekdays during leave/holidays, exposing conflicts. If no calendar exists, every date counts allocations conservatively while available stays unknown. A non-working weekday with nominal zero does not count allocation hours. Ratio rounds to two decimals; zero denominator returns null. Weekly periods align to Monday, clipped to the request range. Total excess sums positive daily overload, not max(0,total allocated−total available), because spare Tuesday capacity cannot cancel Monday overload.

Worked example grounded in `calculate`: five scheduled four-hour weekdays yield 20 available hours. Two three-hour-per-day project allocations yield 30 planned, 150%, and ten excess hours. Two full leave days reduce availability to 12 while allocations remain 30, giving 250% and 18 excess hours. These are planned hours, not clock-time duration; DST does not add/subtract a scheduled local-date hour.

`summary` grants full-resource interpretation only for Admin; a selected project slice is explicitly partial even for Admin. PM-visible projects do not establish total workload. Sensitive actual effort requires `resource_access.effort`, including for Admin; Viewer cannot access it. Actual utilization additionally needs a completeness attestation for every day. Any effort amendment invalidates affected complete coverage and audits the change, preventing stale utilization certainty.

Availability/reporting-team effective periods cannot overlap for a resource. Scope IDs cannot be moved by updating a row. PM allocation mutations need both resource manage and project edit. Calendars and capacity snapshots are immutable. Snapshots freeze non-sensitive sources and computed days, with contract `capacity-snapshot-v1`; they exclude actual effort and do not incorporate future source edits.

`team_summary` requires Admin and at least five resources on every selected date. Missing cohort dates, small cohorts or incomplete calendars suppress/qualify output. Sustained overload means consecutive full weeks with allocated > available, requiring at least two full weeks. Overtime warning requires complete effort and overtime > available/10. These are workload signals, not medical diagnoses, individual rankings or predictive AI.

Evidence: `capacity.calculate`, `summary`, `team_summary`, `authorize`, `validate`, `snapshot`; migration `0004_capacity`; `capacity_schemas.py`; `components/capacity.tsx`; `tests/test_capacity.py` and browser capacity workflow. The tests cover split work, leave, DST, zero/missing data, hidden scope, sensitive audit revocation, revisions and small-cohort suppression.
'''),
'15-assessment-engine': ('Assessment engine, scoring and evidence', '''
`assessment_tables.py` stores editable framework JSONB, immutable published snapshots, assignments, answers, events, private attachment metadata, access grants and idempotency responses. Framework dimensions and questions are nested typed definitions (`Dimension`, `Question`, `Level`), not relational rows. A version snapshot freezes names, weights, rubric levels and question UUIDs so later editing cannot silently change old scores.

Framework publication requires dimension weights to sum exactly 1 and each dimension to contain at least one numeric question. Rubric questions need at least two distinct levels; non-rubric questions cannot carry levels. Definition validation rejects repeated dimension/question IDs. Question weights are positive; dimension weights are >0 and ≤1. Examples are labelled editable seeds, not claims of an externally accredited standard.

`compute_scores(snapshot,answer_map,reviewer_adjustments)` loops through dimensions and questions. A valid answer is a nonblank text value, string `true`/`false`, or an explicitly published rubric level. Boolean normalizes to 1/0. Rubric level v normalizes to `(v-min)/(max-min)` using numeric level values, not ordinal position. A reviewer override replaces normalized numeric value with reviewer_score/100. Text participates in completion/coverage but never the numeric numerator or denominator.

For answered numeric questions, dimension score = `100 × Σ(question_weight × normalized) / Σ(answered_numeric_weight)`, quantized to four decimals. Overall = `Σ(dimension_weight × dimension_score)`, also four decimals. Any uncomputable dimension or invalid total dimension weight makes overall null. A missing required answer adds a note; draft scoring may show a provisional score despite such notes, but `finalize_check` blocks submission/completion. Optional missing numeric questions do not enter the answered denominator.

Example from `test_assessment.py:definition/test_weighting_unknown_and_coverage`: a boolean question has weight 3 and answer true (normalized 1); a rubric question has weight 1 and answer level 1 on levels 0–2 (normalized 0.5). The dimension is `100 × (3×1+1×0.5)/4 = 87.5`. A reviewer override of zero for the rubric answer makes `100 × (3×1+1×0)/4 = 75`. Answer coverage is 100%; evidence only on the boolean question means evidence coverage 50%. If only the rubric answer exists, provisional score is 50, answer coverage 25% and the missing required boolean produces a note that blocks submission. Do not invent a generic maturity-band threshold: the code exposes 0–100 scores and rubric labels, not an overall named maturity-level classifier.

Weighted answer coverage = answered weight across all valid questions / all question weight ×100, rounded to two decimals. Evidence coverage = number of questions with nonblank evidence narrative or released attachment / number of questions ×100. These denominators differ. Evidence is counted separately from numeric score and does not make a claim true. Required text can block completion even though it does not change the numeric score.

Workflow: draft/returned → submit → submitted → reviewer start → in_review → return or complete. The reviewer route also permits its coded actions from submitted; read exact checks rather than assuming every UI step is mandatory. Assignment requires distinct active eligible people. Only assigned respondent may answer/submit; only independent reviewer may review. Reviewer adjustments require notes and target unique valid numeric answers in that assessment. Returning preserves history; editing answers clears reviewer adjustments and stored results. Completed responses remain frozen against their published framework version.

Evidence upload accepts base64 UTF-8 `.txt`, 1–524288 bytes, up to 50 attachments. Body is bounded at 2 MiB; active markup/control bytes/test-malware signature are rejected. Generated tenant/assessment/UUID paths avoid user filenames as paths. Metadata stores SHA256 and released=false; independent reviewer previews and releases with a reason after submission. Downloads reauthorize, require release, verify digest and force plain-text attachment/nosniff. Manual quarantine is not antivirus. Removed draft metadata leaves bytes as inaccessible orphans; filesystem write and DB commit are not one atomic transaction.

The UI uses bars and accessible tables, same-version completed comparisons, autosave and explicit unsaved-state errors. It does not implement a radar chart or semantic AI evaluation. Access administration for scoped editor/results grants is API-only; result access does not grant raw answers/evidence. Evidence: all `assessment.py` handlers, schemas/tables, `0005_assessment`, `assessments.tsx`, `test_assessment.py`, and the independent-review browser scenario.
'''),
'16-command-center': ('Command center metric lineage', '''
One GET `/api/v1/command/snapshot` supplies Executive, Delivery, Risk and Resource views. `command.snapshot` uses `delivery.lock` for a consistent cooperating-reader/writer boundary and restricted-role RLS for source visibility. `CommandCenter` filters, renders and exports this shared `CommandSnapshot`. None of its health metrics is AI-generated.

| Metric | Source / query | Calculation and missing-data meaning | UI |
|---|---|---|---|
| Approved budget | nonarchived approved budget lines for visible projects | Sum Decimal amount, by currency | Executive/project money |
| Recorded spend | signed expenditures incl. reversals | Sum; labelled partial if ledger incomplete | Executive |
| Period spend | expenditure spent_on within [start,end) | Sum within requested period | Executive |
| Budget use | shared `budget_usage` | 100×spend/budget; null if zero budget or incomplete ledger | Executive |
| Alignment | active alignments | 100×Σ(weight×contribution), only weights totaling exactly 1 | Executive |
| Finish variance | selected baseline project target, actual/forecast finish, immutable calendar | Signed working dates in (target,finish]; positive is late | Delivery |
| Schedule risk | variance and baseline working duration | clamp(100×max(0,variance)/max(1,duration),0,100) | Risk |
| Financial risk | metric plan forecast_cost and approved budget | clamp(100×(forecast−budget)/budget,0,100); requires positive budget | Risk |
| Capacity risk | resources allocated in next 28 local days, full-resource capacity | clamp(100×Σdaily excess/Σavailable,0,100); sufficient scope/known capacity required | Risk/Resource |
| Composite risk | all three components | 0.40 schedule + 0.35 financial + 0.25 capacity; any missing → null | Risk |
| Evidence health | composite risk | 100−risk; higher is better | Executive |
| Health category | composite risk plus metric policy | Red if risk≥red, Amber if ≥amber, else Green; missing→Unknown | All project health views |
| Milestone variance | milestone's frozen due date and actual/current due | Calendar working-day difference; missing baseline/calendar→null | Delivery |
| Overdue critical gates | critical, no actual_date, due_date<today | Count and source facts | Delivery/discrepancy |
| Velocity | immutable sprint_closures for closed sprints in period | Completed points frozen at closure; incomplete/missing closure→unknown | Delivery |
| Benefits | records fully contained in selected interval | Show target/realized with unit, no prorating/unlike-unit total | Executive |
| Team workload | capacity.team_summary | Full scope, completeness and cohort suppression | Resource |

Defaults are amber=30, red=60, stale_days=7; Admin may change validated organization policy. Risk points are a deterministic heuristic, not probability of project failure. For the accepted fixture, five working days late over 21-day duration, financial component 10 and capacity 25 give `0.4×(500/21)+0.35×10+0.25×25 ≈19.27381`, health≈80.72619. Remove sufficient resource scope and combined risk becomes unknown rather than redistributing weights.

Reported health remains the human declaration. Discrepancy is true when computed category is worse than a known reported category, or reported Green has an overdue critical milestone. Therefore a visible discrepancy can exist with Unknown composite health. Risk register severity/likelihood fields do not themselves become the weighted schedule/financial/capacity calculation.

Portfolio health averages covered active/on_hold projects equally; coverage states how many eligible projects contributed. Alignment averages covered visible projects. Worst health is the minimum covered active-project health. Unknown projects remain unknown and excluded with explicit coverage; they are not assigned healthy zero-risk values. Money remains partitioned by currency.

Every metric carries value/unit/period/source/facts, source_updated_at, freshness, status and coverage. Freshness uses the oldest contributing source update, not snapshot computation time; reloading cannot make stale evidence fresh. Stable old baselines may therefore conservatively mark a metric stale. `compute_ms` measures service computation, not network/render time.

Limits: max 200 projects, 100 assigned resources and 5,000 rows per loaded source kind; selected date ranges 1–366 days. Date filters do not reconstruct past state. Pre-existing closed sprints without closure snapshots remain unknown; code does not invent history. Personal saved views store filters, not results or grants. JSON download fetches a newly authorized snapshot; no scheduled report or external sending exists.

Evidence: `command.py:workdays/combined/clamped/snapshot`, `metric_math.py`, `command_tables.py`, `command_schemas.py`, `0006_command_center`, `command-center.tsx`, and `test_command.py`. Historical local measurement was 48 statements/79.92ms for only two projects/one resource, not a throughput commitment.
'''),
'17-background-workers': ('Redis, Celery and current background scope', '''
Redis has two implemented responsibilities: identity rate-limit state and Celery broker/result storage. These are distinct from a PostgreSQL database cache. `identity.limited` uses a Lua increment/expiry operation and fails closed if Redis is unavailable. `main.ready` also reports Redis readiness.

`services/worker/ppm_worker/app.py` creates `celery_app` using the configured Redis URL as broker and result backend. JSON-only serialization, default queue `foundation`, UTC, track-started, 300-second result expiry, 30-second hard/20-second soft limits, prefetch multiplier 1 and broker startup reconnect are configured. Compose runs a Linux worker with concurrency 2 after API readiness.

The real task is `foundation.database_checkpoint`. `scripts/smoke_worker.py` dispatches it through Celery. The worker task runs an async coroutine through `asyncio.run`, creates its own engine inside that event loop, selects `FoundationState.instance_id`, raises if missing, returns `{instance_id,status:completed}`, then disposes the engine. This verifies producer/broker/worker/driver/database/result connectivity. It does not process project writes, assessments or dashboards.

Redis AOF and a named volume persist broker storage, but do not create an authoritative PostgreSQL job ledger. No application retry/backoff/dead-letter/lease/outbox/inbox/reconciliation mechanism is implemented for business jobs. The task has no configured application-level retry decorator and is read-only, so repeating it has no domain mutation effect. `broker_connection_retry_on_startup` is connection behavior, not business retry semantics.

If Redis is down, limited identity operations reject and readiness fails; a already-authenticated read that does not call the limiter is a different path. If the worker dies, the API code does not become a recovery engine. Do not promise exactly-once processing or recovery of arbitrary future external effects based on this smoke task. A result expires after five minutes; it is not durable audit history.

Status: checkpoint worker **IMPLEMENTED**; general durable background processing **PLANNED** — **Planned — not verified as implemented in the current workspace.** ADR 004 and roadmap Sprint 08 describe intended outbox/job/lease/idempotent-consumer/SSE design. Those must be implemented and crash-tested before later AI/reporting depends on them.
'''),
'19-transactions-concurrency': ('Transactions, concurrency and retry semantics', '''
`principal` owns one `engine.begin()` transaction for protected domain work. Core execute issues SQL inside it; success commits at context exit and exceptions roll back. Login/refresh/challenge paths own explicit begin blocks. Atomicity means a delivery record, its audit and create receipt persist together or not at all. It does not mean a filesystem write or external provider action rolls back with PostgreSQL.

Consistency comes from both application invariants and SQL constraints: legal lifecycle transitions, valid references, tenant/project composite keys, unique retry keys, positive revisions and immutable privileges. Isolation controls concurrent visibility. No custom transaction isolation is selected in the engine; do not claim SERIALIZABLE. Cooperating domain mutations use transaction advisory locks keyed by organization, shared with membership changes, so post-wait checks see updated authority.

Two project editors load revision 7. A locks the organization, verifies 7, updates with `WHERE id=:id AND revision=7`, writes revision 8 and audit, then completes. B waits, reads 8 and fails 412; no B audit or data update commits. Missing If-Match is 428. The UI retains B's unsaved fields but does not automatically merge. This combines optimistic browser preconditions with pessimistic organization serialization and a final guarded UPDATE.

Two final-Admin demotions use the same organization lock in `identity.admin`. Each rechecks membership count under the lock, so a later attempt to remove the final Admin returns 409. Authorization is re-read after waiting, avoiding a stale permission decision made before an Admin revoked the actor.

Two identical delivery creates with the same organization/user/key find one receipt. Canonical payload fingerprint and resource must match; conflicting reuse returns 409. Replay fetches the current record and reauthorizes. Assessment idempotency includes method, URL, exact request bytes and If-Match, and returns its stored JSON after access checks. Reordering JSON bytes can change the assessment fingerprint. These are deliberately different replay contracts.

Immutable financial corrections append exact reversals rather than overwriting past expenditure. Sprint closure writes the closed sprint and frozen completed points together; later work edits do not rewrite velocity. Effort amendments invalidate coverage in the same transaction. Project reopen can recursively append a baseline in the same connection/transaction.

Important exception: refresh replay commits revocation before returning denial. If denial were raised inside the begin block, rollback would erase the revocation. Another exception is evidence bytes: upload writes filesystem before database metadata; rollback can leave an orphan. `LocalObjectStore.put` atomically replaces a file, but that is not a distributed transaction.

The organization lock simplifies correctness but limits throughput and serializes snapshot reads with mutations. Direct owner SQL outside the protocol is not coordinated by that lock. Future finer-grained locking must preserve last-Admin, dependency-cycle, cross-project allocation and consistent-dashboard invariants and be tested for deadlocks/races. Do not remove locks merely because UPDATE has an optimistic predicate.
'''),
'20-auditability': ('Auditability, history and immutability', '''
Enterprise facts require explanations after the current record changes. `identity.record` appends actor/action/target/organization/request UUID/UTC timestamp in `identity_audit`. `delivery.audit_change` appends resource/target/project, actor, before/after JSON and request ID in `ppm_audit`. Assessment `event` records named lifecycle actions, notes and detail snapshots in `ppm_assessment_events`; mutation also appends identity audit for request correlation.

Application request logs are operational: route, method, status, duration, request ID. They are not business history and omit raw request bodies/credentials. Audit is not a substitute for logging an unavailable dependency. Request ID ties layers together but does not itself prove identity or timestamp integrity.

| Preserved object | What is frozen | How change works |
|---|---|---|
| Baseline | Project/work/milestone/sprint/budget snapshot + version | Append next version with reason |
| Expenditure | Signed original amount and reversal link | Exact negative reversal; no overwrite |
| Status update | Reported health narrative | Append later report; current project health also updated/audited |
| Capacity snapshot | Planning sources/daily values without sensitive effort | Append new snapshot |
| Calendar | Weekly schedule, timezone, holidays | Create another calendar/version record |
| Published framework | Definition/question/rubric snapshot | Publish new version; old assessments keep old version |
| Assessment event | Action, actor, reason/details | Append; no runtime update/delete privilege |
| Sprint closure | Completed-point snapshot | Not recomputed from mutable work items |

Database privileges deny runtime UPDATE/DELETE on protected histories. This is stronger than only disabling an edit button, but not tamper-proof against the migration owner. The code does not implement signed audit chains, event-sourcing replay of the entire system, general temporal tables or automatic retention policy.

Sensitive history must remain scoped after access changes. Capacity migration refines audit policy so old effort before/after values do not leak through a generic history endpoint after sensitive permission revocation. Assessment result-only access does not expose private answers/events/evidence. Delivery history is limited to latest 100 entries and must first resolve the target under current scope.

A simple CRUD delete would destroy why a budget or assessment changed. This design keeps records and reasons while allowing current views to evolve. To explain a disputed dashboard, inspect its facts and their timestamp/revision, chosen frozen baseline and current scope; do not claim you can reconstruct every past dashboard automatically.
'''),
'21-ai-architecture': ('AI architecture: implemented versus intended', '''
**No LLM/RAG/agent/embedding/model-serving path is verified in the current application.** Source modules, runtime dependencies, migrations, routers, worker tasks and frontend consumers implement deterministic PPM functionality. The product specification and ADRs describe much more than this checkpoint delivers.

| Category | Finding | Evidence and status |
|---|---|---|
| A. Actually implemented AI | None verified | No provider SDK/call/retriever/agent path found in services or web source |
| B. Infrastructure prepared | PostgreSQL, local object store, Redis/Celery checkpoint, typed API and snapshots | IMPLEMENTED general infrastructure, not an AI pipeline |
| C. Contracts/specifications | Evidence/model/tool governance, retrieval and workflow design | DOCUMENTATION ONLY as contracts; `docs/contracts/api-events.md`, ADR 005 |
| D. Planned capabilities | Gateway, embeddings/RAG, semantic assessment, agents, copilot, ML | PLANNED in roadmap 09–14 and later |

For LangChain, provider adapters, embeddings, pgvector/vector stores, retrievers, agents, semantic assessment, PMO assistant, root-cause intelligence, recommendations and ML analytics: **Planned — not verified as implemented in the current workspace.** There is no current input/output/function to trace for those features. Proposed providers/models are alternatives, not configured integrations. PostgreSQL presence does not imply pgvector extension or embeddings exist. Celery presence does not imply agent orchestration exists.

Current assessment input is published rubric + raw answer + optional human override; output is Decimal score/coverage. Command-center input is authorized schedule/financial/capacity facts; output is deterministic risk points and health. Team workload input is hours/cohort/coverage; output is threshold signals. None calls an LLM. Removing a hypothetical model provider would not change those current paths.

The following is a proposed extension, not current architecture: authorized request → persisted job/outbox → worker live-scope check → provider gateway → tenant-filtered retrieval over versioned documents → bounded evidence context → structured model output → schema/citation validation → reviewable response. An agent should use typed allowlisted read tools and propose changes through existing version-safe commands, not bypass them with SQL. Prompt text is untrusted data, never permission.

Before implementing that path, Sprint 08 durable jobs must establish retries/crash recovery; document ingestion needs retention/deletion/access propagation; provider choices need measurable quality/cost/privacy evidence; semantic assessment needs evaluation against human-scored examples. Future predicted risk probabilities require labels/calibration and must remain distinct from current rule risk points.

Interview wording: “Through Sprint 07, I can explain the backend system of record and deterministic analytics. RAG and agents are roadmap work; I would integrate them behind the existing authorization, job and versioned-evidence boundaries.” This is stronger and more accurate than claiming a framework dependency or architectural diagram proves a running AI feature.
'''),
'22-testing': ('Testing: what evidence proves', '''
The [code and test index](CODE-AND-TEST-INDEX.md) lists every backend test by actual symbol and source line. Tests are evidence only for their assertions and execution environment. Historical accepted logs are in `docs/verification/`; current documentation verification is separate in `LEARNING-DOCUMENTATION-VERIFICATION.md`.

| Test group | Actual sources | What it proves / bug caught |
|---|---|---|
| API/unit | `test_api.py` | Liveness independence, safe envelopes/correlation and no secret echo; catches raw-error leakage |
| Config/storage | `test_config_storage.py` | Required names, disallowed production env, byte persistence/path boundaries; catches unsafe keys |
| Real database | `test_integration.py` | Actual readiness/checkpoint, committed write/read, app privilege limits; catches fixture-only success |
| Identity/security | `test_identity.py` | Live roles, cookies/CSRF, refresh replay, invitations/reset, last Admin, RLS pool reuse; catches stale authority/cross-tenant access |
| Delivery | `test_delivery.py` | Hierarchy, money/baselines, cycle checks, versions/retry, scoped summaries and FK/RLS; catches duplicate/lost/foreign writes |
| Capacity | `test_capacity.py` | Split allocation, leave/DST, unknown denominator, sensitive scope, cohort suppression; catches falsely precise utilization |
| Assessment | `test_assessment.py` | Weighted arithmetic, versions, review/evidence, duplicate IDs, self-review denial; catches changed historical score or evidence leak |
| Command | `test_command.py` | Rules/calendar, reconciliation, thresholds, source history/filtering, saved-view scope; catches fake healthy/mixed-currency data |
| Browser | seven files in `tests/browser` (foundation has two cases) | Real cookies and UI workflows, persistence, keyboard/layout/axe; catches transport/forms/state wiring |
| Migration lifecycle | `scripts/test_backend.py` | Guarded clean/repeated upgrade, downgrade/re-upgrade, drift; catches incompatible migration path |
| Contracts | `scripts/contracts.mjs --check` | Committed OpenAPI/types match export; catches unregenerated API types |
| Worker | `scripts/smoke_worker.py` | Real broker/process/database roundtrip; does not prove domain retry recovery |
| Restart | `scripts/check-persistence.mjs` | Checkpoint and object survive restart; not disaster recovery certification |
| Preservation | `scripts/check_sources.py` | Original seven source/prompt hashes intact |

Integration cases need isolated PostgreSQL/Redis and use the restricted app role for security boundaries. Running owner queries alone would not test RLS. The guarded backend runner may reset only `ppm_test`, never normal/demo data. Browser fixtures likewise use the isolated identity runner. A unit-only pytest run must not be described as all integration tests passing.

Sprint 07 historical acceptance: 53 backend tests followed by four affected command cases; seven older browser scenarios plus repaired command case in separate invocations; contracts/static/build/worker/persistence checks recorded. A random-answer test bug was repaired by selecting the intended question ID, not by changing scoring. Failed logs were retained rather than relabelled.

CI includes npm audit but no verified Python vulnerability audit, penetration test, cloud load test or complete accessibility certification. No ML accuracy tests exist because no ML inference is implemented. The repository's small local performance fixture is a baseline, not an SLO. This documentation-only change requires link/source/status checks rather than restarting or mutating user data.
'''),
'23-docker-infrastructure': ('Docker and local infrastructure', '''
`compose.yaml` defines postgres, redis, migrate, api, worker, web and profile-gated test. Named volumes are postgres_data, redis_data and objects. Service DNS names work inside the Compose network; browser loopback URLs are a different address space. PostgreSQL and Redis host ports default to 15432/16379, API 8000 and web 3000, all bound to 127.0.0.1.

Startup is a dependency graph: PostgreSQL and Redis healthchecks → migration after PostgreSQL healthy → API after successful migration and healthy Redis → worker and web after healthy API. Worker and web are siblings; web does not wait for worker completion. Database migration is not performed opportunistically by every API process.

PostgreSQL 18 and Redis 8 images are digest-pinned. `infra/postgres/init.sh` creates separate owner/app non-superuser/NOBYPASSRLS roles and local/test/demo databases, revokes public connection/create rights and grants appropriate access. The app runtime uses ppm_app; migrate uses owner credentials. Redis runs AOF with its named volume. The private object volume mounts at `/var/ppm/objects` in backend services.

`infra/api.Dockerfile` uses pinned Python 3.12 slim, installs pinned uv, performs frozen dependency sync, copies services/scripts/tests and runs as uid 10001. Its default command starts uvicorn with application-controlled access logging. The worker reuses this image with Celery command. This local image includes development/test dependencies; no minimal production-image claim follows.

`infra/web.Dockerfile` uses pinned Node 24, npm ci, copies workspace packages and builds Next.js, then runs as node with production mode. `API_ORIGIN=http://api:8000` is internal proxy configuration, not a browser-injected arbitrary target. Exact secrets remain environment references, never documentation literals.

Settings require `PPM_APP_ENV`, database/Redis URLs, storage root and JWT secret; web origin/cookie defaults are validated. `PPM_MIGRATION_DATABASE_URL` belongs only to migration/operator paths. `.env.example` defines placeholders and `scripts/bootstrap.py` creates/preserves ignored local settings. Follow existing `LOCAL-DEVELOPMENT.md` and `IDENTITY-DEVELOPMENT.md` for account setup; do not bootstrap new user data merely to read documentation.

The test profile points to `ppm_test`, Redis DB 1 and temporary objects, with no normal object volume. `compose.demo.yaml` and `compose.identity-test.yaml` define explicit alternate environments; do not mix their ports/origins/data with normal mode. `docker compose up --build -d --wait` is the documented local startup; destructive down-with-volumes is not routine troubleshooting.

Persistence/restart evidence proves named-volume survival, not off-host backup/restore or disaster recovery. No live AWS/ECS/Kubernetes/Terraform deployment is verified. The current implementation accepts local/test/demo settings; cloud architecture in ADR 006 is planned.
'''),
'24-ci-cd': ('CI pipeline and deployment boundary', '''
`.github/workflows/ci.yml` runs “Foundation checks” on push and pull_request with read-only contents permission. One Ubuntu job has a 25-minute timeout. It checks out, configures Node 24/Python 3.12, installs pinned uv, `uv sync --frozen` and `npm ci`.

Static phase runs Ruff lint/format, mypy over API/worker, pytest excluding integration, preserved-source hashes, generated contract drift, frontend lint/types/format and npm audit at high severity. These validate distinct properties: typing is not runtime authorization; formatting is not behavior; audit output changes over time and historical zero findings are not perpetual safety.

Runtime phase bootstraps isolated local settings, validates Compose, builds/starts the stack, runs the test profile backend migration/test runner, and runs the worker smoke command. Browser/persistence phase installs Chromium dependencies, runs `check-identity-browser.mjs` and `check-persistence.mjs`. `if: always()` uploads local/browser/test artifacts and stops the CI stack.

The actual pipeline includes local image builds and tests but no production deployment job, release promotion, cloud credential use, environment approval or infrastructure provisioning. This is CI preparation, not continuous production delivery. Hosted CI execution is **NOT VERIFIED** here; a workflow file and local equivalent runs do not establish a successful GitHub run.

When explaining this to an interviewer: “The repository defines repeatable gates for source integrity, contracts, code quality, real database security, browser behavior and persistence. The recorded acceptance is local. Deployment automation is future scope.” Evidence is the workflow source plus separate `docs/verification/SPRINT-07-CHECKS.md` links, not an invented green hosted badge.
'''),
'27-code-walkthroughs': ('Code walkthroughs and conceptual traps', '''
Use [symbol index](CODE-AND-TEST-INDEX.md) for exact current line locations. These walks identify who calls each function, its input, processing, persistence and consumer without dumping whole files.

| File / symbol | Caller → input | Processing / database | Output → consumer |
|---|---|---|---|
| `main.create_app` | uvicorn/import → optional Settings | Registers routers/middleware; lifespan resources | ASGI app → server |
| `identity.principal` | FastAPI Depends → cookies/request | Decode token, live session/membership, transaction-local context | Principal → protected handlers |
| `delivery.lock` | mutation or snapshot → Principal/request | Tenant precondition, advisory lock, recheck role/session | updated Principal context → domain operation |
| `delivery.write` | create/update → kind/input/id/version/reason | refs, authority, transitions, guarded DML, audit, derived history | RecordView-shaped dict → response |
| `delivery.view` | reads/writes → kind/row mapping | Reconstruct validated domain Input; omit internal columns | safe data envelope → Pydantic/frontend |
| `capacity.calculate` | summary/snapshot → dates/sources/scope | Pure daily Decimal/calendar calculation | daily dictionaries → totals/UI |
| `assessment.compute_scores` | scoring → frozen framework/answers/overrides | Pure weighted calculation with coverage/notes | overall/dimensions/notes → result workflow |
| `assessment.mutation` | decorated route → request/Principal | lock, live access, fingerprint/receipt, event audit | new or replayed result → FastAPI |
| `command.snapshot` | dashboard GET → dates/portfolio | scoped source loads, capacity, shared math, provenance | CommandSnapshot → four views/export |
| `RecordEditor.save` | submit → local field state | typed POST/PATCH with key/revision | success refresh or retained-error form |
| `LocalObjectStore.put` | upload → generated key/bytes | safe path, temporary file, atomic replacement | persisted bytes → authorized download |

Line-by-line conceptual example, `delivery.get`: choose table from allowlisted kind; build `select(t)`; add ID and session organization predicates; await execute on principal connection; convert result to named mapping; take first row; fail 404 if absent; optionally fail 409 if archived; return mapping. RLS executes inside the SELECT. There is no later “filter tenants in Python” stage.

Line-by-line `combined`: if any component is None return None; otherwise multiply Decimal schedule by .4, financial by .35 and staffing by .25 and add. That explicit missing-data branch is why unknown risk is not zero risk. A dashboard renderer must retain null and coverage rather than use JavaScript `value || 0` as an interpretation.

## Common misconceptions, corrected using this project

| Confusion | Correct distinction |
|---|---|
| FastAPI vs business logic | Framework dispatches; `write` enforces project reopen/baseline rule |
| Pydantic vs SQLAlchemy | ProjectInput validates API values; Table/expressions describe/query persistence |
| SQLAlchemy vs PostgreSQL | Python compiles statements; server stores/enforces/concurrently executes |
| Authentication vs authorization | principal identifies live user; can_edit determines mutation rights |
| Authorization vs RLS | Domain action checks vs database row visibility/write checks |
| JWT vs permissions | Signed identity is rechecked against current membership and grants |
| Redis vs Celery | Redis stores broker/limit state; Celery routes/executes registered tasks |
| Celery vs background task | Runtime machinery vs `database_checkpoint` function being executed |
| Alembic vs PostgreSQL | Ordered schema-change scripts vs database applying them |
| Next.js vs React | Routing/server proxy/build environment vs interactive component state/rendering |
| Contract vs generated TS | API source is executable Python contract; generated types are a compile-time projection |
| DB model vs API schema | Table has internal creator/snapshot fields; RecordView deliberately exposes contract data |
| Dashboard vs AI prediction | `combined` is fixed arithmetic, not learned inference |
| Deterministic vs AI scoring | `compute_scores` uses rubric numbers and human overrides, no semantic interpretation |
| Planned vs implemented AI | ADR 005 proposes; source has no provider pipeline |
| Transaction vs isolation | All-or-nothing group vs what concurrent transactions can observe |
| Audit vs log | Business before/after/actor vs request timing/status |
| Session vs connection | Identity session is a DB record; AsyncConnection executes SQL; ORM Session is absent |

Practice: find each symbol, identify one failure branch, and predict which database rows can persist after it. Then compare against the linked tests rather than memorizing library names.
'''),
'28-how-to-modify-project': ('How to extend this architecture', '''
These are teaching proposals; no application change is made by this documentation task. Begin with the existing module ownership, source contract and tests. Preserve applied migrations and old evidence. New work must retain live scope and truthful unknown states.

To add an endpoint: choose the owning router; create strict request/response Pydantic schemas; use `p: Auth` for protected scope; add domain helper logic rather than burying rules in React; use `p.conn` for atomic database work; recheck authority with `lock` for mutations; apply existing revision/idempotency contracts; return explicit DTOs; regenerate OpenAPI/types; add a consuming client component; test positive, hidden-tenant, stale-version and denied-role paths. GET dashboards requiring snapshot consistency should follow the existing lock/header pattern, not assume every GET is lock-free.

To add an entity: define Core table with tenant key, positive revision, timestamps and appropriate composite FKs; define strict input and view schemas; create a NEW additive Alembic revision containing frozen metadata, RLS and least privileges; add typed Kind only if generic delivery mutation is appropriate; implement authorization/reference/archive/lifecycle checks in the correct helper; update form fields/relationship labels; regenerate contracts; exercise fresh/prior migration and direct app-role SQL negatives on the isolated test database. If immutable, omit UPDATE/DELETE grants as well as rejecting route edits. Do not expose an internal snapshot table merely because it is registered in TABLES.

To add a metric: specify source rows, authorization, unit, period, denominator, unknown conditions and provenance first. Implement pure math where shareable (`metric_math.py`), then scoped source loading in `command.snapshot`. Use the same helper in any existing summary that displays the metric. Include source facts/freshness/coverage in DTO, add table/chart UI and export consistency, and test zero/missing data, mixed currencies, hidden projects and stale records. Do not call a threshold “AI”.

To add a task today: a small diagnostic may follow `database_checkpoint`, register the name and send JSON through the configured Celery app, create/dispose its own engine and test on a live Linux worker. For durable business work, first implement planned Sprint 08 job/outbox authority, lease/retry/dedup/reconciliation and live tenant checks. An API commit followed by `.delay()` can lose dispatch if the process fails between them; do not call that atomic. Persist job identity with domain change and dispatch from an outbox instead. That design remains proposed, not existing.

To add AI/RAG later: keep provider integration behind a gateway, define structured output and evidence contract, persist authorized versioned jobs, ingest documents with tenant/project metadata and deletion semantics, retrieve only within current scope, limit context/tools, validate results and citations, evaluate quality and abstention, and route proposed mutations through current commands/revisions. Do not let retrieved text or model output choose roles/tenant or execute arbitrary SQL. Distinguish provider success from correct answer and correct answer from permission to act.

Review checklist for any extension: Who calls it? Which tenant comes from the live session? Which role/grant authorizes it? What does RLS enforce? Which transaction owns its effects? What happens on retry/stale revision? Which historical fact must remain unchanged? Which frontend state shows partial failure? Which test demonstrates the dangerous negative case? These questions are more useful than mechanically creating a repository layer that the current project does not use.
'''),
'30-system-design': ('Senior system design: current and future', '''
Current functional requirements are authenticated multi-organization access, scoped delivery records, auditable financial/planning changes, workforce capacity, independent versioned assessments and source-reconcilable dashboards. Non-functional requirements evidenced in code include tenant separation, request validation, live revocation, immutable app-role history, bounded requests/queries and explicit missing-data semantics. No production availability/latency/recovery SLO is verified.

The modular monolith keeps related domain writes on one PostgreSQL connection. This makes project/audit/receipt atomicity and composite constraints straightforward. Separate web/API/worker processes establish deployable runtime boundaries without claiming independent microservices. PostgreSQL is canonical; Redis provides limiter/broker/result state; local files store evidence bytes. No record cache or derived vector/graph index is implemented.

Identity uses short JWT cookie plus stateful session and live membership; authorization includes organization role, project grants, resource sensitive capabilities and assessment assignments. RLS duplicates critical row boundaries at the database. Organization locks coordinate shared mutations and command snapshots. This favors explainability/correctness at local scale over parallel write throughput.

| Failure scenario | Current response | Remaining limitation |
|---|---|---|
| DB unavailable / wrong migration head | readiness not ready; safe errors | No verified HA/failover |
| Redis unavailable | readiness fails; identity limiter fails closed | No authoritative business-job recovery yet |
| Worker crashes | checkpoint cannot complete normally | No domain job lease/reconciliation |
| Token stolen then revoked | live session rejects future protected request | Browser/device compromise not solved by JWT alone |
| Role removed while waiting for write lock | post-lock membership/session check rejects | Direct privileged writers must follow separate controls |
| Duplicate POST | scoped receipt and fingerprint prevent duplicate effect | External side effects need their own protocol |
| Two editors update | 412/428 instead of silent overwrite | No automatic merge UI |
| Evidence filesystem write then DB failure | DB rolls back | Orphan bytes can remain; no distributed atomicity |
| Partial capacity visibility | unknown full-resource metrics | Less data deliberately means less certainty |
| Large snapshot | bounded rejection | Not scalable analytics execution yet |

Observed local query cost was 48 statements for a tiny fixture; this points toward batching before merely adding API replicas. More replicas add pools (up to 10 connections per engine here) and can increase database pressure while sharing the same organization lock. Redis health does not prove application throughput. Current request logs/IDs and readiness provide basic observability; distributed tracing/SLO dashboards are not verified.

At 10x scale (proposed): measure query plans and p95 latency with realistic tenant distributions; batch source reads and repeated resource summaries; add needed indexes based on plans; budget connections across API/worker replicas; implement durable jobs/outbox; move evidence to a versioned object backend with tested permissions/retention; establish backup/restore and migration rehearsal; improve structured operational metrics. Preserve source-age and authorization in any cached projection and invalidate on grants/membership changes.

At 100x scale (proposed): consider tenant-aware read projections or materialized summaries with explicit lag, partitioning where measured volume warrants, finer-grained locking with invariant-specific coordination, worker queues by workload, service separation only for independently scaled ownership boundaries, and provider/model governance if AI exists by then. Replica reads must not undermine immediate revocation or revision decisions. Cross-tenant analytics requires explicit policy, not removal of filters.

AI evolution is conditional: build durable jobs and scoped ingestion before provider orchestration; separate deterministic operational truth from model suggestions; attach versioned inputs/evidence/evaluations and preserve human approval for consequential mutations. Proposed cloud ECS/RDS/S3/managed Redis or Kubernetes alternatives in ADRs are not deployed today.

Senior-level tradeoff answer: “We chose explicit SQL and transaction-local scope for an explainable local MVP, accepted coarse organization serialization to protect several cross-record invariants, and retained missing-data states instead of inventing certainty. Scaling work should begin with measurements and preserve those semantics.” The rationale is supported by ADRs 010–013; deployment effectiveness remains unverified.
''')
}

EVIDENCE = {
 '04-request-lifecycle': ('delivery.py','create, write, get, view','ppm_projects; ppm_audit; ppm_requests','POST/GET/PATCH /api/v1/delivery/projects','apps/web/components/delivery.tsx:RecordEditor/Delivery','0003_delivery','tests/test_delivery.py'),
 '06-fastapi-backend': ('main.py','create_app, request_context, ready','foundation_state; alembic_version','/api/v1/health/ready','apps/web/app/system/page.tsx','0001_foundation through 0006_command_center','tests/test_api.py; tests/test_integration.py'),
 '08-sqlalchemy': ('database.py','make_engine; delivery.write; identity.principal','current Core tables in Base.metadata','delivery routes','packages/contracts/src/client.ts and apps/web/components/delivery.tsx','full 0001–0006 chain','tests/test_integration.py; tests/test_delivery.py'),
 '10-authentication': ('identity.py','login, principal, refresh, complete','identity_users; identity_sessions; identity_refresh_tokens; identity_challenges','/api/v1/auth/login; /auth/refresh under same prefix','apps/web/app/account/identity-client.tsx','0002_identity','tests/test_identity.py'),
 '11-authorization-multitenancy': ('identity.py','context, principal; delivery.authorize/lock','memberships; ppm_grants; resource/assessment access','protected /api/v1 routes','apps/web/app/account/identity-client.tsx','0002_identity–0006_command_center policies','tests/test_identity.py; tests/test_delivery.py; tests/test_capacity.py; tests/test_assessment.py; tests/test_command.py'),
 '12-security': ('main.py','request_context; identity.principal/limited','session, membership, audit and scoped domain tables','unsafe/protected /api/v1 routes','apps/web/app/api/v1/[...path]/route.ts','0002–0006 grants/policies','tests/test_api.py; tests/test_identity.py; tests/test_config_storage.py'),
 '13-delivery-module': ('delivery.py','write, refs, cycle_check, snapshot, summary','ppm_projects and delivery tables','/api/v1/delivery/{kind}','apps/web/components/delivery.tsx','0003_delivery; 0006 extensions','tests/test_delivery.py; tests/browser/delivery.spec.ts'),
 '14-resource-capacity': ('capacity.py','calculate, summary, team_summary, access','ppm_resources; ppm_calendars; ppm_availability; ppm_allocations; ppm_effort','/api/v1/capacity/resources/{rid}','apps/web/components/capacity.tsx','0004_capacity','tests/test_capacity.py; tests/browser/capacity.spec.ts'),
 '15-assessment-engine': ('assessment.py','compute_scores, save_answers, submit, review, upload, release_evidence','ppm_framework_versions; ppm_assessments; ppm_answers; ppm_evidence_attachments','/api/v1/assessment/assessments/{assessment_id}/submit','apps/web/components/assessments.tsx','0005_assessment','tests/test_assessment.py; tests/browser/assessment.spec.ts'),
 '16-command-center': ('command.py','snapshot, workdays, combined','ppm_metric_plans; ppm_metric_policies; ppm_sprint_closures plus source facts','/api/v1/command/snapshot','apps/web/components/command-center.tsx','0006_command_center','tests/test_command.py; tests/browser/command.spec.ts'),
 '19-transactions-concurrency': ('delivery.py','lock, write, create; assessment.mutation','ppm_projects; ppm_audit; ppm_requests; ppm_assessment_requests','POST/PATCH /api/v1/delivery/{kind}','apps/web/components/delivery.tsx:RecordEditor','0003–0006 constraints and receipts','tests/test_delivery.py; tests/test_identity.py; tests/test_assessment.py'),
 '20-auditability': ('delivery.py','audit_change, snapshot; identity.record; assessment.event','ppm_audit; identity_audit; ppm_assessment_events; baseline/closure snapshots','/api/v1/delivery/history/{kind}/{id_}','apps/web/components/delivery.tsx:ChangeDetails','0002–0006 immutable grants','tests/test_delivery.py; tests/test_capacity.py; tests/test_assessment.py; tests/test_command.py')
}

SNIPPETS = {
'08-sqlalchemy': '''
## Read actual expressions, not an imagined repository

This expression is used by `delivery.get` (surrounding await/result handling omitted):

```python
sa.select(t).where(
    t.c.id == id_, t.c.organization_id == p.session["organization_id"]
)
```

The important update fragment from `delivery.write` is:

```python
t.update()
.where(t.c.id == id_, t.c.revision == version)
.values(**d)
.returning(t)
```

The second snippet is a fluent expression fragment inside the actual `execute(...)` call, not a standalone Python program. `d` contains the server-incremented revision and update timestamp. SQLAlchemy binds those values; PostgreSQL checks the predicate and RLS. The code tests whether RETURNING supplied a row. There is no intermediate repository proxy and no later flush of tracked entities.
''',
'11-authorization-multitenancy': '''
## Exact context-setting SQL

`identity.context` binds user/org/role strings to this SQL:

```sql
SELECT set_config('ppm.user_id', :u, true),
       set_config('ppm.organization_id', :o, true),
       set_config('ppm.role', :r, true)
```

`true` scopes the settings to the transaction. Policy expressions use `current_setting(...,true)` where that second true means tolerate a missing setting; NULLIF turns an empty value into null before casting UUID. These are different function arguments with different meanings. Neither value comes straight from an unverified browser header.
'''
}

if __name__=='__main__':
    for name,(title,body) in chapters.items():
        body+=SNIPPETS.get(name,'')
        if name in EVIDENCE:
            file,fn,table,api,front,migration,tests=EVIDENCE[name]
            body+='\n\n## Evidence\n\n'+f'**Status:** IMPLEMENTED within the stated boundaries.\n\n**Implementation file:** [services/api/ppm_api/{file}](../services/api/ppm_api/{file}). **Important class/function:** `{fn}`. **Database table:** `{table}`. **API endpoint:** `{api}`. **Frontend component:** `{front}`. **Migration:** `{migration}` in `services/api/migrations/versions`. **Tests:** `{tests}`. **Verification:** current source inspection; historical local execution is linked in [feature evidence](26-feature-status.md) and [verification](LEARNING-DOCUMENTATION-VERIFICATION.md). This is not a new integration-test result.'
        write(name+'.md',title,body)
    print('Authored chapters:',len(chapters))
    print('References:',build_references())
