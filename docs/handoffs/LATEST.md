# Latest technical handoff

**16 October documentation closeout:** [All previous-sprint documentation reconciled](../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md). Current Gemini $0 smoke and non-expiring confirmation are recorded; old blocked/planned statements are labeled historical. General model quality, CI/Word/production gates remain open. Sprint 11 is untouched and requires separate authorization.

16 October 2026: [Gemini $0 follow-up](../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md)
adds free-tier Gemini with user-confirmed no billing account, bounded real synthetic
smoke success and explicit source fallback. Read the
[operator guide](../07-setup-and-deployment/GEMINI-FREE-TIER.md) for the one-time
confirmation and request limits. The user subsequently requested removal of the
daily expiry; the existing verified key/project no longer needs renewal.
Full model-quality/production gates remain open.
The 15 October checkpoint below is retained historical evidence.

## Historical checkpoints

15 October 2026: Sprint 10 local implementation VERIFIED; overall acceptance OPEN (provider BLOCKED). Read
[Sprint 10 handoff](../03-sprints/active/sprint-10/HANDOFF.md),
[report](../03-sprints/active/sprint-10/SPRINT_REPORT.md) and
[testing/documentation closure](../04-testing/sprint-based/sprint-10/README.md).
Normal head **0012_ai_runtime** is applied following verified 0011. All 66 established
table hashes/counts, five original objects and frozen files preserved. Normal services,
worker round trip and scanner probe pass. Main base b98110e, all work uncommitted.
150 backend tests, 16 browser scenarios and 12 offline evaluation cases pass; static,
contracts/audits pass. Private backups remain ignored; exact checkpoint is linked in
the handoff. Preserve all now-applied 0001â€“0012, .env, grants/privacy and prior work.

User explicitly authorizes only mocks/fallback: real-provider acceptance BLOCKED,
no paid calls or charges. Stop before 11. Earlier Word visual, hosted CI and
production/release gates stay open. Dated history below retains its actual scope.

# Preserved technical handoff history

15 October 2026 documentation follow-up: the [Sprint 09 hub](../03-sprints/completed/sprint-09/README.md)
now links current learning, user/demo/operator guides, source inventories, tests and
bugs/fixes. [Documentation closure](../04-testing/sprint-based/sprint-09/DOCUMENTATION_CHECKS.md)
records checks and remaining gates; status/catalogue/tracker/mapping are reconciled.
Normal head remains `0011_document_sources`; all work remains uncommitted. Earlier
Word visual/hosted CI gates stay open. **Stop before Sprint 10.**

## Sprint 09 complete locally â€” 15 October 2026

Current normal head **0011_document_sources**, following the actual 0010 baseline.
See [Sprint 09 handoff](../03-sprints/completed/sprint-09/HANDOFF.md),
[report](../03-sprints/completed/sprint-09/SPRINT_REPORT.md),
[checks](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md) and
[source contract](../contracts/documents.md). Library, safe extraction/OCR, scoped
keyword/citations/downloads, assessment references, policy/hold/retention/purge and
scratch recovery are accepted locally. Semantic/hybrid interfaces remain pending 10/11.

Fresh quiesced rollout preserved all 62 established table counts/hashes, five original
object hashes and ten applied migration files; a refresh-token row added before the
upgrade was retained. Existing .env, volumes, pgAdmin and prior work remain. Normal
web/API/worker/dispatcher/scanner are healthy. Changes remain uncommitted on main at
base b98110e; no push or cloud deployment. Full backend 123 passed, focused 24 plus
final security 9 passed, 14 browser regressions plus final source journey passed.

**Stop before Sprint 10.** Earlier 8.1 hosted-CI/Word-layout and production release
gates are not closed. The dated entries below are preserved historical checkpoints.


## Local database viewer â€” 10 October 2026

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

## Subsequent verification and repair â€” 9 October 2026

See the [fresh Sprint 00â€“08 verification report](../04-testing/SPRINT_VERIFICATION_REPORT.md). Overlapping connector field paths are now rejected before persistence; regression tests cover both orders and the UI error/corrected import flow. Fresh results: 67 backend tests, nine existing browser scenarios and one enhanced focused browser scenario passed; seven direct SQL browser-record assertions passed. Normal service rebuild preserved all 60 current public tables and the original checkpoint. Live provider authentication remains blocked; overall end-to-end status is NOT VERIFIED for those implemented provider capabilities. Existing changes remain uncommitted and applied migrations were not edited.

## Planning-only audit and roadmap â€” 9 October 2026

Implementation baseline remains Sprint 08 / migration 0007. [Gap audit](../09-planning/SPRINT_8_1_GAP_AUDIT.md), [Sprint 8.1 plan](../09-planning/SPRINT_8_1_PLAN.md), [09â€“23 roadmap](../09-planning/FUTURE_SPRINT_ROADMAP.md), [traceability](../09-planning/FEATURE_GAP_TRACEABILITY.md) and [release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) are now the proposed future planning pack. 8.1 is not implemented or started; no application code, applied migrations or completed reports were changed by the planning task. Read current working tree before implementation. Frozen original prompts/specifications are preserved. Separate authorization is still required to implement the next sprint.

## Sprint 09 folder correction â€” 15 October 2026

Canonical Sprint 09 documents now live in
[completed/sprint-09](../03-sprints/completed/sprint-09/README.md).
The misleading planned compatibility stub and empty folder were removed; no second
active copy remains. Internal Markdown links and documentation validation now use
the completed location. Local acceptance limits and open CI/Word/release gates are
unchanged. No application, data or migration change; stop before Sprint 10.
