# Sprint 11.1 implementation baseline — T01

User authorized implementation on 17 October 2026. Source HEAD remains `d0ebe32e691a3d63166ced669450911c63151127`; existing uncommitted planning/index/changelog files are preserved. No AGENTS.md was found. Canonical instructions and revised hybrid handover were read.

Observed normal database revision: **0012_ai_runtime** through read-only psql. Source expects 0014. Eight existing Docker containers running; web/API/Postgres/Redis/scanner report healthy. These services were not upgraded or rebuilt. Existing preservation code, with a new private destination `artifacts/local/sprint111`, captured .env/source/prompt/migration hashes, Git patch/untracked archive, counts/hashes of 70 established tables, a database dump and original object archive. Existing Sprint 11 checkpoints were not overwritten. An orphan-container informational warning did not trigger any cleanup.

Fresh offline baseline: **148 passed, 1 skipped, 108 deselected**, one inherited Starlette/httpx deprecation warning. [Output](implementation/baseline-tests.txt). Provider/integration/worker access was not enabled. [Generated-contract baseline](implementation/baseline-contracts.txt) is recorded separately. No normal data, credentials, applied migration or provider binding changed.

Next: T02 typed hybrid/execution contracts and negative validation tests, then additive T03 task/quota persistence. New migrations are tested in guarded disposable ppm_test only. V2 remains default-off. Hardware qualification and optional live free-provider activation are later gates, not assumed implementation success.
