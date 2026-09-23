"""Tests for ``crew.tools.bench``."""

from __future__ import annotations

import subprocess
import sys

import pytest

from crew.tools import bench


def test_count_target_known() -> None:
    assert bench.count_target("crew/issue-102") == 5


def test_count_target_unknown() -> None:
    with pytest.raises(KeyError):
        bench.count_target("crew/issue-9999")


def test_module_invocation_prints_five() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "crew.tools.bench", "--target", "crew/issue-102"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "5" in result.stdout


def test_module_invocation_unknown_target() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "crew.tools.bench", "--target", "crew/issue-9999"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "5" not in result.stdout