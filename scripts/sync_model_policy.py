"""Validate or explicitly synchronize operator-owned provider scopes; never call a model."""

import argparse
import asyncio
import os

import sqlalchemy as sa
from ppm_api.agent_task_tables import scopes
from ppm_api.config import load_settings
from ppm_api.model_registry import ModelPolicy, load_policy
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine


def scope_rows(policy: ModelPolicy) -> list[dict]:
    rows = []
    for sid in sorted({p.quota_scope for p in policy.profiles}):
        profiles = [p for p in policy.profiles if p.quota_scope == sid]
        first = profiles[0]
        rows.append(
            dict(
                id=sid,
                provider_id=first.provider,
                policy_hash=policy.policy_hash,
                billing_class=first.billing_class,
                enabled=any(p.enabled and not p.benchmark_only for p in profiles),
                allowed_tenants=sorted({str(t) for p in profiles for t in p.allowed_tenants}),
                allowed_models=sorted({p.model for p in profiles}),
                concurrency_slots=first.concurrency,
                requests_per_minute=first.requests_per_minute,
                requests_per_day=first.requests_per_day,
                tenant_requests_per_day=first.tenant_requests_per_day,
                tokens_per_minute=first.tokens_per_minute,
                failure_count=0,
                revision=1,
            )
        )
    return rows


async def sync(policy: ModelPolicy) -> None:
    # Keep the DSN out of argv, errors and output. Application credentials cannot write scopes.
    url = os.environ.get("PPM_MIGRATION_DATABASE_URL", "")
    if not url:
        raise ValueError
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            revision = await conn.scalar(sa.text("SELECT version_num FROM alembic_version"))
            if revision != "0015_agent_task_runtime":
                raise ValueError
            for row in scope_rows(policy):
                values = {k: v for k, v in row.items() if k not in ("failure_count", "revision")}
                await conn.execute(
                    insert(scopes)
                    .values(**row)
                    .on_conflict_do_update(
                        index_elements=[scopes.c.id],
                        set_=values | {"revision": scopes.c.revision + 1},
                    )
                )
        # Existing failure, auth-disable and quarantine state is deliberately retained.
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply", action="store_true", help="Write scopes with migration-owner credentials"
    )
    args = parser.parse_args()
    try:
        policy = load_policy(load_settings())
        if args.apply:
            asyncio.run(sync(policy))
        print(
            f"PASS policy {policy.policy_hash}; {len(policy.profiles)} profiles; "
            f"{len(scope_rows(policy))} shared scopes; "
            f"{'synchronized' if args.apply else 'read-only validation'}"
        )
    except Exception:
        raise SystemExit(
            "Policy validation/synchronization unavailable; "
            "check private config, owner access and schema revision."
        ) from None


if __name__ == "__main__":
    main()
