# Identity

Accounts, sessions, membership, live authorization and private account mail.

| File | Responsibility |
| --- | --- |
| [__init__.py](__init__.py) | Package description with no eager exports |
| [mail.py](mail.py) | Private account outbox delivery, local mailbox/SMTP and bounded retries |
| [router.py](router.py) | Thin HTTP adapters, request/response metadata and delegation to business operations |
| [schemas.py](schemas.py) | Account, session, membership and invitation input/output models |
| [service.py](service.py) | Account/session/organization operations, Principal/Auth, live permission checks and transaction-local RLS context |
| [tables.py](tables.py) | Identity, membership, challenge and session tables |

The HTTP layer and all domain callers use the same established Principal and transaction. Authentication, CSRF, live revocation and role/grant rules are unchanged. Account delivery tables now belong to identity/tables.

See the [contract](../../../../../docs/contracts/permissions.md),
[project map](../../../../../docs/01-architecture/PROJECT_MAP.md) and
[completed checks](../../../../../docs/04-testing/BACKEND_STRUCTURE_STEP_32.md).
