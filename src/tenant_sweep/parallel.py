"""Bounded worker pool. Concurrent fan-out; results come back in submission order."""
from __future__ import annotations

import threading
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor


def map_parallel(
    items: Iterable,
    fn: Callable,
    workers: int,
) -> list:
    items = list(items)
    if not items:
        return []
    workers = max(1, workers)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(fn, items))
    return results


def fanout_batches(
    items: list,
    *,
    batch_size: int,
    workers: int,
    fn: Callable[[list], object],
) -> list:
    """Run `fn` on each batch in parallel. Used for storage appends and bulk POSTs."""
    if not items:
        return []
    batches = [items[i : i + batch_size] for i in range(0, len(items), batch_size)]
    return map_parallel(batches, fn, workers=min(workers, len(batches)))


def chunked(items: Iterable, size: int) -> list[list]:
    items = list(items)
    return [items[i : i + size] for i in range(0, len(items), size)]
