# ADR 006 Local runtime and deployment options

Status: proposed baseline. Sources: WT, ST, WP. Decision date: 2026-10-05.

Local development uses Docker Compose; CI uses GitHub Actions; infrastructure definitions use Terraform. Proposed primary production target is AWS ECS with RDS PostgreSQL, S3 and a managed Redis-compatible broker. Web/API/workers use separate immutable images, health checks, secrets references and private service networking. Production readiness requires actual restore, migration and rollback exercises.

The Word document emphasizes Docker/Kubernetes, while the supplement suggests EC2/ECS. Preserve Kubernetes as a Sprint 23 alternative deployment profile using the same images/configuration, not a parallel application. AWS is selected over the Word document's Google Cloud/GCS alternative to match the supplement. EC2 self-management is deferred. No services are created in Sprint 00.

Consequences: region, domain, certificate approach, service sizing, budget, provider spend, data residency, retention and recovery targets remain unset. Sprint 01 requires no cloud credentials. A future deployment request should review concrete infrastructure changes and cost assumptions before live provisioning. Do not infer an approved monthly budget from this architecture choice.
