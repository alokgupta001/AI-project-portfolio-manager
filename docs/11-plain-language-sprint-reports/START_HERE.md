# Getting access and checking features

Use this once before following an individual sprint report.

## 1. Open the application

Open [the local website](http://localhost:3000). Sign in with your own activated account and choose the intended organization at the top of the page. Use the configured website address consistently; switching between `localhost` and `127.0.0.1` can interrupt account flows.

If the website is unavailable, the person operating the local installation can start it from the `enterprise-ppm` project folder in PowerShell:

```powershell
docker compose up -d --build --wait
```

For document uploads and the document-based AI examples, use the scanner-enabled startup instead:

```powershell
docker compose -f compose.yaml -f compose.documents.yaml up -d --build
```

The scanner may need time to download its initial signatures. There is no need to create a new database or replace the existing configuration for these reports. Fresh installation instructions are in [local setup](../07-setup-and-deployment/LOCAL-DEVELOPMENT.md).

## 2. Check your role and permissions

Open **Account & access** to confirm your name, organization and role.

| Role | What it generally allows | What may still need separate permission |
| --- | --- | --- |
| Admin | Organization setup, member administration and module administration | Private actual-effort data still requires an explicit grant. Private assessment evidence follows assignment/access rules. |
| Project Manager (PM) | Editing permitted project work and taking assigned assessment roles | Project/portfolio edit or manage access, resource management, private effort, and assessment assignment are distinct permissions. |
| Viewer | Reading permitted projects and shared completed assessment results | Project access does not automatically share assessment results, evidence or private effort. |

A role alone does not make every record visible. Being named a project owner or a resource does not automatically grant access. If a list is empty, confirm the organization and grants before treating it as a defect.

## 3. Prepare a small practice area

Use fictional records in a separate practice organization or an approved test project. For most checks, an Admin should have:

1. Saved organization timezone and currency under **Organization setup → Organization configuration**.
2. Created a portfolio and a practice project, such as **Sprint report practice**.
3. Given the PM appropriate portfolio/project access and the Viewer read access.
4. Invited a second eligible Admin/PM if assessment review will be checked. Respondent and reviewer must be different people.

Use separate browser profiles for different people so you can see whose permissions apply. No universal password is supplied. For prepared fictional training records, see [training data instructions](../05-demos/WALKTHROUGH_DATA.md); for a complete browser-only exercise, see [the website walkthrough](../06-user-guides/WEBSITE_WALKTHROUGH.md).

## 4. Understand the result

| What you see | What it means or what to check |
| --- | --- |
| Unknown | A required input is missing or cannot support a number. It does not mean zero. |
| Partial | Some inputs or processing results are available, but the result is incomplete. |
| Forbidden or missing edit controls | Check the person's role, grants, assignment and the record's state. |
| Conflict or changed-record message | Someone changed the record. Reload it before deciding what to save. |
| Empty list | Check search, dates, archive settings, pagination and permissions. |
| End date marked “excluded” | That date is not counted. For Monday through Friday, use the following Saturday as the excluded end date. |
| Quarantined document | The file is stored but has not passed the required processing checks. It is not ready evidence. |
| Source fallback | The application is showing source text because an AI-generated answer is unavailable. |

Account links require working delivery. On some installations they go to a private local test mailbox; on configured development installations they can go to email. If a signup, invitation or reset link never arrives, ask the operator to check delivery. A generic request-success message does not mean an account has already been activated.

## 5. Keep a simple check record

Copy this row into your own notes for each feature:

| Sprint / feature | Person and role | Record checked | Expected result | Actual result | Pass / Fail / Blocked |
| --- | --- | --- | --- | --- | --- |
| Example: 04 / project save | Practice PM | Sprint report practice | Saved name remains after reload | Fill in after checking | Fill in after checking |

Use **Blocked** when a prerequisite such as account delivery, a grant or a running scanner is missing. Use **Fail** when the feature has its prerequisites but behaves differently from the stated result. Avoid deleting or purging real evidence during a check; use disposable practice records for archive, cancellation and retention exercises.

[Back to the report index](README.md)
