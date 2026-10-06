# Delivery system of record — Sprint 04

Implemented 2026-10-06. Migration `0003_delivery`; API prefix `/api/v1/delivery`; generated OpenAPI and TypeScript in `packages/contracts`. These DTOs are the supported input to future dashboards. No computed health, resource capacity, ingestion or AI module is implemented.

## Authority and relationships

PostgreSQL owns 19 typed resources: organization settings, departments, teams, dated team memberships, goals, portfolios, programs, projects, scoped grants, sprints, work items, milestones, blockers, dependencies, budget lines, expenditure, status updates, baselines and goal alignments. Separate audit and idempotency tables preserve write evidence. `ppm_tables.py` owns current metadata; migration 0003 freezes its initial schema. Migrations 0001 and 0002 are unchanged.

Organization → portfolio → optional program → project. A direct portfolio project needs no program. A program-linked project's program must belong to the same portfolio. Departments, teams and active member owners are optional project references. Team memberships are dated, non-overlapping half-open ranges; a login identity is not yet a Sprint 05 resource profile. Project children and typed dependency endpoints use composite organization/project references. All records carry organization, UUID, revision, archive flag and timestamps. No hard-delete API exists.

Dependencies point predecessor → successor. Self-edges and cycles are rejected at typed-node and cross-project levels. Both endpoints must be visible, active and writable. Cross-project dependency mutations are Admin-only so cycle validation cannot miss a hidden edge; scoped PMs may maintain intra-project dependencies. Archiving a referenced parent is blocked while active dependents exist. Archiving a project preserves its children/history and makes child writes unavailable until restore.

## Authorization and writes

Existing secure cookies, live session/membership checks, exact-origin CSRF and transaction-local RLS remain mandatory. The application role is neither owner, superuser nor BYPASSRLS. All lists, counts, lookups and totals use the caller's organization and project scope; hidden IDs return 404. Owners do not automatically gain access.

Admin manages organization metadata and all project scopes. PM/Viewer reads require a project or portfolio grant. A portfolio read/edit grant does not imply project write access. PM project edit/manage grants allow project content edits; archive requires manage. PM portfolio manage permits project creation with an atomic own-project manage grant. Only Admin manages other users' grants or transfers projects. Viewer cannot mutate. Organization members may read shared organization metadata and a minimal active-member name/ID selector; membership secrets/emails are not exposed by that selector. Audit reads are organization-wide for Admin, otherwise limited to the actor's own changes on visible targets.

Writes share the organization advisory lock with membership changes, recheck membership/session, and require `X-Organization-ID`. POST requires a UUID `Idempotency-Key`: equal retries reuse the same target; changed payload returns 409. PATCH accepts the complete typed writable record plus integer `If-Match`; missing precondition is 428, stale revision 412. Read-only fields and unknown input keys are rejected. Constraint failures are sanitized. Audit before/after, mutation and receipt commit together.

Project/work/sprint transitions are validated. Reopening completed/cancelled projects or done work requires `X-Change-Reason`; project reopening creates a new baseline. Baselines, expenditure and status updates are append-only at API and application SQL privilege levels. Expense corrections use one exact negative reversal referencing the original entry. Status updates also revise the project's separately reported health. Baselines capture versioned project/work/milestone/sprint/budget data and calendar settings; later forecasts do not rewrite earlier snapshots. Decimal snapshot values remain strings.

## Consumer API and metric rules

- GET `/{kind}`: name search, archived flag, project/portfolio/status filters, name/updated ordering, offset/limit (maximum 100), scoped total and `as_of`.
- GET `/{kind}/{id}`; POST `/{kind}`; PATCH `/{kind}/{id}` use the discriminated typed resource union in generated contracts.
- GET `/people?q=` returns up to 100 matching active member IDs/names.
- GET `/history/{kind}/{id}` returns the latest 100 visible audit changes.
- GET `/project-summary/{id}` returns project, write/manage capabilities, work counts, money, alignment completeness, baseline history and `as_of`, version `delivery-v1`.
- GET `/portfolio-summary/{id}` aggregates authorized active projects, keeps each currency separate and reports visible project count and freshness. It does not imply coverage of hidden projects.

Money uses Decimal/NUMERIC(18,2), never binary float aggregation. Currency is a three-uppercase-letter code, consistent within a project; no FX conversion or currency catalogue validation. Approved budget sums active approved lines. Recorded spend sums immutable expenditure including reversals. Usage = 100 × spend / approved budget, rounded to two decimals, only when budget is nonzero and ledger completeness is explicitly true; otherwise unknown. Portfolio totals retain this completeness rule per currency.

Alignment is 100 × sum(weight × contribution), with each fraction in [0,1], only when active weights total exactly 1; otherwise explicitly incomplete/unknown. Partially configured weights may be saved. Computed health stays null; human reported health is separately labeled. Dates are ISO calendar dates; organization timezone is validated IANA. Baselines include calendar configuration/version. Timeline bars show calendar dates, not business-day schedule variance. Working calendars/holidays and dashboard rule engines belong to later sprints.

## UI scope

Shared Sprint 03 shell, modal, confirmation, field, metric and table primitives power `/organization`, `/portfolios`, `/projects` and `/projects/{id}`. Admin configures the organization timezone/currency first, then hierarchy and grants. Reference selectors search authorized records. Project overview exposes work, milestones, blockers, named dependency edges, budget/spend, alignment, status and immutable plan history. Lists use server pagination; work board shows its current page. Timeline explicitly shows the current milestone page and first 100 work items with an equivalent date table. It is an initial editable delivery workspace, not a drag-and-drop scheduler or complete portfolio dashboard.
