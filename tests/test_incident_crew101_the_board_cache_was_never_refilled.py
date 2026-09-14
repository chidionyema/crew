"""crew#101: the read side of the estate board.

The board of record is a GitHub issue; sessions read a local JSONL cache. Nothing refilled
that cache from the issue, so a session's board was whatever its laptop happened to hold.
These grade the rebuild: what counts as a row, what does not, and that the cache it writes
is one JSON object per line in time order.
"""

import importlib.util
import json
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
#: The script's name carries a hyphen, so it is loaded by path, the way this suite loads
#: every other hyphenated script in scripts/ (see test_incident_crew284_*).
_spec = importlib.util.spec_from_file_location(
    "estate_board_sync", ROOT / "scripts" / "estate-board-sync.py"
)
#: spec_from_file_location returns None when the path is not importable, and a spec can
#: carry no loader. Both are real failure modes -- a renamed or deleted script -- and the
#: type checker refuses the idiom without them, so they are asserted rather than assumed.
assert _spec is not None, "scripts/estate-board-sync.py is not where this test expects it"
assert _spec.loader is not None, "no loader for scripts/estate-board-sync.py"
ebs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ebs)


def test_parse_comment_full_format() -> None:
    row = ebs.parse_comment(
        "`2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): The estate cannot be rebuilt."
    )
    assert row == {
        "ts": "2026-08-23T21:41:15Z",
        "from": "rebuild-drill",
        "kind": "drill-failed",
        "priority": "info",
        "message": "The estate cannot be rebuilt.",
    }


def test_parse_comment_simple_format_defaults_kind_and_priority() -> None:
    row = ebs.parse_comment(
        "`2026-08-24T03:23:01.090857Z` **fable-63**: The board is now crew#102."
    )
    assert row == {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        "kind": "unclassified",
        "priority": "info",
        "message": "The board is now crew#102.",
    }


def test_a_backfill_header_is_not_a_row() -> None:
    """The first comments on the issue are prose a person wrote, not broadcasts."""
    assert (
        ebs.parse_comment(
            "**Backfill 1/3 — the 191 rows that existed before the board became this issue.**"
        )
        is None
    )
    assert ebs.parse_comment("") is None
    assert ebs.parse_comment("just a note from a human") is None


def test_rows_come_back_oldest_first() -> None:
    comments = [
        {"body": "`2026-08-24T10:00:00Z` **b** (note/info): second"},
        {"body": "`2026-08-23T10:00:00Z` **a** (note/info): first"},
        {"body": "**Backfill 2/3 — ignore me.**"},
    ]
    assert [r["message"] for r in ebs.rows_from(comments)] == ["first", "second"]


def test_sync_writes_one_json_object_per_line(tmp_path) -> None:
    """The cache is JSONL: a real newline between objects, not the two characters `\\n`."""
    out = tmp_path / "nested" / "ESTATE_BOARD.jsonl"
    n = ebs.sync_estate_board(
        [
            {"body": "`2026-08-23T10:00:00Z` **a** (note/info): first"},
            {"body": "not a row"},
            {"body": "`2026-08-24T10:00:00Z` **b** (fire/p1): second"},
        ],
        out,
    )
    assert n == 2
    lines = out.read_text().splitlines()
    assert len(lines) == 2, out.read_text()
    assert [json.loads(ln)["message"] for ln in lines] == ["first", "second"]
    assert json.loads(lines[1])["priority"] == "p1"


def test_sync_accepts_a_json_string_as_well_as_a_list(tmp_path) -> None:
    out = tmp_path / "board.jsonl"
    payload = json.dumps([{"body": "`2026-08-23T10:00:00Z` **a** (note/info): only"}])
    assert ebs.sync_estate_board(payload, out) == 1
    assert json.loads(out.read_text().strip())["from"] == "a"


def test_a_rebuild_replaces_the_cache_rather_than_appending(tmp_path) -> None:
    """A session reads this file; two runs must not double every row."""
    out = tmp_path / "board.jsonl"
    comments = [{"body": "`2026-08-23T10:00:00Z` **a** (note/info): only"}]
    ebs.sync_estate_board(comments, out)
    ebs.sync_estate_board(comments, out)
    assert len(out.read_text().splitlines()) == 1


def test_a_failed_read_is_a_loud_non_zero_exit(tmp_path, monkeypatch, capsys) -> None:
    """A board that could not be read is never a quiet empty cache (LAW 28)."""

    def boom(*_a, **_k):
        raise OSError("network is down")

    monkeypatch.setattr(ebs, "fetch_comments", boom)
    assert ebs.main(["estate-board-sync.py", str(tmp_path / "board.jsonl")]) == 1
    assert "network is down" in capsys.readouterr().err
    assert not (tmp_path / "board.jsonl").exists()


# ---------------------------------------------------------------------------
# crew#102 stale-only sync: state file + ETag + dead-letter
# (the four named tests the spec pins).
# ---------------------------------------------------------------------------


def test_sync_short_circuits_when_state_is_fresh(tmp_path, monkeypatch) -> None:
    """A fresh state file + matching live count -> no body fetch, no cache write."""
    state_path = tmp_path / "state.json"
    state_path.write_text(json.dumps({
        "last_pulled_at": time.time(),
        "last_row_count": 7,
        "etag": "W/\"abc\"",
    }))

    cache = tmp_path / "ESTATE_BOARD.jsonl"

    # The body fetch and the gh subprocess are both off-limits when the state
    # proves nothing changed.
    def body_boom(*_a, **_k):
        raise AssertionError("fetch_comments_with_etag must not run when state is fresh")

    def sub_boom(*_a, **_k):
        raise AssertionError("subprocess.run must not run when state is fresh")

    monkeypatch.setattr(ebs, "fetch_comments_with_etag", body_boom)
    monkeypatch.setattr(subprocess, "run", sub_boom)
    monkeypatch.setattr(ebs, "fetch_issue_comment_count", lambda *a, **k: 7)

    n, status = ebs.sync_if_stale(cache, state_path=state_path, min_age_s=300)
    assert status == "fresh", status
    assert n == 0
    assert not cache.exists()


def test_sync_skips_body_fetch_on_etag_match(tmp_path, monkeypatch) -> None:
    """A stale state with a cached etag -> 304 -> 'fresh', no cache rewrite."""
    state_path = tmp_path / "state.json"
    state_path.write_text(json.dumps({
        "last_pulled_at": time.time() - 3600,
        "last_row_count": 7,
        "etag": "W/\"abc\"",
    }))

    cache = tmp_path / "ESTATE_BOARD.jsonl"
    cache.write_text(
        json.dumps({"ts": "t", "from": "x", "kind": "k", "priority": "p", "message": "m"}) + "\n"
    )
    original = cache.read_text()

    monkeypatch.setattr(
        ebs,
        "fetch_comments_with_etag",
        lambda *a, **k: ([], "W/\"abc\"", True),
    )

    n, status = ebs.sync_if_stale(cache, state_path=state_path, min_age_s=0)
    assert status == "fresh"
    assert n == 0
    # Cache was not rewritten on a 304.
    assert cache.read_text() == original


def test_sync_writes_dead_letter_on_gh_failure(tmp_path, monkeypatch) -> None:
    """A CalledProcessError from gh -> one JSON line in BOARD_DEAD_LETTER, status dead-letter."""
    cache = tmp_path / "ESTATE_BOARD.jsonl"
    dead = tmp_path / "deadletter.jsonl"
    monkeypatch.setattr(ebs, "BOARD_DEAD_LETTER", dead)

    monkeypatch.setattr(
        ebs,
        "fetch_comments_with_etag",
        lambda *a, **k: (_ for _ in ()).throw(
            subprocess.CalledProcessError(1, ["gh"], stderr="rate limit")
        ),
    )

    n, status = ebs.sync_if_stale(cache, state_path=tmp_path / "state.json", min_age_s=0)
    assert status == "dead-letter"
    assert n == 0
    assert dead.exists()
    lines = [ln for ln in dead.read_text().splitlines() if ln.strip()]
    assert len(lines) == 1, lines
    row = json.loads(lines[0])
    assert row["repo"] == ebs.BOARD_REPO
    assert row["issue"] == ebs.BOARD_ISSUE
    assert "rate limit" in row["error"] or "CalledProcessError" in row["error"]


def test_state_file_writes_atomically(tmp_path) -> None:
    """save_state writes the file and never leaves a sibling .tmp behind."""
    state_path = tmp_path / "state.json"
    ebs.save_state(state_path, {"etag": "W/\"x\"", "last_row_count": 3})
    assert state_path.exists()
    assert not (tmp_path / "state.json.tmp").exists()
    roundtrip = ebs.load_state(state_path)
    assert roundtrip == {"etag": "W/\"x\"", "last_row_count": 3}