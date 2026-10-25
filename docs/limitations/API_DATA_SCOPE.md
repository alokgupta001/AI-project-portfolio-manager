# Limited API assistance: approved project data scope

The operator explicitly approved synthetic-demo-only activation on 24 October 2026.
The private local overlay is active and one real test call per provider succeeded;
see [verification](LIVE_API_VERIFICATION.md). The checked-in overlay still defaults
to no external calls. The user subsequently explicitly approved the same bounded
payload for **Customer Onboarding Portal** for Alok Gupta, Hement, Blaze and Ashu.
That project is now allowlisted; [access and verification](USER_ACCESS.md).

Each user-initiated run asks **one** assigned provider to select at most two IDs from
at most eight observations. There are no automatic retries, no training upload and
no background inference. Opening or refreshing a saved run makes no model request.
The response is capped at 128 tokens. Invalid output falls back to a manual checklist.

| Provider | Roles | Permitted observation content |
| --- | --- | --- |
| Gemini | Financial, schedule, resource | Selected project's canonical numeric metric keys, values and units; partial-data label |
| Puter | Risk, governance, agile coach | Selected project's risk measure; presence of a selected assessment rubric; sprint status |
| Groq | Team support, PMO, executive | Selected project's numeric measures; aggregate blocker count only when the existing minimum-group and Admin rules permit it |

No document text, assessment answers, personal notes, names, email addresses,
credentials, project IDs or unrelated-project metrics are included in the prompt.
Source IDs and evidence hashes remain in local storage for access revalidation.
An example request contains only:

```json
{"role":"financial","observations":[{"id":"o1","fact":"Recorded usage: 112.50 %."}]}
```

The permitted response is `{"choices":["o1"]}`. All displayed wording, source
links and actions come from the application. Model choices do not qualify broader
semantic interpretation or certify that the selected observation is the most useful.

Activation is restricted to **Guided Review Demo · synthetic** / **Demo project**
and **Northstar Invitation Test 2026-10-10** / **Customer Onboarding Portal**.
Other projects need their own explicit policy scope. Only the already supplied keys and
confirmed free accounts are used; no additional provider or paid endpoint is added.
Keep one request/minute per account and the verified **50/day application ceiling**.
The initial ten/day pilot ceiling was superseded after the account-specific checks
in [QUOTA_REVIEW](QUOTA_REVIEW.md). Existing attempts and account quarantine are
preserved. Do not run historical benchmarks concurrently against the shared keys.

The operator must keep account billing disabled: API requests cannot independently
enforce an account-level free plan. Provider exhaustion leaves the checklist usable.

Automatic approval review requested explicit approval for this scope before
persistent cloud activation; that approval has now been received and applied.
No earlier model qualification is claimed by approving it.
