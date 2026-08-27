"""crew#423 row 25: checkpoint-before-you-switch is a live guard, and the map derives it from
the guard's runner. policy/command.rego cites LAW 25 and is loaded by rule-guard.py (PreToolUse on
Bash), not by opa-hook.py; before this the derivation graded every .rego by opa-hook's tier, so a
command.rego rule was "live" when opa-hook was wired and rule-guard was not. Rung 4, both ways:
live with rule-guard PREVENTIVE, dead with only opa-hook PREVENTIVE, dead without the citation."""
import json
import pathlib

import science.law_enforcement as le

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROW = {"rule": "checkpoint-before-you-switch", "was": 25, "law": None, "guards": ["policy/command.rego"]}


def test_map_row_25_is_live_on_command_rego():
    rows = json.loads((ROOT / "science" / "enforcement-map.json").read_text())["laws"]
    row = next(r for r in rows if r["rule"] == "checkpoint-before-you-switch")
    assert row["state"] == "live" and row["guards"] == ["policy/command.rego"]


def test_command_rego_is_graded_by_rule_guards_tier_not_opa_hooks(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "guard_path", lambda name: str(tmp_path / name))
    (tmp_path / "policy").mkdir()
    (tmp_path / "policy" / "command.rego").write_text("# LAW 25 checkpoint before you switch\n")
    assert le.rego_runner("policy/command.rego") == "rule-guard"
    assert le.rego_runner("policy/reply.rego") == "opa-hook"
    assert le.derive(ROW, {"rule-guard": "PREVENTIVE"}) == "live"
    assert le.derive(ROW, {"opa-hook": "PREVENTIVE"}) == "dead"
    (tmp_path / "policy" / "command.rego").write_text("# no law named here\n")
    assert le.derive(ROW, {"rule-guard": "PREVENTIVE"}) == "dead"
