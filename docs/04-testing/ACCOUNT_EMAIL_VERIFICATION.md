# Account email verification — 10 October 2026

## Outcome

Signup, invitations and recovery have improved email content, configuration validation, truthful delivery statuses and browser recovery guidance. Expired pending invitations are visible for Admin resend/cancel. Existing account/membership/one-time-token controls remain in place.

**Development signup, existing-account invitation acceptance and password recovery work through the website and Gmail.** Personal signup arrived in Spam; test-Admin signup arrived in Inbox. Recovery receipt/reset/sign-in were confirmed by the recipient. The invitation was sent through Gmail and accepted: the website and scoped database read confirm active Viewer membership in the target organization. The recipient confirmed invitation receipt in Spam, acceptance as Viewer and sign-in. Development services run with `PPM_MAIL_MODE=smtp` and are healthy. Authorization covers personal signup/invitation/recovery and one sender-inbox signup for the separate test Admin. The queue was empty before initial activation, so no older messages were sent.

The website signup form requested one verification message for the authorized recipient. Initial attempts recorded `DELIVERY_UNCONFIRMED` and Gmail rejected authentication (**535**). The saved credential was incomplete. After private correction and service reload, authentication succeeded (**235**) and the existing message's fifth attempt reached **`provider_accepted`**, with no error and an empty queue. Only one signup request was created. The recipient subsequently reported **activated — Spam**; a scoped read confirms a verified account with an active Admin membership in the signup organization. Folder placement is recipient-reported, not an agent inspection of Gmail. Credentials and private links were never printed.

The website recovery form then requested one message for the same authorized recipient. It reached **`provider_accepted` on attempt 1**, with no error and an empty queue. The recipient has confirmed recovery receipt; password reset and subsequent sign-in await private user completion. The browser-control policy requires the user to enter and submit their own new credential privately. Invitation testing requires an Admin in a different organization; the recipient cannot accept a duplicate invitation into their existing signup membership.

The recipient confirmed recovery-email receipt but reported that the completion page described invitations. Investigation found shared completion-page wording, not an invitation token in the recovery message. New links include a nonsecret action hint; recovery now shows **Reset your password**, reset-specific instructions/button and **Password reset** success text. The server continues to decide the action from the stored challenge, not the URL hint. Old links use generic instructions covering all account actions. The single-use token is masked in the form and removed from the address after loading. No tokens were inspected or printed.

The follow-up isolated Chromium identity lifecycle passed, including reset heading, masked-token field, successful password reset, old-session invalidation and sign-in with the new password. TypeScript, targeted ESLint/Ruff, production website build and **16 email unit tests** passed. Tests used fictional recipients and forced local delivery. A read-only scoped inspection found a **Demo** organization with an existing verified Admin; its private sign-in session is still needed for the invitation journey.

The verified fix was rebuilt/applied to the development API/worker/dispatcher/web, with healthy services. A replacement recovery request was submitted through the website to the sole authorized recipient and reached `provider_accepted` on attempt 1. There are now two accepted recovery messages; the replacement invalidates the earlier challenge, so only the newest email should be used. Live reset/sign-in completion remains pending the recipient's private action.

The recipient subsequently reported **recovered** in response to the reset-and-sign-in confirmation. A scoped read confirms that the newest reset challenge is consumed and the account remains verified with active Admin membership. This completes the live recovery journey by recipient confirmation; its folder placement remains unspecified.

The recipient did not know the Demo Admin login. They explicitly authorized signup delivery to the sender inbox to create a separate **Northstar Invitation Test 2026-10-10** organization through the website. That signup message reached `provider_accepted` on attempt 1, with no error and an empty queue. Activation and private sign-in of this second Admin are pending. This new authorization covers signup to the sender inbox; invitation delivery still targets the original personal recipient.

The user subsequently confirmed **test Admin signed in — Inbox**. A scoped read confirms a verified active Admin membership in the new test organization and a consumed signup challenge. The controlled website panel retained an older Demo session, so it was signed out and the correct test-Admin login prepared. No invitation was created in Demo. Invitation testing awaits the user's private sign-in in the controlled panel; an external browser login does not share that panel's session.

After the user confirmed panel sign-in, navigation to Account verified the correct sender account and **Northstar Invitation Test 2026-10-10 — Admin** session. The website created a **Viewer** invitation to the personal recipient. Refresh showed **Accepted by email provider — inbox arrival unconfirmed**. The recipient was asked to confirm receipt/placement, accept with their existing password and select the new organization as Viewer. No private invitation link was inspected, stored in screenshots or printed.

Acceptance is now verified: the invitation challenge is consumed, a scoped database read shows active Viewer membership in the target organization alongside the original Admin membership, and the Admin website shows the Viewer member, `invitation.accepted` audit event and no pending invitation. The live evidence image contains membership/status only, without a private link/token. The personal account's different roles in the two organizations demonstrate that invitation acceptance did not overwrite its original Admin role.

`.env` remains Git-ignored. Exact private settings and App Password steps are in ignored `artifacts/local/GMAIL-SETUP.md`. One pasted Markdown fence was removed from `.env` so Docker could parse it; credentials were preserved. The earlier automated tests used isolated local delivery, independently of this live attempt.

Credential diagnostics identified one definition, no shell override, and no whitespace or literal quotes; the original saved value was not 16 characters long. Only boolean comparisons were emitted; the credential itself was not displayed or changed by the agent.

The corrected private credential passes the 16-character format check. API/worker/dispatcher were recreated to load it and are healthy. Gmail's connection-only probe passes verified STARTTLS and authentication (**235**). The delivery worker's subsequent `provider_accepted` result establishes SMTP acceptance separately from that probe.

## Changes

- Private account messages have action-specific subjects/instructions, configured-origin links, expiry timestamps, replacement guidance and password requirements. Invitation messages include the organization name and invited role. Subject line breaks from organization names are normalized to prevent header injection.
- SMTP verifies TLS certificates through STARTTLS before authentication/sending. Recipient refusal is a delivery failure. Incomplete SMTP settings fail startup without exposing credentials. Port 465 is rejected because this adapter supports STARTTLS rather than implicit TLS.
- New terminal queue statuses distinguish `local_preview` from `provider_accepted`. Existing ambiguous `delivered` rows are exposed as acceptance-unverified, not retroactively treated as Gmail delivery. No database migration or historical status rewrite is required.
- Admin can refresh invitation status and resend/cancel expired invitations. Invalid completion links offer signup/recovery links and invitation-resend instructions.
- Existing bounded retries, challenge expiry/replacement checks, inviter-authority checks, generic public responses, private queue-payload clearing and membership rules are retained.
- Isolated test delivery is forced to local mode to prevent fictional fixtures from using a configured real sender.

## Checks completed

| Check | Result | What it establishes |
| --- | --- | --- |
| Host unit/configuration suite | **25 passed** | Templates, header injection boundary, verified TLS/auth order, recipient refusal, SMTP config validation/redaction and local/relay behavior; includes existing storage/config tests |
| Isolated full backend runner | **91 passed**, one dependency deprecation warning | Migration upgrade/downgrade/check lifecycle in `ppm_test` and existing identity/delivery/assessment/capacity/worker-related suite plus email tests; no new migration operations |
| Added expired-invitation regression | **1 passed** in a separate targeted run | Local-preview status, historical ambiguity, expired visibility/resend, old-link rejection and preserved organization/role context |
| Isolated Chromium identity journey | **Passed** | Cookie/session identity lifecycle, new-user invitation acceptance, recovery, password change and revoked session |
| Isolated Chromium signup/pilot journey | **Passed** | Verified signup, organization creation/profile, invitation resend/cancel, invalid-link replacement guidance and existing responsive/accessibility checks |
| Website build | **Passed** in isolated container build | Next.js production compilation/static generation and TypeScript build |
| TypeScript no-emit check | **Passed** | Current website types |
| Targeted ESLint / Python Ruff | **Passed** | Changed website/browser and Python source/tests |
| Python typing | **Passed** for config and account-mail modules | Mypy check of changed configuration/SMTP modules |
| Contract check | **Passed** | OpenAPI and generated TypeScript contracts match |
| Development SMTP activation / service health | **Passed** | Authorized instance restarted; no pre-existing queued mail |
| Gmail connection / verified STARTTLS | **Passed** | Provider reachable with verified encrypted transport |
| Gmail SMTP authentication | **Passed — 235 after credential correction** | Updated private credential loaded into healthy services; earlier 535 explained by incomplete credential |
| Live website signup request / SMTP acceptance | **Passed — provider_accepted** | Existing request succeeded on fifth bounded attempt after credential correction; empty queue |
| Signup Gmail receipt / placement | **Confirmed by recipient — Spam** | Human reports receipt; no agent inbox inspection |
| Signup activation / Admin membership | **Passed** | Recipient completed link; scoped database read confirms verified active Admin account |
| Live recovery request / SMTP acceptance | **Passed — attempt 1** | Requested through website; provider_accepted and empty queue |
| Recovery receipt | **Confirmed by recipient; folder unspecified** | Shared completion-page wording issue reported and fixed |
| Recovery reset / subsequent sign-in | **Confirmed by recipient** | Newest reset challenge consumed; isolated regression also verifies session invalidation and new-password sign-in |
| Separate test-Admin signup / activation / sign-in | **Passed — attempt 1; recipient reports Inbox** | Verified active Admin membership and controlled website session confirmed |
| Live invitation creation / sending status | **Passed — provider accepted** | Created as Viewer through website in the new test organization; useful status shown after refresh |
| Live existing-account invitation acceptance | **Passed** | Consumed challenge, active Viewer membership, website member list and invitation.accepted audit; original organization remains Admin |
| Invitation Gmail receipt / placement | **Confirmed by recipient — Spam** | Recipient reports accepted — Viewer — Spam; provider and membership evidence independently recorded |

The backend and browser tests used fictional addresses, local mailbox previews or mocked SMTP. Browser acceptance used its independent `enterprise-ppm-identity-test` services/volumes, not normal user data. The runner stopped/removed its test containers/network and removed its generated private fixture file; test volumes were preserved. Screenshots/traces are local test artifacts, not real Gmail evidence. The expired-invitation targeted run is listed separately, not claimed as an additional full-suite rerun.

One initial Windows unit run could not create pytest's default temporary directory under the sandbox. It was rerun successfully with a task-specific temporary directory inside ignored workspace artifacts. An executable mypy shim was unavailable; invoking the installed module succeeded. These tooling issues are not application failures.

## Reproduction

Operator/developer commands, never ordinary user signup requirements:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_account_mail.py tests/test_config_storage.py -q --basetemp artifacts/local/account-mail-unit-check
.\.venv\Scripts\ruff.exe check services/api/ppm_api/config.py services/api/ppm_api/account_mail.py services/api/ppm_api/identity.py tests/test_account_mail.py tests/test_pilot.py
.\.venv\Scripts\python.exe -m mypy services/api/ppm_api/config.py services/api/ppm_api/account_mail.py
npm run typecheck
npm run contracts:check
docker compose --profile test run --build --rm test
node scripts/check-identity-browser.mjs tests/browser/identity.spec.ts tests/browser/pilot.spec.ts --grep "identity lifecycle|verified signup"
```

The full backend run in this session mounted the current services/tests read-only into the established test image. Its guarded runner exercised only `ppm_test` and Redis test DB 1. Do not run acceptance suites concurrently against the same database/project. Test browser ports are 3001/8001/15433/16380. Temporary directories must stay in the intended ignored workspace; do not point pytest basetemp at a folder containing important files.

## Acceptance limits

Live signup, existing-account invitation acceptance and recovery are complete for the authorized development accounts. Invitation arrival in Spam is confirmed by the recipient; recovery placement was not specified. Do not infer Inbox delivery from SMTP acceptance.

New-user invitation acceptance, role/isolation enforcement, resend invalidation, cancellation, expiry/replay rejection, retry/failure behavior and session revocation are covered by the recorded isolated backend/browser tests. Those lifecycle variants were not all repeated with real Gmail addresses. The live invitation role was Viewer; no claim is made that every role or every denial path was newly exercised with real inboxes. Both authorized test accounts are now verified, so an additional live new-user invitation would require another explicitly authorized recipient. No account deletion or unauthorized alias is needed for the current verified journeys.

These are development checks, not production certification. Preserve unrelated CI, production, document, provider-integration and future-feature gates. See [Gmail acceptance steps](../07-setup-and-deployment/EMAIL-DELIVERY.md) for any future broader live verification.

The [detailed user manual](../06-user-guides/WEBSITE_WALKTHROUGH.md) retains its complete organization/project/framework/evidence example. It uses the verified website-and-Gmail path and explains one-time tokens, verification versus sign-in, and checking Spam. The private-local alternative remains only for instances explicitly running local mode. Operator setup is separate in [Email delivery](../07-setup-and-deployment/EMAIL-DELIVERY.md).

## Documentation follow-up — 10 October 2026

Updated current user/demo guides, fourteen existing canonical learning chapters and their entry points. Added detailed member/Project Manager access instructions, Gmail SMTP setup and an account email/access learning chapter. Reviewed role and scoped-grant instructions against the current frontend forms and backend permission checks, including exact project/portfolio access controls, independent resource-effort flags and framework/result access panels.

The documentation check scans the updated Markdown files for missing local file-link targets, excluding fenced examples, remote URLs and section anchors. Its private result manifest is `artifacts/local/current-guide-link-check.json`. Application test results above remain the recorded implementation evidence; application suites were not rerun for this documentation-only follow-up. Archived Word snapshots remain historical and were not regenerated.

Results: **37 Markdown documents, 577 local file links, zero missing targets**. The tracked documentation whitespace check (`git diff --check -- docs`) passed. A targeted scan found the original SMTP-blocked statement only in the dated Sprint 8.1 report; an explicit 10 October follow-up now points readers to the completed development email evidence while preserving that historical result.
