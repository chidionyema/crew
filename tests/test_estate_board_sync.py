import json
import os
import pathlib
import tempfile
from unittest.mock import patch

from crew.scripts.estate_board_sync import parse_comment, sync_estate_board


def test_parse_comment_full_format():
    comment_body = "`2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): The estate cannot be rebuilt."
    expected = {
        "ts": "2026-08-23T21:41:15Z",
        "from": "rebuild-drill",
        "kind": "drill-failed",
        "priority": "info",
        "message": "The estate cannot be rebuilt.",
    }
    assert parse_comment(comment_body) == expected


def test_parse_comment_simple_format():
    comment_body = "`2026-08-24T03:23:01.090857Z` **fable-63**: The board is now crew#102."
    expected = {
        "ts": "2026-08-24T03:23:01.090857Z",
        "from": "fable-63",
        "kind": "unclassified",
        "priority": "info",
        "message": "The board is now crew#102.",
    }
    assert parse_comment(comment_body) == expected


def test_parse_comment_invalid_format():
    comment_body = "This is a malformed comment."
    assert parse_comment(comment_body) is None


def test_sync_estate_board_excludes_backfill_and_sorts():
    mock_comments = [
        {
            "author": "chidionyema",
            "body": "**Backfill 1/3 — the 191 rows that existed before the board became this issue (oldest first).**\n- `2026-08-23T21:41:15Z` **rebuild-drill** (drill-failed/info): The estate cannot be rebuilt."
        },
        {
            "author": "some-agent",
            "body": "`2026-08-24T03:33:33.911368Z` **crew63-fable** (directive/high): FOUNDER, 2026-08-24 (verbatim, this morning): estate not harmonised/synchronised."
        },
        {
            "author": "another-agent",
            "body": "`2026-08-24T03:23:01.090857Z` **fable-63**: The board is now crew#102."
        },
        {
            "author": "chidionyema",
            "body": "`2026-08-24T03:37:55.944208Z` **chidionyema-d1** (audit/high): 2026-08-24T03:37:55Z CERTIFICATION SNAPSHOT (a891843)."
        },
    ]

    expected_rows = [
        {
            "ts": "2026-08-24T03:23:01.090857Z",
            "from": "fable-63",
            "kind": "unclassified",
            "priority": "info",
            "message": "The board is now crew#102.",
        },
        {
            "ts": "2026-08-24T03:33:33.911368Z",
            "from": "crew63-fable",
            "kind": "directive",
            "priority": "high",
            "message": "FOUNDER, 2026-08-24 (verbatim, this morning): estate not harmonised/synchronised.",
        },
        {
            "ts": "2026-08-24T03:37:55.944208Z",
            "from": "chidionyema-d1",
            "kind": "audit",
            "priority": "high",
            "message": "2026-08-24T03:37:55Z CERTIFICATION SNAPSHOT (a891843).",
        },
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = pathlib.Path(tmpdir) / "ESTATE_BOARD.jsonl"
        sync_estate_board(json.dumps(mock_comments), str(output_file))

        with open(output_file, "r") as f:
            lines = f.readlines()
            actual_rows = [json.loads(line) for line in lines]

        assert actual_rows == expected_rows


def test_sync_estate_board_handles_empty_comments():
    mock_comments = []
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = pathlib.Path(tmpdir) / "ESTATE_BOARD.jsonl"
        sync_estate_board(json.dumps(mock_comments), str(output_file))
        assert not output_file.exists() or output_file.read_text() == ""


def test_sync_estate_board_handles_unparseable_comments():
    mock_comments = [
        {
            "author": "some-agent",
            "body": "This is an unparseable comment."
        },
        {
            "author": "another-agent",
            "body": "`2026-08-24T03:23:01.090857Z` **fable-63**: The board is now crew#102."
        },
    ]
    expected_rows = [
        {
            "ts": "2026-08-24T03:23:01.090857Z",
            "from": "fable-63",
            "kind": "unclassified",
            "priority": "info",
            "message": "The board is now crew#102.",
        },
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = pathlib.Path(tmpdir) / "ESTATE_BOARD.jsonl"
        sync_estate_board(json.dumps(mock_comments), str(output_file))

        with open(output_file, "r") as f:
            lines = f.readlines()
            actual_rows = [json.loads(line) for line in lines]

        assert actual_rows == expected_rows


@patch('crew.scripts.estate_snapshot.fetch_issue_comments_with_gh')
def test_update_local_estate_board_cache_integration(mock_fetch_comments):
    mock_fetch_comments.return_value = [
        {
            "author": "some-agent",
            "body": "`2026-08-24T03:33:33.911368Z` **crew63-fable** (directive/high): FOUNDER, 2026-08-24 (verbatim, this morning): estate not harmonised/synchronised."
        },
        {
            "author": "another-agent",
            "body": "`2026-08-24T03:23:01.090857Z` **fable-63**: The board is now crew#102."
        },
    ]

    # Temporarily change HOME to a temp directory for this test
    with tempfile.TemporaryDirectory() as tmpdir:
        original_home = os.environ.get("HOME")
        os.environ["HOME"] = tmpdir
        try:
            from crew.scripts.estate_snapshot import update_local_estate_board_cache, HOME as SNAPSHOT_HOME
            # Ensure SNAPSHOT_HOME is updated to the temporary directory
            SNAPSHOT_HOME = pathlib.Path(tmpdir)

            result = update_local_estate_board_cache()
            assert result == [f"| estate board sync | GREEN | Synced from crew#102 to ESTATE_BOARD.jsonl |"], f"Unexpected result: {result}"

            expected_jsonl_path = pathlib.Path(tmpdir) / ".claude/ESTATE_BOARD.jsonl"
            assert expected_jsonl_path.exists()

            with open(expected_jsonl_path, "r") as f:
                lines = f.readlines()
                actual_rows = [json.loads(line) for line in lines]

            expected_rows = [
                {
                    "ts": "2026-08-24T03:23:01.090857Z",
                    "from": "fable-63",
                    "kind": "unclassified",
                    "priority": "info",
                    "message": "The board is now crew#102.",
                },
                {
                    "ts": "2026-08-24T03:33:33.911368Z",
                    "from": "crew63-fable",
                    "kind": "directive",
                    "priority": "high",
                    "message": "FOUNDER, 2026-08-24 (verbatim, this morning): estate not harmonised/synchronised.",
                },
            ]
            assert actual_rows == expected_rows

        finally:
            if original_home is not None:
                os.environ["HOME"] = original_home
            else:
                del os.environ["HOME"]

