# API service

[ppm_api/main.py](ppm_api/main.py) composes the FastAPI process. All feature HTTP
handlers delegate to [business operations](ppm_api/modules/README.md); schemas and
tables live with their owning feature. The [shared foundation](ppm_api/shared/README.md)
contains common record primitives and explicit metadata registration.

Configuration, database setup, errors, health schemas and private storage remain
at the package root. Applied migrations stay in migrations/versions. See the
[project map](../../docs/01-architecture/PROJECT_MAP.md) and
[setup guide](../../docs/07-setup-and-deployment/LOCAL-DEVELOPMENT.md).
