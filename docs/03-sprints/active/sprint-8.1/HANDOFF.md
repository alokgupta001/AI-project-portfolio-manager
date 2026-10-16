# Sprint 8.1 handoff

**Current reconciliation — 16 October 2026:** The 10 October [development mail evidence](../../../04-testing/ACCOUNT_EMAIL_VERIFICATION.md) supersedes missing-SMTP statements for signup, existing-account Viewer invitation and recovery. Sprint 09 is now complete locally and Sprint 10 has bounded Gemini smoke verification; resolve [LATEST](../../../handoffs/LATEST.md) before continuing. Earlier instructions below retain their historical scope and grant no successor authorization.

Read the [report](SPRINT_REPORT.md), [task checks](../../../04-testing/sprint-based/sprint-8.1/PPM-81-010.md), [pilot contract](../../../contracts/pilot.md) and [tester guide](SPRINT_8_1_USER_GUIDE.md). Sprint 8.1 is implemented locally with parent acceptance OPEN. Migration head 0008_pilot_completion is now applied and frozen. Do not edit it; make another migration if a correction is required.

Normal stack uses established ppm_local and volumes, localhost 3000/8000. Browser fixtures use separate identity-test volumes at 3001/8001; runner stops containers and preserves volumes. Backend test runner resets only guarded ppm_test. Private pre-upgrade DB dump, hashes, object archive and restore evidence are ignored under artifacts/local/sprint81. Scratch ppm_sprint81_restore is retained. All 59 established tables match their pre-upgrade fields and contents. Sources/prompts and migrations 0001–0007 match the saved manifest.

Branch main base 90564405bcacc8389e34f3b06d8ab8d00984c5c1 has pre-existing dirty Sprint 08/learning work; preserve it. No Git reset/clean, commit/push or live deployment occurred. Final file manifest is a local review checkpoint, not hosted CI.

Continue only remaining 8.1 acceptance: authorized real SMTP four-message inbox checks; reviewed checkpoint/hosted CI; supported bundled DOCX render and every-page visual review. New Markdown instructions are available, generated Word content is corrected but must not be distributed until visual QA. Read final report for exact test results. No live Jira/GitHub, training/model or production acceptance is established. Sprint 09 is not authorized and prerequisites remain incomplete.

Completed locally: PPM-81-001 and 003–009. Full backend 74 plus focused stream 1; full browser 12 plus affected final 6; all eight static gates pass. Only 002 real mail and 010 external/visual gates remain open. [Checkpoint](../../../verification/sprint81-checkpoint.json) records the reviewed local file hashes, not a hosted revision.
