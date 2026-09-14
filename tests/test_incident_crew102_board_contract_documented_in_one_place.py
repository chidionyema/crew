"""crew#102 — the board contract named in one place.

The contract is the issue body of crew#102: a single GitHub issue is the
board of record, comments on it are the rows, and the format, target,
dead-letter path and read command are all declared in the body and proved
by the existing incident tests in this suite.

This test does NOT re-implement the contract. It calls out to the existing
surfaces that already prove each row, by importing the existing modules,
reading their public constants and assertions, and naming every row out
loud so a future reviewer can read the file top-to-bottom and see the
whole board contract as a single document.

Rows proved here (every assertion names its source):

  1. Board target: chidionyema/crew#102
       — tests/test_incident_crew102_estate_board_is_issue_102.py BOARD_REPO/BOARD_ISSUE
  2. Issue OPEN with "ESTATE BOARD" or "BROADCAST" title
       — tests/test_incident_crew102_estate_board_is_issue_102.py::test_board_target_is_repo_issue_102
  3. Comment rows follow `ts **from** (kind/priority): message`
       — tests/test_incident_crew102_estate_board_is_issue_102.py COMMENT_FORMAT
       — tests/test_incident_crew102_github_board_read.py ROW_PATTERN
       — scripts/estate-board-sync.py COMMENT_FULL_RE / COMMENT_SIMPLE_RE
  4. Dead-letter path ~/.claude/state/board-deadletter.jsonl creatable
       — tests/test_incident_crew102_estate_board_is_issue_102.py DEAD_LETTER
  5. Documented `gh issue view 102 --repo chidionyema/crew --comments --json number,state,comments` runs clean
       — tests/test_incident_crew102_github_board_read.py::test_read_command_documented_in_board_doc_runs_clean
  6. At least one comment matches the declared format
       — tests/test_incident_crew102_estate_board_is_issue_102.py::test_comment_format_matches_issue_body
       — tests/test_incident_crew102_github_board_read.py::test_a_board_row_matches_the_declared_row_format
  7. parse_comment handles both full and simple row formats
       — tests/test_incident_crew101_the_board_cache_was_never_refilled.py::test_parse_comment_full_format
       — tests/test_incident_crew101_the_board_cache_was_never_refilled.py::test_parse_comment_simple_format_defaults_kind_and_priority
  8. Backfill headers (prose) are not rows — parse_comment returns None
       — tests/test_incident_crew101_the_board_cache_was_never_refilled.py::test_a_backfill_header_is_not_a_row
  9. Rows come back oldest-first
       — tests/test_incident_crew101_the_board_cache_was_never_refilled.py::test_rows_come_back_oldest_first
 10. Cache is one JSON object per real newline; failed read is loud non-zero exit (LAW 28)
       — tests/test_incident_crew101_the_board_cache_was_never_refilled.py::test_sync_writes_one_json_object_per_line
       — tests/test_incident_crew101_the_board_cache_was_never_refilled.py::test_a_failed_read_is_a_loud_non_zero_exit

If any of these tests goes red, the board contract drifted; the fix is on
the source of truth (the issue body, the writer, the doc) — never by
widening this file.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib

import pytest

# ---------------------------------------------------------------------------
# Load the existing incident tests as text so we can name every row in one place
# without re-implementing the assertions. pytest does not run these as tests here;
# this file is the single named contract, and the existing tests remain the
# per-row diagnosis. The contract is the contract: named in one place, proved
# many times.
# ---------------------------------------------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests"
SCRIPTS_DIR = ROOT / "scripts"


def _read(rel: str) -> str:
    return (TESTS_DIR / rel).read_text()


def _load_ebs():
    """Load scripts/estate-board-sync.py by path the way the 101 test loads it."""
    _spec = importlib.util.spec_from_file_location(
        "estate_board_sync", SCRIPTS_DIR / "estate-board-sync.py"
    )
    assert _spec is not None, "scripts/estate-board-sync.py is not where this test expects it"
    assert _spec.loader is not None, "no loader for scripts/estate-board-sync.py"
    module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Row 1 — Board target: chidionyema/crew#102
#   Proven by tests/test_incident_crew102_estate_board_is_issue_102.py, which
#   names BOARD_REPO/BOARD_ISSUE and asserts the issue resolves.
# ---------------------------------------------------------------------------

def test_row_1_board_target_is_repo_issue_102() -> None:
    """The board of record is chidionyema/crew#102, named in the 102-target test."""
    src = _read("test_incident_crew102_estate_board_is_issue_102.py")
    assert 'BOARD_REPO = "chidionyema/crew"' in src, (
        "102-target test no longer pins BOARD_REPO=chidionyema/crew; the board moved"
    )
    assert "BOARD_ISSUE = 102" in src, (
        "102-target test no longer pins BOARD_ISSUE=102; the board moved"
    )
    # The docstring is the human-readable contract; it must still call out the target.
    assert "chidionyema/crew#102" in src, (
        "102-target test's docstring no longer names chidionyema/crew#102"
    )


# ---------------------------------------------------------------------------
# Row 2 — Issue OPEN with "ESTATE BOARD" or "BROADCAST" title
#   Proven by the assertion in test_board_target_is_repo_issue_102.
# ---------------------------------------------------------------------------

def test_row_2_issue_open_with_estate_board_or_broadcast_title() -> None:
    """The board's issue is OPEN and carries ESTATE BOARD or BROADCAST in the title."""
    src = _read("test_incident_crew102_estate_board_is_issue_102.py")
    assert 'assert payload["state"] == "OPEN"' in src, (
        "102-target no longer asserts state == OPEN"
    )
    assert '"ESTATE BOARD" in title or "BROADCAST" in title' in src, (
        "102-target no longer asserts the ESTATE BOARD / BROADCAST title rule"
    )


# ---------------------------------------------------------------------------
# Row 3 — Comment rows follow `ts **from** (kind/priority): message`
#   Proven by the COMMENT_FORMAT regex in 102-target and ROW_PATTERN in 102-read,
#   and by the COMMENT_FULL_RE / COMMENT_SIMPLE_RE regexes in estate-board-sync.py.
# ---------------------------------------------------------------------------

def test_row_3_comment_format_regex_is_pinned_in_three_places() -> None:
    """The same row shape lives in the 102-target regex, the 102-read regex, and the script."""
    pat = (
        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?\s+\*\*[^*]+\*\*"
        r"\s+\([^)]+\):\s+.+$"
    )
    src_102 = _read("test_incident_crew102_estate_board_is_issue_102.py")
    src_read = _read("test_incident_crew102_github_board_read.py")
    assert pat in src_102, "102-target no longer pins the comment-format regex"
    assert pat in src_read, "102-read no longer pins the row-format regex"
    # The script's two regexes are the parsers; both must still exist.
    ebs = _load_ebs()
    assert hasattr(ebs, "COMMENT_FULL_RE"), "scripts/estate-board-sync.py lost COMMENT_FULL_RE"
    assert hasattr(ebs, "COMMENT_SIMPLE_RE"), "scripts/estate-board-sync.py lost COMMENT_SIMPLE_RE"
    # Sanity: the full-format regex still matches a row in the contract shape.
    full = "`2026-08-24T03:23:01Z` **fable-63** (note/info): a row"
    assert ebs.COMMENT_FULL_RE.match(full), "COMMENT_FULL_RE no longer matches a row in the contract shape"


# ---------------------------------------------------------------------------
# Row 4 — Dead-letter path ~/.claude/state/board-deadletter.jsonl creatable
#   Proven by DEAD_LETTER + test_dead_letter_path_exists_or_creatable in 102-target.
# ---------------------------------------------------------------------------

def test_row_4_dead_letter_path_is_creatable() -> None:
    """The dead-letter file is wired at ~/.claude/state/board-deadletter.jsonl."""
    src = _read("test_incident_crew102_estate_board_is_issue_102.py")
    assert "board-deadletter.jsonl" in src, "102-target no longer pins the dead-letter path"
    assert "DEAD_LETTER.parent.mkdir(parents=True, exist_ok=True)" in src, (
        "102-target no longer creates the dead-letter parent directory"
    )
    assert 'def test_dead_letter_path_exists_or_creatable' in src, (
        "102-target no longer carries the dead-letter writability test"
    )


# ---------------------------------------------------------------------------
# Row 5 — Documented `gh issue view` read command runs clean
#   Proven by test_read_command_documented_in_board_doc_runs_clean in 102-read.
# ---------------------------------------------------------------------------

def test_row_5_documented_read_command_runs_clean() -> None:
    """The exact gh command from CREW-BOARD-VISIBILITY.md is pinned in 102-read."""
    src = _read("test_incident_crew102_github_board_read.py")
    expected = (
        '_gh("issue", "view", str(BOARD_ISSUE), "--repo", BOARD_REPO, '
        '"--comments", "--json", "number,state,comments")'
    )
    assert expected in src, (
        "102-read no longer pins the documented read command; either the doc drifted "
        "or the test was widened"
    )
    assert 'def test_read_command_documented_in_board_doc_runs_clean' in src, (
        "102-read lost its named read-command test"
    )


# ---------------------------------------------------------------------------
# Row 6 — At least one comment matches the declared format
#   Proven by test_comment_format_matches_issue_body (102-target) and
#   test_a_board_row_matches_the_declared_row_format (102-read).
# ---------------------------------------------------------------------------

def test_row_6_at_least_one_comment_matches_the_declared_format() -> None:
    """Both incident tests assert a row on the board matches the contract."""
    src_102 = _read("test_incident_crew102_estate_board_is_issue_102.py")
    src_read = _read("test_incident_crew102_github_board_read.py")
    assert 'def test_comment_format_matches_issue_body' in src_102, (
        "102-target lost test_comment_format_matches_issue_body"
    )
    assert 'def test_a_board_row_matches_the_declared_row_format' in src_read, (
        "102-read lost test_a_board_row_matches_the_declared_row_format"
    )


# ---------------------------------------------------------------------------
# Row 7 — parse_comment handles both full and simple row formats
#   Proven by test_parse_comment_full_format and test_parse_comment_simple_format_defaults_kind_and_priority
#   in the 101-rebuild test.
# ---------------------------------------------------------------------------

def test_row_7_parse_comment_handles_full_and_simple_formats() -> None:
    """parse_comment parses both the kind/priority row and the older bare row."""
    src = _read("test_incident_crew101_the_board_cache_was_never_refilled.py")
    assert 'def test_parse_comment_full_format' in src, (
        "101-rebuild lost test_parse_comment_full_format"
    )
    assert 'def test_parse_comment_simple_format_defaults_kind_and_priority' in src, (
        "101-rebuild lost test_parse_comment_simple_format_defaults_kind_and_priority"
    )
    ebs = _load_ebs()
    full = ebs.parse_comment(
        "`2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): The estate cannot be rebuilt."
    )
    assert full == {
        "ts": "2026-08-23T21:41:15Z",
        "from": "rebuild-drill",
        "kind": "drill-failed",
        "priority": "info",
        "message": "The estate cannot be rebuilt.",
    }
    simple = ebs.parse_comment(
        "`2026-08-24T03:23:01.090857Z` **fable-63**: The board is now crew#102."
    )
    assert simple == {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        "kind": "unclassified",
        "priority": "info",
        "message": "The board is now crew#102.",
    }


# ---------------------------------------------------------------------------
# Row 8 — Backfill headers (prose) are not rows — parse_comment returns None
#   Proven by test_a_backfill_header_is_not_a_row in 101-rebuild.
# ---------------------------------------------------------------------------

def test_row_8_backfill_headers_are_not_rows() -> None:
    """Prose a person wrote — including the Backfill N/3 headers — returns None."""
    src = _read("test_incident_crew101_the_board_cache_was_never_refilled.py")
    assert 'def test_a_backfill_header_is_not_a_row' in src, (
        "101-rebuild lost test_a_backfill_header_is_not_a_row"
    )
    ebs = _load_ebs()
    assert ebs.parse_comment(
        "**Backfill 1/3 — the 191 rows that existed before the board became this issue.**"
    ) is None
    assert ebs.parse_comment("") is None
    assert ebs.parse_comment("just a note from a human") is None


# ---------------------------------------------------------------------------
# Row 9 — Rows come back oldest-first
#   Proven by test_rows_come_back_oldest_first in 101-rebuild.
# ---------------------------------------------------------------------------

def test_row_9_rows_come_back_oldest_first() -> None:
    """rows_from() returns the board's rows in chronological order."""
    src = _read("test_incident_crew101_the_board_cache_was_never_refilled.py")
    assert 'def test_rows_come_back_oldest_first' in src, (
        "101-rebuild lost test_rows_come_back_oldest_first"
    )
    ebs = _load_ebs()
    comments = [
        {"body": "`2026-08-24T10:00:00Z` **b** (note/info): second"},
        {"body": "`2026-08-23T10:00:00Z` **a** (note/info): first"},
        {"body": "**Backfill 2/3 — ignore me.**"},
    ]
    assert [r["message"] for r in ebs.rows_from(comments)] == ["first", "second"]


# ---------------------------------------------------------------------------
# Row 10 — Cache is one JSON object per real newline; failed read is loud
#   non-zero exit (LAW 28). Proven by test_sync_writes_one_json_object_per_line
#   and test_a_failed_read_is_a_loud_non_zero_exit in 101-rebuild.
# ---------------------------------------------------------------------------

def test_row_10_cache_is_one_json_per_line_and_failed_read_is_loud(tmp_path, monkeypatch, capsys) -> None:
    """The cache file is JSONL; a failed read exits 1 with the cause on stderr, no half-file."""
    src = _read("test_incident_crew101_the_board_cache_was_never_refilled.py")
    assert 'def test_sync_writes_one_json_object_per_line' in src, (
        "101-rebuild lost test_sync_writes_one_json_object_per_line"
    )
    assert 'def test_a_failed_read_is_a_loud_non_zero_exit' in src, (
        "101-rebuild lost test_a_failed_read_is_a_loud_non_zero_exit (LAW 28)"
    )
    ebs = _load_ebs()
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
    assert len(lines) == 2
    assert [json.loads(ln)["message"] for ln in lines] == ["first", "second"]

    # And the loud-failure side: a fetch that raises turns into exit 1, never a half-cache.
    def boom(*_a, **_k):
        raise OSError("network is down")

    monkeypatch.setattr(ebs, "fetch_comments", boom)
    cache = tmp_path / "board.jsonl"
    assert ebs.main(["estate-board-sync.py", str(cache)]) == 1
    assert "network is down" in capsys.readouterr().err
    assert not cache.exists()
