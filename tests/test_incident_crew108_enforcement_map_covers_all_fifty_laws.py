"""crew#108: the enforcement map was written against a 10-law AGENTS.md and rotted 34 laws behind.

LAW 44 says a law without a protocol is a wish; this map is the register of which laws have a
protocol. It rotted because the checker that refuses rot (science/map_covers_laws.py) was never
run by anything (LAW 28). Now crew-qa.yml runs it on every PR, and this test pins the two facts
that made it useful again: the checker reads the 50-row table (LAW 48-50 never had a heading in
the shape the old parser wanted), and the map has one row per law, titles matching.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCI = os.path.join(ROOT, "science")
sys.path.insert(0, SCI)
import map_covers_laws as mcl  # noqa: E402

TABLE = """| # | Law | Fires |
|---|---|---|
| 1 | Put the fire out first | while anything is broken |
| 2 | Proof before action | before every change |
"""


def test_titles_reads_the_table_form(tmp_path):
    p = tmp_path / "AGENTS.md"
    p.write_text(TABLE, encoding="utf-8")
    assert mcl.titles(str(p)) == {"1": "Put the fire out first", "2": "Proof before action"}


def test_laws_file_env_wins(tmp_path, monkeypatch):
    p = tmp_path / "AGENTS.md"
    p.write_text(TABLE, encoding="utf-8")
    monkeypatch.setenv("LAWS_FILE", str(p))
    monkeypatch.setattr(mcl, "LAW_FILES", [str(p)])
    assert mcl.law_source()[0] == str(p)


def test_map_has_one_row_per_law_with_matching_title():
    m = json.load(open(os.path.join(SCI, "enforcement-map.json"), encoding="utf-8"))
    rows = {r["law"]: r for r in m["laws"] if r.get("law") is not None}
    assert sorted(rows) == list(range(1, 51)), sorted(set(range(1, 51)) - set(rows))
    for r in rows.values():
        assert r["verdict"] in ("mechanical", "partial", "judgement"), r["rule"]
        assert r["verdict"] == "judgement" or r["check"].strip(), r["rule"]


def test_checker_is_wired_into_ci():
    wf = open(os.path.join(ROOT, ".github", "workflows", "crew-qa.yml"), encoding="utf-8").read()
    assert re.search(r"LAWS_FILE=\S+ python3 science/map_covers_laws\.py", wf)
