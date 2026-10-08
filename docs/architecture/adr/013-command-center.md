# ADR 013 — Shared deterministic command-center snapshots

2026-10-07. Accepted within user-authorized Sprint 07.

Reuse delivery CRUD/audit/RLS and capacity-v1. Add six typed tables in additive
0006; preserve frozen applied migrations and assessment results. Use one typed
snapshot endpoint for all dashboards and JSON DTO download, with shared Decimal
money/alignment helpers also used by existing delivery summaries. Acquire the
organization transaction lock so related source reads cannot straddle mutations.
This favors consistency at local MVP scale; measured query cost is a baseline,
not a production throughput claim. Bound sources and reject oversized snapshots.

Freeze completed points when a sprint closes; do not recalculate old velocity
from mutable tasks or invent snapshots for pre-existing closed sprints. Select an
explicit immutable baseline/calendar for schedule metrics. Keep current-state
health and selected-period activity clearly distinct. Conservative source age,
missing inputs and scope limitations are part of each DTO.

Preserve identity and sensitive capacity grants. Personal views are actor-owned,
including Viewer-owned filters. A downloaded dashboard DTO is reauthorized as the
same scoped read; no scheduled report, recipient, provider or external send exists.
Broader reporting/export grant policy remains Sprint 21 work.

Reuse native chart bars with accessible tables, existing modal drawer and record
editor; introduce no chart dependency. JSON download avoids CSV formula handling
and keeps typed evidence, rule and freshness metadata intact. Full contract:
[command center](../../contracts/command-center.md).
