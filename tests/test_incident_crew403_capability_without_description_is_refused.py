"""Incident test, crew#403 CP-A: the showcase refuses a capability that cannot self-describe.

Founder, 2026-08-27: "cant have components that cannot self describe." A science module with no
docstring line, or no `__main__` entry, is refused by `showcase.py --check`; a module with both is
permitted. Both directions in one run (LAW 45 step 3). Rung 4.
"""
import pathlib
import sys

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import showcase  # noqa: E402

GOOD = '"""Counts things.\n"""\nif __name__ == "__main__":\n    print(1)\n'
NO_DOC = 'if __name__ == "__main__":\n    print(1)\n'
NO_MAIN = '"""Counts things.\n"""\ndef f():\n    return 1\n'


def _rows(tmp_path, monkeypatch, files: dict[str, str]) -> list[dict]:
    for name, body in files.items():
        (tmp_path / f"{name}.py").write_text(body)
    monkeypatch.setattr(showcase, "SCIENCE", tmp_path)
    monkeypatch.setattr(showcase, "LAUNCHD", tmp_path / "no-launchd")
    rows = [{"name": n, "what": showcase._docstring_line(tmp_path / f"{n}.py"), "run": f"python3 science/{n}.py"} for n in files]
    return rows


def test_a_capability_with_no_docstring_or_no_main_is_refused_and_a_complete_one_is_not(tmp_path, monkeypatch):
    rows = _rows(tmp_path, monkeypatch, {"good": GOOD, "nodoc": NO_DOC, "nomain": NO_MAIN})
    bad = showcase.refusals(rows)
    assert any(b.startswith("nodoc.py: no docstring") for b in bad), bad
    assert any(b.startswith("nomain.py: no __main__") for b in bad), bad
    assert not [b for b in bad if b.startswith("good.py")], bad
    assert showcase.refusals(_rows(tmp_path, monkeypatch, {"good": GOOD})) == []
