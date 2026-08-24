"""A verify.d gate that could not parse itself exited 0, and the harness counted it PASS.

INCIDENT, 2026-08-24. `scripts/verify.d/15-code-standard.sh` carried a case pattern's
closing paren inside a command substitution:

    case "$f" in *.py) continue;; esac

bash 3.2 -- `/bin/bash` on every Mac in this estate, and what a launchd job with no PATH
resolves `bash` to -- cannot parse that. It printed a syntax error, skipped the whole
substitution, ran on with the loop variable unbound, and **exited 0**. `run_all` in
scripts/verify.sh looked only at the exit code, so the dead gate reported PASS and every
"python by shebang" count it printed on a Mac was fabricated.

Nothing upstream sees it. Measured that day, both bashes present on this machine:

    bash 3.2.57  -n  ->  rc=0        the file "parses"
    bash 5.2.32  -n  ->  rc=0        the file "parses"
    bash 3.2.57 run  ->  rc=0        prints the syntax error, exits 0

`bash -n` cannot help, under either version, because bash defers the body of `$( )` to
expansion and `-n` never reaches inside. ShellCheck implements its own parser and calls the
file clean. CI runs bash 5 on ubuntu-latest, where the construct also runs, so CI was green
the whole time.

So the class is not "this construct". A second, unrelated construct produced the identical
outcome the same day -- an apostrophe in a comment inside `$( )`, which bash 3.2 lexes as an
opening quote. The class is **a check whose own crash cannot lower its verdict**, and the
guard is at the harness, where every gate passes through, reading the only evidence that
exists: the message bash prints when its own parser gives up.

Rung 4, incident tests, one per bug, named for the bug.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify.sh"

#: The exact shape that broke 15-code-standard.sh, reduced to a gate. It exits 0 and prints
#: a count, and the count is wrong -- which is the whole point: a fabricated number is not
#: distinguishable from a real one by looking at it.
CANARY = """\
#!/usr/bin/env bash
ALL="a.py
b.txt"
PY="$(printf '%s\\n' "$ALL" | while read -r f; do
  case "$f" in *.py) continue;; esac
  echo "$f"
done)"
echo "counted $(printf '%s\\n' "$PY" | grep -c .) file(s)"
exit 0
"""

#: Same script, one character different: the leading paren that makes bash 3.2 able to parse
#: it. This is the must-permit half. A guard only ever seen refusing has never been shown to
#: permit, and a guard that refuses correct work is an outage (LAW 38).
CONTROL = CANARY.replace('in *.py)', 'in (*.py)')


def _old_bash() -> str:
    """Path to bash 3.x on this machine, or "" if there is none.

    The incident is specific to bash 3.2. On a box that has no bash 3.x -- every Linux
    runner, including this repo's CI -- there is nothing to reproduce, so these tests skip
    rather than pass. A skip says "not checked here"; a pass would say "checked, fine",
    which is the lie that let this ship.

    Returns "" rather than None so callers need no narrowing to pass the result straight to
    subprocess. `pytest.skip` is a NoReturn in principle, but pyright did not narrow through
    it here and produced five errors that only CI saw, so the type carries the guarantee
    instead of the control flow.
    """
    for candidate in ("/bin/bash",):
        if not shutil.which(candidate):
            continue
        out = subprocess.run(
            [candidate, "--version"], check=False, capture_output=True, text=True
        ).stdout
        if "version 3." in out:
            return candidate
    return ""


@pytest.fixture()
def gate_dir(tmp_path: Path) -> Path:
    """A throwaway checkout holding scripts/verify.sh and exactly one gate.

    verify.sh finds its gates by `dirname $BASH_SOURCE/..`, so the copy has to sit at the
    same relative path. Nothing else from the repo is needed.
    """
    (tmp_path / "scripts" / "verify.d").mkdir(parents=True)
    shutil.copy(VERIFY, tmp_path / "scripts" / "verify.sh")
    return tmp_path


def _run(root: Path, body: str, bash: str) -> subprocess.CompletedProcess[str]:
    gate = root / "scripts" / "verify.d" / "99-canary.sh"
    gate.write_text(body)
    return subprocess.run(
        [bash, str(root / "scripts" / "verify.sh"), "99"],
        check=False,
        capture_output=True,
        text=True,
        cwd=root,
        # A launchd job with no PATH is how the failing interpreter gets chosen in the first
        # place, so the reproduction sets the same one rather than inheriting the shell's.
        env={"PATH": "/usr/bin:/bin", "HOME": str(root)},
    )


def test_a_gate_that_cannot_parse_itself_does_not_report_pass(gate_dir: Path) -> None:
    bash = _old_bash()
    if not bash:
        pytest.skip("no bash 3.x here, so the parse failure cannot be reproduced")

    got = _run(gate_dir, CANARY, bash)

    assert "VERDICT: PASS" not in got.stdout, (
        "the gate could not parse itself and the harness still called it PASS:\n" + got.stdout
    )
    assert "VERDICT: FAIL" in got.stdout, got.stdout
    assert got.returncode != 0, "a run containing a dead gate must not exit 0"


def test_the_gate_still_exits_zero_by_itself(gate_dir: Path) -> None:
    """The exit code is not the evidence, which is why the harness cannot rely on it.

    Asserted so that the reason for the guard stays visible: if some future bash makes this
    a non-zero exit, this test fails and the guard can be reconsidered rather than kept out
    of superstition.
    """
    bash = _old_bash()
    if not bash:
        pytest.skip("no bash 3.x here, so the parse failure cannot be reproduced")

    gate = gate_dir / "scripts" / "verify.d" / "99-canary.sh"
    gate.write_text(CANARY)
    got = subprocess.run([bash, str(gate)], check=False, capture_output=True, text=True)

    assert got.returncode == 0, "if this is non-zero, the exit code alone would have caught it"
    assert "syntax error" in got.stderr, got.stderr


def test_a_gate_that_parses_is_still_allowed_to_pass(gate_dir: Path) -> None:
    """The must-permit half, in the same file as the must-refuse half."""
    bash = _old_bash()
    if not bash:
        pytest.skip("no bash 3.x here, so the parse failure cannot be reproduced")

    got = _run(gate_dir, CONTROL, bash)

    assert "VERDICT: PASS" in got.stdout, (
        "correct work was refused, which is the outage LAW 38 names:\n" + got.stdout
    )
    assert got.returncode == 0, got.stdout


def test_a_gate_reporting_another_files_syntax_error_is_not_caught_by_it(gate_dir: Path) -> None:
    """15-code-standard.sh prints other files' parse errors. That must not fail it.

    This is the false positive the guard was most likely to have, so it is asserted rather
    than reasoned about: the guard anchors on the checked file's own path, so another path
    in the same output is ignored.
    """
    bash = _old_bash()
    if not bash:
        pytest.skip("no bash 3.x here, so the parse failure cannot be reproduced")

    broken = gate_dir / "someone-elses-file.sh"
    broken.write_text('f() {\n  echo "unterminated\n')
    body = (
        "#!/usr/bin/env bash\n"
        f'{bash} -n "{broken}" 2>&1 || true\n'
        f'{bash} -n "{broken}" >&2 2>&1 || true\n'
        "exit 0\n"
    )

    got = _run(gate_dir, body, bash)

    assert "VERDICT: PASS" in got.stdout, (
        "a gate was failed for reporting a syntax error it was asked to find:\n"
        + got.stdout
        + got.stderr
    )
