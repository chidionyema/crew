"""Tenant list: loaded once, deduplicated, shared across workers."""
from __future__ import annotations

import threading
from collections.abc import Sequence


def unique_ordered(items: Sequence[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    out: list[str] = []
    for t in items:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return tuple(out)


class TenantList:
    """Loads the tenant list once and presents a dedup'd, indexed view."""

    def __init__(self, raw: Sequence[str] | None = None, loader=None) -> None:
        self._lock = threading.Lock()
        self._raw: tuple[str, ...] | None = tuple(raw) if raw is not None else None
        self._loader = loader

    def all(self) -> tuple[str, ...]:
        with self._lock:
            if self._raw is None and self._loader is not None:
                self._raw = tuple(self._loader())
            return self._raw or ()

    def unique(self) -> tuple[str, ...]:
        return unique_ordered(self.all())
