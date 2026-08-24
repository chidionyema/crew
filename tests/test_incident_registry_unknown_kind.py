"""A registry entry with a mistyped `kind` used to report a full store as an empty one.

THE INCIDENT. `science/sources.json` declares each store's `kind`. `read_rows` branched
`jsonl` / `jsonl-dir` / else, and the else read the file as a single JSON document. So
`kind: "Jsonl"` -- one capital letter -- was accepted by the registry and its store was
parsed as one malformed document. Measured on a real two-row file before the fix:

    registry accepted kind='Jsonl'
    read_rows with kind='Jsonl'    : 0 rows, 1 bad
    the file really holds          : 2 rows

Nothing failed. The source appeared in the collector's report as a store that happened to
be empty, which is a thing stores are genuinely allowed to be. Found by a peer's review of
PR #110, not by any test.

WHAT THIS ASSERTS, AND WHY IT IS A RULE AND NOT AN IMPLEMENTATION. The rule is "an
unrecognised kind is refused, loudly, before anything reads a byte". These tests would
survive `read_rows` being deleted entirely and replaced by DuckDB, which is exactly what
crew#74 is going to do to it -- they name the registry's contract, not the parser's shape.

Rung 4 of the testing doctrine: one incident test per bug, named for the bug.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCIENCE = Path(__file__).resolve().parent.parent / "science"


def write_registry(tmp_path: Path, kind: str) -> Path:
    """A one-source registry over a store that really does hold two rows."""
    (tmp_path / "store.jsonl").write_text(
        '{"at":"2026-08-24T00:00:00","x":1}\n'
        '{"at":"2026-08-24T00:00:01","x":2}\n'
    )
    registry = tmp_path / "sources.json"
    registry.write_text(json.dumps({
        "version": 1,
        "roots": {"home": str(tmp_path), "science": str(tmp_path)},
        "default_stale_after_hours": 48,
        "sources": [{"name": "s", "root": "home", "path": "store.jsonl",
                     "kind": kind, "time_field": "at"}],
        "declined": [],
    }))
    return registry


def load(tmp_path: Path, kind: str) -> subprocess.CompletedProcess:
    """Import collect.py against that registry, in a subprocess.

    A subprocess because `load_registry` runs at import and refuses with `sys.exit`, and
    because collect.py is imported at module scope by two other tools -- catching SystemExit
    in-process would leave a half-imported module behind for whatever runs next.
    """
    return subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, %r); import collect" % str(SCIENCE)],
        env={"SCIENCE_REGISTRY": str(write_registry(tmp_path, kind)),
             "ESTATE_HOME": str(tmp_path),
             "SCIENCE_WAREHOUSE": str(tmp_path / "w.db"),
             "PATH": "/usr/bin:/bin"},
        capture_output=True, text=True, timeout=60,
    )


@pytest.mark.parametrize("kind", ["Jsonl", "JSONL", "jsonl ", "jsonlines", "", "jsonl-directory"])
def test_incident_registry_unknown_kind_is_refused(tmp_path, kind):
    """The incident itself: anything outside the closed set stops the run, and says so."""
    result = load(tmp_path, kind)
    assert result.returncode != 0, (
        f"registry accepted kind={kind!r}. That is the incident: the store behind it reads "
        f"as empty and no one is told."
    )
    assert "unknown kind" in result.stderr, result.stderr
    #: The message names the offender and the alternatives, because the person reading it
    #: is looking at a typo they cannot see.
    assert repr(kind) in result.stderr, result.stderr
    assert "jsonl-dir" in result.stderr, result.stderr


@pytest.mark.parametrize("kind", ["jsonl", "jsonl-dir", "json"])
def test_the_three_real_kinds_still_load(tmp_path, kind):
    """The other direction, which is the half that makes the first half worth anything.

    A guard that refuses everything passes the test above and is an outage (LAW 38). Each
    kind the registry is meant to accept must still import cleanly.
    """
    result = load(tmp_path, kind)
    assert result.returncode == 0, result.stderr


def test_read_rows_refuses_an_unknown_kind_when_called_directly(tmp_path):
    """`read_rows` is called by duckdb_differential.py, which does not go through the registry.

    Before the fix this returned ([], 1) -- an empty store with one bad line -- for any kind
    it did not recognise. The registry now refuses first, so this branch is unreachable
    through normal use; it is asserted because "unreachable" is a claim about today's
    callers and this function has more than one.
    """
    sys.path.insert(0, str(SCIENCE))
    import collect  # noqa: E402  imported here so a registry failure cannot break collection

    store = tmp_path / "store.jsonl"
    store.write_text('{"at":"2026-08-24T00:00:00","x":1}\n')
    with pytest.raises(ValueError, match="unknown kind"):
        collect.read_rows(store, "Jsonl")


def test_the_estates_own_registry_only_uses_known_kinds():
    """The live sources.json, graded against the same closed set.

    This is the check that would have caught the typo on the day it was written, and it
    costs one import.
    """
    sys.path.insert(0, str(SCIENCE))
    import collect  # noqa: E402

    declared = {kind for _path, kind, _tf in collect.SOURCES.values()}
    assert declared <= set(collect.KINDS), f"sources.json uses {declared - set(collect.KINDS)}"
