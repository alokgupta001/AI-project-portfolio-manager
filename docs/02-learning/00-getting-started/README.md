# Start here: learn AI-PPM one request at a time

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](../../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13.

Use the local history/dataset/baseline walkthrough linked from the closeout and
`/integrations` for authority/conflict review. Synthetic results are not real accuracy;
existing guided-provider quotas, access and $0 controls remain unchanged.

Current closeout: Sprints 8.1 and 10 are completed for development scope; hosted CI and the current pilot Word guide are verified. Broad agent/model quality, production and scale remain successor/release gates. See [acceptance disposition](../../10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md). Earlier dated evidence below retains its historical scope.

AI-PPM helps an organization keep project plans, spending, staffing and assessment results in one place. A manager can compare a person's reported project status with the facts behind it. Deterministic calculations remain authoritative. Bounded guided specialist review
and the local history/CPU baseline lab now exist; unrestricted AI quality and forecast
serving remain unqualified/planned.

The original request walkthrough was source-reviewed on 9 October 2026 at base
`9056440`; its dated examples remain valid for that domain. Current Sprint 12 learning
is [From source conflicts to honest local baselines](../06-ai-and-analytics/LOCAL_BASELINES.md). It does not require you to change code or create new data just to learn.

Start with this flow:

**Click Save â†’ React collects fields â†’ Next.js forwards the request â†’ FastAPI checks the request and user â†’ Python checks project rules â†’ SQLAlchemy sends SQL â†’ PostgreSQL saves rows â†’ the API returns JSON â†’ React reloads the list.**

An API is a URL that the frontend calls to ask the backend to do something. JSON is the data format used in these requests and responses. The next chapter shows the actual components and today's features.

## Reading order

Read each row in order. Open the source files alongside the explanation. All source paths in this guide are relative to the `enterprise-ppm` repository unless a link specifies otherwise.

| Read | Open beside it | Before moving on, explain this in your own words |
| --- | --- | --- |
| [1. Project overview](../01-project-foundations/PROJECT_OVERVIEW.md) | `README.md`, `apps/web/components/workspace-home.tsx` | Who uses this application, and what can they do today? |
| [2. One complete request](../02-backend/REQUEST_LIFECYCLE.md) | `apps/web/components/delivery.tsx`, `services/api/ppm_api/delivery.py` | What happens between clicking Save and seeing a project in the list? |
| [3. Frontend](../03-frontend/FRONTEND_GUIDE.md) | `apps/web/app/account/identity-client.tsx`, `packages/contracts/src/client.ts` | Why does changing React state not save a database row? |
| [4. Backend](../02-backend/BACKEND_GUIDE.md) | `services/api/ppm_api/main.py`, `ppm_schemas.py`, `database.py` | Which checks belong to FastAPI, Pydantic and project code? |
| [5. Database](../04-database/DATABASE_GUIDE.md) | `services/api/ppm_api/ppm_tables.py`, `assessment_tables.py` | What does one project row represent, and how does it connect to other rows? |
| [6. Login and permissions](../05-security/AUTHENTICATION_AND_AUTHORIZATION.md) | `services/api/ppm_api/identity.py`, `migrations/versions/0003_delivery.py` | How does the backend identify you and decide what you can change? |
| [7. Main features](../01-project-foundations/FEATURE_WORKFLOWS.md) | `delivery.py`, `capacity.py`, `assessment.py` under `services/api/ppm_api` | Which stored facts support each screen? |
| [8. Scores and dashboards](../06-ai-and-analytics/SCORING_AND_DASHBOARDS.md) | `assessment.py:compute_scores`, `command.py:snapshot`, `metric_math.py` | Calculate a score by hand and explain why a metric might be Unknown. |
| [9. AI status](../06-ai-and-analytics/AI_AND_JOBS.md) | `services/worker/ppm_worker/app.py`, `docs/requirements/roadmap.md` | What is implemented, and what is a future proposal? |
| [10. Sprint history](../01-project-foundations/SPRINT_HISTORY.md) | `docs/sprints/`, `docs/04-testing/sprint-based/sprint-07/SPRINT-07-CI-FIX.md` | How did the current application grow, and what do the records prove? |
| [11. Read and change code](../07-testing-and-debugging/DEVELOPER_GUIDE.md) | `scripts/contracts.mjs`, `tests/test_delivery.py` | Which files would change when adding a project field? |
| [12. Interview preparation](../01-project-foundations/INTERVIEW_PREPARATION.md) | The source you already studied | Explain the project accurately without claiming planned AI is complete. |
| [13. Status and limitations](../08-deployment-and-operations/OPERATIONS_AND_LIMITS.md) | `docs/handoffs/LATEST.md`, `compose.yaml` | Explain the limits of the implementation and its verification. |

You can stop after chapter 2 and trace a real request. Return to the details when you meet a component you do not understand.

## Useful references after you understand the flow

- [Database dictionary](../../01-architecture/DATABASE-DICTIONARY.md): every table and column; use it for lookup, rather than reading it first.
- [API inventory](../../01-architecture/18-api-contracts.md): routes and request/response types.
- [Code and test index](../../10-reference/CODE-AND-TEST-INDEX.md): function and test locations. Some generated line numbers describe the older snapshot; search by symbol if a line has moved.
- [Local setup](../../07-setup-and-deployment/LOCAL-DEVELOPMENT.md) and [account activation](../../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md): use these when you want to run the application.

The previous chapter URLs remain as short links to the new guide. Source specifications, contracts, decision records, Word handbooks and sprint evidence remain available. Earlier dated records describe their own checkpoint; this guide explains the current source.

**Evidence rule:** a source file proves what code is present. A test definition shows what it intends to check. A recorded successful run proves only what that run exercised. This rewrite does not claim a new full application test run.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Start with the current-status page before following older evidence. The new reading path includes the pilot walkthrough, current demo, test strategy and feature mapping. A source example remains a code explanation unless its test evidence is explicitly linked.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

After the login chapter, follow [account email and role access](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md). Reproduce signup/invitation/recovery in the website and Gmail, then add a PM with the website access guide. Sender setup is a separate operator task; ordinary members need no commands.

## Learn Sprint 09 source processing

Follow [Document sources](../06-ai-and-analytics/DOCUMENT_SOURCES.md) through upload authority, private bytes, job/outbox,
ClamAV, bounded extraction/OCR, chunks, keyword citations, original tickets and retention.
It includes real symbols, a worked failure/revocation exercise and debugging steps.
Model inference/embeddings/semantic findings remain later work.

## Sprint 10 shared AI runtime

[Sprint 10 runtime and evidence](../06-ai-and-analytics/AI_GATEWAY.md). Local implementation and bounded Gemini free-tier smoke verified; general model/retrieval quality remains unverified. $0 authorization and source fallback apply; no daily renewal. Stop before 11.
