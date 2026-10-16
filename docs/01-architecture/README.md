# Architecture

[Current system](SYSTEM_ARCHITECTURE.md), [actual API](18-api-contracts.md), [current schema](DATABASE-DICTIONARY.md). Established ADRs/contracts remain separately canonical.

[Source processing trace](../02-learning/06-ai-and-analytics/DOCUMENT_SOURCES.md), [document contract](../contracts/documents.md) and [ADR 015](../architecture/adr/015-document-sources.md) explain the current source boundary. Refresh/check API/schema/symbol inventories with `python scripts/documentation_inventory.py --check`.

## Sprint 10 shared AI runtime

[Sprint 10 runtime and evidence](../03-sprints/completed/sprint-10/README.md). Local implementation and bounded Gemini free-tier smoke verified; general model/retrieval quality remains unverified. $0 authorization and source fallback apply; no daily renewal. Stop before 11.
