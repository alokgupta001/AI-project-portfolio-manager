# Trace a specialist finding through human review

The business problem is a reported Green project with an overdue critical
milestone, or a maturity answer whose text differs from its numeric checkbox.
Sprint 11 adds evidence-backed review candidates while preserving both originals.

`agents.create` delegates admission to `ai.create`. `agents.capture` calls the
existing `command.snapshot`, authorizes selected source versions and private
assessment text, and stores hashes, source spans, framework and revision. The
same transaction creates AI ledger/job/outbox records. Migration 0013 adds
snapshots and decisions without another queue or a scoring formula.

`ai_worker` claims the existing fenced lease and dispatches `agents.execute`.
`AgentProvider` uses the unchanged fixed-origin transport/model gates.
`Runtime.call` admits and precharges every attempt before dispatch, retaining
the six CodeRabbit accounting fixes. One completion batches nine specialists;
at most two attempts stay inside existing ceilings. Intercepted responses and
`test_agents.Double` exercise this flow without calling a provider.

`agent_engine.INPUTS` defines each specialist's source allowlist. `supported_spans`
rejects foreign/unauthorized/stale references and impossible offsets. Strict
Pydantic models reject tool/action/reasoning fields, unsupported confidence and
malformed shapes. These checks prove support references and bounded behavior;
they cannot prove that a model interpreted a paragraph correctly.

`deterministic` preserves the shared critical-milestone discrepancy even when
the provider fails. `aggregate` merges same category/signal/source sets using
stable hash keys, unions provenance, takes highest severity/lowest confidence,
and exposes opposing signals as linked conflicts. A failing/missing agent
does not become a fabricated success.

For maturity, `semantic_suggestions` matches only exact published rubric levels
with permitted dimension text. It calls `assessment.compute_scores` with those
matches and separately with original answers. In the fixture, original 0 and
suggested 87.5 coexist; an independent reviewer can approve 75 with a reason,
then reject it while both decision records remain. Nothing writes an assessment
answer, assessment result or delivery plan.

`agents.current_sources` recaptures current authorized inputs. `publish` and
every read/review repeat the support check. A new source version, changed answer,
revoked project/assessment scope or group suppression withholds unsupported
evidence. `agents.review` locks the tenant, rechecks independent authority,
If-Match and idempotency, then inserts an immutable decision. Review comments
are never prompt inputs. React renders source text/comments as text.

To debug, start with safe stage/code fields, source snapshot hash and exact
versions. PROVIDER_DISABLED/QUOTA/TIMEOUT/MALFORMED are honest degraded states.
CONFIGURATION_CHANGED requires a new run. EVIDENCE_CHANGED requires current
sources, not a retry against revoked bytes. A lost lease never publishes a late
output or silently starts another provider attempt. Inspect ambiguous calls
before creating another run. Do not log keys, raw provider responses or prompts.

Run the [test commands](../../04-testing/sprint-based/sprint-11/TESTING_REPORT.md)
and [demo](../../05-demos/sprint-based/sprint-11/README.md). The trained sentiment,
historical model, free-form copilot, generic approvals/actions and production
quality/scale gates are separate future work. Sprint 12 has not started.
