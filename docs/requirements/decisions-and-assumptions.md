# Decisions assumptions and source reconciliation

Current explicit Sprint 11 authorization permits PPM-11-001/002/003, deterministic acceptance and additive test migration 0013. [ADR 017](../architecture/adr/017-specialists-and-human-review.md) records shared batching, distinct scores and independent reviewed-only decisions. USD 0; no live providers or deployment. Stop before Sprint 12.

Sprint 05 is explicitly authorized and implemented locally. [ADR 011](../architecture/adr/011-resource-capacity.md)
records resource/calendar boundaries, partial project scope, sensitive effort grants,
team suppression and immutable planning snapshots. The dated authorization statements
below describe historical checkpoints. Sprint 06 requires separate authorization.

Sprint 03 update: explicitly authorized enterprise shell is implemented. [ADR 009](../architecture/adr/009-enterprise-shell.md) records native shared UI and deferred optional dependencies. Sprint 04 remains separately authorized work. The Sprint 02 statement below is historical.

Sprint 02 update (2026-10-05): user authorization covers local identity and organization authorization only. [ADR 008](../architecture/adr/008-identity-implementation.md) resolves exact session lifetimes, strict refresh replay behavior, secure localhost cookies, private local-mail delivery and the global identity/RLS boundary. Production provider/policy decisions remain open. Sprint 03 is not authorized by this checkpoint.

Status as of 2026-10-05: proposed engineering baseline prepared under the user's authorization to execute Sprint 00. No claim of owner sign-off. Reasonable reversible defaults may guide Sprint 01; choices requiring actual credentials, cost limits or organizational policy remain explicit later prerequisites.

Sprint 01 update: the user subsequently authorized this proposed architecture as the local development baseline. The web/API/worker foundation is implemented and verified as recorded in [ADR 007](../architecture/adr/007-sprint-01-runtime.md) and the [report](../03-sprints/completed/sprint-01/SPRINT_REPORT.md). This does not settle later production/provider/policy decisions or authorize Sprint 02.

| ID | Source tension or missing detail | Proposed resolution | Review point |
| --- | --- | --- | --- |
| D01 | WT suggests several frameworks/clouds; ST supplies a narrower stack | Next.js + FastAPI modular monolith; separate API/web/worker. ADR 001 | Before changing application foundation |
| D02 | Pinecone/Weaviate in Word versus unspecified vector store elsewhere | Start pgvector with replaceable retrieval interface; a deliberate stack substitution, not a source mandate. ADR 003 | Before Sprint 09; revisit for scale/residency |
| D03 | Kafka/Redis architecture | Redis/Celery with PostgreSQL outbox/job truth; no Kafka initially. ADR 004 | Sprint 08 reliability design |
| D04 | Docker/Kubernetes in Word; EC2/ECS in supplement | ECS primary target; Kubernetes alternative profile in 23 using same images. AWS region and spend remain unset. ADR 006 | Before paid provisioning |
| D05 | Stateless JWT versus timely logout/membership revocation | Stateless signature validation plus server-side session and membership checks; rotated refresh credentials. Not fully stateless authorization. ADR 002 | Sprint 02 |
| D06 | AI thought process streaming | Stream observable stages and concise evidence summaries only, not private chain-of-thought. ADR 005 | Sprint 10 |
| D07 | Pydantic ensures AI never returns malformed JSON | Provider output may fail; validate, bounded-retry and fail safely before persistence/display | Sprint 10 failure tests |
| D08 | Burnout prediction from notes/commit data | Team workload/sentiment support signals, no medical diagnosis or individual ranking; suppress groups under five resources by default | Before importing real workforce notes |
| D09 | Models listed without reliable labels or datasets | Model candidates, not requirement to deploy all; public/synthetic data proves pipeline only. Failure definition and eligible labels required for promotion | Sprint 12 |
| D10 | Real-time and instant have no exact latency boundary | Proposed source-event-to-dashboard p95 10 s after receipt, alert accepted by provider p95 60 s after committed trigger; source polling lag shown separately | Sprint 08/21 load plan |
| D11 | No fiscal calendar/currency/organization timezone given | Per-organization mandatory IANA timezone/currency onboarding values; local demo Asia/Kolkata, INR, calendar quarters, Mon–Fri 8 h. No production default inferred | Sprint 04 onboarding |
| D12 | No risk, maturity or alignment formulas specified | Proposed version-1 definitions in metrics contract; clearly configurable and unvalidated heuristics | Before Sprint 06/07 |
| D13 | Three roles but approval personas need clarity | Admin or scoped PM can be assigned approver; Viewer cannot approve; no self-approval on sensitive actions | Sprint 15 |
| D14 | Cross-team performance comparison | Compatible within-tenant cohorts only, no comparison of raw story points across teams | Sprint 19 |
| D15 | Source order puts multi-agent work in later phase | Build typed runtime before agents; agents before full workflows; preserve capability scope, adjust technical sequence | Roadmap baseline |
| D16 | Provider/model/retention/budget unspecified | Provider adapter with one implementation chosen against available credentials; disabled when not configured; production retention and spend cap required before real data/calls | Sprint 09/10/20/21 |
| D17 | Program/project placement not specified | Project belongs to one portfolio and optionally one program in that portfolio; goals may be many-to-many | Sprint 04 |
| D18 | Enterprise legal/compliance scope unspecified | Governance evaluates user-supplied policies and rubrics, not compliance certification; hosting/data policy needs organizational review | Before production intake |
| D19 | Broad baseline promises zero integration conflicts | Versioned contracts, migration checks and acceptance evidence reduce conflict; cannot guarantee absence of defects | Every sprint |

## Review priorities

The local Sprint 01 foundation can proceed on the proposed architecture without cloud credentials. Before actual deployment, select region, monthly budget and recovery objectives. Before predictive model promotion, obtain lawful, suitable historical labels. Before importing real enterprise data, set retention, provider data handling and authorized workforce evidence policy. Any change to a shared contract requires an ADR and affected-consumer plan.

## Enhancements kept within the product purpose

Evidence drawer, freshness/coverage indicators, saved views, command palette, decision log, scenario comparison, data-quality console and AI usage console. These are separately labeled enhancements in coverage. Email test-to-self, auditability, retry safety and permission checks are enabling controls, not unrelated product expansions.

## Sprint 04 implementation decisions

[ADR 010](../architecture/adr/010-delivery-system-of-record.md) accepts the existing local baseline, normalized delivery schema, explicit grants, Admin-only cross-project dependency writes, append-only financial/history records, incomplete metric handling and isolated seeded demo. Advanced timeline interactions and later intelligence are not included.

## Sprint 06 repair and acceptance

The user explicitly authorized rechecking and fixing Sprint 06 after its initial handoff proved unsupported. [ADR 012](../architecture/adr/012-assessment-engine.md) records frozen framework definitions, explicit assignments, app-role RLS, immutable results and plain-text evidence quarantine. No normal/deployed 0005 data existed at repair start; only disposable prior attempts were replaced. Evidence intake is restricted to UTF-8 text with independent human release; broader formats, automated malware scanning and AI interpretation remain disabled. Local acceptance evidence is recorded in Sprint 06 checks. Sprint 07 remains separately authorized work.

## Sprint 07 authorized implementation

The user authorized Sprint 07 on 2026-10-07. [ADR 013](../architecture/adr/013-command-center.md) records current-state snapshots versus period facts, explicit baseline/calendar selection, immutable sprint closures, actor-owned saved views and existing capacity privacy. Starter rules are deterministic operational heuristics, not predictive probabilities. No historical closure backfill, new dependencies, external communications or Sprint 08 activation.


## Sprint 08 authorized implementation

The user authorized Sprint 08 only on 2026-10-09. [ADR 014](../architecture/adr/014-durable-ingestion.md)
accepts PostgreSQL job/outbox truth, Celery dispatch, live delegated authority,
bounded source import and observable SSE. Provider fixtures are separated from live
credentials. Jira sprint modification time and historical point coverage remain
unknown. No Sprint 09 document/AI work, cloud provisioning or external notification
is activated. Production retention and unattended connector identity remain open.

## Sprint 09 authorized local implementation — 15 October 2026

Current explicit authorization covers only 09. [ADR 015](../architecture/adr/015-document-sources.md)
accepts safe versioned sources, existing durable jobs, scoped keyword/citation access,
policy registry and local retention/recovery. Revised staging keeps embeddings/hybrid
in 10 and semantic findings in 11; those combined requirements stay partial. Existing
metrics/results/identity/privacy and applied 0001–0010 are preserved. New normal head
0011 is frozen. Earlier 8.1 hosted-CI/Word-layout gates remain open. Stop before 10.

## Sprint 10 explicit authorization — 15 October 2026

Current authorization covers implementation, isolated verification, non-destructive
local forward upgrade and documentation for 10 only. User explicitly requires mocks
and fallback; no real AI calls or charges until separate provider/model/spend approval.
[ADR 016](../architecture/adr/016-budgeted-ai-runtime.md) records typed native graph,
Admin-only costly work, conservative reservations and bounded exact JSONB vectors
instead of a database-image/pgvector change. Provider acceptance remains BLOCKED;
semantic agents, metrics/assessment rewrites and automatic plan edits are excluded.
Applied 0001–0011 and all earlier work are preserved. Stop before 11.
