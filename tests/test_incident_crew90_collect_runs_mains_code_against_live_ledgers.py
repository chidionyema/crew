"""Incident test, crew#90 (2026-08-27, second cause): com.founder.sciencecollect ran the live
checkout's collect.py at 838ec8f with an uncommitted registry, while main (7d4efdb) already
carried the contract the ledger needed; a clean origin/main worktree exited 0 and the scheduled
run exited 1. Rule: the scheduled check executes main's code and contract, and the ledgers it
reads and writes stay in the live checkout. Rung 4, both ways: SCIENCE_DATA moves the `science`
root and nothing else; unset, the root is the directory of the collect.py that runs.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECT = ROOT / "science" / "collect.py"


def _roots(tmp_path: Path, extra_env: dict[str, str]) -> dict[str, str]:
    reg = tmp_path / "sources.json"
    reg.write_text(json.dumps({"sources": [
        {"name": "a", "root": "science", "path": "a.jsonl", "receiver": "otlp"},
        {"name": "b", "root": "home", "path": "b.jsonl", "receiver": "otlp"}]}))
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); import collect; "
        "from pathlib import Path; r = collect.load_registry(Path(sys.argv[2])); "
        "print(__import__('json').dumps({k: str(v[0]) for k, v in r['sources'].items()}))")
    env = {k: v for k, v in os.environ.items() if not k.startswith("SCIENCE_")}
    env.update(extra_env)
    out = subprocess.run([sys.executable, "-c", code, str(COLLECT.parent), str(reg)],
                         capture_output=True, text=True, env=env, check=True, cwd=tmp_path)
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_incident_crew90_science_data_moves_the_science_root_and_only_that(tmp_path):
    ledgers = tmp_path / "live-science"
    ledgers.mkdir()
    moved = _roots(tmp_path, {"SCIENCE_DATA": str(ledgers), "ESTATE_HOME": str(tmp_path)})
    assert moved["a"] == str(ledgers / "a.jsonl"), "a science ledger reads from SCIENCE_DATA"
    assert moved["b"] == str(tmp_path / "b.jsonl"), "a home ledger is untouched by SCIENCE_DATA"

    default = _roots(tmp_path, {"ESTATE_HOME": str(tmp_path)})
    assert default["a"] == str(COLLECT.parent / "a.jsonl"), "unset, the root is collect.py's dir"


def test_incident_crew90_scheduled_check_runs_from_a_worktree_with_the_ledgers_pinned_here():
    text = (ROOT / "scripts" / "science-collect").read_text()
    check = text[text.index("python3 \"$COLLECT\" --check"):]
    before = text[: text.index("python3 \"$COLLECT\" --check")]
    assert "origin/main" in before and "git worktree add --detach" in before
    assert 'export SCIENCE_DATA="$CREW/science"' in before
    assert 'SCIENCE_WAREHOUSE="$CREW/science/warehouse.db"' in before
    assert "unset SCIENCE_DATA" in check, "the pin does not leak into showcase or foresight"
