"""crew#434: LAW 31 was enforced by policy/reply.rego (claude-guards#131) and the
enforcement map still said `absent`, because law_enforcement only knew two guard
kinds, .py files and git hooks. Rung 4, incident test. The rule: a Rego rule is
live when it cites the law and opa-hook.py is wired; either missing is dead."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "science"))
import law_enforcement as le


def _entry(): return {"rule": "x", "law": 31, "guards": ["policy/x.rego"]}


def test_rego_rule_is_live_only_when_it_cites_the_law_and_its_runner_is_wired(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "SCRIPTS", str(tmp_path))
    (tmp_path / "policy").mkdir()
    rego = tmp_path / "policy" / "x.rego"
    rego.write_text('deny contains "THE FOUNDER DOES NOT RUN SCRIPTS (LAW 31)"\n')
    assert le.law_refs("policy/x.rego") == {31}
    assert le.derive(_entry(), {"opa-hook": "PREVENTIVE"}) == "live"
    # runner not wired: the file alone enforces nothing
    assert le.derive(_entry(), {}) == "dead"
    # runner wired, rule cites nothing: nothing binds it to LAW 31
    rego.write_text('deny contains "no citation"\n')
    assert le.derive(_entry(), {"opa-hook": "PREVENTIVE"}) == "dead"
