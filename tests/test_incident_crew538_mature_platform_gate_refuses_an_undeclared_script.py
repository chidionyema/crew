"""Incident test, crew#538 CP2 (2026-08-27): #173's gate was closed unmerged by the crew#504 sweep
and rebuilt on main. R6/LAW 43 as a protocol: a .sh/.py ADDED on a branch must name, in its first
40 lines, the standard it uses, the deviation it takes, or the mature tool it rejected.

Both ways: the selftest's five arms pass, and a fresh repo with one bare added script is refused
with exit 1 naming the file, while a declared one passes with exit 0.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "verify.d", "12-mature-platform.sh")


def _repo(tmp_path, script_text):
    r = tmp_path / "r"
    r.mkdir()

    def git(*a):
        return subprocess.run(["git", "-C", str(r), *a], check=True, capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (r / "README.md").write_text("x\n")
    git("add", "README.md")
    git("commit", "-q", "-m", "base")
    git("checkout", "-q", "-b", "feature")
    (r / "new.sh").write_text(script_text)
    git("add", "new.sh")
    git("commit", "-q", "-m", "add")
    return r


def _run(repo):
    return subprocess.run(["bash", GATE], cwd=repo, env={**os.environ, "CREW_ROOT": str(repo)},
                          capture_output=True, text=True, check=False)


def test_selftest_five_arms_pass():
    out = subprocess.run(["bash", GATE, "--selftest"], capture_output=True, text=True, check=False)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "selftest: 5 arms, 0 failures" in out.stdout


def test_an_added_script_that_declares_nothing_is_refused_by_name(tmp_path):
    out = _run(_repo(tmp_path, "#!/bin/sh\n# just a helper\necho hi\n"))
    assert out.returncode == 1, out.stdout + out.stderr
    assert "new.sh" in out.stdout


def test_an_added_script_that_names_the_rejected_tool_passes(tmp_path):
    out = _run(_repo(tmp_path, "#!/bin/sh\n# Rejected: cron, it cannot see machine load.\necho hi\n"))
    assert out.returncode == 0, out.stdout + out.stderr
