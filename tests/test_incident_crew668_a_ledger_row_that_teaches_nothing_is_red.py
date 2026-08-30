"""crew#668 CP1: incidents/LEDGER.jsonl is the estate's what-not-to-do store. A row with no
class, no guard or no receipt is a story, not training data, and the generator refuses it.
Founder, 2026-08-30: "incident reports are learning opportunity and training data for estate"."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "incident-report"
LEDGER = ROOT / "incidents" / "LEDGER.jsonl"


def run(ledger: Path, out: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--check", "--ledger", str(ledger), "--out", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_the_live_ledger_teaches_and_renders(tmp_path):
    res = run(LEDGER, tmp_path / "page.md")
    assert res.returncode == 0, res.stdout + res.stderr
    page = (tmp_path / "page.md").read_text()
    assert "## What not to do, ranked by hours dark" in page
    assert "I1" in page and "Otto" in page


def test_a_row_with_no_class_guard_or_receipt_is_red(tmp_path):
    row = json.loads(LEDGER.read_text().splitlines()[0])
    row.update({"classes": [], "guard": "", "timeline": [{"at": "2026-01-01T00:00Z", "what": "x"}]})
    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps(row) + "\n")
    res = run(bad, tmp_path / "page.md")
    assert res.returncode == 1
    assert "missing classes" in res.stdout
    assert "missing guard" in res.stdout
    assert "no receipt" in res.stdout


def test_an_unknown_class_and_an_unknown_hazard_are_red(tmp_path):
    row = json.loads(LEDGER.read_text().splitlines()[0])
    row.update({"classes": ["vibes"], "hazard": "R999"})
    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps(row) + "\n")
    res = run(bad, tmp_path / "page.md")
    assert res.returncode == 1
    assert "unknown class vibes" in res.stdout and "R999" in res.stdout


def test_the_committed_page_matches_the_ledger(tmp_path):
    run(LEDGER, tmp_path / "page.md")
    assert (tmp_path / "page.md").read_text() == (ROOT / "docs" / "INCIDENTS.md").read_text()
