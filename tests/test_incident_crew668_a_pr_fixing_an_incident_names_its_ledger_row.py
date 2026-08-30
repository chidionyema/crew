"""crew#668 CP4: a pull request that fixes an incident names its ledger row, so the fix and the
lesson are one record. Paired controls against a fixture ledger; an unreadable ledger is BLIND,
never green by silence (silent green is the defect class)."""

import importlib.util
import pathlib

HERE = pathlib.Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), HERE / "scripts" / f"{name}.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pe = _load("pr-evidence")
LEDGER = [{"id": "I1", "issue": "https://github.com/chidionyema/crew/issues/561"}]


def test_a_fix_for_a_traced_issue_must_name_the_row():
    ok, why = pe.incident_named("Closes #561\n\nfix the mount", LEDGER)
    assert not ok and "Incident: I1" in why


def test_the_issue_in_prose_is_the_same_debt():
    assert not pe.incident_named("Otto again, crew#561 is back", LEDGER)[0]


def test_naming_the_row_passes():
    ok, why = pe.incident_named("Closes #561\nIncident: I1\n", LEDGER)
    assert ok and "I1" in why


def test_a_row_the_ledger_does_not_hold_is_refused():
    assert not pe.incident_named("Incident: I9\n", LEDGER)[0]


def test_a_body_touching_no_traced_issue_passes():
    assert pe.incident_named("Closes #12", LEDGER)[0]


def test_a_mention_inside_a_code_fence_is_not_a_fix():
    assert pe.incident_named("```\ncrew#561\n```", LEDGER)[0]


def test_an_unreadable_ledger_is_blind_not_green_by_silence():
    ok, why = pe.incident_named("Closes #561", None)
    assert ok and "BLIND" in why


def test_the_gate_is_wired_into_check():
    src = (HERE / "scripts" / "pr-evidence.py").read_text()
    assert "incident_named(body, incident_ledger())" in src
