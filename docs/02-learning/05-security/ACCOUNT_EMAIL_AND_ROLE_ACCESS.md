# Learn account email, membership and scoped access

Updated 10 October 2026. Read alongside [authentication and authorization](AUTHENTICATION_AND_AUTHORIZATION.md), the [website access guide](../../06-user-guides/MEMBERS_ROLES_AND_ACCESS.md) and [SMTP setup](../../07-setup-and-deployment/GMAIL-SMTP-SETUP.md). The code pointers describe the current checkout; the [email report](../../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) distinguishes automated tests from real Gmail evidence.

## The verified exercise

The personal test account signed up and became Admin of its new organization. After recovery it used its current password to accept an invitation from a second test Admin, becoming Viewer of a different organization. Its original Admin membership remained unchanged. Personal signup and invitation arrived in Spam; the second Admin signup arrived in Inbox. Recovery receipt/reset/sign-in were confirmed. No production certification follows from these development results.

The exercise illustrates four independent objects: a global login identity, an organization membership with a role, a private one-time challenge and a normal sign-in session. A staffing resource profile is a fifth object and does not create login privileges.

## Follow signup into durable email delivery

1. `apps/web/app/account/identity-client.tsx` submits email and organization name to `/api/v1/auth/register` with the normal transport/CSRF handling.
2. `identity.register` normalizes the address, rate-limits, locks the email scope and replaces older registration challenges. Its public response remains generic to avoid revealing whether the email already has an account.
3. `identity.issue_challenge` creates the random private code and stores its digest and purpose in `identity_challenges`. The durable delivery row holds the private message payload until its outcome is resolved.
4. `account_mail.account_message` renders the correct subject, organization/role, expiry, replacement guidance and configured-origin link. The fragment contains the private token; the action hint selects page wording only. The backend decides the operation from the stored challenge.
5. `account_mail.deliver_due` checks challenge validity and, for invitations, the inviter's live Admin authority. In SMTP mode it uses certificate-verified STARTTLS, authenticates and sends. A recipient refusal is failure. Bounded retries stop after five attempts.
6. Successful delivery becomes `provider_accepted`, not proof of Gmail receipt. Local mode produces `local_preview` without contacting Gmail. Final outcomes clear private queue payloads; transient retries need to retain the payload. SMTP is not guaranteed exactly once if acceptance occurs before a connection/transaction failure.
7. The user opens the message. Completion creates user, organization and first Admin atomically after verification. The frontend masks the code and removes it from the address after reading it. Verification does not automatically create a login session; sign-in follows.

No SMTP or website password should appear in logs, documentation, shared screenshots or test reports. The queue's private data and challenge digest are different from a public invitation-list reference.

## Invite and recover

An Admin creates an invitation inside their active organization. The challenge fixes organization, inviter and role. New users choose a password; existing verified users prove their identity with the current account password. Acceptance creates the target membership but does not overwrite an existing membership or reactivate a disabled one. Resend invalidates the old challenge; cancellation and expiry prevent completion. An Admin manages existing members separately through role/Active controls with revision checks; the final active Admin is protected.

Recovery issues a different challenge with a 30-minute lifetime. `identity.complete` changes the password, consumes the challenge and revokes existing sessions; the user signs in with the new password. The earlier completion page misleadingly described invitations for recovery. The fix adds purpose-specific reset text/button and a password-reset success message. A modified URL action hint cannot convert a reset challenge into an invitation because the server validates the stored purpose.

The email code is a single-use verification credential. Access/refresh session credentials are used after normal login and stored in secure HttpOnly cookies. An organization role is neither of those credentials: it is a membership property rechecked by authorization.

## Why a Project Manager still needs grants

| Question | Relevant boundary |
| --- | --- |
| May this person administer organization members? | Active organization role must be Admin |
| May this PM create a project in this portfolio? | Eligible role plus portfolio manage grant |
| May this member read/edit the project? | Applicable project/portfolio grant and role; owner alone is insufficient |
| May this PM manage resource planning? | Resource-management flag plus relevant project permission for allocations |
| May this member see sensitive effort? | Explicit effort permission; do not infer from resource management or Admin role |
| May this PM edit a framework draft? | Active PM plus framework-editor grant; only Admin publishes |
| May this person submit or review an assessment? | Named eligible respondent/reviewer; reviewer differs from respondent |
| May a Viewer read completed scores? | Completed-result grant; private answers/evidence remain restricted |

Trace `identity.principal` and the owning delivery/capacity/assessment guards instead of treating a hidden frontend button as security. The membership selects the organization and role; PostgreSQL RLS/context restrict database scope. Grants add specific work access within that boundary. Changing a role does not erase stored grants, so revocation/reactivation should include a grant review. Other organizations' memberships remain separate.

Browser access controls now exist: project Grants, Resource access, framework Access and completed-assessment Access. They are not API-only. Test in separate browser profiles because tabs share cookies, and confirm the actual current account before a permission exercise.

## Evidence and debugging questions

The isolated suite covers new/existing-user invitation acceptance, replay/expiry/cancel/resend, role isolation, session revocation and provider failures. The latest recovery regression checks reset heading, masked token, success, old-session denial and new-password login. The live Gmail exercise verified signup, existing-account Viewer acceptance and recovery; it did not repeat every lifecycle variant with real inboxes. Read the report before expanding a claim.

When authentication failed in the live setup, a connection-only probe showed successful verified STARTTLS followed by Gmail `535`. Private boolean comparisons confirmed loaded values matched `.env` but the App Password was incomplete. After the user corrected it and services were recreated, authentication returned `235` and delivery succeeded. No secret needed to be printed to diagnose the fault.

Practice explaining: Why is SMTP acceptance weaker evidence than inbox receipt? Why must Verify and Sign in be separate concepts? Why does an Admin membership in one organization not make the user Admin everywhere? Why might revoking one project grant leave portfolio-based access? Why can result access never turn a Viewer into an assessment respondent? Use the website exercises and code/tests to support each answer.


## 10 October account repair follow-up

[`identity.authenticated`](../../../services/api/ppm_api/identity.py) now separates personal `AccountAuth` from organization `Auth`. A verified globally active identity can authenticate without memberships; a revoked membership immediately fails tenant operations. [`account_status.py`](../../../scripts/account_status.py) provides an explicit development operator disable/enable operation, preserves ownership/memberships and revokes sessions. Neither password reset nor invitation acceptance enables a disabled identity. The displayed organization administrators are derived from active Admin memberships, not a separately copied owner name.

The invitation acceptance role remains the stored challenge role. A Project Manager still needs portfolio manage for project creation, explicit project edit/manage for existing delivery work and separate resource/effort grants. The diagnosed Hement relationship required a scoped project grant. [Repair evidence](../../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) records source traces, negative tests and the separate training browser journey; earlier Gmail evidence is not relabelled as a new SMTP run.
