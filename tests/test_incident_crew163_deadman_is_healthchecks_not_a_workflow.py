"""crew#163: the dead-man for the Mac is the estate's Healthchecks on OKE, not a workflow.

The first cut of crew#163 added `.github/workflows/deadman.yml` and `scripts/deadman-check.sh`:
a second dead-man, on GitHub, reading STATE.md commit ages. The estate already runs one
(Healthchecks on OKE, `platform/healthchecks/healthchecks.yaml` in idp; every Mac job is
`hc-wrap.sh <slug> <cmd>` in `idp/scheduler/schedule.yml`), outside the Mac's failure domain.
Two dead-men with different thresholds is the stitching LAW 43 forbids.

This guard fails the moment anyone re-adds a hand-rolled dead-man to this repository.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_no_workflow_reinvents_the_dead_man() -> None:
    hits = []
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
        text = wf.read_text(encoding="utf-8", errors="replace")
        if re.search(r"dead-?man|heartbeat age", text, re.IGNORECASE):
            hits.append(wf.relative_to(ROOT).as_posix())
    assert not hits, f"dead-man reinvented in {hits}: the estate's is Healthchecks (docs/onboarding/monitoring.md)"


def test_no_script_reinvents_the_dead_man() -> None:
    hits = [p.relative_to(ROOT).as_posix() for p in (ROOT / "scripts").glob("*deadman*")]
    assert not hits, f"dead-man reinvented in {hits}: wrap the job with hc-wrap.sh instead"


def test_onboarding_names_the_one_receiver() -> None:
    doc = (ROOT / "docs" / "onboarding" / "monitoring.md").read_text(encoding="utf-8")
    for needle in ("idp-hc-enroll", "hc-wrap.sh", "estate-snapshot"):
        assert needle in doc, f"docs/onboarding/monitoring.md must name {needle}"
