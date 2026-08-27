"""crew#74 row 2: one schema file per source, and a shape change is named by its line.

science/schemas/<source>.json is the closed set of top-level keys and the type names
each has been seen with. A row with a new key, or a key of a new type, fails
`--check` naming the source and the 1-based line. Rung 4, proved both ways in one run.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))

import collect  # noqa: E402


def test_every_collected_source_has_a_schema_file_in_git():
    missing = sorted(n for n in collect.SOURCES if not (collect.SCHEMAS / f"{n}.json").exists())
    absent = sorted(n for n in collect.SOURCES if not collect.SOURCES[n][0].exists())
    assert set(missing) <= set(absent), f"sources with rows and no schema file: {sorted(set(missing) - set(absent))}"


def test_a_new_field_or_a_new_type_is_named_by_line(tmp_path, monkeypatch):
    monkeypatch.setattr(collect, "SCHEMAS", tmp_path)
    rows = [{"at": "2026-08-27T00:00:00Z", "n": 1}, {"at": "2026-08-27T00:01:00Z", "n": 2}]
    assert collect.schema_verdict("src", rows) == []   # no file: blind, never a failure (LAW 38)
    collect.write_schema("src", rows)
    #: crew#84: a fresh file also carries the contract half, empty, with the baseline recorded.
    assert json.loads((tmp_path / "src.json").read_text()) == {
        "fields": {"at": ["str"], "n": ["int"]}, "field_docs": {}, "undescribed_baseline": 2}
    assert collect.schema_verdict("src", rows) == []
    drifted = [*rows, {"at": "x", "n": "3"}, {"at": "y", "n": 4, "extra": True}]
    assert collect.schema_verdict("src", drifted) == [
        "src: line 3: field 'n' is str, schema says int",
        "src: line 4: field 'extra' is not in the schema",
    ]
    many = [*rows, *({"at": "z", "new": i} for i in range(10))]
    out = collect.schema_verdict("src", many)
    assert len(out) == collect.SCHEMA_LINES_NAMED + 1 and out[-1] == "src: 7 more line(s) off schema"


def test_check_wires_the_schema_verdict():
    src = (ROOT / "science" / "collect.py").read_text()
    assert '"schema": schema_verdict(name, rows)' in src and "failures.extend(schema_failures)" in src
