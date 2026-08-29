"""crew#522 (2026-08-27): idp's operating-model gate refused idp#427 and crew#522 for the same
defect -- a `- LAW n <slug>:` line written as a sentence -- and `pr-evidence.py check` passed
both bodies because it never graded that section. The gate's regex now runs locally, so the
sentence is refused before the PR, the evidence commit and the review ask exist.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "pr_evidence", Path(__file__).resolve().parents[1] / "scripts" / "pr-evidence.py"
)
assert _spec and _spec.loader
pe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pe)

GOOD = """## Architecture laws
- LAW 1 zero-gravity: n/a: no new config
- LAW 2 fractal: python3 -m pytest -q tests/test_x.py
- LAW 3 nervous system: `bin/idp-science-facts` -> FAIL sources=0 on the first receipt
- LAW 4 calibration: docs/x.md
"""


def test_the_two_refused_lines_are_refused_here_too():
    # idp#427 at e9ddd10: LAW 4 as a sentence.
    body = GOOD.replace(
        "- LAW 4 calibration: docs/x.md",
        "- LAW 4 calibration: prediction: first receipt reads FAIL until slice 2 lands",
    )
    ok, why = pe.architecture_laws(body)
    assert not ok and "LAW 4 calibration" in why and "sentence" in why
    # crew#522 at c69d039: LAW 1 as a sentence.
    body = GOOD.replace(
        "- LAW 1 zero-gravity: n/a: no new config",
        "- LAW 1 zero-gravity: endpoint and headers come from the two OTel env vars",
    )
    ok, why = pe.architecture_laws(body)
    assert not ok and "LAW 1 zero-gravity" in why


def test_a_proof_shaped_line_passes_and_a_missing_line_does_not():
    assert pe.architecture_laws(GOOD) == (True, "four law lines carry a proof or an n/a reason")
    ok, why = pe.architecture_laws(
        GOOD.replace("- LAW 2 fractal: python3 -m pytest -q tests/test_x.py\n", "")
    )
    assert not ok and "LAW 2 fractal" in why
    # Same regex as the gate, so the same known hole: a bare `n/a` contains a `/` and passes
    # both. Pinned here so a tightening lands in policy/operating_model.rego and here together.
    assert pe.architecture_laws(GOOD.replace("n/a: no new config", "n/a"))[0] is True


def test_no_section_is_refused_not_ignored():
    ok, why = pe.architecture_laws("## Definition of done\n1. Tracked item: x\n")
    assert not ok and "Architecture laws" in why


def test_check_wires_the_verdict_in():
    src = (Path(__file__).resolve().parents[1] / "scripts" / "pr-evidence.py").read_text()
    assert "ok_laws, why_laws = architecture_laws(body)" in src
    assert "{why_dod}, {why_laws}, {why_acc};" in src
