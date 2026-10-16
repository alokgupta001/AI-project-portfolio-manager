# Sprint 02 — Accounts and controlled access

**Status:** Completed for local accounts and organization access.

## What was built and why it matters

People can sign in, manage their own accounts and work inside the correct organization. Admins can invite members and control their roles. One organization's records must not become visible simply because someone knows a record's address.

| Delivered function | Where to access it | How to check / expected result |
| --- | --- | --- |
| Activate an account and choose a password | The private invitation/activation link opens **Account completion** at `/account/complete`. | Open a valid practice invitation and complete it. The invited membership becomes active. A used/expired link cannot be reused. |
| Sign in and sign out | [Sign in](http://localhost:3000/login); **Account & access** for sign out. | Sign in with your activated account, confirm your identity, then sign out. Protected records require sign-in again. |
| Update your own profile | **Account & access** at `/account`. | Change your display name and reload. The saved name remains. |
| Switch organizations | Organization selector at the top of the workspace. | With two memberships, switch between them. The displayed organization and permitted records change. |
| Invite and administer members | Admin: **Organization members** at `/account#members`. | Invite a practice member, have them accept, then inspect their role/state. A PM or Viewer cannot administer members. |
| Change roles or deactivate a membership | Admin: member controls on **Account & access**. | Change a practice membership and reload as that person. Organization permissions follow the change. The last active Admin is protected from removal/demotion. |
| View and revoke sign-in sessions | **Account & access**, session controls. | Sign into a second browser profile, revoke that session from the first, then try an organization action in the second. It must require a valid session. |
| Recover a forgotten password | [Password recovery](http://localhost:3000/account/reset). | Request recovery for your own practice account, open the delivered link and set a new password. Previous sessions are revoked. |
| Read the identity change log | Admin: identity audit on **Account & access**. | Make a practice membership change and inspect the scoped audit records. |
| Keep organizations separate | Applies across all protected screens and requests. | Use separate practice accounts in separate organizations. A record visible in one should not become readable in the other without valid access. |

## A short check you can follow

**You need:** One activated Admin and an invited practice member. See [Getting access](../START_HERE.md). Invitation and recovery checks also need working link delivery.

1. Sign in as Admin and confirm the selected organization.
2. Invite a practice Viewer through Organization members.
3. Open the invitation in a separate browser profile and complete acceptance.
4. Confirm the Viewer can manage their own profile but cannot invite or change members.
5. In the Admin profile, deactivate the practice membership; reload an organization screen as the Viewer.
6. Restore the practice membership if you need it for the remaining reports.

**Expected result:** The account and membership controls work, and organization operations respect the current membership. Later account repairs allow a globally active account with no organization access to sign in to its personal account; that does not restore organization permissions.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Account screens and interactions | [Identity client](../../../apps/web/app/account/identity-client.tsx), [login](../../../apps/web/app/login/page.tsx), [recovery](../../../apps/web/app/account/reset/page.tsx), [completion](../../../apps/web/app/account/complete/page.tsx) |
| Account, session and membership rules | [Identity service](../../../services/api/ppm_api/identity.py), [account tables](../../../services/api/ppm_api/identity_tables.py) |
| Original account storage | [Identity migration](../../../services/api/migrations/versions/0002_identity.py) |
| First-Admin and test-link tools | [Identity bootstrap](../../../scripts/bootstrap_identity.py), [private local mailbox](../../../scripts/local_mailbox.py) |

## Recorded checks, later changes and limits

The sprint recorded 28 backend and three browser tests covering account flows, permissions and organization isolation. Original delivery used a private local mailbox. Self-service signup, email delivery, invitation resend/cancel and later account repairs are described in [Sprint 8.1](../in-progress/SPRINT-8.1.md); they were not all delivered in Sprint 02.

[Original report](../../03-sprints/completed/sprint-02/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-02/TESTING_REPORT.md) · [Report index](../README.md)
