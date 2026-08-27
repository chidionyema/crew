"""Incident test, crew#90 (2026-08-27): com.founder.sciencecollect exited 1 on every run because
RESEARCH-LEDGER.jsonl line 25 carried a field ('verdict') the schema contract did not list, and
the contract was only ever checked inside the scheduled run. Rule: every row of the research
ledger in git has only the keys its contract in git lists. Rung 4, both ways: the ledger as
committed passes; a row with an unlisted key is named by line.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "science/RESEARCH-LEDGER.jsonl"
CONTRACT = ROOT / "science/schemas/research_ledger.json"


def _off_contract(lines: list[str], fields: set[str]) -> list[str]:
    bad = []
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        extra = sorted(set(json.loads(line)) - fields)
        if extra:
            bad.append(f"line {i}: {extra}")
    return bad


def test_incident_crew90_every_ledger_row_is_on_the_contract():
    fields = set(json.loads(CONTRACT.read_text())["fields"])
    assert _off_contract(LEDGER.read_text().splitlines(), fields) == []


def test_incident_crew90_an_unlisted_key_is_named_by_line():
    fields = set(json.loads(CONTRACT.read_text())["fields"])
    rows = [json.dumps({"date": "2026-08-27", "ticket": "crew#90"}), json.dumps({"date": "2026-08-27", "surprise": 1})]
    assert _off_contract(rows, fields) == ["line 2: ['surprise']"]
