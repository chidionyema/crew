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
import time
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
#: The dead-letter channel the loud-failure contract names. Every row that fails to reach
#: GitHub lands here, append-only, and emits a WARN to stderr -- never silently dropped
#: (LAW 28). Module-level constants so a session can override by monkeypatch in tests.
BOARD_DEAD_LETTER = pathlib.Path.home() / ".claude" / "state" / "board-deadletter.jsonl"
#: The sync-side state file. Holds the ETag of the last successful body fetch, the row count
#: at that time, and `last_pulled_at`. Atomic write, tmp -> rename, missing/corrupt -> {}.
BOARD_STATE = pathlib.Path.home() / ".claude" / "state" / "board-sync-state.json"


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


#: ---------------------------------------------------------------------------
#: crew#102 stale-only sync: state file + ETag + dead-letter.
#:
#: The prompt hook fires on every UserPromptSubmit (potentially many times per minute).
#: A full sync on every prompt would be a GitHub rate-limit trip the second any
#: session opened. The state file holds the ETag from the last successful body fetch
#: plus the row count at that time; the next sync short-circuits unless the issue
#: has actually moved. Any gh failure dead-letters the attempt -- never silent.
#: ---------------------------------------------------------------------------


def load_state(state_path) -> dict:
    """Read the sync state file. Returns {} on missing or corrupt JSON.

    A state file that exists but is unreadable JSON, or holds anything but a dict,
    is treated the same as a missing file: the next sync starts from scratch. A
    silent partial is the failure mode the watermark module already rejected;
    the same contract holds here.
    """
    p = pathlib.Path(state_path)
    try:
        text = p.read_text()
    except (OSError, FileNotFoundError):
        return {}
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def save_state(state_path, state) -> None:
    """Write the sync state file atomically. tmp -> rename, mkdir -p.

    Crash safety mirrors the cache writer: a failing rename leaves the previous
    state file in place, never a half-written one. A state file that does not
    exist yet is fine; the next sync treats it as the first run.
    """
    p = pathlib.Path(state_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(state, separators=(",", ":"), sort_keys=True) + "\n")
    tmp.replace(p)


def fetch_issue_comment_count(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> int | None:
    """The board's current comment count. Returns None on a failed read.

    Used by `sync_if_stale` to short-circuit when the count agrees with the state
    file: the cheap path that proves nothing changed without paying for a body
    fetch. A count of None is a failure and falls through to the body fetch.
    """
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{repo}/issues/{issue}", "--jq", ".comments"],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return None
    try:
        return int(out)
    except (ValueError, TypeError):
        return None


def fetch_comments_with_etag(
    repo: str,
    issue: int,
    *,
    etag: str | None = None,
) -> tuple[list[dict], str | None, bool]:
    """Fetch the comments list with an optional ETag. Returns (comments, new_etag, not_modified).

    A 304 from GitHub is `not_modified=True` with an empty list and the same ETag: the
    state file carries forward unchanged. Any 2xx with a body returns the parsed
    comments and the ETag from `ETag:` (or None when the server omits it). Other
    non-zero exits raise so the caller can dead-letter.

    The body shape is what `rows_from` already consumes: a list of dicts with a `body`
    field. No second parser is written here.
    """
    cmd = ["gh", "api", "-i", f"repos/{repo}/issues/{issue}/comments"]
    if etag:
        cmd += ["-H", f"If-None-Match: {etag}"]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        # `gh api -i` prints the body on stdout and exits 0; on a 304 it also exits 0
        # with no body and an `HTTP/2 304` status header at the top. A non-zero exit is
        # therefore a real failure and the caller dead-letters.
        raise
    raw = proc.stdout
    # Headers and body are separated by a blank line.
    if "\r\n\r\n" in raw:
        header_block, body = raw.split("\r\n\r\n", 1)
    elif "\n\n" in raw:
        header_block, body = raw.split("\n\n", 1)
    else:
        header_block, body = raw, ""
    status_line = header_block.splitlines()[0] if header_block else ""
    if "304" in status_line:
        return [], etag, True
    new_etag: str | None = None
    for line in header_block.splitlines():
        # ETag header is `ETag: "..."` per RFC 7232; gh prints it verbatim.
        if line.lower().startswith("etag:"):
            value = line.split(":", 1)[1].strip()
            new_etag = value.strip('"') or value
            break
    try:
        comments = json.loads(body) if body.strip() else []
    except (ValueError, TypeError) as exc:
        raise ValueError(f"could not parse comments body: {exc}") from exc
    if not isinstance(comments, list):
        comments = []
    return comments, new_etag, False


def _record_dead_letter(exc, *, repo=BOARD_REPO, issue=BOARD_ISSUE, command="gh issue view") -> None:
    """Append one JSON line to BOARD_DEAD_LETTER. Atomic. Never raises.

    The dead-letter file is the loud-failure channel. Any gh failure (CalledProcessError,
    TimeoutExpired, OSError, ValueError) lands here with ts/error/repo/issue/command --
    enough to reproduce and retry without guessing. A silent drop is worse than a
    red board (LAW 28), and the dead-letter is the only writer allowed to fail
    without raising because a) the caller cannot do anything with the failure and
    b) the noise on stderr is the second channel already.
    """
    try:
        path = pathlib.Path(BOARD_DEAD_LETTER)
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(
            {
                "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "error": f"{type(exc).__name__}: {exc}",
                "repo": repo,
                "issue": issue,
                "command": command,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        tmp.replace(path)
    except Exception:                                    # noqa: BLE001
        # The dead-letter is the last line of defence; a failure to write it is
        # already loud via the stderr print below, and there is nothing left to do.
        pass


def sync_if_stale(cache, state_path=BOARD_STATE, min_age_s: int = 300) -> tuple[int, str]:
    """Prompt-hook sync: skip work when nothing changed; otherwise fetch, write, dead-letter on failure.

    Returns (rows_written, status). `status` is one of "fresh", "updated", "dead-letter".

    Logic:
      * load state.
      * If `now - last_pulled_at < min_age_s` AND the live count == state["last_row_count"]:
        short-circuit. No fetch, no write, status "fresh", n=0.
      * Otherwise call `fetch_comments_with_etag(repo, issue, etag=state.get("etag"))`.
        A 304 returns status "fresh", n=0, state unchanged.
        A 200 parses through `rows_from`, writes atomically via `sync_estate_board`,
        saves state with the new ETag and counts. status "updated", n=rows.
      * Any CalledProcessError / OSError / ValueError -> `_record_dead_letter`,
        stderr print, return (0, "dead-letter"). Never raises.
    """
    state = load_state(state_path)
    last_pulled_at = state.get("last_pulled_at")
    last_row_count = state.get("last_row_count")
    state_etag = state.get("etag")

    now = time.time()
    if isinstance(last_pulled_at, (int, float)) and (now - float(last_pulled_at)) < min_age_s:
        live_count = fetch_issue_comment_count()
        if isinstance(live_count, int) and isinstance(last_row_count, int) and live_count == last_row_count:
            return 0, "fresh"

    try:
        comments, new_etag, not_modified = fetch_comments_with_etag(
            BOARD_REPO, BOARD_ISSUE, etag=state_etag
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError, ValueError) as exc:
        _record_dead_letter(exc, repo=BOARD_REPO, issue=BOARD_ISSUE,
                            command="gh issue view")
        print(
            f"estate-board-sync: stale-only -> dead-letter; {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 0, "dead-letter"

    if not_modified:
        # 304: server says nothing changed. Persist the touch so the count
        # short-circuit has a fresh `last_pulled_at`.
        state["last_pulled_at"] = now
        try:
            save_state(state_path, state)
        except OSError:
            pass
        return 0, "fresh"

    try:
        n = sync_estate_board(comments, cache)
        save_state(state_path, {
            "last_pulled_at": now,
            "last_row_count": n,
            "etag": new_etag,
            "repo": BOARD_REPO,
            "issue": BOARD_ISSUE,
        })
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError, ValueError) as exc:
        _record_dead_letter(exc, repo=BOARD_REPO, issue=BOARD_ISSUE,
                            command="gh issue view")
        print(
            f"estate-board-sync: stale-only -> dead-letter; {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 0, "dead-letter"

    return n, "updated"


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
    """`estate-board-sync.py [cache-path]` [-- --stale-only] -- reads the board, writes the cache.

    argv[1] is the cache path (default ~/.claude/ESTATE_BOARD.jsonl). `--stale-only`
    switches to the prompt-hook path: short-circuit on state and ETag, dead-letter
    on gh failure, never raise. The legacy full sync path is unchanged: existing
    callers and the verify gate keep byte-identical output.

    The watermark fast path is enabled by default. Pass ESTATE_BOARD_SYNC_MODE=full
    to force a full fetch (a hand-edit to the cache, or a one-off after the
    watermark was rotated). Pass ESTATE_BOARD_NOOP=1 to enable the --check style
    short-circuit even on a non-empty cache.
    """
    if "--stale-only" in argv:
        cache = pathlib.Path(BOARD_REPO) if False else DEFAULT_CACHE  # noqa: E712
        # cache stays the same default the legacy path uses; the only difference
        # is the path through `sync_if_stale`.
        cache = DEFAULT_CACHE
        n, status = sync_if_stale(cache)
        print(
            f"estate-board-sync: stale-only -> {status}, {n} row(s) "
            f"from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}"
        )
        return 0

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
            _record_dead_letter(exc, repo=BOARD_REPO, issue=BOARD_ISSUE,
                                command="gh issue view")
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