# Gmail SMTP setup for the development operator

Updated 10 October 2026. This guide configures account signup, activation, invitations and password-recovery email. Members use only the website and their inbox; they never enter SMTP credentials or run these commands. The development signup, existing-account Viewer invitation and recovery journeys have been verified. See the [evidence report](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) for exact results and limits.

## Before you start

You need a dedicated Gmail sending account you control, access to that account's security settings, the existing project `.env`, and explicitly authorized recipient inboxes for test messages. Use an App Password for this application's SMTP username/password adapter, not your ordinary Google password. Google requires 2-Step Verification for App Passwords and describes account-policy restrictions in its [App Password instructions](https://support.google.com/accounts/answer/185833?hl=en).

The sender and recipient are separate choices. The SMTP username is the sending account. Signup/invitation/recovery forms supply recipient addresses; there is no recipient environment variable. Permission to send from an account does not automatically authorize test messages to every inbox.

## Create the Gmail App Password

1. Sign in to the dedicated sender's Google account. Check the account avatar/address so you do not generate a password for your personal recipient by mistake.
2. Open [Google Account Security](https://myaccount.google.com/security) and enable **2-Step Verification** if needed.
3. Open [App Passwords](https://myaccount.google.com/apppasswords). Google may ask you to sign in again.
4. Create an App Password named **AI-PPM development**.
5. Copy the generated password privately into the local `.env`. Google App Passwords contain 16 characters; removing display-grouping spaces must retain all 16. Do not publish the value, put it in a screenshot, or paste it into chat.
6. If App Passwords are unavailable, check the account-policy restrictions in Google's guide. Use a permitted provider/authentication arrangement; do not disable protections to force access. This adapter does not implement Google OAuth.

Changing the sender's normal Google account password revokes its App Passwords according to Google; generate a replacement privately if necessary. Do not change the application users' website passwords to repair SMTP authentication.

## Store the exact variables privately

From the `enterprise-ppm` project root, open the existing `.env` in a local editor. Preserve database passwords, JWT secret and unrelated configuration. Define each key once. Copy only the lines, without the Markdown fence markers below.

```dotenv
PPM_MAIL_MODE=smtp
PPM_SMTP_HOST=smtp.gmail.com
PPM_SMTP_PORT=587
PPM_SMTP_USER=YOUR_DEDICATED_SENDER@gmail.com
PPM_SMTP_PASSWORD=PASTE_THE_COMPLETE_APP_PASSWORD_PRIVATELY
PPM_MAIL_SENDER=YOUR_DEDICATED_SENDER@gmail.com
PPM_WEB_ORIGIN=http://localhost:3000
```

Replace both sender placeholders with the actual authorized sending account and replace the password placeholder locally. Do not leave placeholders in the running configuration. Gmail's [SMTP setup documentation](https://support.google.com/a/answer/176600?hl=en) lists `smtp.gmail.com` and TLS port 587. This application uses certificate-verified **STARTTLS**; it rejects implicit TLS port 465.

`PPM_WEB_ORIGIN` must match the website origin recipients use, with no path or trailing slash. `http://localhost:3000` is suitable when the emailed link is opened on the computer running the application. A phone or another PC resolves localhost to itself. Remote access needs a reachable configured website origin and appropriate HTTPS hosting; SMTP setup alone does not host the website or make this application production-ready.

The repository ignores `.env` and `.env.*`, except the intentionally tracked `.env.example`. Keep only empty/example credentials in the template. You can verify ignore rules without displaying secrets:

```powershell
git check-ignore .env
git ls-files --error-unmatch .env
```

The first command should identify `.env` as ignored. The second should report that it is not tracked; its nonzero exit is expected in that case. If `.env` is tracked, resolve that separately before storing secrets. Git ignore does not encrypt files or prevent cloud-folder syncing such as OneDrive. Never print `.env`, expanded Compose configuration, private queue payloads or received links into a shared report.

## Reload the development services

Before enabling real mail, inspect outstanding queued recipients privately and confirm they are authorized. Switching from local to SMTP must not unexpectedly send old queued messages to another inbox. Check required fields without printing credential values.

After saving settings, the operator runs from the project root:

```powershell
docker compose config --quiet
docker compose up --build -d --wait api worker dispatcher web
```

The first command validates without dumping resolved secrets. The second applies current source and configuration to the development services and checks health. Changing `.env` alone does not update existing containers. Keep API, worker and dispatcher on the same SMTP configuration. Preserve database volumes and the existing JWT secret; no database reset or migration change is required for SMTP setup.

If only the private credential changed and images are already current, `docker compose up -d --wait api worker dispatcher` recreates services as necessary. A simple `docker compose restart` does not reload changed Compose environment values.

## Check authentication before sending tests

Use a private connection-only diagnostic that opens Gmail, verifies STARTTLS and authenticates without sending a message. Record only safe result categories or SMTP reply codes; never enable raw SMTP protocol logging because authentication exchanges contain credentials. The development investigation recorded initial rejection `535` for an incomplete App Password, then success `235` after correcting/reloading it. These codes describe authentication, not email receipt.

For a mismatch, privately compare `.env`, Compose interpolation and running API/worker/dispatcher values in memory and print only match booleans. Check for duplicate definitions, shell overrides, unwanted whitespace/quotes and an incomplete password. Do not publish hashes or portions of the credential to troubleshoot.

## Verify website-to-Gmail delivery

1. Authorize the exact signup, invitation and recovery recipients before sending. For this session the personal inbox was authorized for all three flows; the sender inbox was separately authorized for a signup test that created a second Admin.
2. On `/signup`, enter an authorized inbox and a new training organization. Check actual Inbox and Spam arrival, sender, organization, expiry and website origin. Do not copy the private link into a report.
3. The recipient opens the link, chooses their own website name/password privately, verifies, then signs in. Confirm the initial Admin membership.
4. In a separate profile, the Admin opens Account & access and invites another authorized account with the intended role. Refresh invitation status. The recipient checks actual receipt and accepts; an existing verified account uses its current website password.
5. Confirm active membership and role in the target organization. A user can be Admin in one organization and Viewer/PM in another. Verify that acceptance did not overwrite the original membership.
6. Request recovery through `/account/reset`. The recipient opens the newest email, sees **Reset your password**, privately submits a new password, then signs in again. Reset links expire in 30 minutes; signup/invitation links in 24 hours. Verify used/replaced links cannot be reused and previous sessions lose access.
7. Record website request, SMTP acceptance, actual receipt/folder and successful completion as separate outcomes. Do not turn a provider-accepted status into an Inbox-delivered claim.

Personal signup and invitation arrived in Spam in the verified development exercise. The second Admin signup arrived in Inbox. Recovery receipt/completion were confirmed; its folder was not specified. These results do not guarantee future folder placement. A recipient can use Gmail's **Not spam** action for an expected legitimate message. Custom-domain sender authentication and delivery tuning are separate operator concerns covered in [Email delivery](EMAIL-DELIVERY.md).

## Status, failure and local-development behavior

| Observation | Meaning / action |
| --- | --- |
| Waiting to send or retry | Durable queue is pending; check worker/dispatcher and wait for bounded processing |
| Provider accepted | SMTP accepted the message; still obtain recipient confirmation |
| Sending failed after retries | Up to five attempts were used; safe error is `DELIVERY_UNCONFIRMED`. Fix sending, then request/resend a fresh message |
| Authentication `535` | Check sender account and complete App Password, then reload services; do not guess credentials |
| Connection/TLS failure | Check hostname, STARTTLS port, network and certificate validation; do not bypass TLS checks |
| Correct password saved but old value still running | Recreate services with Compose; check overrides privately |
| `.env` parse failure | Remove pasted Markdown fences or malformed variable lines without exposing values |
| Link says invalid/used/expired | Use the newest message; resend replaces invitations, cancellation prevents acceptance, and recovery replacement invalidates older reset links |
| Local test message | No Gmail message was sent; local previews are operator-only |

For an intentional local-preview environment, set `PPM_MAIL_MODE=local` and recreate the relevant services. Local previews are not automatically resent when SMTP is later enabled. Isolated backend/browser tests force local or mocked delivery so fictional test addresses cannot reach the real SMTP sender. Keep local-preview retrieval in [Identity development operations](IDENTITY-DEVELOPMENT.md), separate from ordinary user instructions.

For shutdown, ongoing provider policies, retries/duplicate delivery boundaries and broader acceptance steps, see [Email delivery](EMAIL-DELIVERY.md) and [environment variables](ENVIRONMENT_VARIABLES.md). No purchases, external DNS changes or production deployment were part of the verified development setup.
