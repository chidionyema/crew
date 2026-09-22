import threading

from tenant_sweep.audit import AuditRow, AuditWriter


def test_flushes_only_when_batch_full():
    sink_calls: list[list[AuditRow]] = []
    w = AuditWriter(batch_size=3, sink=lambda rows: sink_calls.append(rows))
    w.append(AuditRow("t1", "ok"))
    w.append(AuditRow("t2", "ok"))
    assert w.batches_written == 0
    w.append(AuditRow("t3", "ok"))
    assert w.batches_written == 1
    assert len(sink_calls[0]) == 3


def test_final_flush_writes_remainder():
    w = AuditWriter(batch_size=10, sink=lambda rows: None)
    for i in range(7):
        w.append(AuditRow(f"t{i}", "ok"))
    assert w.batches_written == 0
    w.flush()
    assert w.batches_written == 1
    assert w.pending == 0


def test_concurrent_append_is_safe():
    w = AuditWriter(batch_size=100, sink=lambda rows: None)

    def push(n: int) -> None:
        for i in range(n):
            w.append(AuditRow(f"t{i}", "ok"))

    threads = [threading.Thread(target=push, args=(20,)) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert w.pending == 100
    w.flush()
    assert w.batches_written == 1
