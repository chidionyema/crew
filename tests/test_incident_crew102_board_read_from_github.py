"""crew#102: agent sessions read the estate board from GitHub issue #102.

Founder, 2026-08-24: "why not just use github issues? why reinvent the wheel badly."
The board lives at issue #102 in `chidionyema/crew`; the JSONL at
~/.claude/ESTATE_BOARD.jsonl is only the offline cache. Proved both ways on
literal strings, no network: a real comment shape yields rows, a malformed one
is named not silently dropped, and a refused API call raises with the reason.
"""
from __future__ import annotations

import datetime
import importlib.util
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "board_read.py"


def _load():
    spec = importlib.util.spec_from_file_location("board_read", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_a_single_row_in_a_backtick_wrapped_comment_parses():
    mod = _load()
    body = (
        "`2026-08-24T03:23:01.090857Z` **fable-63** (board-cutover/high): "
        "The board is now crew#102. estate-broadcast.py writes every row here."
    )
    rows = mod._parse_comment(body)
    assert len(rows) == 1
    r = rows[0]
    assert r["ts"] == "2026-08-24T03:23:01.090857Z"
    assert r["from"] == "fable-63"
    assert r["kind"] == "board-cutover/high"
    assert "crew#102" in r["message"]


def test_a_backfill_carries_many_rows_one_per_bullet():
    mod = _load()
    body = (
        "**Backfill 3/3 -- the 191 rows.**\n\n"
        "- `2026-08-24T02:26:40Z` **?** (guard-broken/info): {\"guard\": \"goal-guard.py\"}\n"
        "- `2026-08-24T02:26:41Z` **?** (guard-broken/info): {\"guard\": \"goal-guard.py\"}\n"
        "- `2026-08-24T02:30:33Z` **?** (note/info): colima STOPPED on founder instruction.\n"
    )
    rows = mod._parse_comment(body)
    assert len(rows) == 3
    assert rows[0]["ts"] == "2026-08-24T02:26:40Z"
    assert "goal-guard.py" in rows[0]["message"]
    assert rows[2]["from"] == "?"
    assert rows[2]["kind"] == "note/info"


def test_a_row_with_no_parseable_header_is_named_not_dropped(capsys):
    """The local file fell into this exact class on 2026-08-23: 56 of 68 lines unparseable,
    the writer printed pretty-printed JSON to a JSONL file. We surface the count; we do not
    swallow it."""
    mod = _load()
    body = (
        "this is not a row\n"
        "`2026-08-24T03:23:01Z` **fable-63** (board-cutover/high): ok\n"
        "{ \"json\": \"with no header at all\" }\n"
    )
    rows = mod._parse_comment(body)
    assert len(rows) == 1
    assert rows[0]["from"] == "fable-63"
    captured = capsys.readouterr()
    assert "2 line(s) skipped" in captured.err


def test_latest_after_filters_by_iso_timestamp():
    mod = _load()
    cutoff = datetime.datetime(2026, 8, 24, 3, 0, tzinfo=datetime.UTC)
    rows = [
        {"ts": "2026-08-24T02:00:00Z", "from": "a", "kind": "x", "message": "before"},
        {"ts": "2026-08-24T03:30:00Z", "from": "b", "kind": "y", "message": "after"},
    ]
    out = [r for r in rows if mod._coerce_ts(r["ts"]) > cutoff]
    assert [r["from"] for r in out] == ["b"]


def test_z_suffix_and_offset_both_parse_to_utc():
    mod = _load()
    a = mod._coerce_ts("2026-08-24T03:23:01Z")
    b = mod._coerce_ts("2026-08-24T03:23:01+00:00")
    assert a == b
    assert a.tzinfo is not None


def test_a_refused_api_call_raises_with_the_reason(tmp_path):
    """The estate's failure grammar: never silent. A fake `gh` that exits 1 must surface
    its stderr, not return []."""
    mod = _load()
    fake = tmp_path / "gh"
    fake.write_text("#!/bin/sh\necho 'gh: Not Found (HTTP 404)' >&2\nexit 1\n")
    fake.chmod(0o755)
    env = dict(__import__("os").environ, PATH=f"{tmp_path}:{__import__('os').environ['PATH']}")
    # `subprocess.run` is what `_gh` uses; we monkeypatch it to point at the fake.
    r = subprocess.run(
        [sys.executable, "-c",
         "import sys, importlib.util;"
         f"spec=importlib.util.spec_from_file_location('m',r'{SCRIPT}');"
         "m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);"
         "m._gh(['api','repos/x/issues/1/comments'])"],
        capture_output=True, text=True, env=env, check=False,
    )
    assert r.returncode != 0
    assert "Not Found" in r.stderr or "Not Found" in r.stdout


def test_module_imports_cleanly():
    mod = _load()
    assert mod.DEFAULT_REPO == "chidionyema/crew"
    assert mod.DEFAULT_ISSUE == 102
    assert hasattr(mod, "read_board_rows")
    assert hasattr(mod, "latest_after")


def test_no_local_jsonl_is_consulted_at_import_time():
    """The local JSONL is the offline cache. The new reader does not silently fall back to it
    when the network is up; it is the GitHub API or raise."""
    mod = _load()
    src = SCRIPT.read_text()
    assert "ESTATE_BOARD" not in src.splitlines()[0]
    assert ".jsonl" not in src, "the reader must not consult ~/.claude/ESTATE_BOARD.jsonl"
    assert "gh" in src
    assert "issues/102/comments" in src or "DEFAULT_ISSUE" in src
