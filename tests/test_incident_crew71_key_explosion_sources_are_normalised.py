"""crew#71 DoD row 3: the three key-explosion sources are normalised so schema stops growing with data.

The writers live on the machine outside this repo; the declared contract is the schema file
under science/schemas/<name>.json, which collect.py --write-schemas regenerates from the rows
the writers emit. These tests assert the committed schema files declare the bounded
(normalised) shapes, so a writer that regresses to a data-keyed dict, or a schema that is
edited back to one, goes red here before the drift gate ever sees it.

The three smells this pins (measured 2026-08-24):
  1. agent_cert: 810 field paths for 12 rows -- requirement ids used as object keys
     (rows.REQ-001.state). Normalised: rows is an array of per-test records.
  2. spend: 42 fields, 38 partial -- project names used as keys (by_owner.<project>).
     Normalised: by_owner and reqs_by_owner are arrays of per-project records.
  3. stuck_detector: 11 fields, all partial -- two record shapes sharing one source name.
     Normalised: every row carries a kind discriminator ("observation" or "run_summary").
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
SCHEMAS = HERE / "science" / "schemas"


def _schema(name):
    return json.loads((SCHEMAS / f"{name}.json").read_text())


def test_agent_cert_rows_is_an_array_not_a_dict():
    """Smell 1: a dict keyed by test id made the schema grow with the requirements."""
    s = _schema("agent_cert")
    assert "rows" in s["fields"], "agent_cert schema must declare rows"
    assert "dict" not in s["fields"]["rows"], \
        "rows must not be a dict keyed by test id; the schema would grow with the data"
    assert "list" in s["fields"]["rows"], \
        "rows must be declared as an array of per-test records (crew#71)"


def test_spend_by_owner_and_reqs_by_owner_are_arrays_not_dicts():
    """Smell 2: dicts keyed by project made the money source's schema grow with the projects."""
    s = _schema("spend")
    for key in ("by_owner", "reqs_by_owner"):
        assert key in s["fields"], f"spend schema must declare {key}"
        assert "dict" not in s["fields"][key], \
            f"{key} must not be a dict keyed by project; the schema would grow with the data"
        assert "list" in s["fields"][key], \
            f"{key} must be declared as an array of per-project records (crew#71)"


def test_stuck_detector_declares_kind_discriminator():
    """Smell 3: two record shapes shared one source name with no discriminator."""
    s = _schema("stuck_detector")
    assert "kind" in s["fields"], "stuck_detector schema must declare the kind discriminator"
    docs = s.get("field_docs") or {}
    assert "kind" in docs, \
        "stuck_detector schema must document the kind discriminator and its two values"
    desc = docs["kind"].get("description", "")
    assert "observation" in desc and "run_summary" in desc, \
        "the kind field_doc must name both record shapes (observation, run_summary)"
