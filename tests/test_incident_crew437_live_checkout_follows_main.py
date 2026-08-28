"""crew#437: the scheduled jobs run from ~/dev/code/crew, which sat on feat/research-engine-step1
at a 2026-08-25 commit with 50 dirty rows for two days, so every merge since ran nowhere. Rung 4,
incident test, both ways: a clean checkout on main behind origin is fast-forwarded and a local
edit to an untouched file survives; a checkout on another branch, or one whose edited file the
update also changes, is not moved and the row is RED.

2026-08-28, the same issue and the state the first fix left behind. `~/dev/code/.crew-state` is
the cwd `com.founder.estatesnapshot` runs `scripts/estate-snapshot --commit` from every two
hours. It was detached at 870a04f, 129 commits and 31 hours behind origin/main, and
`grep -c "def portability_row" scripts/estate-snapshot` there returned 0 -- so the row crew#569
merged at 12:37 was absent from every board the job produced after it. This row was watching that
checkout the whole time and printing `RED ... on detached HEAD ... the scheduled jobs run that`,
then returning without moving it. The tests below hold the repair to the same bar as the
fast-forward: it moves a detached HEAD that is an ancestor of origin/main, it still refuses a
named branch and a conflicting edit, and the proof is the merged file on disk rather than the
wording of the row.
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


def _detach_behind(live, pusher, name="c.txt", text="new code\n"):
    """The .crew-state shape: HEAD off any branch, one commit of new code on origin/main."""
    _advance(pusher, name, text)
    _git(live, "fetch", "-q", "origin")
    _git(live, "checkout", "-q", "--detach", "HEAD")
    return _git(live, "rev-parse", "HEAD")


def test_incident_crew437_a_detached_checkout_behind_main_is_moved_not_narrated(tmp_path):
    """The incident. Before this, the row printed RED and returned, and the job kept running the
    old code -- 129 commits of it. The assertion that matters is the third: the new file exists
    on disk, so the next scheduled run executes the code that was merged."""
    live, pusher = _estate(tmp_path)
    was = _detach_behind(live, pusher)
    row = _snap().live_checkout_row(live)[0]
    assert "GREEN" in row and "moved 1 commit(s)" in row, row
    assert _git(live, "rev-parse", "HEAD") != was
    assert _git(live, "rev-parse", "HEAD") == _git(live, "rev-parse", "origin/main")
    assert (live / "c.txt").read_text() == "new code\n"


def test_incident_crew437_the_row_names_the_sha_the_next_run_will_execute(tmp_path):
    """LAW 28: a row that says it moved something and does not say where to is not readable."""
    live, pusher = _estate(tmp_path)
    _detach_behind(live, pusher)
    row = _snap().live_checkout_row(live)[0]
    assert _git(live, "rev-parse", "--short", "HEAD") in row, row


def test_incident_crew437_a_local_edit_the_update_does_not_touch_survives_the_move(tmp_path):
    """The move must not cost what the fast-forward does not cost. .crew-state holds generated
    ledgers no commit owns; a repair that discarded them would be a worse fault than staleness."""
    live, pusher = _estate(tmp_path)
    (live / "a.txt").write_text("edited here\n")
    _detach_behind(live, pusher)
    row = _snap().live_checkout_row(live)[0]
    assert "GREEN" in row and "1 local edit(s) kept" in row, row
    assert (live / "a.txt").read_text() == "edited here\n"


def test_incident_crew437_a_detached_checkout_whose_edit_the_update_changes_is_still_refused(tmp_path):
    """The over-fix guard. Moving a detached HEAD is safe because nothing is lost; the moment
    something would be, the answer is the same RED it was before."""
    live, pusher = _estate(tmp_path)
    _git(live, "checkout", "-q", "--detach", "HEAD")
    was = _git(live, "rev-parse", "HEAD")
    _advance(pusher, "a.txt", "theirs\n")
    _git(live, "fetch", "-q", "origin")
    (live / "a.txt").write_text("mine\n")
    row = _snap().live_checkout_row(live)[0]
    assert "RED" in row and "not moved" in row and "a.txt" in row, row
    assert _git(live, "rev-parse", "HEAD") == was
    assert (live / "a.txt").read_text() == "mine\n"


def test_incident_crew437_a_named_branch_that_is_not_main_is_still_a_persons_work(tmp_path):
    """The second over-fix guard: detached and "on feat/x" are not the same situation, and only
    the first one is this row's to repair. crew#437's original case must stay RED."""
    live, pusher = _estate(tmp_path)
    _advance(pusher, "a.txt", "a2\n")
    _git(live, "fetch", "-q", "origin")
    _git(live, "switch", "-qc", "feat/somebody-elses")
    was = _git(live, "rev-parse", "HEAD")
    row = _snap().live_checkout_row(live)[0]
    assert "RED" in row and "feat/somebody-elses" in row, row
    assert "detached" not in row, row
    assert _git(live, "rev-parse", "HEAD") == was


def test_incident_crew437_a_detached_checkout_already_at_origin_main_is_green(tmp_path):
    """Detached is not itself the fault -- running old code is. A checkout sitting on exactly the
    commit origin/main names is green whether or not a branch name points at it."""
    live, _ = _estate(tmp_path)
    _git(live, "checkout", "-q", "--detach", "origin/main")
    row = _snap().live_checkout_row(live)[0]
    assert "GREEN" in row and "detached at origin/main" in row, row
