# Quality, security and operational limitations

26 October 2026. Current local sample: Sprint 12 at normal schema **0018**. [Reviewed closeout](../10-reference/SPRINT-12-LOCAL-CLOSEOUT.md) records application commit `f93a596`, both passing hosted CI runs and CodeRabbit's final review with no actionable comments. Live connectors/genuine model quality remain unverified and AT17 remains BLOCKED. Earlier dated checkpoints below retain their original scope; stop before Sprint 13.

Use the local history/dataset/baseline walkthrough linked from the closeout and
`/integrations` for authority/conflict review. Synthetic results are not real accuracy;
existing guided-provider quotas, access and $0 controls remain unchanged.

Current closeout: Sprints 8.1 and 10 are completed for development scope; hosted CI and the current pilot Word guide are verified. Broad agent/model quality, production and scale remain successor/release gates. See [acceptance disposition](../10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md). Earlier dated evidence below retains its historical scope.

[Current limitations](../00-overview/CURRENT_STATUS.md) identifies snapshot bounds, evidence/file transaction limits, notification presentation retention, SSE polling cost and open external/release gates. [Security walkthrough](../02-learning/05-security/AUTHENTICATION_AND_AUTHORIZATION.md) explains live membership, RLS, roles/grants/ownership and private effort. [Test strategy](../04-testing/TESTING_STRATEGY.md) maps negative cases; [Release criteria](../00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md) retains performance/recovery/accessibility obligations. Existing local checks do not imply independent security certification, production throughput or full recovery acceptance.

## Sprint 09 boundaries

Document sources are scanner-gated and bounded; unavailable ClamAV quarantines and
has no manual bypass. English OCR confidence is recognized-word confidence, not
accuracy. Keyword search is not semantic inference and its synthetic 8/8 queries do
not measure production relevance. Source ownership never bypasses project/private
assessment authority. Version bytes are immutable; delete revokes reads immediately,
eligible explicit purge retains tombstones. Archived-project holds protect orphan GC.
Pilot retention defaults to 30 days; backup erasure/production storage/recovery,
hosted CI and archived Word visual acceptance remain open. Read the [contract](../contracts/documents.md),
[operator guide](../07-setup-and-deployment/DOCUMENT-PROCESSING.md) and
[actual checks](../04-testing/sprint-based/sprint-09/TESTING_REPORT.md).
## Sprint 10 acceptance limits

Defaults remain disabled; the configured local Gemini free tier is authorized at $0 and its bounded smoke passed. Broader quality remains unverified; deterministic support gates
are not real-model accuracy. JSONB vectors support only 20 chunks/index and 200
permitted semantic candidates with keyword fallback; pgvector/ANN scale is not
accepted. Conservative USD charges are not invoices. No semantic agents, private
reasoning, automatic plan edits, hosted CI, archived Word visual QA, full WCAG
certification or production readiness is claimed. See the active Sprint 10 handoff.
