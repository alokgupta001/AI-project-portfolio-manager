# Current system architecture

10 November 2026. Normal schema remains **0020**. The current source is a modular
monolith with a Next.js frontend, one FastAPI service and Celery worker/dispatcher
processes. The [project map](PROJECT_MAP.md) is the directory and file guide.

## Processes and storage

Next.js sends typed requests through its same-origin proxy. FastAPI registers
thin thin feature routers in main.py and owns request IDs, sanitized errors, readiness and
application resources. PostgreSQL stores identity, domain facts, immutable history,
durable jobs/outbox and usage reservations. Redis supplies transport/shared limits.
Private storage holds original source bytes and generated artifacts. The optional
ClamAV service and bounded parser/OCR child support document processing.

The [backend feature map](../../services/api/ppm_api/modules/README.md) links all
feature owners. Identity/session authority, delivery/capacity facts, assessment
scores, document evidence, command metrics, integrations, ML baselines, assistance,
specialists, personal workspace and selection research have separate packages.

All 129 feature HTTP handlers delegate to operations. Domain services and workers
call operation owners directly. Table definitions live at their feature owners;
shared/table_registry explicitly composes metadata. The generic record API composes
typed inputs across features using shared record primitives.

All 129 feature HTTP handlers delegate to operations. Domain services and workers
call operation owners directly. Table definitions live at their feature owners;
shared/table_registry explicitly composes metadata. The generic record API composes
typed inputs across features using shared record primitives.

## Request and authorization flow

Form → typed client → proxy → origin/CSRF and identity → active-organization
Principal/transaction → owning feature validation and operation → transaction-local
user/organization/role → application-role RLS and constraints → commit → response.
Roles, explicit project grants, private effort and independent-review eligibility
remain distinct. Backend/database checks enforce authority.

API and workers use ppm_app without superuser/BYPASSRLS. Migration ownership remains
separate. Workers use persisted authority and recheck live scope, revocation,
generation/lease fences and source eligibility before effects. Existing task names
pipeline.dispatch and pipeline.run retain their identifier-only envelopes.

## Processing and failure boundaries

Durable state/outbox commits in PostgreSQL; Redis is dispatch transport. File bytes
and SQL metadata have separate commit boundaries. Document operations preserve
source integrity, holds/retention and guarded orphan cleanup. Workspace change
streams recheck committed authorized revisions and live sessions. Mail's durable
delivery status preserves ambiguity between transport acceptance and inbox delivery.

Deterministic Python services own scoring and metrics. AI/agents reuse scoped
evidence, operator policy, bounded transports, shared quotas and immutable lineage.
ML history/dataset/baseline jobs preserve as-of splits, source/code fingerprints,
withdrawal and artifact access. Selection research remains separately scoped and
stopped; restructuring does not execute it.

## Verification and remaining boundaries

[Structure verification](../04-testing/BACKEND_STRUCTURE_STEP_32.md) records actual
offline/integration checks, the unchanged public contract and retained
environment issues. Current normal schema/data, applied migrations, provider
configuration, source prompts and historical artifacts remain preserved. Broad
live-model quality, production deployment and successor sprint work retain their
existing gates; see the [latest handoff](../handoffs/LATEST.md).

See [API details](18-api-contracts.md), [schema](DATABASE-DICTIONARY.md),
[permission contract](../contracts/permissions.md), [document contract](../contracts/documents.md),
[ML contract](../contracts/ml.md) and [ADRs](../architecture/adr).
The [previous architecture entry](../10-reference/history/SYSTEM_ARCHITECTURE_BEFORE_STRUCTURE_CLEANUP.md)
preserves earlier dated descriptions.
