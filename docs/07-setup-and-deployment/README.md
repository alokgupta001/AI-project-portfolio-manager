# Setup And Deployment

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13.

## Sprint 12 local runtime

The existing Compose API/worker/beat stack runs the baseline lab; pandas/scikit-learn are pinned in the normal lockfile. No Ollama/new service is required. Follow [user steps](../03-sprints/completed/sprint-12/USER_GUIDE.md) after the verified forward migration. Production concerns stay in [future deployment points](../limitations/FUTURE_DEPLOYMENT_POINTS.md).

[Gemini free-tier development ($0)](GEMINI-FREE-TIER.md) covers private key setup,
operator-confirmed no-billing projects, one-time confirmation, quotas and fallback.

[Local setup](LOCAL-DEVELOPMENT.md), [identity operation](IDENTITY-DEVELOPMENT.md), [configuration fields](ENVIRONMENT_VARIABLES.md). Production deployment is PLANNED; no successful deployment is claimed.

[Docker services explained](DOCKER-SERVICES-EXPLAINED.md) describes all eight services shown in Docker Desktop, their dependencies, ports, persistent data, background processing and troubleshooting commands.

[Account email setup and Gmail acceptance](EMAIL-DELIVERY.md) covers sender verification, private SMTP configuration, sending status and verified development outcomes and remaining production limits.

[Step-by-step Gmail SMTP setup](GMAIL-SMTP-SETUP.md) gives App Password creation, exact environment keys, private storage, service reload, safe diagnostics and website/Gmail checks. Development signup, existing-account invitation and recovery are now verified; production and unrelated provider gates remain separate.

[Sprint 09 document processing/scanner and preservation](DOCUMENT-PROCESSING.md) remains the source/scanner operator reference; [AI runtime](AI-RUNTIME.md) extends it. Current normal revision 0018 is recorded in [the latest handoff](../handoffs/LATEST.md).

## Sprint 10 shared AI runtime

[Sprint 10 runtime and evidence](AI-RUNTIME.md). Local implementation and bounded Gemini free-tier smoke verified; general model/retrieval quality remains unverified. $0 authorization and source fallback apply; no daily renewal. Stop before 11.
