"""crew#453 residual (2026-08-27): `_ledger_hooks()` swallowed every OSError and returned an
empty set, so a hook-outcomes ledger that exists but cannot be read graded all 46 guards
NEVER_EMITTED with no signal. Rung 4. Both ways: a missing ledger is an honest empty (no hook
has ever run here); a ledger that exists and cannot be read makes the mac domain BLIND, naming
the path, and BLIND fails the gate."""
import importlib.util
import pathlib
import sys

import pytest

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
# Load this checkout's producers.py by path: a `producers` already on sys.path (another
# checkout, the live one) would be graded instead of the code under test.
sys.path.insert(0, str(SCIENCE))
_spec = importlib.util.spec_from_file_location("producers_under_test", SCIENCE / "producers.py")
assert _spec is not None and _spec.loader is not None
producers = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(producers)


@pytest.fixture(autouse=True)
def _fresh_ledger_cache():
    # _ledger_hooks is memoised for the run; each case here needs its own read.
    clear = getattr(producers._ledger_hooks, "cache_clear", None)
    if clear:
        clear()
    yield
    if clear:
        clear()


def test_missing_ledger_is_an_honest_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("HOOK_OUTCOMES", str(tmp_path / "absent.jsonl"))
    assert producers._ledger_hooks() == frozenset()


def test_unreadable_ledger_raises_so_the_domain_is_blind(tmp_path, monkeypatch):
    ledger = tmp_path / "hook-outcomes.jsonl"
    ledger.mkdir()  # exists, is a directory: open() raises IsADirectoryError, an OSError
    monkeypatch.setenv("HOOK_OUTCOMES", str(ledger))
    with pytest.raises(RuntimeError) as e:
        producers._ledger_hooks()
    assert str(ledger) in str(e.value) and "unreadable" in str(e.value)


def test_readable_ledger_names_its_hooks(tmp_path, monkeypatch):
    ledger = tmp_path / "hook-outcomes.jsonl"
    ledger.write_text('{"hook": "a-guard"}\nnot json\n{"nohook": 1}\n')
    monkeypatch.setenv("HOOK_OUTCOMES", str(ledger))
    assert producers._ledger_hooks() == frozenset({"a-guard"})
