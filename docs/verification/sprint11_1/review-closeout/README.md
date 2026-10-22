# Sprint 11.1 review closeout — 23 October 2026

PR #4 merged at `72e0b8e` after both hosted foundation checks passed. The following
four CodeRabbit findings were verified against that merged code and reproduced
before the fix:

| Finding                                                   | Change                                                                                        | Regression evidence                                                                                                      |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Local benchmark retries could reset with request metadata | Bind quality roots to model digest, role, sources and rubric; fail closed on old opaque roots | Two attempts survive output/corpus/case-name changes; legacy ledger bytes remain unchanged; warm timing remains separate |
| Worker cancellation became a normal failure               | Settle the admitted attempt as unknown, then re-raise cancellation                            | Worker task stays cancelled; one call settled as `CANCELLED`/unknown; no later provider call                             |
| Oversized context reached the database constraint         | Reject serialized context above 80 KB before binding, below the existing 90 KB database limit | No model call or bound context; `CONTEXT_LIMIT` and useful baseline produce an explicit partial result                   |
| Heartbeat cleanup replaced the main outcome               | Contain heartbeat task errors during cleanup                                                  | Database, cancellation and deadline heartbeat failures cannot replace a completed baseline result                        |

The focused checks pass: **50 benchmark tests** and **5 database regressions**.
These scopes overlap the full suite. Ruff, formatting, mypy (65 modules), generated
contract drift, frontend lint/typecheck/format and seven preserved source hashes
pass. Full disposable database lifecycle/backend verification is running; its final
result will be recorded before closeout. No real provider calls were made.

[Documentation audit](documentation-audit.json) records 186/186 documented
production Python functions across the original sprint's non-migration files,
up from 7. Executable ASTs match the merged base in all files changed only for
documentation. The two runtime/benchmark fix files contain the intentional logic
changes above. Applied migration files are unchanged. OpenAPI descriptions and
source inventories were regenerated. This is local Python coverage, not a claim
about CodeRabbit's independent cross-language metric.

The user asked us to arrange review rather than nominate a reviewer. The
[separate AI review request](review-request.json) binds the current 108-case corpus
and revised source strategy. The [approval template](label-approval-template.json)
is intentionally empty. The audit must identify ambiguity by case ID and declare
any unreviewed scope before any approval is considered. AI review is recorded as
AI review, not human approval. No held-out inference, qualification or activation
has occurred. Earlier calibration receipts, exhausted budgets and strategy hashes
remain historical evidence.

Normal data remains on schema 0012, with v2 providers disabled and $0 spend limits.
Ollama stays outside project routing. The 21 unrelated older verification artifact
changes remain outside this follow-up. Sprint 12 is not started.
