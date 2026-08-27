"""crew#433: tracked.py --sync commits live copies straight onto claude-guards main
(aae334c wiped LAW 50 and unwired every hook; 0d9da69 is a normal run). A job that
writes a default branch is a LAW 24 guard and the map must name it, with the
residual it cannot close: that push meets no required check. Rung 4, incident."""
import json
from pathlib import Path

MAP = Path(__file__).resolve().parents[1] / "science" / "enforcement-map.json"


def _row24():
    rows = [r for r in json.loads(MAP.read_text())["laws"] if r.get("was") == 24]
    assert len(rows) == 1, rows
    return rows[0]


def test_incident_crew433_tracked_py_is_named_as_a_law24_guard():
    assert "tracked.py" in _row24()["guards"]


def test_incident_crew433_the_row_states_the_residual_it_cannot_close():
    check = _row24()["check"]
    assert "residual" in check and "required check" in check
