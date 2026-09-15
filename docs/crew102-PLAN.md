# crew#102 — the four optimisations, in plan order

The plan posted on issue #102 names four optimisations, in this order:

1. **Memoised** — store `updatedAt` and the cache's content `sha256` in
   `~/.claude/ESTATE_BOARD.meta.json`. Pass `updatedAt` as a tag on the next
   `gh issue view`; on a match, skip the body fetch and go straight to the
   hash compare. An unchanged hash means skip the rename.

2. **Lazy** — sniff the first line of each comment for a backtick + 4-digit
   year. Backfill headers and prose fail the sniff and cost zero regex work.
   The three backfill comments never enter the parser.

3. **Parallelised** — fan the regex pass out across `min(N, os.cpu_count())`
   workers in `concurrent.futures.ThreadPoolExecutor`. Worth it when
   `N > 32`; below that the thread spin-up eats the win, so the planner
   picks serial.

4. **Batched** — hash the joined would-be output with `hashlib.sha256`
   and compare to the stored hash before opening the temp file. No
   content change → no rename.

This is a working note, not a contract. The contract lives in the code
(`scripts/estate-board-sync.py`, `scripts/estate-board-sync-meta.py`,
`scripts/estate-board-sync-graphql.py`) and the prove-mode tests
(`tests/test_incident_crew102_prove_mode.py`).

## Where each optimisation lives

| Optimisation   | Module                                | Test arm                                  |
|----------------|----------------------------------------|--------------------------------------------|
| Memoised       | `scripts/estate-board-sync-meta.py`    | `test_memoised_meta_module_…`             |
| Lazy           | `scripts/estate-board-sync.py:parse_comment` | `test_lazy_sniff_skips_prose`        |
| Parallelised   | `scripts/estate-board-sync-graphql.py:_max_workers` | `test_parallel_threshold_is_32` |
| Batched        | `scripts/estate-board-sync-meta.py:hash_joined` | `test_batched_hash_compare_skips_rename` |

## Plan proof rows

The plan's "Done commands" section names the proof; the gates pin it:

1. `python3 scripts/estate-board-sync.py --prove <cache>` — proves the
   summary line, prints `N row(s) from chidionyema/crew#102 -> <cache>`.
   Pinned by `test_prove_prints_pinned_summary_line`.
2. A second `python3 scripts/estate-board-sync.py <cache>` invocation
   logs `fetch: cache-hit` and `write: skipped (hash unchanged)`. Pinned
   by `test_second_invoke_logs_cache_hit_and_write_skipped` and arms D/E
   of `scripts/verify.d/46-estate-board-prove.sh`.
3. `bash scripts/verify.sh` returns `FAIL=0`. Pinned by the orchestrator
   and arms B/C of `scripts/verify.d/47-estate-board-snapshot-smoke.sh`
   (the snapshot's `board_sync()` row reports GREEN against the rebuilt
   cache).
