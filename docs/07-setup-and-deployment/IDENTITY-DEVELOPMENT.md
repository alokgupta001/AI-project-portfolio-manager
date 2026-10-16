# Sprint 02 identity: local operation and acceptance

This page retains the operator-only local-preview alternative. Development Gmail signup, existing-account invitation and recovery are now verified. Normal users follow the [website manual](../06-user-guides/WEBSITE_WALKTHROUGH.md) and [member/PM access guide](../06-user-guides/MEMBERS_ROLES_AND_ACCESS.md); operators follow [Gmail SMTP setup](GMAIL-SMTP-SETUP.md) and [email delivery](EMAIL-DELIVERY.md). Current schema head is `0012_ai_runtime`; statements about the Sprint 02 migration below describe that historical checkpoint.

Use the project root. Start Docker's Linux engine, then:

```powershell
.\.venv\Scripts\python.exe scripts/bootstrap.py
docker compose up --build -d --wait
```

On this host Docker is not on PATH. For this terminal:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;$env:PATH"
```

Bootstrap preserves existing database passwords and adds a missing random `PPM_JWT_SECRET`. Do not regenerate the signing key on each run. `PPM_WEB_ORIGIN` defaults to `http://localhost:3000`; use that exact browser origin for identity screens. Secure cookies were verified in Chromium on localhost. Other browsers/origins are not claimed verified; production remains disabled and needs HTTPS. The root foundation status can still be read at 127.0.0.1.

## Create the first organization and activate its Admin

Replace the example address and organization with the local account you want. This command does not send email, create paid resources or set a known default password:

```powershell
docker compose run --rm migrate python scripts/bootstrap_identity.py --email admin@example.com --organization "My organization"
docker compose exec -T api python scripts/local_mailbox.py --email admin@example.com --kind activate
```

The second command deliberately displays private one-time activation links in your terminal. Open the latest unexpired link, enter a display name and a password of at least 12 characters and at most 72 UTF-8 bytes. Activation proves possession of the delivered challenge. Then sign in at http://localhost:3000/login. Do not copy mailbox contents or credentials into reports, screenshots or Git.

Initialization refuses to create another organization unless the operator explicitly passes `--additional-organization`. This privileged local flow can attach an existing verified user as the new organization's Admin. It is not a browser privilege and must not become an anonymous API endpoint. No local first Admin was created automatically during implementation; acceptance identities were isolated test fixtures.

## Exercise roles and account settings

At `/account`, choose an organization; IDs distinguish identical names. Admin can create invitations, review/update member role and active state, and read identity audit entries. Project Manager and Viewer can manage their own profile, credentials and sessions; neither can administer membership. Project/portfolio Grants, Resource access and framework/result Access panels are now implemented; follow the website access guide for the separate scoped permissions.

An invitation appears in the same private local mailbox:

```powershell
docker compose exec -T api python scripts/local_mailbox.py --email invited@example.com --kind invite
```

New recipients choose a password and name when accepting. Existing verified users enter their current password. The token's organization/role cannot be changed by the form. Existing memberships are not overwritten or silently reactivated. Membership reactivation and role changes require Admin edits, and the final active Admin cannot be removed/demoted. Member updates use the displayed revision; reload after a stale-data error. Unsafe membership requests must include `X-Organization-ID` matching the current session as a precondition against stale tabs; it never supplies authorization.

Use `/account/reset` to request recovery. It returns the same message for eligible and unknown addresses. For local eligible accounts, inspect `--kind reset` messages. A successful reset consumes the challenge and invalidates every session, including the requesting browser. Activation/invitation links expire after 24 hours; reset links after 30 minutes. Consumed or expired links cannot be reused.

The session list shows the latest 100 active sessions. Revoke one immediately, or reset the password to revoke all. Access tokens expire after ten minutes and refresh rotates within a fixed seven-day session. Refresh replay revokes the whole session; simultaneous refreshes from different tabs can require signing in again. Browser tokens are Secure/HttpOnly cookies, not localStorage values.

## Reproduce acceptance

```powershell
docker compose --profile test run --build --rm test
npm run contracts:check
node scripts/check-identity-browser.mjs
docker compose exec -T api python scripts/smoke_worker.py
node scripts/check-persistence.mjs
```

Use `PPM_DOCKER` for the full Docker path if needed. Backend tests use `ppm_test` and Redis DB 1; the migration runner checks these guards. Browser acceptance creates project `enterprise-ppm-identity-test`, ports web3001/API8001/PostgreSQL15433/Redis16380, and independent named volumes. Its fixture generator refuses non-test databases. The runner creates random credentials only in ignored `artifacts/local/identity-fixture.json`; fixtures remain in the isolated test volumes. It stops/removes only this test project's containers/network afterward, preserving volumes. Do not run multiple acceptance runners against the same project concurrently.

The runner removes its generated fixture JSON on exit. The ordinary `npm run test:e2e` skips identity without that fixture; it is not complete Sprint 02 acceptance. Use the runner above. GitHub Actions invokes the same isolated runner, but no hosted Actions execution is claimed. Screenshots/traces are private ignored artifacts. Browser traces can include test cookies and tokens; do not publish them as general documentation.

## Recovery, migration and limitations

Migration head is `0002_identity`, extending the unchanged `0001_foundation`. No existing installation checkpoint is replaced. On initialized databases, role grants/RLS arrive through the migration; the original PostgreSQL init script is not relied upon to rerun. No domain tables, backfills, cloud provider or SMTP credentials are needed.

Rollback removes identity tables and credentials; it is destructive to identity data and is exercised only in the isolated test DB. Back up real local identity data before any deliberate rollback. `docker compose stop` preserves volumes. Do not use a factory reset or `down --volumes` to work around Docker startup errors.

Mailbox files are stored under `/var/ppm/objects/__identity_mailbox__` in the local object volume, private to the application container user and local operators. They are retained until deliberate operator cleanup; token expiry does not erase inbox files. Real email delivery, automated retention, account lockout recovery policy, production signing-key rotation, penetration/load testing and full accessibility auditing are not claimed here. See [ADR 008](../architecture/adr/008-identity-implementation.md) for the security boundary and implementation tradeoffs.


## Global account lifecycle after account repair

Migrations `0009_account_repair` and `0010_account_authority` separate global active identity from nullable selected-organization context and cancel queued work after global disable. All personal account routes still validate session, signature, verified/active identity and CSRF on writes. Organization routes additionally require live membership; no-member login confers no tenant access. Global disable uses the development owner-only command documented in [training provisioning](../05-demos/WALKTHROUGH_DATA.md). Do not use organization role changes as global suspension.
