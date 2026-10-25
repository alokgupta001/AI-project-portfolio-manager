# Approved demo API verification — 24 October 2026

The operator explicitly approved **synthetic demo only** in this conversation.
Gemini, Puter and Groq are now enabled for organization
`da69d9f9-e400-5268-941e-b091c8c8e611` and project
`3ba23317-7ce9-540c-9ca8-b34303d74c08`, using the existing free-account bindings.
Existing business projects remain unauthorized for these cloud routes.

| Provider / configured model | Live role | Result | Selected observations | Reported output tokens |
| --- | --- | --- | --- | --- |
| Gemini / `gemini-3.5-flash-lite` | financial | succeeded / api_selected | 2 | 24 |
| Puter / `gpt-4.1-mini-2025-04-14` | agile_coach | succeeded / api_selected | 1 | 7 |
| Groq / `openai/gpt-oss-20b` | executive | succeeded / api_selected | 1 | 70 |

Exactly **one request per provider** was admitted, each capped at 128 output tokens.
All completed without retry or repair. Each run retained all nine manual role
checklists and recorded `charged_usd=0.000000` in the application. This is application
accounting under the existing confirmed-free binding, not a fresh billing-console audit.

The actual localhost UI displayed all three saved API selections and their
checklists. Each saved run was reopened after reload; the database still contained
exactly one quota reservation per provider afterwards. The financial screenshot
was visually inspected. The source wording and amounts came from the application,
not model-authored text. This smoke test proves this limited workflow worked with
the supplied accounts at this checkpoint; it does not establish general reasoning
accuracy, useful ranking across a representative dataset, or future availability.

Read-only preflight verified all nine role assignments. Other tenant IDs, other
project IDs, broad interpretation task classes and document-text categories were
rejected. Only the [approved structured observation scope](API_DATA_SCOPE.md) is
enabled. Original profile policy and historical benchmark ledgers matched their
pre-activation hashes. Shared account scope IDs are unchanged; no quarantine or
failure history was cleared.

Limits: one concurrent request and one request/minute/account; at most ten requests
per rolling day/account and tenant; 8,000 reserved tokens/minute/account; $0 policy;
Ollama and the legacy Gemini caller disabled. Retained historical provider calls
were outside the prior 24-hour window at activation. Do not run old benchmarks
concurrently with this pilot; see the shared-account limitation in the register.

The original cloud-disabled overlay is unchanged. The approved local overlay is
ignored by Git: `artifacts/local/guided-review/cloud.compose.yaml`. Private policy
and egress files are mounted read-only from `artifacts/local/guided-review/cloud/`.
No keys or passwords are checked in or exposed to the browser.

Private receipts: `cloud-approval-receipt.json`, `scopes-before-cloud.json`,
`start-cloud.log`, `live-output.log`, `live-browser.log` and `live-*.png` under
`artifacts/local/guided-review/`. Use the [walkthrough](TRY_IT_NOW.md) to try it.
