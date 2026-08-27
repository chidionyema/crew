"""crew#84: 19 sources, 1064 field paths, 0 contracts, 0 descriptions, 0 owners, and nothing
refused a source arriving that way. Rule: the schema file is the contract; it names an owner
and a description, documents fields with a PII flag, and records the number of undescribed
fields the tree was accepted with. A missing owner, a documented field the data lost, or a new
undescribed field fails ``--check`` and ``--contracts``. Rung 4, incident test; the DoD
commands on the issue are run here in order."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from science import collect

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "science" / "schemas"


def test_every_schema_file_in_git_is_a_complete_contract():
    """DoD 1 and 2: one contract per collected source, and the gate passes on the tree."""
    files = sorted(p.stem for p in SCHEMAS.glob("*.json"))
    absent = sorted(n for n in collect.SOURCES if not collect.SOURCES[n][0].exists())
    missing = sorted(n for n in collect.SOURCES if n not in files and n not in absent)
    assert not missing, f"sources with no contract: {missing}"
    bad = [f for n in files for f in collect.contract_verdict(n)]
    assert bad == []
    r = subprocess.run([sys.executable, "science/collect.py", "--contracts"], cwd=ROOT,
                       capture_output=True, text=True, check=False)
    assert r.returncode == 0, r.stdout


def _contract(tmp_path, monkeypatch, **over):
    monkeypatch.setattr(collect, "SCHEMAS", tmp_path)
    c = {"owner": "crew/science", "description": "a test source", "fields": {"at": ["str"], "n": ["int"]},
         "field_docs": {"at": {"description": "when", "pii": False}}, "undescribed_baseline": 1}
    c.update(over)
    (tmp_path / "t.json").write_text(json.dumps(c))
    return c


def test_missing_owner_undeclared_field_and_baseline_growth_each_refuse(tmp_path, monkeypatch):
    """DoD 3, 4 and 5 both ways in one run."""
    _contract(tmp_path, monkeypatch)
    assert collect.contract_verdict("t") == []
    assert collect.schema_verdict("t", [{"at": "x", "n": 1}]) == []
    # 3: no owner
    _contract(tmp_path, monkeypatch, owner="")
    assert collect.contract_verdict("t") == ["t: contract names no owner"]
    # 4: a field in the data and not in the contract
    _contract(tmp_path, monkeypatch)
    assert collect.schema_verdict("t", [{"at": "x", "n": 1, "surprise": 2}]) == \
        ["t: line 1: field 'surprise' is not in the schema"]
    # 5: a field admitted to the schema without a description, above the baseline
    _contract(tmp_path, monkeypatch, fields={"at": ["str"], "n": ["int"], "m": ["int"]})
    assert collect.contract_verdict("t") == ["t: 2 undescribed field(s), baseline is 1: m, n"]
    # a documented field the data lost
    _contract(tmp_path, monkeypatch, field_docs={"gone": {"description": "x", "pii": False}}, undescribed_baseline=2)
    assert collect.contract_verdict("t") == ["t: field_docs describes 'gone', which the schema does not have"]
    # no file: blind, never a failure (LAW 38)
    assert collect.contract_verdict("nothing-here") == []


def test_rewriting_a_schema_keeps_its_contract_and_drops_docs_for_lost_fields(tmp_path, monkeypatch):
    _contract(tmp_path, monkeypatch, field_docs={"at": {"description": "when", "pii": False},
                                                 "n": {"description": "count", "pii": False}}, undescribed_baseline=0)
    collect.write_schema("t", [{"at": "x", "k": True}])
    c = json.loads((tmp_path / "t.json").read_text())
    assert c["owner"] == "crew/science" and c["description"] == "a test source"
    assert list(c["field_docs"]) == ["at"] and c["undescribed_baseline"] == 1
    assert collect.contract_verdict("t") == []


@pytest.mark.parametrize("flag", ["--contracts"])
def test_verify_rung_and_flag_agree(flag):
    a = subprocess.run([sys.executable, "science/collect.py", flag], cwd=ROOT, capture_output=True, text=True, check=False)
    b = subprocess.run(["scripts/verify.d/90-data-contracts.sh"], cwd=ROOT, capture_output=True, text=True, check=False)
    assert (a.returncode, a.stdout.splitlines()[0]) == (b.returncode, b.stdout.splitlines()[0])
