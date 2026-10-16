# Sprint 8.1 — Making everyday use easier

**Status:** Local pilot implementation exists; parent sprint acceptance remains open. This report is separate from the completed-sprint reports.

## What was built and why it matters

After the core modules existed, this work filled gaps that made them difficult to use: creating an organization, finishing setup, finding records, sharing assessment access and seeing assigned work. Follow-up account repairs improved membership handling and browser guidance.

| Delivered function | Where to access it | How to check / expected result |
| --- | --- | --- |
| Verified self-service signup | [Signup](http://localhost:3000/signup). | Request signup with an authorized practice address, open its verification link and complete account setup. A new organization/Admin is created after verification, not merely after the request. |
| Account email delivery, resend and cancel | Admin: **Account & access → Pending invitations**. | Inspect a practice invite, resend it and use only the latest link. Cancelling/replacing a link makes the old link unusable. Delivery depends on installation configuration. |
| Saved setup guidance | **Workspace overview → Getting started**; **Organization setup**. | Save organization profile/configuration and complete relevant setup steps. Reload and check that guidance reflects saved progress. |
| Framework-editor access | **Maturity assessments**, framework **Access** controls. | Admin grants a PM draft editing; the PM can edit the permitted draft but cannot publish as Admin. |
| Shared completed results | Completed assessment **Access** controls. | Admin shares a completed result with a practice Viewer. The Viewer can read scores/coverage but not private answers, notes, files or history. |
| Search real records | Top-bar Ctrl+K → record search, or overview search. | Find permitted projects, work, risks and assessments by name. Open a result; hidden records should not be disclosed. |
| Search and paging in lists/selectors | Assessment lists and shared record selectors. | Search for an older permitted record and use paging where available. Records are not limited to the first visible page. |
| Department comparisons by version and period | Assessment **Department comparison**. | Select the published version and creation-date period. Only eligible completed results from that exact version are compared. |
| Personal assignment list | **Workspace overview → My work**. | Assign a practice item/assessment to an eligible person. That person sees the permitted actionable record. |
| Saved personal notification state/preferences | Top-bar **Open notifications**. | Inspect an eligible event, mark its receipt read and reload. The read state persists. In-app receipts are not scheduled email reports. |
| Optional business metadata | Project/work editors and industry filtering. | Save supported metadata, reload and filter where available. Blank values remain Unknown rather than invented facts. |
| Refresh after saved changes | Command center while another authorized person changes a source record. | Save a practice milestone change in another profile. The authorized dashboard receives a saved-change notice and refetches facts. |

## A short check you can follow

**You need:** Admin, practice PM/Viewer, an existing project and a completed assessment. See [Getting access](../START_HERE.md).

1. As Admin, share the completed assessment result with the Viewer.
2. As Viewer in another profile, open Maturity assessments and inspect the result.
3. Confirm that scores are visible and private evidence is not.
4. Search for a project the Viewer is permitted to read, then open it.
5. Keep the Viewer's Command center open while an authorized editor saves a milestone change.
6. Check the dashboard refresh and inspect relevant My work/notification receipts as the assigned person.

**Expected result:** Sharing is specific, search respects access, assignments are personal, and dashboards refresh from saved authorized changes.

## Later account repairs included in today's application

The 10 October follow-ups separate an active personal account from its organization membership: removing a membership denies organization work but can still allow personal sign-in. They also added password visibility controls, organization-name/profile improvements, calendar navigation and clearer business errors. A further account-authority migration exists in the current source. These are follow-ups, not evidence that the original Sprint 02 delivered every current account function.

The [account-email verification](../../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) records real development Gmail signup, an existing-account Viewer invitation and recovery on 10 October. This supersedes the original Sprint 8.1 email blocker for those demonstrated flows; it does not guarantee mail delivery on every installation.

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Signup and account/invitation controls | [Signup page](../../../apps/web/app/signup/page.tsx), [identity client](../../../apps/web/app/account/identity-client.tsx), [identity service](../../../services/api/ppm_api/identity.py), [mail adapter](../../../services/api/ppm_api/account_mail.py) |
| Setup, record search, My work, notifications and comparison | [Pilot screen controls](../../../apps/web/components/pilot.tsx), [pilot service](../../../services/api/ppm_api/pilot.py), [live workspace updates](../../../apps/web/components/live-workspace.ts) |
| Assessment sharing | [Assessment screen](../../../apps/web/components/assessments.tsx), [assessment service](../../../services/api/ppm_api/assessment.py) |
| Pilot records and subsequent account repairs | [Pilot migration](../../../services/api/migrations/versions/0008_pilot_completion.py), [account repair](../../../services/api/migrations/versions/0009_account_repair.py), [account authority](../../../services/api/migrations/versions/0010_account_authority.py) |
| Browser checks | [Pilot scenario](../../../tests/browser/pilot.spec.ts), [account repair scenario](../../../tests/browser/account-repair.spec.ts) |

## Recorded checks and remaining work

The original pilot recorded 74 backend tests, 12 combined browser passes and later affected-flow checks. Subsequent account/email verification is documented separately. Hosted CI for the relevant working changes and visual verification of regenerated Word guides remain open in the sprint records. This is why the parent sprint remains outside the completed group.

[Original report](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md) · [Pilot user guide](../../03-sprints/active/sprint-8.1/SPRINT_8_1_USER_GUIDE.md) · [Account repair evidence](../../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) · [Report index](../README.md)
