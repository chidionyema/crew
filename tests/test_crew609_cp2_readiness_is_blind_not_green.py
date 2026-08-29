"""crew#609 CP2: a readiness row whose source is missing reads BLIND, never green; hermes first.

The defect this test prevents: a scorecard that prints prospector's pay path green from
memory of a proof file that is no longer there, or that buries the hermes rows under the
platform's.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "product"))

import readiness as rd

TODAY = dt.date(2026, 8, 28)
PROOF = "# Buy-button proof\n\n**Date:** 2026-06-20 20:45:47 BST\n**Verdict:** ✅ ALL 12 CHECKOUTS REAL\n"
CFG = "listing:\n  pricing:\n    # These numbers are a HYPOTHESIS, not a finding.\n    rungs: [1999, 2999, 4999, 7999, 9999]\n"


def estate(tmp_path: pathlib.Path, *, proof: bool = True) -> pathlib.Path:
    p = tmp_path / "prospector-main"
    (p / "store/launch").mkdir(parents=True)
    if proof:
        (p / "store/launch/checkout-proof.md").write_text(PROOF)
    (p / "config.yaml").write_text(CFG)
    h = tmp_path / "hermes-v2"
    h.mkdir()
    (h / "README.md").write_text("| WATCH | **$22.63/month** |\n")
    i = tmp_path / "idp"
    (i / "svc").mkdir(parents=True)
    (i / "svc/catalog-info.yaml").write_text("kind: Component\n")
    return tmp_path


def by(g, asset, step):
    return next(r for r in g["rows"] if r["asset"] == asset and r["step"] == step)


def test_prospector_proof_older_than_thirty_days_is_amber_and_hypothesis_rungs_are_amber(tmp_path):
    g = rd.grade(estate(tmp_path), TODAY)
    assert by(g, "prospector", "pay path")["status"] == "amber"
    assert "69 days" in by(g, "prospector", "pay path")["reason"]
    assert by(g, "prospector", "price")["status"] == "amber"
    assert "HYPOTHESIS" in by(g, "prospector", "price")["reason"]


def test_missing_checkout_proof_reads_blind_with_the_path_it_looked_for(tmp_path):
    g = rd.grade(estate(tmp_path, proof=False), TODAY)
    row = by(g, "prospector", "pay path")
    assert row["status"] == "BLIND"
    assert "checkout-proof.md" in row["reason"]


def test_hermes_rows_come_first_and_no_pay_path_is_red(tmp_path):
    g = rd.grade(estate(tmp_path), TODAY)
    assert g["rows"][0]["asset"] == "hermes"
    assert by(g, "hermes", "pay path")["status"] == "red"
    assert by(g, "hermes", "price vs run cost")["status"] == "amber"
    assert "22.63" in by(g, "hermes", "price vs run cost")["reason"]
    assert rd.check(g) == []


def test_missing_estate_is_blind_everywhere_and_check_refuses_fewer_than_three_assets(tmp_path):
    g = rd.grade(tmp_path / "nowhere", TODAY)
    assert {r["status"] for r in g["rows"]} == {"BLIND"}
    # crew#610 review: three BLIND rows are honest rows, but an estate the grader could not read
    # at all is a failed check, not a pass (it cleared >=3 assets and hermes-first with nothing read).
    assert any(e.startswith("every row is BLIND") for e in rd.check(g))


def test_horizons_have_one_experiment_each_and_unlinked_science_is_blind(tmp_path):
    g = rd.grade(estate(tmp_path), TODAY)
    assert len(g["horizons"]) == 4
    assert all(h["experiment"] for h in g["horizons"])
    assert any("glasses" in h["surface"] for h in g["horizons"])
    assert {h["research"] for h in g["horizons"]} <= {"linked", "BLIND"}
    page = rd.render(g)
    assert page.splitlines()[0].startswith("# Product readiness")
    assert "| hermes |" in page.splitlines()[7]


# crew#610 review (code-e9, comment 5459186713): two ways the grader read green off nothing.

def _gh(date_header):
    def run(*a, **k):
        class R:
            stdout = ("HTTP/2.0 200 OK\r\n" + (f"Date: {date_header}\r\n" if date_header else "") + "\r\n{}")
        return R()
    return run


def test_the_age_follows_githubs_clock_not_this_machines(tmp_path):
    # 69-day-old proof; the machine's clock is never consulted, so any local clock gives one verdict.
    today = rd.authority_clock(run=_gh("Fri, 29 Aug 2026 00:00:00 GMT"))
    assert today == dt.date(2026, 8, 29)
    g = rd.grade(estate(tmp_path), today)
    row = next(r for r in g["rows"] if r["asset"] == "prospector" and r["step"] == "pay path")
    assert row["status"] == "amber", row


def test_no_clock_is_blind_never_green(tmp_path):
    assert rd.authority_clock(run=_gh(None)) is None
    g = rd.grade(estate(tmp_path), None)
    row = next(r for r in g["rows"] if r["asset"] == "prospector" and r["step"] == "pay path")
    assert row["status"] == "BLIND", row
    assert any("no trusted clock" in e for e in rd.check(g))


def test_a_proof_stamped_in_the_future_is_blind_not_green(tmp_path):
    g = rd.grade(estate(tmp_path), dt.date(1970, 1, 1))
    row = next(r for r in g["rows"] if r["asset"] == "prospector" and r["step"] == "pay path")
    assert row["status"] == "BLIND", row


def test_check_refuses_an_estate_it_could_not_read(tmp_path):
    g = rd.grade(tmp_path / "nowhere", TODAY)
    assert all(r["status"] == "BLIND" for r in g["rows"])
    assert any(e.startswith("every row is BLIND") for e in rd.check(g))


def test_no_clock_leaves_the_pages_untouched(tmp_path, monkeypatch):
    monkeypatch.setattr(rd, "CREW", tmp_path)
    (tmp_path / "docs/product").mkdir(parents=True)
    page = tmp_path / "docs/product/READINESS.md"; page.write_text("yesterday, measured")
    monkeypatch.setattr(rd, "authority_clock", lambda: None)
    monkeypatch.setenv("ESTATE_ROOT", str(estate(tmp_path)))
    assert rd.main([]) == 1
    assert page.read_text() == "yesterday, measured"
