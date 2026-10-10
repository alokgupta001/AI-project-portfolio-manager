# Account email delivery: operator setup and Gmail acceptance

Updated 10 October 2026. Development Gmail SMTP signup, existing-account invitation acceptance and recovery are verified for the authorized accounts. Verified STARTTLS/authentication pass after private App Password correction. Personal signup arrived in **Spam** and the separately authorized test-Admin signup in **Inbox**, according to the recipients. Recovery receipt/reset/sign-in are confirmed. The invitation created through the website was accepted and added the intended Viewer membership, while preserving the original organization's Admin role. These checks cover development, not production readiness. See the [verification report](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md).

Ordinary users need only the website and their inbox. They do not need Docker, a terminal, or the private test mailbox. This document is for the operator configuring the application; the detailed member manual is [Website walkthrough](../06-user-guides/WEBSITE_WALKTHROUGH.md).

For a complete Gmail-specific setup sequence, including App Password creation, exact variables, private storage, environment reload and safe authentication diagnostics, use [Gmail SMTP setup](GMAIL-SMTP-SETUP.md). For adding PMs and managing their work scope, use [Members, roles and access](../06-user-guides/MEMBERS_ROLES_AND_ACCESS.md).

## Choose the sender

Gmail can receive the message regardless of which provider sends it. Use an existing authorized SMTP account supporting STARTTLS, normally on port 587. Verify the sender/address or domain in that provider's console according to its rules; some sandbox accounts also require recipient verification. Do not impersonate an address/domain the provider has not authorized.

For a custom domain, obtain the provider's actual SPF/DKIM records and follow its sender-verification process. Google requires SPF or DKIM for all senders to personal Gmail, with stricter bulk requirements, and recommends SPF, DKIM and DMARC. Managed providers handle their SMTP infrastructure; the domain owner configures the supplied DNS records. DNS changes and purchases require separate authorization. Do not invent DNS values. See [Google's sender guidelines](https://support.google.com/mail/answer/81126?hl=en).

An authorized Gmail sending account can be a small pilot option where its policy permits SMTP app-password access: host `smtp.gmail.com`, STARTTLS port `587`, username the full sender address, and sender the same authorized address. This application currently uses SMTP username/password, not Google OAuth. Google app passwords require 2-Step Verification and may be unavailable for some organization, security-key-only or Advanced Protection accounts. Use an app password where allowed, never the normal Google account password. See [Google SMTP application setup](https://support.google.com/a/answer/176600?hl=en) and [Google app-password instructions](https://support.google.com/accounts/answer/185833?hl=en). Provider/account policies and sending limits still apply.

## Private configuration

Supply these fields privately in the project's ignored `.env`. Do not paste passwords into a chat, commit them, or publish full Compose configuration output.

| Field | Required value |
| --- | --- |
| `PPM_MAIL_MODE` | `smtp` for real sending; `local` for private test previews |
| `PPM_SMTP_HOST` | Provider's SMTP hostname |
| `PPM_SMTP_PORT` | Provider's STARTTLS port, normally `587`; implicit TLS `465` is unsupported |
| `PPM_SMTP_USER` | SMTP username supplied by provider |
| `PPM_SMTP_PASSWORD` | SMTP credential/app password stored privately |
| `PPM_MAIL_SENDER` | Verified email address; `Enterprise PPM <accounts@your-domain>` display-name form is supported |
| `PPM_WEB_ORIGIN` | The exact website origin used by recipients, with no path or trailing slash |

Authenticated SMTP requires both username and password. An authorized relay may use neither. Host and a valid sender are required in smtp mode. Invalid/incomplete SMTP configuration fails startup with field/configuration names rather than credential values.

For same-PC tests, `http://localhost:3000` remains valid. If a recipient opens the message on another computer or phone, localhost points to that device, not this server. Use a reachable configured HTTPS origin for remote recipients. Configuring SMTP does not host the website or enable the currently disabled production environment.

Compose supplies these settings to API, migration, worker and dispatcher services. After source/configuration changes, the operator can apply them from the project root:

```powershell
docker compose up --build -d --wait api worker dispatcher web
```

This restarts/recreates application services as needed; schedule it appropriately for a shared instance. Do not reset databases, remove volumes or regenerate the JWT secret. Keep worker and dispatcher settings aligned with API settings. Ordinary users never run this command. Merely changing `.env` does not change an already-running container.

## How sending works

Signup/recovery public requests preserve generic responses for eligible and unknown/existing addresses. A response means the request was handled, not that email arrived. Eligible requests enqueue private account messages. The dispatcher schedules reconciliation every ten seconds, and the worker processes due messages.

Messages include an appropriate subject, the invitation organization/role when present, a single-use link to the configured website, an explicit expiry timestamp, password instructions and replacement-link guidance. The SMTP adapter uses certificate-verified STARTTLS before authentication and sending, and rejects recipient-refusal results. It does not log credentials or message bodies.

Provider failures receive bounded retry handling: at most five attempts, backoff between attempts, and the safe code `DELIVERY_UNCONFIRMED`. Raw provider errors are not exposed to users. Successful/finally failed/cancelled queue payloads are cleared. Transient queued payloads retain the private link until delivery resolves. The provider may have accepted a message before a connection failure or transaction failure, so duplicate delivery is possible; do not claim exactly-once SMTP delivery. The stable Message-ID and single-use challenge bound the user-facing effect.

Queued delivery is stopped if the challenge has been used/replaced/cancelled or expired. Invitation sending also rechecks the inviter's active Admin authority. Previously sent emails cannot be recalled; cancellation/resend invalidates their links.

## Invitation status in the website

Admin opens Account and access → Pending invitations → **Refresh invitations**.

| Website label | Meaning / action |
| --- | --- |
| Waiting to send (or retry) | Queued; allow the worker to process it |
| Accepted by email provider — inbox arrival unconfirmed | SMTP accepted the message; recipient checks inbox and Spam |
| Local test message — no inbox email sent | Private development preview; not Gmail delivery |
| Sending failed after retries — resend after fixing delivery | Fix credentials/provider/network first, then resend |
| Sending stopped — resend for a new link | The queued challenge was stopped; request a replacement if needed |
| Earlier delivery — inbox arrival unconfirmed / status unverified | Historical records do not establish the delivery mechanism or arrival |

Expired invitations remain listed for Admin resend/cancel. Accepted/cancelled/replaced invitations are no longer pending. Resending creates a fresh 24-hour link and invalidates the old one. Message status is not a read receipt, bounce-tracking service, or confirmation of inbox placement.

## Live acceptance: authorized inboxes only

Record recipient authorization before sending. Use a fictional organization and separate browser profiles. Do not put tokens/passwords in the acceptance report or screenshots.

1. Confirm a verified sender and private SMTP settings are present, and services use the updated code/configuration.
2. In the website, submit `/signup` using an authorized Gmail inbox and a new training organization name.
3. Verify actual Gmail receipt, sender, organization wording, timestamp and link origin. Record Inbox or Spam placement without copying the link. In Gmail, inspect Show original for authentication results if investigating delivery.
4. Follow the link in the authorized browser, choose name/password, and sign in. Verify new organization and Admin membership.
5. Invite an authorized second inbox as Project Manager. Check website status, actual Gmail receipt, organization and role; accept as a new user and verify the membership.
6. Invite an already verified authorized user into the training organization and test the existing-password acceptance path.
7. Use a separate controlled invitation for resend: verify the old link fails and the latest received link works. Do not resend excessively into real inboxes.
8. Cancel a controlled invitation and verify its received link is unusable. Test expiry using isolated automated fixtures rather than waiting or modifying a real database.
9. Request recovery for the activated test account, verify Gmail receipt and the 30-minute expiry wording, complete the reset and confirm prior sessions are revoked. Verify the used link cannot be replayed and the new password signs in.
10. Verify unknown-address public responses are generic without sending to unapproved recipients; automated tests cover that case.
11. Record automated tests, browser results and actual Gmail arrival separately. Only then change the real-inbox acceptance status and the normal user guide's delivery claim.

## Troubleshooting

- **No messages for anyone:** confirm smtp mode, updated services, worker/dispatcher availability, STARTTLS reachability, verified sender and credentials. Use status/error codes; do not print secrets.
- **Provider accepted but Gmail absent:** recipient checks Spam and address spelling; operator checks provider's private delivery/bounce console and domain authentication. SMTP acceptance is insufficient to close acceptance.
- **Auth fails:** correct provider SMTP credentials; for permitted Gmail sending, use an app password. Fix the configuration before resending failed invitations.
- **Sender rejected:** complete provider sender/domain verification or sandbox-recipient verification. Do not swap in an unverified From address.
- **Wrong/inaccessible link origin:** correct the website origin and issue fresh messages; old emails retain the old URL.
- **Invalid/expired/used link:** website offers signup/recovery replacement links; an invitation recipient asks Admin to resend. Do not expose a token to troubleshoot.
- **Local-preview status:** real sending is not enabled. Changing mode does not resend previous previews automatically; use a fresh signup/recovery request or Admin invitation resend after configuration.

## Development alternative and automated tests

Retain `PPM_MAIL_MODE=local` for development. This writes a private preview to the existing operator mailbox and does not contact Gmail. Operator-only retrieval is documented in [Identity operations](IDENTITY-DEVELOPMENT.md). Tests use fictional addresses and local/mocked adapters. The isolated backend test service and browser-test API/worker/dispatcher force local mode so a configured real provider is not used by those fixtures.

The user authorized Gmail SMTP activation and signup/invitation/recovery tests to one recipient after configuring credentials privately. Signup provider acceptance, recipient-reported arrival in Spam and verified Admin account activation are confirmed. Recovery reached provider acceptance and the recipient confirmed receipt/reset/sign-in. The separately authorized test Admin invited the personal account as Viewer; the recipient confirmed invitation arrival in Spam and successful acceptance/sign-in. Private host-specific instructions are in ignored `artifacts/local/GMAIL-SETUP.md`; credentials are never stored in this documentation. These development checks do not establish production readiness. See the [account email verification report](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md).
