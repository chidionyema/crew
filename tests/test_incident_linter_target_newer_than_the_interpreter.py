"""Incident: the code standard auto-fixed a line the interpreter could not import.

Measured 2026-08-24 on `fix/a-decline-can-cover-a-directory`, after `ruff check --fix`:

    $ .venv/bin/python science/collect.py
      File ".../science/collect.py", line 61, in <module>
        from datetime import UTC, datetime
    ImportError: cannot import name 'UTC' from 'datetime'
    (/Users/chidionyema/anaconda3/lib/python3.10/datetime.py)

    $ bash scripts/verify.d/15-code-standard.sh
    PASS: every file this branch touched meets the standard.

`pyproject.toml` said `target-version = "py311"`. The venv every session runs gates
through was 3.10.9. So ruff applied UP017 -- `timezone.utc` -> `datetime.UTC`, added in
3.11 -- and then graded its own rewrite as clean, because it was clean *for 3.11*. The
gate printed PASS over code that could not be imported. It was caught by running the
collector, not by any checker.

That is the exact defect class the code standard exists to stop, produced by the code
standard. A linter configured for a newer Python than the runtime is not a strict
checker; it is a generator of false greens, and it gets worse the stricter it is.

The rule, asserted here rather than in prose: the version the linters are configured for
is never newer than the interpreter that runs this suite. Older is fine and normal --
code written for 3.10 runs on 3.11, which is why CI on 3.11 stays green against a py310
target. Newer is the break.

This is a test rather than a line in a shell gate because it must hold for every
interpreter anyone runs the suite on, including runners this repo does not configure, and
because the suite already blocks CI.

The same seam reopened on 2026-08-24 in a place these tests could not see. "The
interpreter that runs this suite" is not the interpreter that runs every file: launchd
hands `scripts/estate-lander` and `science/law_enforcement.py` to /usr/bin/python3, which
is 3.9.6, while ruff graded them at py311. The tests for that are at the foot of this
file, under the banner, and the declaration they check is
`[tool.ruff.per-file-target-version]` in pyproject.toml.
"""
import os
import pathlib
import plistlib
import re
import subprocess
import sys
from xml.parsers.expat import ExpatError

import pytest

try:  # tomllib is 3.11+; tomli is its backport and is already a dependency below that.
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - only taken on 3.10
    import tomli as tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
SKIP = {".venv", "node_modules", ".git", "store", "storage"}


def _config() -> dict:
    return tomllib.loads(PYPROJECT.read_text())


def _python_programs(tree: pathlib.Path) -> list[pathlib.Path]:
    """Every Python program under `tree`: by extension, and by shebang for the rest.

    A file is what its shebang says it is. `rglob("*.py")` stood here and could not see
    `scripts/estate-lander` or `bin/crew` -- the commands a person types the name of, which
    carry no extension because nobody should have to type `.py`. That is the same blind
    spot `scripts/verify.d/15-code-standard.sh` had until #149, one lane over, and it
    matters here because those extensionless commands are exactly the ones launchd runs.
    """
    out = []
    for p in tree.rglob("*"):
        if not p.is_file() or SKIP & set(p.parts):
            continue
        if p.suffix == ".py":
            out.append(p)
            continue
        try:
            if re.match(rb"^#!.*python", p.open("rb").read(60)):
                out.append(p)
        except OSError:  #: unreadable is not "not python" -- but it is not evidence either
            continue
    return out


def _running() -> tuple[int, int]:
    return sys.version_info[0], sys.version_info[1]


def test_ruff_target_version_is_not_newer_than_this_interpreter():
    """`target-version = "py311"` on a 3.10 interpreter is what caused the incident."""
    target = _config()["tool"]["ruff"]["target-version"]
    m = re.fullmatch(r"py(\d)(\d+)", target)
    assert m, f"target-version {target!r} is not in the pyNM form ruff documents"
    configured = (int(m.group(1)), int(m.group(2)))

    assert configured <= _running(), (
        f"ruff is configured for Python {configured[0]}.{configured[1]} but this suite "
        f"runs on {_running()[0]}.{_running()[1]}. `ruff check --fix` will rewrite code "
        f"into syntax this interpreter cannot execute, and the code-standard gate will "
        f"pass it. Either raise the interpreter (see README, 'Tests') or lower "
        f"target-version in pyproject.toml to the oldest Python this code has to run on."
    )


def test_pyright_python_version_is_not_newer_than_this_interpreter():
    """The same rule for the type checker, which decides which stdlib names exist."""
    declared = str(_config()["tool"]["pyright"]["pythonVersion"])
    m = re.fullmatch(r"(\d+)\.(\d+)", declared)
    assert m, f"pythonVersion {declared!r} is not in the N.M form pyright documents"
    configured = (int(m.group(1)), int(m.group(2)))

    assert configured <= _running(), (
        f"pyright is configured for Python {configured[0]}.{configured[1]} but this "
        f"suite runs on {_running()[0]}.{_running()[1]}. It will accept stdlib names "
        f"that do not exist at runtime and report zero errors over them."
    )


def test_the_two_checkers_are_configured_for_the_same_python():
    """One of them being lowered and the other forgotten reopens the same hole."""
    cfg = _config()
    ruff = _config()["tool"]["ruff"]["target-version"]
    pyright = str(cfg["tool"]["pyright"]["pythonVersion"])
    assert ruff == "py" + pyright.replace(".", ""), (
        f"ruff targets {ruff} and pyright targets {pyright}. They grade the same files "
        f"and must agree, or one of them is judging code the other is not."
    )


@pytest.mark.parametrize("name", ["UTC"])
def test_the_specific_name_that_broke_is_importable(name):
    """The incident itself. If this fails, the tree carries a rewrite this Python lacks.

    Not a substitute for the rules above -- it catches one name where they catch the
    class -- but it is the assertion that would have gone red the moment the autofix
    landed, in under a second, without running the collector.
    """
    import datetime

    users = []
    for p in _python_programs(ROOT):
        try:
            src = p.read_text()
        except UnicodeDecodeError:
            continue
        if re.search(rf"^\s*from datetime import .*\b{name}\b", src, re.MULTILINE):
            users.append(p)
    if not users:
        pytest.skip(f"nothing in the tree imports datetime.{name}")
    assert hasattr(datetime, name), (
        f"{len(users)} file(s) do `from datetime import {name}`, which Python "
        f"{_running()[0]}.{_running()[1]} does not have: "
        f"{', '.join(str(p.relative_to(ROOT)) for p in users[:5])}"
    )


# --------------------------------------------------------------------------------------
# The second seam, 2026-08-24. Everything above compares the linter's target to the
# interpreter running THIS SUITE. That is not the interpreter that runs every file.
#
# Two scheduled programs are handed to /usr/bin/python3, which is 3.9.6 on this machine,
# because their launchd plists name it in argv and set no PATH that would find a newer one.
# The linters grade them at py311. Same false green as the incident above, one seam over:
# `ruff check --fix` can rewrite a file into a name its own runtime lacks, `py_compile`
# passes because the rewrite is an attribute access, and the job dies at import.
#
# ruff's `per-file-target-version` states each one's real target. These two tests keep the
# statement honest: one checks it against the machine, one checks the shape of the entries.
# --------------------------------------------------------------------------------------

LAUNCH_AGENTS = pathlib.Path.home() / "Library" / "LaunchAgents"
LAUNCHD_DEFAULT_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"


def _interpreter_for(argv: list[str], env_path: str | None) -> str | None:
    """The python a plist's argv actually gets: named outright, or found on its PATH."""
    for a in argv:
        if re.search(r"/python3?(\.\d+)?$", a):
            return a
    for a in argv:
        if pathlib.Path(a).name.startswith("python"):
            return a
    #: Nothing named, so the program's own shebang decides, and `env python3` walks PATH.
    #:
    #: Take the LOWEST version on that PATH, not the first hit. `command -v python3` answers
    #: "what would run right now", and the answer moves without anything in this repo
    #: changing: estate-snapshot's plist puts /opt/homebrew/bin first, which holds no python3
    #: at all, so it falls through to /usr/local/bin/python3 3.14.6 -- and would fall to
    #: /usr/bin/python3 3.9.6 the day a homebrew python appears there or /usr/local/bin goes.
    #: Grading the file at the first hit told ruff py311, and ruff rewrote four
    #: `dt.timezone.utc` calls to `dt.UTC`, which under 3.9.6 is `AttributeError: module
    #: 'datetime' has no attribute 'UTC'` at line 521, in main() -- at call time, so
    #: `py_compile` passes the file. Not the ImportError at line 8 of this docstring:
    #: collect.py used `from datetime import UTC`, which fails at import; an attribute
    #: access fails only when reached, and line 521 precedes the write at 555, so the job
    #: dies with STATE.md untouched rather than blank.
    #: Found by chidionyema-d1 on PR #159. A checker that reports what it happened to see
    #: rather than what it is allowed to see is the defect this whole file exists for.
    lowest: tuple[tuple[int, ...], str] | None = None
    for entry in (env_path or LAUNCHD_DEFAULT_PATH).split(":"):
        cand = pathlib.Path(entry) / "python3"
        if not (cand.is_file() and os.access(cand, os.X_OK)):
            continue
        got = subprocess.run([str(cand), "-c",
                              "import sys;print('%d.%d' % sys.version_info[:2])"],
                             check=False, text=True, capture_output=True, timeout=30)
        m = re.fullmatch(r"(\d+)\.(\d+)", got.stdout.strip())
        if not m:
            continue
        ver = (int(m.group(1)), int(m.group(2)))
        if lowest is None or ver < lowest[0]:
            lowest = (ver, str(cand))
    return lowest[1] if lowest else None


def _same_program_here(target: pathlib.Path) -> pathlib.Path | None:
    """The path a plist names, expressed as a path in THIS checkout, or None.

    Asked from the plist's side, not from this checkout's side. Walk up from the file
    launchd actually runs until something marks a repo root, take the path relative to it,
    and ask whether this checkout holds the same file. So the question is "does the repo I
    am testing contain the program that job runs", which is the question, and it does not
    care whether this checkout is the main one, a worktree of it, or a separate clone.

    It was written from this checkout's side first: `_checkouts()` matched against ROOT and
    the main checkout found via `git rev-parse --git-common-dir`. That handled a worktree
    and nothing else. chidionyema-03 broke it on review, from a plain clone, and measured
    both halves rather than describing them:

        $ git clone --local ~/dev/code/crew crew-clone-test
        $ python3 -m pytest tests/test_incident_...py -q -rs
        5 passed, 1 skipped
        SKIPPED [1] no launchd job on this machine runs a Python file from this repo

    Green because it saw nothing, one level out from the case it had just fixed. That is
    not academic: the scheduled runner for this suite has to use an isolated clone -- an
    hourly job cannot run pytest in ~/dev/code/crew, which sits on whatever branch another
    session left it on and whose tracked store/ and storage/ pytest writes into. So the
    clone is the case the guard exists for, and it was the one case it could not see.

    From that same clone, this version finds three programs where the old one found zero,
    and the third is the point:

        OK   science/law_enforcement.py   /usr/bin/python3   -> 3.9    py39
        OK   scripts/estate-lander        /usr/bin/python3   -> 3.9    py39
        OK   scripts/estate-snapshot      /usr/local/bin/python3 -> 3.14   py311

    That third line was read the wrong way round when it was written. "3.14 -> py311" is
    what the plist's PATH resolves to on the day the resolver runs, and estate-snapshot was
    left out of the pyproject table on the strength of it. chidionyema-d1 broke that
    reviewing PR #159: the plist sets
    PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin, `/opt/homebrew/bin`
    is FIRST and holds no python3 at all, and the same PATH without /usr/local/bin resolves
    to /usr/bin/python3 3.9.6. Nothing in this repo has to change for the answer to move.
    Meanwhile ruff, told py311, had already rewritten four `dt.timezone.utc` calls in that
    file to `dt.UTC`. Under 3.9.6 that is `AttributeError: module 'datetime' has no
    attribute 'UTC'` at line 521, in main() -- at call time, so `py_compile` passes it. The
    write is at line 555, so the job dies with STATE.md untouched and the page every session
    reads stops moving without going blank.

    So estate-snapshot is now IN the table at py39, and the rule this function serves is
    the lower one: a program whose interpreter comes from PATH is graded at the lowest
    version that PATH can reach, not at what it resolves to today. First-hit resolution is
    the same defect this whole file was opened for, one level up -- a checker reporting
    what it happened to see rather than what it is allowed to see.
    """
    for parent in target.parents:
        #: `.git` is a directory in a clone and a file in a worktree; either marks a root.
        if (parent / ".git").exists() or (parent / "pyproject.toml").is_file():
            here = ROOT / target.relative_to(parent)
            return here.relative_to(ROOT) if here.is_file() else None
    return None


def _scheduled_repo_programs() -> dict[pathlib.Path, str]:
    """Repo files launchd runs, mapped to the python each one is actually handed.

    Read from the plists rather than from a list in this file, because a list in this file
    is a claim about the machine that nothing checks. This is the machine.
    """
    out: dict[pathlib.Path, str] = {}
    for plist in sorted(LAUNCH_AGENTS.glob("*.plist")):
        try:
            spec = plistlib.loads(plist.read_bytes())
        #: plistlib raises InvalidFileException (a ValueError) on a bad binary plist
        #: and lets expat's error through on bad XML. A plist this test cannot read is
        #: launchd's problem, not this test's.
        except (ValueError, OSError, ExpatError):
            continue
        argv = [str(a) for a in spec.get("ProgramArguments", []) if isinstance(a, str)]
        if not argv:
            continue
        env_path = (spec.get("EnvironmentVariables") or {}).get("PATH")
        interp = _interpreter_for(argv, env_path)
        if not interp:
            continue
        for a in argv:
            p = pathlib.Path(a)
            if not p.is_absolute() or not p.is_file():
                continue
            rel = _same_program_here(p.resolve())
            if rel is None:
                continue
            if p.suffix == ".py" or re.match(rb"^#!.*python", p.open("rb").read(60)):
                out[rel] = interp
    return out


def _version_of(interpreter: str) -> tuple[int, int] | None:
    r = subprocess.run([interpreter, "-c",
                        "import sys;print(sys.version_info[0],sys.version_info[1])"],
                       check=False, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    a, b = r.stdout.split()
    return int(a), int(b)


def _declared() -> dict[str, tuple[int, int]]:
    table = _config()["tool"]["ruff"].get("per-file-target-version", {})
    out = {}
    for path, target in table.items():
        m = re.fullmatch(r"py(\d)(\d+)", str(target))
        assert m, f"per-file-target-version[{path!r}] = {target!r} is not in the pyNM form"
        out[path] = (int(m.group(1)), int(m.group(2)))
    return out


@pytest.mark.skipif(not LAUNCH_AGENTS.is_dir(),
                    reason=f"no {LAUNCH_AGENTS}; scheduled jobs are a property of a machine "
                           f"and a CI runner has none to read")
def test_a_scheduled_program_is_linted_for_the_python_that_runs_it():
    """The rule: a file launchd hands to an older python declares that python to ruff.

    This is the test that would have gone red the moment somebody scheduled a program under
    /usr/bin/python3 without saying so, which is how the seam opened.

    Two limits, both measured 2026-08-24 rather than assumed:

    It reads ~/Library/LaunchAgents and not /Library/LaunchDaemons. There are 18
    non-Apple plists there, all vendor (Adobe, Cisco, Docker, Google, Microsoft, Nord,
    Oracle, homebrew, Canon, postgres, Zoom), and `grep -l dev/code/crew` over them
    returns 0. It misses nothing today; an estate daemon added there would be invisible.

    It fires only where the plists are. A GitHub runner has no ~/Library/LaunchAgents, so
    it skips in CI by construction, and no loaded plist runs this suite -- 03 checked
    every argv for pytest, run_tests and verify and found none. The declaration is what
    is enforced everywhere: ruff reads per-file-target-version on every run including
    CI, so the autofix cannot rewrite those two files whoever runs it. Declaration is the
    brace, this test is the belt, and only the belt is machine-local. 03 is landing the
    launchd job that runs the suite here.
    """
    global_target = _config()["tool"]["ruff"]["target-version"]
    m = re.fullmatch(r"py(\d)(\d+)", global_target)
    assert m, f"target-version {global_target!r} is not in the pyNM form"
    default = (int(m.group(1)), int(m.group(2)))
    declared = _declared()

    scheduled = _scheduled_repo_programs()
    if not scheduled:
        pytest.skip("no launchd job on this machine runs a Python file from this repo")

    problems = []
    for rel, interp in sorted(scheduled.items()):
        actual = _version_of(interp)
        if actual is None:
            continue  #: an interpreter that will not answer is not evidence of a version
        want = declared.get(str(rel), default)
        if want > actual:
            problems.append(
                f"  {rel} is run by {interp} (Python {actual[0]}.{actual[1]}) and linted "
                f"at py{want[0]}{want[1]}. Add\n"
                f'      "{rel}" = "py{actual[0]}{actual[1]}"\n'
                f"  under [tool.ruff.per-file-target-version] in pyproject.toml.")
    assert not problems, (
        "a linter is configured for a newer Python than the interpreter that runs the "
        "file. `ruff check --fix` will rewrite it into names that interpreter does not "
        "have, `py_compile` will pass, and the scheduled job will fail at import:\n"
        + "\n".join(problems))


def test_every_per_file_target_names_a_file_that_exists():
    """A stale entry protects nothing and reads as though it does (LAW 28).

    Renaming or deleting a program leaves its declaration behind, still green, still
    claiming a floor for a path nothing runs.
    """
    missing = [p for p in _declared() if not (ROOT / p).exists()]
    assert not missing, (
        "per-file-target-version names path(s) that are not in the tree, so nothing is "
        f"being protected by them: {', '.join(missing)}")
