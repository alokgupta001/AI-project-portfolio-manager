# ADR 002 Identity sessions and tenant isolation

Status: proposed baseline. Sources: S4.1 and master instruction. Decision date: 2026-10-05.

Use a global user identity with per-organization memberships and explicit project scopes. Short-lived JWT access credentials identify user/session/active organization. The server checks live membership/session validity for requests and streaming/delivery boundaries; role claims alone are not authority. Rotated refresh credentials are server-recorded and revocable. Cookie transport uses HttpOnly/Secure settings and a documented CSRF defense; same-origin deployment is preferred. bcrypt follows the source, with safe length validation and hash-version metadata.

The supplement's fully stateless implication is narrowed: signature verification may be stateless, but timely revocation requires state. Proposed access lifetime is 10 minutes and refresh lifetime 7 days, configurable; verify their operational suitability in Sprint 02. Membership or role changes invalidate cached policy decisions immediately through version checks.

Use application scoping plus PostgreSQL row policies with transaction-local tenant context and a non-owner, non-superuser, non-BYPASSRLS application role. Migration credentials are separate. Both read policies and insert/update checks are required. Tests must use the actual app role and reused pooled connections. Composite foreign keys prevent relationships that cross organization boundaries; sanitize referential errors to avoid exposing foreign object existence.

Why: row policies are defense in depth rather than a replacement for endpoint, project or object permissions. PostgreSQL documents default-deny behavior when RLS is enabled without applicable policy and notes that owners/superusers may bypass it. Reference: [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html), consulted 2026-10-05.

Consequence: every cache, worker, object URL, stream and search service needs policy enforcement. Admin is an organization role, not a platform superuser. WebAuthn comes in Sprint 22; no custom cryptography.
