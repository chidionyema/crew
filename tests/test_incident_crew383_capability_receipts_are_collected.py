"""crew#383 (datamap WIRED_NEVER): ~/.estate/state/capability_receipts.jsonl, 24,953 rows and
10 MB, the largest ledger under ~/.estate, and no collector named it. The wrapper stamps
`ended_at` as an epoch string ("1787811578.055679"), which row_time() treated as no time at
all, so registering the source alone would have filed 25k rows without a time (crew#73 row 4).
Rule: the source is registered with its time field, and an epoch stored as a string is a time.
Rung 4, incident test, both ways."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))
import collect  # noqa: E402


def test_the_receipt_ledger_is_a_registered_source_with_its_time_field():
    reg = json.loads((ROOT / "science/sources.json").read_text())
    src = next(s for s in reg["sources"] if s["name"] == "capability_receipts")
    assert src["path"].endswith("capability_receipts.jsonl") and src["time_field"] == "ended_at"
    ver = json.loads((ROOT / "science/verdicts.json").read_text())
    ent = next(e for e in ver["entries"] if e["key"] == "mac/ledger/*capability_receipts.jsonl")
    assert ent["verdict"] == "COLLECTED" and "capability_receipts" in ent["reader"]


def test_an_epoch_stored_as_a_string_is_a_time_and_a_bare_number_string_is_not():
    assert collect.row_time({"ended_at": "1787811578.055679"}, "ended_at") == collect.iso(1787811578.055679)
    assert collect.row_time({"ended_at": "42"}, "ended_at") is None
    assert collect.row_time({"ended_at": "not a time"}, "ended_at") is None
    assert collect.row_time({"at": "2026-08-27T06:00:00Z"}, "at") == "2026-08-27T06:00:00Z"
