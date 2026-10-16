# Sprint 09 technical handoff

> Historical sprint checkpoint — documentation review, 16 October 2026. The original outcomes, schema/version and stop-at-next-sprint statements below describe their recorded date. For today's availability and safe setup, use [current status](../../../00-overview/CURRENT_STATUS.md) and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

15 October 2026. **Complete locally; normal head 0011_document_sources applied**. Read [report](SPRINT_REPORT.md),
[checks](../../../04-testing/sprint-based/sprint-09/TESTING_REPORT.md), [user guide](USER_GUIDE.md),
[source contract](../../../contracts/documents.md), permissions/assessment/jobs/pilot
contracts and ADR 015. MASTER/LATEST and revised roadmap govern continuation.

Base is clean `main` at `b98110e`, already containing older work. Sprint 09 changes
remain uncommitted; no reset/clean/commit/push/cloud deployment. **Stop before 10.**

Versioned library, scanner-gated bounded PDF/DOCX/text/tabular/image extraction,
real English OCR, source locations/confidence, paged previews, keyword/citation
retrieval, signed reauthorized originals, released assessment references, policy
registry and guarded retention/holds/purge are implemented. No normal demo data,
workforce-note ingestion, semantic findings, AI provider, vector index or model.

Preserve live project grants, private assessment authority, identity/CSRF/session
transport, resource privacy, frozen results and shared metrics. Owners grant no
access. Jobs reuse durable_jobs/outbox/events/Celery with persisted actor/session,
fenced leases and authority rechecks. Forged tuples cannot enter connector cancellation.
Complete retention references include hidden archived projects; held/referenced files
cannot become orphans. Source/version rows are not hard-deleted by the app role.
Deletion immediately closes every retrieval/citation/preview/download/ticket path.

Schema: PASS: head 0011_document_sources applied; healthy restart/worker; 62 quiesced table hashes/counts, five object hashes and ten frozen migrations preserved. Prior actual head was 0010_account_authority; forward head
is 0011_document_sources. Frozen 0001–0010 and seven sources/prompts stay unchanged.
No backfill or consumer removal. OpenAPI/generated types remain authoritative.
Key code: document_tables/schemas/parser/retrieval/documents.py, migration 0011,
Documents component/page, existing jobs/worker dispatch. Do not replace foundations.

Use existing `.env`/volumes. Start `docker compose -f compose.yaml -f
compose.documents.yaml up -d --build`. Web/API 3000/8000; existing pgAdmin 5050.
Scanner has no host port or original-volume mount; wait for signatures/health.
Missing scanner fails closed. Exact runtime packages are checked against
infra/document-packages.lock; pypdf 6.20.1 is locked. Contracts record formats,
chunk/ticket/event/API versions. UTC calendar labels govern policy dates.

Backend runner resets only guarded ppm_test. Browser runner uses independent
3001/8001 and preserved test volumes. Full backend **123 passed**; final format/source
**24 passed**; final security **9 passed**; prior-head/drift passed. Browser regressions
**14 passed** plus affected document flow PASS: final document journey, 1 passed in 34.4 s (sprint09-browser-accepted.txt). Static/contracts/source hashes
and npm/Python audits passed; hosted CI remains unverified. See exact commands/logs
and failed/intermediate run explanations in checks, not just this summary.

Private normal backup restored only to ppm_sprint09_restore: 62 table counts/hashes
and five objects. Separate synthetic fixture restore to ppm_sprint09_documents_restore:
67 table counts/hashes and one fixture object, with authenticated signed download and
citation. No normal restore/purge or scratch overwrite. Backups/manifests/token-bearing
fixtures are ignored under artifacts/local/sprint09. One refresh-token row appeared
while the old stack was live; retain it in the fresh quiesced rollout baseline.
Normal preservation/runtime: PASS: head 0011_document_sources applied; healthy restart/worker; 62 quiesced table hashes/counts, five object hashes and ten frozen migrations preserved.

Do not publish private artifacts. Restore tombstones/deletion history before reopening
pre-deletion backups. Production retention/backup erasure, storage, performance,
availability and cloud acceptance remain open. Restore an archived project before
library management; GC still protects its held/referenced files. Local 30-day
retention is not legal approval. Earlier 8.1 CI/Word gates remain open.

The next separately authorized sprint is 10: shared budgeted AI gateway/embeddings
and hybrid retrieval. Candidate semantic findings belong to 11. Revalidate every
source/citation/tool scope, verify actual Git/migration state, preserve data and
uncommitted changes, and read the revised ordered section first. No continuation
authorization, full-product acceptance or production-readiness claim is implied.

## Documentation follow-up — 15 October 2026

The first closeout omitted required updates to current learning/user/demo/operator
guides, inventories, status/catalogue, navigation, feature mapping and tracker. Those
Markdown omissions are now reconciled. [Documentation closure](../../../04-testing/sprint-based/sprint-09/DOCUMENTATION_CHECKS.md)
records affected canonical paths, actual checks and retained Word/CI/release gates.
Application acceptance above remains its recorded run; this follow-up does not rerun
or infer new application tests. Work remains uncommitted. Stop before Sprint 10.
