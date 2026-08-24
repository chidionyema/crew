"""Incident: the code standard matched Python by extension and shell by shebang.

Measured 2026-08-24 on `fix/the-snapshot-job-must-know-which-branch-it-is-on`, a PR that
rewrote the commit path of `scripts/estate-snapshot`:

    scripts/estate-snapshot on origin/main   64 ruff findings
    the same file on that branch             77
    inside the lines that branch added       16   (all UP031, percent format)

    $ bash scripts/verify.d/15-code-standard.sh
    PASS: every file this branch touched meets the standard.

`scripts/verify.d/15-code-standard.sh` selected shell with a shebang sniff and Python with
`grep '\\.py$'`. `scripts/estate-snapshot` has a python shebang and no extension -- like
every command on this estate a person types the name of -- so the gate never opened it,
and the PR that named the gap was waved through by the gap. Four tracked files were in it:
bin/crew, scripts/crew-triage, scripts/estate-lander, scripts/estate-snapshot, carrying 84
ruff findings and 0 pyright errors between them.

The rule, asserted here rather than described: a file is what its shebang says it is, for
Python exactly as for shell. Two half-rules for two languages is how a gate ends up
grading a file extension instead of a program.

These tests run the real `15-code-standard.sh` against a throwaway git repo. A test that
re-implemented the gate's file selection would pass while the gate stayed blind, which is
the same mistake one level up.

Rung 4.
"""
import os
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "verify.d" / "15-code-standard.sh"

#: `#!/usr/bin/env python3` with a percent-format line: one UP031 and nothing else.
DIRTY_PY = '#!/usr/bin/env python3\nprint("%s" % 1)\n'
CLEAN_PY = '#!/usr/bin/env python3\nprint("ok")\n'
CLEAN_SH = '#!/usr/bin/env bash\necho ok\n'


def _venv() -> pathlib.Path:
    """The venv the gate would find, which in a worktree is the main checkout's.

    A worktree has no `.venv` of its own. `ROOT / ".venv"` therefore does not exist in the
    place every agent actually runs this suite before pushing, and a skip guard that looked
    only there would skip all six tests locally and run them only in CI -- a checker that
    cannot tell "ruff is absent" from "ruff is not at the one path I looked at", which is
    the defect this whole file is about, one level up. So ask the same question the gate
    asks: `git rev-parse --git-common-dir` is how it finds the main checkout from inside a
    worktree.
    """
    if (ROOT / ".venv" / "bin" / "ruff").exists():
        return ROOT / ".venv"
    r = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                       cwd=ROOT, check=False, capture_output=True, text=True)
    if r.returncode == 0:
        main = pathlib.Path(r.stdout.strip().removesuffix("/.git"))
        if (main / ".venv" / "bin" / "ruff").exists():
            return main / ".venv"
    return ROOT / ".venv"


VENV = _venv()


def _run(cwd: pathlib.Path, gate: pathlib.Path = GATE) -> subprocess.CompletedProcess:
    """Run a gate script against `cwd`, with this checkout's tools on the search path."""
    env = {**os.environ, "CREW_ROOT": str(cwd), "CREW_VENV": str(VENV)}
    #: check=False throughout this file: the exit code is the thing under test.
    return subprocess.run(["bash", str(gate)], cwd=cwd, env=env, check=False,
                          capture_output=True, text=True, timeout=300)


@pytest.fixture
def repo(tmp_path):
    """A one-commit git repo on main, with this repo's ruff and pyright configuration.

    The gate reads uncommitted and untracked work as well as committed, so a test only has
    to drop a file in. The pyproject is copied rather than invented: a gate judged against
    a hand-written config is judged against a config nobody ships.
    """
    def git(*args):
        subprocess.run(["git", *args], cwd=tmp_path, check=True,
                       capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "test@example.invalid")
    git("config", "user.name", "test")
    shutil.copy(ROOT / "pyproject.toml", tmp_path / "pyproject.toml")
    git("add", "pyproject.toml")
    git("commit", "-q", "-m", "base")
    return tmp_path


needs_tools = pytest.mark.skipif(
    not (VENV / "bin" / "ruff").exists(),
    reason=f"no ruff at {VENV}/bin/ruff nor in the main checkout; the gate reports BLIND")


@needs_tools
def test_incident_a_python_program_without_a_py_extension_is_checked(repo):
    """The incident. `scripts/estate-snapshot` is this file, minus 500 lines."""
    (repo / "estate-thing").write_text(DIRTY_PY)

    out = _run(repo).stdout
    assert "estate-thing" in out, (
        "the gate ran over a python program with a shebang and no .py and never named it. "
        f"This is the incident, unchanged:\n{out}")
    assert "UP031" in out, f"it opened the file and did not report its finding:\n{out}"


# `test_the_gate_on_main_was_blind_to_the_same_file` stood here and is deleted.
#
# It was the differential oracle for the widening: fetch the gate at
# `git merge-base HEAD origin/main`, run it on the same input, assert it does NOT name the
# file. That is what proved the test above was measuring the change rather than a gate that
# names every file it sees. It did its job -- the run is on PR #149, and the committed
# evidence image `docs/evidence/the-standard-can-see-a-script-without-py.png` keeps it.
#
# #149 merged as 7f1ae02, so the merge base now IS the widened gate. The oracle compares
# the gate against itself and fails, correctly and permanently. Rung 3 in AGENTS.md says
# it in one line: "A differential test is a migration tool, not a permanent test: delete it
# when the old implementation goes." The old implementation is gone.
#
# Pinning the oracle to 2249494 instead would keep it green forever, which is the argument
# against it: a test that cannot fail for any reason a reader would act on is a `git show`
# on every run and an assertion about a commit nobody will edit.


@needs_tools
def test_a_clean_shebang_python_file_is_not_reported(repo):
    """The paired control. A checker only ever seen complaining has not been shown to be
    reading the file -- it may be complaining about the file's existence. This one is
    clean and must produce no would-fail verdict (LAW 38)."""
    (repo / "estate-thing").write_text(CLEAN_PY)

    r = _run(repo)
    assert "estate-thing" in r.stdout, "the control was not looked at either"
    assert "WOULD-FAIL" not in r.stdout, (
        f"a clean file was reported as failing, which makes the report useless:\n{r.stdout}")
    assert r.returncode == 0, f"a clean tree did not pass:\n{r.stdout}"


@needs_tools
def test_the_new_coverage_reports_and_does_not_yet_block(repo):
    """Report-only, per docs/STANDARDS.md "Widening a gate".

    Widening the selection and enforcing it in one change turns branches red on findings
    their authors did not write, and a red check everyone learns to ignore is no gate.
    So the finding is printed, the verdict says WOULD-FAIL, and the exit code stays 0.

    This assertion is the one the flip PR inverts, and it is why the flip is visible in a
    diff rather than a side effect of some other change.
    """
    (repo / "estate-thing").write_text(DIRTY_PY)

    r = _run(repo)
    assert "WOULD-FAIL" in r.stdout, f"the report gave no verdict to quote:\n{r.stdout}"
    assert r.returncode == 0, (
        "the newly-visible file changed the exit code. New coverage lands report-only "
        f"first; flipping it is its own PR:\n{r.stdout}")


@needs_tools
def test_a_py_file_with_a_finding_still_blocks(repo):
    """The other half of the pair: report-only must not have loosened what was enforced.

    A widening that quietly turned the existing Python check into a report would satisfy
    every assertion above and remove the gate.
    """
    (repo / "thing.py").write_text(DIRTY_PY)

    r = _run(repo)
    assert r.returncode == 1, (
        f"a .py file breaking the standard no longer fails the gate:\n{r.stdout}")


@needs_tools
def test_shell_without_an_extension_is_still_checked(repo):
    """The shebang sniff for shell predates this change and must survive it -- the point
    of the PR is that both languages are selected the same way, not that Python took the
    shell rule and shell lost it."""
    (repo / "some-command").write_text(CLEAN_SH)

    out = _run(repo).stdout
    #: The count line, because a clean shellcheck run prints no filenames -- asserting on
    #: the name here would fail against a working gate.
    assert "0 python, 1 shell" in out, f"the shell sniff stopped working:\n{out}"
