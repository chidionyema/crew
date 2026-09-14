#!/usr/bin/env python3
"""estate-broadcast.py — the writer half of the board cutover.

The board of record is the GitHub issue printed by `bin/board-target` (default
chidionyema/crew#102, this file's source-of-truth). Every broadcast lands
there as a comment in the form `ts **from** (kind/priority): message`. The
local JSONL at ESTATE_BOARD_JSONL is only the offline cache the prompt hooks
read; the dead-letter JSONL at BOARD_DEAD_LETTER is the loud-failure channel.

This script is the one writer. It runs without third-party deps, posts one row,
falls back to the cache when the GitHub API is unreachable, dead-letters when
the cache is also unreachable, and warns loudly on stderr — never silently
drops a row.

    python3 bin/estate-broadcast.py --from session --kind note --priority info --message "..."
    python3 bin/estate-broadcast.py --print-target
    python3 bin/estate-broadcast.py --dry-run --from s --kind k --priority p --message "m"

The --print-target form prints `chidionyema/crew#102` and exits 0; it costs no
network call and is what tests and docs use to pin the target. The --dry-run
form prints the row that would be written and exits 0 — same effect for
documenting what gets sent without spending a rate-limit budget.

Refused: any option that would change the row format, batch rows, or retry on
failure — a board whose writer can drift from the issue body is the failure
mode the cutover removed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
from typing import Iterable

#: The format the issue body declares: `\`ts\` **from** (kind/priority): message`.
#: A drift here is a defect (crew#101, crew#102), not a feature — the regexes that
#: parse the board on the read side pin this string for the same reason.
DEFAULT_BOARD_REPO = "chidionyema/crew"
DEFAULT_BOARD_ISSUE = 102
DEFAULT_CACHE = pathlib.Path.home() / ".claude" / "ESTATE_BOARD.jsonl"
DEFAULT_DEAD_LETTER = pathlib.Path.home() / ".claude" / "state" / "board-deadletter.jsonl"


def _target(repo: str | None = None, issue: int | None = None) -> tuple[str, int]:
    """Read the board target from env or use the crew-default. Args allow override for tests."""
    return (
        os.environ.get("BOARD_REPO", repo or DEFAULT_BOARD_REPO),
        int(os.environ.get("BOARD_ISSUE", str(issue if issue is not None else DEFAULT_BOARD_ISSUE))),
    )


def _cache_path() -> pathlib.Path:
    return pathlib.Path(os.environ.get("ESTATE_BOARD_JSONL", str(DEFAULT_CACHE)))


def _dead_letter_path() -> pathlib.Path:
    return pathlib.Path(os.environ.get("BOARD_DEAD_LETTER", str(DEFAULT_DEAD_LETTER)))


def _now_utc() -> str:
    """ISO-8601 UTC, second precision: `2026-08-23T21:41:15Z`. The 191 backfilled rows
    on crew#102 are second-precision; fractions of a second are present on a few
    but they don't decide ordering — the cache/board reader sorts by full ISO parse.
    """
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _row(from_: str, kind: str, priority: str, message: str, ts: str | None = None) -> dict[str, str]:
    """The one row, rendered as a dict. All three sinks (comment body, cache
    JSONL, dead-letter JSONL) read this dict back, so the byte-identical
    requirement (DoD 7) is enforced by construction."""
    return {
        "ts": ts or _now_utc(),
        "from": from_,
        "kind": kind,
        "priority": priority,
        "message": message,
    }


def _render_comment(row: dict[str, str]) -> str:
    return f"`{row['ts']}` **{row['from']}** ({row['kind']}/{row['priority']}): {row['message']}"


def _render_jsonl(row: dict[str, str]) -> str:
    """One JSON object per line, no trailing newline — concat-safe."""
    return json.dumps(row, ensure_ascii=False, sort_keys=True)


#: Subprocess lookups for `gh`. The script shells to the same `gh` binary the rest
#: of the repo uses, so GH auth stays in one place. The two helpers are split so
#: tests can monkey-patch them without touching the rest of the module.
def _gh_env() -> dict[str, str]:
    env = os.environ.copy()
    # Belt and braces: GH_TOKEN is what `gh` uses. Setting "" is a way to disable
    # it for tests, which is cleaner than `gh logout`.
    if os.environ.get("ESTATE_BROADCAST_NO_GH") == "1":
        env["GH_TOKEN"] = ""
    return env


def _gh(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=_gh_env(),
        check=False,
    )


def _post_comment(repo: str, issue: int, body: str) -> tuple[bool, str]:
    """Try the GitHub write. Returns (ok, hint). hint is the comment URL on success,
    or a one-line reason on failure. Never raises: a board that blows up the writer
    is a board nobody trusts (LAW 28)."""
    proc = _gh(
        "issue", "comment", str(issue),
        "--repo", repo,
        "--body", body,
    )
    if proc.returncode == 0:
        # `gh issue comment` prints the new comment's URL on stdout. If it does
        # not (older `gh` builds), an empty string is returned and the caller
        # still treats the call as successful.
        return True, proc.stdout.strip()
    err = (proc.stderr or proc.stdout or "gh exited non-zero").strip().splitlines()
    reason = err[-1] if err else f"gh exited {proc.returncode}"
    return False, reason[:160]


def _append_jsonl(path: pathlib.Path, line: str) -> tuple[bool, str]:
    """Append one JSON line to the file. Atomicity is per line (one write), which is
    what the reader expects: it never sees a half-written line because the line is
    written in a single syscall. Creates parents if missing."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        return True, str(path)
    except OSError as exc:
        return False, f"{type(exc).__name__}: {exc}"[:160]


def broadcast(from_: str, kind: str, priority: str, message: str,
              *, repo: str | None = None, issue: int | None = None,
              cache: pathlib.Path | None = None, dead_letter: pathlib.Path | None = None,
              now: dt.datetime | None = None) -> int:
    """The one writer. Returns the process exit code (0 on board or cache, non-zero
    on dead-letter)."""
    if not from_ or not kind or not priority or not message:
        print("estate-broadcast: --from, --kind, --priority, --message are all required",
              file=sys.stderr)
        return 2
    board_repo, board_issue = _target(repo, issue)
    cache = cache or _cache_path()
    dead_letter = dead_letter or _dead_letter_path()
    ts = (now or dt.datetime.now(dt.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = _row(from_, kind, priority, message, ts=ts)
    comment = _render_comment(row)

    # 1) GitHub first. A successful post is the only path that prints the
    # comment URL — the cache/board reader never has to know we failed.
    ok, hint = _post_comment(board_repo, board_issue, comment)
    if ok:
        print(hint or f"posted to {board_repo}#{board_issue}")
        return 0

    # 2) Cache fallback. A failed GitHub write still exits 0 because the row
    # landed somewhere readers can find it (LAW 31: dead and unreported must
    # never look the same).
    jsonl_line = _render_jsonl(row)
    ok, hint = _append_jsonl(cache, jsonl_line)
    if ok:
        print(f"cached to {hint} (GitHub unreachable: {hint})", file=sys.stderr)
        return 0

    # 3) Dead-letter. Loud warning, non-zero exit, never silent.
    ok, dl_hint = _append_jsonl(dead_letter, jsonl_line)
    reason = f"gh failed: {hint}; cache failed: {hint}"
    if ok:
        print(f"WARNING: estate-broadcast dead-lettered row ts={ts} reason={reason}", file=sys.stderr)
    else:
        # The dead-letter file itself is unwritable. The board cannot reach the
        # reader; print to stderr loud enough that nothing ignores it.
        print(f"WARNING: estate-broadcast DEAD-LETTER WRITE FAILED ts={ts} reason={reason} "
              f"dead_letter_error={dl_hint}", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="estate-broadcast",
                                description="Write one row to the estate board (chidionyema/crew#102).")
    p.add_argument("--from", dest="from_", required=False, help="session/actor name (bold in the comment)")
    p.add_argument("--kind", required=False, help="row kind (e.g. note, fire, alert, claim)")
    p.add_argument("--priority", required=False, help="row priority (e.g. info, p0, p1)")
    p.add_argument("--message", required=False, help="row body")
    p.add_argument("--print-target", action="store_true",
                   help="print `chidionyema/crew#102` and exit (no network)")
    p.add_argument("--dry-run", action="store_true",
                   help="print what would be written and exit (no network)")
    args = p.parse_args(argv)

    if args.print_target:
        repo, issue = _target()
        print(f"{repo}#{issue}")
        return 0

    if args.dry_run:
        if not (args.from_ and args.kind and args.priority and args.message):
            print("estate-broadcast --dry-run: --from, --kind, --priority, --message are all required",
                  file=sys.stderr)
            return 2
        row = _row(args.from_, args.kind, args.priority, args.message)
        print(_render_comment(row))
        print(_render_jsonl(row))
        return 0

    return broadcast(args.from_, args.kind, args.priority, args.message)


if __name__ == "__main__":
    raise SystemExit(main())
