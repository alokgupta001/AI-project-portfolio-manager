# Sprint 12 actual validation

## Final application checkpoint — 26 October 2026

Application `f93a596` passed both hosted Foundation workflows and CodeRabbit's final
review produced no actionable comments. Normal schema is 0018. [Closeout](../../../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md)
and [review evidence](../../../verification/sprint12/REVIEW_FIXES.md) identify exact
commits, commands and repaired failures. The 36-case final affected-path run, the
separately strengthened case and six final browser journeys passed; they overlap.
The earlier full local gate passed 535/one skipped before the last two source fixes;
the subsequent hosted workflows cover final application regression. Do not add counts
across runs or claim synthetic scores as real-world accuracy. AT17 remains BLOCKED.

## Documentation refresh — 26 October 2026

Validation is recorded in
[the command receipt](../../../verification/sprint12/documentation-final-checks.json).
It checks Markdown links/anchors, prior-sprint packages, generated inventories,
source hashes, Ruff/mypy, generated contracts and frontend static checks. PostgreSQL
UUID/timestamp type rendering was compared with the normal schema read-only. Original
26 frozen inputs, applied 0017/0018 hashes and the 21 pre-existing artifacts remain
unchanged. Application code, tests, locks, migrations and runtime configuration are
unchanged by this refresh; the preceding application CI/review evidence is retained.
No new local application/browser regression run or live/model qualification is claimed
for a documentation-only change. Newly triggered hosted CI is a separate result.

## Original implementation checkpoint — 25 October 2026

25 October 2026. **LOCAL SAMPLE ACCEPTED; full original live/model acceptance OPEN.**
Starting HEAD `c192d69a49c55240876d22c641360d44522d1eba` plus uncommitted work.
Raw receipts/starting diff/dump/hashes are private in `artifacts/local/sprint12`.
[Public evidence](../../../verification/sprint12/README.md).

26 October PR follow-up: [review findings and fresh checks](../../../verification/sprint12/REVIEW_FIXES.md)
supersede the original 0017 validation checkpoint below. Normal schema is now 0018;
all established data hashes and frozen inputs remain unchanged. The original tests
remain evidence for their recorded commit, not a claim about subsequent fixes.

| Command / environment | Actual result |
| --- | --- |
| `docker compose --profile test run --rm -T test` (guarded ppm_test/test) | **528 passed, 1 skipped**, 832.89 seconds; one inherited Starlette deprecation warning |
| Same runner migration stages | Head → 0006 → head → base → head → head; `alembic check`: no drift |
| `pytest tests/test_sprint12.py tests/test_jobs.py -q` in isolated app-role DB | **27 passed**, 143.06 seconds, before the final remote namespace narrowing |
| Windows `pytest tests/test_sprint12.py -m "not integration" -q` | **14 passed**, four integration cases deselected, 12.31 seconds; includes final provider identity narrowing |
| Current mounted source `pytest tests/test_sprint12.py -m integration -q` | **4 passed**, 14 offline cases deselected, 21.29 seconds; final source mounted read-only |
| `PPM_TEST_AI_V2=1 node scripts/check-identity-browser.mjs sprint12.spec.ts integrations.spec.ts guided-review.spec.ts guided-access.spec.ts --workers=1` | **5 passed**, 2.3 minutes; cloud/Ollama disabled |
| Earlier serial identity browser regression | Identity lifecycle plus guided-access/review and ingestion passed (four); first lab locator failure repaired |
| Contracts, TypeScript, ESLint, Prettier | All pass; [exit-code receipt](../../../verification/sprint12/frontend-checks.json) |
| Ruff lint/format, mypy, source hashes, generated inventories | All pass; [exit-code receipt](../../../verification/sprint12/backend-static-checks.json) |
| npm audit + pinned exported-lock pip-audit | Zero npm vulnerabilities; no known Python vulnerabilities |
| Markdown links/inventories | Final command receipt is in the public evidence folder; all local links/anchors resolved |
| Normal forward upgrade and startup | 0016 → **0017**; API/web/worker/dispatcher healthy; `/ml` HTTP 200 |
| Preservation | **77** established table counts/hashes, **26** frozen file hashes, **5** object byte/key hashes unchanged; all **8** original job/AI associations also matched the full starting dump |
| Runtime read-only verification | Gemini/Puter/Groq, shared **50/day**, **one/minute**, concurrency 1, spend limit **0**, Ollama off; **zero inference requests** |

The full image gate precedes the final provider namespace narrowing; the current-tree
offline/focused checks supplement it without claiming another full-image run. Fixture
size is 90 aggregate observations per target with 30/30/30 splits; direct API tests use
two real app-role tenants. Five compatible target types reproduce exact result hashes
in a pinned environment (documented tolerance 1e-10). Synthetic metrics are never
reported as real-world accuracy. Browser checks include zero Axe violations, no page
horizontal overflow at 1440/768/360 and visual inspection; mobile comparison tables
scroll with keyboard focus. Conflict UI shows current local/candidate values.

## Failures found and repaired

- Initial ingestion regression expected `LOCAL_REVISION_CONFLICT`; retained that code
  while adding durable source review.
- Disposable downgrade initially encountered ML job rows. It now deletes only those
  new job children/rows during guarded downgrade, never normal data; lifecycle passes.
- A new test was inserted inside another test's setup; split/reordered it correctly.
  This caused the earlier 527-pass/one-failure run, now superseded by the green full run.
- Parallel guided browser cases competed for the same tenant's concurrency limit;
  serial execution preserves the existing guard. New namespace field added a valid
  keyboard tab stop and the regression now checks it.
- Controlled textarea exact-label lookup changed with content; explicit aria-label
  fixes it. Web proxy initially retained the old 16-KB generic body ceiling; ML now
  shares the existing bounded 650-KB streaming import path. API limits were retained.
- Initial normal migration invocation used the old separate image and left 0016
  unchanged; rebuilding migrate applied 0017, followed by full preservation checks.

## Retained gates

No connector credentials were configured; live Jira/GitHub equality/recovery is
unverified. No completed projects/closed sprint snapshots or complete genuine outcome
history existed. Organization-attested manual data is not independently verified.
No external real dataset was downloaded: license and exact-target suitability review
is still required. Native MLflow tracking/import and XGBoost/DistilBERT comparisons
remain explicit limitations. AT17 remains BLOCKED. Publication and application hosted
CI are now verified in the closeout. No serving/promotion, production deployment, merge
or Sprint 13 work is claimed.
