# Identity tenant and permission contract

Sprint 05 implements [resource permissions](capacity.md): resource-level manager
capabilities plus project edit for allocations; explicit effort grants even for
Admin; Viewer read-only; sensitive record/audit revocation enforced by RLS. Only
Admin publishes full-resource totals or archives resources. Scoped views are partial.

Sprint 04 adds project/portfolio grants and delivery RLS: [implemented authorization](delivery.md). Owners do not imply access. Cross-project dependency mutations require Admin; PM intra-project writes need explicit edit/manage scope. Existing session, CSRF and organization controls are retained.

Sprint 02 implementation checkpoint: local account/session controls and organization membership authorization are implemented. The broader matrix below still defines later domain behavior. See [ADR 008](../architecture/adr/008-identity-implementation.md) and [Sprint 02 checks](../verification/SPRINT-02-CHECKS.md).

| Implemented operation | Admin | Project Manager | Viewer |
| --- | --- | --- | --- |
| Own profile, password recovery, own sessions/logout | Yes | Yes | Yes |
| Switch to another active membership | Yes | Yes | Yes |
| List members, invite, change role or active state | Yes, selected organization only | Denied | Denied |
| Read organization identity audit | Yes, selected organization only | Denied | Denied |
| Remove/demote final active Admin | Denied | Denied | Denied |

Every authenticated operation rechecks the server session and live active membership. `X-Organization-ID` on unsafe organization routes is a required matching precondition against stale tabs, not authority; a mismatch returns 409. Member edits also require the returned revision in `If-Match`. Organization locking serializes final-admin checks. PM/Viewer account access does not imply project access; future projects need explicit scope.

Access JWTs last ten minutes; rotated refresh sessions have a fixed seven-day expiry. Replayed refresh tokens revoke the session, including concurrent reuse. Browser cookies are Secure/HttpOnly/SameSite=Strict on the configured localhost origin. Unsafe requests require exact Origin plus a CSRF header/cookie and, when authenticated, session-bound CSRF hash. Removed memberships fail immediately and revoke matching sessions; role changes are live without trusting JWT role claims.

Activation/invitation lasts 24 hours, recovery 30 minutes, all single-use. Reset revokes all sessions. Global identity credential tables are deliberately outside tenant RLS; tenant organization/membership/audit tables use transaction-local policies with the restricted application role. Composite references bind organization/member relationships. Actual negative checks cover two same-name organizations, all roles, forged/hidden IDs, stale revisions, RLS read/write/pool cleanup, replay/expiry, CSRF, reset and concurrent final-admin changes. SSE/download/vector/graph/queued notification surfaces are not implemented and retain their future tests below.

Version 0.1, proposed baseline for Sprint 02. Deny by default. All roles require an active organization membership; no organization role grants access to another organization. Admin can administer all project scopes in its organization. PM and Viewer require explicit project or portfolio read grants; portfolio read grants include its projects but do not grant project writes. A PM's project edit grant does not grant organization settings or staffing allocation authority across unrelated projects.

## Role matrix

`Scoped` means the role plus an explicit relevant scope/assignment is required. `Assigned` means a named workflow/assessment responsibility plus eligible role; it does not bypass data scope. A denied endpoint returns the standard forbidden/not-found behavior without leaking hidden records.

| Action | Admin | Project Manager | Viewer |
| --- | --- | --- | --- |
| Read own profile/manage own credentials | Yes | Yes | Yes |
| Change organization membership/roles/integrations | Yes | No | No |
| Read portfolio/project dashboards | Organization-wide | Scoped | Scoped |
| Create portfolio/program and organization goals | Yes | No | No |
| Create project in portfolio | Yes | Explicit portfolio manage grant | No |
| Edit project/work/baseline/budget | Yes | Project edit grant | No |
| Archive project | Yes | Project manage grant | No |
| Manage resource profiles/calendar | Yes | Explicit resource manager scope | No |
| View sensitive effort or raw workforce notes | Restricted data grant | Restricted data grant | No |
| Change allocation | Yes | Resource manager scope plus edit access to every affected project | No |
| Create/publish assessment frameworks and policies | Yes | Draft only with delegated framework editor grant | No |
| Answer assessment | Assigned | Assigned | No |
| Review/approve assessment | Assigned; no own sensitive submission | Assigned; no own sensitive submission | No |
| Read assessment results | Organization-wide except restricted evidence | Scoped | Explicit result read grant |
| Upload/manage documents and recordings | Scoped by restricted content policy | Project edit or assigned assessment scope | No |
| Read evidence/files | Scope plus content classification | Scope plus content classification | Scope plus content classification |
| Ask copilot/use natural language analytics | Scoped | Scoped | Scoped read-only |
| Start costly analyses | Yes subject to budget | Scoped with analysis grant | No; may read existing answers/results |
| Propose risk/recommendation/roadmap/scenario | Yes | Scoped | No |
| Approve sensitive changes | Assigned eligible approver, not proposer | Assigned eligible approver, not proposer | No |
| Apply approved changes | Authorized system command, current permission recheck | Same through approved workflow | No |
| Export reports | Scoped with export grant | Scoped with export grant | Scoped with export grant |
| Configure external recipients/Slack/email | Yes | No | No |
| Manage own briefing preferences | Within authorized destinations | Within authorized destinations | Within authorized destinations |
| Read audit and AI usage console | Admin; sensitive fields restricted | Own scoped activity only | No |

The grants above are capabilities attached to membership/project/assignment, not extra global role names. Implement one policy service with explicit action and resource scope. Resource transfers require rights to the source and destination; hidden project names must not appear in failure responses. Admin cannot read every classified document merely because it can manage settings; restricted-data access is explicit and audited.

## Session and tenant rules

- Login establishes user identity. Organization selection validates active membership and issues a tenant-bound context; a user-supplied header/body organization ID is only a selector, never authority.
- Every scoped request, worker operation and download verifies active membership, current role/grants and session validity. Removal/revocation increments policy version and invalidates caches.
- Proposed access JWT lifetime 10 minutes; refresh lifetime 7 days. Refresh rotation is atomic with replay detection and family revocation. Actual settings validated in Sprint 02.
- Browser credentials use Secure HttpOnly cookies with SameSite policy plus CSRF tokens/origin validation on unsafe methods. Restrict CORS to configured origins; do not log cookies or bearer tokens.
- Invitation/reset/challenge tokens expire, are single-use and stored hashed where appropriate. Return non-enumerating public errors. Password input must not be silently truncated by bcrypt's byte limit.

## Enforcement across data surfaces

Database: RLS transaction context plus application policies; composite foreign keys. Object downloads: short-lived signed links only after permission check, with expiry documented (proposed max 60 s); immediate revocation of already-issued direct links is not promised, so especially sensitive downloads should be proxied. Vector retrieval: scope filter before candidate retrieval and citation recheck. Neo4j: server-owned parameterized query templates and tenant/project constraints. Cache keys: tenant, user/policy scope version and input version. SSE: authorize subscription and recheck on policy change, never cross-run topic guessing. Reports/notifications: verify every recipient at generation and delivery, avoid protected details in public channel messages. Workers: tenant context plus initiating/service authority and current action policy.

## Mandatory negative fixtures

Two tenants with overlapping project/resource names; one user in both with different roles; Viewer attempting writes; PM editing another project; forged tenant selector; revoked membership during SSE/download/queued send; copied foreign document/vector/graph identifiers; application-role database connection reused across tenants. Each new surface adds equivalent fixtures to its sprint evidence.

## Sprint 06 implemented assessment scope

Named respondent/reviewer assignments are explicit assessment scope and require an active Admin or Project Manager role. Admins cannot answer or approve merely by virtue of their role; the actual actor must match the assignment and reviewers cannot approve their own submission. Admins can delegate editing of a particular framework draft to a PM (publication remains Admin-only) and grant reads of completed results. Result-only grants never expose private answers, events or evidence. Evidence release requires the independent reviewer and a reason. All new tables use the existing `ppm.*` transaction context and real non-bypass application role. See [assessment contract](assessment.md), ADR 012 and Sprint 06 checks.

## Sprint 07 command-center scope

Dashboard/JSON DTO reads use live delivery project RLS; risk/benefit/plan writes require Admin or project edit grants. Policy writes are Admin-only. Personal saved views are actor-owned even for Admin and Viewer; they confer no access. Resource privacy/grants remain unchanged. [Contract](command-center.md).
