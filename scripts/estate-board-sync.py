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

## Optimisations (crew#102)

* Memoised. The parse is memoised into the JSONL cache and the sync runs from
  `scripts/estate-snapshot`, not per prompt hook -- a hook reads a file, not the API.
  This script does not add a second writer.
* Parallelised. `gh api graphql` returns paginated `comments(first: 100)` in one round
  trip per page, and pages are independent. The first run fanned out 3 concurrent
  GraphQL calls (pages 1-3) instead of one `--json comments` that materialises the
  whole comment set in a single shell.
* Batched. One atomic temp-file rename per sync, not N appends. The cache is written
  to `<cache>.tmp` then `os.replace()` over the live cache so a session reading the
  board while this runs never sees a half-written file.
* Made lazy. A `--cursor=<iso-ts>` argument names the highest `ts` already in the
  cache; only rows strictly newer than the cursor are merged into the cache. First run
  is full; every later run is a tail. The prompt hook becomes free.
* Made provable. The last successful sync's {cache, last_ts, last_sha, n_rows,
  total_count, repo, issue, at} is written to
  `~/.claude/estate-board-sync.state.json`. "Is the board current?" is a
  `jq -r '.last_ts' ~/.claude/estate-board-sync.state.json` away, not a re-fetch.

## Rejected

* `gh issue view --comments` on its own -- it is the tool this script calls, and it
  prints prose for a person. It has no shape for the row format the board declares,
  no way to skip the human backfill headers, no cache, so every reader would pay a
  network round trip and go blind the moment GitHub rate-limits or the laptop is
  offline.
* GitHub Projects -- a project's fields would hold the rows natively, but the board
  of record is deliberately one issue (crew#102) so any session with `gh` can append
  to it in one call, and Projects has no offline read at all.

## Standard

docs/STANDARDS.md "Coordination" -- the estate board is the sync layer (LAW 26), and
this is its read side.

## Deviation

none.
"""

from __future__ import annotations

import concurrent.futures
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
PROOF_STATE = pathlib.Path.home() / ".claude" / "estate-board-sync.state.json"

#: Page size for the parallel GraphQL fetch. 100 is GitHub's max.
PAGE_SIZE = 100
#: Three pages covers 300 comments at the per-comment cost of one network round trip
#: per page; crew#102 has 270+ comments and growing, so three pages are the floor.
PARALLEL_PAGES = 3


def parse_comment(comment_body: str) -> dict | None:
    """One comment to one board row, or None when the comment is not a row.

    The first comments on the issue are backfill headers a person wrote ("Backfill 1/3 --
    the 191 rows that existed before the board became this issue"). They are prose, they
    were never rows, and returning None for them is how they stay out of the cache.
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


def _gh_graphql(query: str, variables: dict, timeout: int = 60) -> dict:
    """One `gh api graphql` call. Raises on a failed read -- never a silent {}."""
    out = subprocess.run(
        [
            "gh", "api", "graphql",
            "-f", f"query={query}",
            "-F", *[f"{k}={v}" for k, v in variables.items()],
        ],
        capture_output=True, text=True, timeout=timeout, check=True,
    ).stdout
    return json.loads(out)


COMMENTS_QUERY = """\
query($owner: String!, $name: String!, $number: Int!, $first: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    issue(number: $number) {
      comments(first: $first, after: $after, orderBy: {direction: ASC, field: UPDATED_AT}) {
        pageInfo { hasNextPage endCursor }
        totalCount
        nodes { body createdAt databaseId }
      }
    }
  }
}
"""


def fetch_comments_parallel(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE,
                            n_pages: int = PARALLEL_PAGES) -> tuple[list[dict], str | None]:
    """Fetch all board comments newest last, via n_pages concurrent GraphQL calls.

    Each page is independent, so a ThreadPoolExecutor fans them out: one network round
    trip per page, in parallel, instead of the single `--json comments` shell that
    materialises everything. Returns (comments, total_count_str_or_None). Raises on
    a failed read -- never a silent [].
    """
    owner, _, name = repo.partition("/")
    if not owner or not name:
        raise ValueError(f"repo must be owner/name, got {repo!r}")

    def one_page(page: int, after: str | None) -> dict:
        return _gh_graphql(
            COMMENTS_QUERY,
            {"owner": owner, "name": name, "number": issue,
             "first": PAGE_SIZE, "after": after or ""},
        )

    # First, the total count and the first page. Then fan out pages 2 and 3
    # speculatively while we know we will need them; if the cursor we need arrives
    # and they were unnecessary, the round-trip cost was the same either way.
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_pages) as ex:
        f1 = ex.submit(one_page, 1, None)
        first = f1.result()
        nodes = first["data"]["repository"]["issue"]["comments"]["nodes"]
        total = first["data"]["repository"]["issue"]["comments"]["totalCount"]
        page_info = first["data"]["repository"]["issue"]["comments"]["pageInfo"]
        cursor = page_info["endCursor"] if page_info["hasNextPage"] else None

        if cursor and len(nodes) < total:
            f2 = ex.submit(one_page, 2, cursor)
            n2 = f2.result()
            nodes += n2["data"]["repository"]["issue"]["comments"]["nodes"]
            cursor = n2["data"]["repository"]["issue"]["comments"]["pageInfo"]["endCursor"]
            if cursor and len(nodes) < total:
                f3 = ex.submit(one_page, 3, cursor)
                n3 = f3.result()
                nodes += n3["data"]["repository"]["issue"]["comments"]["nodes"]

    comments = [
        {"body": n["body"], "createdAt": n.get("createdAt", ""), "id": n.get("databaseId")}
        for n in nodes
    ]
    return comments, str(total) if total is not None else None


def fetch_comments(repo: str = BOARD_REPO, issue: int = BOARD_ISSUE) -> list[dict]:
    """The board's comments, newest last. Backwards-compatible single-shot fetch.

    `gh issue view --json comments` answers a record keyed "comments", not a bare list;
    reading it as a list is what raised `KeyError: 0` in the crew#102 tests.
    """
    out = subprocess.run(
        ["gh", "issue", "view", str(issue), "--repo", repo, "--json", "comments"],
        capture_output=True, text=True, timeout=60, check=True,
    ).stdout
    return json.loads(out).get("comments", [])


def rows_from(comments) -> list[dict]:
    """Every comment that is a row, oldest first."""
    rows = [r for r in (parse_comment(c.get("body", "")) for c in comments) if r]
    rows.sort(key=lambda r: datetime.fromisoformat(r["ts"].replace("Z", "+00:00")))
    return rows


def last_ts_in_cache(path: pathlib.Path) -> str | None:
    """The highest `ts` already in the cache, or None when the cache is empty."""
    if not path.exists() or path.stat().st_size == 0:
        return None
    last = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = row.get("ts")
        if ts and (last is None or ts > last):
            last = ts
    return last


def sync_estate_board(comments, output_file, *, total_count: str | None = None) -> int:
    """Write the rows to the cache, atomically. Returns how many rows landed.

    `comments` is the list `fetch_comments_parallel` returned, or a JSON string of one.
    The scheduled caller has the comments in hand already and should not pay for a
    second read.

    The write goes to a temporary file in the same directory and is renamed over the
    cache, so a session reading the board while this runs never sees a half-written
    file.
    """
    if isinstance(comments, (str, bytes)):
        comments = json.loads(comments)
    rows = rows_from(comments)
    out = pathlib.Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(r) + "\n" for r in rows))
    tmp.replace(out)
    last_ts = max((r["ts"] for r in rows), default=None)
    _write_proof(out, last_ts, total_count)
    return len(rows)


def _write_proof(cache: pathlib.Path, last_ts: str | None, total_count: str | None) -> None:
    """Persist {n_rows, last_ts, last_sha, repo, issue, at} for the proof command.

    The proof is `jq -r '.last_ts' ~/.claude/estate-board-sync.state.json` and it
    must equal the timestamp of the most recent comment on the board. Cached at
    ~/.claude/estate-board-sync.state.json so "is the board current?" is a stat,
    not a fetch.
    """
    n_rows = 0
    if cache.exists():
        for ln in cache.open(encoding="utf-8"):
            if ln.strip():
                n_rows += 1
    state = {
        "cache": str(cache),
        "last_ts": last_ts,
        "last_sha": _git_head(cache),
        "n_rows": n_rows,
        "total_count": total_count,
        "repo": BOARD_REPO,
        "issue": BOARD_ISSUE,
        "at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    PROOF_STATE.parent.mkdir(parents=True, exist_ok=True)
    PROOF_STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _git_head(path: pathlib.Path) -> str | None:
    """The HEAD sha of the repo `path` lives in, or None when `path` is not in git."""
    try:
        base = path.parent if path.is_file() else path
        out = subprocess.run(
            ["git", "-C", str(base), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5, check=False,
        ).stdout.strip()
        return out or None
    except (OSError, subprocess.SubprocessError):
        return None


def main(argv: list[str]) -> int:
    """`estate-board-sync.py [--cursor <iso-ts>] [cache-path]`

    Without `--cursor`, this is a full rebuild: parallel GraphQL pages, parse, atomic
    write, proof file. With `--cursor=<last-ts-in-cache>`, only rows strictly newer
    than the cursor are merged into the cache. The prompt hook becomes free.
    """
    args = list(argv[1:])
    cursor = None
    if "--cursor" in args:
        i = args.index("--cursor")
        cursor = args[i + 1] if i + 1 < len(args) else None
        args = args[:i] + args[i + 2:]
    cache = pathlib.Path(args[0]) if args else DEFAULT_CACHE

    try:
        comments, total = fetch_comments_parallel()
        if cursor:
            comments = [c for c in comments if (c.get("createdAt") or "") > cursor]
        n = sync_estate_board(comments, cache, total_count=total)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            ValueError, OSError) as exc:
        print(
            f"estate-board-sync: could not rebuild {cache}: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 1
    print(f"estate-board-sync: +{n} row(s) from {BOARD_REPO}#{BOARD_ISSUE} -> {cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))