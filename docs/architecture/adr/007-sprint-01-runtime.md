# ADR 007 Sprint 01 runtime baseline

Status: implemented local foundation; final acceptance status is in the Sprint 01 report. This refines ADRs 001, 004 and 006 without introducing later product modules.

Use Node 24 and Python 3.12. The verified host versions are Node 24.20.0, npm 11.19.0 and Python 3.12.14; the pinned Linux Python image reported 3.12.15. Next.js 16.3.8, React 19.3.0, TypeScript 5.9.3, FastAPI 0.142.2, SQLAlchemy 2.0.54, Alembic 1.20.0, redis-py 6.4.0 and Celery 5.6.3 were resolved from the package registries and locked. All exact dependencies are in package files/locks; licenses are retained in npm lock metadata and the Python inventory.

Next.js documents Node 20.9 or later for version 16; this repository deliberately targets the Node 24 line. [Next.js installation](https://nextjs.org/docs/app/getting-started/installation). Celery does not support Windows as its worker platform, so the real worker runs in Linux containers. [Celery FAQ](https://docs.celeryq.dev/en/main/faq.html). Python 3.12 remains in security support. [Python version status](https://devguide.python.org/versions/). Sources were checked on 2026-10-05; exact dependency compatibility is further evidenced by local checks and container builds.

The initial framework lint preset pulled a vulnerable braces dependency and plugins incompatible with ESLint 10. It was removed in favor of supported ESLint 10 plus typescript-eslint, with TypeScript 5.9.3 satisfying openapi-typescript's 5.x peer contract. The resulting npm audit reported zero vulnerabilities. This is not a permanent security guarantee; CI repeats the audit. Shared UI design-system work and Next-specific lint policies can be extended in Sprint 03.

Foundation state is one non-tenant installation checkpoint, readable by the restricted app role. No unauthenticated write endpoint or enterprise domain tables exist. Production environment values are rejected until authentication and authorization are implemented. Local storage uses a bounded filesystem adapter; no S3 service or upload route is claimed.

Compose uses separate migration credentials and read-only app access. The test profile points only to `ppm_test`; demo uses `ppm_demo` and a separate Compose project. The sample worker task verifies process/broker/database connectivity; it is not the durable outbox implementation scheduled for Sprint 08.

Containers intentionally include developer/test tools for this local sprint. Production image minimization, TLS ingress, deployment IAM and release hardening remain Sprint 23 work. An actual CI-hosted run requires a Git remote and push, neither created here.
