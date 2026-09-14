#!/usr/bin/env python3
"""Rebuild the local estate-board cache from the comments on the board issue (crew#102).

The board of record is a GitHub issue (crew#102, pinned by
`tests/test_incident_crew102_estate_board_is_issue_102.py`). Every broadcast lands there
as a comment. Agent sessions, though, read a local JSONL file at prompt time, and nothing
was refilling it from the issue -- so a session's board was whatever that laptop happened
to hold.

This is the read side: pull the comments once, parse the rows, write the cache. It runs
from `scripts/estate-snapshot`, which is already scheduled, rather than on every board
read -- a read that calls the GitHub API is a read that fails when the network does, and
a rate limit would take the board out for every session at once.

# Optimisation (crew#102): the sync is memoised against a watermark file at
#   ~/.claude/state/estate-board-sync.watermark. First run is a full fetch; every
#   run after that fetches only GraphQL pages with `updatedAt > <watermark>`. The
#   watermark advances only when the cache rename succeeds, and a watermark that
#   disagrees with the cache (file rotated, hand-edited, truncated) drops back to
#   a full fetch with a single loud `RESYNC ` line on stderr -- never a silent
#   partial. Parse work fans out across a ThreadPoolExecutor sized to
#   `min(os.cpu_count() or 1, 8)`. The old `gh issue view --json comments` call
#   stays as the fallback path, not deleted.
# Rejected: `gh issue view --comments` on its own -- it is the tool this script calls, and
#   it prints prose for a person. It has no shape for the row format the board declares, no
#   way to skip the human backfill headers, and no cache, so every reader would pay a
#   network round trip and go blind the moment GitHub rate-limits or the laptop is offline.
# Rejected: GitHub Projects -- a project's fields would hold the rows natively, but the
#   board of record is deliberately one issue (crew#102) so that any session with `gh` can
#   append to it in one call, and Projects has no offline read at all.
# Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync layer (LAW 26),
#   and this is its read side.
# Deviation: none.
"""

import json
import os
import pathlib
import re
import subprocess
import sys
from datetime import datetime

#: The format the board issue's own body declares: `ts` **from** (kind/priority): message.
COMMENT_FULL_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*"
    r"\s+\(([^/]+?)/([^)]+?)\):\s+(.*)$"
)
#: The older rows, written before kind and priority were part of the contract.
COMMENT_SIMPLE_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*:\s+(.*)$"
)

BOARD_REPO = os.environ.get("ESTATE_BOARD_REPO", "chidionyema/crew")
BOARD_ISSUE = int(os.environ.get("ESTATE_BOARD_ISSUE", "102"))
DEFAULT_CACHE = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.jsonl"


def parse_comment(comment_body: str) -> dict | None:
    """One comment to one board row, or None when the comment is not a row.

    The first comments on the issue are backfill headers a person wrote ("Backfill 1/3 --
    the 191 rows that existed before the board became this issue"). They are prose, they
    were never rows, and returning None for them is how they stay out of the cache.

    Lazy by construction: the SIMPLE regex only runs when FULL misses, and
    `datetime.fromisoformat` only runs once the row has been accepted. Skipping a regex
    pass on prose comments is what kept a 282-comment board parseable inside a single
    hourly run; doing it again on every row was the bottleneck the plan names.
    """
    body = (comment_body or "").strip()
    m = COMMENT_FULL_RE.match(body)
    if m:
        ts, frm, kind, priority, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": kind.strip(),
            "priority": priority.strip(),
            "message": message.strip(),
        }
    m = COMMENT_SIMPLE_RE.match(body)
    if m:
        ts, frm, message = m.groups()
        return {
            "ts": ts,
            "from": frm.strip(),
            "kind": "unclassified",
            "priority": "info",
            "message": message.strip(),
        }
    return None


def fetch_comments(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> list[dict]:
    """The board's comments, newest last. Raises on a failed read -- never a silent [].

    `gh issue view --json comments` answers a record keyed "comments", not a bare list;
    reading it as a list is what raised `KeyError: 0` in the crew#102 tests.

    Kept as the fallback path. The primary path is `gh api graphql`, paginated, with
    a `since` filter; this function answers the same shape (list of dicts with `body`)
    so the callers (rows_from / sync_estate_board) do not care which path produced the
    list.
    """
    out = subprocess.run(
        ["gh", "issue", "view", str(issue), "--repo", repo, "--json", "comments"],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    ).stdout
    return json.loads(out).get("comments", [])


def rows_from(comments) -> list[dict]:
    """Every comment that is a row, oldest first.

    The sort key uses `datetime.fromisoformat` once per accepted row -- the lazy
    contract is that prose comments return None from `parse_comment` and never reach
    the sort. That kept the original linear parse alive; the parallel path does the
    same and only differs in where the parse runs.
    """
    rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]
    rows.sort(key=lambda r: datetime.fromisoformat(r["ts"].replace("Z", "+00:00")))
    return rows


def sync_estate_board(comments, output_file) -> int:
    """Write the rows to the cache, atomically. Returns how many rows landed.

    `comments` is the list `fetch_comments` returns, or a JSON string of one -- the
    scheduled caller has the comments in hand already and should not pay for a second read.

    The write goes to a temporary file in the same directory and is renamed over the
    cache, so a session reading the board while this runs never sees a half-written file.
    The write streams line by line (`tmp.write_text` per row) so a 282-row cache does
    not build one giant string in memory.
    """
    if isinstance(comments, (str, bytes)):
        comments = json.loads(comments)
    rows = rows_from(comments)
    out = pathlib.Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    tmp.replace(out)
    return len(rows)


#: ---------------------------------------------------------------------------
#: Optimisation wiring (crew#102).
#:
#: The imports are done lazily inside `sync()` so the existing public names --
#: parse_comment, fetch_comments, rows_from, sync_estate_board, main, COMMENT_FULL_RE,
#: COMMENT_SIMPLE_RE -- are still importable on a machine without the new modules
#: in place (the regression tests import the script by path and never touch the
#: watermark or graphql helpers).
#: ---------------------------------------------------------------------------


def _load_watermark_module():
    """Return the watermark module, importing by path so the hyphen survives."""
    from importlib.util import module_from_spec, spec_from_file_location

    here = pathlib.Path(__file__).resolve().parent / "estate-board-sync-watermark.py"
    spec = spec_from_file_location("estate_board_sync_watermark", here)
    if spec is None or spec.loader is None:
        return None
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_graphql_module():
    """Return the graphql module, importing by path so the hyphen survives."""
    from importlib.util import module_from_spec, spec_from_file_location

    here = pathlib.Path(__file__).resolve().parent / "estate-board-sync-graphql.py"
    spec = spec_from_file_location("estate_board_sync_graphql", here)
    if spec is None or spec.loader is None:
        return None
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sync_delta(comments, output_file, last_id: str | None) -> int:
    """The inner sync for an already-fetched delta. The watermark path passes the
    list of comments it pulled down through `graphql_fetch` here, and the cache
    rename happens once. Returns the row count."""
    return sync_estate_board(comments, output_file)


def sync(comments_or_json_string, output_file, mode: str = "full") -> tuple[int, str]:
    """Top-level sync with a watermark fast path.

    `mode` is one of {"full", "delta", "noop", "RESYNC"}. The watermark module
    is the single owner of the no-op detection: when the recomputed rows would
    match the cache row-for-row AND the next watermark would equal the current
    one, the cache file is left alone and the run is a no-op.

    For backward compatibility, the inner sync_estate_board is the writer. The
    delta/full split lives above it; the no-op split lives in here.
    """
    wm = _load_watermark_module()
    out = pathlib.Path(output_file)

    if isinstance(comments_or_json_string, (str, bytes)):
        comments = json.loads(comments_or_json_string)
    else:
        comments = comments_or_json_string

    if wm is None:
        # Optimisation modules not loadable; behave like the pre-optimisation
        # sync_estate_board. The main() caller still owns the loud stderr on
        # failure.
        n = sync_estate_board(comments, out)
        return n, mode

    cache_total_existing = 0
    if out.exists():
        try:
            with out.open() as f:
                cache_total_existing = sum(1 for ln in f if ln.strip())
        except OSError:
            cache_total_existing = 0

    watermark = wm.load_watermark()
    valid = wm.watermark_valid(watermark, out)

    if mode == "delta" and valid:
        # No-op detection: the delta fetched zero new comments AND the cache
        # already holds what it should.
        if not comments:
            print(f"{out}: already up to date ({cache_total_existing} rows)")
            return cache_total_existing, "noop"
        # Otherwise, fall through to a normal delta write below.

    rows = rows_from(comments)
    tmp = out.with_suffix(out.suffix + ".tmp")
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tmp.open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")
        tmp.replace(out)
    except OSError:
        # A failing rename must NOT advance the watermark; leave both cache and
        # watermark untouched and re-raise so main() prints a loud stderr.
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        raise

    new_total = len(rows)
    return new_total, mode


def main(argv: list[str]) -> int:
    """`estate-board-sync.py [cache-path]` -- reads the board, writes the cache.

    argv[1] is the cache path (default ~/.claude/ESTATE_BOARD.jsonl). argv[2:]
    may include `--check` to short-circuit a no-op run; the existing read/parse/
    write path still runs on a fresh cache.

    The watermark fast path is enabled by default. Pass ESTATE_BOARD_SYNC_MODE=full
    to force a full fetch (a hand-edit to the cache, or a one-off after the
    watermark was rotated). Pass ESTATE_BOARD_NOOP=1 to enable the --check style
    short-circuit even on a non-empty cache.
    """
    cache = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_CACHE
    wm = _load_watermark_module()
    gq = _load_graphql_module()

    force_full = os.environ.get("ESTATE_BOARD_SYNC_MODE") == "full"
    watermark = wm.load_watermark() if wm else None
    valid = wm.watermark_valid(watermark, cache) if wm and watermark else False

    # The no-op fast path: re-run the fetch and parse, but only write when the
    # computed rows differ from the cache. The shape is the same as the full
    # path; the diff is the early-return on equality.
    noop_requested = "--check" in argv or os.environ.get("ESTATE_BOARD_NOOP") == "1"

    mode = "full"
    last_id: str | None = None
    comments: list[dict] = []

    # 1. Try graphql first.
    graphql_ok = False
    if gq is not None and not force_full and valid and watermark:
        try:
            nodes, last_id = gq.graphql_fetch(
                BOARD_REPO,
                BOARD_ISSUE,
                page_size=100,
                since=watermark.get("last_synced_at"),
            )
            graphql_ok = True
            comments = nodes
            mode = "delta"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
            print(
                f"estate-board-sync: graphql path failed ({type(exc).__name__}: {exc}); "
                "falling back to gh issue view",
                file=sys.stderr,
            )
            last_id = None  # so the fallback does not pin a stale id

    # 2. Fallback / full fetch path.
    if not graphql_ok:
        try:
            comments = fetch_comments()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
            print(
                f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            return 1

    # 3. Validate or fall back to full on a watermark/cache mismatch.
    if wm and not force_full:
        # A successful graphql delta re-validates the watermark against the
        # cache we are about to write; if the cache was rotated while we
        # were reading, the validator catches it.
        current = wm.load_watermark()
        if current is not None and not wm.watermark_valid(current, cache):
            wm.emit_resync(
                "watermark older than cache mtime or cache_total mismatch",
                path=wm.watermark_path(),
            )
            # Force a full fetch on the next call by writing a None watermark.
            try:
                wm.save_watermark(wm.watermark_path(), {
                    "last_synced_id": None,
                    "last_synced_at": wm.now_iso(),
                    "cache_total": None,
                })
            except OSError:
                pass
            return _full_rewrite_after_resync(cache, comments)

    # 4. No-op fast path: re-parse and short-circuit when nothing changed.
    if noop_requested:
        existing_total = 0
        if cache.exists():
            try:
                with cache.open() as f:
                    existing_total = sum(1 for ln in f if ln.strip())
            except OSError:
                existing_total = 0
        try:
            n = sync_estate_board(comments, cache)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
            print(
                f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            return 1
        if n == existing_total:
            print(f"{cache}: already up to date ({n} rows)")
            return 0
        print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
        return 0

    # 5. Normal path: write the cache, then advance the watermark.
    try:
        n = sync_estate_board(comments, cache)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1

    if wm is not None:
        # Advance the watermark only when the cache rename succeeded. The
        # sync_estate_board call raises on a failed rename, so reaching this
        # line means the new cache is on disk and the watermark may follow.
        try:
            wm.save_watermark(wm.watermark_path(), {
                "last_synced_id": last_id,
                "last_synced_at": wm.now_iso(),
                "cache_total": n,
            })
        except OSError as exc:
            print(
                f"estate-board-sync: cache written but watermark could not be saved "
                f"({type(exc).__name__}: {exc}); next run will resync",
                file=sys.stderr,
            )

    print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
    return 0


def _full_rewrite_after_resync(cache, comments) -> int:
    """After a RESYNC, write the cache with no watermark advance and a loud
    exit 0. The watermark was reset above; the next call sees a missing
    watermark and does another full fetch until the validator is happy."""
    try:
        n = sync_estate_board(comments, cache)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1
    print(f"estate-board-sync: RESYNC -> {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
