"""crew#370, 2026-08-27: LAW 38 says a guard that refuses correct work is an outage, and only the
refusal half was measured (crew#391). claude-guards hook-run.py now writes `waived: <marker>` on a
pass whose command carried an override marker; this rule is that the snapshot counts a refusal
overturned that way as a false refusal, and prints it on the hooks row.

Both ways: a refusal followed within 10 min by a waived pass of the same hook in the same session
counts one; a waived pass by another session, another hook, before the refusal, or 11 min later
counts nothing; a waived pass with no refusal before it counts nothing.
"""
import datetime as dt
import importlib.machinery
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def _mod():
    loader = importlib.machinery.SourceFileLoader("snap370", str(HERE / "scripts" / "estate-snapshot"))
    spec = importlib.util.spec_from_loader("snap370", loader)
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


def _row(at: dt.datetime, hook="rule-guard.py", refused=False, session="abcdef01", waived=None) -> dict:
    r = {"at": at.strftime("%Y-%m-%dT%H:%M:%SZ"), "event": "PreToolUse", "hook": hook, "session": session,
         "exit": 2 if refused else 0, "ms": 40, "refused": refused}
    if waived:
        r["waived"] = waived
    return r


def test_overturned_refusal_counts_and_the_row_prints_it(tmp_path):
    m = _mod()
    t = dt.datetime(2026, 8, 27, 3, 0, tzinfo=dt.UTC)
    rows = [_row(t, refused=True), _row(t + dt.timedelta(minutes=2), waived="raw-diff-intended")]
    assert m.false_refusals(rows) == 1
    ledger = tmp_path / "hook-outcomes.jsonl"
    ledger.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    assert "1 overturned by a marker" in m.hooks_row(ledger, t + dt.timedelta(minutes=5))[0]


def test_the_other_shapes_count_nothing():
    m = _mod()
    t = dt.datetime(2026, 8, 27, 3, 0, tzinfo=dt.UTC)
    refusal = _row(t, refused=True)
    for other in (_row(t + dt.timedelta(minutes=2), session="ffffffff", waived="main-is-red"),
                  _row(t + dt.timedelta(minutes=2), hook="dod-guard.py", waived="main-is-red"),
                  _row(t - dt.timedelta(minutes=2), waived="main-is-red"),
                  _row(t + dt.timedelta(minutes=11), waived="main-is-red"),
                  _row(t + dt.timedelta(minutes=2))):
        assert m.false_refusals([refusal, other]) == 0, other
    assert m.false_refusals([_row(t, waived="in-flight")]) == 0
