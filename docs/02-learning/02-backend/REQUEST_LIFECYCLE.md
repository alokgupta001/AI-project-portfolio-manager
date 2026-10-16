# How creating a project works

[Learning roadmap](../00-getting-started/README.md) Â· Next: [frontend](../03-frontend/FRONTEND_GUIDE.md)

This feature has a connected form, route, permission checks, database write and list refresh. Before trying it, activate an account using [the account setup guide](../../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md). The organization needs timezone/currency settings and an accessible portfolio. An Admin can create a project; a Project Manager needs a manage grant on its portfolio.

Keep [`delivery.tsx`](../../../apps/web/components/delivery.tsx), [`delivery.py`](../../../services/api/ppm_api/delivery.py), [`ppm_schemas.py`](../../../services/api/ppm_api/ppm_schemas.py) and [`identity.py`](../../../services/api/ppm_api/identity.py) open.

## Step 1: User action

Open the Projects workspace at `/projects` and use its create action. Enter the project's name, portfolio, currency and any relevant dates. The `Delivery` component opens `RecordEditor` with `kind="projects"` and no existing row. Submitting the form calls its `save` function.

## Step 2: Frontend code collects the fields

`RecordEditor` stores field values in React state, a temporary value used to render the form. `delivery-fields.ts` describes the fields for each record kind. `save` builds a body containing `kind`, `name`, `description`, `archived` and the project fields.

Checkboxes become booleans. Empty fields normally become `null`, except fields whose definitions require an empty string. The form also keeps one UUID command key while that editor is open. A UUID is an identifier designed to be unique.

Actual create-call excerpt from `RecordEditor.save`:

```typescript
await client.POST("/api/v1/delivery/{kind}", {
  params: { path: { kind }, header: { "idempotency-key": command } },
  body: body as DeliveryInput,
})
```

`POST` asks the API to create a record. `path` replaces `{kind}` with `projects`. The header identifies this particular create command. `body` carries the fields. The TypeScript cast describes the expected type; it does not validate data at runtime.

## Step 3: The browser sends the API request

The request is **POST `/api/v1/delivery/projects`**. Its body is a `ProjectInput`, with `kind: "projects"` and actual form values. Optional fields may be null; required fields include the common name, portfolio reference and currency.

`transport` in `apps/web/app/account/identity-client.tsx` supplies `x-csrf-token` and the loaded `x-organization-id`. Cookies carry login credentials. CSRF is a check that helps stop another website from submitting a change using your cookies.

`proxy` in `apps/web/app/api/v1/[...path]/route.ts` forwards allowed headers and JSON to its fixed `API_ORIGIN`. It forwards status and response data back. It does not save the project itself.

## Step 4: FastAPI receives the request

`main.create_app` registers `delivery.router`. The router prefix is `/api/v1/delivery`; its `@router.post("/{kind}")` calls `delivery.create` and declares a `RecordView` response with status 201.

Before the endpoint body can run, middleware checks the request, and FastAPI must successfully resolve parameters, authentication and body validation. These framework steps are not a promise that validation happens before every authentication query.

## Step 5: Authentication and permission checks

`identity.principal` verifies the access cookie and loads the database session. It rejects an expired or revoked session, an inactive membership or an unverified user. It supplies a `Principal` containing the user, session, current organization role and a database connection.

`delivery.lock` checks that the organization header matches the session organization, then takes a database lock shared by cooperating operations in that organization. A lock makes another operation wait. After waiting, it checks the membership and session again, so removed access cannot be used just because the earlier check passed.

`delivery.authorize` allows Admin creation. A Project Manager needs `grant(..., "portfolio_id", ..., ("manage",))`. The browser cannot select its own tenant or creator by adding fields to JSON.

## Step 6: Data validation

`Input` in `ppm_schemas.py` chooses its schema using `kind`. For projects it uses `ProjectInput`. UUID fields must parse as UUIDs. Status must be one of the allowed values. `ProjectInput.dates` rejects end dates before start dates, and completed projects need `actual_end_date`.

The common input schema rejects extra fields. Invalid request data produces HTTP 422 through `main.validation_error`, including field locations and reasons. Permission and state failures are different from invalid field types.

## Step 7: Project rules and retry handling

`delivery.create` calculates a fingerprint of the validated payload: a hash used to recognize whether a retry contains the same command. It searches `ppm_requests` for the organization, user and command key.

If a receipt exists with different data or record kind, the API returns 409. If it is the same command, the API reads the existing target and checks current authority again. It avoids creating another project.

For a new command, `delivery.write` checks that body kind and URL kind agree, that organization settings exist, and that referenced records are active and accessible. `refs` checks relationships such as the selected program belonging to the selected portfolio. The backend supplies the project ID, organization, creator, revision 1 and timestamps.

## Step 8: Database operation

Projects use `TABLES["projects"]` in `ppm_tables.py`, which describes table `ppm_projects`. This is a SQLAlchemy Core table, rather than a JPA-style managed entity.

Actual insert excerpt from `delivery.write`:

```python
d.update(id=id_, organization_id=p.session["organization_id"], created_at=stamp)
row = (await p.conn.execute(t.insert().values(**d).returning(t))).mappings().one()
```

The first line adds server-owned values to `d`, which already contains the validated fields, revision and update timestamp. The second builds an INSERT, sends it on the request connection, and asks PostgreSQL to return the inserted row. `mappings().one()` gives named columns and expects exactly one row.

Approximate SQL, shortened to show the idea rather than every column:

```sql
INSERT INTO ppm_projects (id, organization_id, name, portfolio_id, currency, revision, ...)
VALUES (:id, :organization_id, :name, :portfolio_id, :currency, 1, ...)
RETURNING *;
```

The `...` makes this explanatory SQL, not a command to paste into a database. SQLAlchemy sends values separately through asyncpg. PostgreSQL checks foreign keys, allowed values and row policies while executing the statement.

## Step 9: Save the whole operation

`audit_change` adds the new record and actor to `ppm_audit`. `create` adds a retry receipt to `ppm_requests`. If a Project Manager creates the project, `write` also inserts a project manage grant for that creator.

These database writes share the transaction opened by `principal` using `engine.begin()`. Successful exit commits them together. An exception rolls them back together; a project INSERT alone is not yet a permanent save.

The current definition is:

```python
Auth = Annotated[Principal, Depends(principal, scope="function")]
```

`Depends` tells FastAPI to prepare this shared request object. `scope="function"` makes dependency cleanup, including commit, finish before the response is sent. This matters because the UI immediately reads after saving. The [recorded CI fix](../../04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md) explains the earlier response-before-commit race. If commit fails, the caller must not receive a success response.

## Step 10: Response

`delivery.view` selects the public fields and checks the record data through the input adapter. `RecordView` contains `id`, `organization_id`, `revision`, timestamps and typed `data`. FastAPI serializes it as JSON; the proxy forwards it.

The frontend's `check` helper rejects a failed HTTP result. A successful create returns 201. It does not mean every planned module has become available.

## Step 11: UI update

`RecordEditor.save` calls `onSaved()` and `onClose()`. In `Delivery`, `onSaved` increments `refresh`, which causes the loading effect to fetch the scoped data again. React then renders the new records.

On failure, the form sets an error and retains unsaved values. Closing and reopening a create editor generates another command key; retry protection is tied to the original key, not to matching project names.

**The user saves a project. The frontend sends `ProjectInput` to `/api/v1/delivery/projects`. The backend verifies identity, portfolio permission and references, writes the project, audit and retry receipt together, commits before returning, and the frontend reloads its list.**

## Verify the flow yourself

1. Use your running local workspace and an authorized test record. In browser developer tools, open Network and save a project.
2. Inspect the POST URL, body, 201 response and following list GET. Avoid copying cookies or tokens into notes.
3. Reload the page and confirm that the project remains. Read `tests/test_delivery.py` for database and permission cases.
4. Read the create receipt branch and `ProjectInput.dates` to predict retry and invalid-date behavior without modifying normal data.

## Two shorter flows to read next

**View:** `Delivery` fetches GET `/api/v1/delivery/projects/{id_}` â†’ `delivery.detail` â†’ `get` selects by ID and session organization â†’ PostgreSQL applies row visibility â†’ `view` builds `RecordView` â†’ React displays the record. An absent or hidden record returns 404.

**Edit:** `RecordEditor.save` sends PATCH to the same detail URL with `If-Match: row.revision` â†’ `update` calls `write` â†’ current revision and permission are checked â†’ UPDATE uses the expected revision â†’ audit is appended â†’ commit â†’ list reload. PATCH here sends a full validated record payload. If two editors loaded revision 4, the first save produces 5 and the second gets 412. A missing revision gets 428. The second user's unsaved form stays available for reconciliation.


## Source-reviewed Sprint 8.1 update — 9 October 2026

The project-save lifecycle remains authoritative. Optional priority, industry, category, methodology and size travel through delivery form fields, `ppm_schemas.py`, `delivery.write`, and nullable project columns. Work priority/type follow the same route. Unknown is stored as missing metadata, not an invented classification. Inspect 0008 and `test_pilot.py` when a value is rejected; unrelated identity/notification changes do not alter dashboard formulas.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

For account email, trace `identity.register` or `reset_request` into `issue_challenge`, the durable delivery row and `account_mail.deliver_due`. Provider processing is asynchronous; the generic request response is not proof of receipt. Completion uses the stored challenge kind; the URL action hint only selects frontend wording. Signup creates organization/Admin after verification, invitation adds the intended membership, and recovery revokes sessions. See [the complete account lifecycle](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md).

## Sprint 09 extension

The document path adds private original storage before transactional version/job/outbox publication. SQL and file storage are not atomic, so orphan cleanup must recompute all protected references. Reads revalidate current authority, latest version/deletion and original hash. [Follow the complete source request](../06-ai-and-analytics/DOCUMENT_SOURCES.md).
## Sprint 10 evidence runtime

The asynchronous evidence path starts at AI in ai.tsx, enters ai.create, commits the shared durable job/outbox and is claimed by ai_worker. It preserves the project creation example above.

Read [the practical trace](../06-ai-and-analytics/AI_GATEWAY.md) for actual symbols, flow, failures and debugging. No Sprint 11 semantic agents or automatic changes are implemented.
