"""Tests for the ``gh search issues`` index swap and watermark (#102)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from typing import Any
from unittest import mock

# Make ``crew`` importable when pytest is run from the repo root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crew import board


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_row(number: int, *, state: str = "OPEN", updated_at: str = "2024-01-01T00:00:00Z") -> dict[str, Any]:
    return {
        "number": number,
        "title": f"issue #{number}",
        "labels": [{"name": "bug"}],
        "state": state,
        "updatedAt": updated_at,
    }


def _payload_json(rows: list[dict[str, Any]]) -> str:
    return json.dumps(rows)


# ---------------------------------------------------------------------------
# (a) ``gh search issues`` paginates past 200 rows
# ---------------------------------------------------------------------------


def test_search_issues_returns_more_than_200_rows() -> None:
    rows = [_make_row(i, updated_at=f"2024-01-{((i % 28) + 1):02d}T00:00:00Z") for i in range(1, 251)]

    with tempfile.TemporaryDirectory() as tmp:
        cache_path = os.path.join(tmp, "index.json")
        config = mock.Mock(repos=["octo/cat"])

        with mock.patch.object(board, "run_gh", return_value=_payload_json(rows)) as run_gh, \
             mock.patch.object(board, "gh_with_retry", side_effect=lambda fn: fn()) as _retry:
            merged = board.build_index(cache_path, config=config)

        assert len(merged) == 250, f"expected 250 indexed rows, got {len(merged)}"
        # Downstream consumer contract: every row carries the five keys.
        for key, row in merged.items():
            for required in ("number", "title", "labels", "state", "updatedAt"):
                assert required in row, f"row {key} missing {required!r}"
        # We asked ``gh search issues`` with the exact flag set from the plan.
        called_args = run_gh.call_args.args
        assert "search" in called_args
        assert "issues" in called_args
        assert "--paginate" in called_args
        assert "--repo" in called_args
        assert called_args[called_args.index("--repo") + 1] == "octo/cat"
        assert "--limit" in called_args
        assert called_args[called_args.index("--limit") + 1] == "200"
        # Retried via the project's helper.
        _retry.assert_called()


# ---------------------------------------------------------------------------
# (b) Watermark steady-state
# ---------------------------------------------------------------------------


def test_watermark_rerun_returns_zero_new_rows() -> None:
    rows_first = [_make_row(i, updated_at=f"2024-02-{((i % 28) + 1):02d}T00:00:00Z") for i in range(1, 51)]
    rows_third: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory() as tmp:
        cache_path = os.path.join(tmp, "index.json")
        config = mock.Mock(repos=["octo/cat"])

        with mock.patch.object(board, "run_gh") as run_gh, \
             mock.patch.object(board, "gh_with_retry", side_effect=lambda fn: fn()):
            # First call: populate the index + watermark.
            run_gh.return_value = _payload_json(rows_first)
            merged_first = board.build_index(cache_path, config=config)
            assert len(merged_first) == 50

            # Third call: upstream is unchanged → empty payload.
            run_gh.return_value = json.dumps(rows_third)
            merged_third = board.build_index(cache_path, config=config)
            assert len(merged_third) == 50, "steady-state re-run must not drop rows"

        # We asked ``gh`` to honour the watermark on the steady-state call.
        last_call_args = run_gh.call_args.args
        assert "--search-updated" in last_call_args, last_call_args
        idx = last_call_args.index("--search-updated")
        marker = last_call_args[idx + 1]
        assert marker.startswith(">="), marker


# ---------------------------------------------------------------------------
# (c) ``format_index_row`` golden string
# ---------------------------------------------------------------------------


_FIXTURE_INPUT: dict[str, Any] = {
    "number": 42,
    "title": "hello\nworld",
    "labels": [{"name": "bug"}, {"name": "p1"}],
    "state": "OPEN",
    "updatedAt": "2024-03-04T05:06:07Z",
}

# Pre-change golden output for the same input dict — encoded as a literal so
# this test catches any accidental formatter drift in either direction.
_FIXTURE_EXPECTED = "#42    OPEN        2024-03-04T05:06:07Z  bug,p1  hello world"


def test_format_index_row_byte_identical_to_fixture() -> None:
    assert board.format_index_row(_FIXTURE_INPUT) == _FIXTURE_EXPECTED


if __name__ == "__main__":  # pragma: no cover - pytest discoverability
    unittest.main()
