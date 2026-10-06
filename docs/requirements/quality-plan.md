# Acceptance evidence and quality plan

This plan specifies future verification; no application performance or security result is claimed in Sprint 00. Each requirement's coverage row is closed only by evidence of actual implementation behavior. The Sprint 00 documentation checks are recorded separately in [verification](../verification/SPRINT-00-CHECKS.md).

## Core verification layers

| Layer | Required evidence when relevant | First owner |
| --- | --- | --- |
| Source/contract integrity | Copies hash-match, IDs unique, local links valid, changes versioned | 00 |
| Runtime setup | Exact install/start/check commands and exits from fresh checkout | 01 |
| Persistence | Real PostgreSQL migrations from empty and previous supported schema | 01 onward |
| Authorization | Actual application DB role; two tenants, all roles, foreign IDs and revocation | 02 onward |
| UI | Responsive states, keyboard/focus/contrast review and screenshots | 03 onward |
| Metric correctness | Known-value fixtures including null/zero/currency/calendar boundaries | 04 onward |
| Jobs | Kill/restart, duplicate event, expired lease, queue outage and reconciliation | 08 |
| AI/RAG | Citation existence/access, injection, malformed output, budgets and abstention | 09–11 |
| ML | Frozen holdout, temporal/entity split, baseline comparison, leakage check, calibration where relevant | 12–13 |
| External adapters | Contract fixtures plus explicitly separate live-provider verification | 08 onward |
| Release | Full journeys, security/accessibility regression, backup restore, deployment rollback | 23 |

## Proposed performance measurement profiles

Source targets need conditions; these profiles are proposed test defaults to refine before measurement, not a production capacity promise. Use a documented 4-vCPU/8-GB API test host with separate database/worker capacity, 50 concurrent authenticated users, two isolated fixture tenants, up to 1,000 projects per tenant and 100,000 work items. Record actual hardware, service sizing and seed counts with results. Test no-load separately from concurrent behavior.

| Target | Measurement definition | Release evidence |
| --- | --- | --- |
| Login under 1 second | p95 complete login API response including bcrypt verification, excluding human interaction/network beyond stated profile | At least 1,000 attempts under declared mix/load; errors separately |
| FCP under 2 seconds | Authenticated dashboard cold navigation on named browser/device, with stated cache/network profile | Repeated runs and median/p95, same data scope; baseline and optimized results |
| 60fps chart target | Representative chart hover/filter/pan interaction; 16.7 ms frame budget at 60 Hz | Frame-time distribution and dropped frames, trace plus dataset size; no universal all-device guarantee |
| Live dashboard update | Proposed p95 10 s from accepted backend source event to visible update | Correlated timestamps and SSE reconnect test; upstream polling lag reported separately |
| Instant risk alert | Proposed p95 60 s from committed qualifying trigger to provider acceptance | End-to-end trace; provider delivery/read time excluded and explicitly stated |
| 99.9% alert worker availability | Healthy minute if synthetic notification can be processed within configured deadline; successes / scheduled minutes | Rolling 30-day observation, missing observations unhealthy; deployment test alone cannot prove SLO |

At 30 days, 99.9% availability permits 43.2 unsuccessful minutes by this minute-based definition. Also track queue age, failed jobs, provider failures and acceptance latency so availability cannot hide stuck customer deliveries. Recovery time and data-loss objectives must be chosen before production; record actual restore results rather than inventing RTO/RPO attainment.

## AI and ML evaluation gates

Before agent release, build a labeled set of answerability, evidence correctness, permission boundaries and failure cases. Access leakage and unauthorized tool execution are zero-tolerance failures. Set task-quality thresholds before scoring the final evaluation set. Schema validity is necessary but not sufficient; unsupported confident answers count as failures.

For regression report MAE and error quantiles versus simple baseline; for imbalanced classification report PR-AUC, precision/recall by threshold and class counts; probabilities need calibration/Brier analysis. Evaluate time/entity-separated holdout and record out-of-domain limits. Exact promotion thresholds cannot responsibly be chosen without task labels, sample sizes and costs; Sprint 12 must freeze them before model selection, and unavailable suitable data remains a documented promotion blocker. Do not claim one model solves all targets.

## Documentation checks at Sprint 00

Run `./docs/verification/check-sprint-00.ps1` from the project root. The script checks preserved-file hashes, sprint sequence, unique coverage IDs, required planning artifacts, balanced Markdown fences, local link targets, and absence of application scaffolding. It writes the verification report. These checks do not prove architecture optimality, application functionality or future feature completeness; source-to-feature coverage is also manually reviewed against both originals.
