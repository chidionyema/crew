"""crew#508 CP8: the scheduled outward research intake, both ways.

Founder, 2026-08-27: "we cant afford to rest on laurels and fall behind on research". The
intake pulls the newest release of every watched STANDARDS.md tool; the first release seen
per repo is the baseline, later ones are candidates the estate must answer; the grade goes
RED when the pull is >2 days old or a candidate sits >7 days unanswered.
"""
import datetime as dt
import json
import pathlib
import sys

CREW = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CREW / "science"))
import research_grade as rg  # noqa: E402
import research_intake as ri  # noqa: E402

NOW = dt.datetime(2026, 8, 27, 15, 0, tzinfo=dt.UTC)
SRC = [{"row": "GitOps", "repo": "fluxcd/flux2"}, {"row": "Data", "repo": "duckdb/duckdb"}]


def fake_fetch(releases: dict):
    def fetch(endpoint: str):
        repo = endpoint.split("repos/")[1].split("/releases")[0].split("/tags")[0]
        if endpoint.endswith("releases/latest"):
            tag = releases.get(repo)
            return {"tag_name": tag, "published_at": "2026-08-01T00:00:00Z"} if tag else None
        return []
    return fetch


def test_first_pull_files_baselines_not_candidates():
    new, state = ri.pull(SRC, [], NOW, fake_fetch({"fluxcd/flux2": "v2.9.4", "duckdb/duckdb": "v1.5.5"}))
    assert [r["status"] for r in new] == ["baseline", "baseline"]
    assert state["new"] == 2 and state["unreachable"] == [] and state["last_pull"] == "2026-08-27T15:00:00+00:00"


def test_later_release_is_a_candidate_and_seen_release_is_not_refiled():
    rows, _ = ri.pull(SRC, [], NOW, fake_fetch({"fluxcd/flux2": "v2.9.4", "duckdb/duckdb": "v1.5.5"}))
    new, state = ri.pull(SRC, rows, NOW, fake_fetch({"fluxcd/flux2": "v2.10.0", "duckdb/duckdb": "v1.5.5"}))
    assert [(r["repo"], r["tag"], r["status"]) for r in new] == [("fluxcd/flux2", "v2.10.0", "candidate")]
    assert state["new"] == 1


def test_unreachable_repo_is_named_and_does_not_stop_the_pull():
    new, state = ri.pull(SRC, [], NOW, fake_fetch({"duckdb/duckdb": "v1.5.5"}))
    assert state["unreachable"] == ["fluxcd/flux2"] and [r["repo"] for r in new] == ["duckdb/duckdb"]


def test_grade_is_red_when_never_pulled_or_stale():
    assert ri.grade([], None, SRC, NOW)["fresh"] is False
    stale = {"last_pull": (NOW - dt.timedelta(days=3)).isoformat()}
    assert ri.grade([], stale, SRC, NOW)["fresh"] is False
    fresh = {"last_pull": (NOW - dt.timedelta(days=1)).isoformat()}
    assert ri.grade([], fresh, SRC, NOW)["fresh"] is True


def test_candidate_unanswered_past_seven_days_is_late_and_answered_one_is_not():
    old = (NOW - dt.timedelta(days=8)).isoformat()
    rows = [{"seen": old, "row": "GitOps", "repo": "fluxcd/flux2", "tag": "v2.10.0", "url": "u", "status": "candidate"},
            {"seen": old, "row": "Data", "repo": "duckdb/duckdb", "tag": "v1.6.0", "url": "u", "status": "adopted", "ticket": "crew#1"}]
    g = ri.grade(rows, {"last_pull": NOW.isoformat()}, SRC, NOW)
    assert [r["repo"] for r in g["late"]] == ["fluxcd/flux2"] and g["adopted"] == 1 and g["candidates"] == 1
    assert "RED 8d" in ri.render(g, rows)


def test_outward_grade_drops_to_gap_when_the_intake_is_stale_or_late():
    healthy = {"questions": 3, "stale": [], "sourceless": 0}
    inw = {"trained": True, "scored": 1, "evidence": "x"}
    assert rg.grades(healthy, inw, {"fresh": True, "late": []})[0] == "ELITE"
    assert rg.grades(healthy, inw, {"fresh": False, "late": []})[0] == "GAP"
    assert rg.grades(healthy, inw, {"fresh": True, "late": [{}]})[0] == "GAP"


def test_check_exits_one_on_a_stale_pull(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(ri, "SOURCES", tmp_path / "s.json")
    monkeypatch.setattr(ri, "INTAKE", tmp_path / "i.jsonl")
    monkeypatch.setattr(ri, "STATE", tmp_path / "st.json")
    (tmp_path / "s.json").write_text(json.dumps({"watch": SRC}))
    (tmp_path / "st.json").write_text(json.dumps({"last_pull": "2026-01-01T00:00:00+00:00"}))
    assert ri.main(["--check"]) == 1
    assert "RED: last pull" in capsys.readouterr().out
    (tmp_path / "st.json").write_text(json.dumps({"last_pull": dt.datetime.now(dt.UTC).isoformat()}))
    assert ri.main(["--check"]) == 0


def test_every_watched_row_names_a_standards_row():
    rows = {ln.split("|")[1].strip() for ln in (CREW / "docs" / "reference" / "STANDARDS.md").read_text().splitlines() if ln.startswith("| ")}
    missing = [w for w in ri.watched() if w["row"] not in rows]
    assert not missing, missing
