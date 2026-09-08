"""A module-level path constant used as a default argument is bound once, at import.

2026-09-08: `tests/test_crew508_research_intake.py::test_check_exits_one_on_a_stale_pull`
was red on main and had blocked five unrelated pull requests -- a dependabot bump, two
docs changes, an SBOM change and a board change -- none of which touched research intake.

The cause was `def read_rows(path: pathlib.Path = INTAKE)`. Python evaluates a default
argument once, when the `def` executes, so the test's `monkeypatch.setattr(ri, "INTAKE",
tmp_path / "i.jsonl")` rebound the module global and changed nothing: `main()` went on
reading the real `science/RESEARCH-INTAKE.jsonl`. The test passed for as long as that
real ledger held no candidate older than ANSWER_DAYS, and went red on the day the fourth
one crossed seven days. Nothing in any pull request moved; a date did.

The guard is the shape, not the one function: a default argument that is a bare module
constant naming a path can never be monkeypatched, so a test that tries reads live estate
data instead of its fixture. Resolve inside the body -- `path = INTAKE if path is None
else path` -- and the patch takes.
"""

import ast
import pathlib

import pytest

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"

# Constants whose value is a path into the estate. A default that names one of these is
# the defect; a plain numeric or string tunable (ANSWER_DAYS, BOARD_TOP) is not.
PATHISH = (
    "PATH",
    "PATHS",
    "SOURCES",
    "SOURCE",
    "INTAKE",
    "STATE",
    "LOG",
    "LEDGER",
    "REGISTRY",
    "RECEIPTS",
    "CONFIG",
    "DIR",
    "ROOT",
    "FILE",
    "DB",
    "BOARD",
)


def _is_pathish(name: str) -> bool:
    return name.isupper() and any(name == p or name.endswith("_" + p) for p in PATHISH)


def test_no_module_path_constant_is_a_default_argument():
    offenders = []
    for py in sorted(SCIENCE.rglob("*.py")):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        consts = {
            t.id
            for node in tree.body
            if isinstance(node, ast.Assign)
            for t in node.targets
            if isinstance(t, ast.Name) and _is_pathish(t.id)
        }
        if not consts:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            args = node.args
            for arg, default in zip(
                args.args[len(args.args) - len(args.defaults) :], args.defaults, strict=True
            ):
                if isinstance(default, ast.Name) and default.id in consts:
                    offenders.append(
                        f"{py.relative_to(SCIENCE.parent)}:{node.lineno} "
                        f"{node.name}({arg.arg}={default.id}) -- bound at import; "
                        f"resolve in the body so monkeypatch takes"
                    )
    if offenders:
        pytest.fail("path constants bound as default arguments:\n" + "\n".join(offenders))
