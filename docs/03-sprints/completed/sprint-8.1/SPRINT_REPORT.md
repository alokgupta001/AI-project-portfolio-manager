# Sprint 8.1 report

**Closeout — 16 October 2026: Sprints 8.1 and 10 are COMPLETED for their implemented development scope.** The reviewed application checkpoint `631c149` passed [hosted CI](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/38885041673), including regression, migration and browser checks. The current pilot Word guide is rendered and visually verified in the linked closeout evidence. Earlier blocked/active statements below describe their recorded checkpoints. Production deployment, broad real-model/agent quality and scale remain OPEN release/successor gates. Stop before 11. [Acceptance matrix](../../../10-reference/SPRINT-8.1-AND-10-CLOSEOUT.md).

## Historical record before closeout

**Current reconciliation — 16 October 2026:** Development Gmail signup, existing-account Viewer invitation and recovery were subsequently verified on 10 October; [mail evidence](../../../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) supersedes the missing-SMTP blocker for those journeys. Parent hosted CI/archived Word visual and production gates remain open. The original task counts/results below are the dated 9 October baseline, not today's complete feature status.

Execution date: 2026-10-09. **Implementation completed locally; parent acceptance remains OPEN.** No next sprint or live deployment was started. User authorization covered application, additive migration, tests and documentation. The revised planning pack is the execution authority; original specifications and frozen prompts remain unchanged.

10 October follow-up: the SMTP block described below records the original 9 October run. Real development Gmail signup, existing-account Viewer invitation acceptance and password recovery have since been verified in the [account email verification report](../../../04-testing/ACCOUNT_EMAIL_VERIFICATION.md). Use its current evidence and linked website/setup guides; unrelated parent acceptance gates remain open.

## Actual starting point

Branch main, base `90564405bcacc8389e34f3b06d8ab8d00984c5c1`, with substantial uncommitted Sprint 08 and learning work. The planning baseline was checked against code and a fresh isolated test run: 67 passed (one inherited Starlette/httpx warning). Normal services were stopped, and normal migration head was 0007. Existing project/resource grants, identity challenges, assessment grants, API pagination and job outbox were reused instead of rebuilt. Existing data was backed up privately before migration. No reset, clean, clone, normal database replacement or applied migration edit occurred.

## Task disposition

| Task | Status | Delivered behavior and acceptance evidence |
| --- | --- | --- |
| PPM-81-001 | COMPLETE locally | Verified registration and atomic first organization/Admin, replacement/concurrency/replay and generic responses. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-001.md). |
| PPM-81-002 | BLOCKED external acceptance | Durable delivery adapter, local preview, SMTP STARTTLS, retries, invitation list/resend/cancel and revoked inviter checks implemented. Real provider credentials/inbox verification absent. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-002.md). |
| PPM-81-003 | COMPLETE locally | Saved setup checklist, Admin organization profile with revision conflict, account/resource distinction and optional sample guidance. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-003.md). |
| PPM-81-004 | COMPLETE locally | Existing project/resource grants retained; framework/result grant controls and scope explanations added. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-004.md). |
| PPM-81-005 | COMPLETE locally | Four-type scoped escaped record search, permitted counts, older record deep links and retained page commands. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-005.md). |
| PPM-81-006 | COMPLETE locally | Server paging/search in assessment lists and selectors; full version/UTC-period cohort comparison. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-006.md). |
| PPM-81-007 | COMPLETE locally | My work, transactional deduplicated receipts, persistent read/preferences, target revalidation and 30-day presentation window. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-007.md). |
| PPM-81-008 | COMPLETE locally | Nullable controlled project/work metadata and industry filtering, preserving Unknown and existing CSV allowlist validation. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-008.md). |
| PPM-81-009 | COMPLETE locally | Authorized committed revision SSE and coalesced dashboard refetch, no record-content notices. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-009.md). |
| PPM-81-010 | PARTIAL | New tester guide and corrected generated DOCX content, system wording, completed backend/static/source/restore/preservation gates. Hosted CI UNVERIFIED; DOCX visual QA BLOCKED because the bundled Windows runtime has no LibreOffice executable. [Checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-010.md). |

## Verification and limitations

- Backend: initial Sprint 8.1 full run **74 passed**, one inherited warning, 152.13 seconds. Full migration lifecycle: upgrade, downgrade to 0006, upgrade, downgrade to base, upgrade, repeat upgrade and Alembic drift check passed in disposable ppm_test. The final full suite in `sprint81-backend-complete.txt` passed **74 tests**, one inherited warning, 138.24 seconds. The additional real-database SSE reconnect/duplicate-cursor/live-revocation test passed **1 test** in 6.40 seconds (`sprint81-stream.txt`). Two strengthened metadata/preference/cohort cases passed in 6.78 seconds (`sprint81-final-negatives.txt`); the legacy invitation transition case passed in 2.68 seconds on the final code (`sprint81-legacy-final.txt`; earlier pass retained in `sprint81-legacy.txt`).
- Static checks: Ruff, Python format, mypy (30 application/worker modules), generated contracts, TypeScript, ESLint, Prettier and seven preserved-source hashes all passed in `sprint81-static-results.json`. Final rerun after browser fixes passed all eight gates.
- Browser: isolated Compose project enterprise-ppm-identity-test, web/API 3001/8001, independent volumes and ppm_test. 125 project/resource/member/assessment fixtures; Admin/PM/Viewer and existing second-organization suite. Initial failed logs are retained, including selector/organization-header mistakes and the stale closed notification drawer fixed during verification. **12 passed** in 1.0 minute in `sprint81-browser-complete.txt`. After the final assessment stale-response/paging and organization-state fixes, **6 affected browser tests passed** in `sprint81-browser-closure.txt`. No failed run is claimed successful.
- Normal data: additive head **0008_pilot_completion**. All **59 established table row counts and content hashes unchanged**, comparing the original fields and excluding only newly added nullable fields/revision. [Preservation log](../../../verification/sprint81-preservation.txt).
- Scratch restore: private pre-upgrade pg_dump restored to new ppm_sprint81_restore; 59 table hashes/counts and one object hash matched. Normal database was not replaced. The final application restart also preserved the one established object hash (`sprint81-object-preservation.txt`). [Restore log](../../../verification/sprint81-restore.txt). Private backups, tokens, fixture credentials and object contents remain in ignored artifacts/local.
- Real SMTP signup/activation/invitation/reset: **BLOCKED** until an authorized SMTP provider/sender and recipients are available. Adapter fixtures and SMTP acceptance flags do not prove inbox delivery.
- Hosted CI: **UNVERIFIED**. The base commit is not a checkpoint of this dirty working tree. A reviewed revision must be committed/pushed with preserved unrelated work and linked to an actual hosted run before closing this gate.
- DOCX regenerated using bundled Python; packaged renderer failed with missing soffice.exe (and sandbox temporary cleanup errors). Content correction is complete, visual layout is **UNVERIFIED**. Do not distribute the regenerated Word guide until rendering and every-page QA pass. The reviewed Markdown guide is available now.
- Jira/GitHub real credentials and genuine training/history remain unverified; this sprint adds no model, evidence/OCR, document intelligence or production deployment.

## Changed surfaces and decisions

New migration 0008; identity/challenge/profile/invitation APIs and mail worker integration; workspace search/setup/comparison/My work/notifications/events; nullable delivery metadata; existing assessment access/list APIs and shared selectors; signup, Account, overview, palette, project, resources, assessments, integrations and command center screens; generated OpenAPI/TypeScript contracts; backend/browser fixtures and preservation/restore/static scripts. Full current file list is recorded in [the checkpoint manifest](../../../verification/sprint81-checkpoint.json). Pre-existing dirty changes are not all attributable to Sprint 8.1.

The [pilot contract](../../../contracts/pilot.md) records revision-based SSE instead of a duplicate manual-change outbox, notification presentation retention and delivery ambiguity. The [user guide](SPRINT_8_1_USER_GUIDE.md) explains local operator mail, role scopes, Unknown metadata and planned → active → closed sprints.

## Closure and next action

Tasks 001 and 003–009 are complete locally (**8 of 10**). Task 002 remains BLOCKED for real inbox acceptance; task 010 remains PARTIAL for hosted CI and Word visual QA.

Sprint 09 prerequisites are **not fully satisfied**: real account delivery, hosted CI and rendered Word-guide acceptance remain open. Existing data/identity/grants/metadata/paging/restore interfaces are available locally. Resolve only these Sprint 8.1 gates next; do not start Sprint 09 without separate authorization. No release criterion was weakened to close a task.


## 10 October 2026 follow-up: account and website workflow repair

The separate [repair and walkthrough execution report](../../../04-testing/ACCOUNT_WORKFLOW_REPAIR_REPORT.md) records migration `0009_account_repair`, account/membership separation, organization profile/name controls, calendar navigation, shared business errors, the verified scoped Hement grant correction, guarded training data and current tests. Earlier sprint evidence remains historical. Global production identity administration, live-provider acceptance, general document intake and AI remain PLANNED or unverified according to their existing gates; this follow-up does not close those gates.
