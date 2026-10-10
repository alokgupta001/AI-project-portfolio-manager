# Isolated delivery demo

Sprint 04 demo v1 is separate from the user's normal localhost:3000 workspace. It uses project `enterprise-ppm-demo`, database `ppm_demo`, distinct named volumes, and ports 3002/8002/15434/16381. Never use `down --volumes` as routine cleanup. Docker Desktop Linux engine must be running.

In a fresh PowerShell terminal at the repository root (with Docker on PATH):

```powershell
$env:PPM_MAIL_MODE = 'local'
$env:PPM_WEB_PORT = '3002'
$env:PPM_API_PORT = '8002'
$env:PPM_POSTGRES_PORT = '15434'
$env:PPM_REDIS_PORT = '16381'
$env:PPM_WEB_ORIGIN = 'http://localhost:3002'
docker compose -f compose.yaml -f compose.demo.yaml up --build -d --wait
docker compose -f compose.yaml -f compose.demo.yaml run --rm migrate python scripts/seed_delivery_demo.py
```

Seed is guarded by demo configuration and actual database name. It is transactional and deterministic; repeat execution preserves all records and subsequent edits. Two separate tenants each contain a portfolio/program, department/team/goal, healthy Customer Portal and troubled ERP projects, milestones/work/blockers, alignments and different-currency budgets/expenditure. Canonical repeated names exercise isolation. One project has a complete ledger; another deliberately incomplete. No source data or normal local tenant is imported.

The first tenant's account is `demo@example.com`; there is **no default password**. Activation uses the existing private local mailbox. The second tenant's separate account is `other-demo@example.com`; the first account is not its member. In the same demo-configured terminal, inspect your private activation message:

```powershell
docker compose -f compose.yaml -f compose.demo.yaml exec -T api python scripts/local_mailbox.py --email demo@example.com --kind activate
```

Open the returned localhost:3002 activation link privately, choose your password, then sign in at http://localhost:3002/login. Do not copy challenge links into reports or Git. Expired activation follows the existing identity recovery/bootstrap guide; an already seeded demo does not reissue activation automatically. The normal localhost:3000 account/password is independent. Nothing is emailed externally.

Stop only this demo with `docker compose -f compose.yaml -f compose.demo.yaml down`. Close this terminal before running normal local commands, so its demo port/origin overrides cannot affect the normal stack.
