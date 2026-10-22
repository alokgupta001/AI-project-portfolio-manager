# Risk register and explicit unknowns

Status: planning decisions selected; implementation not started. Risk severity concerns potential implementation impact, not an incident claim.

| ID / severity | Unknown or risk and why it matters | Evidence missing | Default / mitigation | Owner and revisit trigger |
| --- | --- | --- | --- | --- |
| K01 high | Qwen3 4B CPU latency may exceed 22 s/90 s limits | Actual machine/Ollama timing | Single model/slot, 4096 context, bounded sections; deterministic fallback; no latency promise | T12; measured p95 or cold failure |
| K02 high | 16 GB host can page under Docker/browser/model | Measured peak and host RAM | 2 GB headroom, conservative model envelope, no simultaneous chat/embedding models | T05/T12; OOM/headroom breach |
| K03 high | Semantic output can cite irrelevant real evidence | Independent case labels/model runs | Distinguish hard validation from interpretation; human review and optional critique; no confidence-based correctness | T09/T12; unsupported claim in held-out set |
| K04 high | Free tier/billing can change outside application | Current account/project tier and provider enforcement | Cloud off by default; non-billable account verification, fixed allowlist; no paid fallback | Operator/T06/T13; key/project/model/tier or terms change |
| K05 high | Provider quotas shared across tenants/keys | Account-specific active limits | Shared provider-scope ledger plus tenant limits; conservative unknown attempts; quotas required before enablement | T03/T06; new account scope or 429 |
| K06 high | Source checkout 0014 versus historic normal 0012 | Read-only actual DB revision/deployed image | Never upgrade normal DB during planning; T01 checks before rollout | T01; deployment request |
| K07 high | Worker crash between request and response ambiguous | Provider idempotency guarantees unavailable | Exactly-once local publication only; do not replay unknown external attempt; preserve sections | T08; crash-injection test |
| K08 high | Global quota table could leak tenant information | New RLS/function negative tests | Owner-only tables/narrow fixed-search-path function; return safe denial only | T03; any forged scope/direct SELECT succeeds |
| K09 high | Stale evidence/reference access in durable results | New item-level authorization tests | Live read/accept/inference checks; invalidated dependencies withheld; assessment revision global to its derived results | T07/T11; source edit/tombstone/grant change |
| K10 medium | 512 tokens cannot cover all rubric questions or rich findings | Token fit per model/schema | ≤2 items/section, three initial sections, exact deferred IDs; no automatic new-run expansion | T07/T12; useful small fixtures cannot fit |
| K11 medium | Coarse old duplicate key merges distinct issues | v2 claim fixtures | Preserve old history; v2 normalized claim identity and potential-duplicate links | T09; false merge or conflict |
| K12 medium | Lower-quality fallback silently degrades advice | Per-task model qualification | Hard minimum quality before ranking; explicit degraded route; abstain if unqualified | T06/T12; fallback fixture failure |
| K13 medium | Embedding dimensional/model mismatch | Installed EmbeddingGemma 256 API behavior and retrieval quality | Keyword default; no manual vector trimming; one selected projection, explicit rebuild | T13; dimensional/cosine mismatch |
| K14 medium | No native Ollama executable found on PATH | Actual installation/runtime availability | No install assumed, no download; mock-first adapter and documented setup | T05/T12; operator setup |
| K15 medium | Native host listener inaccessible from Docker or publicly exposed | Network/firewall proof | Private Compose service if secure native route unavailable; no public bind workaround | T05; endpoint isolation test |
| K16 medium | Repeated retries/decomposition bypass limits | Counter/transaction tests | Shared root attempt budget, max24 nodes, depth1, four calls, absolute deadline | T08/T10; failure-injection loops |
| K17 medium | Raw text/secrets in logs/errors | Redaction/security tests | Persist codes/hashes and approved snippets only; no thought or raw malformed payload storage | T04/T11; test leakage |
| K18 medium | Blueprint drifts with subsequent code | Source diff at implementation | Baseline commit, T01 check, explicit conflict log and affected-task stop | Sol; any verified contradiction |
| K19 medium | Hardware gates too strict for useful semantics | Benchmark case failures | Do not silently lower gate; smaller model/scope first, documented alternate local profile only after evidence | Architect/operator; all candidates fail |
| K20 low | Expanded runtime complexity burdens student maintainer | Implementation effort feedback | Native modules, existing queue; no framework/service sprawl; ordered small tasks and single default profile | T14; module/state maintenance becomes disproportionate |
| K21 high | All nine roles can reason, but four attempts cannot guarantee nine AI interpretations | Per-goal plan fixtures and benchmark results | Goal-aware selection, reserved synthesis slots, separate base/semantic coverage and exact deferred work; no hidden budget increase | T07/T11/T12; full-nine request mislabeled complete |
| K22 high | New financial/schedule/resource or synthesis inputs could broaden data access | Role context/derived-evidence security tests | Explicit target allowlists, minimal text windows, no raw personnel notes, live original-source checks even for accepted upstream findings | T07/T09; any dependency bypasses scope/privacy |

## Intentionally configurable decisions

Exact installed model digest, task-specific eligible profile priority, private endpoint profile, measured memory reservation, provider request/token caps, tenant egress allowlist and later embedding enablement. Configurability never permits bypassing the initial 512/four/90 limits, role/privacy policy, hard validation or authorized spending. Changing those invariants needs a new documented decision and tests.

## Explicitly deferred work

General conversational PMO assistant/multi-turn state (Sprint 14), predictive causal/impact models and historical labels (12–14), optimization/plans/approval execution, mature team sentiment, large vector index, multi-model embeddings, automatic business actions, production HA/scale and multi-day workflows. This architecture provides extension seams without claiming these are implemented.

## Qualification and access limitations

This sprint inspected repository source, ran offline tests and static documentation/contract checks, and read running-container health labels. It did not query normal data, apply migrations, rerun browser/integration suites, install models, benchmark hardware or call inference providers. Public provider documentation was checked; account billing/quotas/egress policy were not. The exact installed Ollama state and normal DB revision remain open. These are bounded implementation prerequisites, not hidden architectural choices.

The hybrid-role revision is documentation-only. It enables interpretation contracts across all nine roles; it does not prove model quality, authorize new data categories at runtime, or change live output/time/spend limits. Sentiment remains a privacy-safe team support capability until a separately reviewed text-data contract exists.
