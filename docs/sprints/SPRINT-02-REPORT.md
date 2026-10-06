# Sprint 02 implementation report

## Status and scope

2026-10-05: **Complete for local identity and organization authorization.** F-001 JWT/session lifecycle, F-002 identity/member RBAC, F-003 implemented tenant isolation and N-001 bcrypt are accepted within this scope. N-012/N-018 remain ongoing. Source S4.1 and Sprint 02 map through [coverage](../requirements/coverage.md). Branch main has no commit/remote; work is uncommitted. Originals and `0001_foundation` are preserved. No paid service, external email, AI or later domain module was implemented. Sprint 03 has not started.

## What was built

Working `/login`, `/account`, `/account/reset` and `/account/complete` screens support activation, login/logout, organization switching, own profile, sessions/revocation and recovery. Admins invite members, change roles/active state and read scoped identity audit. PM/Viewer manage their own accounts but cannot administer organizations. The final active Admin cannot be removed/demoted. Forms have accessible labels, loading/error feedback and responsive enterprise styling; data comes through the real generated API client.

An explicit operator command creates an organization and pending first Admin. One-time links are delivered only to a private local mailbox. No default password or user-owned administrator was invented; acceptance users live in isolated test databases.

## Why and how

Later project, assessment and intelligence features need a consistent authenticated organization boundary. This extends the existing runtime/schema instead of creating another auth stack. Live membership checks make permission changes effective immediately; PostgreSQL row policies add defense in depth. [ADR 008](../architecture/adr/008-identity-implementation.md) records the design.

Operator bootstrap uses separate migration credentials. The recipient proves possession of an activation challenge and chooses a password, stored as bcrypt. Login checks credentials/membership and sets access/refresh cookies. Each request verifies JWT/session and current membership before transaction-local tenant context. Admin writes recheck authority inside an organization lock and compare revisions. A matching organization header is a stale-tab precondition, never authority.

Atomic refresh detects reuse and revokes the session family. Reset consumes the challenge and revokes all sessions. Exact Origin, cookie/header CSRF and session binding protect unsafe calls. Redis rate limiting fails closed. Successful actions and refresh replay append scoped audit records. No AI or business scoring is involved.

## How to use

Follow [IDENTITY-DEVELOPMENT](../IDENTITY-DEVELOPMENT.md) for complete setup, first-admin and mailbox commands. Run bootstrap then `docker compose up --build -d --wait`; open http://localhost:3000/login. `PPM_WEB_ORIGIN` must match exactly. Existing ports remain 3000/8000/15432/16379. On this host use the project Python and documented Docker path when absent from PATH.

Create the chosen local Admin through the operator guide and retrieve its private activation link. Admin invitations fix email/role/organization; existing verified recipients prove their current password. Activation/invitations expire after 24 hours, reset after 30 minutes. Recovery responses do not reveal account existence. Controls report validation, permission, expiry, stale-data and rate-limit failures.

## Implementation record

| Area | Files/behavior |
| --- | --- |
| Identity API | `identity.py`, `identity_schemas.py`: sessions/CSRF/account/invite/reset/member/audit |
| Persistence | `identity_tables.py`, `0002_identity.py`: seven tables, grants, composite references and RLS |
| Runtime | Config/env/bootstrap/Compose: random validated JWT key, configured browser origin |
| Web | Account/login routes, fixed same-origin proxy, shared typed transport, responsive CSS |
| Operators | `bootstrap_identity.py`, `local_mailbox.py`: first Admin and private delivery |
| Verification | Identity tests, isolated browser runner/fixture/Compose profile, updated CI |
| Dependencies | Locked bcrypt/PyJWT/email-validator; regenerated OpenAPI/types/license inventory |

Head `0002_identity` adds users, organizations, memberships, sessions, refresh hashes, challenges and identity audit. No domain backfill. The app role stays non-owner/non-super/non-bypass. Global credential lookup is a narrow auth control plane; organization/membership/audit use tenant RLS. Project permissions await project entities.

## Verification

[Acceptance evidence](../verification/SPRINT-02-CHECKS.md) links actual transcripts. **28 backend and 3 Chromium tests passed.** They cover roles, same-name tenants, forged/hidden IDs, RLS/pool reuse, live revocation, CSRF, expiry/replay, concurrent refresh/final-admin changes, existing-account invites, operator activation and reset. Migration lifecycle/drift passed. Browser tests verify cookies, real invitations/recovery and mobile layout; screenshots were reviewed.

Ruff, mypy, TypeScript, ESLint, Prettier and deterministic contracts pass. npm audit reported zero vulnerabilities. Container builds/start and worker/database/object restart checks pass; the original local checkpoint is unchanged. Hosted CI and external email were not run.

## Operations and remaining limits

Access lifetime 10 minutes; refresh fixed seven days. Cookies are Secure/HttpOnly/SameSiteStrict. Passwords require 12 characters and at most 72 UTF-8 bytes, bcrypt cost 12. Token digests are stored in PostgreSQL; raw links exist only in the private mailbox until operator cleanup. Logs exclude credentials/body/query tokens. Audit is scoped and append-only for the runtime role.

Strict refresh replay can require re-login after cross-tab races. Session list caps at 100; reset revokes all. Profile-name writes are last-write-wins; identity command exceptions are documented. Production remains disabled. Real mail, hosted CI, production key/edge/retention policy, full accessibility/penetration/load and Python vulnerability scanning remain unverified/later work. An inherited Starlette test-client warning is non-blocking.

Docker's stale sockets were recovered with preserved runtime-directory backups, without resetting volumes. No application acceptance failure remains. Future domain/file/search/worker surfaces need their own authorization tests.

## Next sprint readiness

Authenticated local runtime is ready for Sprint 03 design system/application shell. Read the [handoff](../handoffs/SPRINT-02-HANDOFF.md) before separately authorized work. This execution stops after Sprint 02.
