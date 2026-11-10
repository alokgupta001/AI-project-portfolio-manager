# Sprint 12.1 — Narrow demo access proposal

26 October 2026. **Owner approved all four demo Admins; four demo-only grants applied.**

The direct user reply was **“Approve all four demo Admins.”** The approved accounts
are Alok Gupta, Ashu, Blaze and Hement, limited to the existing synthetic demo
organization / Demo project. The original grant check is intact. Other guided
grants, business roles, provider configuration and quota ledger hash-match their
pre-change values. [Actual receipt](../../verification/sprint12_1/demo-grants-approved.json).
Personal label review is still a separate, unrecorded action. The original narrower
proposal below is retained as the decision history; do not request this access again.

The initial live check showed Alok Gupta, Ashu, Blaze and Hement as existing Admins in
**Guided Review Demo · synthetic**. A read-only database check confirms that none
had an explicit guided grant for **Demo project**. Ordinary Admin guided runs
already work there, but the pilot additionally requires that grant.

Automatic approval review rejected removing the pilot's guided-grant check because
that would expand its persistent Admin authorization boundary. Keep the check.

## Proposed smallest change

Add or enable exactly two explicit guided grants in the existing synthetic demo:

| Existing account | Existing organization/project | Intended pilot work |
| --- | --- | --- |
| Ashu | Guided Review Demo · synthetic / Demo project | Prepare the saved pilot through the current signed-in session |
| Alok Gupta | Same synthetic organization/project | Independently review labels and, if personally satisfied, record approval |

This lets those two accounts satisfy the unchanged pilot gate. It creates no new
account, role, project or external provider scope. Their business-project roles,
other users' access, Gemini/Puter/Groq configuration, keys, $0 policy, quotas and
usage history remain unchanged. It does not grant broad semantic qualification.

An alternative is the same demo-only grant for all four existing demo Admins;
that is a separate explicit scope choice. Keeping current access leaves preparation
blocked in the synthetic demo. Promoting business-project members is not proposed.

## Review is still separate

Approving this access proposal **does not approve the labels**. A different
authorized human must personally examine the [full packet](LABEL_REVIEW_PACKET.md)
and record their decision through the app. The coding agent cannot claim personal
human review, use another person's credentials to fabricate it, or count a grant
as a model-quality result. AT17 remains BLOCKED.

Any approved change must retain the original rows, record the exact two/four
target grants, and be verified through normal UI/API checks before measurement.
