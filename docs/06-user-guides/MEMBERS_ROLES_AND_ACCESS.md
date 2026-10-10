# Website guide: members, Project Managers and access

Updated 10 October 2026. Every step below uses the website and the member's email inbox. SMTP configuration belongs to the operator, in the [Gmail SMTP setup guide](../07-setup-and-deployment/GMAIL-SMTP-SETUP.md).

## Start from the verified progress

Signup, password recovery and an existing-account invitation have been completed with real Gmail messages on this development instance. The personal account is Admin in **Northstar Gmail Delivery Test 2026-10-10** and Viewer in **Northstar Invitation Test 2026-10-10**. The separate test Admin administers the second organization. Personal signup and invitation arrived in Spam; the second Admin's signup arrived in Inbox. Check both folders. These are training organizations, not preloaded business projects.

Open **Account & access** and check the signed-in email, selected Organization and current role before every change. A person's role applies to the selected organization. A successful invitation does not change their role in another organization. Use separate browser profiles or separate browsers for different members; ordinary tabs share sign-in cookies. A login in another browser does not update the Codex website panel.

For the full sample organization, project, staffing and assessment framework, follow the [website walkthrough](WEBSITE_WALKTHROUGH.md). This guide explains membership and permissions in more detail.

## Choose the right role

| Role | Intended person | Membership powers | Work access |
| --- | --- | --- | --- |
| Admin | Organization owner or administrator | Invite, change roles, deactivate/reactivate members; manage grants | Organization administration; sensitive resource effort still has its own permission |
| Project Manager | Delivery manager, assigned respondent or independent reviewer | Own profile, password and sessions; cannot administer membership | Relevant project/portfolio, resource and framework grants, or assessment assignments are also required |
| Viewer | Stakeholder inspecting permitted records/results | Own profile, password and sessions; cannot administer membership | Read-only delivery scope and completed-result access; cannot submit assessments, evidence or reviews |

Respondent and Independent reviewer are assessment assignments, not organization roles. A reviewer must be a different eligible active Admin/Project Manager from the respondent. Project owner, resource profile and team member are also different from a login role. None grants access automatically.

## Invite a new Project Manager

1. Sign in as an Admin of the intended organization. Check its name in the Organization selector.
2. Open **Account & access** (`/account`). Find **Invite a member**.
3. Enter an actual email address that the intended person can access. For controlled tests, obtain authorization for that inbox first; do not invent aliases or use another person's address.
4. Choose **Project Manager** from **Role**. To add a Viewer or another Admin, choose that role instead.
5. Click **Create invitation**. Inspect **Pending invitations** for the email and role.
6. Click **Refresh invitations** to check delivery. Waiting means queued/retrying. **Accepted by email provider — inbox arrival unconfirmed** means the sending provider accepted it; ask the person to check Inbox and Spam. A local-preview label means no inbox email was sent. A failed status needs the operator's attention before retrying.
7. The member opens **Enterprise PPM: invitation to [organization]** in their own browser profile. Check the organization and invited role.
8. A new account enters a display name and chooses a website password. An existing verified account enters its current website password, including a recently reset password. Do not enter the Admin's password or Gmail password.
9. The link automatically supplies a masked one-time token. Click **Verify and continue** to accept. Then open **Sign in** and sign in with the recipient's email and website password.
10. Select the invited organization if the account belongs to more than one. Confirm **Project Manager** on Account & access.
11. Back in the Admin profile, reload Account & access. **Organization members** should show the person as Active with the chosen role. The accepted invitation disappears from Pending invitations; the access audit records acceptance.

Use invitations to join an existing organization. Sending the colleague through `/signup` instead creates a separate organization after verification. An invitation request alone is not an active membership, and SMTP acceptance alone is not evidence of receipt.

## Promote the existing Viewer to Project Manager

You already have a verified Viewer in the invitation-test organization, so you can use it for a PM learning exercise without another invitation or email. The following is an optional website exercise; the completed email test itself left that member as Viewer.

1. In the test Admin's browser profile, select **Northstar Invitation Test 2026-10-10**.
2. Open Account & access → **Organization members**. Search the member's email in **Filter loaded members** if needed.
3. In that member's row, change **Role for [email]** from Viewer to **Project Manager**. Keep **Active** checked.
4. Click that row's **Save member** and confirm the access-change dialog. If the page reports stale data, reload and repeat from the latest member row.
5. In the member's separate browser profile, reload Account & access. Confirm the selected organization and **Project Manager** role.
6. Provide the scoped grants below. Promotion does not automatically reveal every project or resource.
7. To return to the original test state later, use the same Admin controls to restore **Viewer**. Review and revoke any work grants added for the exercise.

Do not resend an invitation to change an existing member's role. Existing memberships are not overwritten or silently reactivated by acceptance. Use **Save member**. Preserve an active Admin: the final active Admin cannot be demoted or deactivated.

## Give a PM permission to create projects

This example uses **Customer Experience Portfolio** and **Priya Manager** from the full walkthrough. Substitute your saved portfolio and accepted PM member. If neither exists, first follow the walkthrough's organization/portfolio setup and invitations.

1. As Admin, open **Organization setup** (`/organization`) and its **Project & portfolio access** section.
2. Click **Create project & portfolio access**. Name the record **Priya — customer portfolio management**. Add a description such as **Allows project creation in the training portfolio**.
3. Select **Member: Priya Manager** and **Portfolio: Customer Experience Portfolio**. Leave Project blank; choose one scope, not both Project and Portfolio.
4. Set **Access: manage** and click **Save record**.
5. In Priya's profile, open **Projects**, create a project in that portfolio, save and reload. An eligible PM who creates a project receives a project-creator manage grant for that new project.

Portfolio **read** lets a permitted member read its projects; it does not permit project edits. Portfolio manage is needed for PM project creation. Selecting a person as owner or adding them to a team does not replace the grant.

## Give access to an existing project

1. As Admin, open **Projects**, click the intended project's name, then open **Project & portfolio access** in its workspace.
2. Click **Create project & portfolio access**. Enter a descriptive name, select the accepted member and the intended project scope. When the project is already fixed by the workspace, use that scope.
3. Select **read** for a Viewer who only needs to inspect the project. Select **edit** or **manage** for a PM according to the delivery responsibilities you want to permit.
4. Save and confirm the grant appears. Reload the member's separate browser profile and open that project.
5. Check an allowed action: the Viewer reads records; the PM edits an allowed delivery record and reloads it to confirm persistence. PM project access does not allow organization membership/grant administration.

To revoke, edit the relevant grant and archive it through the website. Test after reloading the member's open page and search results. Also inspect portfolio grants: revoking one project grant does not remove access still supplied by another applicable grant. Missing scoped records may be hidden rather than producing a visible error.

## Resource and sensitive effort access

1. As Admin, open **Resource planning** (`/resources`). Create the resource profile first if needed; a resource is a capacity/staffing record, not another login account.
2. Open **Resource access** → **Create resource access**. Enter a name, select **Resource** and **Member**.
3. Check **May manage resource** when the PM should manage that resource's permitted planning records.
4. Grant **May access sensitive effort** separately only when that person's duties require it. Resource management, project ownership and Admin role do not substitute for the explicit effort permission. A Viewer cannot enter sensitive effort.
5. Save. In the PM profile, select the resource and check its visible summary and permitted forms. Resource allocations also need the applicable project permission.
6. Revoke/archive the resource grant when access is no longer needed, and reload the other profile to verify the effect.

Availability/calendar setup, team membership and actual effort data remain separate records. Follow the full walkthrough for complete sample values; giving a permission does not create staffing data.

## Framework editing, assignments and result readers

1. As Admin, open **Maturity assessments** (`/assessments`) and find the framework.
2. In its **Access** panel, select an active PM under **Member** and click **Grant framework editing**. The PM can edit the framework draft; only Admin publishes a version.
3. To make the PM a respondent or reviewer, use **Assign assessment** on a published framework. Choose two different eligible active Admin/PM members as respondent and independent reviewer. A framework-editor grant is not a respondent assignment.
4. The assigned respondent completes and submits answers/evidence. The named independent reviewer reviews and completes the assessment. A Viewer cannot do either job.
5. To let a Viewer read the completed scores, use the completed assessment's **Access** panel, choose the member and click **Grant result access**.
6. Confirm the Viewer can open completed results. This grant shares scores, not private answers or evidence, and does not permit editing or review.
7. Use the panel's revoke control to remove a framework/result grant and test again after reload.

Project access, resource access, framework editing, assessment participation and completed-result readership are independent. Grant only the scopes the member needs.

## Deactivate, reactivate and review access

As Admin, find the member on Account & access, clear **Active**, click **Save member** and confirm. That person's membership in this organization stops authorizing access; their memberships in other organizations are separate. Do not assume deactivation deletes their global account, history or saved grants. For reactivation, check Active, select the intended role, save and review old grants and assignments before returning the person to work.

Use the **Access audit** to review membership/invitation actions. Personal **Active sessions** controls are on Account & access; password recovery revokes the account's existing sessions. Resetting a password is different from granting a role.

## Troubleshooting and role exercise checklist

| Symptom | Website check / next step |
| --- | --- |
| No invitation email | Check spelling, Inbox and Spam; Admin refreshes invitation status; operator investigates failed sending |
| Invalid or expired invitation | Ask Admin to resend; open only the newest message. Cancelled, replaced or used links cannot be accepted |
| Password rejected during existing-account acceptance | Use the recipient's current website password; recover it if forgotten. A replacement recovery invalidates older reset links |
| PM sees no project or cannot create one | Check selected organization, active PM role, project grant or portfolio manage grant |
| Resource or effort is restricted | Check its separate Resource access flags; project access is insufficient |
| PM cannot answer/review | Check published assignment, respondent/reviewer identity, active eligible role and different reviewer |
| Viewer cannot see assessment results | Check completed state and completed-result grant; a project grant does not share results |
| Revocation seems ineffective | Reload, check the active organization and inspect other applicable portfolio/project grants |
| Final Admin change refused | Retain an active Admin; appoint an appropriate additional Admin before attempting a handover |

Record the expected and actual behavior for Admin, PM and Viewer in separate profiles. Confirm saved records after reload. The live email exercise verified a Viewer invitation; broader role/grant controls were source-reviewed and covered by the retained isolated tests, not newly exercised against every real account in this documentation update.


## Account independence after the 10 October repair

Clearing membership Active does not disable or delete the global account. The removed organization immediately rejects protected requests, while sign-in, personal profile/session controls and other active memberships remain usable. An account without memberships sees an explanation and organization selection/onboarding state. Global account suspension is a separate operator operation, not an organization member control. Global disabling also blocks reset/invitation completion from silently reactivating the identity.

Organization name starts read-only: **Edit name**, **Save organization name**, or **Cancel name change**. Administrators shown in the profile come from active Admin membership and active account status. For Hement's existing Admin-created portal, the correction adds only an explicit project edit grant; portfolio manage permits project creation but does not imply editing other projects. [Current report and permission matrix](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) record the exact evidence and scope.
