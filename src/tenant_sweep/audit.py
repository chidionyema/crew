"""Batched audit writer: coalesce many rows into one append per batch."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from threading import Lock


@dataclass
class AuditRow:
    tenant_id: str
    status: str
    detail: str = ""


class AuditWriter:
    """Holds rows until `flush` is called; one append per batch."""

    def __init__(self, batch_size: int = 500, sink=None) -> None:
        self._batch_size = batch_size
        self._sink = sink
        self._buf: list[AuditRow] = []
        self._lock = Lock()
        self.batches_written = 0

    def append(self, row: AuditRow) -> None:
        with self._lock:
            self._buf.append(row)
            if len(self._buf) >= self._batch_size:
                self._locked_flush()

    def _locked_flush(self) -> None:
        if not self._buf:
            return
        batch = self._buf
        self._buf = []
        if self._sink is not None:
            self._sink(list(batch))
        self.batches_written += 1

    def flush(self) -> None:
        with self._lock:
            self._locked_flush()

    @property
    def pending(self) -> int:
        with self._lock:
            return len(self._buf)
