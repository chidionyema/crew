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
"""
import pathlib
import re
import sys

import pytest

try:  # tomllib is 3.11+; tomli is its backport and is already a dependency below that.
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - only taken on 3.10
    import tomli as tomllib

PYPROJECT = pathlib.Path(__file__).resolve().parents[1] / "pyproject.toml"


def _config() -> dict:
    return tomllib.loads(PYPROJECT.read_text())


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

    tree = pathlib.Path(__file__).resolve().parents[1]
    users = [p for p in tree.rglob("*.py")
             if ".venv" not in p.parts and "node_modules" not in p.parts
             and re.search(rf"^\s*from datetime import .*\b{name}\b", p.read_text(),
                           re.MULTILINE)]
    if not users:
        pytest.skip(f"nothing in the tree imports datetime.{name}")
    assert hasattr(datetime, name), (
        f"{len(users)} file(s) do `from datetime import {name}`, which Python "
        f"{_running()[0]}.{_running()[1]} does not have: "
        f"{', '.join(str(p.relative_to(tree)) for p in users[:5])}"
    )
