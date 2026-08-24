"""PR #166, 2026-08-24: the code standard reported 5 type errors against correct code.

The file under review took a `str | None` from `shutil.which` and guarded it with
`pytest.skip()`, which is typed `NoReturn`, so the value was `str` at every later use.
pyright agreed -- when it could see pytest. In CI it could not, the narrowing vanished,
and the gate printed five errors on lines 117, 139, 151 and 179 without ever saying that
it had read the file with pytest invisible. `reportMissingImports = "warning"` in
pyproject.toml turned the admission into a warning, and the block that prints the report
filtered to `severity == "error"`, so the warning was dropped and only its consequences
were shown. The author's code was correct and the gate spent a review cycle on it.

crew#164, clause 1: a check that cannot reach its evidence returns BLIND. This one
returned a verdict.

Rung 4, one incident test named for the bug. It does not run pyright -- it reads the
python block OUT OF scripts/verify.d/15-code-standard.sh and feeds it reports, the same
way tests/test_incident_the_review_gate_read_a_whole_line_as_a_name.py runs the `grep -Po`
patterns out of review-gate.yml. So an edit to that block that breaks this rule fails a
test here rather than a pull request somewhere else.

Both directions are asserted, because a guard that refuses correct work is an outage
(LAW 38): `test_the_imports_that_are_meant_to_be_unresolvable_stay_clean` is main's real
case -- `datamap` and `founder_board` are local modules no requirements file names and
this interpreter cannot import either. Measured on main the day this was written, with
the deps visible: 3 unresolved diagnostics, 0 BLIND.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

GATE = Path(__file__).resolve().parents[1] / "scripts" / "verify.d" / "15-code-standard.sh"


def _block() -> str:
    """The python heredoc the gate runs on pyright's report."""
    text = GATE.read_text()
    m = re.search(r"<<'PYEOF'\n(.*?)\nPYEOF\n", text, re.DOTALL)
    assert m, f"no PYEOF heredoc in {GATE} -- this test reads the real block, not a copy"
    return m.group(1)


def _report(*, files: int = 1, unresolved: tuple[str, ...] = (), errors: int = 0) -> dict:
    diags: list[dict] = []
    for mod in unresolved:
        diags.append({
            "file": "/repo/x.py",
            "severity": "warning",
            "rule": "reportMissingImports",
            "message": f'Import "{mod}" could not be resolved',
            "range": {"start": {"line": 0, "character": 0}},
        })
    for i in range(errors):
        diags.append({
            "file": "/repo/x.py",
            "severity": "error",
            "message": "Argument of type \"str | None\" cannot be assigned to parameter",
            "range": {"start": {"line": i, "character": 0}},
        })
    return {"generalDiagnostics": diags, "summary": {"filesAnalyzed": files}}


def _run(tmp_path: Path, report: dict, requirements: str | None) -> subprocess.CompletedProcess[str]:
    (tmp_path / "report.json").write_text(json.dumps(report))
    if requirements is not None:
        (tmp_path / "requirements-dev.txt").write_text(requirements)
    return subprocess.run(
        [sys.executable, "-c", _block(), str(tmp_path / "report.json")],
        check=False, capture_output=True, text=True, cwd=tmp_path,
    )


def test_a_declared_dependency_pyright_cannot_see_is_blind(tmp_path: Path) -> None:
    # Signal 2. A name requirements-dev.txt declares, which this interpreter also cannot
    # import -- so only the declaration says it should have been there. That is the CI
    # shape: the deps go into .venv and pyright resolves somewhere else.
    got = _run(tmp_path, _report(unresolved=("notarealpackage9",), errors=5),
               "notarealpackage9>=1\n")
    assert got.returncode == 2, f"graded instead of reporting BLIND:\n{got.stdout}"
    assert "BLIND" in got.stdout
    assert "notarealpackage9" in got.stdout


def test_pyright_and_the_interpreter_disagreeing_is_blind(tmp_path: Path) -> None:
    # Signal 1. pytest is importable right here -- this is a pytest process -- and the
    # report says pyright, pointed at this same interpreter, could not find it. No
    # requirements file at all, so signal 2 cannot be what fires.
    got = _run(tmp_path, _report(unresolved=("pytest",), errors=5), None)
    assert got.returncode == 2, f"graded instead of reporting BLIND:\n{got.stdout}"
    assert "BLIND" in got.stdout


def test_the_error_that_started_this_is_not_reported_as_the_authors_fault(tmp_path: Path) -> None:
    got = _run(tmp_path, _report(unresolved=("pytest",), errors=5), "pytest>=8\n")
    assert "5 error(s)" not in got.stdout, (
        "the five errors are downstream of an import pyright could not read; printing "
        "them as the verdict is the incident this test is named for:\n" + got.stdout)


def test_the_imports_that_are_meant_to_be_unresolvable_stay_clean(tmp_path: Path) -> None:
    # LAW 38. main's real case: local modules reached through sys.path at run time, named
    # in no requirements file and not importable here. A guard that calls this BLIND takes
    # the whole standard out on every branch.
    got = _run(tmp_path, _report(unresolved=("datamap", "founder_board")),
               "pytest>=8\nruff>=0.14\n")
    assert got.returncode == 0, f"refused correct work:\n{got.stdout}"
    assert "BLIND" not in got.stdout


def test_real_errors_with_every_import_resolved_still_fail(tmp_path: Path) -> None:
    got = _run(tmp_path, _report(errors=3), "pytest>=8\n")
    assert got.returncode == 1
    assert "3 error(s) over 1 file(s)." in got.stdout


def test_analysing_no_files_is_still_blind(tmp_path: Path) -> None:
    # Behaviour that predates this fix, asserted so the insertion above it cannot displace it.
    got = _run(tmp_path, _report(files=0), "pytest>=8\n")
    assert got.returncode == 2
    assert "BLIND" in got.stdout


@pytest.mark.parametrize(
    ("line", "expected"),
    [('tomli>=2 ; python_version < "3.11"', "tomli"),
     ("dbt-duckdb>=1.11", "dbt_duckdb"),
     ("hypothesis>=6", "hypothesis"),
     ("# a comment", "")],
)
def test_requirements_names_are_read_the_way_the_block_reads_them(line: str, expected: str) -> None:
    # The one line of parsing in the block, pinned. `dbt_duckdb` is the residual the block
    # documents: the distribution is dbt-duckdb and it imports as `dbt`, so signal 2 will
    # never match it and signal 1 has to carry that package alone.
    got = re.split(r"[<>=!;\[\s#]", line.strip(), maxsplit=1)[0].lower().replace("-", "_")
    assert got == expected
