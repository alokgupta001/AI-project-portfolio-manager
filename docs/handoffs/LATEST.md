# Latest technical handoff

## Local database viewer — 10 October 2026

User-requested pgAdmin desktop viewer is running at <http://localhost:5050> with
the existing `ppm_local` connection preconfigured. See
[database viewer setup](../07-setup-and-deployment/DATABASE-VIEWER.md) and
`compose.database-viewer.yaml`. HTTP 200, viewer-to-database connection and browser
server/database list verified; 63 public tables, three organizations, zero project
rows. Existing web/API healthy; migration remains `0008_pilot_completion`.
Only the viewer was added; no application data or migrations were modified.
No Sprint 09 work was started. The local bootstrap secret is ignored under
`artifacts/local/`; preserve it and the existing `.env` and Docker data volumes.

**Sprint 8.1 implemented locally, acceptance OPEN**, 2026-10-09. Applied head `0008_pilot_completion`; preserved existing normal data. See [Sprint 8.1 handoff](../03-sprints/active/sprint-8.1/HANDOFF.md), [report](../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [pilot contracts](../contracts/pilot.md) and [user guide](../03-sprints/active/sprint-8.1/SPRINT_8_1_USER_GUIDE.md). Real SMTP delivery BLOCKED; hosted CI and regenerated DOCX layout UNVERIFIED. Stop before Sprint 09; no deployment authorization.

## Preserved Sprint 08 handoff history


**Sprint 08 complete locally**, verified 2026-10-09. Normal migration `0007_durable_jobs`; healthy local web/API 3000/8000, worker and dispatcher running. Branch `main`, base `90564405bcacc8389e34f3b06d8ab8d00984c5c1`; Sprint 08 changes remain uncommitted alongside preserved pre-existing work.

Read [Sprint 08 handoff](../03-sprints/completed/sprint-08/HANDOFF.md), [report](../03-sprints/completed/sprint-08/SPRINT_REPORT.md), [checks](../04-testing/sprint-based/sprint-08/TESTING_REPORT.md) and [jobs/integrations contract](../contracts/jobs-integrations.md).

Accepted: 63 full backend tests, 8 final focused job tests, 9 browser tests, static/source gates, normal migration/data/worker/restart preservation. Live Jira/GitHub credentials and sync remain unverified; fixture acceptance is explicit. All 54 established table hashes/counts unchanged. Applied head 0007 is frozen.

**Stop before Sprint 09**; it requires separate authorization. No AI/OCR/cloud deployment or production-readiness claim. Sprint 07 CI correction/history remains in [its handoff](../03-sprints/completed/sprint-07/HANDOFF.md).

## Subsequent verification and repair — 9 October 2026

See the [fresh Sprint 00–08 verification report](../04-testing/SPRINT_VERIFICATION_REPORT.md). Overlapping connector field paths are now rejected before persistence; regression tests cover both orders and the UI error/corrected import flow. Fresh results: 67 backend tests, nine existing browser scenarios and one enhanced focused browser scenario passed; seven direct SQL browser-record assertions passed. Normal service rebuild preserved all 60 current public tables and the original checkpoint. Live provider authentication remains blocked; overall end-to-end status is NOT VERIFIED for those implemented provider capabilities. Existing changes remain uncommitted and applied migrations were not edited.

## Planning-only audit and roadmap — 9 October 2026

Implementation baseline remains Sprint 08 / migration 0007. [Gap audit](../09-planning/SPRINT_8_1_GAP_AUDIT.md), [Sprint 8.1 plan](../09-planning/SPRINT_8_1_PLAN.md), [09–23 roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md), [traceability](../09-planning/FEATURE_GAP_TRACEABILITY.md) and [release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) are now the proposed future planning pack. 8.1 is not implemented or started; no application code, applied migrations or completed reports were changed by the planning task. Read current working tree before implementation. Frozen original prompts/specifications are preserved. Separate authorization is still required to implement the next sprint.
