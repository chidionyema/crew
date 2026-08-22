"""Run the executable Monday test for one checkpoint, and read the verdict.

A runner that reports success because it ran nothing is the failure mode this
module exists to stop. `behave` exits 0 having matched no scenarios at all, and
`pytest` exits 5 having collected none, either of which would tick a checkbox on
an empty run. Every result carries the counts, and a pass needs at least one
case to have passed.

Two runners are understood. `behave` takes `--tags=@cp1` and a checkpoint owns a
Gherkin scenario. `pytest` takes `-m cp1` and a checkpoint owns tests marked
`@pytest.mark.cp1`. Which one is in use is read off the configured command, so a
repo picks its runner by writing the command it already runs.
"""

from __future__ import annotations

import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .errors import CrewError

COUNTS_RE = re.compile(
    r"^(?P<n>\d+) scenarios? (?:passed|failed)", re.MULTILINE
)
SUMMARY_RE = re.compile(
    r"^(?P<passed>\d+) scenarios? passed, (?P<failed>\d+) failed"
    r"(?:, (?P<error>\d+) error)?"
    r"(?:, (?P<skipped>\d+) skipped)?",
    re.MULTILINE,
)

# pytest's last line: "1 failed, 13 passed in 1.98s", with or without the "=" rule
# around it. "no tests ran in 0.01s" carries no counts, which is the empty run
# this module refuses, so it must not match.
PYTEST_SUMMARY_RE = re.compile(
    r"^=*\s*(?P<counts>\d+ [a-z]+(?:,\s*\d+ [a-z]+)*)"
    r"(?:\s*\([^)]*\))?\s*in \d[\d.]*s",
    re.MULTILINE,
)
PYTEST_PAIR_RE = re.compile(r"(\d+) ([a-z]+)")


def runner_kind(command_template: str) -> str:
    """behave, pytest, or unknown, read off the command the repo already runs."""
    c = command_template.lower()
    if "behave" in c:
        return "behave"
    if "pytest" in c:
        return "pytest"
    return "unknown"


@dataclass(frozen=True)
class Result:
    cp: str
    tag: str
    command: str
    exit_code: int
    output: str
    scenarios_passed: int
    scenarios_failed: int

    @property
    def ran_nothing(self) -> bool:
        return self.scenarios_passed + self.scenarios_failed == 0

    @property
    def passed(self) -> bool:
        return self.exit_code == 0 and self.scenarios_failed == 0 and not self.ran_nothing

    @property
    def verdict(self) -> str:
        if self.passed:
            return "PASS"
        if self.ran_nothing:
            return "FAIL (no scenarios matched)"
        return "FAIL"


def tag_for(cp: str) -> str:
    return "@" + cp.strip().lower()


def find_feature(features_dir: Path, tag: str) -> Path | None:
    if not features_dir.is_dir():
        return None
    for f in sorted(features_dir.rglob("*.feature")):
        if tag in f.read_text(errors="replace"):
            return f
    return None


def find_marker(tests_dir: Path, cp: str) -> Path | None:
    """The python file carrying @pytest.mark.cp1 for this checkpoint."""
    if not tests_dir.is_dir():
        return None
    want = f"pytest.mark.{cp.lower()}"
    for f in sorted(tests_dir.rglob("*.py")):
        if want in f.read_text(errors="replace"):
            return f
    return None


def find_case(kind: str, root: Path, features_dir: str, tag: str, cp: str) -> Path | None:
    """Where this checkpoint's executable test lives, whichever runner is in use."""
    if kind == "pytest":
        return find_marker(root / features_dir, cp)
    return find_feature(root / features_dir, tag)


def parse_counts(output: str) -> tuple[int, int]:
    """(passed, failed). An unreadable summary is (0, 0), which reads as an
    empty run and fails, because a runner whose output cannot be read has not
    proved anything."""
    m = SUMMARY_RE.search(output)
    if m:
        return (int(m.group("passed")), int(m.group("failed")))
    m = PYTEST_SUMMARY_RE.search(output)
    if not m:
        return (0, 0)
    counts = dict((k, int(n)) for n, k in PYTEST_PAIR_RE.findall(m.group("counts")))
    # An error is a failure. A test that could not even start is not a pass.
    failed = counts.get("failed", 0) + counts.get("error", 0) + counts.get("errors", 0)
    return (counts.get("passed", 0), failed)


def run(root: Path, command_template: str, cwd: str, cp: str, timeout: int = 3600) -> Result:
    tag = tag_for(cp)
    command = command_template.format(tag=tag, cp=cp.lower(), CP=cp.upper())
    workdir = (root / cwd).resolve()
    if not workdir.is_dir():
        raise CrewError(f"bdd_cwd does not exist: {workdir}")
    try:
        p = subprocess.run(
            shlex.split(command), cwd=workdir, capture_output=True, text=True, timeout=timeout
        )
        output = (p.stdout or "") + (p.stderr or "")
        code = p.returncode
    except FileNotFoundError as e:
        raise CrewError(f"cannot run the BDD command `{command}`: {e}") from e
    except subprocess.TimeoutExpired:
        output = f"timed out after {timeout}s"
        code = 124
    passed, failed = parse_counts(output)
    return Result(
        cp=cp.upper(), tag=tag, command=command, exit_code=code,
        output=output, scenarios_passed=passed, scenarios_failed=failed,
    )
