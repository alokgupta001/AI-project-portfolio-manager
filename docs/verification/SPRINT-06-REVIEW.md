> Resolution 2026-10-06: the findings below describe the original rejected implementation. Repairs and final local acceptance are recorded in [Sprint 06 checks](SPRINT-06-CHECKS.md) and the [report](../sprints/SPRINT-06-REPORT.md). Preserve this historical review.

# Sprint 06 independent implementation review

Date: 2026-10-06. Verdict: **Not accepted; incomplete implementation with correctness and security blockers.**

Reviewed the current working tree against ANTIGRAVITY.md, the canonical Sprint 06 prompt, master definition of done, permission and metric contracts, report and handoff. HEAD is f53d771 (Sprint 05); Sprint 06 changes are uncommitted. This review does not implement repairs or authorize Sprint 07.

## Findings

1. **P1 — Migration omits app write grants and tenant RLS.** `services/api/migrations/versions/0005_assessment.py:21` creates eight tables without policies or explicit write grants. On freshly migrated ppm_test, frameworks, assessments and answers have `relrowsecurity=false`, app SELECT=true and app INSERT=false. The initialization script grants default SELECT. Consequently normal app writes fail, while database reads have no tenant defense in depth. Add scope-aware policies and minimum grants, including immutable-version/event restrictions; verify with the actual app role and two tenants. HTTP queries do have some explicit tenant filters; this finding does not claim a demonstrated cross-tenant HTTP exploit.

2. **P1 — Migration and runtime metadata disagree.** `services/api/migrations/env.py:5` imports identity/delivery metadata but not assessment metadata. The existing guarded backend runner fails `alembic check`, proposing removal of the new assessment tables, and never reaches pytest. In addition, `0005_assessment.py:76` omits question `name` and `description`, although `assessment_tables.py:51` and `assessment.py:618` select/insert them; rubric-level metadata also contains `name` absent from the migration. Import and reconcile complete metadata, constraints and indexes, then pass clean/prior-state migration and drift checks. Preserve any migration already applied outside this reviewed local environment.

3. **P1 — Required frontend and evidence intake are missing.** `apps/web/components/shell.tsx:35` still declares maturity assessments a future module. No assessment page, editor, autosave UI, chart/table, comparison UI or browser acceptance test exists. The eight new tables and router provide no evidence attachment entity/upload/download path, despite the report/handoff claiming attachments. Evidence text is not secure file intake. Implement the required usable vertical slice and restricted attachment lifecycle before completion.

4. **P1 — Review can change answers belonging to another assessment.** `assessment.py:1334-1350` resolves adjustment answer IDs by organization only, without `assessment_id == id_`. A reviewer of assessment A can target a known answer ID from assessment B in the same tenant, including a completed or unassigned assessment. Restrict both lookup and update to the authorized assessment and preserve before/after adjustment history.

5. **P1 — Viewer and self-review restrictions are bypassed.** `assessment.py:1067` accepts any active member as respondent/reviewer, and answer/submit/review checks at 1167, 1270 and 1325 allow assigned users without an eligible-role check. A Viewer can therefore be assigned and perform prohibited writes. The self-review test at 1328 compares configured reviewer with assignee instead of the acting user; an Admin respondent can approve their own submission when a different reviewer is configured. Enforce eligible role plus assignment/scope and compare actual submitter/reviewer identities.

6. **P1 — Incomplete assessments can be finalized.** `assessment.py:1275` discards scoring warnings and submits without checking required answers; review at 1358-1379 similarly marks completed without completeness validation. Missing required answers, all-missing answers and invalid rubric answers can reach completed, with provisional or unknown scores and no explicit provisional state. Publishing at 889-932 checks only aggregate dimension weight and question count, allowing invalid/single-level rubrics and empty scoring dimensions. Validate frozen definitions at publication and required answers against that version before finalization.

7. **P2 — Coverage contradicts the metric contract.** `assessment.py:230-234` divides all numerically answered questions by the count of required questions. Reproduced: a required answer with 25% of question weight reports 50% coverage; one required plus one optional answer reports 200%. The metric contract requires weight coverage (25% in the first case), separate from evidence coverage. Required text answers also enter the denominator but never the answered count. Correct definitions, labels and tests.

8. **P2 — Concurrent edits and retries are not protected.** Assessment routes increment revision but never require an expected revision, condition updates on it, or use the existing write/idempotency machinery. Two autosaves can silently overwrite each other; repeated publish calls create additional versions, and concurrent publication can collide on max(version)+1. Reuse established locking, revision conflict and idempotency behavior, including negative tests.

9. **P1 — Claimed deployed checkpoint is false.** A read-only query of the normal ppm_local database returned `0004_capacity`; none of the eight assessment tables exists there. The handoff says `0005_assessment` is applied. Local healthy containers do not prove the new source is deployed. Forward migration and local runtime verification remain outstanding after isolated acceptance succeeds.

10. **P2 — Completion evidence and handoff are incomplete.** Coverage still marks Sprint 06 requirements Planned; no Sprint 06 checks document, updated scoring contract, ADR or changelog accompanies the work. The five tests cover helpers and structure, not workflow/database/browser acceptance. The report's contract evidence path `packages/contracts/src/openapi.json` is incorrect (actual file: `packages/contracts/openapi.json`). Replace the Complete/ready-for-Sprint-07 claims with an accurate incomplete checkpoint and link acceptance evidence after remediation.

## Checks performed

- `.venv/Scripts/python.exe -m pytest tests/test_assessment.py -q`: **5 passed**.
- `npm run contracts:check`: **passed**; agreement of generated files does not validate runtime/database behavior.
- `docker compose --profile test build test`: **passed**.
- `docker compose --profile test run --rm test`: **failed**, exit 1. Clean upgrade, downgrade/base and re-upgrade executed only against guarded disposable ppm_test. `alembic check` exited 255; full backend pytest was not reached. Log: [sprint-06-review-backend.txt](sprint-06-review-backend.txt).
- Read-only PostgreSQL inspection: normal database remains 0004_capacity; isolated database is 0005_assessment with missing RLS/write grants as above. No normal/demo data was migrated or downgraded.
- Direct scoring probes reproduced 50% instead of 25% weighted coverage and 200% coverage. Existing five tests do not detect these cases.
- Source review verified the missing frontend/evidence workflows and authorization/finalization issues. These route findings were not exercised as end-to-end authenticated HTTP exploits; migration/runtime blockers must be corrected before full acceptance.

## Repair order and acceptance handoff

1. Correct database metadata, schema and least-privilege RLS; pass migration/drift checks.
2. Correct assignment/reviewer authorization, answer ownership, finalization, rubric validation, concurrency and audit behavior; add integration/security regressions.
3. Implement assessment UI, secure evidence intake, compatible-version comparisons, charts/tables and history.
4. Demonstrate two departmental assessments, review/return/completion, republishing without changing old scores, weighted and all-missing cases, invalid rubrics, unauthorized requests, cross-tenant app-role behavior, CSRF and revision/idempotency handling. Save a worked score-difference fixture and browser evidence.
5. Run full regression/contract/static/security gates, then forward-upgrade the authorized normal stack while preserving the existing checkpoint/data. Correct coverage, report, checks, changelog and handoff. Do not accept Sprint 06 or advance on the current completion claim.
