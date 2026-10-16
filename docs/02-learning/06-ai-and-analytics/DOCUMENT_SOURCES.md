# Trace a document from upload to citation

Sprint 09 implements a reusable source and keyword workflow. It provides no model inference,
embeddings, semantic findings or automated project changes. Read the [document contract](../../contracts/documents.md)
for exact formats/limits, [user steps](../../03-sprints/completed/sprint-09/USER_GUIDE.md)
to operate it and [executed checks](../../04-testing/sprint-based/sprint-09/TESTING_REPORT.md)
for evidence rather than treating this explanation as a test result.

## Follow one source through the code

1. Open `/documents`. [`Documents`](../../../apps/web/components/documents.tsx)
   collects title/category/project/file and calls the generated typed API through the
   existing same-origin client. `can_manage` controls available actions; the server
   independently checks every request. A PM needs project edit/manage, a Viewer can
   read scoped sources, and only Admin manages an organization-wide policy.
2. [`documents.upload`](../../../services/api/ppm_api/documents.py) validates the
   bounded input, live principal and idempotency fingerprint. Bytes are private objects;
   document/version, durable job, outbox, event and audit state commit together in PostgreSQL.
   A database rollback can leave an orphan object: object storage and SQL are not one transaction.
3. [`document_tables`](../../../services/api/ppm_api/document_tables.py) defines
   `source_documents`, `source_versions`, `source_chunks`, `source_evidence_links`.
   [`0011_document_sources`](../../../services/api/migrations/versions/0011_document_sources.py)
   installs RLS, immutable byte identity, guarded retention functions and document-job authority.
   A version number/hash identifies original bytes; status/chunks are replaceable derived state.
4. The existing outbox dispatcher sends a durable job through Redis to Linux Celery.
   `documents.document_worker` rechecks persisted actor/session/project authority under
   the organization lock, rereads the job with `FOR UPDATE`, and uses a fenced lease.
   A late/revoked/cancelled worker cannot publish derived text. Broker tuples are not authority.
5. [`document_parser.scan`](../../../services/api/ppm_api/document_parser.py) streams
   bytes to real ClamAV. Failure/unavailability quarantines; there is no manual bypass.
   `isolated_extract` executes parsing in a bounded child. `extract` handles digital text,
   DOCX tables, CSV/XLSX and PDF/images; scanned pages/images use Poppler/Tesseract.
   Text, ZIP expansion, page count, chunk count, process memory/CPU and wall time are bounded.
6. Processing atomically replaces chunks and sets the source ready only while authority
   and the lease remain valid. A retry does not append duplicate active chunks. A source
   exceeding 5,000 chunks fails rather than exposing only its beginning.
7. `documents.search` applies tenant/project RLS before PostgreSQL simple keyword ranking.
   Only the latest version participates and it must be ready. `documents.citation`
   rechecks latest version, access and deletion. Replacing a version can invalidate an old citation.
   [`document_retrieval`](../../../services/api/ppm_api/document_retrieval.py) defines
   retrieval/candidate interfaces; its embedding boundary is implemented by Sprint 10 Runtime.index, with bounded Gemini free-tier smoke verified and broader retrieval quality unverified; see [the gateway trace](AI_GATEWAY.md).
8. `ticket` issues a 60-second user/session/org/version/hash-bound JWT. `download` also
   authenticates current authority and checks original SHA-256. Attachment headers disable
   sniffing and sandbox the response. Escaped preview content and source instructions never execute.

## Work through a concrete failure

Upload a fictional `charter.txt` containing `cedar launch evidence` to a permitted
project, wait for Ready and search `cedar`. Check its source location, then append changed
bytes. The original remains downloadable through authorized history, while search uses
the latest ready version. Remove the reader's grant in another profile: listing, citation
and an earlier download ticket must all lose access. Run this in the isolated demo/test
environment, not by changing established customer data.

| Symptom | Inspect | Correct recovery |
| --- | --- | --- |
| `SCANNER_UNAVAILABLE` | Scanner override/health, host/port, signatures | Restore scanner health, then explicitly reprocess; never manually release antivirus quarantine |
| Parsing/quarantine failure | Fixed diagnostic, format/ZIP/page/text bounds, parser runtime | Correct the source or runtime; keep untrusted bytes from retrieval |
| Stale edit | Document revision / pending browser save | Reload after save completes and repeat the intended edit |
| Missing keyword result | Current organization, project grant, latest version status, actual extracted terms | Repair legitimate authority/dependency; empty results are valid |
| Assessment link denied | Released attachment SHA and private-evidence authority plus document edit | Use identical bytes and independent permission; do not modify scores or weaken evidence privacy |
| Purge refused | Retention expiry, hold, deleted state | Retain until eligible; holds on archived projects also protect referenced objects |

Use request ID, document/version/job IDs and fixed stage/error codes for debugging.
Do not log bodies, tickets, private evidence or secrets. Digital extraction confidence is
unknown; OCR reports recognized-word confidence, not factual certainty. Policy date labels
use UTC calendar dates; approval belongs to Sprint 15. The pilot retention default is
30 days, with explicit deletion/purge and tombstones. Production backup erasure and
release recovery remain open.

## Evidence and practical limits

[`tests/test_documents.py`](../../../tests/test_documents.py),
[`tests/test_document_parser.py`](../../../tests/test_document_parser.py) and the
[browser journey](../../../tests/browser/documents.spec.ts) cover source authority,
real ClamAV clean/EICAR, actual English OCR, replay, worker fencing, immutable SQL identity,
citations, private references and retention. The eight labeled keyword queries hit the
expected source/location 8/8 on distinct synthetic terms; this measures neither semantic
understanding nor production relevance. See [bugs/fixes](../../04-testing/sprint-based/sprint-09/BUGS_AND_FIXES.md)
and [operator recovery](../../07-setup-and-deployment/DOCUMENT-PROCESSING.md).
