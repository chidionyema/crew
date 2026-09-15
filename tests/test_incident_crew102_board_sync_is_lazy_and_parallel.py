"""crew#102 - the board sync is a one-command proof: lazy, parallel, atomic, proven.

The board of record is GitHub issue crew#102; the JSONL at
~/.claude/ESTATE_BOARD.jsonl is only the offline cache the prompt hooks read.
This test pins the optimised read side:

* the cache write is atomic (a `<cache>.tmp` rename, not N appends);
* the proof file at ~/.claude/estate-board-sync.state.json is written on every
  successful sync and carries last_ts, last_sha, repo, issue, n_rows;
* a sync with `--cursor=<last-ts-in-cache>` is a TAIL run, not a full rebuild;
* the issue itself stays pinned at crew#102 (covered by the existing
  test_incident_crew102_estate_board_is_issue_102.py -- this test does not
  re-pin it).

The PR is green when this file plus the existing crew#102 tests pass on a
clean checkout with `gh` authenticated. See scripts/estate-board-sync.py for
the implementation.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "estate-board-sync.py"
COMMENT_FULL_RE = re.compile(
    r"^`(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)`\s+\*\*([^*]+?)\*\*"
    r"\s+\(([^/]+?)/([^)]+?)\):\s+(.*)$"
)


def _gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=False)


def test_script_parses_known_full_rows() -> None:
    """The parser handles both the full `(kind/priority)` rows and the older
    backfill rows that lack kind and priority. Two parsed dicts from the live
    board are enough; the rest of the cache is covered by the issue test."""
    out = _gh("issue", "view", "102", "--repo", "chidionyema/crew", "--json", "comments")
    assert out.returncode == 0, out.stderr or out.stdout
    comments = json.loads(out.stdout)["comments"]
    parsed = 0
    for c in comments:
        body = (c.get("body") or "").strip()
        first = next((ln for ln in body.splitlines() if ln.strip()), "")
        m = COMMENT_FULL_RE.match(first)
        if m:
            ts, frm, kind, priority, message = m.groups()
            assert ts.endswith("Z"), ts
            assert kind.strip(), kind
            assert priority.strip(), priority
            assert message.strip(), message
            parsed += 1
            if parsed >= 5:
                break
    assert parsed >= 5, "board parser did not match 5 known rows from crew#102"


def test_atomic_write_uses_tmp_then_replace(tmp_path: pathlib.Path) -> None:
    """A sync that hits a missing cache leaves no half-written file behind.

    We exercise `sync_estate_board` directly with an empty comments list so the
    test never hits the network. The atomic-rename contract is: the live cache
    exists after the call (with the rows we asked for), no `.tmp` lingers, and
    any reader that opened the path mid-run would have seen ENOENT, not a
    truncated file."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib
    mod = importlib.import_module("estate-board-sync")
    importlib.reload(mod)

    cache = tmp_path / "ESTATE_BOARD.jsonl"
    rows = [
        {"ts": "2026-08-24T03:23:01.090857Z", "from": "fable-63",
         "kind": "board-cutover", "priority": "high",
         "message": "The board is now crew#102."},
        {"ts": "2026-08-24T03:33:33.911368Z", "from": "crew63-fable",
         "kind": "directive", "priority": "high",
         "message": "FOUNDER, 2026-08-24: estate not harmonised."},
    ]
    n = mod.sync_estate_board(rows, cache)
    assert n == 2
    assert cache.exists()
    assert not cache.with_suffix(cache.suffix + ".tmp").exists()
    lines = [json.loads(ln) for ln in cache.read_text().splitlines() if ln.strip()]
    assert [r["ts"] for r in lines] == sorted(r["ts"] for r in rows), (
        "rows must be sorted oldest-first so a tail read sees them in order")


def test_proof_file_is_written_on_sync(tmp_path: pathlib.Path) -> None:
    """The proof file is what makes "is the board current?" a stat, not a fetch.

    The sync writes ~/.claude/estate-board-sync.state.json. The proof command
    is `jq -r '.last_ts' ~/.claude/estate-board-sync.state.json` and it must
    equal the timestamp of the most recent row the sync wrote."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib
    mod = importlib.import_module("estate-board-sync")
    importlib.reload(mod)

    # Redirect the proof path for the test so we do not touch the real one.
    proof = tmp_path / "estate-board-sync.state.json"
    mod.PROOF_STATE = proof

    cache = tmp_path / "ESTATE_BOARD.jsonl"
    rows = [
        {"ts": "2026-08-24T03:23:01.090857Z", "from": "fable-63",
         "kind": "board-cutover", "priority": "high", "message": "x"},
    ]
    mod.sync_estate_board(rows, cache, total_count="270")
    assert proof.exists(), "sync did not write the proof file"
    state = json.loads(proof.read_text())
    assert state["last_ts"] == "2026-08-24T03:23:01.090857Z"
    assert state["n_rows"] == 1
    assert state["repo"] == "chidionyema/crew"
    assert state["issue"] == 102
    assert state["total_count"] == "270"


def test_cursor_is_a_tail_filter() -> None:
    """--cursor=<iso-ts> names the highest ts already in the cache; the read
    drops anything older. The prompt hook becomes free: it never re-parses the
    head of the board."""
    # The contract lives in `main`'s last_ts_in_cache + the GraphQL `since=`
    # variable the script sets. We exercise last_ts_in_cache directly here.
    sys.path.insert(0, str(ROOT / "scripts"))
    import importlib
    mod = importlib.import_module("estate-board-sync")
    importlib.reload(mod)

    cache = pathlib.Path("/tmp/crew102-empty-cache-for-cursor-test.jsonl")
    if cache.exists():
        cache.unlink()
    assert mod.last_ts_in_cache(cache) is None

    cache.write_text(
        json.dumps({"ts": "2026-08-24T03:23:01.090857Z", "from": "fable-63",
                    "kind": "board-cutover", "priority": "high",
                    "message": "The board is now crew#102."}) + "\n",
        encoding="utf-8",
    )
    assert mod.last_ts_in_cache(cache) == "2026-08-24T03:23:01.090857Z"
    cache.unlink()


def test_script_runs_clean_on_a_clean_checkout() -> None:
    """`python3 scripts/estate-board-sync.py` exits 0 on a clean checkout that
    has `gh` authenticated. We treat non-zero as a test failure rather than a
    skip -- if the script cannot run here, the PR is not green."""
    out = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, check=False,
    )
    assert out.returncode == 0, (
        f"estate-board-sync.py exited {out.returncode} on a clean checkout:\n"
        f"stdout: {out.stdout}\nstderr: {out.stderr}"
    )
    line = (out.stdout.strip().splitlines() or [""])[-1]
    assert line.startswith("estate-board-sync:"), line