"""High-level sweep: pull every lever from the plan in one place."""
from __future__ import annotations

from dataclasses import dataclass

from .audit import AuditRow, AuditWriter
from .idp_client import IdpClaims, IdpClient
from .normalise import is_empty_payload, validate_and_normalise
from .parallel import fanout_batches, map_parallel
from .tenants import TenantList


@dataclass
class SweepSummary:
    swept: int
    skipped: int
    fetches: int
    posts: int
    audit_batches: int
    workers: int


def run_sweep(
    *,
    dry_run: bool,
    limit: int,
    workers: int,
    audit_batch_size: int,
) -> SweepSummary:
    tenants = TenantList(raw=tuple(f"tenant-{i:05d}" for i in range(limit)))
    idp = IdpClient()
    audit = AuditWriter(batch_size=audit_batch_size, sink=None if dry_run else lambda rows: None)

    # Shared, fetched once and reused across all workers.
    _ = idp.get_auth_token()
    schema_version = idp.get_schema_version()

    unique = tenants.unique()[:limit]
    fetches = 0
    posts = 0

    def per_tenant(tenant_id: str) -> tuple[str, IdpClaims, bool]:
        # Per-tenant claims are memoised: duplicates hit zero extra fetches.
        claims = idp.get_claims(tenant_id)
        # Lazy: skip validation/normalisation for empty payloads.
        if is_empty_payload(claims):
            return (tenant_id, claims, True)
        validate_and_normalise(claims, schema_version)
        return (tenant_id, claims, False)

    # Fan out GETs in parallel.
    fetched = map_parallel(unique, per_tenant, workers=workers)
    fetches += sum(1 for _ in unique)  # unique tenants only

    # Bulk POST in parallel batches where IDP supports it.
    to_post = [tid for tid, claims, skipped in fetched if not skipped]
    if not dry_run and to_post:
        def post_batch(batch: list[str]) -> None:
            idp.post_onboarding(tuple(batch))

        fanout_batches(to_post, batch_size=audit_batch_size, workers=workers, fn=post_batch)
        posts += len(to_post)

    # Batched audit appends: one storage write per batch.
    for tenant_id, claims, skipped in fetched:
        if skipped:
            continue
        if not dry_run:
            audit.append(AuditRow(tenant_id=tenant_id, status="ok", detail=claims.tenant_id))
    if not dry_run:
        audit.flush()

    return SweepSummary(
        swept=len(to_post),
        skipped=len(unique) - len(to_post),
        fetches=fetches,
        posts=posts,
        audit_batches=audit.batches_written,
        workers=workers,
    )
