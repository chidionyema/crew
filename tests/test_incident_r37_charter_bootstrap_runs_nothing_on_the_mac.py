"""Incident test (rung 4), named for R37, 2026-08-25.

The research charter's bootstrap told step 1 to run MLflow against a local SQLite file under
launchd. Founder: a local SQLite "tapeworm" on the Mac is incompatible with the cloud-agnostic
standard (R36, R37). Rule: no bootstrap step in the charter installs a platform store on the
laptop. Proved both ways: the old step text must fail, the live file must pass.
"""

from __future__ import annotations

import re
from pathlib import Path

CHARTER = Path(__file__).resolve().parents[1] / "docs" / "research-engine" / "CHARTER.md"
MAC_BOUND = re.compile(r"sqlite:///|--backend-store-uri|under launchd")


def bootstrap_steps(text: str) -> list[str]:
    section = text.split("## Bootstrap, in commands, in order", 1)[1]
    section = section.split("\nEach step is a crew issue", 1)[0]
    return re.findall(r"^\d+\..*?(?=^\d+\.|\Z)", section, flags=re.M | re.S)


def test_incident_r37_live_charter_bootstrap_names_no_mac_store() -> None:
    steps = bootstrap_steps(CHARTER.read_text())
    assert len(steps) == 6
    offenders = [s.splitlines()[0] for s in steps if MAC_BOUND.search(s)]
    assert offenders == []


def test_incident_r37_the_old_step_1_is_refused() -> None:
    old = (
        "## Bootstrap, in commands, in order\n\n"
        "1. `mlflow server --backend-store-uri sqlite:///science/mlflow.db` under launchd;\n"
        "   snapshot row goes ABSENT → GREEN.\n\nEach step is a crew issue"
    )
    steps = bootstrap_steps(old)
    assert [bool(MAC_BOUND.search(s)) for s in steps] == [True]
