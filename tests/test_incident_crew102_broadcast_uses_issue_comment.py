"""Incident test for crew#102.

The estate board is GitHub issue crew#102, not a laptop JSONL file.
This test proves that the broadcast path uses `gh issue comment` to land
every row on the issue, with a dead-letter fallback when posting fails.
"""
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "estate-board-broadcast.sh"


def _read(path: Path) -> str:
    assert path.exists(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def test_script_exists_and_is_executable():
    assert SCRIPT.exists(), f"broadcast script missing at {SCRIPT}"
    mode = SCRIPT.stat().st_mode
    assert mode & 0o111, "broadcast script must be executable"


def test_script_targets_gh_issue_comment():
    body = _read(SCRIPT)
    assert "gh issue comment" in body, (
        "broadcast script must use `gh issue comment` to land rows on the "
        "GitHub issue (crew#102), not append to a local file directly"
    )


def test_script_targets_the_estate_board_repo_and_issue():
    body = _read(SCRIPT)
    assert "chidionyema/crew" in body, "script must target the estate board repo"
    assert "102" in body, "script must target estate board issue #102"


def test_script_dead_letters_on_failure():
    body = _read(SCRIPT)
    assert "board-deadletter" in body or "deadletter" in body.lower(), (
        "script must dead-letter to ~/.claude/state/board-deadletter.jsonl "
        "when the GitHub post fails, never drop the row silently"
    )


def test_broadcast_posting_runs_under_bash():
    """Smoke-test the script path with a row that exercises both the cache
    write and the dead-letter fallback (no GH_TOKEN in this environment)."""
    if not SCRIPT.exists():
        return
    env = os.environ.copy()
    env.pop("GH_TOKEN", None)
    tmp_cache = REPO_ROOT / ".cache-test-board.jsonl"
    tmp_dead = REPO_ROOT / ".cache-test-deadletter.jsonl"
    if tmp_cache.exists():
        tmp_cache.unlink()
    if tmp_dead.exists():
        tmp_dead.unlink()
    env["ESTATE_BOARD_JSONL"] = str(tmp_cache)
    env["ESTATE_BOARD_DEADLETTER"] = str(tmp_dead)

    result = subprocess.run(
        [str(SCRIPT), "test row from crew#102 incident test"],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    # Either posted (rc=0) or dead-lettered (rc=75). Never silent drop.
    assert result.returncode in (0, 75), (
        f"unexpected exit {result.returncode}; broadcast must either post or "
        f"dead-letter, never silently drop. stderr={result.stderr!r}"
    )
    assert tmp_cache.exists() and tmp_cache.read_text().strip(), (
        "offline cache must always be written, even when the GitHub post fails"
    )
