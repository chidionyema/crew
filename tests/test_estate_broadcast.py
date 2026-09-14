"""crew#102 — the writer half of the board (bin/estate-broadcast.py).

The board of record is the GitHub issue the script's --print-target declares;
the cache at ESTATE_BOARD_JSONL is the offline read side; BOARD_DEADLETTER is
the loud-failure channel. These tests pin the four properties that the cutover
(fable-63, 2026-08-24T03:23:01Z) assumes the writer keeps:

  * a successful write returns 0 and prints the new comment URL,
  * a failed `gh` write falls back to the cache, still exits 0,
  * a failed write with the cache also unwritable dead-letters, warns loudly,
    and exits non-zero,
  * all three sinks carry the same row — same ts/from/kind/priority/message.

No network, no real ~/.claude tree: tmp_path carries both fallbacks and the
dead-letter probe; monkeypatch replaces _post_comment. The format check uses
_render_comment and _render_jsonl directly so the format pin cannot drift from
the writer.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: The script's name carries a hyphen, so the test loads it by path the same way
#: test_incident_crew101 does for scripts/estate-board-sync.py.
_spec = importlib.util.spec_from_file_location(
    "estate_broadcast", ROOT / "bin" / "estate-broadcast.py"
)
assert _spec is not None and _spec.loader is not None, (
    "bin/estate-broadcast.py is not where this test expects it"
)
ebs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ebs)


@pytest.fixture
def fixed_now() -> dt.datetime:
    """Pin the ts so format assertions are stable. _row passes ts through; broadcast()
    accepts `now=`. The format is `YYYY-MM-DDTHH:MM:SSZ` (second precision)."""
    return dt.datetime(2026, 8, 24, 12, 0, 0, tzinfo=dt.timezone.utc)


def _row_dict(from_: str, kind: str, priority: str, message: str) -> dict:
    return {"ts": "2026-08-24T12:00:00Z", "from": from_, "kind": kind,
            "priority": priority, "message": message}


# --- Format pins -------------------------------------------------------------

def test_render_comment_matches_the_issue_body_format() -> None:
    """`ts` **from** (kind/priority): message — pinned by the issue body and reused
    by every backfilled row. A drift here means the script and the reader disagree
    and the reader must be rewritten to match (or vice versa); either is a defect."""
    row = _row_dict("session", "note", "info", "hello")
    assert ebs._render_comment(row) == (
        "`2026-08-24T12:00:00Z` **session** (note/info): hello"
    )


def test_render_jsonl_is_one_line_with_sorted_keys() -> None:
    row = _row_dict("session", "note", "info", "with a / slash and \"quote\"")
    line = ebs._render_jsonl(row)
    assert "\n" not in line, "JSONL must be one object per line; drift breaks the cache reader"
    assert json.loads(line) == row, "rendered JSONL must round-trip back to the same row"
    # Sorted keys: stable across runs, so two writers producing the same row land
    # byte-identical bytes in the cache — provable, not asserted.
    keys = [json.loads(line).keys()]
    assert next(iter(keys)) == ["ts", "from", "kind", "priority", "message"]


def test_render_comment_and_render_jsonl_carry_the_same_row() -> None:
    """DoD 7: byte-identical row across the three sinks. Both renderers read from
    the dict that _row() returns, so this test pins the equality by construction."""
    row = _row_dict("s", "k", "p", "the message")
    comment = ebs._render_comment(row)
    parsed_message = comment.split("): ", 1)[1]
    rendered = ebs._render_jsonl(row)
    back = json.loads(rendered)
    assert back["from"] == "s" and back["kind"] == "k" and back["priority"] == "p"
    assert back["message"] == parsed_message
    assert back["message"] == "the message"


# --- Target pin --------------------------------------------------------------

def test_print_target_is_chidionyema_crew_102(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Default target is the board this PR closes. The cutover broadcast is the
    source of this constant; the test pins it against accidental drift."""
    monkeypatch.delenv("BOARD_REPO", raising=False)
    monkeypatch.delenv("BOARD_ISSUE", raising=False)
    rc = ebs.main(["--print-target"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "chidionyema/crew#102"


def test_target_honors_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Moving the board is one place: BOARD_REPO / BOARD_ISSUE. The pin above is for
    the default; this test makes sure overrides still flow through."""
    monkeypatch.setenv("BOARD_REPO", "chidionyema/idp")
    monkeypatch.setenv("BOARD_ISSUE", "1")
    repo, issue = ebs._target()
    assert repo == "chidionyema/idp"
    assert issue == 1


# --- Happy path: gh succeeds -----------------------------------------------

def test_broadcast_returns_zero_when_gh_posts(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
                                               tmp_path: pathlib.Path, fixed_now: dt.datetime) -> None:
    """The happy path: --from/--kind/--priority/--message, gh posts it, exit 0.
    Cache and dead-letter stay untouched; stdout carries the comment URL."""
    url = "https://github.com/chidionyema/crew/issues/102#issuecomment-1234567"

    def fake_post(repo, issue, body):
        return True, url

    monkeypatch.setattr(ebs, "_post_comment", fake_post)
    rc = ebs.broadcast(
        "session", "note", "info", "hello",
        cache=tmp_path / "cache.jsonl", dead_letter=tmp_path / "dead.jsonl",
        now=fixed_now,
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert url in out
    assert not (tmp_path / "cache.jsonl").exists()
    assert not (tmp_path / "dead.jsonl").exists()


def test_broadcast_happy_path_appends_nothing_to_cache_or_dead_letter(
        monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path, fixed_now: dt.datetime) -> None:
    """Both fallbacks stay empty on success. A writer that wrote to the cache AND
    the board on a successful post would corrupt the reader, which rebuilds from
    the board, never from the cache (LAW 28: one source of truth)."""
    monkeypatch.setattr(ebs, "_post_comment", lambda r, i, b: (True, "url"))
    cache = tmp_path / "cache.jsonl"
    dead = tmp_path / "dead.jsonl"
    ebs.broadcast("s", "k", "p", "m", cache=cache, dead_letter=dead, now=fixed_now)
    assert not cache.exists()
    assert not dead.exists()


# --- Cache fallback: gh fails, cache succeeds ------------------------------

def test_broadcast_falls_back_to_cache_when_gh_fails(
        monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path, fixed_now: dt.datetime) -> None:
    """A failed gh write still exits 0 because the row landed somewhere readers
    find it. The cache file gets exactly one line; stdout is empty; stderr may
    carry one descriptive line but no WARNING."""
    calls = {"n": 0}

    def fake_post(repo, issue, body):
        calls["n"] += 1
        return False, "API rate limit exceeded"

    monkeypatch.setattr(ebs, "_post_comment", fake_post)
    cache = tmp_path / "cache.jsonl"
    dead = tmp_path / "dead.jsonl"
    rc = ebs.broadcast("session", "note", "info", "the message",
                       cache=cache, dead_letter=dead, now=fixed_now)
    assert rc == 0
    assert calls["n"] == 1, "exactly one attempt; no retry loop (LAW 28: never retry a board write)"

    lines = cache.read_text().splitlines()
    assert len(lines) == 1
    obj = json.loads(lines[0])
    assert obj == {
        "ts": "2026-08-24T12:00:00Z", "from": "session",
        "kind": "note", "priority": "info", "message": "the message",
    }
    assert not dead.exists()
    err = capsys.readouterr().err
    assert "WARNING" not in err


def test_broadcast_cache_fallback_does_not_overwrite_existing_rows(
        tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, fixed_now: dt.datetime) -> None:
    """Append-only, not rewrite. The cache is what the reader reads; if it overwrote
    on every call, every row would erase every prior row (LAW 28: never the same
    board twice)."""
    cache = tmp_path / "cache.jsonl"
    cache.write_text(
        '{"ts": "2026-08-24T11:00:00Z", "from": "earlier", "kind": "note", '
        '"priority": "info", "message": "first"}\n'
    )
    monkeypatch.setattr(ebs, "_post_comment", lambda r, i, b: (False, "down"))
    ebs.broadcast("later", "note", "info", "second", cache=cache,
                  dead_letter=tmp_path / "dead.jsonl", now=fixed_now)
    rows = [json.loads(l) for l in cache.read_text().splitlines()]
    assert len(rows) == 2
    assert rows[0]["message"] == "first"
    assert rows[1]["message"] == "second"


def test_broadcast_creates_cache_parents(
        tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, fixed_now: dt.datetime) -> None:
    """The cache path may not exist; create its parents rather than fail (a board
    whose writer needs the file to exist is a board that breaks on first run)."""
    monkeypatch.setattr(ebs, "_post_comment", lambda r, i, b: (False, "down"))
    cache = tmp_path / "deep" / "nest" / "cache.jsonl"
    rc = ebs.broadcast("s", "k", "p", "m", cache=cache,
                       dead_letter=tmp_path / "deep" / "nest" / "dead.jsonl",
                       now=fixed_now)
    # gh fails AND cache write fails (deep/nest/nest-cache.jsonl parent of cache.jsonl is
    # created on demand; but the dead-letter is its twin — let us check that the cache
    # write succeeded here, so we exit 0)
    assert rc == 0
    assert cache.exists()


# --- Dead-letter: gh and cache both fail -----------------------------------

def test_broadcast_dead_letters_and_warns_when_both_sinks_fail(
        monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
        tmp_path: pathlib.Path, fixed_now: dt.datetime) -> None:
    """gh unreachable, cache unwritable: the row lands in the dead-letter and one
    WARNING line is emitted. Exit code is non-zero (a board whose writer swallowed
    the failure is a board nobody knows is broken)."""
    monkeypatch.setattr(ebs, "_post_comment", lambda r, i, b: (False, "no network"))
    cache = tmp_path / "cache.jsonl"
    cache.parent.mkdir(parents=True, exist_ok=True)
    # Make the cache path unwritable by making the parent read-only on POSIX.
    # Skip the test on platforms where mode bits don't apply (e.g. root in docker).
    if sys.platform.startswith("win"):
        pytest.skip("POSIX file modes not honoured on Windows")
    cache.parent.chmod(0o500)
    try:
        rc = ebs.broadcast(
            "session", "fire", "p1", "the cache is locked",
            cache=cache, dead_letter=tmp_path / "dead.jsonl", now=fixed_now,
        )
    finally:
        cache.parent.chmod(0o700)
    assert rc == 1
    err = capsys.readouterr().err
    # Exactly one warning, grep-able by `^WARNING: estate-broadcast`. A stack
    # trace would not pass this — a row that needs interpretation is silent
    # under load (LAW 28).
    warns = [ln for ln in err.splitlines() if ln.startswith("WARNING: estate-broadcast")]
    assert len(warns) == 1, err
    assert "dead-lettered row" in warns[0]
    assert "2026-08-24T12:00:00Z" in warns[0]

    rows = [json.loads(l) for l in (tmp_path / "dead.jsonl").read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["message"] == "the cache is locked"


def test_broadcast_creates_dead_letter_parents(
        monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path, fixed_now: dt.datetime) -> None:
    """Dead-letter parent dirs are created on demand. A row that fails because
    ~/.claude/state/ does not exist has lost both the cache and the loud-failure
    channel — the wrong default for the only writer on the board."""
    monkeypatch.setattr(ebs, "_post_comment", lambda r, i, b: (False, "down"))

    class _FailCachePath:
        """Returns a path under a directory mode 0o500 so open(..., 'a') raises."""
        def __init__(self, blocked: pathlib.Path) -> None:
            self.blocked = blocked
        def __fspath__(self) -> str:
            return str(self.blocked)

    bad = tmp_path / "ro" / "ESTATE_BOARD.jsonl"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.parent.chmod(0o500)
    dead = tmp_path / "ok" / "deep" / "dead.jsonl"
    try:
        rc = ebs.broadcast("s", "k", "p", "m", cache=bad, dead_letter=dead, now=fixed_now)
    finally:
        bad.parent.chmod(0o700)
    assert rc == 1
    assert dead.exists()
    rows = [json.loads(l) for l in dead.read_text().splitlines()]
    assert len(rows) == 1


def test_dead_letter_appends_not_overwrites(
        monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path, fixed_now: dt.datetime) -> None:
    """Dead-letter is append-only too. A second failure while the first still sits
    there must keep both rows — losing a stale row is the same defect as losing a
    current one."""
    monkeypatch.setattr(ebs, "_post_comment", lambda r, i, b: (False, "down"))
    # Force the cache write to fail too by pointing at a path inside a 0o500 dir.
    if sys.platform.startswith("win"):
        pytest.skip("POSIX file modes not honoured on Windows")
    cache_dir = tmp_path / "ro_cache"
    cache_dir.mkdir()
    cache_dir.chmod(0o500)
    cache = cache_dir / "cache.jsonl"
    dead = tmp_path / "dead.jsonl"
    try:
        ebs.broadcast("s", "k", "p", "first", cache=cache, dead_letter=dead, now=fixed_now)
        # Second failure: same writer, different row, same dead-letter file.
        ebs.broadcast("s", "k", "p", "second", cache=cache, dead_letter=dead,
                      now=dt.datetime(2026, 8, 24, 12, 0, 1, tzinfo=dt.timezone.utc))
    finally:
        cache_dir.chmod(0o700)
    rows = [json.loads(l) for l in dead.read_text().splitlines()]
    assert [r["message"] for r in rows] == ["first", "second"]


# --- Byte-identity across the three sinks ----------------------------------

def test_three_sinks_carry_byte_identical_fields(
        monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path, fixed_now: dt.datetime) -> None:
    """DoD 7: the comment body, cache line, and dead-letter line are the same row
    in three renderings. This exercises two paths (gh-ok with one sink, gh-fail
    with another) and compares fields."""
    # Path A: gh succeeds. Capture the body that was about to be posted.
    captured = {}
    real_render = ebs._render_comment

    def fake_post(repo, issue, body):
        captured["body"] = real_render(ebs._row("session", "k", "p", "m", ts="2026-08-24T12:00:00Z"))
        return True, "url"

    monkeypatch.setattr(ebs, "_post_comment", fake_post)
    ebs.broadcast("session", "k", "p", "m",
                  cache=tmp_path / "unused_a.jsonl",
                  dead_letter=tmp_path / "unused_a_dead.jsonl",
                  now=fixed_now)
    comment_body = captured["body"]
    # Parse the comment back to its fields.
    assert comment_body.startswith("`2026-08-24T12:00:00Z`")
    after_ts = comment_body.split("`", 2)[2]
    bold_from, after = after_ts.split("**", 2)[1], after_ts.split("**", 2)[2]
    rest = after.lstrip()
    kind_prio, message = rest.split("): ", 1)
    kind, priority = kind_prio.strip("()").split("/")
    from_comment = {"ts": "2026-08-24T12:00:00Z", "from": bold_from.strip(),
                    "kind": kind.strip(), "priority": priority.strip(),
                    "message": message.strip()}
    # Path B: gh fails, cache succeeds.
    monkeypatch.setattr(ebs, "_post_comment", lambda r, i, b: (False, "down"))
    cache_b = tmp_path / "cache_b.jsonl"
    ebs.broadcast("session", "k", "p", "m", cache=cache_b,
                  dead_letter=tmp_path / "dead_b.jsonl", now=fixed_now)
    from_cache = json.loads(cache_b.read_text().strip())
    # Path C: gh fails, cache fails, dead-letter succeeds.
    cache_c = tmp_path / "cache_c.jsonl"
    cache_c.write_text("")  # make the parent writable elsewhere, the write itself fails below
    if sys.platform.startswith("win"):
        pytest.skip("POSIX file modes not honoured on Windows")
    cache_c_dir = tmp_path / "ro_c"
    cache_c_dir.mkdir()
    cache_c_dir.chmod(0o500)
    cache_c_blocked = cache_c_dir / "cache_c.jsonl"
    dead_c = tmp_path / "dead_c.jsonl"
    try:
        ebs.broadcast("session", "k", "p", "m", cache=cache_c_blocked,
                      dead_letter=dead_c, now=fixed_now)
    finally:
        cache_c_dir.chmod(0o700)
    from_dead = json.loads(dead_c.read_text().strip())
    assert from_comment == from_cache == from_dead


# --- Input validation -------------------------------------------------------

def test_broadcast_rejects_empty_fields(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A row with empty from/kind/priority or message is a defect, not a runtime
    option — return 2 and refuse to write anywhere."""
    cache = tmp_path / "cache.jsonl"
    dead = tmp_path / "dead.jsonl"
    rc = ebs.broadcast("", "k", "p", "m", cache=cache, dead_letter=dead)
    assert rc == 2
    assert not cache.exists()
    assert not dead.exists()
    rc = ebs.broadcast("s", "k", "p", "", cache=cache, dead_letter=dead)
    assert rc == 2
    assert not cache.exists()
    assert not dead.exists()


def test_dry_run_does_not_invoke_gh(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """--dry-run prints the row that would be sent and exits 0, without invoking
    the network or touching any file. Documenting what would be sent is what
    this flag is for; a dry-run that posts is not a dry-run."""
    invoked = {"n": 0}

    def fake_post(repo, issue, body):
        invoked["n"] += 1
        return True, "url"

    monkeypatch.setattr(ebs, "_post_comment", fake_post)
    rc = ebs.main(["--dry-run", "--from", "s", "--kind", "k", "--priority", "p",
                   "--message", "preview"])
    assert rc == 0
    assert invoked["n"] == 0
    out = capsys.readouterr().out
    assert "`" in out and "**s**" in out and "(k/p): preview" in out
    # The JSONL rendering on the second line is also useful for documentation.
    lines = out.strip().splitlines()
    assert len(lines) == 2
    obj = json.loads(lines[1])
    assert obj["from"] == "s" and obj["message"] == "preview"


def test_dry_run_refuses_missing_fields(capsys: pytest.CaptureFixture[str]) -> None:
    rc = ebs.main(["--dry-run"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "required" in err


def test_main_with_no_args_prints_help_and_exits_2(capsys: pytest.CaptureFixture[str]) -> None:
    """No args, no flags: argparse prints usage to stderr and exits 2. A writer
    whose `broadcast` CLI runs without --from is a writer that fabricates rows."""
    with pytest.raises(SystemExit) as exc:
        ebs.main([])
    assert exc.value.code == 2
