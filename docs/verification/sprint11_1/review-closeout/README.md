# Sprint 11.1 review closeout — 23 October 2026

## Final code and evaluation disposition

CodeRabbit's final code review at `b83e726` completed with two optional nits.
Both are [addressed and validated](nit-followup.json): payload-free heartbeat
diagnostics and a coherent positive clear-finding control. The 95 offline/nine
runtime scopes pass; both full hosted runs at that reviewed base passed. The
latest coverage gate passed at **87.86%**. See PR #5 for checks on the nit follow-up.

**495 backend tests pass**, including the disposable database lifecycle/drift
checks, in 470.08 seconds. One inherited Starlette warning remains. The final
focused scopes are 95 offline acceptance/specialist checks and nine runtime DB
regressions, overlapping the full suite. The last regressions reject contradictory
`no_adverse_evidence`/adverse metadata and preserve worker cancellation arriving
during heartbeat cleanup. Both reproduced failures before their fixes.

Model qualification remains **BLOCKED**. All three evaluation workers stopped
after **20 new calibration requests / 42 role outputs**, with **zero evaluated-provider
held-out requests**. [Retained results](acceptance-stopped.json) reconcile every new
attempt with account ledgers. Gemini emitted three unsupported conditions in
absence cases; Groq executive synthesis also failed a required abstention. The
[independent 12-record output audit](output-audit-rejected.json) additionally found
unsupported privacy interpretation, weak restatements and contradictory metadata.
Hard validation was never counted as semantic accuracy.

The [108-case AI label pass](label-audit-pass.json) binds measured strategy `f9c761cd`.
The later deterministic guard and cleanup fixes change the current strategy to
`f5616c25`; earlier approvals/measurements cannot qualify that revised strategy.
The [fresh empty template](label-approval-template-current.json) prepares deliberate
review before future inference. Old approvals, attempts, failures and allocations
remain immutable history. No authorization is renewed, no model is promoted, and
no weight training or held-out prompt tuning occurred.

Normal schema 0012, seven disabled/unqualified profiles, $0 limits, Ollama stopped
and the 21 unrelated artifact changes are preserved. Required hosted checks and
the latest CodeRabbit review are visible on [PR #5](https://github.com/alokgupta001/AI-project-portfolio-manager/pull/5).
Sprint 12 is not started. Earlier entries below are point-in-time checkpoints.

## Earlier 493-test checkpoint

The final full backend/lifecycle/drift run passes **493 tests** in 474.52 seconds,
with one inherited Starlette warning. CodeRabbit independently [passed all 108
revised labels](label-audit-pass.json), including 54 held-out cases, at the exact
corpus/strategy hashes. The [frozen approval record](ai-label-approval.json) names
the AI reviewer and explicitly excludes human approval and measured accuracy.
The original empty template remains a template. Earlier failed and incomplete
audits remain evidence, rather than approvals.

A separately bounded acceptance sequence now uses that frozen strategy and
retains every provider attempt. The first four calibration calls cover all nine
roles and pass hard checks. Calibration precedes held-out inference; no prompt
tuning occurs during this sequence. Existing one-request/minute and twenty/day
account caps remain, with a maximum additional allocation of 36 calls/provider.
Each provider stops on its first invalid/unknown result or its existing cap.
Output review and measured qualification remain pending; profiles stay disabled.

The latest CodeRabbit code re-review is rate-limited. Its successful check status
does not mean the latest commit was reviewed. The first code review passed
docstring coverage at 92.35%; all four subsequent findings have verified fixes and
regressions. Latest hosted CI is still running. The [validation receipt](validation.json)
binds the full backend result to `880629d`.

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
