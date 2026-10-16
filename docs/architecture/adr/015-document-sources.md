# ADR 015: versioned sources before semantic intelligence

Accepted for authorized local Sprint 09, 15 October 2026. Baseline is actual head
0010 and clean checkpoint b98110e. The newer revised roadmap governs future scope.

Keep original bytes and source identity immutable. Store rebuildable, versioned
location chunks in PostgreSQL. Use its simple keyword ranking and live project RLS;
leave the embedding/hybrid DTO explicitly pending Sprint 10 and semantic findings
pending 11. This honors the staged requirement without introducing a second AI stack.

Extend the existing durable job table with an exclusive document-version reference,
retaining integration consumers and dispatch. A document-specific authorization
branch permits scoped PM writes without broadening connector administration. Process
untrusted bytes in a bounded child process and fail closed when scanning/OCR fails.

Scope organization-wide sources to policies. Assessment bridge references identical
released files and checks both authorities; it never recalculates old scores or
turns result grants into private-evidence grants. No restricted workforce notes are
added to generic document permissions.

Use explicit logical deletion and held/retained originals. Purge is a separate Admin
command after expiration. Additive tombstones and isolated recovery evidence avoid
destructive cleanup of established evidence. Default 30-day retention is a local
pilot setting, not legal or production approval. Production retention, capacity,
backup erasure and cloud storage remain external release decisions.
