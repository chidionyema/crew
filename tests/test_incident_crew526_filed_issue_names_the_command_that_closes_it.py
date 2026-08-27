"""crew#526 CP1 (founder 2026-08-27: "158 unclaimed open how come this never goes down"): guards
filed issues with no closing rule and nothing ever read them back. A datamap gap issue now carries
`Closes-when: python3 science/datamap.py --row <key>`, and that command exits 0 only once the
entry's verdict has left the gap set; 3 (never argparse's 2) when the entry does not exist."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from science import datamap as dm  # noqa: E402


def test_the_filed_body_carries_the_closes_when_line(monkeypatch, tmp_path):
    seen = {}

    class R:
        returncode = 0
        stdout = "https://github.com/chidionyema/crew/issues/777\n"
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda argv, **kw: seen.setdefault("argv", argv) and R())
    monkeypatch.setattr(dm, "REGISTER", tmp_path / "verdicts.json")
    reg = {"entries": [{"key": "audit.event", "verdict": "WIRED_NEVER", "why": "no reader"}]}
    graded = [{"entry": "audit.event", "verdict": "WIRED_NEVER", "key": "audit.event", "kind": "log", "measures": ["n"]}]
    assert dm.file_tickets(graded, reg, "chidionyema/crew") == 1
    body = seen["argv"][seen["argv"].index("--body") + 1]
    assert "Closes-when: `python3 science/datamap.py --row audit.event`" in body


def test_row_exit_is_zero_only_once_the_entry_left_the_gap_set():
    reg = {"entries": [{"key": "a", "verdict": "WIRED_NEVER"}, {"key": "b", "verdict": "COLLECTED"},
                       {"key": "c", "verdict": "EXCLUDED"}]}
    assert dm.row_status(reg, "a") == 1
    assert dm.row_status(reg, "b") == 0
    assert dm.row_status(reg, "c") == 0
    assert dm.row_status(reg, "missing") == 3


def test_the_cli_row_mode_runs_without_discovery():
    r = subprocess.run([sys.executable, "science/datamap.py", "--row", "no.such.entry.crew526"],
                       cwd=ROOT, capture_output=True, text=True, check=False, timeout=120)
    assert r.returncode == 3, r.stdout + r.stderr
    assert "BLIND" in r.stdout
