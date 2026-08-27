"""crew#320 row 3: `datamap.py --file-tickets` existed and nobody ran it, so a new gap entry
sat silent for two days (crew#319). The filer must run on a schedule, off the laptop, with the
permissions filing and landing need. Rung 4 incident test, both ways.
"""
import pathlib
import re

WF = pathlib.Path(__file__).resolve().parents[1] / ".github" / "workflows" / "datamap-tickets.yml"


def _scheduled_filer(text: str) -> list[str]:
    bad = []
    if not re.search(r"^\s+- cron: \"", text, re.M):
        bad.append("no schedule")
    if "--file-tickets" not in text:
        bad.append("does not run --file-tickets")
    for perm in ("issues: write", "contents: write", "pull-requests: write"):
        if perm not in text:
            bad.append(f"missing permission {perm}")
    if "science/verdicts.json" not in text:
        bad.append("never lands the ticket numbers back in the register")
    return bad


def test_the_ticket_filer_is_scheduled_with_the_permissions_it_needs():
    assert _scheduled_filer(WF.read_text()) == []


def test_a_workflow_that_only_reports_would_be_refused():
    stripped = WF.read_text().replace("--file-tickets", "").replace("issues: write", "issues: read")
    assert set(_scheduled_filer(stripped)) == {"does not run --file-tickets", "missing permission issues: write"}
