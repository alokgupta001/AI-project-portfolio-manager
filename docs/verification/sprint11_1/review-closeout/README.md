# Sprint 11.1 review closeout — 23 October 2026

## Follow-up after independent AI review

CodeRabbit's first code review passed docstring coverage at **92.35%** and found
four further issues. Source order is now normalized in version 3 evidence roots;
earlier ledger versions remain blocked without resetting their history. Unknown
call outcomes retain `unknown` ledger status. The pre-existing unconditional
RUNNING-task replay guard already prevented a new send; explicit Groq/Ollama
cancellation/resume tests now verify it. Cancellation also propagates if settlement
itself fails. Two origin/storage-path docstrings now match their actual checks.
Current focused scopes pass: **53 benchmark tests**, **8 runtime database cases**,
and **94 benchmark/acceptance/specialist tests** (overlapping scopes).

The [separate label audit](label-audit-round-1.json) examined all 108 cases and
declined approval: 18 negative cases were ambiguous, one governance scenario was
duplicated across splits, and Windows CRLF exports did not match Git's LF hash.
The 18 evidence drafts now explicitly state the condition is unestablished; the
held-out governance case uses a distinct documented-only exception review (level 1).
New immutable exports use LF, covered by a Windows regression. The fresh request
and empty approval template bind the revised corpus and strategy. Historical
packets remain unchanged. A new independent audit is required before inference.

The final full suite is rerunning with these changes; the 487-pass checkpoint
below is retained history. One obsolete intermediate run was deliberately stopped
and retained rather than reported as a pass.

## Initial verified fixes

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
pass. Full disposable database lifecycle and schema-drift checks passed, with
**487 backend tests passing in 466.83 seconds** and one inherited Starlette
deprecation warning. See the [validation receipt](validation.json).
No real provider calls were made.

[Documentation audit](documentation-audit.json) records 186/186 documented
production Python functions across the original sprint's non-migration files,
up from 7. Executable ASTs match the merged base in all files changed only for
documentation. Runtime, benchmark and draft-authoring files contain the intentional
changes described above. Applied migration files are unchanged. OpenAPI descriptions and
source inventories were regenerated. This is local Python coverage, not a claim
about CodeRabbit's independent cross-language metric.

The fixes are published in [PR #5](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/5).
Hosted CI and CodeRabbit code review are in progress. The user asked us to arrange
evaluation review rather than nominate a reviewer. The
[separate AI review request](review-request.json) binds the current 108-case corpus
and revised source strategy. The [approval template](label-approval-template.json)
is intentionally empty. The [CodeRabbit request](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/5#issuecomment-6353350329)
asks the audit to identify ambiguity by case ID and declare
any unreviewed scope before any approval is considered. AI review is recorded as
AI review, not human approval. No held-out inference, qualification or activation
has occurred. Earlier calibration receipts, exhausted budgets and strategy hashes
remain historical evidence.

Normal data remains on schema 0012, with v2 providers disabled and $0 spend limits.
Ollama stays outside project routing. The 21 unrelated older verification artifact
changes remain outside this follow-up. Sprint 12 is not started.
