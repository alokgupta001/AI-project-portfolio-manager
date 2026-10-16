# Sprint 09 documentation closure — 15 October 2026

The first Sprint 09 closeout updated reports/contracts/evidence but omitted required
current learning, user/demo/operator guides, inventories, catalogue, navigation,
tracker and mapping updates. This follow-up corrects that documentation gap. It changes
Markdown and documentation tooling only; it performs no database, migration, object,
application-feature or secret mutation and does not start Sprint 10.

## Canonical completion record

| Checklist obligation | Canonical document / correction |
| --- | --- |
| Requirements and exact scope | [Coverage](../../../requirements/coverage.md), [catalogue](../../../00-overview/FEATURE_CATALOGUE.md), [gap trace](../../../09-planning/FEATURE_GAP_TRACEABILITY.md), [roadmap](../../../09-planning/FUTURE_SPRINT_ROADMAP.md). F-065/068/069/073 accepted locally; F-066/067/074 and N-014/N-017 partial; F-070–072 remain 11. T-004 vector runtime remains pending. |
| Current availability/revision | [Current status](../../../00-overview/CURRENT_STATUS.md), [documentation index](../../../README.md), [sprint index](../../../03-sprints/README.md), [Sprint 09 hub](../../../03-sprints/completed/sprint-09/README.md). Base b98110e plus uncommitted work; normal head 0011. |
| Technical explanation and practical learning | [Source chapter](../../../02-learning/06-ai-and-analytics/DOCUMENT_SOURCES.md), [learning index](../../../02-learning/README.md), [Sprint 09 learning](../../../02-learning/sprint-based/sprint-09/README.md). Existing backend/request/frontend/database/security/workflow/AI/history/developer/operations chapters now explain their affected extension. |
| Actual user steps | [Library guide](../../../03-sprints/completed/sprint-09/USER_GUIDE.md), [current user guide](../../../06-user-guides/USER_GUIDE.md), [website walkthrough](../../../06-user-guides/WEBSITE_WALKTHROUGH.md). Viewer reads versus authorized Admin/PM uploads; separate TXT assessment intake remains explicit. |
| Executable demo | [Sprint 09 current demo](../../../05-demos/sprint-based/sprint-09/README.md), [demo index](../../../05-demos/CURRENT_DEMO_GUIDE.md); 09 removed from future demo table, 10–23 remain future. |
| API/database/architecture | [Generated API](../../../01-architecture/18-api-contracts.md), [generated dictionary](../../../01-architecture/DATABASE-DICTIONARY.md), [system architecture](../../../01-architecture/SYSTEM_ARCHITECTURE.md), [symbol/test index](../../../10-reference/CODE-AND-TEST-INDEX.md), [ADR 015](../../../architecture/adr/015-document-sources.md). Inventories regenerated from actual OpenAPI/metadata/AST. |
| Security, privacy and contracts | [Document contract](../../../contracts/documents.md); frontend, assessment and jobs contracts cross-reference the extension alongside permissions/events. [Known limits](../../../08-quality-and-security/KNOWN_LIMITATIONS.md) retains scanner, OCR, source scope, retention and release limits. |
| Setup, configuration and recovery | [Operator guide](../../../07-setup-and-deployment/DOCUMENT-PROCESSING.md), [local setup](../../../07-setup-and-deployment/LOCAL-DEVELOPMENT.md), [configuration](../../../07-setup-and-deployment/ENVIRONMENT_VARIABLES.md), Docker/identity/database-viewer guides reflect 0011 and private scanner. |
| Tests, failures and evidence | [Testing report](TESTING_REPORT.md), [bugs/fixes](BUGS_AND_FIXES.md), [strategy](../../TESTING_STRATEGY.md), [test hub](README.md), three PPM task receipts. Exact failed/accepted runs retained; no new application test pass inferred. |
| Report, handoff, entry points | [Report](../../../03-sprints/completed/sprint-09/SPRINT_REPORT.md), [handoff](../../../03-sprints/completed/sprint-09/HANDOFF.md), [LATEST](../../../handoffs/LATEST.md), MASTER, root README and portable agent entry; stop before 10. |
| Mapping, tracker and changelog | [Feature mapping](../../../09-planning/FEATURE_DOCUMENT_MAPPING.md), [tracker](../../../09-planning/DOCUMENTATION_UPDATE_TRACKER.md), [documentation changelog](../../../10-reference/DOCUMENTATION_CHANGELOG.md), root CHANGELOG and [checklist](../../../09-planning/SPRINT_DOCUMENTATION_CHECKLIST.md). |

## Checks for this follow-up

Checks are recorded after execution in the final closure below. Application acceptance
is retained from [TESTING_REPORT.md](TESTING_REPORT.md), not rerun for Markdown changes.
The inventory tool constructs OpenAPI without lifespan/settings/provider/database access
and compares it with the committed generated contract. The Markdown checker validates
local link targets/heading anchors and requirement/mapping counts; it does not fetch
external URLs, validate plain-text paths or inspect archived Word pages.

## Remaining gates and next owner

Historical reports, frozen original prompts/source files and archived Word/generators
retain their recorded scope. Archived Word outputs were not regenerated or visually
accepted by this follow-up. Earlier parent 8.1 hosted CI/Word layout acceptance remains
open; local Markdown closure does not close those gates. The 9 October audit counts
remain historical, with this dated closure carrying the current inventory/check results.

Production storage, retention/legal policy and backup erasure/all-surface recovery,
capacity/performance, availability and hosted CI need their owning release work. Hybrid
embeddings need separately authorized Sprint 10; semantic findings/review remain 11,
policy approvals 15. The next agent reads LATEST/MASTER/Sprint 09 handoff and verifies
actual Git/runtime state before any separately authorized work. Stop before Sprint 10.

## Executed follow-up results

| Command / check | Actual local result |
| --- | --- |
| `python scripts/documentation_inventory.py --check` | PASS: actual API, metadata dictionary and symbol/test inventories match their generator; OpenAPI equals committed contract. 95 operations across 83 paths, 66 metadata tables plus runtime Alembic table. |
| `python scripts/check_documentation.py` | PASS: 262 Markdown files, all checked local targets/anchors present; catalogue/mapping each retain 156 unique requirements and 36 gaps, matched to canonical coverage; required Sprint 09 hubs and accepted/partial status boundaries present. |
| `python scripts/check_sources.py` | PASS: all seven frozen source/prompt hashes retained. |
| `ruff check` and `ruff format --check` on both documentation tools | PASS. |
| Per-repository `git diff --check` | PASS. No global Git configuration changed. |
| Prior Sprint 09 checkpoint comparison | PASS: 133 pre-existing non-Markdown implementation/evidence hashes and applied 0011 unchanged. New documentation tools are the only code additions in this follow-up. |

Exact commands, outputs, reference counts and exit codes are retained in
[the log](../../../verification/sprint09-documentation-followup.txt) and
[machine-readable results](../../../verification/sprint09-documentation-followup.json).
The [refreshed local checkpoint](../../../verification/sprint09-checkpoint.json)
hashes the resulting uncommitted source/evidence files. External URLs, plain-text
paths and archived Word visual layout are outside these checks. Application test
results remain the earlier executed Sprint 09 acceptance, not a new rerun.

## Folder correction follow-up

Moved the four canonical Sprint 09 documents from active to completed, removed the
former planned README stub and updated all internal Markdown callers. The planned
and active Sprint 09 directories no longer exist. This classifies the verified local
slice consistently with earlier completed sprints, while retaining every external
acceptance limit. The validator now requires the completed Sprint 09 hub.

Post-move results: local links/anchors, source inventory drift, frozen source hashes,
documentation-tool Ruff checks and Git whitespace checks passed. Exact commands and
outputs are retained in [the folder correction log](../../../verification/sprint09-folder-correction.txt).
Prior documentation-audit logs retain the counts and paths they recorded at that time.
