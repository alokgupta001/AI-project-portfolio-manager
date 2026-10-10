# Website walkthrough provisioning — 10 October 2026

This operator guide accompanies the unchanged 18-section [website journey](../06-user-guides/WEBSITE_WALKTHROUGH.md). The training data is fictional and isolated in **Northstar Website Training**. It does not alter the existing invitation-test organization or reuse personal accounts.

## Prepared local instance

The local `ppm_local` database contains Asha Admin (Admin), Priya Manager and Ravi Reviewer (Project Managers), and Vera Viewer (Viewer). Reserved emails are `walkthrough-asha@example.com`, `walkthrough-priya@example.com`, `walkthrough-ravi@example.com`, and `walkthrough-vera@example.com`. These addresses receive no external mail. Seed provisioning uses a guarded operator bootstrap, while the separate browser test exercises real signup and invitation acceptance in local mail mode.

Passwords are randomly generated once. The private container file is `/var/ppm/objects/__walkthrough__/credentials.json`; an ignored local copy is at `artifacts/local/repair-20261010/walkthrough-credentials.json`. Read it locally for the intended training account. Do not share it, commit it, paste it into logs, or use these credentials outside this development instance. Keep four browser profiles separate and open [localhost:3000](http://localhost:3000).

The seed creates 41 manifest records: settings; department/team and two team memberships; goal/portfolio/program; delivery and resource grants; metric policy; immutable calendar; linked resource, availability, staffing and skill; portal project; planned sprint; three work items; two milestones; budget/expenditure; risk/blocker; goal alignment/benefit; baseline/metric plan/status; allocation/time off/effort; framework/version and a draft assessment assigned to Priya with Ravi as reviewer. The automatic project-creator grant is additional to the manifest. It leaves delivery and assessment states available for practice; no answers, completed score, AI output or external integration success is fabricated.

## Reproduce safely

Run from the repository root with the established Compose environment:

```powershell
docker compose up --build -d --wait
docker compose run --build --rm migrate python scripts/seed_walkthrough.py
docker compose run --rm migrate python scripts/check_walkthrough.py
```

The script refuses a production or mismatched database, uses the owner connection only for the reserved identity transaction, and uses authenticated restricted application requests for planning records. Stable identifiers, idempotency keys and a private manifest prevent duplicate creation. Reserved-email collisions or inconsistent identities cause a refusal rather than account adoption. Reruns preserve existing values and deliberate edits; missing or inaccessible manifest records require inspection rather than automatic replacement. The checker verifies memberships, selected relationships, counts and a content fingerprint. Compare its fingerprint before and after a rerun.

For a fresh first-time identity-only setup, use `--empty` on the **first** seed invocation. It does not delete records if the full seed already ran. To practice every action from signup, create a fresh fictional organization through the website using controlled email addresses or the isolated browser runner. Do not recreate existing projects with the same names in the prepared organization simply to repeat setup.

## Reset and account administration

There is no one-click destructive reset. Archive training records through supported website controls, revoke unused grants/memberships, and retain immutable baselines, calendar versions and results. Do not truncate the database or remove shared volumes. `docker compose down` preserves volumes; `down -v` is not a training cleanup instruction.

Global account disabling is a separate development operator operation:

```powershell
docker compose run --build --rm migrate python scripts/account_status.py <user-uuid> disable --reason "Authorized development account suspension"
docker compose run --rm migrate python scripts/account_status.py <user-uuid> enable --reason "Authorized development restoration"
```

Use a verified UUID and retain the operator's reason/change record. The owner connection is the authorization boundary; organization Admin does not expose this command as a website API. Disabling preserves all memberships/ownership, revokes sessions, and refuses an organization's last active verified Admin. Enabling restores no sessions and changes no memberships or grants. This command is restricted to matching local/test/demo databases; production identity administration remains PLANNED. No real user's global account was disabled during this repair.

The guarded `repair_hement_access.py` is a one-time local data correction for the exact diagnosed Hement/project relationship, not a general seeding command. It leaves role, ownership, credentials and unrelated grants unchanged and reruns as a no-op.

## The project in the user's existing organization

The user's browser was signed in as Ashu in **Northstar Invitation Test 2026-10-10**, rather than the separate seeded training organization. The actual [Customer Onboarding Portal](http://localhost:3000/projects/1c152bcb-ff85-4f5b-9c18-2678ba4af628) is now populated with clearly labelled fictional demo records in all 14 delivery sections. Its existing project metadata, creator/owner, member identities, organization roles and portfolio grants are preserved.

| Section | Active records |
| --- | --- |
| Work items | 6 |
| Milestones | 3 |
| Sprints | 2 |
| Blockers | 1 |
| Risk register | 2 |
| Business benefits | 2 |
| Metric plans | 1 |
| Dependencies | 3 |
| Budget lines | 2 |
| Expenditure | 2 |
| Status updates | 2 |
| Plan baselines | 1 |
| Goal alignment | 1 |
| Project & portfolio access | 3 |

Ashu remains Admin with organization authority. Hement and Alok Gupta remain Project Managers with explicit project **edit** grants; Blaze remains Viewer with explicit project **read** access. Work is assigned to Hement and Alok. The planned sprints cover 12–23 October and 26 October–6 November. Six work items carry owners, types, points, dates, status and detailed descriptions. Three acyclic dependencies connect predecessor/successor work. The immutable baseline captures the populated work/sprint/milestone/budget plan, and the metric plan references that baseline and a new immutable India weekday calendar.

The example approved budget totals INR 200,000 and fictional expenditure INR 20,000. The ledger remains partial; realized business benefits remain unknown. Planned milestones and sprints are not falsely marked complete. The latest fictional risk update reports Amber. No actual payment, release, customer acceptance or measured benefit is claimed.

The narrowly guarded operator command below requires a live Ashu Admin session in this exact local organization. It uses the restricted application connection and existing validation, live authority locks, audit/history, notification and baseline commands. It performs all writes in one transaction and refuses changed identities/roles or a mismatched/archived project. Reruns reuse existing records and preserve subsequent edits; the verified second run created no records. Credentials and memberships are never replaced.

```powershell
docker compose run --build --rm migrate python scripts/fill_current_portal.py
```

Private before-state and result files are under `/var/ppm/objects/__current_portal__/`; browser counts/screenshots and execution logs are in ignored `artifacts/local/repair-20261010/current-portal-*`. All 14 tabs were opened and their saved record counts verified in the user's browser after reload. This command targets the existing portal only; `seed_walkthrough.py` continues to target the separate fictional training organization.
