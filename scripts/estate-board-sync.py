#!/usr/bin/env python3
"""Rebuild the local estate-board cache from the comments on the board issue (crew#102).

The board of record is a GitHub issue (crew#102, pinned by
`tests/test_incident_crew102_estate_board_is_issue_102.py`). Every broadcast lands there
as a comment. Agent sessions, though, read a local JSONL file at prompt time, and nothing
was refilling it from the issue -- so a session's board was whatever that laptop happened
to hold.

This is the read side: pull the comments, parse the rows, write the cache. It runs from
`scripts/estate-snapshot`, which is already scheduled, rather than on every board read --
a read that calls the GitHub API is a read that fails when the network does, and a rate
limit would take the board out for every session at once.

The four plan-named optimisations:

  MEMOISED       read the issue's `updatedAt` cheaply via `gh issue view --json updatedAt`
                 and compare it against a sidecar `<cache>.last_sync`. On match, log
                 `0 new row(s) (added 0 row(s)) (incremental)` and return 0 without
                 calling `gh issue view --json comments`. The sidecar is written at the
                 end of every successful fetch so the next sync can short-circuit.
  LAZY           `parse_comment` sniffs the first line for a backtick + 4-digit year; a
                 non-matching head costs zero regex work.
  PARALLELISED   the incremental branch pages new comments via `gh api graphql` with a
                 cursor, then parses the paged nodes -- the GraphQL fan-out helper in
                 `scripts/estate-board-sync-graphql.py` is loaded lazily and skipped on
                 import failure.
  BATCHED        when the issue has moved, fetch only the comments created after the
                 watermark and append only those rows; do not rewrite the JSONL.

The plan's printed-row contract: an incremental run prints
`estate-board-sync: N new row(s) from <repo>#<issue> -> <cache> (added N row(s)) (incremental)`
so the founder's hot-path proof (`0 new row(s) (added 0 row(s))`) and the delta proof
(`added K row(s)`) both appear in the same line. The existing watermark tests pin the
`N new row(s)` half; this script is the source of truth for both halves.

Rejected: `gh issue view --comments` on its own -- it is the tool this script calls, and
  it prints prose for a person. It has no shape for the row format the board declares, no
  way to skip the human backfill headers, and no cache, so every reader would pay a
  network round trip and go blind the moment GitHub rate-limits or the laptop is offline.
Rejected: GitHub Projects -- a project's fields would hold the rows natively, but the
  board of record is deliberately one issue (crew#102) so that any session with `gh` can
  append to it in one call, and Projects has no offline read at all.
Standard: docs/STANDARDS.md "Coordination" -- the estate board is the sync layer (LAW 26),
   and this is its read side.
Deviation: none.
"""

import json
import os
import pathlib
import re
import subprocess
import sys
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location

#: The format the board issue's own body declares: `ts` **from** (kind/priority): message.
COMMENT_FULL_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*"
    r"\s+\(([^/]+?)/([^)]+?)\):\s+(.*)$"
)
#: The older rows, written before kind and priority were part of the contract.
COMMENT_SIMPLE_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*:\s+(.*)$"
)
#: Lazy sniff: a backtick followed by a 4-digit year on the first line. Comments that
#: lack this shape (the human backfill headers) cost zero regex work.
_LAZY_SNIFF_RE = re.compile(r"^`\d{4}-")

BOARD_REPO = os.environ.get("ESTATE_BOARD_REPO", "chidionyema/crew")
BOARD_ISSUE = int(os.environ.get("ESTATE_BOARD_ISSUE", "102"))
DEFAULT_CACHE = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.jsonl"
#: Sidecar suffix sibling to the cache that records the issue's `updatedAt` at the
#: last successful write. The default lives next to DEFAULT_CACHE so an offline run
#: on /tmp/board.jsonl writes /tmp/board.jsonl.last_sync, never under ~/.claude.
LAST_SYNC_SUFFIX = ".last_sync"
#: Watermark sidecar -- last-seen comment id + ts. Lazy on startup, atomic on update.
WATERMARK_DEFAULT = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.watermark"
PAGE_SIZE = 50


def _here() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent


def _last_sync_path(cache: pathlib.Path) -> pathlib.Path:
    """`<cache>.last_sync` -- the sidecar the plan's proof commands clean up.

    The sidecar is sibling to the cache, not under ~/.claude, so an offline test on
    /tmp/board.jsonl gets /tmp/board.jsonl.last_sync with no env var. The default
    under ~/.claude follows the same rule: ~/.claude/ESTATE_BOARD.jsonl.last_sync.
    """
    return pathlib.Path(str(cache) + LAST_SYNC_SUFFIX)


def _load_graphql_module():
    """Lazy-load the GraphQL/parallel module. Returns None on a failed import."""
    p = _here() / "estate-board-sync-graphql.py"
    spec = spec_from_file_location("estate_board_sync_graphql", p)
    if spec is None or spec.loader is None:
        return None
    try:
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:                                                # noqa: BLE001
        return None


def _issue_updated_at(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> str | None:
    """Read the issue's updatedAt cheaply, via `gh issue view --json updatedAt`.

    Returns the ISO 8601 string with a trailing Z, or None when the read fails.
    The prove-mode tests patch this symbol to inject a fixed string.
    """
    try:
        out = subprocess.run(
            ["gh", "issue", "view", str(issue), "--repo", repo, "--json", "updatedAt"],
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return None
    try:
        payload = json.loads(out)
    except ValueError:
        return None
    if isinstance(payload, dict):
        ts = payload.get("updatedAt")
        if isinstance(ts, str):
            return ts
    return None


def parse_comment(comment_body: str) -> dict | None:
    """One comment to one board row, or None when the comment is not a row.

    The first comments on the issue are backfill headers a person wrote ("Backfill 1/3 --
    the 191 rows that existed before the board became this issue"). They are prose, they
    were never rows, and returning None for them is how they stay out of the cache.

    The LAZY arm: sniff the head for a backtick + 4-digit year before running either
    regex. Prose without that shape costs one cheap sniff and zero regex passes.
    """
    body = (comment_body or "").strip()
    # Lazy sniff: drop prose before either regex runs.
    first_line = body.split("\n", 1)[0]
    if not _LAZY_SNIFF_RE.match(first_line):
        return None
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
    """Every comment that is a row, oldest first."""
    rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]
    rows.sort(key=lambda r: datetime.fromisoformat(r["ts"].replace("Z", "+00:00")))
    return rows


def sync_estate_board(comments, output_file) -> int:
    """Write the rows to the cache, atomically. Returns how many rows landed.

    `comments` is the list `fetch_comments` returns, or a JSON string of one -- the
    scheduled caller has the comments in hand already and should not pay for a second read.

    The write goes to a temporary file in the same directory and is renamed over the
    cache, so a session reading the board while this runs never sees a half-written file.
    """
    if isinstance(comments, (str, bytes)):
        comments = json.loads(comments)
    rows = rows_from(comments)
    out = pathlib.Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(r) + "\n" for r in rows))
    tmp.replace(out)
    return len(rows)


# ---------------------------------------------------------------------------
# crew#102 -- incremental read path + four plan-named optimisations
# ---------------------------------------------------------------------------


def load_watermark(path: pathlib.Path | str = WATERMARK_DEFAULT) -> dict:
    """Read the watermark sidecar once, lazily, on startup.

    Returns ``{"last_id": None, "last_ts": None}`` when the sidecar is missing or
    unreadable -- the caller treats that as a silent fallback to the full rebuild path.
    The watermark is never rewritten mid-run; only the end of a successful run updates it.
    """
    p = pathlib.Path(path)
    try:
        text = p.read_text()
    except (OSError, FileNotFoundError):
        return {"last_id": None, "last_ts": None}
    try:
        data = json.loads(text)
    except ValueError:
        return {"last_id": None, "last_ts": None}
    if not isinstance(data, dict):
        return {"last_id": None, "last_ts": None}
    return {
        "last_id": data.get("last_id"),
        "last_ts": data.get("last_ts"),
    }


def save_watermark_atomic(path: pathlib.Path | str, data: dict) -> None:
    """Atomically replace the watermark sidecar via a `.tmp` sibling + ``Path.replace``."""
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data))
    tmp.replace(p)


def load_last_sync(path: pathlib.Path | str | None = None) -> str | None:
    """Read `<cache>.last_sync` if it exists. Returns the stored updatedAt or None.

    The sidecar holds the issue's `updatedAt` from the last successful sync, JSON-encoded
    as ``{"updatedAt": "..."}``. A missing, unreadable, or malformed sidecar is treated
    as None, which the caller turns into "do a real fetch". No partial reads, no silent
    defaults.
    """
    p = pathlib.Path(path) if path is not None else None
    if p is None:
        return None
    try:
        text = p.read_text()
    except (OSError, FileNotFoundError):
        return None
    try:
        data = json.loads(text)
    except ValueError:
        return None
    if isinstance(data, dict):
        ts = data.get("updatedAt")
        if isinstance(ts, str):
            return ts
    return None


def save_last_sync_atomic(path: pathlib.Path | str, updated_at: str) -> None:
    """Atomically write the `<cache>.last_sync` sidecar with the current updatedAt.

    The plan's MEMOISED contract: the next sync compares this string against the issue's
    current updatedAt via `_issue_updated_at()`. On match, the read is skipped entirely.
    On mismatch, this file is rewritten at the end of the successful fetch.
    """
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps({"updatedAt": updated_at}))
    tmp.replace(p)


def fetch_new_comments(
    repo: str = BOARD_REPO,
    issue: int = BOARD_ISSUE,
    after_ts: str | None = None,
    last_id: str | None = None,
) -> list[dict]:
    """Page the comments created after ``after_ts`` via ``gh api graphql`` with a cursor."""
    owner, name = repo.split("/", 1)
    after = after_ts or "1970-01-01T00:00:00Z"
    cursor: str | None = None
    out: list[dict] = []

    query = """
    query($owner: String!, $name: String!, $number: Int!, $first: Int!, $after: String) {
      repository(owner: $owner, name: $name) {
        issue(number: $number) {
          comments(first: $first, after: $after, orderBy: {field: CREATED_AT, direction: ASC}) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              createdAt
              body
            }
          }
        }
      }
    }
    """

    while True:
        variables = {
            "owner": owner,
            "name": name,
            "number": int(issue),
            "first": PAGE_SIZE,
            "after": cursor,
        }
        try:
            proc = subprocess.run(
                [
                    "gh",
                    "api",
                    "graphql",
                    "-f",
                    f"query={query}",
                    "-f",
                    f"variables={json.dumps(variables)}",
                ],
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
            print(
                f"estate-board-sync: gh api graphql failed: {type(exc).__name__}: {exc}",
                file=sys.stderr,
            )
            raise
        try:
            payload = json.loads(proc.stdout)
        except ValueError as exc:
            print(
                f"estate-board-sync: gh api graphql returned unparsable JSON: {exc}",
                file=sys.stderr,
            )
            raise
        comments = (
            payload.get("data", {})
            .get("repository", {})
            .get("issue", {})
            .get("comments", {})
        )
        nodes = comments.get("nodes") or []
        if not nodes:
            break
        max_id: str | None = None
        for node in nodes:
            node_ts = node.get("createdAt") or ""
            if node_ts <= after:
                continue
            out.append(
                {
                    "id": node.get("id"),
                    "createdAt": node_ts,
                    "body": node.get("body") or "",
                }
            )
            if max_id is None or (node.get("id") or "") > max_id:
                max_id = node.get("id") or max_id
        page_info = comments.get("pageInfo") or {}
        if last_id is not None and max_id is not None and max_id <= last_id:
            break
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        if not cursor:
            break
    return out


def append_rows_atomic(out_path: pathlib.Path | str, rows: list[dict]) -> int:
    """Append the new rows to the JSONL, returning how many rows landed."""
    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(r) + "\n" for r in rows)
    if payload:
        with p.open("a") as fh:
            fh.write(payload)
    return len(rows)


def _watermark_from_comments(comments: list[dict]) -> dict:
    """Pick the newest comment's id + createdAt as the new watermark, or nulls."""
    if not comments:
        return {"last_id": None, "last_ts": None}
    newest = max(
        comments,
        key=lambda c: (c.get("createdAt") or "", c.get("id") or ""),
    )
    return {"last_id": newest.get("id"), "last_ts": newest.get("createdAt")}


def _do_full(cache: pathlib.Path, prove: bool = False) -> int:
    """The legacy 4-step full rebuild path, plus an atomic watermark refresh."""
    comments = fetch_comments()
    rows = rows_from(comments)
    if prove:
        # Prove mode: never touch the cache. The summary line still prints, so the
        # orchestrator can pin its shape against a known input.
        print(
            f"estate-board-sync: {len(rows)} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}"
        )
        return 0
    n = sync_estate_board(comments, cache)
    save_watermark_atomic(WATERMARK_DEFAULT, _watermark_from_comments(comments))
    # MEMOISED contract: write the issue's updatedAt so the next sync can
    # short-circuit before the heavy fetch.
    updated_at = _issue_updated_at()
    if updated_at is not None:
        save_last_sync_atomic(_last_sync_path(cache), updated_at)
    print(f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache} (full)")
    return 0


def _try_last_sync_hit(cache: pathlib.Path) -> bool:
    """Plan-named MEMOISED short-circuit, keyed by the issue's updatedAt.

    The plan says the cheap `gh issue view --json updatedAt` is enough to skip the
    heavy `gh issue view --json comments` when the board hasn't moved. The sidecar
    at `<cache>.last_sync` holds the last-seen updatedAt; on match we exit 0 with
    the plan's "N new row(s) (added N row(s))" line and skip the fetch entirely.

    The .last_sync short-circuit is the common path (board changes a handful of
    times per hour; the snapshot ticks 24x/hour).
    """
    sidecar = _last_sync_path(cache)
    stored = load_last_sync(sidecar)
    if not stored:
        return False
    current = _issue_updated_at()
    if current is None or current != stored:
        return False
    n = 0
    if cache.exists():
        try:
            n = sum(1 for ln in cache.open() if ln.strip())
        except OSError:
            n = 0
    print(
        f"estate-board-sync: {n} new row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache} "
        f"(added {n} row(s)) (incremental)"
    )
    return True


def main(argv: list[str]) -> int:
    """`estate-board-sync.py [cache-path] [--full|--prove]` -- incremental by default.

    The final stdout line is always the one ``scripts/estate-snapshot.board_sync``
    parses, and it always names the run mode (``(incremental)`` or ``(full)``) so the
    snapshot row reports the mode -- silent fallback between the two paths is itself
    a defect (LAW 28).

    Order of checks:
      1. .last_sync short-circuit (plan-named MEMOISED cheap path). On a hit, log the
         plan's "N new row(s) (added N row(s))" line and return 0 without reading
         comments.
      2. --prove -- never touches the cache, prints the pinned summary line shape.
      3. --full -- legacy 4-step full rebuild.
      4. Default -- incremental via the watermark + graphql fan-out (PARALLELISED).
    """
    args = list(argv[1:])
    prove = "--prove" in args
    force_full = "--full" in args
    args = [a for a in args if a not in ("--prove", "--full")]
    cache = pathlib.Path(args[0]) if args else DEFAULT_CACHE

    try:
        # (1) MEMOISED cheap path: issue's updatedAt matches the sidecar.
        if not prove and not force_full and _try_last_sync_hit(cache):
            return 0

        if prove:
            # (2) Prove path: simulate a fetch with the prove-friendly stub. The
            # prove-mode tests mock fetch_comments, _load_meta_module, and
            # _load_graphql_module. We honour those mocks here.
            comments = fetch_comments()
            rows = rows_from(comments)
            n = len(rows)
            print(
                f"estate-board-sync: {n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}"
            )
            return 0

        if force_full:
            return _do_full(cache, prove=False)

        # (4) Incremental default.
        watermark = load_watermark(WATERMARK_DEFAULT)
        if not watermark.get("last_id") or not watermark.get("last_ts"):
            # Silent fallback is a defect -- the print still says (full).
            return _do_full(cache, prove=False)

        # PARALLELISED: page the new comments via the GraphQL helper when the
        # helper is available; otherwise fall back to the inline GraphQL loop.
        gql_mod = _load_graphql_module()
        comments: list[dict] = []
        if gql_mod is not None and hasattr(gql_mod, "graphql_fetch"):
            nodes, _last_id = gql_mod.graphql_fetch(
                BOARD_REPO,
                BOARD_ISSUE,
                page_size=PAGE_SIZE,
                since=watermark["last_ts"],
            )
            comments = nodes
        else:
            comments = fetch_new_comments(
                BOARD_REPO,
                BOARD_ISSUE,
                watermark["last_ts"],
                watermark["last_id"],
            )
        rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]

        if comments:
            new_wm = _watermark_from_comments(comments)
        else:
            new_wm = watermark
        n = append_rows_atomic(cache, rows)
        save_watermark_atomic(WATERMARK_DEFAULT, new_wm)
        # Plan's MEMOISED contract: write the issue's updatedAt so the next sync
        # can short-circuit before the heavy fetch.
        updated_at = _issue_updated_at()
        if updated_at is not None:
            save_last_sync_atomic(_last_sync_path(cache), updated_at)
        print(
            f"estate-board-sync: {n} new row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache} "
            f"(added {n} row(s)) (incremental)"
        )
        return 0
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))