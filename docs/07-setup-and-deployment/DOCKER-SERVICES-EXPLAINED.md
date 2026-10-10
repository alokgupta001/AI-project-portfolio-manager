# Enterprise PPM Docker Services Explained

This guide explains the eight services shown in Docker Desktop for `enterprise-ppm`: `postgres`, `redis`, `migrate`, `api`, `dispatcher`, `worker`, `web`, and `pgadmin`. It describes what each process does, how requests and background jobs move between them, where data is stored, and how to check a problem without deleting project data.

The application needs several processes because serving pages, storing records, and executing background work have different responsibilities. **PostgreSQL holds the authoritative business records; Redis transports background tasks; the API implements application rules; the web service provides the browser interface.** The scheduler and worker keep background processing separate from interactive requests. Migration and database administration have their own containers.

Container status was checked on **10 October 2026 at approximately 10:46 IST**. Status is a snapshot and can change after this document is written.

## Guide contents

- [Service overview](#service-overview) and [how the services work together](#how-the-services-work-together)
- [PostgreSQL](#postgresql-stores-application-records), [Redis](#redis-transports-tasks-and-stores-short-lived-state), and [migrate](#migrate-prepares-the-database-schema)
- [API](#api-implements-application-rules), [dispatcher](#dispatcher-schedules-recurring-work), and [worker](#worker-performs-background-tasks)
- [Web](#web-serves-the-browser-interface) and [pgAdmin](#pgadmin-provides-direct-database-administration)
- [Ports and persistent data](#ports-networks-and-persistent-data), [everyday commands](#everyday-commands), and [troubleshooting](#troubleshooting-by-symptom)
- [Test service](#additional-service-outside-the-screenshot) and [further reading](#configuration-and-further-reading)

## Service overview

| Service | Technology | Main responsibility | Access from this PC | Verified state |
| --- | --- | --- | --- | --- |
| `postgres` | PostgreSQL 18 | Persistent relational database | `localhost:15432`, PostgreSQL protocol | Running and healthy |
| `redis` | Redis 8 | Celery task broker, task results, and identity rate limits | `localhost:16379`, Redis protocol | Running and healthy |
| `migrate` | Alembic in the Python backend image | Apply database schema migrations | No published port | Exited successfully with code 0 |
| `api` | FastAPI and Uvicorn on Python 3.12 | Validate requests, enforce access, and read or write application data | <http://localhost:8000> | Running and healthy |
| `dispatcher` | Celery Beat | Schedule `pipeline.dispatch` every 10 seconds | No published port | Running |
| `worker` | Celery worker | Execute dispatch, ingestion, and checkpoint tasks | No published port | Running |
| `web` | Next.js 16 and React 19 on Node.js 24 | Serve the user interface and proxy API requests | <http://localhost:3000> | Running and healthy |
| `pgadmin` | pgAdmin 4 version 9.18 | Browse and administer PostgreSQL | <http://localhost:5050> | Running |

`dispatcher`, `worker`, and `pgadmin` do not have explicit health checks in these Compose files. Their running status confirms that the container process is active; it does not prove that every operation succeeds. `migrate` is a one-time task, so its successful stopped state is expected.

## How the services work together

### Ordinary browser requests

```text
Your browser
    | http://localhost:3000
    v
web  -- /api/v1 requests -->  api  -->  postgres
                              |          business records
                              +-----> redis
                              |          identity rate limits
                              +-----> objects volume
                                         stored files
```

For example, opening a projects page loads the interface from `web`. Its API requests go through the Next.js proxy to `http://api:8000` inside Docker. The API checks the user's identity, organization, permissions, and request data before accessing PostgreSQL. The response returns through `web` to the browser.

The browser does not connect directly to PostgreSQL or Redis. Accessing `api:8000` from inside Docker is different from accessing `localhost:8000` from Windows.

### Background integration jobs

```text
api --> postgres: persist job, progress, audit, and outbox record

dispatcher --> redis: schedule pipeline.dispatch every 10 seconds
                  |
                  v
worker: execute pipeline.dispatch
    | deliver due account mail
    | query PostgreSQL for due jobs
    +--> redis: publish pipeline.run for each due job
              |
              v
worker: execute pipeline.run --> postgres: effects and progress
```

The container named `dispatcher` runs **the scheduler**, not the function that queries due jobs. That query occurs when a worker executes the scheduled `pipeline.dispatch` task. Both dispatch and ingestion use the `foundation` queue. If the worker stops, scheduling can continue but the scheduled tasks cannot execute.

PostgreSQL records which jobs need work. Redis carries messages that make workers act on those records. The application can rediscover queued jobs, due retries, and jobs whose processing lease expired. This design supports recovery from interruptions without making Redis the sole record of unfinished work.

### Startup order

1. PostgreSQL and Redis start and must pass their health checks.
2. `migrate` waits for healthy PostgreSQL and runs `alembic upgrade head`.
3. `api` waits for a successful migration and healthy Redis.
4. `web`, `worker`, and `dispatcher` wait for the API health check to pass.
5. When included through its additional Compose file, `pgadmin` waits for healthy PostgreSQL.

These conditions govern startup. They are not a continuous mechanism that restarts all dependents if a dependency later fails. [Docker documents the distinction between starting, being healthy, and completing successfully](https://docs.docker.com/compose/how-tos/startup-order/).

## PostgreSQL stores application records

### Purpose and contents

`postgres` runs the project's PostgreSQL 18 database server. It stores structured records such as organizations, users, memberships, portfolios, programs, projects, work items, assessments, integration configuration, durable jobs, progress events, and audit history. Persistent identifiers and relationships let the application connect these records reliably.

The initialization script creates three databases:

- `ppm_local` for the ordinary local application.
- `ppm_test` for the isolated backend test runner.
- `ppm_demo` for demo use.

The main Compose stack points its application services at `ppm_local`. Separate databases provide data separation, but a demo deployment also needs its documented configuration and startup procedure; merely having `ppm_demo` present does not activate a demo stack.

### Connections and database roles

From Windows, database clients use host `localhost`, port `15432`, and database `ppm_local`. Inside Docker, services use `postgres:5432`. The mapping `15432:5432` means host port 15432 forwards to container port 5432. It is a database connection, not a website link.

The backend application uses `ppm_app`; migration uses `ppm_owner`; the configured pgAdmin connection uses the administrative `postgres` role. The initialization script makes the two project roles non-superusers without permission to bypass row level security. Domain policies and transaction context help scope application access to the current organization and user. PostgreSQL superusers can bypass ordinary row security, so the pgAdmin connection is more powerful than application access. [PostgreSQL row security documentation](https://www.postgresql.org/docs/18/ddl-rowsecurity.html).

### Persistence and checks

The named volume `enterprise-ppm_postgres_data` is mounted at `/var/lib/postgresql`. It contains database files that survive container replacement when the volume is preserved. The first initialization also mounts `infra/postgres/init.sh` into the image's initialization directory. That script is setup for a new database volume, not a password rotation mechanism for an existing installation.

The health check uses `pg_isready -U postgres -d ppm_local` every three seconds, with a three-second timeout and 30 retries. It tests database availability; the API readiness check separately verifies the required application schema checkpoint.

If PostgreSQL stops, database-backed API operations and background jobs fail. For an initial check:

```powershell
docker compose logs --tail 100 postgres
docker compose exec -T postgres pg_isready -U postgres -d ppm_local
```

Do not delete the database volume to fix an ordinary connection problem. Preserve existing credentials and inspect the error first.

Sources: [Compose configuration](../../compose.yaml), [database initialization](../../infra/postgres/init.sh), [application database engine](../../services/api/ppm_api/database.py), and [database viewer guide](DATABASE-VIEWER.md).

## Redis transports tasks and stores short lived state

### Actual use in this application

`redis` runs Redis 8. Its main role is the message transport between Celery Beat and Celery workers. The same configured Redis URL serves as the Celery result backend, where task result metadata is retained for 300 seconds.

The API also uses Redis for identity rate limiting. Its limiter atomically increments a counter and sets a 600-second expiry. When the limit is exceeded, the API returns HTTP 429. If Redis is unavailable, this limiter rejects the affected operation with HTTP 503 instead of silently allowing unlimited attempts.

Although Redis is commonly used as a general cache, the code inspected here establishes task transport, task result storage, and identity limiting. Do not assume that project pages or all database queries are cached in Redis.

### Connection details and storage

The local stack uses `redis://redis:6379/0`. The final `/0` selects logical Redis database 0. The profile-based test runner uses database 1 on the same Redis server; this is logical separation rather than a separate container.

Windows clients use `localhost:16379`; Docker services use `redis:6379`. Redis speaks its own protocol, so opening port 16379 in a web browser is not a useful connectivity test.

Redis starts with `redis-server --appendonly yes`. Its append-only persistence files are stored under `/data` in `enterprise-ppm_redis_data`. Persistence helps retain Redis state across restarts, but it does not make Redis a replacement for PostgreSQL or guarantee recovery from every failure.

### Health and failure effects

The health check runs `redis-cli ping` every three seconds, with a three-second timeout and 30 retries. A normal reply is `PONG`.

```powershell
docker compose exec -T redis redis-cli ping
docker compose logs --tail 100 redis
```

If Redis stops, publishing or consuming Celery messages is interrupted, task result access fails, identity rate limiting becomes unavailable, and API readiness returns not ready. PostgreSQL still retains durable job records. When transport and workers recover, scheduled reconciliation can discover due jobs again; this should not be interpreted as an exactly-once delivery guarantee.

Sources: [Compose configuration](../../compose.yaml), [Celery application](../../services/worker/ppm_worker/app.py), and [identity limiter](../../services/api/ppm_api/identity.py).

## Migrate prepares the database schema

### Why a separate container exists

`migrate` is a one-time Alembic migration process. It creates or updates the schema expected by the backend: tables, constraints, indexes, access policies, and migration-defined functions. Keeping it separate makes successful migration an explicit prerequisite for API startup.

It uses the shared Python backend build from `infra/api.Dockerfile` but replaces the default API command with:

```text
alembic upgrade head
```

`head` means the latest migration revision in the migration source bundled into that image. For this project checkpoint, the API readiness code expects `0008_pilot_completion`.

### Credentials and execution

The migration-specific connection uses `ppm_owner` and `ppm_local` at `postgres:5432`. Ordinary API and worker access uses `ppm_app`. Different roles separate schema ownership from routine application access.

The container waits for PostgreSQL to be healthy. It applies pending revisions and exits. It has no HTTP server, no published port, and no reason to stay running after successful completion. The shared backend configuration mounts the `objects` volume, but its main responsibility is database schema maintenance.

### Reading its status correctly

In the supplied screenshot, `migrate` has a start control instead of a stop control. The live check confirmed **`Exited (0)`**, which means the process completed successfully. You do not need to keep starting it simply because the other containers continue running.

A nonzero exit code requires investigation. The API's dependency condition is `service_completed_successfully`, so a failed migration can prevent dependent application services from starting.

```powershell
docker compose ps -a migrate
docker compose logs --tail 100 migrate
```

After intentionally updating application code and reviewing migration changes, the documented build and startup procedure will apply the image's current schema changes. Do not downgrade the active local database or remove migration history as an ordinary troubleshooting step. An already initialized database also needs its original compatible credentials; changing a password string in `.env` does not itself update a PostgreSQL role.

Sources: [Compose configuration](../../compose.yaml), [backend Dockerfile](../../infra/api.Dockerfile), [migration source directory](../../services/api/migrations/versions/), and [API readiness code](../../services/api/ppm_api/main.py).

## API implements application rules

### What it serves

`api` runs FastAPI through Uvicorn on Python 3.12. Its default container command launches `ppm_api.main:app` on port 8000. It provides the backend for identity, organization access, delivery records, capacity, assessments, command center functions, pilot features, and integration jobs.

The API validates request structure, verifies identity and permissions, applies business rules, accesses PostgreSQL, and returns responses. Integration job requests persist their job and associated records before background execution. This lets a user request work without keeping a browser request open until ingestion completes.

Requests carry generated or validated request IDs. The API returns an `X-Request-ID` header and records structured request timing information. Its errors are sanitized so raw driver messages and connection strings are not exposed to the caller.

### Dependencies and security

The API uses PostgreSQL through SQLAlchemy and asyncpg, Redis through the asynchronous Redis client, and a local object store rooted at `/var/ppm/objects`. The `objects` named volume preserves stored files across container replacement.

State-changing requests normally require the configured origin and matching CSRF cookie/header. The code has a specific exception for the signed GitHub webhook route; that route has its own integration verification. A browser call to the wrong origin can therefore fail even when the API process is healthy.

The Compose configuration uses `PPM_WEB_ORIGIN`, defaulting to `http://localhost:3000`, and enables secure cookies. Use the project's documented identity setup and configured browser origin when troubleshooting login. Do not change security settings just to make a failing test appear successful.

### Health endpoints

| Endpoint | Meaning |
| --- | --- |
| `/api/v1/health/live` | The API process can serve its liveness endpoint |
| `/api/v1/health/ready` | Database checkpoint, expected schema revision, Redis ping, and object-store read/write probe succeed |
| `/api/v1/foundation` | Return the persisted installation checkpoint |
| `/docs` | Interactive FastAPI API documentation |

Readiness returns HTTP 200 when every dependency probe succeeds and HTTP 503 otherwise. Docker calls this readiness endpoint every five seconds, with a six-second timeout and 20 retries.

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/health/ready
docker compose logs --tail 100 api
```

If the API is unavailable, the web interface cannot reliably load or change application data. Readiness does not test worker consumption or SMTP delivery, so a healthy API alone does not prove that background work is completing.

Sources: [API entry point](../../services/api/ppm_api/main.py), [settings](../../services/api/ppm_api/config.py), [object storage](../../services/api/ppm_api/storage.py), and [local development guide](LOCAL-DEVELOPMENT.md).

## Dispatcher schedules recurring work

### What this container actually runs

`dispatcher` runs **Celery Beat**, the scheduler associated with the project's Celery application. It uses the shared backend image and starts with:

```text
celery -A ppm_worker.app:celery_app beat --loglevel=WARNING --schedule=/tmp/ppm-celerybeat
```

Its schedule contains one recurring entry named `reconcile-durable-jobs`. Every 10 seconds, Beat publishes a `pipeline.dispatch` task to Redis. An available worker then executes it. The schedule is explicitly configured for UTC.

This distinction matters operationally: the scheduler container can be running while no jobs are processed if the worker is stopped or unavailable. The function called `dispatch` lives in the worker application and is executed by workers, not directly by Beat.

### What the scheduled task triggers

When a worker receives `pipeline.dispatch`, it first attempts due account-mail delivery. Then it calls the database function `public.ppm_due_jobs()` and publishes a `pipeline.run` task for each returned job identifier. Those messages include job, organization, and actor identifiers; persisted records supply the actual job data and authorization context.

This recurring scan finds queued jobs, due retry jobs, and running jobs with expired leases. A scan every 10 seconds is a polling interval, not a guarantee that a particular job starts or finishes within 10 seconds. Worker availability, queue backlog, mail delivery, and provider responses can affect timing.

### Runtime and checks

The container has no published port. Its scheduler state file is under `/tmp/ppm-celerybeat`, outside a dedicated persistent scheduler volume. Durable application job state remains in PostgreSQL. Compose starts the scheduler after the API becomes healthy; no separate scheduler health check is defined.

```powershell
docker compose ps dispatcher
docker compose logs --tail 100 dispatcher
```

The configured `WARNING` logging level can make an idle, healthy scheduler appear quiet. Lack of frequent log messages alone is not evidence of failure.

If the scheduler stops, already queued tasks may still execute, but new recurring dispatch scans stop. Keep one scheduler for this schedule. [Celery explains that multiple schedulers for the same schedule can publish duplicate tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html).

Sources: [Compose command](../../compose.yaml) and [task definitions and schedule](../../services/worker/ppm_worker/app.py).

## Worker performs background tasks

### Execution responsibilities

`worker` is the Celery process that consumes task messages from Redis and performs the actual work. The command configures concurrency 2 and a worker hostname beginning with `foundation@`. The default queue is `foundation`.

The registered tasks are:

- `foundation.database_checkpoint`: read the persisted installation identifier from PostgreSQL and return a completion result. This is a diagnostic task, not a recurring scheduled entry in the current configuration.
- `pipeline.dispatch`: deliver due account mail, discover due database jobs, and enqueue execution tasks.
- `pipeline.run`: execute a durable integration job using its stored identifiers and records.

Integration execution supports bounded CSV import and configured GitHub or Jira adapters. Live provider access requires valid connector configuration and credentials. Merely running the worker does not establish that external provider authentication works.

### Durable processing and authorization

Business job progress lives in PostgreSQL. The ingestion code uses a 45-second lease, heartbeat updates, and a fencing token for each attempt. It skips terminal jobs and avoids taking over a job with a current lease. Row or page checkpoints preserve completed work across recoverable interruptions.

The worker rechecks persisted actor, session, organization, and permission information. A queue message cannot grant permissions by itself. Attempts are limited to five; retryable provider errors cause delayed retry, while some errors fail with a sanitized reason. Completed effects are not automatically rolled back by a later cancellation.

`pipeline.run` uses late acknowledgment and rejection when a worker is lost. Combined with leases and repeated due-job discovery, this supports recovery and repeat-safe processing. It should not be described as universal exactly-once execution.

### Limits and operational checks

The Celery configuration sets a 280-second soft task time limit and a 300-second hard limit, uses JSON messages, retains task results for 300 seconds, and prefetches one message per worker process. Both ingestion and dispatch share worker capacity.

```powershell
docker compose logs --tail 100 worker
docker compose exec -T worker celery -A ppm_worker.app:celery_app inspect ping --timeout=5
```

A responding worker normally returns `pong`. The inspector sends Celery control messages through the broker; it does not test a live provider import. Empty or timed-out responses require checking the broker and worker logs.

If the worker stops, the web/API may remain usable, but ingestion and scheduled mail-delivery tasks stop executing. Compose gives this service no explicit health check.

Sources: [Celery application](../../services/worker/ppm_worker/app.py), [ingestion execution](../../services/api/ppm_api/jobs.py), and [durable jobs contract](../contracts/jobs-integrations.md).

## Web serves the browser interface

### User facing responsibilities

`web` runs the Next.js application with React. It provides pages for the workspace, login and signup, organizations, portfolios, projects, resources, assessments, command center, integrations, and account actions. The `/system` page provides technical diagnostics; `/design-system` is a component gallery.

The Docker image uses Node.js 24, installs dependencies from `package-lock.json`, and builds the application during image creation. It then runs `next start` in production mode on container port 3000 under the non-root `node` user. This is a built server, so changing source files on Windows does not automatically rebuild this container.

### API proxy behavior

The environment sets `API_ORIGIN=http://api:8000`. The route under `app/api/v1/[...path]/route.ts` forwards browser API calls to the backend. It passes selected cookies and headers needed for CSRF verification, organization selection, concurrency control, idempotency, and integration requests. It also forwards response cookies and selected diagnostic headers.

The proxy disables fetch caching, applies request body limits, and normally uses a 15-second API timeout. Event streams receive special handling so progress can stream through to the browser. If the backend cannot be reached, the proxy returns an API-unavailable response with HTTP 503.

Keeping the API proxy on the same browser origin simplifies cookie and request handling. The browser uses `http://localhost:3000`; the Next.js server uses the internal Docker hostname `api`.

### Access and health

Open <http://localhost:3000> for the application. The web health check fetches the root page inside the container every 10 seconds, with a 10-second timeout and 20 retries. A successful root page does not prove that every protected API request or background job succeeds.

```powershell
docker compose logs --tail 100 web
(Invoke-WebRequest http://localhost:3000).StatusCode
```

If `web` stops, the browser interface is unavailable, but the API, database, and background processes can still be running. If pages load but data does not, inspect API readiness and failed browser network requests. For login problems, use the configured origin consistently: `localhost` and `127.0.0.1` are different origins.

Sources: [web Dockerfile](../../infra/web.Dockerfile), [web package configuration](../../apps/web/package.json), [API proxy](../../apps/web/app/api/v1/%5B...path%5D/route.ts), and [identity development guide](IDENTITY-DEVELOPMENT.md).

## pgAdmin provides direct database administration

### Purpose and access

`pgadmin` is a database administration website. It lets you inspect tables, view records, execute SQL, and administer PostgreSQL. It is separate from the Enterprise PPM user interface and is optional for normal application operation.

It is defined in `compose.database-viewer.yaml`, which supplements `compose.yaml`. The image is `dpage/pgadmin4:9.18`, pinned by digest. Its host mapping is `5050:80`: Windows uses <http://localhost:5050>, while pgAdmin's internal web server listens on container port 80.

The preconfigured database connection uses host `postgres`, port 5432, maintenance database `ppm_local`, and username `postgres`. Because pgAdmin is itself inside Docker, `localhost:15432` is not the connection it uses to reach the database.

### Local desktop configuration

The configuration disables server mode and the master-password requirement. The project guide describes a local viewer that opens without a login screen. A bootstrap password secret is still mounted for container configuration; do not copy its value into documentation or share it.

The server definition is supplied through `servers.json`, and a password file supplies the PostgreSQL connection credentials. pgAdmin's own preferences and state live in `enterprise-ppm_pgadmin_data` mounted at `/var/lib/pgadmin`. This volume is distinct from the actual PostgreSQL database volume.

### Reading records safely

In the viewer, expand:

```text
Servers > Enterprise PPM - Local database > Databases > ppm_local
        > Schemas > public > Tables
```

For example, open Query Tool and run:

```sql
SELECT id, name FROM public.ppm_projects LIMIT 50;
```

The configured `postgres` connection is administrative. Changes made through pgAdmin affect the real application database and can bypass application-level permission checks. Start with read-only inspection when learning the schema.

### Runtime behavior

pgAdmin depends on healthy PostgreSQL and has `restart: unless-stopped`. Unlike the other services shown, it has an explicit restart policy. It has no explicit Compose health check.

```powershell
docker compose -f compose.yaml -f compose.database-viewer.yaml logs --tail 100 pgadmin
```

If pgAdmin stops, the application can still run normally. If its page loads but the database connection fails, check PostgreSQL and the saved connection settings separately.

Sources: [viewer Compose configuration](../../compose.database-viewer.yaml) and [database viewer instructions](DATABASE-VIEWER.md).

## Ports networks and persistent data

### Interpreting the screenshot

Docker Desktop groups these containers under the Compose project name `enterprise-ppm`. A service is the named configuration, an image is the packaged software, and a container is an instance created from that image. For example, service `api` currently has container `enterprise-ppm-api-1` and image `enterprise-ppm-api`.

Several services use the same backend Dockerfile but start different commands. `api` launches Uvicorn, `migrate` launches Alembic, `worker` launches a Celery worker, and `dispatcher` launches Celery Beat. Similar image names do not mean they are doing the same work.

The published ports are bound to `127.0.0.1`, restricting host access to this PC's loopback interface. Internal container traffic uses the Compose network `enterprise-ppm_default` and service names such as `postgres`, `redis`, and `api`. Inside a container, `localhost` refers to that container itself.

| Data | Volume | Container location | Why it matters |
| --- | --- | --- | --- |
| PostgreSQL database files | `enterprise-ppm_postgres_data` | `/var/lib/postgresql` | Business records, schema, identities, jobs, and audit data |
| Redis persistence | `enterprise-ppm_redis_data` | `/data` | Task transport and persisted Redis state |
| Object storage | `enterprise-ppm_objects` | `/var/ppm/objects` | Application files and local account-mail artifacts when local mail mode is used |
| pgAdmin preferences | `enterprise-ppm_pgadmin_data` | `/var/lib/pgadmin` | Viewer state, distinct from application records |

The backend services share the object volume through a Compose configuration anchor. `web` has no application-data volume in this configuration. Do not treat a container's writable layer as the durable location for important application data.

### Mail delivery is not another container

The screenshot has no separate mail server. Account messages are processed during worker execution of `pipeline.dispatch`. With `PPM_MAIL_MODE=local`, delivery writes private JSON artifacts under `/var/ppm/objects/__identity_mailbox__`. With configured SMTP mode, the worker connects to the external SMTP server. The default in Compose is local mode; the effective mode can be overridden by local configuration.

Stopping the worker can therefore affect account invitation, activation, registration verification, or password-reset delivery even while the website remains accessible. See [account-mail implementation](../../services/api/ppm_api/account_mail.py) and [SMTP setup](GMAIL-SMTP-SETUP.md).

## Everyday commands

Run commands from the project root:

```powershell
Set-Location 'C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm'
```

### Inspect the whole stack

```powershell
docker compose -f compose.yaml -f compose.database-viewer.yaml ps -a
docker compose logs --tail 100 api worker dispatcher
Invoke-RestMethod http://localhost:8000/api/v1/health/ready
```

Use `ps -a` to include the completed migration container. When checking pgAdmin, include its additional Compose file. Avoid publishing full resolved Compose output because environment substitution can reveal credentials.

### Start or stop existing services

```powershell
# Start the configured stack including the existing database viewer.
docker compose -f compose.yaml -f compose.database-viewer.yaml up -d

# Stop it while preserving containers and named volumes.
docker compose -f compose.yaml -f compose.database-viewer.yaml stop

# Stop only the optional database viewer.
docker compose -f compose.yaml -f compose.database-viewer.yaml stop pgadmin
```

The viewer startup requires its existing password-secret file. Keep the established `.env` and local secret files. Routine start and stop actions do not require running bootstrap again.

### Apply a deliberate code update

```powershell
docker compose -f compose.yaml -f compose.database-viewer.yaml up --build -d --wait
```

This builds local application images, starts or recreates changed services, and waits for applicable running/healthy conditions. Review schema changes before updating an established database. `docker compose restart` restarts existing containers; it does not rebuild images or apply changed environment configuration.

For stopping or ordinary troubleshooting, **do not use `docker compose down -v`**. The `-v` option removes Compose-managed named volumes, including persistent data. A preserved volume is also not a backup: an actual backup must be separately created and recoverable.

## Troubleshooting by symptom

| Symptom | First checks | Likely relationship |
| --- | --- | --- |
| Migration container is stopped | Check exit code and migration logs | Exit code 0 is normal; a nonzero code can block API startup |
| API is unhealthy | Read `/api/v1/health/ready` and API logs | Database, schema checkpoint, Redis, or object storage probe failed |
| Website does not open | Check `web` state, port 3000, and web logs | Browser entry point is unavailable |
| Website opens but data requests fail | Check API readiness and response status | A healthy root page does not establish backend request success |
| Jobs remain queued | Check dispatcher, worker response, Redis ping, and job activity | Scheduling or consumption may be interrupted, or worker capacity occupied |
| Jobs show retry or failure | Check sanitized activity and connector configuration | Provider, authorization, mapping, or processing errors may be involved |
| Account email does not arrive | Check worker and configured mail mode | Local mode writes artifacts; SMTP requires external configuration and successful delivery |
| pgAdmin opens but cannot connect | Check PostgreSQL and pgAdmin connection settings | Viewer availability and database connectivity are separate |
| Login or writes return 403 | Check exact origin and CSRF flow | Identity verification can reject a request despite healthy containers |
| Identity request returns 429 | Respect retry delay and inspect intended request flow | Redis-backed rate limiting is active |

Investigate the failing layer first. Restarting every container can temporarily hide a symptom without resolving its cause. Keep data and credentials intact while gathering status, bounded logs, readiness results, and job activity.

## Additional service outside the screenshot

The main Compose file also defines `test`, gated behind the `test` profile. It runs `python scripts/test_backend.py`, uses `ppm_test`, selects Redis database 1, and uses temporary test object storage without the main objects mount. It is a test runner rather than an ordinary continuously running application service.

The documented command is:

```powershell
docker compose --profile test run --build --rm test
```

This command executes tests and migration lifecycle checks against the isolated test database. It is included here for reference; tests are not required just to read the service guide or inspect the running application.

## Configuration and further reading

The descriptions above refer to the current local stack and its source configuration. The project documents local implementation bounds and does not establish production acceptance. Service names and available pages should not be taken as proof that every planned capability or external integration is enabled.

For the next level of detail, use:

- [Local development and startup](LOCAL-DEVELOPMENT.md)
- [Environment variable reference](ENVIRONMENT_VARIABLES.md)
- [Identity development and browser setup](IDENTITY-DEVELOPMENT.md)
- [Database viewer guide](DATABASE-VIEWER.md)
- [Durable jobs and integrations contract](../contracts/jobs-integrations.md)
- [Main Compose configuration](../../compose.yaml) and [viewer extension](../../compose.database-viewer.yaml)
- [Celery task implementation](../../services/worker/ppm_worker/app.py) and [API implementation](../../services/api/ppm_api/main.py)

Official references used for platform behavior are [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/), [Celery periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), and [PostgreSQL 18 row security](https://www.postgresql.org/docs/18/ddl-rowsecurity.html).
