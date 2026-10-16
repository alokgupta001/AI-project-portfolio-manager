# Sprint 09 checks

> Historical sprint checkpoint — documentation review, 16 October 2026. The original outcomes, schema/version and stop-at-next-sprint statements below describe their recorded date. For today's availability and safe setup, use [current status](../../../00-overview/CURRENT_STATUS.md) and [documentation closure](../../../10-reference/PREVIOUS-SPRINTS-DOCUMENTATION-CLOSURE.md).

15 October 2026; base b98110e plus uncommitted Sprint 09. No hosted-CI revision claim.
Accepted locally. Read the
[report](../../../03-sprints/completed/sprint-09/SPRINT_REPORT.md) for scope/limitations.

| Command / environment | Result | Evidence under docs/verification |
| --- | --- | --- |
| docker compose -f compose.yaml -f compose.documents.yaml --profile test run --rm --no-deps test python scripts/test_backend.py | 123 passed, one inherited warning, 320.63 s; clean/prior/base/repeated migration and drift | sprint09-backend-final.txt |
| Same isolated runner: python -m pytest -q tests/test_documents.py tests/test_document_parser.py | 24 passed, 117.84 s | sprint09-documents-final.txt |
| Final runner: python scripts/check_document_migration.py | prior-head downgrade/upgrade and no drift | sprint09-migration-accepted.txt |
| Final runner: python -m pytest -q tests/test_documents.py | 9 passed, 52.04 s, latest authority/retention/immutability changes | sprint09-security-accepted.txt |
| node scripts/check-identity-browser.mjs | 14 regressions passed; new source flow found a save/reopen race, repaired | sprint09-browser-all.txt |
| node scripts/check-identity-browser.mjs tests/browser/documents.spec.ts | PASS: final document journey, 1 passed in 34.4 s (sprint09-browser-accepted.txt) | sprint09-browser-accepted.txt |
| python -m ruff check services scripts tests; python -m ruff format --check services scripts tests; python -m mypy services/api/ppm_api services/worker/ppm_worker | PASS; mypy 36 source files | sprint09-ruff.txt; sprint09-python-format.txt; sprint09-mypy.txt |
| npm run typecheck/lint/format:check/contracts:check | PASS; generated OpenAPI/types authoritative | sprint09-types.txt; sprint09-lint.txt; sprint09-format.txt; sprint09-contracts.txt |
| npm audit --audit-level=high; pinned pip-audit on uv-exported locked set | no known vulnerabilities after pypdf 6.20.1 | sprint09-npm-audit.txt; sprint09-python-audit-final.txt/json |
| python scripts/check_sources.py | seven original sources/prompts unchanged | sprint09-sources.txt |
| python scripts/sprint09_recovery.py capture/restore | 62 tables + five objects match original normal backup in scratch | sprint09-recovery-capture.txt; sprint09-recovery-normal.txt |
| python scripts/sprint09_document_recovery_run.py | 67 table hashes/counts + one fixture original, signed download and citation match in scratch | sprint09-recovery-documents.txt |
| Quiesced scripts/sprint09_preserve.py before/after rollout and recovery.py verify | PASS: head 0011_document_sources applied; healthy restart/worker; 62 quiesced table hashes/counts, five object hashes and ten frozen migrations preserved; retains intervening refresh-token activity | sprint09-preservation-rollout.txt; sprint09-preservation-final.txt |

Synthetic fixture matrix: two tenants, Admin/PM/Viewer; eight document categories;
TXT/CSV/DOCX table/XLSX formula omission/text PDF/scanned PDF/PNG/JPEG; corrupt/mismatched,
active/EICAR/oversize files; escaped prompt-injection text; unknown digital confidence;
duplicate bytes/concurrent retry; revision/CSRF/stale organization; 125 paged metadata
rows; revoked grants and queued/in-flight work; expired/tampered tickets and bytes;
latest-version citation invalidation; replay/reprocessing; retention/holds/purge;
archived held sources excluded from GC; completed assessment row unchanged and Viewer
private references hidden. Real ClamAV and Poppler/Tesseract checks are separate from
explicit scanner transport doubles used for deterministic dependency failures.

Keyword evaluation: eight labeled synthetic distinct-keyword queries, eight expected
category/source/paragraph locations, 8/8 top-1. This is a baseline, not production
retrieval or semantic accuracy. Embeddings/hybrid/findings remain pending 10/11.

Screenshots at 1440/768/360 are `sprint09-documents-{width}.png`. Automated accessibility
and body-overflow checks do not certify full assistive-technology/WCAG compliance.
Visual review caused a real mobile table repair, not merely screenshot generation.

Earlier failed logs remain. The worker harness retains an actual SIGKILL, unchanged
45-second lease, restart attempt 2 and exactly 500 unique effects, with a larger
bounded polling allowance for loaded Compose execution. No runtime SLA is inferred.

Normal data is never reset/restored/purged. All lifecycle resets are guarded test DB
operations. Private dump/object/token/fixture contents remain ignored under artifacts/local;
CI artifacts no longer include that directory. Existing 8.1 hosted-CI/Word gates stay open.


Regression screenshots/JSON produced under older sprint names were copied to sprint09-regression-* and their original committed artifacts restored. See sprint09-regression-preservation.txt. An additional parser chunk-budget boundary passed (sprint09-chunk-limit.txt), preventing ready sources that exceed preview paging limits.

## Documentation reconciliation follow-up

[Documentation closure](DOCUMENTATION_CHECKS.md) covers corrected current scope,
learning, user/demo/setup guides, generated inventories, tracker/mapping and local
link/source checks. No application, data or migration suite was rerun for this
Markdown/tooling follow-up; the commands/results above remain their recorded evidence.
