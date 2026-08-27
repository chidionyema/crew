"""crew#140: the fact files are one code location on the one scheduler, not a second project.

Asserted against the real module, on whatever interpreter runs pytest (the idp venv in
production, Python 3.11 in crew CI): facts.py builds a Definitions that carries one asset
spec per source declared in science/sources.json and the 15-minute observation schedule,
and needs nothing beyond `dagster` to do so. A location that imports dagster-dbt would
fail this on the scheduler's interpreter, which is the trap definitions.py documents.
"""
import json
import sys
from pathlib import Path

SCIENCE = Path(__file__).resolve().parents[2]


def test_facts_location_declares_one_asset_per_declared_source():
    from estate_dagster.facts import SPECS, defs

    declared = json.loads((SCIENCE / "sources.json").read_text(encoding="utf-8"))["sources"]
    keys = {tuple(k.path) for k in defs.resolve_asset_graph().get_all_asset_keys()}
    assert len(SPECS) == len(declared)
    assert keys == {("estate", s["name"]) for s in declared}


def test_facts_location_observes_every_15_minutes_by_default():
    from estate_dagster.facts import defs

    sched = {s.name: s for s in defs.schedules}
    assert list(sched) == ["observe_estate_facts_every_15m"]
    assert sched["observe_estate_facts_every_15m"].cron_schedule == "*/15 * * * *"
    assert sched["observe_estate_facts_every_15m"].default_status.name == "RUNNING"


def test_facts_location_needs_no_dbt_integration():
    import estate_dagster.facts  # noqa: F401  (import side effects are the point)

    assert not any(m == "dagster_dbt" or m.startswith("dagster_dbt.") for m in sys.modules), (
        "facts.py pulled dagster_dbt in; the scheduler's interpreter cannot carry it"
    )
