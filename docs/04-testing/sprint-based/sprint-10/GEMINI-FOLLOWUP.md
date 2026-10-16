# Gemini $0 follow-up — 16 October 2026

## Update: daily expiry removed at the user's request

The existing verified key/project confirmation no longer expires after 24 hours.
No daily renewal or key re-entry is required. Tests now exercise old confirmation
timestamps through the adapter and database runtime; zero-dollar gates, approved
models, key binding, authorization, rolling request-count limits and quota fallback
remain unchanged. The original verification below records the earlier version;
its expiry-related results are historical, superseded by this update.

Verification after expiry removal: **63 AI/provider regression tests passed in
54.21 seconds** on isolated `ppm_test`, with external provider access blocked by
fixtures. Confirmations aged two days and ten years pass the adapter gate; the
database runtime accepts a one-year-old confirmation and still enforces its
persistent request limit. Ruff, mypy, TypeScript, ESLint, Prettier and generated
contract checks pass. Updated documentation validation: 294 Markdown files and
4,538 local links/anchors, zero missing at that check. The application was rebuilt
for reload with the existing key/project settings; no new real AI request or
database migration is needed for this change.

This user-authorized follow-up adds Gemini free-tier support without changing the
original Sprint 10 checkpoint or asserting general provider-quality acceptance.
The user confirmed no linked billing account and supplied the project ID.

## Evidence

- Real synthetic smoke: completion exact-quote/citation check passed; input 149
  tokens, output 67 tokens including any reported thinking. Embedding 2 returned
  256 finite dimensions. Its token usage is unknown, not fabricated.
- [Redacted smoke record](../../../verification/gemini-free-tier-smoke.json).
- Real requests were confined to the operator-confirmed Free Tier project;
  no billing setup, credit purchase, paid provider, paid model, production
  deployment, root `.env` change or database migration was performed.
- Original disabled-provider screenshots/checkpoints remain historical evidence.
- Final AI/provider regression suite: **62 passed in 52.71 seconds** against the
  isolated `ppm_test` database with real network access prohibited by the fixtures.
  Includes zero-budget admission, persistent request limits across runs, quota
  fallback without completion, expiration, disabled keys, paid model/tariff
  rejection, malformed/partial responses, opaque signatures, redacted HTTP errors,
  redirects, timeouts, and existing authority/cancellation/citation checks.
- Isolated Chromium UI scenario: **1 passed in 5.4 seconds** after final wording
  changes. Active free-tier disclosure, source/data-use notice, optional embedding
  disablement, and paused recovery pass. Backend real providers stay disabled;
  the UI's Gemini status response is explicitly intercepted for this scenario.
  [New screenshot](../../../verification/gemini-free-tier-ui.png) was visually
  reviewed separately from the retained Sprint 10 screenshots.
- Ruff lint/format, mypy (42 service files), TypeScript, ESLint, Prettier and
  OpenAPI/generated contract checks pass. No public schema fields/routes changed.
- Documentation link/coverage validator: 280 Markdown files, 4,355 local
  links/anchors, zero missing; 156 requirements and 36 gaps retained at that check.
- Saved key absent from 895 public source/test/contract/documentation files;
  private provider settings and backups remain ignored and outside build contexts.
- Normal API/worker/dispatcher agree on Gemini, authorized $0 cap, 20-attempt tenant
  limit and 24-hour confirmation expiry. API/web readiness passes and schema
  remains `0012_ai_runtime`. [Read-only runtime probe](../../../verification/gemini-runtime.json).
- Final images build successfully. No normal data migration was required. Original
  root `.env`, migration bytes, prior work and private volumes were not changed by
  this follow-up. All source work remains uncommitted.

See [operator setup and limits](../../../07-setup-and-deployment/GEMINI-FREE-TIER.md)
for the external no-billing precondition, one-time project/key confirmation,
persistent call-count limits, fallback semantics and initial setup command.
