# Operate local document processing

Current local migration is `0012_ai_runtime`. Preserve established `.env`,
volumes and applied migrations. No bootstrap, normal reset, reseed or downgrade is
needed to use an already upgraded instance. The normal UI/API remain on 3000/8000;
isolated browser tests use 3001/8001. Production configuration remains disabled.

## Start the scanner and application

From the repository root with Docker Desktop's Linux engine:

```powershell
docker compose -f compose.yaml -f compose.documents.yaml config --quiet
docker compose -f compose.yaml -f compose.documents.yaml up -d --build
docker compose -f compose.yaml -f compose.documents.yaml ps
docker compose exec -T api python scripts/smoke_worker.py
```

Wait for ClamAV health/signatures before intake, then open Document library at
`http://localhost:3000/documents`. Initial signatures need external network access.
The optional override sets `PPM_DOCUMENT_SCANNER_HOST=clamav` for API/worker/test;
`PPM_DOCUMENT_SCANNER_PORT` defaults to 3310. Base Compose leaves the host blank,
which makes scanning fail closed. Existing quarantined versions need explicit Reprocess
after the dependency recovers. Never disable scanning to make a source ready.

[`compose.documents.yaml`](../../compose.documents.yaml) pins ClamAV 1.4.6 by digest,
keeps signatures in a separate volume and exposes no host port or source-object mount.
[`infra/document-packages.lock`](../../infra/document-packages.lock) pins direct
Poppler/Tesseract package versions; image builds run
[`verify_document_runtime.py`](../../scripts/verify_document_runtime.py) to reject drift.
`pypdf==6.20.1` is in the Python lock. English is the installed OCR language.
Changing runtime locks requires rebuilding and new parser/security acceptance.

## Verify and diagnose

Use API readiness, source job status and fixed diagnostics; the foundation worker
probe proves Redis → worker → PostgreSQL connectivity, not document acceptance.
For a real intake check use a small fictional source in an isolated organization,
then confirm Ready, preview/source location, keyword hit and downloaded original hash.
[User operations](../03-sprints/completed/sprint-09/USER_GUIDE.md) explain permissions,
supported formats and retry/cancel/version behavior. [Learning/debugging](../02-learning/06-ai-and-analytics/DOCUMENT_SOURCES.md)
traces the real symbols. Source bodies/tickets/backups stay out of public logs.

The file bound is 8 MiB; the HTTP JSON bound is 11.2 MB. PDF is bounded to 50 pages,
ZIP containers to 500 entries/16 MiB expanded, text to 500,000 characters and chunks
to 5,000 at 1,200 characters each. The child has a 60-second wall limit, Linux
45-second CPU/768 MiB address-space/8 MiB output limits; OCR commands have a 12-second
timeout. Unsupported/active/corrupt content quarantines. XLSX formulas/cache values
are omitted. Oversize upload bodies are rejected before original storage.

## Retention and recovery

Admin controls explicit holds and retention (pilot default 30 days). Logical delete
immediately revokes originals, previews, retrieval and tickets. Eligible explicit
purge removes objects/chunks/evidence links and retains metadata tombstones. Orphan
preview is capped to 100 results after a 10,000-object scan and requires age 30 days;
purge recomputes eligibility. All tenant references and held archived-project versions
are protected. Restore an archived project before normal library management.

The executed preservation and restore commands/results are in
[the test report](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md), including
`sprint09_preserve.py`, `sprint09_recovery.py` and `sprint09_document_recovery_run.py`.
Those scripts retain private manifests/backups under ignored `artifacts/local/sprint09`,
guard target names and refuse existing scratch targets. They are acceptance utilities,
not a normal restore/reset procedure. The accepted normal-data scratch restore matched
62 established tables/five objects at head 0010. The independent document fixture
matched 67 tables/one source object plus signed download/citation. No normal restore
or purge was performed. The quiesced normal rollout preserved 62 table hashes/counts,
five objects and all ten earlier migrations; a legitimate refresh-token row created
before quiescence is retained.

Reopening a pre-deletion backup requires replaying subsequent tombstones/deletions
before granting reads. Production storage, backup expiration/erasure, incident recovery,
capacity and hosted CI remain release gates. Existing volumes must never be removed
as a troubleshooting shortcut. Stop services with the same Compose file arguments
if needed; preserve volumes and signatures.
