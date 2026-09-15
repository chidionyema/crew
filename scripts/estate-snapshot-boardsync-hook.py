"""Document the append-only tail of scripts/estate-snapshot.

The actual snapshot script is in `scripts/estate-snapshot` and the wiring
adds one new block at the bottom that calls `scripts/estate-board-sync.py`
against the default cache. This docstring is what the bottom block does,
verbatim, so a reader of the snapshot script does not have to reverse
engineer it.

Wire, at the bottom of `scripts/estate-snapshot`:

    #############################
    # crew#102 — rebuild the board cache every snapshot run.
    # Append-only contract: do not gate the snapshot on board rebuild.
    # If the sync fails, surface it ONCE: print `[board-sync FAILED]` to
    # stderr and append a row to ~/.claude/state/board-deadletter.jsonl.
    #############################
    _board_sync_line = _board_sync()
    if _board_sync_line is not None:
        print(_board_sync_line, file=open(os.devnull, "w"))  # captured into the snapshot receipt
"""
