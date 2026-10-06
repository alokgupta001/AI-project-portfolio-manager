# ADR 011 — Local-date resource capacity and explicit workforce permissions

2026-10-06, accepted for the authorized local Sprint 05.

Use independent resource UUIDs with optional identity links; retain login-backed
team history. Add migration 0004 and extend the existing typed delivery commands,
shared organization lock, RLS and audit. Do not replace authentication or the UI shell.

Use immutable seven-day calendar versions, dated non-overlapping availability and
reporting-team periods, approved leave hours, additive project allocation hours and
explicit daily timesheet coverage. Scheduled local-date hours remain stable across
DST; timestamp shift accounting is not implied. Publish daily excess and reconcile
weekly totals, preserving unknown/zero-capacity cases.

Separate staffing authority from project edit and sensitive effort access. Even
Admin requires a resource effort grant. Restrict full-resource totals to proven full
scope (Admin); others receive partial authorized project hours without hidden totals.
Restrict resource archive to full scope. Require five resources on every date for
team support signals and complete authorized effort before overtime flags.

Persist immutable planning snapshots with recorded time, source revisions and calendar
versions. Future ML/simulations must enforce the recorded-time cutoff. Audit history
alone is not an implemented as-of reconstruction service. Snapshot SQL is append-only.

Reuse shared forms and source-driven tables/heatmaps without new dependencies. Initial
selectors are bounded and calculations are per resource, without a performance claim.
Atomic transfers, automated approval workflows, external timesheet ingestion, executive
dashboard and predictive workload analysis remain their later sprints.

See [capacity contract](../../contracts/capacity.md) for formulas, privacy and recovery.
