"""crew#423: opa-hook.py runs every policy/*.rego except command.rego, but guards() listed only
files whose names matched guard|fence|compliance|scrub|ledger|capture. opa-hook never entered the
tier map, so derive() graded every reply.rego row (LAW 4, 16, 20, 31) "dead" in the live
com.founder.lawenforcement job; the rows flipped to "live" in crew#440/#442 held only against a
hand-supplied tiermap. Rung 4, both ways: opa-hook.py present is listed, absent is not, and a
.py that matches none of the names is still not a guard."""
import pathlib

import science.law_enforcement as le


def test_opa_hook_is_a_guard_when_present_and_not_when_absent(tmp_path, monkeypatch):
    monkeypatch.setattr(le, "SCRIPTS", str(tmp_path))
    (tmp_path / "rule-guard.py").write_text("")
    (tmp_path / "hook-run.py").write_text("")
    assert le.guards() == ["rule-guard"]
    (tmp_path / "opa-hook.py").write_text("")
    assert le.guards() == ["opa-hook", "rule-guard"]


def test_live_scripts_dir_lists_opa_hook():
    if not pathlib.Path(le.SCRIPTS, "opa-hook.py").exists():
        return  # BLIND off the founder Mac, never a verdict
    assert "opa-hook" in le.guards()
