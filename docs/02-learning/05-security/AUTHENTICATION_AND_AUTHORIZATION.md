# Login and permissions are different checks

[Learning roadmap](../00-getting-started/README.md) Â· Next: [main features](../01-project-foundations/FEATURE_WORKFLOWS.md)

Authentication means identifying the logged-in user. Authorization means deciding whether that user may perform an action. Both are needed: being logged in does not let a Viewer edit a project.

## Authentication: from login to the next request

**What?** The app creates a revocable login session after checking credentials. **Why?** Every protected request needs a live identity, including after a role change or session revocation. **Where?** [`identity.py`](../../../services/api/ppm_api/identity.py), `identity_tables.py`, and the frontend's `IdentityClient` and `transport`.

The actual flow is:

1. The `/login` form in `IdentityClient` collects email and password. Shared transport obtains `/api/v1/auth/csrf` and adds its token to POST `/api/v1/auth/login`.
2. `main.request_context` requires the configured Origin and matching CSRF cookie/header for a write request.
3. `identity.login` validates `Credentials`, lowercases email and applies Redis login limits. `password_matches` checks a bcrypt password hash in a worker thread. A hash is a stored password-checking value, rather than the original password. Missing users also incur a dummy hash check.
4. Login requires a verified, globally active identity. It selects the first live membership ordered by organization UUID, or creates a session with no organization when there is none. A missing organization role does not disable the global account.
5. In a transaction, it inserts `identity_sessions`, a hashed random refresh credential in `identity_refresh_tokens`, and an audit entry. The session expires after seven days.
6. After its transaction completes, login sets access and refresh cookies and returns safe account data. The access cookie is a signed JWT with a ten-minute expiry. A JWT is a token containing claims that the server can verify; it is not a permission database.
7. A subsequent protected request resolves `principal`. It verifies the token signature, fixed HS256 algorithm, issuer, audience and required claims. It then loads the session, live membership and verified active user from PostgreSQL. `AccountAuth` permits personal account operations without membership; tenant `Auth` requires it.
8. `principal` rejects a revoked/expired session or mismatched organization and sets database user/organization/role context. Its connection and identity become the route's `Principal`.

Actual live-session check excerpt:

```python
if (
    not session
    or session["revoked"]
    or session["expires_at"] <= now()
    or session["organization_id"] != oid
):
    deny()
```

The first branch rejects a missing session. The next rejects revocation, even with a valid token signature. The expiry branch rejects an old session. The final branch prevents an old organization token being used after a switch. Membership and user checks follow this excerpt.

**Internally:** HttpOnly access/refresh cookies are managed by the browser and unavailable to normal JavaScript. The readable CSRF cookie is intentionally different. Cookie flags include Secure and SameSite Strict. The frontend's organization value is a request precondition; the verified session supplies authority.

**If something goes wrong:** an eligible 401 makes transport try `/auth/refresh`, sharing one refresh promise within that page and retrying a cloned request on success. `refresh` rotates the stored credential under a session lock. Reusing a consumed credential revokes the session; that revocation commits before denial so rollback cannot erase it. Separate tabs do not share a refresh grace window and may require signing in again.

Remember:

- The token must be valid, and the database session must still be active.
- A membership role is checked live, rather than trusted forever from the token.
- Refresh credentials rotate; replay is a session-revocation event.
- The local activation/reset mailbox is not external email delivery.

## Authorization: can this user change this project?

**What?** Authorization applies action rules after identity is established. **Why?** Organization membership alone should not grant every project action. **Where?** `delivery.authorize`, `grant`, `can_edit`; capacity access checks; assessment respondent/reviewer checks.

Actual `delivery.can_edit` expression:

```python
return (
    p.role == "Admin"
    or p.role == "Project Manager"
    and await grant(p, "project_id", id_, ("manage",) if manage else ("edit", "manage"))
)
```

Admin passes the project-edit check. Otherwise the user must be a Project Manager, and a project grant must exist at the required level. Ordinary edits accept edit or manage; actions needing manage require manage. A portfolio read grant can expose project data without satisfying this direct project-edit check.

For creating a project, `authorize` instead permits an Admin or a Project Manager with a portfolio manage grant. The creator then receives project manage access in the same transaction. A Viewer cannot bypass these checks by sending handcrafted PATCH JSON.

**Internally:** `delivery.lock` compares the organization header with the session, takes the shared organization lock, and reloads membership/session after waiting. This prevents permission removed during a wait from being used afterward. `identity.admin` uses the same lock for membership changes and protects the final active Admin.

**Failure:** insufficient authority gives a denial, such as 403; a hidden/missing target commonly gives 404. An organization mismatch gives 409 asking for reload. These causes differ from a stale record's 412.

Remember:

- Login identifies the user; role, grant and assignment checks decide actions.
- UI button visibility helps users but does not enforce access.
- Admin does not automatically get private resource effort access or impersonate an assigned assessment respondent.

## Organization separation and PostgreSQL row policies

Row Level Security, or RLS, lets PostgreSQL filter or reject rows based on policies. It supports the Python checks at the database boundary. The app uses shared tables with `organization_id`, rather than a separate database schema for each organization.

Actual excerpt from `identity.context`:

```python
"SELECT set_config('ppm.user_id', :u, true), "
"set_config('ppm.organization_id', :o, true), "
"set_config('ppm.role', :r, true)"
```

The bound `u`, `o` and `r` values come from the verified identity and membership. Each `true` makes the setting last only for the transaction. Commit or rollback clears it before the pooled connection is reused. The browser does not directly set these database values.

`0003_delivery.py:upgrade` builds `tenant_read` for `ppm_projects`. The policy requires the row's organization to equal the transaction's `ppm.organization_id`, and the user to be Admin or hold an allowed project/portfolio grant. Its `granted` helper checks user, organization, target, access level and that the grant is not archived.

For example, `delivery.get` sends a SELECT for a project ID and session organization. PostgreSQL adds its policy checks to determine which rows are available. A foreign organization's row stays hidden; a local row without scope may also stay hidden. Missing transaction context does not grant access.

The mechanism is connected: the request sets transaction context, queries use the restricted `ppm_app` role, and migrations install policies/privileges. A policy file alone would not prove protection if the app connected as an unrestricted owner. `infra/postgres/init.sh` creates a non-owner app role without RLS bypass. Owner maintenance queries are a different boundary.

Read `tests/test_identity.py` and `tests/test_delivery.py` for cross-tenant and reused-connection cases. The guarded backend runner exercises these on the test database. A Python tenant filter, a foreign key and RLS serve related but different purposes: selecting scope, enforcing valid relationships and restricting database rows.

## Other checks worth understanding

`identity.limited` stores login/reset attempt counts in Redis for a ten-minute window. Redis failure returns 503 rather than bypassing the limiter; too many attempts returns 429.

`main.request_context` checks exact Origin and CSRF. `principal` also checks the token against the session's CSRF digest for unsafe requests. Request IDs help correlate an error; they do not identify the user.

Evidence upload uses generated paths, size/content restrictions and manual reviewer release. A SHA256 digest detects changed bytes; it does not establish that the document is true. Manual quarantine is not antivirus. Chapter [7](../01-project-foundations/FEATURE_WORKFLOWS.md) explains that workflow.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Trace `/signup` to `identity.register`, then the challenge completion branch in `identity.complete`. Email-scoped locking and one atomic transaction create the verified user, organization and first Admin only after verification. `account_mail.py` stores/dispatches local or SMTP delivery; a timeout may follow provider acceptance, so single-use/replaced challenges remain the authority. Organization profile editing requires Admin and If-Match; invitation resend/cancel rechecks live inviter authority. Framework/result Access panels reuse assessment guards. Debug private operator mailbox configuration and challenge expiry without exposing tokens; `test_pilot.py` covers replay, revoked authority and scope.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

Real Gmail signup, existing-account Viewer invitation acceptance and recovery are verified in development. A one-time email challenge and cookie-based access/refresh session credentials serve different purposes. The URL action hint is presentation only; server challenge validation and live membership/grants remain authoritative. Role changes use Admin controls, while portfolio/project, resource, framework and result grants control work access. Read [account email and role access](ACCOUNT_EMAIL_AND_ROLE_ACCESS.md) for the full trace and safe debugging example.


## Account status and membership are separate

[`0009_account_repair`](../../../services/api/migrations/versions/0009_account_repair.py) adds global account status and nullable session organization. Revoking an organization membership immediately denies that organization's requests; it leaves personal profile/session access and other organizations intact. Refresh removes a revoked active organization, and selecting another accessible organization rechecks its own role. [`authenticated`](../../../services/api/ppm_api/identity.py) enforces this before route queries, and [`test_account_repair.py`](../../../tests/test_account_repair.py) tests the boundary.

[`account_status.py`](../../../scripts/account_status.py) is a separate development operator operation. Disabling a user preserves membership and project ownership, revokes sessions and protects the last active Admin. Organization administrators cannot call a global-disable API. Background jobs also read global status before effects.

The Hement example illustrates the next boundary: portfolio manage permits creating a project; editing an Admin-created project requires a direct project edit/manage grant. Neither an owner label nor a team assignment creates that permission. The guarded local correction gives only the diagnosed portal project edit grant. See [repair results](../../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md).

## Sprint 09 extension

Project document reads require scoped grants; writes require Admin or explicitly permitted PM. Organization-wide policy writes require Admin. Same-byte assessment links separately require private released-evidence authority. Citation/download reads recheck live scope/deletion; a 60-second ticket also binds user/session/org/version/hash. Workers revalidate persisted authority and fenced leases. [Source security/debugging](../06-ai-and-analytics/DOCUMENT_SOURCES.md) explains fail-closed antivirus, hostile text, limits and retention.
## Sprint 10 evidence runtime

Admin starts analyses and reads diagnostics; PM/Viewer cannot access restricted usage/errors/budgets. SourceTool independently rechecks immutable run scope, and every result resolves current permitted citations. Retrieved text has no mutation or tool authority.

Read [the practical trace](../06-ai-and-analytics/AI_GATEWAY.md) for actual symbols, flow, failures and debugging. No Sprint 11 semantic agents or automatic changes are implemented.
