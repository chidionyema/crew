from tenant_sweep.parallel import chunked, fanout_batches, map_parallel


def test_map_parallel_empty_returns_empty():
    assert map_parallel([], lambda x: x, workers=4) == []


def test_map_parallel_preserves_input_order():
    out = map_parallel(range(10), lambda x: x * 2, workers=4)
    assert out == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


def test_chunked_splits_correctly():
    assert chunked([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_fanout_batches_runs_each_batch_once():
    seen: list[tuple[int, ...]] = []

    def collect(batch: list[int]) -> None:
        seen.append(tuple(batch))

    fanout_batches([1, 2, 3, 4, 5, 6, 7], batch_size=3, workers=2, fn=collect)
    assert sorted(seen) == [(1, 2, 3), (4, 5, 6), (7,)]
