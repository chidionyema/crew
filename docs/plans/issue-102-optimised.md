# Optimised plan for issue 102

## Plain-English restatement

The ticket asks for an optimised plan that takes a naive step count, identifies
the bottleneck, decides what is memoised, parallelised, made lazy, or batched,
gives a final step count, and lists the exact commands that mark the work as
done. This file is the deliverable.

## Naive count: 12 sequential steps

1. Fetch input 1
2. Fetch input 2
3. Fetch input 3
4. Validate input 1
5. Validate input 2
6. Validate input 3
7. Transform input 1
8. Transform input 2
9. Transform input 3
10. Write output 1
11. Write output 2
12. Write output 3
(implicit verify step)

## Bottleneck

The repeated per-item network and disk work. Every item pays the full
round-trip cost serially, so latency stacks and the run is I/O bound, not
CPU bound.

## What is memoised

The per-item transformed payload, keyed by content hash. A second pass over
the same item becomes a dictionary lookup instead of a recompute.

## What is parallelised

The per-item fetch and validate steps, run as a bounded worker pool so
network calls overlap instead of stacking.

## What is made lazy

Schema validation and final aggregation only run on the items that survive
the cheap pre-filter, not on every candidate.

## What is batched

Writes are flushed once per buffer window and writes to the output target
are grouped into a single multi-item commit instead of one commit per
record.

## Optimised count: 5 logical steps

1. Warm cache
2. Parallel fetch + validate
3. Lazy transform with memo
4. Batched write
5. Verify

## Definition of done (commands that must pass)

- pytest -q
- ruff check .
- mypy src
- python -m crew.tools.bench --target crew/issue-102

After writing the file, return the commit sha from write_file. Do not do
anything else. Do not merge, do not open a pull request, do not touch any
cluster.
