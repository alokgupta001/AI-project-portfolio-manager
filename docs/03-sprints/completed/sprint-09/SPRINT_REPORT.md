# Sprint 09 implementation report

> Historical sprint checkpoint — documentation review, 16 October 2026. The original outcomes, schema/version and stop-at-next-sprint statements below describe their recorded date. For today's availability and safe setup, use [current status](../../../00-overview/CURRENT_STATUS.md) and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

## Status and scope

15 October 2026. **Complete locally for the revised Sprint 09 scope.** Sprint 09 only;
Sprint 10 has not started. Base: clean `main` at `b98110e`, already containing prior
Sprint 08/8.1 work. This sprint remains uncommitted; no reset, clean, commit, push,
cloud deployment or real notification occurred. Actual starting head was
`0010_account_authority`, superseding historical handoff references to 0008.

Read MASTER/LATEST/8.1 handoff/report, revised 8.1 planning pack and Sprint 09 ordered
section, frozen original Sprint 09 prompt, requirements/coverage, permissions,
API/events/pilot/assessment/jobs/frontend contracts and release criteria. Current user
authorization permits 09 without closing earlier parent 8.1 CI/Word-layout gates.

Scope: PPM-09-001/002/003; Word module 5 / source F-065–074. The revised roadmap stages
keyword/source contracts in 09, budgeted embeddings/hybrid in 10 and reviewed semantic
findings in 11. Original combined semantic requirements remain partial.

## What and why

`/documents` supplies persistent categorized uploads, versions, processing status,
paged escaped previews, source locations, keyword search, revalidated citations,
verified-original downloads, assessment references and policy/retention controls.
SRS/BRD/PRD/MOM/sprint report/risk log/charter/policy are separate categories. Supported
formats: PDF/scanned PDF, DOCX tables, UTF-8 text, CSV/XLSX and PNG/JPEG. This establishes
reusable trustworthy evidence before intelligence consumes it.

Admin manages organization policies and authorized project sources. PM needs explicit
project edit/manage; Viewer reads only scoped project sources and shared organization
policies. Ownership grants nothing. Existing workforce privacy, private assessment
evidence, results, metrics, grants and identity stay authoritative. See
[ADR 015](../../../architecture/adr/015-document-sources.md) and
[contract](../../../contracts/documents.md).

## How it works

The existing cookie/CSRF/organization transport resolves live authority. Bounded
upload stores immutable hashed bytes, then commits version/job/audit/event/outbox
together. Replays recheck access; duplicate bytes within a document return the old
version. Shared edits use revision guards. Existing Celery dispatch handles document
jobs with persisted actor/session, fenced leases and authority checks before claim
and publication. Forged tenant/actor tuples cannot cancel a valid document job.

ClamAV must accept bytes before a bounded child process extracts text. Missing
scanner/OCR, active/corrupt/unsupported content and limits fail closed, with no manual
antivirus bypass. Digital confidence stays unknown; OCR confidence measures recognized
words, not factual accuracy. Reprocessing replaces derived chunks atomically.
PostgreSQL keyword ranking applies RLS before results and activates only the latest
ready version. Citations recheck permission/version/tombstone. A 60-second ticket binds
user/session/tenant/version/hash; downloads still authenticate and verify SHA-256.
Untrusted source text cannot issue commands or mutate delivery data.

Admin registers policy owner/applicability/source version/state/effective/review dates
(UTC calendar labels; workflow approval is pending 15). Pilot retention defaults to
30 days with explicit holds. Delete closes source access immediately. Purge requires
expiration and no hold, deletes bytes/chunks/links, and preserves metadata tombstones.
Orphan cleanup includes references/holds on hidden archived projects. Assessment
links require identical released bytes and both private-evidence and document authority;
saved scores/answers/coverage/history remain unchanged.

## Use and implementation

Follow [USER_GUIDE.md](USER_GUIDE.md). Start local scanner/app with
`docker compose -f compose.yaml -f compose.documents.yaml up -d --build`, wait for
signatures/health, and open Document library. No normal demo records are seeded.
The scanner has no host port or original-object mount. Without its override, intake
remains quarantined. Configuration names: PPM_DOCUMENT_SCANNER_HOST/PORT; existing
secrets and `.env` are retained.

New migration `0011_document_sources` adds four tenant source tables and an exclusive
integration/document-version reference in durable_jobs. It expands without backfill
or contract removal. Applied 0001–0010 remain unchanged. The application role cannot
change version byte identity or hard-delete source/version rows. Narrow fixed-path
functions resolve worker authority, complete retention references and guarded purge.
New API/parser/retrieval DTOs, library UI, shell/account registration, assessment
reference display, generated OpenAPI/types, scanner override, runtime lock and tests
form the slice. Candidate/embedding types are interfaces only, with no provider,
vector index or semantic findings enabled.

pypdf is pinned to **6.20.1** after audit found vulnerabilities in the initial 6.12.0
choice. Image builds enforce exact Poppler/Tesseract versions against
`infra/document-packages.lock`; dependency/license metadata is recorded. CI adds
Python vulnerability auditing and excludes private artifacts/local backups from
artifact uploads. Hosted CI remains unverified.

## Verification

Docker Linux/PostgreSQL 18/Redis 8/Python 3.12/Node 24, real non-bypass ppm_app role.
Backend mutations/lifecycle use guarded ppm_test; browser uses independent volumes
and 3001/8001. Normal is 3000/8000.

| Gate | Actual result / evidence |
| --- | --- |
| Full backend/lifecycle | **123 passed**, inherited Starlette/httpx warning, 320.63 s. Clean base, prior-head upgrades, downgrade/re-upgrade and drift. [Log](../../../verification/sprint09-backend-final.txt). |
| Format/source closure | **24 passed**, 117.84 s: nine API and fifteen parser cases; actual scanned PDF/PNG/JPEG OCR, real ClamAV clean/EICAR, 125 metadata rows, concurrent replay. [Log](../../../verification/sprint09-documents-final.txt). |
| Final security | **9 passed**, 52.04 s: forged worker tuples, SQL immutability/delete denial, revoked scope, held archived-project orphan protection, scanner recovery, two tenants/three roles, private assessment bridge, ticket expiry/integrity. [Log](../../../verification/sprint09-security-accepted.txt). |
| Final migration | 0010 → 0011 and drift passed. [Log](../../../verification/sprint09-migration-accepted.txt). |
| Retrieval fixtures | Eight categories / eight labeled queries: **8/8 top-1 expected source/location matches**. Synthetic distinct-keyword baseline, not semantic/production accuracy. See named evaluation in test_documents.py. |
| Browser | **14 prior scenarios passed** in full run; new flow exposed a stale save/reopen race, repaired by disabling selection during pending saves. Final affected flow: PASS: final document journey, 1 passed in 34.4 s (sprint09-browser-accepted.txt). [Full run](../../../verification/sprint09-browser-all.txt). |
| Accessibility/visual | 1440/768/360 automated WCAG-tag and body-overflow checks; visual review caught compressed mobile columns, fixed with a focusable horizontal region/minimum table width. Final UI evidence: PASS: final document journey, 1 passed in 34.4 s (sprint09-browser-accepted.txt). |
| Static/contracts | Ruff/format, mypy (36 modules), TS, ESLint, Prettier, OpenAPI/types and seven preserved source/prompt hashes; final checkpoint in [checks](../../../04-testing/sprint-based/sprint-09/TESTING_REPORT.md). |
| Vulnerabilities | npm zero; locked Python set no known vulnerabilities after parser upgrade. [npm](../../../verification/sprint09-npm-audit.txt), [Python](../../../verification/sprint09-python-audit-final.txt). No comprehensive OS/security certification claim. |
| Existing-data recovery | ppm_sprint09_restore: **62 table counts/hashes and five object hashes matched**, original head 0010. [Log](../../../verification/sprint09-recovery-normal.txt). |
| Document fixture recovery | ppm_sprint09_documents_restore: **67 table counts/hashes and one synthetic fixture object matched**; authenticated signed original and keyword citation passed. Other ephemeral test objects are outside this fixture file manifest. [Log](../../../verification/sprint09-recovery-documents.txt). |
| Normal preservation | PASS: head 0011_document_sources applied; healthy restart/worker; 62 quiesced table hashes/counts, five object hashes and ten frozen migrations preserved. One refresh-token row was added while the old stack was live, before migration. It is retained in the fresh quiesced rollout checkpoint; initial backups/manifests are also preserved. |

Failed/intermediate runs remain recorded. The first full run had 122 passes and a
worker timing failure; another retry reached attempt 2 but exceeded the harness wait.
Waits were bounded at 180 iterations (startup 1,500 short polls) without shortening
the real 45-second lease or removing crash/restart/attempt-2/500-unique-effect checks.
The full rerun passed. Windows sandbox temp/path and wrapper failures were isolated
using a workspace temp directory, Python modules and supported Linux execution.
Initial browser selector/race failures are not claimed as passes.

## Operations, limitations and next sprint

Logs contain fixed stages/routes/request IDs, not source bodies or secrets. Parsing,
uploads, jobs and retries are bounded. Private backups, tokens and object archives
remain ignored. No normal restore/purge is performed. Restore an archived project
before library management; its files/holds remain protected from orphan cleanup.

Open release gates: hosted CI at reviewed revision, earlier Word layout QA, production
storage/retention/backup-erasure policy, performance/availability measurement and cloud
deployment. Parent 8.1 acceptance remains open. No full-product RAG, semantic findings,
predictive accuracy or production-readiness claim.

The source/keyword/retention interfaces enable later work. Read [handoff](HANDOFF.md)
and coverage before continuation. **Stop before Sprint 10**; it needs separate
authorization and provider/budget decisions. No next sprint is started by this report.


Final boundary closure: a source that expands beyond 5,000 location chunks is rejected rather than marked ready with inaccessible tail text. The focused boundary test passed (sprint09-chunk-limit.txt); the same pinned runtime was rebuilt/restarted healthy. Thirteen fresh regression renders were saved under Sprint 09 names and earlier committed evidence restored. The [local checkpoint](../../../verification/sprint09-checkpoint.json) records file hashes, not hosted CI.

## Documentation follow-up — 15 October 2026

The first closeout omitted required updates to current learning/user/demo/operator
guides, inventories, status/catalogue, navigation, feature mapping and tracker. Those
Markdown omissions are now reconciled. [Documentation closure](../../../04-testing/sprint-based/sprint-09/DOCUMENTATION_CHECKS.md)
records affected canonical paths, actual checks and retained Word/CI/release gates.
Application acceptance above remains its recorded run; this follow-up does not rerun
or infer new application tests. Work remains uncommitted. Stop before Sprint 10.
