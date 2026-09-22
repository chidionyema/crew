"""Entry point: `python -m tenant_sweep --dry-run --limit 1000`."""
from __future__ import annotations

import argparse

from .sweep import run_sweep


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tenant_sweep")
    parser.add_argument("--dry-run", action="store_true", help="Do not POST or write audit rows.")
    parser.add_argument("--limit", type=int, default=10_000, help="Cap on tenants per run.")
    parser.add_argument("--workers", type=int, default=32, help="Parallel worker pool size.")
    parser.add_argument(
        "--audit-batch-size",
        type=int,
        default=500,
        help="Audit rows coalesced per append.",
    )
    args = parser.parse_args(argv)

    summary = run_sweep(
        dry_run=args.dry_run,
        limit=args.limit,
        workers=min(args.workers, args.limit),
        audit_batch_size=args.audit_batch_size,
    )
    print(
        f"swept={summary.swept} skipped={summary.skipped} "
        f"fetches={summary.fetches} posts={summary.posts} "
        f"audit_batches={summary.audit_batches} workers={summary.workers}"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
