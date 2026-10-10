# Sprint 02 acceptance evidence

Executed 2026-10-05, Asia/Kolkata. Host Node 24.20.0/npm 11.19.0/Python 3.12.14; Docker Linux engine 29.7.2/container Python 3.12.15. Existing framework baseline retained. bcrypt 5.0.0, PyJWT 2.15.0 and email-validator 2.3.0 are locked. Declared licenses are in `python-dependencies.json` (59 installed host packages including tools).

| Acceptance | Actual execution | Result/evidence |
| --- | --- | --- |
| Starting checkpoint | Compose status; migration-role `alembic current`; contracts/source checks | PASS: healthy Sprint 01, head 0001, matching contracts before edits |
| Original preservation | `python scripts/check_sources.py`; migration SHA256 | PASS: seven source/prompt hashes; `0001_foundation.py` remains `C25D97DCFC74E0901A37673C160A7DBE6A80F7AD07B8A8BADCC80BA4127B4116` |
| Migration lifecycle | `docker compose --profile test run --build --rm test` | PASS: upgrade, downgrade to base, re-upgrade, repeated upgrade, schema drift; [backend transcript](../../../verification/sprint-02-backend.txt) |
| Backend suite | Same isolated runner | **28 passed**, one inherited Starlette warning; original 16 plus 12 identity integration tests |
| Tenant/RLS | Real app-role pool, two same-name organizations | PASS: missing-context empty reads, cross-tenant reads/writes denied, pooled context cleared, foreign composite reference rejected; non-super/non-bypass role |
| Roles/IDs/revisions | API integration tests | PASS: all three roles, live role/removal, forged selectors/hidden member/session IDs, stale organization writes and member revisions |
| Sessions/CSRF | Real DB/Redis HTTP tests | PASS: verified login, JWT expiry/audience/session checks, Origin/CSRF rejection, logout/revocation/session expiry |
| Concurrency | Simultaneous refresh and Admin demotions | PASS: one refresh winner plus replay rejection/family revocation; at least one active Admin retained |
| Activation/invitations | Real challenge rows/local spool and operator subprocess | PASS: guarded bootstrap, pending activation, single use, fixed organization, existing password proof, revoked inviter denied |
| Recovery/bcrypt | Reset/session tests | PASS: non-enumerating response content, expiry/single use, cost 12 hashes, UTF-8 byte limit, reset-wide revocation |
| Rate limits/audit | Redis and scoped audit | PASS: 429/Retry-After, scoped identity events and Admin-only audit reads |
| Browser lifecycle | `node scripts/check-identity-browser.mjs` | **3 Chromium tests passed** on separate test project; [browser transcript](../../../verification/sprint-02-browser.txt) |
| Browser detail | Sign-in, profile/reload, org switch, forbidden API, invite acceptance, recovery/new-password login | PASS: Secure/HttpOnly/SameSite cookies, no localStorage credentials, no JS errors, 360px no overflow; desktop/mobile screenshots visually reviewed |
| Python checks | Ruff check/format and mypy | PASS: 29 formatted files, 11 typed sources; tool output |
| Frontend/contracts | npm lint/typecheck/format:check/contracts:check | PASS; tool output |
| Build/start | `docker compose up --build -d --wait` | PASS; [runtime transcript](../../../verification/sprint-02-runtime.txt) |
| Regression | Real worker, persistence restart, migration current | PASS: checkpoint `44e56ee2-3bb9-4603-98e8-bf33e4dc8a5c` retained, object verified, head 0002; [regression transcript](../../../verification/sprint-02-regression.txt) |
| npm audit | `npm audit --audit-level=high` | PASS: zero reported vulnerabilities; no Python vulnerability audit claimed |
| Hosted CI / real email | Workflow updated; private local spool only | NOT RUN: no remote/push or external provider |

Resolved failures: API correctly refused migration commands without owner credentials; migration service succeeded. New migration rollback needed its dependent organization policy removed first; the corrected isolated lifecycle passes, with original 0001 unchanged. Browser fixture JSON initially included build output; capture is now separate. The nested organization selector needed its verified accessible combobox name. Screenshot review prompted atomic account-state updates and improved member controls; final UI run passed.

Interruptions left Docker's zero-byte Windows socket reparse points unusable. With Docker stopped, inspected runtime directories were preserved as sibling `run-stale-ppm-sprint02` and `docker-secrets-engine-stale-ppm-sprint02` backups and recreated. No images/settings/volumes reset. Sandbox ACL startup failures required reviewed escalation; Git inspection uses an exact per-command safe-directory exception, not global trust.

Limits: no hosted CI, real SMTP, other-browser certification, full accessibility/penetration/load test or production deployment. These tests cover identity, not future projects/files/SSE/vectors/workers. Global credential tables, strict replay and local mailbox retention are documented in [ADR 008](../../../architecture/adr/008-identity-implementation.md). Fixture credentials are ignored and removed; traces may contain disposable tokens. No user-owned local Admin was fabricated; use the tested [operator guide](../../../07-setup-and-deployment/IDENTITY-DEVELOPMENT.md). Work remains uncommitted.
