# ADR 012 — Versioned assessments and quarantined evidence

2026-10-06. Accepted for the user-authorized Sprint 06 repair.

Store each draft framework as a validated nested definition with stable UUIDs and publish immutable JSON snapshots. This makes the version the sole authority for question membership, rubric bounds and scoring. Answers reference question UUIDs inside their assigned snapshot; the API validates membership. Relational composite foreign keys protect tenant-owned framework, assignment, answer, access, history and attachment relationships. The unaccepted normalized draft implementation had no working UI or deployed normal data, so no supported consumer/data migration is discarded. Freeze the complete schema in 0005 rather than importing future live metadata into historical migrations.

Use existing membership/session/CSRF controls and the organization's advisory transaction lock. Explicit assignment governs respondent/reviewer scope, separate from project/resource grants. Published snapshots and event histories are insert-only to the app role. Admin-granted delegated draft editing and completed-result-only access use scoped grants. Protect all tenant tables with the established ppm.* context, not a second identity context.

Use existing local ObjectStore with bounded plain-text-only intake and quarantine. Independent human review releases downloads; broader documents and automated malware scanning remain disabled until a supported intake pipeline exists. Store hashes and immutable release/adjustment history. No additional dependency, provider, AI or cloud service is introduced.

The frontend reuses the existing authenticated transport, shell, form controls and chart/table conventions. It uses generated DTOs and a typed nested builder. Saving drafts, publishing, autosave and review have revision/idempotency safeguards. Comparisons require identical version IDs. Details and verification limits: [assessment contract](../../contracts/assessment.md).
