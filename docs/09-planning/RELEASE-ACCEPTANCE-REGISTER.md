# Release and successor acceptance register

16 October 2026. These requirements remain OPEN independently of the completed
Sprint 8.1 pilot and Sprint 10 gateway development scope. Original thresholds,
requirement dispositions and historical results remain in their owning contracts.

| Gate | Owning work | Required evidence before claiming acceptance |
| --- | --- | --- |
| Nine-agent and semantic assessment quality | Sprint 11; local controls [verified](../04-testing/sprint-based/sprint-11/TESTING_REPORT.md), real-model quality UNVERIFIED/BLOCKED | Per-agent supported/missing/contradictory/injected fixtures; real-provider quality measured separately; reviewer approval, citation/source revocation and privacy checks |
| Predictive model validity and promotion | Sprints 12–13 | Suitable authorized real history, temporal/entity split, leakage controls, predeclared target metrics, calibration and reviewed promotion; synthetic data is not production accuracy evidence |
| Retrieval scale and any pgvector/ANN replacement | Explicit retrieval extension and release work | Representative authorized corpus, relevance/latency/recall measurements and migration/rollback evidence; current bounds remain 20 chunks/index and 200 candidates |
| Production identity, email and external integrations | Relevant integration/identity work and Sprint 23 | Authorized environment/provider setup, all required journeys and templates, recipient/delivery evidence, revocation and failure handling; development Gmail journeys do not establish universal deliverability |
| Production storage, retention, physical/backup erasure and recovery | Relevant data lifecycle work and Sprints 22–23 | Real deployment topology, retention/erasure guarantees, backup policy, timed recovery and failure/rollback exercises |
| Accessibility, availability, security and performance release targets | Sprint 23 | Required end-to-end, assistive-technology, load, operational/security and deployment checks against an identified environment/revision |
| Archived learning/setup Word books | Documentation maintenance when republished | Content reconciliation, rendering and every-page visual inspection before treating an archived book as a current deliverable; the pilot guide has a newly verified current edition |

Provider authorization is still limited to the existing confirmed unbilled Gemini
project and maximum spend **$0**. This register grants no spending, deployment or
successor implementation authorization. See [release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md),
[roadmap](FUTURE_SPRINT_ROADMAP.md) and [development closeout](../10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md).
