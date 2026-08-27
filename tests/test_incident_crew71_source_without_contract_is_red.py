"""crew#71: 28 sources, 1,064 field paths, no owner, method, retention or sensitivity on any.

Rung 4, incident test. The rule: a source in science/sources.json carries all four contract
fields with values from the closed sets, and its owner is a file that exists. The gate is
datamap.py --check, which is where the register is already graded (LAW 50)."""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "science"))
import datamap  # noqa: E402

GOOD = {"name": "x", "owner": "science/datamap.py", "method": "push",
        "retention_days": 30, "sensitivity": "internal"}


def _write(tmp_path, sources):
    d = tmp_path / "science"
    d.mkdir(exist_ok=True)
    f = d / "sources.json"
    f.write_text(json.dumps({"version": 1, "sources": sources}))
    (tmp_path / "science" / "datamap.py").write_text("")  # the owner GOOD names, relative to the repo
    return f


def test_the_committed_register_declares_every_contract():
    assert datamap.contract_violations() == []


def test_a_source_missing_any_field_is_red(tmp_path):
    for field in datamap.CONTRACT_FIELDS:
        s = dict(GOOD)
        del s[field]
        v = datamap.contract_violations(_write(tmp_path, [s]))
        assert any(field in m for m in v), (field, v)


def test_values_outside_the_closed_sets_are_red_and_good_is_green(tmp_path):
    assert datamap.contract_violations(_write(tmp_path, [GOOD])) == []
    for bad in ({"method": "cron"}, {"sensitivity": "secret"}, {"retention_days": 0},
                {"retention_days": "30"}, {"owner": "science/no-such-file.py"}):
        assert datamap.contract_violations(_write(tmp_path, [{**GOOD, **bad}])), bad


def test_a_map_of_scalars_keyed_by_data_folds_to_one_field():
    """Smell 2: spend.by_owner.<project> was 42 fields for one measure (54 -> 6 after)."""
    rows = [{"total": 1.0, "by_owner": {f"proj-{i}": 0.5}} for i in range(datamap.MAP_MIN_KEYS)]
    keys, types = datamap.sh_fields(rows)
    assert set(keys) == {"total", "by_owner.*"} and types["by_owner.*"] == "float"
    # below the threshold, or mixed types, a wide dict stays a record: no fold
    few = [{"by_owner": {f"proj-{i}": 0.5}} for i in range(datamap.MAP_MIN_KEYS - 1)]
    assert "by_owner.*" not in datamap.sh_fields(few)[0]
    mixed = [{"cfg": {f"k{i}": (0.5 if i % 2 else "s")}} for i in range(datamap.MAP_MIN_KEYS)]
    assert "cfg.*" not in datamap.sh_fields(mixed)[0]
