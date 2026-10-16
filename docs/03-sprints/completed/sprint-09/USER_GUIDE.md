# Sprint 09 document library

Use the existing account and organization selector, then **Document library**.
No sample records are added to a normal organization by this sprint.

1. An Admin, or a PM with project edit/manage access, chooses a title, category,
   project and source file. Organization-wide policies can omit the project and
   require Admin. Standard project read grants control all other readers. Document
   ownership never grants access. Do not place restricted workforce notes here.
2. Store and process. The stored version records its original SHA-256 and file size.
   Processing reports queued/scanning/ready or a fixed failure code. Missing scanner
   or OCR remains unavailable; it is not an approved source. There is no manual
   antivirus bypass. Cancel stops pending/in-flight publication; reprocess retries a
   failed dependency after it has been repaired.
3. Open a source to read page/paragraph/sheet locations. Preview text is escaped and
   paged. OCR confidence is mean recognized-word confidence, not factual accuracy;
   digital text confidence stays unknown. Download verifies the original hash and
   obtains a short-lived, user/session-bound ticket. Permission is checked again.
4. Add version to the open document to append changed bytes. Identical bytes return
   the existing version. Scope/title/category remain fixed. Old originals stay in
   history; keyword retrieval uses only the latest ready version. Reprocessing does
   not create another active copy of a chunk.
5. Search source text with keywords, then Open source location. The citation is
   checked again against current permissions and source version. Source text cannot
   issue commands or change project records. Semantic findings/embeddings remain
   unavailable in Sprint 09.
6. To link assessment evidence, copy the reference shown beside a released attachment
   in Assessments. Open an identical ready library version and Link released attachment.
   Both private assessment authority and document edit access are required. Existing
   results, answers, coverage and saved scores are unchanged.
7. Admin can register a policy owner, applicability, selected ready version, state
   and effective/review dates. Review overdue, not-yet-effective and superseded states
   are labels, not a claim of compliance. Approval workflow belongs to Sprint 15.
8. Admin controls retention and legal holds. The pilot default is 30 days; review it
   before real enterprise use. Delete immediately removes every retrieval/download
   path, including previously issued tickets. In Deleted sources and legal holds,
   purge requires expired retention and no hold. It permanently removes original
   objects and derived text while preserving a metadata tombstone.
9. Orphan cleanup first previews old, unreferenced objects. Purging recomputes eligibility
   and excludes other tenants, legal holds and all referenced versions. There is no
   automatic cleanup of existing evidence. Only invoke it for an approved retention
   decision; this sprint exercises it with isolated synthetic objects.

Local scanner startup: `docker compose -f compose.yaml -f compose.documents.yaml up -d --build`.
Wait for ClamAV's initial signature download/healthy state. The scanner has no host
port or source-volume mount. Without the override, valid uploads remain quarantined
with SCANNER_UNAVAILABLE until configured and explicitly reprocessed.

Supported: UTF-8 TXT/CSV, PDF (including scanned pages), DOCX, XLSX, PNG/JPEG, maximum
8 MiB. Parsing has strict memory/time/page/ZIP/text limits; unsupported, active or
corrupt files stay quarantined. Oversize HTTP/file bodies are rejected before storage.
English OCR is the installed language. XLSX formulas/cache values are omitted rather
than calculated. See the [format and security contract](../../../contracts/documents.md).

Recovery scripts save ignored private backups and restore only to newly named scratch
databases/object folders. Existing scratch targets are never overwritten. Do not
restore the normal database from a pre-deletion backup without replaying subsequent
tombstones/deletions before reopening access. Backup retention and production-wide
erasure need the later release policy.
