"""crew#558, 2026-08-28. The LAW 50 bootstrap had no meter and no ceiling.

LAW 50 makes `science/datamap.py --check` the temporary bootstrap: "what exists and what does not
emit yet, every gap a ticket. It retires surface by surface as the query takes over." The founder
refused crew#394 as the law on 2026-08-27 -- "No more custom code for discovery. The platform
discovers itself ... coverage is verified by querying the backend, not by scanning files."

Nothing measured whether a surface ever retired, so none did. Measured 2026-08-28: 8180 of 8289
producers (98.7%) came from walking one laptop's disk, and seven of the ten domains were still
doing it. The cost was already paid in crew#556 -- because the register walks a filesystem it saw
git worktree copies, `science/ships.jsonl` read 57 rows in a copy against 150 in the real file, and
every ships-based number the founder was given came off the copy. The fix for THAT was 163 more
lines teaching the scanner about worktrees, which is the refused thing getting bigger. This is the
guard that would have refused it.

The unit is domains, not rows, and the test pins that too: a row count moves on its own every hour
(a new session writes transcripts), so a ceiling counted in rows would go red for correct work,
which is an outage (LAW 38).
"""
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "science"))

import datamap  # noqa: E402
import producers  # noqa: E402


def test_every_domain_declares_whether_it_scans_or_queries():
    """The register is closed-world; so is its provenance. A domain added without a provenance
    is a surface nobody decided about, which is how the bootstrap grew unnoticed."""
    assert producers.untagged_domains() == [], (
        "these domains declare no provenance in producers.PROVENANCE: "
        f"{producers.untagged_domains()}"
    )
    assert set(producers.PROVENANCE.values()) <= {"scan", "query"}


def test_the_ceiling_file_exists_and_matches_what_the_code_actually_does():
    """A ceiling nobody keeps current is a wish (LAW 44)."""
    ceiling = json.loads(datamap.CEILING.read_text())
    assert ceiling["scan_domains"] == len(producers.scan_domains()), (
        f"{datamap.CEILING.name} says {ceiling['scan_domains']} scan domain(s) but the code has "
        f"{len(producers.scan_domains())}: {producers.scan_domains()}. Lower it in the pull request "
        "that retires a surface; never raise it."
    )


def _b(scan, ceiling, untagged=()):
    return {"scan_domains": list(scan), "query_domains": [], "untagged": list(untagged),
            "scan_producers": 0, "producers": 0, "share": 0.0, "ceiling": ceiling}


def test_a_new_scanning_domain_is_refused():
    """The half that matters: adding an eighth file-scanning surface is red."""
    v = datamap.ceiling_violations(_b(["a", "b", "c", "d", "e", "f", "g", "h"], 7))
    assert v, "eight scan domains against a ceiling of seven must be a violation"
    assert "up from the ceiling of 7" in v[0]


def test_retiring_a_surface_is_permitted():
    """The other half. A guard that refuses correct work is an outage (LAW 38): moving a domain
    from scan to query is exactly the work LAW 50 asks for and must never be refused."""
    assert datamap.ceiling_violations(_b(["a", "b", "c", "d", "e", "f"], 7)) == []
    assert datamap.ceiling_violations(_b(["a", "b", "c", "d", "e", "f", "g"], 7)) == []


def test_an_untagged_domain_is_refused():
    v = datamap.ceiling_violations(_b(["a"], 7, untagged=["newthing"]))
    assert any("newthing" in x for x in v)


def test_a_missing_ceiling_file_is_itself_the_violation():
    """No ceiling means nothing stops the bootstrap growing, which is the state this ticket found."""
    v = datamap.ceiling_violations(_b(["a"], None))
    assert v and "no ceiling" in v[0]


def test_the_ceiling_counts_domains_not_rows():
    """Pinned deliberately. Producers churn hourly; domains move only when someone retires one."""
    src = (ROOT / "science" / "bootstrap-ceiling.json").read_text()
    doc = json.loads(src)
    assert "scan_domains" in doc
    assert doc["scan_domains"] < 100, "a ceiling in the thousands is a row count, not a domain count"
