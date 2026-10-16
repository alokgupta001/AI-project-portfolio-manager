# Website user manual: from a new organization to a reviewed assessment

Prepared 10 October 2026. Covers the current Enterprise PPM website source and local development behavior. The original account signup, existing-account invitation acceptance and recovery were exercised through the website and Gmail with authorized test accounts. The dated account-repair follow-up now executes the applicable project/assessment journey through section 18 using four automated browser sessions and private local test mail; [execution evidence](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) distinguishes that run from the earlier Gmail acceptance and from optional/external branches.

Account email update: development Gmail SMTP is enabled. Personal signup arrived in **Spam** and the separate test-Admin signup arrived in **Inbox**, according to the recipients. Recovery receipt/reset/sign-in are confirmed. A website invitation was accepted by the existing personal account; the target organization's Viewer membership and acceptance audit are verified. See [email acceptance report](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md). On this instance use the website and Gmail, checking Spam as well as Inbox. Private-mailbox instructions apply only to instances explicitly running in local test mode.

## 1. What you will accomplish

You will create a fictional organization, invite members with different roles, configure the organization, plan a project, enter delivery and resource information, build an assessment framework from scratch, answer an assessment, independently review it, and inspect the results as a Viewer.

Every action in the walkthrough is a website action. You do not need to write code, run a command, use Docker, prepare an existing framework, or already own project documents. The sample information and evidence notes are supplied below. You can paste evidence directly into the website, so uploading a file is optional.

**One prerequisite belongs to the operator:** working email delivery. This development instance now sends through Gmail SMTP, and signup receipt/activation have been confirmed. You request signup/invitations on the website and complete them from the received email link. If another instance says **local test mode**, no inbox email is sent; ask its operator to arrange delivery or privately supply the intended recipient's link. The guide contains no operator commands. Do not mistake a generic request-success message for a verified account.

If the site is already available and delivery works, the remaining exercise uses website screens only. If the site itself is unavailable, the website has no button to start its underlying services.

### Website and Gmail inbox journey

Use real email addresses the intended members can access. Submit signup on the website, then check Gmail Inbox and Spam for **Enterprise PPM: verify your email**. Open the private link, set your name/password and sign in. For invitations, Admin uses Account and access → Invite a member; the recipient opens **Enterprise PPM: invitation to [organization]**, checks the role, and accepts using a new password or the existing verified account password. For recovery, use `/account/reset`, open **Enterprise PPM: reset your password**, enter your display name as requested by the current form and choose a new password, then sign in again. Verification/invitation links expire in 24 hours; recovery in 30 minutes.

Signup delivery has been tested on this development instance: the message arrived in Spam and the recipient activated their Admin account. Check both Inbox and Spam; you can mark an expected legitimate message **Not spam** in Gmail. Recovery completion is confirmed; existing-account invitation acceptance and the target Viewer membership are also verified. If the website says local test mode, no inbox message is sent. Sender/provider setup belongs to the operator; users do not enter SMTP credentials into website forms. Remote recipients need a reachable website address; a localhost link only opens this application on the computer where it runs.

Recovery emails open the shared `/account/complete` route with reset instructions: **Reset your password**, **Display name**, a masked **One-time token**, a new password and **Reset password**. The token is automatically loaded from the private email link; you do not need to copy or share it. It is a single-use recovery credential, not an invitation or your normal sign-in token. After success, sign in with the new password; existing sessions are signed out. Older messages can show **Complete your account request** with generic guidance. Open the newest recovery email after requesting a replacement; older links stop working.

### What the email token and Verify mean

The private email link contains a **one-time token**, a code that identifies the signup, invitation or recovery request. The website loads it automatically and hides it after loading. Keep the link private; you do not need to copy, save or send the code to anyone.

For an invitation, **Verify and continue** checks the code and your password, then adds your membership with the invited role. It does not sign you in automatically. **Sign in** is the next step: enter your email and website password to start a normal login session. After signing in, select the invited organization from the Organization list. Your role can differ between organizations; for example, you can be Admin in your own organization and Viewer in the invited one.

Signup and invitation codes expire after 24 hours; recovery codes expire after 30 minutes. A successful completion uses the code once. Resending/replacing a request invalidates its earlier code; if a link is expired or already used, follow the replacement instructions rather than trying to reuse it.

### About Viewer submissions

The website has **Admin**, **Project Manager**, and **Viewer** roles. Respondent and Independent reviewer are assessment assignments, not additional organization roles.

A Viewer does not submit assessments, upload assessment evidence, create delivery records, or review assessments. They inspect permitted projects, dashboards, and shared completed scores. Both assessment participants must be different active Admin or Project Manager members. This manual uses a Project Manager as respondent and another Project Manager as reviewer.

Business users sometimes provide requirements, acceptance feedback, meeting notes, or evidence to a project manager. There is currently no Viewer document-submission journey in this website. The sample documents in Section 12 therefore belong in the assigned respondent's evidence notes. Sprint 09 now provides a separate Document library for authorized Admin/PM uploads, PDF/Word intake, English OCR and keyword citations. Viewer can read permitted sources but cannot submit them. Follow [the library guide](../03-sprints/completed/sprint-09/USER_GUIDE.md); AI interpretation remains planned.

## 2. Your sample organization and people

Use these fictional names and values to learn the flow. They are training data, not facts about a real business.

| Item | Value |
| --- | --- |
| Organization | Northstar Website Training |
| Organization timezone | Asia/Kolkata |
| Currency | INR |
| Department | Digital Delivery |
| Team | Portal Delivery Team |
| Strategic goal | Reduce customer onboarding effort |
| Portfolio | Customer Experience Portfolio |
| Program | Customer Self-Service Program |
| Project | Customer Onboarding Portal |
| Project objective | Provide a self-service onboarding portal and reduce manual follow-up. |
| Framework | Northstar Delivery Readiness |
| First assessment | Digital Delivery — Portal Readiness — October 2026 |

Create four people:

| Display name | Organization role | Purpose |
| --- | --- | --- |
| Asha Admin | Admin | Organization setup, invitations, access, framework publication and assignments |
| Priya Manager | Project Manager | Project planning and assessment responses |
| Ravi Reviewer | Project Manager | Independent assessment review |
| Vera Viewer | Viewer | Read permitted project information and completed assessment scores |

Use four distinct email addresses you control or the actual addresses of participating testers. The names above are examples; there are no existing accounts or preassigned passwords. Each person chooses their own password. Do not paste an invented address into an invitation and expect a real message to arrive there.

### Role and permission map

| Activity | Admin | Project Manager | Viewer |
| --- | --- | --- | --- |
| Invite/change organization members | Yes | No | No |
| Configure organization, department/team, portfolio and calendar | Yes | Not through these setup forms | No |
| Create project | Yes | With portfolio manage grant | No |
| Edit delivery project and related records | Yes | With project edit/manage access | No |
| Read delivery records | Organization scope | Granted scope | Granted scope |
| Create resource profiles / grant resource access | Yes | No | No |
| Manage an existing resource/allocation | Yes | With resource management and applicable project permission | No |
| Access sensitive effort | Separate effort permission applies | Separate effort permission applies | No |
| Create/publish framework | Yes | No | No |
| Edit framework draft | Yes | Explicit framework-editor grant | No |
| Create assessment assignment through current UI | Yes | No | No |
| Answer/submit assessment | Only when assigned respondent | Only when assigned respondent | No |
| Review assessment | Only when assigned independent reviewer | Only when assigned independent reviewer | No |
| Read completed assessment scores | Admin scope | Participant or completed-result grant | Completed-result grant |
| Read private assessment evidence | Admin scope | Eligible named respondent/reviewer | No |

Always combine role and record permissions. A role label is not a blanket right to every record.

For dates, this manual uses a training project from **12 October to 6 November 2026** and an initial sprint from **12 to 23 October 2026**. If you run the guide later, move the dates together to your training period. Never record simulated completion dates in a real project as if work actually occurred.

### Keep the four sessions separate

1. Create a separate browser profile for each person, or use separate browsers.
2. Sign in to one account in each profile.
3. Verify the name, current organization, and role on **Account and access** before each role exercise.
4. Keep the Admin profile available while testing permissions in the other profiles.

Different tabs in the same profile share login cookies. A second ordinary tab is not a separate person. If you have only one profile, sign out before signing in as the next member; expect to repeat this several times.

## 3. Website navigation and common form behavior

The local website address is [http://localhost:3000](http://localhost:3000). If your application has a different address, use that same address consistently and append the paths below. For the local identity flow, use `localhost` consistently rather than switching between `localhost` and `127.0.0.1`.

| Screen | Path | What you do there |
| --- | --- | --- |
| Sign up | `/signup` | Request a verified new account and new organization |
| Sign in | `/login` | Sign in with an activated account |
| Workspace | `/` | Getting started checklist, My work, navigation |
| Account and access | `/account` | Organization name, invitations, membership, personal account and sessions |
| Organization setup | `/organization` | Timezone, currency, departments, teams, goals and delivery grants |
| Portfolios | `/portfolios` | Portfolios, programs and portfolio alignment |
| Projects | `/projects` | Find/create a project and open its workspace |
| Resource planning | `/resources` | Resource profiles, calendars, availability and allocations |
| Maturity assessments | `/assessments` | Frameworks, assignments, answers, evidence and review |
| Command center | `/command-center` | Executive, Delivery, Risk and Resource dashboards |
| Password recovery | `/account/reset` | Request a password recovery message |

Open a project by clicking its name in the Projects list. Its address includes a generated record identifier; you do not need to copy or type that identifier.

For delivery and resource records, the usual pattern is:

1. Open the relevant page and section tab.
2. Click **Create ...** for that section.
3. Enter **Name**, **Description**, and the listed fields.
4. Select related records by their saved names; use search and **Next choices** if necessary.
5. Click **Save record**.
6. Confirm the record appears in the list. Reload once to confirm it was saved.

Use **Edit [record name]** to change a mutable record. Some records, including calendars, expenditure entries, status updates, and plan baselines, preserve history and cannot be edited like ordinary records. Append a new record or use the supported reversal flow instead.

If a stale-data/conflict error appears, preserve any unsaved text, reload the current data, and retry from the latest saved record. Repeated clicking does not fix missing permissions or a conflict. Clear search/status/archive filters if a record seems absent.

## 4. Sign up as the first Admin

**Person:** Asha Admin, in the Admin browser profile.

1. Open `/signup`, or click **Create an account** on the sign-in screen.
2. Enter Asha's email address.
3. Enter **Northstar Website Training** as the organization name.
4. Submit the signup form to request verification.
5. Read the response. The website uses a generic message for eligible and existing addresses; it does not prove the account was created.
6. Open the latest verification message sent to Asha. If local mode is active, obtain Asha's private link from the operator. If neither is possible, stop this account-creation step as **Blocked**.
7. Open that link in Asha's browser profile.
8. Enter the display name **Asha Admin** and choose a private password. The password must be at least 12 characters and at most 72 UTF-8 bytes; ordinary ASCII characters make the length easy to judge.
9. Submit the activation/verification form.
10. Open `/login` and sign in with Asha's email and password.
11. Open `/account`; confirm the current organization is **Northstar Website Training** and the role is **Admin**.
12. Open Workspace and inspect **Getting started**. A fresh signup does not automatically insert demo projects or frameworks.

**Expected result:** After verification, the new account has a new organization and Admin membership. Requesting verification alone creates neither the finished organization nor the usable login.

Signup creates a new organization. Do not send Priya, Ravi, or Vera through signup to join Asha's organization; invite them instead.

## 5. Invite and activate the other members

For an expanded explanation of adding a Project Manager, promoting your existing Viewer, granting work access and deactivating/reactivating members, use [Members, roles and access](MEMBERS_ROLES_AND_ACCESS.md). The current verified personal account can be used as Viewer or optionally promoted by its invitation-test Admin for a PM exercise; changing roles in this guide is an instruction for you, not a change already applied to that account.

### 5.1 Admin creates invitations

1. As Asha, open **Account and access** (`/account`).
2. Find **Invite a member**.
3. Enter Priya's actual email address.
4. Set **Role** to **Project Manager**.
5. Click **Create invitation**.
6. Repeat for Ravi with **Project Manager**.
7. Repeat for Vera with **Viewer**.
8. Inspect **Pending invitations**. Check the recipient, role, delivery status, and expiry.

Use **Refresh invitations** to check progress. **Waiting to send (or retry)** means queued. **Accepted by email provider — inbox arrival unconfirmed** means SMTP acceptance, not Gmail receipt. **Local test message — no inbox email sent** means private development preview. **Sending failed after retries** means the operator must fix sending before you resend. Historical delivery labels remain unverified. Expired invitations stay listed so Admin can resend or cancel them. Signup/activation/invitation links expire after 24 hours. Do not include private links in screenshots, shared notes, or this manual.

### 5.2 Each member accepts

For each member separately:

1. Open their own browser profile.
2. Open the invitation message for that email address and organization. If necessary, obtain that intended recipient's private link from the operator.
3. Open the link in that member's profile.
4. For a new account, enter the display name from Section 2 and choose a private password satisfying the same password limits.
5. For an already verified account, follow the acceptance screen using the existing account password.
6. Submit the invitation acceptance form.
7. Sign in at `/login`.
8. Open `/account` and confirm the current organization and assigned role.

**Expected result:** All four people belong to the same organization. In Asha's profile, **Organization members** shows each accepted member as Active.

If an existing user belongs to several organizations, select the correct current organization before proceeding. An invitation does not silently overwrite an existing membership or reactivate a disabled member.

### 5.3 Invitation and member-management exercise

Use an additional controlled test address for this optional exercise, so you do not disrupt the four main accounts.

1. Create an invitation, then use **Resend** in Pending invitations.
2. Verify that the earlier link no longer works and the latest one is the applicable link.
3. Create another invitation and use **Cancel**. Verify that its link cannot be accepted.
4. In Organization members, choose a member's role, keep **Active** checked, and click **Save member** to change their role. Read and confirm the access-change dialog.
5. To disable a test member, clear **Active**, click **Save member**, and confirm.
6. In that member's separate browser profile, reload and check that the removed access is denied. Restore Active afterward if the person is needed for the exercise.

Keep Priya and Ravi as Project Managers for assessment work. Do not disable or demote Asha during the walkthrough. The final active Admin is protected.

## 6. Admin: configure the organization from scratch

**Person:** Asha. Complete these steps before delivery planning.

### 6.1 Organization name, timezone and currency

1. Open `/account`, find **Organization profile**, and verify the name **Northstar Website Training**. The name is read-only initially. If necessary, click **Edit name**, change it, and click **Save organization name**; **Cancel name change** discards the draft. Unchanged names do not need saving. The profile also shows the administrators derived from active memberships, optional description/industry/website, member counts and operating setup state.
2. Open **Organization setup** (`/organization`).
3. If the page says setup is required, click **Configure organization**. Otherwise use the **Organization configuration** section and its Create/Edit action.
4. Enter **Name:** Northstar operating settings.
5. Enter **Description:** Training organization using India time and INR reporting.
6. Enter **IANA timezone:** `Asia/Kolkata`.
7. Enter **Currency (3-letter code):** `INR`.
8. Click **Save record** and confirm the saved configuration.

The display name on Account and access is separate from this configuration record's name. Timezone and currency settings are required before delivery records can be created.

### 6.2 Department

1. Open the **Departments** tab.
2. Click **Create departments**.
3. Name: **Digital Delivery**.
4. Description: **Owns the customer portal and its delivery practices.**
5. Owner: **Asha Admin**.
6. Save.

### 6.3 Team

1. Open **Teams** and create a record.
2. Name: **Portal Delivery Team**.
3. Description: **Plans, builds, tests and releases the onboarding portal.**
4. Department: **Digital Delivery**.
5. Owner: **Priya Manager**.
6. Save.

### 6.4 Team membership

1. Open **Team membership** and create a record.
2. Name: **Priya — Portal Delivery Team**.
3. Team: **Portal Delivery Team**.
4. Member: **Priya Manager**.
5. Start date: **2026-10-12**. Leave End date blank for continuing membership.
6. Save.
7. Repeat for **Ravi — Portal Delivery Team**, member **Ravi Reviewer**, using the same team and start date.

Team membership describes organization structure. It does not replace project grants or assessment assignments.

### 6.5 Strategic goal

1. Open **Strategic goals** and create a record.
2. Name: **Reduce customer onboarding effort**.
3. Description: **Enable self-service onboarding and target 100 staff hours saved per reporting period.**
4. Owner: **Asha Admin**.
5. Save.

### 6.6 Portfolio and program

1. Open `/portfolios`, select **Portfolios**, and create **Customer Experience Portfolio**.
2. Description: **Customer-facing improvements with measurable service benefits.** Owner: **Asha Admin**. Save.
3. Select **Programs** and create **Customer Self-Service Program**.
4. Description: **Coordinates the portal and related customer self-service work.**
5. Portfolio: **Customer Experience Portfolio**. Owner: **Priya Manager**. Save.

### 6.7 Give the Project Manager permission to create a project

1. Return to `/organization` and open **Project & portfolio access**.
2. Create a grant with Name **Priya — customer portfolio manage**.
3. Member: **Priya Manager**.
4. Portfolio: **Customer Experience Portfolio**.
5. Leave Project blank. This is a portfolio grant.
6. Access: **manage**.
7. Save.

Priya needs portfolio manage access to create a project there. Selecting Priya as an owner, inviting them as a Project Manager, or placing them on a team is not sufficient by itself. When an eligible Project Manager creates a project, the application creates a project-creator manage grant for that project. Editing existing projects still depends on project access.

Give Vera an initial portfolio-read grant:

1. Create another grant named **Vera — customer portfolio read**.
2. Member: **Vera Viewer**. Portfolio: **Customer Experience Portfolio**. Project: blank.
3. Access: **read**. Save.

Portfolio read includes readable projects in that portfolio. It does not allow edits. Later, Section 14 uses a project-only grant to demonstrate revocation without a remaining portfolio grant.

### 6.8 Metric policy

1. Open **Metric policy** in Organization setup.
2. Create **Northstar training metric policy**.
3. Description: **Training thresholds for deterministic risk indicators.**
4. Amber risk threshold: **30**. Red risk threshold: **60**. Source stale after days: **7**.
5. Save.

These are training thresholds, not an industry certification or an AI forecast.

## 7. Admin: establish resource planning and its permissions

Login members and resource profiles are different. A login grants access; a resource describes capacity and staffing. Linking a login to a resource does not automatically grant resource-management or private-effort access.

1. Open **Resource planning** (`/resources`).
2. Use the visible **Working calendars** button (or choose it under **Planning records**) and create **India weekday calendar — v1**.
3. Description: **Training calendar: eight hours per weekday.**
4. IANA timezone: **Asia/Kolkata**.
5. Monday through Friday hours: **8** each. Saturday and Sunday: **0** each.
6. Holiday dates: leave blank for this fictional exercise. Use actual holiday dates for real staffing.
7. Save. Calendars preserve their versions; create another version if the schedule changes.
8. Open **Resource profiles**, create **Priya delivery capacity**, and select **Priya Manager** as Login member (optional). Description: **Training resource linked to the project manager.** Save.
9. Select this resource in the page's resource selector when inspecting its summary and adding related records.
10. Open **Resource access** and create **Priya — own training resource management**.
11. Resource: **Priya delivery capacity**. Member: **Priya Manager**.
12. Check **May manage resource**. Leave **May access sensitive effort** unchecked initially. Save.
13. Open **Availability** and create **Priya — October availability**.
14. Resource: **Priya delivery capacity**. Start: **2026-10-12**. End date (excluded): **2026-11-07**. Calendar version: **India weekday calendar — v1**. Save.
15. Open **Resource teams** and create **Priya — portal staffing**. Choose Priya's resource, Portal Delivery Team, and the same start/end dates. Save.
16. Open **Skills** and create **Priya — delivery planning**. Resource: Priya's resource. Skill: **Project delivery planning**. Save.

The excluded end date means the period stops before that date: an end of 7 November includes 6 November. Follow each form's date label; not every delivery-date field uses this convention.

Optional effort exercise, after Section 8 creates the project:

1. First let Priya check that sensitive effort is unavailable without permission.
2. As Asha, edit Priya's resource access and check **May access sensitive effort**. Save.
3. Let Priya follow Section 9 to record effort.
4. Create another Resource access record named **Asha — training effort oversight**, select Priya's resource and Asha as Member, and check **May access sensitive effort**. Save. Admins also need this explicit permission for sensitive effort operations.
5. Only mark **Full resource timesheet is complete** when the entire resource's day has been accounted for, not just one project entry. The Admin performs the coverage-completeness exercise; it is not a consequence of a single effort entry.

## 8. Project Manager: create and set up the project

**Person:** Priya. Verify the organization and Project Manager role first.

### 8.1 Create the project

1. Open `/projects`.
2. Click **Create projects**.
3. Fill the following fields; leave other optional fields blank unless specified.

| Field | Training value |
| --- | --- |
| Name | Customer Onboarding Portal |
| Description | Deliver a self-service onboarding portal; success means an agreed release and evidence of lower manual follow-up. |
| Project priority | high |
| Industry | technology |
| Category | delivery |
| Methodology | agile |
| Size band | small |
| Portfolio | Customer Experience Portfolio |
| Program (optional) | Customer Self-Service Program |
| Department | Digital Delivery |
| Delivery team | Portal Delivery Team |
| Owner | Priya Manager |
| Status | active |
| Reported health | Green |
| Currency | INR |
| Expenditure ledger is complete | unchecked initially |
| Start date | 2026-10-12 |
| Planned finish | 2026-11-06 |
| Forecast finish | 2026-11-06 |
| Actual start / Actual finish | blank initially |

4. Click **Save record**.
5. Open the project by clicking its name.
6. Confirm Priya can use **Edit project** and create delivery records in its tabs.

If project creation is denied, Asha checks Priya's portfolio manage grant. If an Admin created the project instead, Asha must give Priya an explicit project edit/manage grant. Owner alone gives no extra permission.

### 8.2 Grant another member project access — Admin step

Switch to Asha's profile:

1. Open the saved project and its **Project & portfolio access** tab.
2. Create **Ravi — portal project read**.
3. Member: **Ravi Reviewer**. Project: **Customer Onboarding Portal**. Portfolio: blank. Access: **read**.
4. Save.
5. Vera already has portfolio read access from Section 6.7; no duplicate grant is needed.

Return to Priya. Ravi's assessment assignment is separate from this delivery-project grant.

### 8.3 Create a sprint

1. In the project workspace, open **Sprints**.
2. Create **Portal Sprint 1**.
3. Description: **Confirm requirements and prepare the first portal slice.**
4. Project: **Customer Onboarding Portal**. Team: **Portal Delivery Team**.
5. Start: **2026-10-12**. End: **2026-10-23**. Status: **planned**.
6. Save, then edit that sprint, change Status to **active**, and save.

Create a planned sprint first. Do not initially create it as active or closed. For an existing Admin-created project, Priya/Hement needs an explicit project edit/manage grant; portfolio manage alone does not permit its sprint writes. Project selection is supplied automatically when creating records inside that project's workspace.

### 8.4 Create work items

For each row below, open **Work items**, create a record, select the saved project, select **Portal Sprint 1**, set Owner to **Priya Manager**, and save. Use the Description shown.

| Name | Description | Type | Priority | Points | Initial status | Start | Due |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Confirm onboarding requirements | Capture required fields, validation and acceptance criteria. | story | high | 3 | ready | 2026-10-12 | 2026-10-14 |
| Build onboarding form | Implement the agreed portal form for the training release. | feature | high | 5 | backlog | 2026-10-15 | 2026-10-21 |
| Run acceptance checks | Validate form completion and agreed error handling. | task | normal | 2 | backlog | 2026-10-21 | 2026-10-23 |

Keep Blocked unchecked initially. Later set a work item to blocked only when you also record what is preventing it. Story points are team-specific and should not be compared as productivity rankings between teams.

### 8.5 Milestones

Open **Milestones** and create these two records for the project:

| Name | Description | Due date | Critical | Actual finish |
| --- | --- | --- | --- | --- |
| Requirements agreed | Training scope and acceptance criteria confirmed. | 2026-10-14 | checked | blank |
| Portal release | Agreed portal release ready for customers. | 2026-11-06 | checked | blank |

Save each record. Leave Actual finish blank until a training exercise intentionally records completion or real completion is known.

### 8.6 Budget and expenditure

1. Open **Budget lines** and create **Portal delivery budget**.
2. Description: **Training budget allocation.** Project: portal. Amount: **200000**. Currency: **INR**. Approved budget: checked. Save.
3. Open **Expenditure** and create **Portal design workshop**.
4. Description: **Fictional training expenditure.** Project: portal. Amount: **20000**. Currency: **INR**. Expenditure date: **2026-10-12**. Leave Reverse original expenditure blank. Save.
5. Inspect the project summary: approved budget should be INR 200,000 and recorded spend INR 20,000.

The ledger is initially partial. If this training entry represents the entire intended training ledger, edit the project and check **Expenditure ledger is complete**. For real data, reconcile all entries before making that claim. Where coverage is sufficient, 20,000 out of 200,000 is 10% budget usage. A recorded cost is not proof of a complete financial account.

Expenditure entries preserve history. If an entry is wrong, use a new reversal entry with the original selected and the appropriate negative amount; do not expect ordinary editing to replace the entry.

### 8.7 Risk and blocker

Create this in **Risk register**:

| Field | Value |
| --- | --- |
| Name | Customer validation rules may arrive late |
| Description | Late agreement on validation rules could delay the portal form. |
| Project / Owner | Portal / Priya Manager |
| Severity / Likelihood | 3 / 3 |
| Mitigation | Review validation rules with stakeholders before form development. |
| Status | open |
| Review date | 2026-10-16 |
| Resolution / acceptance reason | blank |

Create this in **Blockers**:

- Name: **Awaiting validation examples**.
- Description: **Training blocker: missing valid and invalid customer examples.**
- Project: portal. Related work item: **Build onboarding form**. Owner: Priya. Status: **open**.

If the form work is actually blocked in the exercise, edit the work item and check **Blocked** too. When the issue is solved, mark the blocker resolved and clear the work item's Blocked flag. A risk records uncertainty; a blocker records an existing impediment.

When changing the risk to accepted or closed, supply a meaningful resolution/acceptance reason. Example: **Validation examples agreed and documented in the training requirements note.**

### 8.8 Goal alignment and business benefit

1. Open **Goal alignment** in the project.
2. Create **Portal contribution to onboarding goal**.
3. Project: portal. Portfolio: blank. Strategic goal: **Reduce customer onboarding effort**.
4. Weight: **1**. Contribution: **0.8**. Save.
5. Open **Business benefits** and create **Onboarding administration hours saved**.
6. Description: **Fictional measured benefit for the training period.** Project: portal.
7. Unit: **hours saved**. Target: **100**. Realized: **20**.
8. Period start: **2026-10-12**. Period end (excluded): **2026-11-07**. Save.

Alignment weights for a scope must total 1. With a single goal, use weight 1. The contribution is a declared input, not independently measured impact. Blank realized benefit means unknown; enter zero only when you know it is zero. Do not combine unlike benefit units as one meaningful total.

### 8.9 Freeze the initial plan and provide a metric plan

1. Once sprint, work, milestones and budget are saved, open **Plan baselines**.
2. Create **Portal approved plan — v1** with description **Initial training schedule and budget before changes.** Select the project and save.
3. Open **Metric plans** and create **Portal measurement plan — v1**.
4. Project: portal. Frozen baseline: **Portal approved plan — v1**. Working calendar: **India weekday calendar — v1**.
5. Forecast final cost (project currency): **210000**. Description: **Manual training estimate of final delivery cost.** Save.

A baseline preserves the saved plan. Later edits do not rewrite it. The forecast cost is your manual estimate; it is not a model prediction. Missing plans/calendars/baselines can leave derived dashboard measures Unknown.

### 8.10 Report status

1. Open **Status updates** and create **Portal weekly update — 12 October**.
2. Description: **Requirements are being confirmed. Validation examples are outstanding. Mitigation owner: Priya; next review: 16 October.**
3. Project: portal. Reported health: **Amber**. Save.
4. Confirm the displayed reported health reflects the saved status update.

Status updates preserve history. Add the next update as a new record. Dashboard evidence health may disagree with reported health; inspect the supporting sources rather than forcing both values to match.

## 9. Project Manager: allocation, effort and delivery checks

### 9.1 Allocate the resource

As Priya:

1. Open `/resources` and select **Priya delivery capacity**.
2. Open **Allocations** and create **Priya — portal allocation**.
3. Resource: Priya's resource. Project: portal.
4. Start: **2026-10-12**. End date (excluded): **2026-11-07**.
5. Hours per scheduled day: **4**. Save.
6. Inspect the resource summary for the same period. With the training calendar, this represents four of eight weekday hours allocated to this project, before time off or other allocations.

Priya needs both resource-management permission and project edit/manage access. No resource calendar/availability means capacity may be Unknown. A project grant alone is insufficient for managing a resource.

### 9.2 Optional time off and effort

1. In **Approved time off**, create **Priya — training half day**: Priya's resource; start **2026-10-16**; excluded end **2026-10-17**; hours per scheduled day **4**. Save. This records already approved time off; it is not a request-and-approval workflow.
2. After Asha grants sensitive effort access, open **Actual effort**.
3. Create **Priya — portal work — 12 October**: resource Priya; project portal; Worked on **2026-10-12**; Total hours **4**; Included overtime hours **0**. Save.
4. As Asha, use **Timesheet coverage** for that resource/day only if the complete intended day has been recorded. Do not treat four project hours as a complete eight-hour resource day automatically.

Actual effort has separate privacy permission. Vera should not gain it through portfolio read access.

### 9.3 My work and notifications

1. As Priya, open Workspace and inspect **My work**.
2. Check that permitted owned work, owned open risks, and active named assessments appear as they are created.
3. Open the website's **Notifications** destination from navigation.
4. Check **Show in-app notifications**, if you want them enabled.
5. Open an eligible assignment/review notification and click **Mark read**.
6. Reload and confirm the read state remains.

This feed shows eligible receipts for 30 days while access exists. It is not email, Slack, or a timed reminder service. Assignment alone does not override missing scope access for delivery work.

### 9.4 Exercise the sprint lifecycle

Perform this in the fictional project, not against unfinished real work:

1. Edit **Confirm onboarding requirements** from ready to in_progress and then done, saving each meaningful transition.
2. Resolve the training blocker and clear Blocked on **Build onboarding form**.
3. Move the remaining work items through their supported status sequence to done.
4. Record Actual finish on a milestone only when the exercise intends to demonstrate completion.
5. Edit **Portal Sprint 1** from active to closed and save.
6. Open Command center, select Delivery, and select a period that includes the sprint end date.
7. Look for closed-sprint velocity. With all three point-bearing work items completed before closure, the saved point total is **10**.

Closed sprints are immutable. If reopening a completed work item is needed, enter a reason in **Change reason (required when reopening)**. Reopening a completed/cancelled project also produces a new preserved baseline. Do not expect a closed sprint to reopen.

## 10. Admin: create an assessment framework from scratch

**Person:** Asha. No existing framework or external document is required.

### 10.1 Open the framework builder

1. Open **Maturity assessments** (`/assessments`).
2. In **Framework library**, click **Create framework**.
3. Framework name: **Northstar Delivery Readiness**.
4. Description: **Training framework for governance, delivery planning and evidence discipline. Scores reflect answers and independent human review.**
5. Category: **delivery**.
6. Use the initial dimension as Governance. Add two more with **Add dimension**.

Use the following three dimensions. Dimension weights total 1.

| Dimension | Weight |
| --- | --- |
| Governance | 0.30 |
| Delivery planning | 0.40 |
| Evidence discipline | 0.30 |

For every question below, set **Question weight = 1** and check **Required answer**. Add a second question within each dimension using **Add question**.

### 10.2 Enter all six questions

| Dimension | Question name | Question prompt | Answer type |
| --- | --- | --- | --- |
| Governance | Named accountable owner | Does the portal have a named owner and agreed responsibility for scope decisions? | Yes / no |
| Governance | Governance practice | Select the level that best describes documented decisions and review practice. | Rubric level |
| Delivery planning | Baseline and milestones | Are an initial plan baseline and dated critical milestones recorded for the portal? | Yes / no |
| Delivery planning | Risk management practice | Select the level that best describes how delivery risks are recorded, owned and reviewed. | Rubric level |
| Evidence discipline | Traceable supporting evidence | Do the answers reference dated evidence and identify who owns it? | Yes / no |
| Evidence discipline | Evidence summary | Summarize the documents reviewed, the main gaps, and the next improvement action. | Text (not scored) |

For both rubric questions, use exactly these values and labels:

| Level value | Level label | Meaning for the respondent |
| --- | --- | --- |
| 0 | Not demonstrated | No usable evidence of the practice |
| 1 | Partially established | Practice exists but its records or repeatability are incomplete |
| 2 | Established and repeatable | Dated records show owners and a repeatable review process |

Selecting Rubric level initially adds levels 0 and 1. Change their labels, click **Add rubric level**, and set the added level value to **2** with its label above. Enter the meaning through the question prompt if desired; the builder exposes level values and labels, not a separate visible level-description editor.

The default new question has placeholder text. Replace every default name/prompt. Each dimension needs at least one scored question; Yes / no and Rubric level are scored, while Text is not. Rubrics need at least two distinct levels. Do not make an entire dimension text-only.

### 10.3 Save and publish

1. Check the dimension weights: 0.30 + 0.40 + 0.30 = **1.00**.
2. Check the six question names, prompts, types, weights, required flags, and rubric levels.
3. Click **Save framework draft**.
4. Confirm the framework card says **Draft — not published**.
5. Click **Publish version**.
6. Confirm **Published version 1**.

Published versions are preserved. **Edit draft** changes the editable definition; publishing again produces a new immutable version. Existing assessments keep their original version. An updated draft does not rewrite previous scores.

### 10.4 Optional delegated framework editing

1. As Asha, find the framework card's **Access** section.
2. Choose Priya in **Member** and click **Grant framework editing**.
3. As Priya, reload Assessments and verify **Edit draft** is available for that framework.
4. Verify Priya has no **Publish version** button.
5. For this exercise, leave the published version unchanged.

Only Admin creates/publishes through the current framework-library flow. An explicitly granted active Project Manager can edit that framework's draft. Viewer is not an eligible framework editor.

## 11. Admin: assign respondent and independent reviewer

1. On the published framework card, click **Assign assessment**.
2. Assessment name: **Digital Delivery — Portal Readiness — October 2026**.
3. Published version: **Version 1**.
4. Department: **Digital Delivery**.
5. Team: **Portal Delivery Team**.
6. Respondent: **Priya Manager**.
7. Independent reviewer: **Ravi Reviewer**.
8. Click **Create assignment**.
9. Confirm the assessment appears in the Assessments list.

Priya and Ravi must be active Admin or Project Manager members, and different people. A Viewer cannot be used for either assignment. The team must belong to the selected department. No due-date or recurring-assessment setup is required by this current assignment form.

If a person's name is missing, verify accepted invitation, Active membership, current organization, and search/pagination in the member selector.

## 12. Respondent: complete answers using supplied evidence documents

**Person:** Priya. These sample documents are fully supplied; paste them into the relevant **Evidence notes** fields. They describe a fictional training exercise, not independently verified business approvals.

### 12.1 Open the assignment and answer

1. Open Workspace → My work and select the assigned assessment, or open `/assessments`, find it, and click **Open [assessment name]**.
2. Confirm **Northstar Delivery Readiness, version 1** and the assessment name.
3. In **Answers and supporting evidence**, enter these answers.

| Question | Answer | Evidence to paste |
| --- | --- | --- |
| Named accountable owner | Yes | Document A below |
| Governance practice | 1 — Partially established | Document B below |
| Baseline and milestones | Yes | Document C below |
| Risk management practice | 2 — Established and repeatable | Document D below |
| Traceable supporting evidence | Yes | Document E below |
| Evidence summary | Text from Document F | Put the evidence-reference line from Document F in its Evidence notes too |

The Yes answers and rubric values assume you performed the relevant fictional setup steps. For real assessments, answer from the actual evidence, including No or a lower level when a practice is missing.

### Document A — Training project charter

Suggested document name: `portal-project-charter.txt`. Paste this into Evidence notes for Named accountable owner:

> TRAINING DOCUMENT — Portal project charter  
> Organization: Northstar Website Training  
> Project: Customer Onboarding Portal  
> Record date: 10 October 2026  
> Sponsor and organization administrator: Asha Admin  
> Accountable delivery owner: Priya Manager  
> Objective: deliver a customer self-service onboarding portal and reduce manual follow-up.  
> In scope: onboarding form, validation rules, acceptance checks and initial release.  
> Out of scope for this training release: payments, AI scoring and integrations with live external providers.  
> Planned delivery period: 12 October–6 November 2026.  
> Training budget: INR 200,000.  
> Scope decisions: Priya prepares the impact and Asha records the training decision.  
> Acceptance: required fields and error handling are agreed, checks are recorded, and the portal release milestone is completed.  
> Approval status: fictional training charter; no real customer approval is claimed.

### Document B — Governance review and decision note

Suggested name: `portal-governance-review.txt`. Paste into Governance practice evidence:

> TRAINING DOCUMENT — Governance review note  
> Organization: Northstar Website Training  
> Project: Customer Onboarding Portal  
> Record date: 10 October 2026  
> Participants: Asha Admin, Priya Manager and Ravi Reviewer.  
> Decision: Priya owns delivery planning; Asha owns organization access and framework publication; Ravi independently reviews assessment evidence.  
> Decision: requirements and critical milestone dates must be recorded before the plan baseline is frozen.  
> Open action: Priya gathers valid/invalid customer examples before the form work proceeds.  
> Current gap: the exercise has an initial decision record but no history showing repeated governance meetings.  
> Assessment implication: choose Partially established rather than claiming repeatable governance.  
> Next improvement: maintain dated decisions and verify follow-through at the next review.  
> These are fictional training decisions, not legally binding approvals.

### Document C — Delivery plan and requirements/acceptance note

Suggested name: `portal-delivery-plan-and-requirements.txt`. Paste into Baseline and milestones evidence:

> TRAINING DOCUMENT — Portal delivery plan and requirements  
> Owner: Priya Manager. Record date: 10 October 2026.  
> Portfolio: Customer Experience Portfolio. Program: Customer Self-Service Program.  
> Planned project start: 12 October 2026. Planned release: 6 November 2026.  
> Milestone 1: Requirements agreed, due 14 October 2026, critical.  
> Milestone 2: Portal release, due 6 November 2026, critical.  
> Sprint 1: 12–23 October 2026; requirements 3 points, form 5 points, checks 2 points.  
> Baseline reference: Portal approved plan — v1, saved in the website after work, milestones and budget were entered.  
> Training approved budget: INR 200,000. Initial recorded expenditure: INR 20,000.  
> Requirement 1: a customer can complete the agreed onboarding fields.  
> Requirement 2: invalid entries show clear validation errors.  
> Requirement 3: agreed acceptance checks are recorded before release.  
> Acceptance check: valid input completes the flow; invalid input displays the agreed message; unresolved critical issues are reviewed before release.  
> This note defines the training plan; it does not claim software has already passed acceptance.

### Document D — Risk log and review procedure

Suggested name: `portal-risk-log.txt`. Paste into Risk management practice evidence:

> TRAINING DOCUMENT — Portal risk log  
> Owner: Priya Manager. Record date: 10 October 2026.  
> Risk: customer validation rules may arrive late.  
> Impact: form development and acceptance checks may slip.  
> Severity: 3 of 5. Likelihood: 3 of 5.  
> Mitigation: review validation rules and examples before form development.  
> Review date: 16 October 2026.  
> Related blocker: Awaiting validation examples, attached to Build onboarding form.  
> Repeatable procedure for this fictional exercise: Priya reviews each open risk on its review date, updates its status and mitigation, records a resolution/acceptance reason, and clears related blockers only when their cause is removed.  
> Evidence references: Risk register and Blockers in the portal workspace; dated status update and mitigation owner.  
> Training assessment answer: Established and repeatable, based on this supplied fictional procedure. For a real organization, repeated dated review records would be needed to substantiate that answer.

### Document E — Evidence register and source ownership

Suggested name: `portal-evidence-register.txt`. Paste into Traceable supporting evidence notes:

> TRAINING DOCUMENT — Portal evidence register  
> Record date: 10 October 2026. Evidence owner: Priya Manager.  
> A: Project charter — names accountable owner and scope; owner Priya.  
> B: Governance review note — initial decisions and repeatability gap; owner Asha.  
> C: Delivery plan and requirements — milestones, saved baseline and acceptance criteria; owner Priya.  
> D: Risk log — severity, likelihood, owner, mitigation and review procedure; owner Priya.  
> E: This register — links each answer to a dated named training source.  
> F: Assessment summary — consolidates strengths, limitations and follow-up.  
> Reviewer: Ravi Reviewer. Respondent: Priya Manager. They are different members.  
> All evidence is fictional, dated training text. Evidence coverage indicates the presence of notes/attachments, not independent proof that every assertion is true.

### Document F — Assessment summary and improvement action

Paste this into the Evidence summary **answer**:

> The portal training setup has a named owner, a saved baseline, dated critical milestones and recorded risk ownership. Governance is only partially established because the supplied note does not demonstrate a repeated meeting history. The risk-management answer follows the supplied fictional procedure; a real assessment would require repeated review records. The next improvement is to record two dated governance reviews with decision owners and completed follow-up actions. Priya owns the improvement; Asha will check progress at the next review. No AI evaluation or external certification is claimed.

Paste this into the question's **Evidence notes**:

> Training summary, dated 10 October 2026, prepared by Priya Manager. Sources: Documents A–E pasted into the preceding questions and the portal records created in this exercise. Independent review assigned to Ravi Reviewer.

### 12.2 Save and submit

1. After each answer or note, wait for **Draft saved.** The website attempts autosave after a brief pause.
2. If there are still unsaved changes, use **Save answers** when available.
3. Check every required answer and evidence note. Do not navigate away while the page says Unsaved changes.
4. Inspect the provisional scores and answer/evidence coverage.
5. Enter this **Review or submission note**: **Training answers and Documents A–F are ready for independent review. Please check the governance gap and the evidence supporting the risk-management level.**
6. Click **Submit for review**.
7. Confirm status becomes **submitted**. Scores remain provisional until independent review completes.

With the supplied answers and no reviewer adjustments: Governance is 75, Delivery planning is 100, Evidence discipline is 100, and overall is **92.50 / 100**. Text is not numerically scored. This is a calculation exercise, not a maturity certification. If an answer is missing or different, do not force this number; inspect the recorded answers and coverage.

### 12.3 Optional website file-upload exercise

The main journey uses pasted notes and needs no files. If you want to test an existing file upload:

1. Use a UTF-8 plain-text `.txt` file, no larger than **512 KiB**. PDF, Word, Excel and scanned documents are not supported evidence uploads here.
2. Save pending answers first; upload controls are disabled while answers are dirty.
3. Use the question's evidence file chooser and select the file.
4. Confirm its name appears with **quarantined** status.
5. Submit the assessment after all answers and uploads are saved.

Creating a local file is outside the website, so it is deliberately optional. Uploading a supported existing file uses the website. A reviewer must preview and release every quarantined attachment before completion. Pasted evidence notes do not use that file-release step.

## 13. Independent reviewer: review, return, and complete

**Person:** Ravi. This is an assessment assignment performed under Project Manager membership.

1. In Ravi's profile, open Workspace → My work or Assessments.
2. Open **Digital Delivery — Portal Readiness — October 2026**.
3. Confirm status **submitted** and that Ravi can review.
4. Enter **Review or submission note:** **Starting independent review of the fictional training evidence. I will verify answer consistency and distinguish documented practice from claims.**
5. Click **Start review**. Confirm **in review**.
6. Read each answer and its evidence notes. Compare the baseline/milestones/risk statements with the delivery records Ravi has permission to inspect.
7. If there are uploaded attachments, click **Preview [filename]**, read the text, enter a meaningful review note, then click **Release [filename]** for each acceptable file.
8. If corrections are necessary, enter a specific note and click **Return for changes**. Example: **Please replace the risk-management claim with repeated review records or lower the level to match the evidence.**
9. As Priya, reload, confirm **returned**, update the answers/notes, wait for Draft saved, and **Submit for review** again.
10. As Ravi, reload the resubmission and start review again where applicable.
11. If adjusting a scored answer, use **Adjusted score for [question]** and **Adjustment reason for [question]**. The score is **0–100**, not the rubric's 0–2 level. Do not adjust a text answer numerically.
12. For the basic exercise, leave adjustments blank and accept the supplied fictional values.
13. Enter a completion note: **Reviewed the training answers and supplied evidence. Governance remains partially established. The risk procedure is accepted for this fictional exercise; repeated real records remain necessary for a real readiness claim. Improvement action owner: Priya.**
14. Click **Complete review**.
15. Confirm **completed**, approved score, and the preserved framework version.

All required answers must be valid for completion. Unreleased quarantined attachments block completion. The respondent cannot review their own submission. Admin status does not allow an unassigned person to replace the assigned independent reviewer for this action.

If you deliberately enter an adjustment of 80 for Risk management practice, its dimension becomes 90 and the overall becomes **88.50**, with other sample answers unchanged. Record a reason such as **Training adjustment: evidence describes the procedure but does not show repeated review history.** This tests the reviewer-adjustment path; it is optional.

Completed assessments preserve their history. For a later cycle, create another assessment against the appropriate published version rather than rewriting a completed result.

## 14. Admin: share completed results and check effective access

### 14.1 Share the result with Vera

1. As Asha, open the completed assessment.
2. In its **Access** section, select **Vera Viewer** as Member.
3. Click **Grant result access**.
4. In Vera's profile, reload Assessments and open the completed result.

**Expected result:** Vera can read the shared completed scores and coverage. This grant does not share private answers, evidence notes, uploaded files, or assessment history. A project/portfolio-read grant by itself does not share an assessment result. A framework-editor grant also does not make someone an assessment respondent or reviewer.

### 14.2 Project-read revocation exercise

Use the fictional Viewer account:

1. As Asha, open Organization setup → Project & portfolio access.
2. Edit **Vera — customer portfolio read**, check **Archived**, and save. This removes the broad portfolio path.
3. Open the portal's Project & portfolio access section and create **Vera — portal project read**: Vera, portal project, portfolio blank, Access read.
4. As Vera, reload Projects and open the portal. Confirm read access.
5. As Asha, edit **Vera — portal project read**, check Archived, and save.
6. As Vera, reload the open portal, try a new search for its name, and refresh Command center.
7. Confirm that the project is denied/absent through those delivery paths.
8. As Asha, restore the intended project grant by editing its archived record and clearing Archived, then saving. Use the archive filter to find it.

Revocation only removes the selected grant. If another project or portfolio grant still allows access, the member can remain authorized. Do not declare revocation broken without checking the other grants.

Separately click **Revoke access** on Vera's assessment result grant and check that it disappears after Vera reloads. Regrant it afterward for the Viewer exercise. Removing delivery-project access does not automatically remove a separately granted assessment result.

## 15. Viewer: inspect the website and prepare a reading checklist

**Person:** Vera, role Viewer. Confirm the role on Account and access.

### 15.1 Read project delivery information

1. Open Projects, search **Customer Onboarding Portal**, and open it.
2. Read Project overview, reported health, approved budget and recorded expenditure.
3. Open Work items, Milestones, Risk register, Blockers and Status updates.
4. Check that permitted records are readable.
5. Confirm there is no usable **Edit project** or delivery **Create ...** action for Vera.
6. Open Account and access and confirm Vera can manage their personal account but cannot invite/change organization members as Admin.

### 15.2 Read Command center

1. Open `/command-center`.
2. Set From date **2026-10-12** and To date (excluded) **2026-11-07**.
3. Select **Customer Experience Portfolio** if available under the current grants; otherwise use **All authorized portfolios** for project-only access.
4. Click **Refresh** after changing filters where needed.
5. Select **Executive**. Read reported versus evidence health, financial measures and strategic alignment.
6. Select **Delivery**. Read milestone/timeline information and closed-sprint velocity after the training sprint is closed.
7. Select **Risk**. Inspect the risk register, mitigation and source coverage. Automated escalation/approval workflows are not implemented here.
8. Select **Resource**. Read permitted capacity/allocation information. Do not expect access to private actual effort through a delivery read grant.
9. Open a metric's evidence/source drawer where available. Read source dates, calculation explanation and coverage before interpreting the number.
10. Save a personal view named **Vera — portal oversight** using **New view name** and **Save view**. Reload and select the saved view. Saved filters do not grant access.

Unknown means the available inputs do not support a measure; it is not automatically zero or a healthy condition. Dashboard periods are limited to 1–366 days, and the current snapshot has record-count bounds. The training dataset is small enough for this exercise; the dashboard should not be treated as an unbounded historical analysis.

The available **Export metric DTO** is a structured data export, not a polished PDF/Word executive report. Automated weekly reports, email risk alerts and AI failure forecasts are future features.

### 15.3 Read the assessment result

1. Open Assessments and find the shared completed assessment.
2. Open it and confirm the framework version, completed status, overall score and dimension scores.
3. Read answer weight coverage and evidence coverage.
4. Confirm private answer/evidence controls and respondent/reviewer actions are unavailable.
5. Inspect **Department comparison** using dates that include the assessment's creation date. The comparison uses completed permitted results from exactly that published framework version and creation dates in UTC, not the project's scheduled dates.

One assessment is not a benchmark across departments. To exercise comparison, Asha can create a second department/team, assign another assessment against Version 1 with different eligible participants, complete its review, and share that completed result with Vera. An unscored department should remain unscored.

### 15.4 What documents does a Viewer submit?

**In the current website: none through a Viewer submission flow.** Viewer membership is for reading permitted information. Document library permits scoped Viewer reads, with uploads/changes restricted to authorized Admin/PM. Viewer has no document-upload or assessment-submit action.

Typical business material and the supported handling are:

| Business material | Supplied example in this manual | Current website handling |
| --- | --- | --- |
| Project charter | Document A | Assigned Admin/PM pastes it into question evidence notes |
| Governance decisions/meeting note | Document B | Assigned Admin/PM supplies it as evidence; no general meeting-minutes ingestion |
| Requirements and acceptance criteria | Document C | PM records work/milestones and respondent pastes relevant evidence |
| Risk log | Document D | PM creates structured risks and provides assessment evidence |
| Evidence register | Document E | Respondent adds evidence notes to the relevant questions |
| Assessment summary/improvement action | Document F | Assigned respondent submits; assigned independent reviewer reviews |
| PDF/Word/Excel/scanned source documents | Separate Document library for authorized Admin/PM, with scoped Viewer reads | Assessment attachment upload remains TXT; [library steps](../03-sprints/completed/sprint-09/USER_GUIDE.md) explain same-byte released evidence links |

If Vera must personally submit assessment evidence, Asha would need to change Vera to Project Manager and assign Vera as respondent in a new suitable assessment, with a different eligible reviewer. That changes the person's capabilities and is a separate workflow; it does not demonstrate Viewer submission. Do not upgrade real members merely to bypass an intended read-only policy.

Vera can use this reading checklist for their own review. There is no website submission form for this checklist:

- Do the milestone dates support the reported status?
- Does recorded spend have a complete ledger or only partial coverage?
- Are open risks owned, mitigated and reviewed on time?
- Is capacity known, and are private effort details correctly restricted?
- Which framework version produced the completed score?
- Does evidence coverage indicate presence of notes while leaving evidence quality to human review?
- Are gaps and improvement owners clear?

## 16. Feature and role testing worksheet

For each check, record **Pass**, **Fail**, or **Blocked** in your own test notes. A website error contradicting the expected result is Fail. Missing delivery or a missing prerequisite is Blocked, not proof the feature is broken. The website has no general test-result submission screen.

| No. | Person | Website check | Expected result |
| --- | --- | --- | --- |
| 1 | Asha | Signup request | Generic verification-request message; not yet a finished account |
| 2 | Asha | Open valid verification link and activate | New organization and Admin membership after verification |
| 3 | Asha | Save timezone/currency | Delivery setup becomes available |
| 4 | Asha | Invite Priya/Ravi/Vera | Correct roles, pending invitations, accepted Active memberships |
| 5 | All | Inspect Account and access | Correct person, organization and role in each separate session |
| 6 | Asha | Resend/cancel an extra invitation | Replaced/cancelled old links cannot be used |
| 7 | Priya | Create project with portfolio manage | Project saves and creator can manage it |
| 8 | Priya | Edit project and create work/milestones | Allowed with effective project permission |
| 9 | Ravi | Read project under read grant | Read allowed, delivery editing denied |
| 10 | Vera | Read permitted portal | Read allowed, delivery editing denied |
| 11 | Asha | Save calendar/resource/availability | Saved resource context and capacity inputs |
| 12 | Priya | Allocate granted resource to granted project | Allocation allowed; summary reflects saved inputs |
| 13 | Priya | Inspect effort before/after effort grant | Separate sensitive permission changes availability |
| 14 | Vera | Inspect private effort | No access via portfolio/project read grant |
| 15 | Priya | Save risk/blocker/status | Structured records persist; status/blocked flags match intended exercise |
| 16 | Priya | Save plan baseline and edit later plan | Original baseline remains preserved |
| 17 | Priya | Close the training sprint | Closed record preserved; velocity reflects completed point-bearing work |
| 18 | Asha | Create/publish framework | Valid weights/questions; immutable Version 1 |
| 19 | Priya | Edit explicitly granted framework draft | Edit allowed; publication remains Admin-only |
| 20 | Asha | Assign Priya and Ravi | Different active eligible members accepted |
| 21 | Asha | Try Vera as an assessment participant | Viewer assignment rejected |
| 22 | Priya | Answer, autosave and submit | Draft saved; submitted provisional result |
| 23 | Ravi | Start/return review | Review/returned statuses and specific notes persist |
| 24 | Priya | Revise returned assessment and resubmit | Updated saved answers submitted for another review |
| 25 | Ravi | Complete independent review | Completed preserved result; adjustments require reasons |
| 26 | Ravi | Optional preview/release attachment | Quarantined text released before completion |
| 27 | Asha/Vera | Share completed result | Scores readable; private evidence remains restricted |
| 28 | Vera | Try answering/submitting assessment | No permitted respondent submission path |
| 29 | All | Search using top search or Ctrl K → Find a record | Only permitted projects/work/risks/assessments returned |
| 30 | Priya/Ravi | My work and Notifications | Eligible assigned records/receipts and persistent read state |
| 31 | Vera | Save personal dashboard view | Filters persist; permissions do not expand |
| 32 | Asha/Vera | Revoke only read path and reload | Project denied/absent; restore grant to continue |
| 33 | Asha/Vera | Revoke result grant and reload | Result removed independently of delivery grants |
| 34 | Priya/Vera | Save milestone change while Vera has Command center open | Authorized saved-change freshness notice and refetched snapshot |

For the live-refresh check, keep Vera's Command center open in its own profile, then have Priya save a milestone change in the fictional project. The notice signals saved changes; inspect the refreshed authorized data. It is not AI streaming.

## 17. Website-only troubleshooting

| What you see | What to check/do in the browser |
| --- | --- |
| Signup response but no email | Check the intended inbox and Spam. In local test mode no inbox email is sent and there is no public website mailbox. Ask the operator for intended private delivery. Mark verification Blocked if unavailable. |
| Invitation provider-accepted but absent | Recipient checks Inbox, Spam and address spelling. Operator checks provider delivery/authentication. Acceptance is not proof of receipt. |
| Invitation sending failed | Ask the operator to correct mail configuration, then use Resend and open only the latest message. |
| Invitation link invalid/expired | Admin uses Resend; recipient opens the latest link. Cancelled/replaced links are unusable. |
| Member is not in a selector | Confirm invitation accepted, Active membership, correct organization, eligible role, and selector search/paging. |
| Setup required message | Admin saves Organization configuration with timezone and currency. |
| PM cannot create project | Admin checks portfolio manage grant; owner/team membership alone is insufficient. |
| PM cannot edit an existing project | Admin checks explicit project edit/manage grant and that the project is not archived. |
| Resource capacity Unknown | Select correct resource/period and check saved calendar plus availability; missing inputs are not zero capacity. |
| PM cannot allocate or record effort | Check resource management, project edit and separate sensitive effort access as applicable. |
| Framework cannot publish | Check dimension weights total 1, scored question per dimension, valid distinct rubric levels and required fields. |
| Assessment cannot be assigned | Publish first; use different active Admin/PM participants and matching department/team. |
| Submit disabled | Wait for Draft saved; finish required answers; resolve any saving error. |
| Reviewer actions missing | Check correct person, role, assignment and submitted/in-review status; respondent cannot review themself. |
| Complete review fails | Inspect required answers, review note, adjustment reasons and unreleased quarantined attachments. |
| Viewer sees no assessments | Admin shares a completed result; delivery grants do not share assessments. |
| Result visible but no evidence | Expected for a completed-result reader; it is not an evidence grant. |
| Search/list seems incomplete | Clear filters, check archive settings and use pagination. |
| Access remains after one revoke | Check remaining project/portfolio grants; then reload the affected member's screen. |
| Dashboard value Unknown | Read coverage/source explanation, verify required inputs and period. Do not substitute a guessed value. |
| Password forgotten | Use `/account/reset`, request message, open latest recovery link, and set a new password. Delivery is the same prerequisite; reset link expires after 30 minutes and password change revokes existing sessions. |

## 18. Completion checklist by responsibility

**Admin finishes:** verified organization; active invited members; timezone/currency; departments/team/membership; goal/portfolio/program; portfolio/project/resource grants; calendar/resource/availability; valid published framework; distinct respondent/reviewer assignment; completed-result sharing; access checks.

**Project Manager finishes:** project and metadata; planned-to-active sprint; assigned work; dated milestones; budget/expenditure; risk/blocker; alignment and benefit; baseline/metric plan; status updates; permitted allocation and effort; saved assessment answers/evidence; submission and returned corrections.

**Independent reviewer finishes:** reads evidence, checks consistency, previews/releases any files, returns issues or records justified adjustments, and completes the assessment with a review note.

**Viewer finishes:** verifies read-only delivery access, reads dashboards with coverage/source explanations, reads shared completed scores, checks evidence privacy, and records their own oversight observations. Viewer has no general document-submission step in this version.

Keep this fictional organization separate from real business records. When the exercise is finished, use the website's archive controls where allowed and revoke unneeded test-member access. Records with active dependents may resist archiving; do not expect a one-click organization reset or permanent deletion flow.

## Maintenance references

These references explain the implemented scope; you do not need to read them to follow the exercise:

- [Current user guide](USER_GUIDE.md)
- [Sprint 8.1 tester guide](../03-sprints/active/sprint-8.1/SPRINT_8_1_USER_GUIDE.md)
- [Current capability and acceptance limits](../00-overview/CURRENT_STATUS.md)
- [Feature catalogue](../00-overview/FEATURE_CATALOGUE.md)

Screen labels, role restrictions, sample field options, framework construction, assessment scoring/review, and evidence limits were checked against the current website components and server permission rules. Screens on a different running version may vary; compare the actual label and permission response before recording a test result.


## Account repair and execution follow-up — 10 October 2026

The complete original 1–18 flow above is preserved. [Current execution evidence and every-action checklist](../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) distinguish browser checks, API regressions, optional branches and external limitations. The original Gmail acceptance evidence above remains historical; the new repeatable browser journey uses a separate local-mail test environment.

Sign-in and account-completion password inputs start masked; use **Show password**/**Hide password** without losing the value. Removing Active from a membership immediately denies that organization's operations while the verified, globally active account can still sign in and manage its own profile/sessions. With no memberships, the website explains the missing organization access; an Admin invitation is needed to join an existing organization. Choosing an accessible organization rechecks its own role. Global disabling is a separate operator operation.

Operators can prepare the four fictional accounts and planning inputs using [guarded training provisioning](../05-demos/WALKTHROUGH_DATA.md). The prepared seed already contains setup and a draft assessment; use a fresh website signup to practice setup from the beginning. No shared password is published here. Keep the prepared organization separate from the user's existing invitation-test organization.

## 18. Reuse project documents in the separate library

For the same permitted fictional project, follow [Sprint 09 user steps](../03-sprints/completed/sprint-09/USER_GUIDE.md)
and [document demo](../05-demos/sprint-based/sprint-09/README.md). Admin/PM upload,
inspect job status, preview pages/paragraphs/sheets, search keywords, open source locations
and append versions. Viewer reads only granted sources and shared organization policies.
The TXT-only assessment upload in Section 12 remains a separate private release workflow.
Linking identical released bytes does not alter answers, coverage or saved scores.
Do not upload private workforce notes or purge real evidence for a walkthrough.
## AI evidence preview — Sprint 10

Open AI operations & evidence as Admin to retrieve a permitted project source
preview, inspect no-key diagnostics and manage a zero-spend tenant budget. Follow
[the current steps](../03-sprints/active/sprint-10/USER_GUIDE.md). Keyword excerpts are labeled source_fallback; no match
stays unavailable. Index embeddings and real model answers remain disabled until
explicit provider/model/spend authorization. PM/Viewer use the document library;
restricted Admin diagnostics are inaccessible. No semantic agents or plan edits.
