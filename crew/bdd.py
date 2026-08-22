"""Run the executable Monday test for one checkpoint, and read the verdict.

A runner that reports success because it ran nothing is the failure mode this
module exists to stop. `behave` can exit 0 having matched no scenarios at all,
which would tick a checkbox on an empty run. Every result therefore carries the
scenario counts, and a pass needs at least one scenario to have passed.
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


def parse_counts(output: str) -> tuple[int, int]:
    m = SUMMARY_RE.search(output)
    if not m:
        return (0, 0)
    return (int(m.group("passed")), int(m.group("failed")))


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
