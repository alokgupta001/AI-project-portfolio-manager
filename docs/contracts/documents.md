# Document sources — sources-v1

Sprint 11 [candidate document findings](agents.md) consume selected ready source spans with current authorization/version/hash checks. Acceptance means reviewed only. Source version/revocation changes withhold unsupported outputs; source ingestion and original objects are unchanged.

Sprint 09 extends the existing API, storage abstraction, durable_jobs/outbox/events,
Celery dispatcher and live identity/project grants. Migration 0011 follows the actual
0010_account_authority baseline. Applied 0001–0010 and source prompts are frozen.

`/documents` is the browser library; `/api/v1/documents` owns source APIs. OpenAPI and
generated TypeScript are authoritative. Upload/reprocess require a UUID idempotency
key and recheck access before replay. Version append, cancellation, governance,
delete and purge require If-Match; writes retain CSRF/origin/organization guards.
Pagination is stable created_at/id, default 25, maximum 100; previews page 25 chunks.
There are at most 100 versions/document. A hash repeated within a document returns
the existing version; hashes never deduplicate across scope or reveal foreign files.

Project evidence requires a live project read grant; uploads/changes require Admin
or PM with explicit project edit/manage. Organization documents are limited to
policies, readable by active members and writable by Admin. Owners confer no access.
No restricted workforce-note intake, raw effort or sentiment pipeline is activated.
Existing resource privacy and result-only assessment access remain unchanged.

Original bytes are immutable server-generated tenant/document/version object keys.
SHA-256 binds versions, processing and downloads. A forward database trigger rejects
changes to version identities/bytes metadata. Source text has location/method and
nullable confidence; unknown confidence is never replaced by certainty. There are
no summaries, model outputs or semantic findings in this sprint.

| Format | Extraction and boundaries |
| --- | --- |
| UTF-8 TXT | Paragraph plus character offsets; control characters/active markup rejected |
| CSV | UTF-8; maximum 5,000 rows and 100 columns; consistent width; sheet/row locations; formulas treated as text |
| DOCX | OOXML paragraph order, including table-cell paragraphs; no macros, embedded objects or external relationships |
| XLSX | Named worksheet/row/cell references and strings; formula/cache values omitted explicitly; no calculation |
| PDF | pypdf 6.20.1; maximum 50 pages, encrypted/active PDFs refused; Poppler/Tesseract fallback on image-only pages |
| PNG/JPEG | Tesseract English OCR; image location and mean recognized-word confidence (not factual certainty) |

All files are 1 byte–8 MiB; HTTP JSON/base64 is capped at 11.2 MB before model parsing.
ZIP entries cap at 500 and 16 MiB expanded. Format signatures are checked. XML
entities/DOCTYPE, macros and unsafe external references are refused. Parsing runs
in a child process, 60-second wall time, 45-second CPU, 768 MiB address space and
8 MiB output-file bound on Linux; output has at most 500,000 text characters/5,000
locations. OCR commands have 12-second timeouts. Raw parser diagnostics are discarded.

Every source must pass clamd INSTREAM before extraction can become ready. The
optional local scanner uses patched ClamAV 1.4.6, pinned image digest, private
network and separate signature volume; no original-object mount or published port.
Missing/unreachable scanner, malformed/unsupported files and parser failures remain
quarantined with fixed diagnostic codes. There is no manual scanner bypass. Start
with `docker compose -f compose.yaml -f compose.documents.yaml up -d --build` and
wait for the scanner's signatures/health. Without that override scanning is disabled
and intake fails closed. Real signature service availability is an operational gate.

Document work reuses durable_jobs; after 0012 exactly one integration, document-version
or AI-run reference is required. Job, event, audit and outbox commit together. Existing dispatcher discovers
queued/expired jobs. A 120-second fenced lease and three-attempt crash bound apply
to documents; deterministic scanner/parser failures require explicit reprocess.
The worker uses persisted actor/session, rechecks verified active identity, live
membership/project edit scope and tombstone before claim and before publishing.
Cancellation/deletion during extraction cannot publish results. Duplicate delivery
and reprocessing replace derived chunks atomically. Progress is sanitized persistent
stages, polled by the library; existing integration SSE/semantics are retained.

Keyword retrieval uses PostgreSQL simple text search and permission-filtered RLS
before ranking. Only the latest document version is active, and only when ready.
Chunking `locations-1200-v1` retains source locations and never exceeds 1,200 characters.
Citation reads revalidate source existence, readiness, permissions and latest version.
Older originals remain explicit version history. `Retrieval` marks budgeted_ai_runtime; direct GET search remains keyword-only.
Sprint 10 exposes budgeted hybrid only through its authenticated durable runtime;
Gemini free-tier completion/embedding smoke passed; no semantic AI extraction is produced by the source pipeline. Untrusted
document text has no tools or privileges and is rendered as escaped React text.

Download tickets use the maintained JWT implementation with a separate issuer/audience,
60-second expiry, bound tenant/user/session/version/hash. GET still requires live
authentication/source authorization and verifies object SHA-256. Cookies/tickets
are not stored in browser storage. Attachments use octet-stream/nosniff/sandbox and
server-validated filenames. Logs contain route templates, never token query strings.

Assessment links are additive references to identical, already released attachment
bytes. Both private assessment evidence authority and document edit scope are required.
No answer, rubric, saved score, evidence coverage or completed-result history changes.
Result-only readers do not gain private evidence access from a link.

Admin registers policy owner (active member), applicability, ready source version,
draft/current/superseded state and effective/review dates. UI labels review overdue
and not-yet-effective dates. This is a registry, with approval workflow pending 15.

Local pilot default retention is 30 days and requires organizational review before
real enterprise use. Admin can set timezone-aware retention and legal hold. Logical
deletion immediately blocks all retrieval, citation, preview and ticket/download
access, including outstanding tickets. Retained originals survive legal holds.
Explicit Admin purge requires deleted state, expired retention and no hold under the
same organization lock. Physical object deletion is repeatable; a narrowly guarded
function removes chunks/links and leaves metadata tombstones marked purged. There
is no automatic purge of existing assessment objects or application data. Private
backups have separate operator retention; backup restoration must preserve tombstones
or replay deletions before reopening access. Scratch-only orphan cleanup is documented
in recovery tooling; production-wide erasure remains a later release gate.

Official references reviewed 15 October 2026:
[pypdf text extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html),
[ClamD protocol](https://docs.clamav.net/manual/Usage/ClamdProtocol.html),
[Tesseract command line](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html),
[ClamAV patch releases](https://blog.clamav.net/).

Parser dependency pypdf is BSD-3-Clause; Tesseract is Apache-2.0, Poppler GPL-2.0-or-later,
ClamAV GPL-2.0. Preserve notices in container/distribution inventory. Exact Poppler/
Tesseract versions are enforced by `infra/document-packages.lock` and the build checker.
Runtime evidence is recorded in Sprint 09 verification, not inferred from tags.
## Sprint 10 AI runtime extension

[ai-evidence-v1](ai.md) owns the additive /api/v1/ai and /ai behavior, immutable
snapshots, budgets/accounting, protected source tools, citation reauthorization,
versioned evaluation and disabled fallback. durable_jobs references exactly one
integration, document version or AI run; existing event/SSE/authority rules remain.
Bounded Gemini free-tier smoke verified; broad model quality unverified. No semantic agents, private assessment ingestion,
metric changes or automatic plan edits. Admin-only restricted operations apply.
