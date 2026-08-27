"""crew#404: the rebase of the showcase branch kept two prediction rows with id 2 that were two
different predictions, one from foresight (crew#141) and one made by hand (crew#227). Both writers
allocate max(id)+1 and git merges the file without knowing that, so `latest[r["id"]]` let the later
row hide the earlier one. A repeated id is legitimate only when it is the same prediction again
(outcomes.py appends the scored copy under the same id). Rung 4: one id names one prediction."""
import json
import pathlib

LEDGER = pathlib.Path(__file__).resolve().parents[1] / "science" / "predictions.jsonl"


def _rows() -> list[dict]:
    return [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]


def _identity(r: dict) -> tuple:
    # the prediction, not its scoring: when it was made and what it was about
    return (r.get("at"), r.get("issue"), r.get("repo"), r.get("pr"), r.get("step"))


def test_incident_crew404_one_id_names_one_prediction() -> None:
    by_id: dict[int, set[tuple]] = {}
    for r in _rows():
        by_id.setdefault(r["id"], set()).add(_identity(r))
    clashes = {i: sorted(map(str, v)) for i, v in by_id.items() if len(v) > 1}
    assert not clashes, f"an id was allocated to two different predictions (two max+1 writers merged): {clashes}"
