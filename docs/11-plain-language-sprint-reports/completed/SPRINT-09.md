# Sprint 09 — A document library with traceable sources

**Status:** Completed and verified locally for document storage, processing, keyword retrieval and governance. Semantic document analysis is later work.

## What was built and why it matters

Project documents can now be stored once, updated through versions, previewed and searched. A search result points back to a page, paragraph or sheet so a reader can check the source. The library also tracks policy information and controls how deleted evidence is retained.

Open **Document library** at [Documents](http://localhost:3000/documents).

| Delivered function | Where to find it | How to check / expected result |
| --- | --- | --- |
| Categorized project and policy uploads | Library upload form. | Choose a project, title, category and supported file, then **Store and process**. The document gets a saved version and processing status. |
| Virus checking and text extraction | Document/job processing status. | Wait for scanning/processing to finish. Only successful processing reaches ready. A missing scanner keeps the source quarantined. |
| Multi-format previews | Open a ready version. | Read the escaped text and its page/paragraph/sheet location. Use preview paging to inspect later locations. |
| Read text from scanned pages/images (OCR) | Ready scanned PDF, PNG or JPEG preview. | Upload a clear fictional English sample. Check the recognized text against the image; the confidence value describes recognition, not truth. |
| Version history | Open document → **Add version**. | Upload changed bytes to append a version. Uploading identical bytes returns the existing version; old originals remain in history. |
| Keyword retrieval and citations | **Search source text**, then **Open source location**. | Search a distinctive word. The result opens its source location and rechecks current access/version. |
| Verified original download | Open a document version's download control. | Download your practice original and compare it with the file you uploaded. Download requires current permission. |
| Link existing assessment evidence | **Link released attachment** on an identical ready library version. | Copy the reference beside an assessment's released attachment and link it with both required permissions. Answers and scores remain unchanged. |
| Policy register | Admin: policy controls in the library. | Register owner, applicability, ready source version, state and effective/review dates. Inspect the saved labels, including overdue review where applicable. |
| Retention and legal holds | Admin: retention controls and **Deleted sources and legal holds**. | Inspect the retention period and a practice hold. Purge is unavailable before expiry or while held. Use practice records only. |
| Delete, eligible purge and orphan preview | Admin: deleted-source and cleanup controls. | Deletion immediately hides source access. Preview cleanup eligibility without purging real files. Permanent purge is a separate operation. |
| Project and policy access rules | All library operations. | Compare an authorized PM/Viewer with someone lacking the project grant. Ownership alone does not expose a source. |

## A simple document check

**You need:** Admin or PM with project edit/manage, a practice project, and scanner-enabled startup from [Getting access](../START_HERE.md). A Viewer can check permitted reads but cannot upload.

1. Create a small TXT file containing: `Practice launch approval is required before release.`
2. Store and process it under the practice project with a suitable category.
3. Wait for ready, open its preview and check the sentence.
4. Search for `approval` and open the returned source location.
5. Add a version changing `approval` to `signoff`. Wait for ready, search for `signoff` and inspect version history.
6. Download the original for a selected version and compare it with the corresponding local file.

**Expected result:** Ready files are readable and searchable with source locations; the changed file has a new version. Keyword retrieval uses the latest ready version, while earlier originals stay in history. A quarantined file is not presented as usable evidence.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Library, versions, search and policy/retention controls | [Document screen](../../../apps/web/components/documents.tsx) |
| Uploads, downloads, access, policy and retention rules | [Document service](../../../services/api/ppm_api/documents.py) |
| File parsing/OCR and keyword/source retrieval | [Parser](../../../services/api/ppm_api/document_parser.py), [retrieval](../../../services/api/ppm_api/document_retrieval.py) |
| Saved document versions and scanner setup | [Document tables](../../../services/api/ppm_api/document_tables.py), [document migration](../../../services/api/migrations/versions/0011_document_sources.py), [scanner configuration](../../../compose.documents.yaml) |
| Browser check | [Document scenario](../../../tests/browser/documents.spec.ts) |

## Recorded checks and limits

The sprint recorded 123 full backend tests, 24 focused format/source cases, nine final security checks and a final document-browser pass after fixing a selection/save race. A synthetic keyword check found the expected source/location for eight of eight distinct-keyword examples; that is not a general search-quality guarantee.

Supported files: TXT, CSV, PDF/scanned PDF, DOCX, XLSX and PNG/JPEG, up to 8 MiB, with additional parsing limits. OCR is English. Spreadsheet formulas/cached formula values are omitted rather than calculated. The library does not judge document meaning, produce approved semantic findings or change assessment scores. Policy labels are not an approval/compliance workflow. Production storage, retention and erasure decisions remain open.

[Original report](../../03-sprints/completed/sprint-09/SPRINT_REPORT.md) · [Detailed user steps](../../03-sprints/completed/sprint-09/USER_GUIDE.md) · [Recorded testing](../../04-testing/sprint-based/sprint-09/TESTING_REPORT.md) · [Report index](../README.md)
