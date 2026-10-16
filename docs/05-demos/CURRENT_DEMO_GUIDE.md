# Current demo guide

**CURRENT DEMO**, source-reviewed against the local pilot and retained browser checks. Development Gmail signup, existing-account Viewer invitation and recovery were completed on 10 October; broader business scenarios were not all rerun. Use fictional data and separate browser profiles. Live Jira/GitHub and production demonstration retain their external gates. [Sprint 04 sample setup](sprint-based/sprint-04/DEMO-DEVELOPMENT.md) is the canonical guarded seed guide; the operator follows [local setup](../07-setup-and-deployment/LOCAL-DEVELOPMENT.md) and [Gmail SMTP setup](../07-setup-and-deployment/GMAIL-SMTP-SETUP.md). Ordinary members follow the website/email path; no default password exists.

| Scenario | Exact page/actions | Expected result | Recovery / limitation |
| --- | --- | --- | --- |
| Signup and onboarding | Open `/signup`; request message; check Inbox/Spam; privately open verification link; complete and sign in; follow Getting started | Saved organization/first Admin; checklist reflects stored records | Development Gmail verified; expired/replaced links fail; explicit local-preview instances still need operator help |
| PM delivery | Admin invites/promotes PM and grants portfolio manage; PM opens `/projects`, creates in that portfolio, opens `/projects/<project-id>`, adds permitted milestone/work/risk and reloads | Records persist and belong to that project; optional classification may be Unknown | PM role alone is insufficient; follow [member/access steps](../06-user-guides/MEMBERS_ROLES_AND_ACCESS.md); re-read revision on conflict |
| Project detail and discovery | Ctrl K → Find a record; query permitted project/work/risk; choose result; page to older records | Project detail opens; child deep link filters target | Wrong scope/revocation hides results; no semantic document retrieval |
| Assessment | `/assessments`: create/publish allowed framework, assign separate respondent/reviewer; respondent answers/submits; reviewer reviews/completes | Deterministic score, coverage and immutable completed history; published version retained | Required answer, self-review and missing scope block transition; evidence is UTF-8 text/manual release |
| Executive overview | `/command-center`: choose available view/scope/date; open source/evidence drawer; compare project facts | Deterministic measures and explicit missing/stale inputs; currency remains separate | Missing inputs stay Unknown; snapshot limits remain; no AI prediction |
| Resource planning | `/resources`: open permitted profile, schedule/leave/allocation; inspect capacity for period | Hours, overload and coverage reflect actual scope | Full workload/effort requires separate grants; missing calendar is not zero capacity |
| Pilot receipts and refresh | Workspace My work; Notifications; mark read; change preference. Keep Command center in second signed-in profile while saving permitted milestone in first | Persistent read/preferences and authorized saved-change refetch | Receipt needs qualifying assignment/review/import event; 30-day window; revoked target hidden |
| Imports | `/integrations`: use labeled supported fixture or CSV mapping; inspect progress/rejected rows | Durable persisted job outcome and errors | Fixture is not live-provider proof; retry only owning supported action |

## Safe reset and failure handling

Use the isolated demo project/database and documented deterministic seed; repeated seeding preserves subsequent edits and does not reset everything. Archive fictional records through authorized forms only after dependent checks. A fresh scenario can use another fictional organization. Do not reset/delete databases or use `down --volumes`. Stop the demo with its identical compose file arguments; preserve volumes. No cleanup/reset command was run by this audit.

Record expected/actual result and Pass/Fail/Blocked when you actually execute. Do not reuse old screenshots as proof of a new run. [Future outlines](FUTURE_DEMO_PLANS.md) contain unavailable assistant/report experiences.

## Current source-library demonstration

The [Sprint 09 demo](sprint-based/sprint-09/README.md) gives a concrete fictional
charter upload, Ready/preview/download, keyword citation, appended version, permitted
Viewer and denied tenant, private assessment reference and Admin policy/retention journey.
Run with the optional healthy scanner in the isolated environment. Its browser
acceptance and mobile screenshots are retained; future semantic results are not shown.
Existing assessment evidence remains a separate TXT/manual-release intake.
## AI evidence preview — Sprint 10

Open AI operations & evidence as Admin to retrieve a permitted project source
preview, inspect no-key diagnostics and manage a zero-spend tenant budget. Follow
[the current steps](../03-sprints/active/sprint-10/USER_GUIDE.md). Keyword excerpts are labeled source_fallback; no match
stays unavailable. Index embeddings and real model answers remain disabled until
explicit provider/model/spend authorization. PM/Viewer use the document library;
restricted Admin diagnostics are inaccessible. No semantic agents or plan edits.
