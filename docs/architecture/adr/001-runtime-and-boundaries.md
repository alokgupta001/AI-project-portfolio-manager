# ADR 001 Modular monolith and application boundaries

Status: proposed baseline. Sources: WT, ST. Decision date: 2026-10-05.

Use Next.js App Router/TypeScript/Tailwind/shadcn, Motion and Recharts, with an accessible purpose-built Gantt/timeline. Use a query-cache library for server state and Zustand for local UI state. Use FastAPI/Uvicorn, Pydantic, async SQLAlchemy and Alembic. Domain modules share PostgreSQL but expose explicit service interfaces; separate web/API/worker processes can scale independently.

Why: most modules need common project, permission and metric definitions. One transactional authority and generated API client reduce accidental drift while retaining a migration path to services if measured need emerges. A managed ingress supplies same-origin routing; no separate custom gateway implementation is needed.

Alternatives: NestJS duplicates the Python AI integration surface; Chart.js remains viable for charts but does not replace the timeline/accessibility work. Microservices impose distributed consistency before there is a measured need. Avoid installing all alternatives.

Consequence: module ownership is enforced through code organization/reviews, not physical databases. Sprint 01 must pin compatible supported versions and locks using official release documentation at implementation time. No version is claimed validated in Sprint 00. Extract a service only with measured scale/security boundaries and a compatibility plan.

Browser route protection is insufficient by itself; server-side data operations must enforce authorization. Reference: [Next.js authentication guidance](https://nextjs.org/docs/app/guides/authentication), consulted 2026-10-05.
