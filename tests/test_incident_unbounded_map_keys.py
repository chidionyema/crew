"""Incident: 800 of the estate's 1064 "field paths" were data sitting in key position.

Measured 2026-08-24. `science/shapes.json` reported 810 fields for `agent_cert`, a source
holding 12 rows. The rows carried a dict keyed by certification test ID:

    rows.MAE-001.blocked_reason
    rows.REQ-062.phase
    ...  160 test IDs x 5 attributes = 800 paths

`sh_fields` recursed into every dict, so a dict used as a map was walked as though its keys
were schema. Nothing was wrong with the data. The measurement was wrong, and it was wrong in
the direction that matters: a schema that grows with the rows can never have a contract
written against it, because the next certification run invents new keys.

These tests assert the rule, not the implementation: a dict whose keys are data is recorded
once, and a dict whose keys are schema is still walked. They are written to survive a rewrite
of the detection heuristic.
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "science"))

from datamap import sh_fields  # noqa: E402


def _paths(rows):
    keys, _ = sh_fields(rows)
    return set(keys)


def test_map_keyed_by_data_does_not_become_one_field_per_key():
    """The incident itself: 160 keys x 5 attributes must not become 800 paths."""
    rows = [{
        "agent": "claude",
        "rows": {
            f"REQ-{i:03d}": {"phase": "run", "state": "pass", "detail": "", }
            for i in range(160)
        },
    }]
    paths = _paths(rows)

    assert "rows" in paths, "the map itself must still be recorded as a field"
    assert not any(p.startswith("rows.REQ-") for p in paths), \
        "a key that is data must never appear in a field path"
    # The child shape survives, recorded once, so the contract can still describe it.
    for attr in ("phase", "state", "detail"):
        assert f"rows.*.{attr}" in paths, f"child field {attr} was lost, not summarised"
    assert len(paths) < 10, f"expected a bounded schema, got {len(paths)} paths"


def test_field_count_does_not_grow_with_the_number_of_rows():
    """The property that makes a schema contractable: adding data adds no fields."""
    def rows_with(n):
        return [{"rows": {f"K{i}": {"a": 1, "b": 2} for i in range(n)}}]

    small = _paths(rows_with(20))
    large = _paths(rows_with(2000))
    assert small == large, (
        "the field set changed when only the row count changed; a schema that grows "
        "with the data is not a schema"
    )


def test_a_genuinely_wide_record_is_still_walked():
    """The paired control. A guard that refuses correct work is an outage (LAW 38).

    A record with many keys whose values are unrelated is a record, not a map, and its
    fields must still be reported individually.
    """
    rows = [{
        "cfg": {
            "host": "localhost", "port": 8080, "retries": 3, "debug": False,
            "name": "estate", "region": "eu", "tier": "free", "quota": 100,
            "owner": "platform", "created": "2026-08-24", "ttl": 60, "tags": "a,b",
            "enabled": True, "path": "/tmp", "mode": "ro",
        }
    }]
    paths = _paths(rows)
    assert "cfg.host" in paths and "cfg.port" in paths and "cfg.mode" in paths, \
        "a wide record was misread as a map and its fields were collapsed"
    assert "cfg.*" not in {p[:5] for p in paths}


def test_a_small_uniform_dict_is_a_record_not_a_map():
    """Below the key threshold, uniform children are still schema.

    A record can legitimately hold two or three sub-objects of the same shape --
    `{"before": {...}, "after": {...}}` is a record, not a map -- and collapsing it
    would lose real field names.
    """
    rows = [{
        "diff": {
            "before": {"count": 1, "at": "x"},
            "after": {"count": 2, "at": "y"},
        }
    }]
    paths = _paths(rows)
    assert "diff.before.count" in paths and "diff.after.count" in paths, \
        "a two-key record was collapsed as though it were a map"


def test_nested_maps_are_summarised_at_every_depth():
    """A map inside a record still collapses, so the fix is not top-level only."""
    rows = [{
        "run": {
            "id": "r1",
            "results": {f"T{i}": {"ok": True, "ms": i} for i in range(50)},
        }
    }]
    paths = _paths(rows)
    assert "run.id" in paths
    assert "run.results" in paths
    assert "run.results.*.ok" in paths
    assert not any(p.startswith("run.results.T") for p in paths)
