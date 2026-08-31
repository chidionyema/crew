"""Founder ask, 2026-08-31: what science collects from the estate "must be transparent,
critical for auditing", plus "a living document detailing their assets and roadmap".

The showcase page answers both with two generated sections. This pins that they render
from the real register and plan, name every declared dataset with its full contract
(owner, method, sensitivity, retention), keep every declined store's reason, and go
BLIND with a path rather than vanishing when a source is missing (LAW 45).
"""

import datetime as dt
import json
import pathlib
import sys

SCIENCE = pathlib.Path(__file__).resolve().parents[1] / "science"
sys.path.insert(0, str(SCIENCE))
import showcase  # noqa: E402

NOW = dt.datetime(2026, 8, 31, 0, 0, tzinfo=dt.UTC).replace(tzinfo=None)


def test_every_declared_dataset_is_on_the_page_with_its_contract():
    reg = json.load(showcase.SOURCES.open())
    d = showcase.register(NOW)
    assert {r["name"] for r in d["rows"]} == {s["name"] for s in reg["sources"]}
    for r in d["rows"]:
        for key in ("owner", "method", "sensitivity", "retention_days"):
            assert r[key] != "MISSING", f"{r['name']} has no {key}; the register is the audit"
    assert {r["id"] for r in d["declined"]} == {
        e.get("id") or e.get("path", "?") for e in reg["declined"]
    }
    assert all(r["reason"] for r in d["declined"]), "a declined store with no reason is a gap"


def test_the_two_sections_render_with_their_rows():
    data = {
        showcase.REGISTER_TITLE: showcase.register(NOW),
        showcase.ROADMAP_TITLE: showcase.roadmap(NOW),
    }
    blind = {t: "not built in this test" for t, _, _ in showcase.SECTIONS if t not in data}
    page = showcase.render(NOW, data, blind, {})
    reg_section = page.split(f"## {showcase.REGISTER_TITLE}")[1].split("\n## ")[0]
    for r in data[showcase.REGISTER_TITLE]["rows"]:
        assert f"| {r['name']} |" in reg_section
    assert "Declined: found by the crawl" in reg_section
    road = page.split(f"## {showcase.ROADMAP_TITLE}")[1]
    assert data[showcase.ROADMAP_TITLE]["goals"], "the roadmap read no goal from PLAN.md"
    for g in data[showcase.ROADMAP_TITLE]["goals"]:
        assert g["title"] in road and "graded by:" in road


def test_a_missing_register_or_plan_is_blind_never_absent(monkeypatch, tmp_path):
    monkeypatch.setattr(showcase, "SOURCES", tmp_path / "sources.json")
    monkeypatch.setattr(showcase, "PLANFILE", tmp_path / "PLAN.md")
    data, blind = showcase.build(NOW)
    assert "sources.json absent" in blind[showcase.REGISTER_TITLE]
    assert "PLAN.md absent" in blind[showcase.ROADMAP_TITLE]
    page = showcase.render(NOW, data, blind, {})
    assert "BLIND:" in page.split(f"## {showcase.REGISTER_TITLE}")[1].split("\n## ")[0]
