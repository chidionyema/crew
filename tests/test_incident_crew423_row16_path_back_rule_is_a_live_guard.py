"""crew#423 row 16 (leave-a-path-back-when, Stop, mechanical): the guard is the LAW 16 rule in
claude-guards policy/reply.rego (claude-guards#134). The row has no effective law number
(law: null, was: 16), so the citation the map checks is the `was` number, and the rule must say
"LAW 16". Rung 4, both ways: a rego that cites LAW 16 with opa-hook wired is live; the same rego
with the runner unwired, or one that cites nothing, is dead."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "science"))
import law_enforcement as le

ROW = {"rule": "leave-a-path-back-when", "was": 16, "law": None, "guards": ["policy/reply.rego"]}


def test_row16_is_bound_to_the_rego_rule_in_the_map():
    m = json.loads((pathlib.Path(__file__).resolve().parents[1] / "science/enforcement-map.json").read_text())
    row = next(r for r in m["laws"] if r["rule"] == "leave-a-path-back-when")
    assert row["state"] == "live" and row["guards"] == ["policy/reply.rego"]


def test_row16_rego_is_live_only_when_it_cites_law_16_and_opa_hook_is_wired(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "guard_path", lambda name: str(tmp_path / name))
    rego = tmp_path / "policy" / "reply.rego"
    rego.parent.mkdir()
    rego.write_text('deny contains "LAW 16: leave a path back when you drop something"\n')
    assert le.law_refs("policy/reply.rego") == {16}
    assert le.derive(ROW, {"opa-hook": "PREVENTIVE"}) == "live"
    assert le.derive(ROW, {}) == "dead"
    rego.write_text('deny contains "no citation"\n')
    assert le.derive(ROW, {"opa-hook": "PREVENTIVE"}) == "dead"
