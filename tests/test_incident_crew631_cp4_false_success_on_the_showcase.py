"""crew#631 CP4: the false-success rate is a number on the showcase, computed from the board's
claim/verdict pairs, with the query that made it; a pending claim is never folded into the rate."""

import datetime as dt
import pathlib
import sys

CREW = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CREW / "science"))
import false_success as fs  # noqa: E402
import showcase  # noqa: E402


def _issue(n, labels):
    return {"number": n, "title": f"t{n}", "labels": [{"name": label} for label in labels]}


def test_pairing_counts_rejected_over_decided_and_keeps_pending_out():
    issues = [
        _issue(1, ["VERIFIED"]),
        _issue(2, ["REJECTED"]),
        _issue(3, [fs.CLAIM]),
        _issue(4, []),
    ]
    mv = {
        1: [("t", fs.CLAIM, "VERIFIED", "PASS")],
        2: [("t", fs.CLAIM, "REJECTED", "FAIL")],
        3: [],
        4: [],
    }
    d = fs.pair(issues, lambda n: mv[n])
    assert (d["verified"], d["rejected"], d["pending"]) == (1, 1, 1)
    assert d["false_success_pct"] == 50 and len(d["claims"]) == 3
    assert fs.pair([_issue(5, [fs.CLAIM])], lambda n: [])["false_success_pct"] is None


def test_the_move_regex_reads_the_apps_comment():
    body = "ticket-verify: RESOLVED_PENDING_VERIFICATION -> REJECTED. FAIL run 1 on sha256:abc"
    assert fs.MOVE_RE.findall(body) == [(fs.CLAIM, "REJECTED", "FAIL run 1 on sha256:abc")]


def test_the_showcase_renders_the_number_with_its_query(monkeypatch):
    title = "False success: claims the prover rejected"
    assert any(t == title for t, _, _ in showcase.SECTIONS)
    data = {
        title: {
            "claims": [{"number": 2, "title": "x", "verdict": "REJECTED"}],
            "verified": 3,
            "rejected": 1,
            "pending": 2,
            "false_success_pct": 25,
            "window_days": 30,
            "query": "q",
        }
    }
    page = showcase.render(
        dt.datetime(2026, 8, 29, tzinfo=dt.UTC),
        data,
        {t: "not run" for t, _, _ in showcase.SECTIONS if t != title},
        {},
    )
    assert "false-success rate 25%: 1 rejected of 4 decided claims, 2 pending" in page
    assert "`python3 science/false_success.py --days 30`" in page
    assert showcase.numbers(data)["false-success %"] == 25
