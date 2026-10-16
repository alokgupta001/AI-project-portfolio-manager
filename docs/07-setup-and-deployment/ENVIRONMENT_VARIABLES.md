# Configuration field reference

Verified against `config.Settings`, Compose and `.env.example` by field name only. No real secret values were read/copied. Local/test/demo are allowed; production is rejected. Setup commands are source-reviewed, not freshly run.

| Variable | Purpose / definition |
| --- | --- |
| `PPM_APP_ENV` | Literal['local', 'test', 'demo']; required |
| `PPM_DATABASE_URL` | SecretStr; required |
| `PPM_REDIS_URL` | SecretStr; required |
| `PPM_STORAGE_ROOT` | Path; required |
| `PPM_JWT_SECRET` | SecretStr; required |
| `PPM_WEB_ORIGIN` | str; default/validation: `'http://localhost:3000'` |
| `PPM_COOKIE_SECURE` | bool; default/validation: `True` |
| `PPM_MAIL_MODE` | Literal['local', 'smtp']; default/validation: `'local'` |
| `PPM_SMTP_HOST` | str; default/validation: `''` |
| `PPM_SMTP_PORT` | int; default/validation: `Field(default=587, ge=1, le=65535)` |
| `PPM_SMTP_USER` | str; default/validation: `''` |
| `PPM_SMTP_PASSWORD` | SecretStr; default/validation: `SecretStr('')` |
| `PPM_MAIL_SENDER` | str; default/validation: `''` |
| `PPM_DEPENDENCY_TIMEOUT_SECONDS` | float; default/validation: `Field(default=3.0, gt=0, le=10)` |

Additional Compose/bootstrap-only configuration keys: `PPM_API_PORT`, `PPM_APP_PASSWORD`, `PPM_JWT_SECRET`, `PPM_MAIL_MODE`, `PPM_MAIL_SENDER`, `PPM_OWNER_PASSWORD`, `PPM_POSTGRES_PASSWORD`, `PPM_POSTGRES_PORT`, `PPM_REDIS_PORT`, `PPM_SMTP_HOST`, `PPM_SMTP_PASSWORD`, `PPM_SMTP_PORT`, `PPM_SMTP_USER`, `PPM_WEB_ORIGIN`, `PPM_WEB_PORT`

`API_ORIGIN` is the Next.js server proxy destination. Loopback origins/ports must match CSRF/cookies. Migration credentials belong only to migration tooling; ordinary requests use the app role. SMTP uses STARTTLS and private secrets; development Gmail signup, existing-account invitation and recovery are verified. See [Gmail SMTP setup](GMAIL-SMTP-SETUP.md), [local setup](LOCAL-DEVELOPMENT.md) and [identity operations](IDENTITY-DEVELOPMENT.md).

In smtp mode, host and a valid verified sender are required; user/password must both be supplied or both absent for an authorized relay. Implicit TLS port 465 is rejected; use the provider's STARTTLS port, usually 587. Configuration errors redact values. Apply settings to API/worker/dispatcher together; isolated automated services force local delivery. Full setup and Gmail acceptance: [Email delivery](EMAIL-DELIVERY.md).

## Document scanner configuration

| Variable | Current definition |
| --- | --- |
| `PPM_DOCUMENT_SCANNER_HOST` | Empty by default; missing scanner quarantines. `compose.documents.yaml` sets `clamav` for API/worker/test. |
| `PPM_DOCUMENT_SCANNER_PORT` | Default 3310, valid ports 1–65535. Private scanner network port, no published host listener. |

Do not add secrets or scanner bypass flags. [Operator startup/recovery](DOCUMENT-PROCESSING.md)
documents the pinned image/package locks, required health and explicit reprocess after recovery.
## AI provider and budget configuration

The [AI runtime operator reference](AI-RUNTIME.md#configuration-and-spending) owns
all PPM_AI_* fields, explicit real-call authorization, zero/default spend, model IDs,
upper tariffs and the private optional env_file. Defaults remain disabled. The current local configuration authorizes Gemini free tier at $0 with one-time project/key confirmation; see [Gemini setup](GEMINI-FREE-TIER.md). Positive tariffs/ceilings apply only to separately authorized paid adapters, not Gemini's free-tier configuration.
A tenant budget never overrides the operator ceiling. Test/browser services force
disabled provider and no key. Never publish provider keys or private backups.
