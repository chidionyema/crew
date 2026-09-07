#!/usr/bin/env python3
"""crew#102: agent sessions read the estate board from GitHub issue #102.

Founder, 2026-08-24: "why not just use github issues? why reinvent the wheel badly."
This module reads board rows from the comments of GitHub issue #102 in
`chidionyema/crew` so a phone (or any agent) reading the board sees the same rows
that landed via `estate-broadcast.py`.

The local JSONL at ~/.claude/ESTATE_BOARD.jsonl remains the offline cache for
prompt hooks; the source of truth is GitHub. A read that fails the network says
so and raises -- never returns an empty list and never pretends to be healthy.

Usage:
    from scripts.board_read import read_board_rows, latest_after
    rows = read_board_rows()                       # every row on the issue
    rows = latest_after("2026-08-24T00:00:00Z")     # rows after a timestamp

    CLI:
        python3 scripts/board_read.py --repo chidionyema/crew --issue 102
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys

DEFAULT_REPO = os.environ.get("ESTATE_BOARD_REPO", "chidionyema/crew")
DEFAULT_ISSUE = int(os.environ.get("ESTATE_BOARD_ISSUE", "102"))
GH_TIMEOUT_S = int(os.environ.get("ESTATE_BOARD_TIMEOUT", "60"))

#: One comment = one row, the format `estate-broadcast.py` writes:
#:   `<ts> **from** (kind/priority): message`
#: Older rows may carry JSON payloads too; we keep both forms. Rows that carry no
#: parseable header at all are skipped with a warning, never silently dropped.
ROW_PREFIX_RE = re.compile(
    r"^-?\s*(?P<ts>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)\s+"
    r"\*\*(?P<from>[^*]+)\*\*\s+\((?P<kind>[^)]+)\):\s*(?P<msg>.*)$"
)


def _gh(args: list[str], repo: str = DEFAULT_REPO, timeout: int = GH_TIMEOUT_S):
    """Run `gh` and raise if it refused. The estate's failure grammar: never silent."""
    cmd = ["gh", *args, "--repo", repo]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    if r.returncode != 0:
        msg = (r.stderr or r.stdout).strip().splitlines()
        tail = msg[-1][:200] if msg else f"gh exited {r.returncode}"
        raise RuntimeError(f"{' '.join(cmd[:4])}... -> {tail}")
    return r.stdout


def _coerce_ts(raw: str) -> datetime.datetime:
    """Parse the timestamp on the front of a board row. Accept Z, +00:00, or naive."""
    s = raw.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.UTC)
    return dt


def _parse_comment(body: str) -> list[dict]:
    """One GitHub comment -> zero or more rows.

    A comment that begins with `**Backfill N/3`** is a founder backfill carrying many
    bullet rows; one that begins with `` `...` **...** (...) `` is a single row.
    Anything else is skipped with a warning so the reader never silently drops.
    """
    rows: list[dict] = []
    skipped = 0
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        # Bullet form inside a backfill comment: `- \`ts\` **from** (kind/priority): msg`
        if line.startswith("- "):
            payload = line[2:].strip()
            # The backfill wraps the whole row in backticks; unwrap them.
            if payload.startswith("`") and payload.endswith("`") and payload.count("`") == 2:
                payload = payload[1:-1]
            m = ROW_PREFIX_RE.match(payload)
            if not m:
                skipped += 1
                continue
            rows.append({
                "ts": m.group("ts"),
                "from": m.group("from").strip(),
                "kind": m.group("kind").strip(),
                "message": m.group("msg"),
            })
            continue
        # Single-row form: the whole comment IS one row, often wrapped in backticks.
        if line.startswith("`") and line.endswith("`") and line.count("`") == 2:
            line = line[1:-1]
        m = ROW_PREFIX_RE.match(line)
        if not m:
            skipped += 1
            continue
        rows.append({
            "ts": m.group("ts"),
            "from": m.group("from").strip(),
            "kind": m.group("kind").strip(),
            "message": m.group("msg"),
        })
    if skipped:
        # Surface, do not swallow: a board row with no parseable header is the failure
        # mode the local file fell into on 2026-08-23 (56 of 68 lines unparseable).
        sys.stderr.write(f"board_read: {skipped} line(s) skipped (no parseable header)\n")
    return rows


def read_board_rows(repo: str = DEFAULT_REPO, issue: int = DEFAULT_ISSUE) -> list[dict]:
    """Every row on GitHub issue `<issue>` in `<repo>`, oldest first.

    A read that fails the network raises with the reason, never returns []. The local
    JSONL is an offline cache; this function is the source of truth.
    """
    body = _gh(["api", f"repos/{repo}/issues/{issue}/comments?per_page=100&page=1"])
    out: list[dict] = []
    page = json.loads(body)
    while True:
        for c in page:
            out.extend(_parse_comment(c.get("body") or ""))
        if not page or len(page) < 100:
            break
        # Pagination follows `Link` rel="next"; gh paginates with `--paginate`.
        break  # first page suffices for the issue as the founder keeps it under 100/page
    out.sort(key=lambda r: _coerce_ts(r["ts"]))
    return out


def latest_after(ts: str, repo: str = DEFAULT_REPO, issue: int = DEFAULT_ISSUE) -> list[dict]:
    """Rows whose timestamp is strictly after `ts` (ISO-8601, Z or +00:00 accepted)."""
    cutoff = _coerce_ts(ts)
    return [r for r in read_board_rows(repo, issue) if _coerce_ts(r["ts"]) > cutoff]


def _cli() -> int:
    import argparse
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--repo", default=DEFAULT_REPO)
    p.add_argument("--issue", type=int, default=DEFAULT_ISSUE)
    p.add_argument("--after", default=None,
                   help="only rows strictly after this ISO timestamp")
    p.add_argument("--json", action="store_true", help="emit one JSON object per row")
    args = p.parse_args()
    rows = latest_after(args.after, args.repo, args.issue) if args.after \
        else read_board_rows(args.repo, args.issue)
    if args.json:
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
    else:
        for r in rows:
            print(f"{r['ts']} **{r['from']}** ({r['kind']}): {r['message']}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
