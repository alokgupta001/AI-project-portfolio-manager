# ADR 008 Local identity and authorization implementation

Date: 2026-10-05. Scope: Sprint 02 local implementation of ADR 002. Acceptance status is recorded separately in the Sprint 02 report.

## Identity and tenant boundary

Global user identities are verified through a one-use activation/invitation challenge delivered to a private local mailbox. An explicit operator command using migration credentials creates organizations and the first pending Admin. There is no anonymous organization or Admin creation route. Email identifiers are normalized to lowercase; display names and organization names are not unique identifiers.

Organizations, memberships and identity audit records are tenant-owned. PostgreSQL RLS restricts their reads and writes for `ppm_app`. A verified session resolves the user and active membership before the server sets transaction-local `ppm.user_id`, `ppm.organization_id` and `ppm.role`. Pool commit/rollback clears these settings. A user's own memberships may be read across organizations for the validated switcher. Other membership and audit reads are limited to the selected organization; membership management additionally requires a live Admin role. Composite foreign keys bind sessions, invitation issuers and audit actors to the matching organization membership.

The global identity control plane (`identity_users`, `identity_sessions`, hashed refresh tokens and hashed challenges) deliberately supports unauthenticated login/challenge lookup. It does not use tenant RLS: its operations are narrow server-owned code paths, with explicit user/session/token predicates and no public listing routes. Possession of a valid invitation is authority to accept only its recorded organization/role; the inviter must still be an active Admin. Existing verified identities must also prove their current password. Invitations cannot overwrite or reactivate an existing membership. No user-supplied organization header becomes authority.

The runtime remains a non-owner, non-superuser, non-BYPASSRLS role. Migration/fixture tooling uses separate owner credentials. Organization membership changes are serialized with a transaction advisory lock keyed by organization; role/revision and final active Admin count are rechecked inside that lock. Requests read current membership every time, so role changes apply without waiting for JWT expiry. Removal revokes matching sessions. Project/portfolio grants remain specified in the permission matrix and will be enforced when those entities arrive; none is implied by a PM role today.

## Credentials and browser transport

Use bcrypt 5.0.0, cost 12, with a minimum of 12 characters for new passwords and an explicit maximum of 72 UTF-8 bytes. No silent truncation. Work runs off the async event loop. Stored hashes include their algorithm/cost prefix. PyJWT 2.15.0 pins HS256 verification, issuer `enterprise-ppm`, audience `ppm-web`, and mandatory subject/session/organization/expiry/issued-at/JTI claims. The signing key is randomly generated in ignored `.env`; startup rejects keys shorter than 32 bytes.

Access tokens last ten minutes. Sessions have a fixed seven-day expiry and hashed refresh credentials. Atomic refresh rotation keeps consumed hashes to detect replay. A replay revokes the session family and commits that revocation before returning 401. Concurrent refresh requests using one token yield one success and one rejection; the session is then revoked. This strict replay policy intentionally requires sign-in again after independent tabs race; it does not introduce a replay grace window. The web client coalesces refresh within a page.

Access/refresh cookies are host-only, Secure, HttpOnly, SameSite=Strict, Path=/; tokens are never put in localStorage. The readable CSRF cookie is compared to a custom header; authenticated unsafe requests additionally bind its hash to the server session. Every unsafe request also requires exact configured Origin. No CORS origins are enabled. A fixed same-origin Next.js proxy forwards only allowlisted headers to the configured internal API; it never trusts a browser-supplied upstream URL. Local browser use is through `http://localhost:3000` (Chromium's secure loopback handling); other deployments require HTTPS and are still disabled by environment validation. `PPM_WEB_ORIGIN` must match the actual browser origin. Referrer policy is no-referrer, and mailbox links carry secrets in URL fragments, removed on page load.

Redis provides atomic ten-minute rate windows: ten login attempts per email, 100 per direct network peer, three reset requests per email, 30 reset/completion attempts per peer and 20 invitations per actor. Behind the local proxy, the peer budget is shared; forwarded IP headers are not trusted. Limiter failure rejects the action. Public login/reset failures do not reveal whether an email exists in response content. Production distributed edge rate policy and latency/load measurement remain later work.

## Challenges, audit and local delivery

Reset tokens expire in 30 minutes; activation/invitation tokens in 24 hours. Random secrets are stored as SHA256 digests in PostgreSQL. Successful activation/reset consumes related activation/reset challenges, changes the bcrypt hash and revokes all the user's sessions. Local mailbox JSON contains the deliverable link, analogous to an email inbox; it is operator-only, under the named object volume, with directory mode 0700/files 0600. No mailbox HTTP endpoint or external email service exists. Tokens are not included in audit or request logs. Spool files remain locally until the operator removes them; expiry prevents reuse, but automatic retention cleanup is not claimed.

Successful login/logout/revocation, organization switching, profile/membership changes, invitations and challenge completion append tenant audit events with actor, action, target, UTC time and request UUID. Refresh replay is also audited. Runtime privileges permit append/read, not audit update/delete. Failed unauthenticated logins are represented by sanitized operational status logs rather than a fabricated tenant audit context. This is not the later enterprise audit console or notification platform.

## Compatibility and local exceptions

Unsafe membership routes also require `X-Organization-ID` to match the server-resolved session organization. A mismatch returns 409; this is a stale-tab precondition, never tenant authority. The browser sends the organization whose data it last loaded. Automatic token refresh cannot silently turn a stale membership edit into a write in a newly selected organization.

Migration `0001_foundation` is preserved. `0002_identity` adds seven tables and RLS policies; no enterprise domain table or backfill is added. Readiness and generated foundation metadata now expect this head. Backend OpenAPI remains the source for frontend types.

Membership updates require `If-Match` with the returned integer revision (428 missing, 412 stale, 409 final-admin conflict). Member/audit lists use bounded UUID cursor pagination. Personal session listing is limited to the most recent 100 active sessions; password recovery revokes all sessions. Self profile-name updates use last-write-wins, a documented exception to shared-resource revisioning. Login/refresh/challenge completion use credential semantics rather than generic idempotency keys. Repeated invitation creation deliberately creates a new delivery challenge; acceptance remains single-use and cannot create duplicate membership. No future business command should infer idempotency support from these identity routes.

## References checked during implementation

- [PyJWT API verification rules](https://pyjwt.readthedocs.io/en/stable/api.html): fixed algorithms and registered claim validation.
- [bcrypt maintainer package documentation](https://pypi.org/project/bcrypt/): maintained implementation and 72-byte limit.
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html): non-owner application role and default-deny policy behavior.
