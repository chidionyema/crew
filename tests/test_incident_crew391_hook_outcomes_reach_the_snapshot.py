"""crew#391 incident, 2026-08-27: 36 hooks ran on every event and recorded nothing, so the
founder could not see refusal rate or latency. claude-guards#122 writes the ledger; this rule
is that the ledger reaches STATE.md as one row.

Rule: hooks_row is GREEN with the refusal count and the hook that refused most when the window
has runs; RED when the ledger exists but the window is silent (an unwired wrapper looks like a
quiet day otherwise); NOT RUN with no ledger. Rung 4, named for the ticket.
"""
import datetime as dt
import importlib.machinery
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def _mod():
    loader = importlib.machinery.SourceFileLoader("snap", str(HERE / "scripts" / "estate-snapshot"))
    spec = importlib.util.spec_from_loader("snap", loader)
    assert spec is not None
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


def _row(at: dt.datetime, hook: str, refused: bool, ms: int = 40) -> str:
    return json.dumps({"at": at.strftime("%Y-%m-%dT%H:%M:%SZ"), "event": "Stop", "hook": hook,
                       "session": "abcdef01", "exit": 2 if refused else 0, "ms": ms, "refused": refused})


def test_hooks_row_green_red_and_not_run(tmp_path):
    m = _mod()
    now = dt.datetime(2026, 8, 27, 3, 0, tzinfo=dt.UTC)
    ledger = tmp_path / "hook-outcomes.jsonl"

    assert "NOT RUN" in m.hooks_row(ledger, now)[0]

    ledger.write_text("\n".join([_row(now - dt.timedelta(hours=1), "jargon-guard.py", True, 160),
                                 _row(now - dt.timedelta(hours=2), "jargon-guard.py", True),
                                 _row(now - dt.timedelta(hours=3), "dod-guard.py", False),
                                 _row(now - dt.timedelta(days=3), "opa-hook.py", True)]) + "\n")
    row = m.hooks_row(ledger, now)[0]
    assert row.startswith("| hooks | GREEN |") and "3 runs in 24h, 2 refused (most: jargon-guard.py 2), slowest 160 ms" in row

    ledger.write_text(_row(now - dt.timedelta(days=3), "opa-hook.py", True) + "\n")
    assert m.hooks_row(ledger, now)[0].startswith("| hooks | RED |")

    ledger.write_text("not json\n")
    assert "NOT RUN" in m.hooks_row(ledger, now)[0]
