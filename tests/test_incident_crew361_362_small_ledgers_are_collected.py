"""crew#361 and crew#362: two small ledgers under ~/.claude/state were graded WIRED_NEVER, one
of them with the reason "the mechanism was replaced", while its writer (founder_actions.py)
wrote a row hours before the grade was read. Rule: a ledger with a live writer is a source,
however small; smallness sets stale_after_hours, not the verdict. Rung 4, incident test, both
ways: each source's time_field parses on a live-shaped row, and a row missing it is unstamped."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import collect  # noqa: E402

LIVE = {
    "worktree_cleanup": {"ts": 1787491151, "iso": "2026-08-23T13:19:11Z", "stamp": "20260823T131823Z",
                         "salvaged": 18, "kept": 18, "kb": 27665, "sha256": "5295", "applied": 0},
    "founder_actions": {"id": "kini-cp1-photo-receipt", "what": "w", "why_founder": "y", "done_when": "d",
                        "unblocks": ["crew#313"], "opened": "2026-08-26", "source": "s"},
}


def _sources():
    reg = json.loads((ROOT / "science/sources.json").read_text())["sources"]
    return {s["name"]: s for s in reg if s["name"] in LIVE}


def test_both_ledgers_are_registered_graded_collected_and_stamped_from_their_time_field():
    srcs = _sources()
    assert set(srcs) == set(LIVE)
    ver = json.loads((ROOT / "science/verdicts.json").read_text())["entries"]
    for key, name in (("mac/*estate-worktr*", "worktree_cleanup"), ("mac/*founder-actio*", "founder_actions")):
        ent = next(e for e in ver if e["key"] == key)
        assert ent["verdict"] == "COLLECTED" and name in ent["reader"]
        assert srcs[name]["stale_after_hours"] >= 168, "a ledger that writes weekly must not read stale daily"
        assert collect.row_time(LIVE[name], srcs[name]["time_field"]) is not None


def test_a_row_without_its_time_field_is_unstamped_not_misdated():
    srcs = _sources()
    row = {k: v for k, v in LIVE["founder_actions"].items() if k != "opened"}
    assert collect.row_time(row, srcs["founder_actions"]["time_field"]) is None
