"""crew#437: the scheduled jobs run from ~/dev/code/crew, which sat on feat/research-engine-step1
at a 2026-08-25 commit with 50 dirty rows for two days, so every merge since ran nowhere. Rung 4,
incident test, both ways: a clean checkout on main behind origin is fast-forwarded and a local
edit to an untouched file survives; a checkout on another branch, or one whose edited file the
update also changes, is not moved and the row is RED.
"""
import importlib.machinery
import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _snap():
    loader = importlib.machinery.SourceFileLoader("snap", str(ROOT / "scripts" / "estate-snapshot"))
    spec = importlib.util.spec_from_loader("snap", loader)
    assert spec is not None
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


def _git(cwd: Path, *args: str) -> str:
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "HOME": str(cwd), "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"}
    return subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=cwd, check=True,
                          capture_output=True, text=True, env=env).stdout.strip()


def _estate(tmp: Path) -> tuple[Path, Path]:
    origin = tmp / "origin.git"
    _git(tmp, "init", "-q", "--bare", "-b", "main", str(origin))
    live = tmp / "live"
    _git(tmp, "clone", "-q", str(origin), str(live))
    (live / "a.txt").write_text("a\n")
    (live / "ledger.jsonl").write_text("1\n")
    _git(live, "add", "."); _git(live, "commit", "-qm", "c1"); _git(live, "push", "-q", "origin", "HEAD:main")
    _git(live, "branch", "-q", "--set-upstream-to=origin/main", "main")
    pusher = tmp / "pusher"
    _git(tmp, "clone", "-q", str(origin), str(pusher))
    return live, pusher


def _advance(pusher: Path, name: str, text: str) -> None:
    (pusher / name).write_text(text)
    _git(pusher, "add", "."); _git(pusher, "commit", "-qm", f"advance {name}"); _git(pusher, "push", "-q", "origin", "HEAD:main")


def test_incident_crew437_behind_and_clean_is_fast_forwarded_and_a_local_edit_survives(tmp_path):
    live, pusher = _estate(tmp_path)
    _advance(pusher, "b.txt", "local\n")
    _git(live, "fetch", "-q", "origin"); _git(live, "merge", "-q", "--ff-only", "origin/main")
    (live / "b.txt").write_text("local edit\n")  # edited here, and no later commit touches it
    _advance(pusher, "a.txt", "a3\n")
    _advance(pusher, "ledger.jsonl", "1\n2\n")  # published by the last snapshot ...
    (live / "ledger.jsonl").write_text("1\n2\n")  # ... and already appended here: same bytes
    _git(live, "fetch", "-q", "origin")
    row = _snap().live_checkout_row(live)[0]
    assert "GREEN" in row and "fast-forwarded" in row, row
    assert _git(live, "rev-parse", "HEAD") == _git(live, "rev-parse", "origin/main")
    assert (live / "a.txt").read_text() == "a3\n"
    assert (live / "b.txt").read_text() == "local edit\n"
    assert (live / "ledger.jsonl").read_text() == "1\n2\n"
    assert _git(live, "diff-index", "--name-only", "HEAD", "--") == "b.txt"  # the kept edit, nothing else


def test_incident_crew437_off_main_or_blocked_is_red_and_not_moved(tmp_path):
    live, pusher = _estate(tmp_path)
    _advance(pusher, "a.txt", "a2\n")
    _git(live, "fetch", "-q", "origin")
    before = _git(live, "rev-parse", "HEAD")
    _git(live, "switch", "-qc", "feat/somewhere")
    row = _snap().live_checkout_row(live)[0]
    assert "RED" in row and "feat/somewhere" in row and "1 commit(s) behind" in row, row
    assert _git(live, "rev-parse", "HEAD") == before
    _git(live, "switch", "-q", "main")
    (live / "a.txt").write_text("mine\n")  # edited here, and the update changes it to a2
    row = _snap().live_checkout_row(live)[0]
    assert "RED" in row and "not moved" in row and "a.txt" in row, row
    assert _git(live, "rev-parse", "HEAD") == before
    assert (live / "a.txt").read_text() == "mine\n"
