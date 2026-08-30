"""crew#668 CP2: the retroactive audit is generated, and a guard row that lacks its repo, path,
class or first commit -- or names a class outside the vocabulary -- turns the check red."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "scripts" / "incident-report"
BACKFILL = ROOT / "scripts" / "incident-backfill"


def run(*args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, str(REPORT), *args], cwd=cwd, capture_output=True, text=True, check=False
    )


def test_the_committed_guards_file_is_what_the_backfill_generates_from_this_repo(tmp_path):
    out = tmp_path / "g.jsonl"
    r = subprocess.run(
        [sys.executable, str(BACKFILL), "--repo", "crew=.", "--out", str(out)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    mine = [json.loads(line) for line in out.read_text().splitlines()]
    committed = [
        json.loads(line)
        for line in (ROOT / "incidents" / "GUARDS.jsonl").read_text().splitlines()
        if '"repo": "crew"' in line
    ]
    assert {g["guard"] for g in mine} == {g["guard"] for g in committed}, (
        "a guard was added or renamed: rerun scripts/incident-backfill and commit incidents/GUARDS.jsonl"
    )


def test_the_page_carries_the_audit_section_with_counts():
    assert run("--check").returncode == 0
    page = (ROOT / "docs" / "INCIDENTS.md").read_text()
    assert "retroactive audit" in page
    assert "repeat offenders" in page
    assert "are unclassified" in page


def test_a_guard_row_without_a_class_or_with_an_unknown_class_is_red(tmp_path):
    good = {
        "repo": "crew",
        "guard": "tests/test_incident_x.py",
        "title": "x",
        "class": "silent-green",
        "first_commit": "abc1234",
        "guarded_at": "2026-08-01T00:00:00+00:00",
    }
    g = tmp_path / "g.jsonl"
    g.write_text(
        json.dumps(good)
        + "\n"
        + json.dumps({**good, "class": ""})
        + "\n"
        + json.dumps({**good, "class": "vibes"})
        + "\n"
    )
    r = run("--check", "--guards", str(g), "--out", str(tmp_path / "p.md"))
    assert r.returncode == 1, r.stdout
    assert "missing class" in r.stdout
    assert "unknown class vibes" in r.stdout
    assert "3 guards on record, 2 malformed" in r.stdout
