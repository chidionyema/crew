# Demo: every lane graded on what it emits (crew#508)

Founder, 2026-08-27: "science covers everything, when I say science I need to see progress
across all lanes simultaneously, everything needs to be feeding the machine."

## The command

    python3 science/showcase.py --print | awk '/^## Lanes/,/^## Warehouse/'

## The number behind it, straight from the store

    sqlite3 science/warehouse.db "select source, count(*) from facts \
      where ingested_at >= datetime('now','-24 hours') group by source order by 2 desc"

Add the per-source counts of one lane's sources (the `Sources counted` column names them) and
you get that lane's `Facts, 24h` cell. Nothing on the row is typed by hand.

## What it printed (2026-08-27, this checkout)

```
## Lanes

`sqlite3 science/warehouse.db "select source, count(*) from facts where ingested_at >= datetime('now','-24 hours') group by source"`

BLIND: science/warehouse.db has no readable facts table (no such table: facts)
```

The warehouse in this checkout is a 0-byte file, so the section refuses rather than printing
six zeroes that would read as "all lanes quiet". Before crew#508 that same empty file raised
`sqlite3.OperationalError` out of `build()` and took the whole page down.

## What it prints with a store that answers

```
| Lane | Facts, 24h | Checkpoints, 24h | Grade | Sources counted |
|---|---:|---:|---|---|
| data-ml | 0 | 0 | BLIND | dagster-ticks, dagster-runs, temporal_dev_executions, job_timelines |
| hermes-v2 | 0 | 0 | BLIND | alerts_inbox, sovereign_receipts, sovereign_budget, revenue, ... |
| portal | 0 | 0 | BLIND | estate_registry, capability_receipts, enforcement_map, drills, ... |
| science | 0 | 0 | BLIND | research_ledger, predictions, method_metrics, history, spend |
| code | 3 | 0 | GAP | ships, ci_runs, ci_reach, bundle_push, estate_push, ... |
| crew | 5 | 0 | GAP | board, ledger, decisions, directives, tickets, ... |
```

BLIND rows sort first, on purpose: a lane emitting nothing is unobserved, not healthy.

## The grades

| Grade | Means |
|---|---|
| ELITE | facts landed in 24h **and** a checkpoint was ticked in 24h |
| GAP | one of the two, never both — the lane runs but records nothing, or records but emits nothing |
| BLIND | zero facts in 24h; the lane is not feeding the machine and cannot be graded on anything else |
