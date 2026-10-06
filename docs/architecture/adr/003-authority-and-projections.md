# ADR 003 Canonical data and derived indexes

Status: proposed baseline. Sources: WT, WD, W5, W8, ST. Decision date: 2026-10-05.

Use PostgreSQL for canonical entities, decimal money, history, JSONB run metadata and outbox/jobs. Objects store immutable document/export/audio versions behind an S3-compatible interface. Authorization uses metadata and policy checks, not opaque file paths alone.

Start vectors in pgvector and keep retrieval behind a service interface. This intentionally substitutes for the Word document's Pinecone/Weaviate suggestions, reducing initial infrastructure while allowing later evaluation of dedicated vector services. Evaluate filtered retrieval quality, tenant isolation, index cost and embedding-version migrations before acceptance. Do not assume a tenant filter added after retrieval is secure.

Use Neo4j in Sprint 18 as a rebuildable projection with canonical IDs, organization and project scope, provenance and lag metadata. PostgreSQL records and approved relationships remain authority. Graph results are bounded and parameterized; inferred edges cannot execute live changes.

Consequence: document deletion/access changes must invalidate vectors, cached answers and graph-derived evidence. A full rebuild and reconciliation command is required. Choose external vector storage only if scale/residency/performance evidence justifies the cost and a tested export/import path exists.
