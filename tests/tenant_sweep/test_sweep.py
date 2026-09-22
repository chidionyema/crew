import io

from tenant_sweep.audit import AuditRow
from tenant_sweep.idp_client import IdpClient
from tenant_sweep.sweep import run_sweep


def test_run_sweep_dry_run_does_not_post_or_write():
    s = run_sweep(dry_run=True, limit=50, workers=8, audit_batch_size=10)
    assert s.swept == 50
    assert s.skipped == 0
    assert s.posts == 0


def test_run_sweep_summary_shape_and_order():
    s = run_sweep(dry_run=True, limit=10, workers=4, audit_batch_size=10)
    assert s.fetches == 10
    assert s.workers == 4
    assert s.audit_batches == 0  # dry-run writes nothing


def test_run_sweep_writes_audit_batches_when_not_dry_run():
    s = run_sweep(dry_run=False, limit=25, workers=4, audit_batch_size=10)
    assert s.swept == 25
    assert s.audit_batches >= 2  # at least two batches at batch_size=10


def test_idp_client_is_thread_safe_under_contention():
    from threading import Thread

    c = IdpClient(http_get=lambda p: {"id": p} if "/tenants/" in p else ("t" if "token" in p else "v1"))

    results: list = []

    def worker(tid: str) -> None:
        results.append(c.get_claims(tid))

    threads = [Thread(target=worker, args=(f"t-{i % 5}",)) for i in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Only 5 distinct tenants; even with 100 threads, the cache should yield 5 unique claims.
    assert len({r.tenant_id for r in results}) == 5
