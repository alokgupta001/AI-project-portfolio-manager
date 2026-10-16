# The backend: receiving requests and applying rules

[Learning roadmap](../00-getting-started/README.md) Â· Next: [database](../04-database/DATABASE_GUIDE.md)

## Python and FastAPI

**What?** Python runs the functions that check and process requests. FastAPI connects an HTTP method and URL to a Python function, parses input and returns a response.

**Why here?** The frontend needs reliable operations such as create project, save answers and calculate capacity. Those operations must run on the server with access to the database and the logged-in user's permissions.

**Where?** [`main.py:create_app`](../../../services/api/ppm_api/main.py) constructs the app and registers routers from `identity.py`, `delivery.py`, `capacity.py`, `assessment.py` and `command.py`.

**Real example**, from `delivery.py`:

```python
@router.get("/{kind}/{id_}", response_model=RecordView)
async def detail(kind: Kind, id_: UUID, p: Auth) -> dict:
    return view(kind, await get(p, kind, id_))
```

The decorator registers a GET route under the router's `/api/v1/delivery` prefix. `Kind` limits the record types; `UUID` requires a valid identifier. `p: Auth` asks FastAPI to prepare the authenticated request object. `get` queries the row; `view` creates public response data. `response_model=RecordView` checks and serializes the result shape.

**Internally:** the server passes a request to the app. Middleware runs around route handling. FastAPI resolves parameters and dependencies, then calls the endpoint when those steps succeed. `async` lets this code wait for database/network work without blocking the whole event loop; it does not make a query faster by itself.

**If something goes wrong:** `main.validation_error` turns invalid input into 422. `http_error` handles expected HTTP failures. `request_context` returns a safe 500 for unexpected failures and records method, route, status, duration and request ID, without logging raw credentials or database exceptions.

Remember:

- FastAPI supplies request handling and response contracts.
- `write`, `refs` and `authorize` define project rules.
- `async` allows efficient waiting; it does not replace permission checks or transactions.

## Pydantic: checking the data

**What?** Pydantic turns incoming data into validated Python values. Its schema classes are comparable to DTOs: objects that describe data crossing an API boundary.

**Why here?** The API must reject wrong dates, statuses and references before treating them as project data. It also needs documented response shapes.

**Where?** `ppm_schemas.py` holds delivery schemas; `identity_schemas.py`, `capacity_schemas.py`, `assessment_schemas.py` and `command_schemas.py` hold the other modules' shapes.

**Real excerpt**, from `ProjectInput`:

```python
portfolio_id: UUID
program_id: UUID | None = None
status: Literal["draft", "active", "on_hold", "completed", "cancelled"] = "draft"
```

`portfolio_id` is required and must parse as a UUID. `program_id` is optional, with null as the default. `status` accepts only the listed strings, and defaults to draft. `ProjectInput.dates` additionally checks date relationships. The common schema forbids extra fields.

**Internally:** FastAPI supplies the body to the schema and uses its validated values. `payload.model_dump()` produces a dictionary for the write logic. A Python type hint alone does not perform all of these checks. Pydantic cannot decide whether a portfolio is accessible; that requires live database queries in `refs` and `authorize`.

**If something goes wrong:** an invalid field gives 422. A valid portfolio UUID that points to an unavailable record is handled by project code. Database constraints still guard stored relationships if another SQL caller bypasses API validation.

Money and scoring use Python `Decimal`, which represents decimal values without ordinary binary floating-point approximations. The schemas constrain accepted precision; numeric database columns store the corresponding values. That helps keep money and weighted calculations consistent.

Remember:

- Validate the public shape at the API boundary.
- Check permissions and referenced rows against current database state.
- Keep database constraints too; a schema cannot protect every SQL caller.

## SQLAlchemy: turning Python expressions into SQL

**What?** SQLAlchemy helps Python describe tables and build database statements. Most AI-PPM domain code uses its Core API, which sends explicit statements on a connection.

**Why here?** Projects, memberships, answers and metrics need queries and updates. Core supplies parameter binding, result handling and shared table definitions.

**Where?** `database.make_engine` creates the connection machinery. Tables are in `identity_tables.py`, `ppm_tables.py`, `assessment_tables.py` and `command_tables.py`. Protected routes use `p.conn` from `identity.principal`.

**Real excerpt**, from `delivery.get`, inside its execute call:

```python
sa.select(t).where(
    t.c.id == id_, t.c.organization_id == p.session["organization_id"]
)
```

`select(t)` requests the table's columns. `t.c.id` means the table's ID column. The two conditions select the requested record and current session organization. `p.conn.execute` sends the statement; `.mappings().first()` reads the first row as named values.

**Internally:** SQLAlchemy's PostgreSQL support compiles SQL and bound parameters. The asyncpg driver sends them over the database connection. PostgreSQL applies row policies and executes the SQL. Returned rows become response data through `view` and Pydantic.

The engine manages a pool of reusable connections. `make_engine` sets five normal connections and up to five extra connections, with a pre-use connection check. It is not one permanently open connection per user. Identity sessions in the database are a different concept from SQL connections.

**If something goes wrong:** a broken reference or constraint can reject a statement. A transaction exception rolls back its database work. An engine being constructed does not prove PostgreSQL is reachable; readiness actually probes it.

Remember:

- Core sends SQL explicitly on the request connection.
- Changing a returned Python dictionary does not update a row.
- Executing INSERT does not commit by itself.

`FoundationState` uses an ORM mapping, but domain requests do not use an ORM Session, automatic dirty checking or lazy-loaded entity relationships. The equivalent of your JPA/Hibernate/JDBC chain here is **Core expression â†’ SQLAlchemy PostgreSQL support â†’ asyncpg â†’ PostgreSQL**.

## Transactions, conflicting edits and duplicate requests

A transaction groups database changes so they all commit or all roll back. `principal` opens one with `engine.begin()`, yields the same connection to the handler, and exits before the response because `Auth` uses `scope="function"`.

Project creation saves its row, audit and retry receipt together. If the audit insert fails, the project is rolled back too. A filesystem write is outside this transaction; an assessment upload can leave orphan file bytes if its database work fails.

`delivery.lock` uses an organization-level transaction lock and rechecks access after waiting. `write` also checks `If-Match` against the loaded revision and includes that revision in UPDATE. This prevents one user's older form from silently replacing another user's newer edit. A missing revision gives 428; a stale one gives 412.

`create` uses an idempotency key, meaning an identifier for a command that should not create duplicate effects when retried. It checks a payload fingerprint in `ppm_requests`. Assessment mutation receipts use their own fingerprint including method, URL, exact request bytes and revision; their replay rules are not identical to delivery's.

No custom database isolation level is set in `make_engine`. Do not claim the app runs with SERIALIZABLE isolation. Its lock coordinates participating operations, including membership changes and command snapshots; a privileged SQL writer outside that protocol is a separate case.

## Startup and diagnostics

`main.lifespan` loads settings and creates the engine, Redis client and local object store. Shutdown closes them. Compose applies migrations before API readiness; startup does not create all tables automatically.

GET `/api/v1/health/live` checks that the app responds. GET `/api/v1/health/ready` checks the database installation row, exact migration `0006_command_center`, Redis and storage. GET `/api/v1/foundation` returns the installation checkpoint. Readiness can fail while liveness succeeds.

To inspect without changing data, read those routes and `tests/test_api.py`/`tests/test_integration.py`. To understand an actual write, return to [chapter 2](REQUEST_LIFECYCLE.md).


## Source-reviewed Sprint 8.1 update — 9 October 2026

In `services/api/ppm_api/pilot.py`, `search` validates query length, type, offset and limit, then calls `records`. It builds SELECTs for projects/work/risks/assessments, escapes SQL wildcard characters, counts under the current principal/RLS, sorts by due date/name/type/id and returns items with links. `my_work` uses the same function with personal filters. Debug the authenticated organization and owning-row access before blaming pagination. This is SQL record discovery, not semantic document search; the latter is PLANNED in Sprint 09.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

Read `account_mail.account_message`, `smtp_delivery` and `deliver_due` with `identity.issue_challenge`/`complete`. STARTTLS verifies certificates, recipient refusal is failure, attempts are bounded, and terminal payloads are cleared. `provider_accepted` is distinct from `local_preview` and actual Gmail receipt. New links include an action hint but the stored challenge remains authoritative. Follow [account email and role access](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md) for code, live evidence and role/grant boundaries.

## Sprint 09 extension

Trace `documents.upload` → persisted version/job/outbox → `document_worker` → ClamAV/isolated parser → atomically replaced chunks. Actor/session/tenant authority is rechecked under the organization lock before publication; a broker tuple is not authority. [Document sources](../06-ai-and-analytics/DOCUMENT_SOURCES.md) explains transaction boundaries, replay, fencing and failures.
## Sprint 10 evidence runtime

ai.create, Runtime.call, ai_worker and settle extend the shared authorization, outbox and worker flow. Input/model/tool provenance is immutable; publication rechecks authority.

Read [the practical trace](../06-ai-and-analytics/AI_GATEWAY.md) for actual symbols, flow, failures and debugging. No Sprint 11 semantic agents or automatic changes are implemented.
