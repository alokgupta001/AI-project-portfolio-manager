# Can the pilot support 50 requests per day?

Reviewed 25 October 2026. The user requested a feasibility check after approving
Customer Onboarding Portal's bounded cloud scope, then requested account-specific
checks so the limit could be 50. Those checks are now complete and the local
application ceiling is **50/day per provider**, shared across users and projects.

## Result

The application can support 50 requests per rolling 24 hours per provider account.
An in-memory policy validation and all nine role eligibility checks passed with
the proposed daily settings. Gemini's signed-in dashboard and Puter's read-only
metering API were then checked. No model requests were made for these checks.

| Provider and current model | Evidence | 50/day conclusion |
| --- | --- | --- |
| Groq / openai/gpt-oss-20b | Official Free Plan Limits table lists 1,000 requests/day, 30/minute, 8,000 tokens/minute and 200,000 tokens/day. The free-plan button was selected in the browser. | Within published free-plan limits for this bounded workload; account-specific exceptions and other usage still apply. |
| Gemini / gemini-3.5-flash-lite | Signed-in ai-ppm-dev project: Free tier, 500 requests/day, 15/minute, 250,000 input tokens/minute. Configured project and key suffix match. | 50/day fits the actual configured project's free quota. |
| Puter / gpt-4.1-mini-2025-04-14 | Account metering reports 962.4141 credits remaining from a 1,000-credit monthly allowance. Current native model rates: 0.0008 credits/input token and 0.0032/output token. | 50 small guided requests/day is feasible at observed usage; it is a ceiling, not a guarantee of 50 successful calls every day regardless of token size or other account use. |

Sources: [Groq rate limits](https://console.groq.com/docs/rate-limits),
[Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits),
[Puter rate limits and credit](https://docs.puter.com/rate-limits-and-quotas/),
[Puter monthly usage](https://docs.puter.com/Auth/getMonthlyUsage/).
Gemini's initial sign-in blocker was resolved by the user. Its dashboard showed
peak usage of 15/500 daily requests over the selected 28-day range; 15 is historical
peak usage, not today's remaining allowance. A private screenshot records the table.
Puter's live response explicitly labels its unit **credits**; do not convert those
numbers as microcents merely because the older object documentation describes that unit.

The existing Puter guided demo reported 154 input tokens and seven output tokens.
At the current model prices that is 0.1456 credits/call, or **225.68 credits for
50/day over 31 days**. Keeping the same input size but consuming the full 128-token
output cap would be 825.84 credits. Larger inputs, other apps, pricing changes and
other metered operations can consume the allowance faster. No credit reset date was
returned by the read-only response; monthly reset behavior comes from Puter's docs.
This is an estimate using one small completed run, not a representative benchmark
or a worst-case bound for every allowed eight-observation payload.

## Why ten was used

Ten was a conservative initial pilot setting to bound shared free-allowance use,
not a model limitation or a provider-specified universal quota. Each provider's
allowance is shared across all four application users, both authorized projects
and its three assigned roles. It is not ten per user or per role. The application
uses a rolling 24-hour window; provider reset rules can differ. A request cap alone
does not guarantee zero provider billing or a sustainable monthly allowance.

## Applied configuration

Changed both the provider profile's `requests_per_day` and
`tenant_requests_per_day` to 50, keeping the same `quota_scope`, credentials,
one-request-per-minute pacing, one concurrent request and 128 output-token limit.
Synchronized owner-managed provider scopes without resetting usage, failures or
quarantine state. Gemini's `ai_gemini_daily_call_limit` is also set to 50 in the private
runtime overlay. Existing frozen environment files and historical benchmarks are unchanged.

The dry run confirmed that Gemini's existing guard blocks a 50-request profile;
adjusting that guard in memory made the proposed routes eligible. Following actual
account checks, policy and runtime were updated and local services reloaded. Private
receipts: `fifty-dry-run.json`, `fifty-activation.json`, `puter-usage-20261025.json`,
`puter-costs-20261025.json`, and `gemini-quota-20261025.png` in
`artifacts/local/guided-access/`. Credentials are never included in the report.

Fifty **per provider** permits up to 150 model requests across three accounts,
not 50 total. A user-triggered guided analysis uses at most one assigned provider
request; opening saved results and using manual checklists require none. Provider
quota or credit exhaustion still leaves the rules-only checklist available.

No quota stress test, paid upgrade, additional API key or model retraining was used.
Monitor Puter's remaining credit as real usage grows; the application does not yet
reserve a monthly credit budget before each call. Its $0 policy and the user's
confirmed free-only provider billing settings remain the operating constraints.
