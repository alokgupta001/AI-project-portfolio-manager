# Dependency verification — Sprint 12

Pandas 3.1.0 and scikit-learn 1.9.1 are pinned with the existing Python 3.12 stack.
Their BSD-3-Clause declarations and transitive versions are recorded in
[the regenerated installed inventory](../python-dependencies.json).
Official [pandas release metadata](https://pypi.org/project/pandas/3.1.0/) and
[scikit-learn install/support documentation](https://scikit-learn.org/stable/install.html)
were checked before adding them. No public external dataset was downloaded.

Actual `npm audit --audit-level=high`: 0 vulnerabilities.
Actual exported-lock `uvx --from pip-audit==2.9.0 python -m pip_audit --disable-pip --no-deps -r ...`:
No known vulnerabilities found. The audit retains its advisory to hash pinned exports;
installation still uses the repository's hash-locked uv.lock and frozen Compose build.
Raw logs are retained privately in artifacts/local/sprint12. No new paid/hosted service.
