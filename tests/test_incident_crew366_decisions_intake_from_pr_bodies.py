"""crew#366, 2026-08-28: act/agent_decisions was NEVER_EMITTED. decision-log.py's writer was
last called 2026-08-24 (13 hand-written rows); every merged PR since carried its decision in
`## Options considered` and nothing read it. decisions_intake.py pull files one decision row
per merged PR on the same log, in decision-log.py's row shape.

Both ways: a body with two rejected roads and a Chosen line becomes a row naming them and the
author session; a body with no block (or no Chosen line) files nothing; a second pull adds
nothing for a PR already on the log; the warehouse view counts per session."""
import json
import sqlite3
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "science"))
import collect  # noqa: E402
import decisions_intake as di  # noqa: E402

BODY = """No-Issue: tracked in chidionyema/crew#1
Author-session: 09cd04a6

## Options considered
- Branch protection: a GUI click per merge.
- Require the Reviewed-by line: the author writes it.
- **Chosen:** the reviewer's own comment naming the sha.

## Definition of done
1. x
"""
PR = {"number": 7, "title": "merge only on a KEEP naming head", "body": BODY, "html_url": "https://github.com/chidionyema/crew/pull/7",
      "merged_at": "2026-08-27T18:00:00Z", "merge_commit_sha": "abc1234"}
NOW = datetime(2026, 8, 28, 0, 0, tzinfo=UTC)


def test_options_block_becomes_a_decision_row_in_the_log_shape():
    row = di.row_for(PR, "chidionyema/crew")
    assert row["kind"] == "decision" and row["session"] == "09cd04a6"
    assert row["options"] == ["Branch protection: a GUI click per merge.", "Require the Reviewed-by line: the author writes it."]
    assert row["chosen"] == "the reviewer's own comment naming the sha."
    assert row["undo"] == "git revert abc1234" and row["reversible"] is True and row["status"] == "standing"
    assert set(row) >= {"id", "ts", "question", "why", "rests_on", "revisit_when", "superseded_by"}


def test_no_block_or_no_chosen_files_nothing():
    assert di.row_for({**PR, "body": "Author-session: x\n\nJust a fix."}, "r") is None
    assert di.row_for({**PR, "body": "## Options considered\n- a road\n- another road\n"}, "r") is None


def test_pull_dedups_by_pr_and_records_state(tmp_path):
    log, state = tmp_path / "DECISIONS.jsonl", tmp_path / "state.json"
    fetched = lambda repo, since: [PR] if repo.endswith("/crew") else []  # noqa: E731
    di.pull(log=log, fetcher=fetched, state=state, now=NOW)
    di.pull(log=log, fetcher=fetched, state=state, now=NOW)
    rows = [json.loads(l) for l in log.read_text().splitlines()]
    assert len(rows) == 1 and rows[0]["pr"] == PR["html_url"]
    assert json.loads(state.read_text())["since"] == "2026-08-27T00:00:00Z"


def test_warehouse_view_counts_decisions_per_session(tmp_path):
    con = sqlite3.connect(tmp_path / "w.db")
    con.executescript("CREATE TABLE facts(source TEXT, at TEXT, ingested_at TEXT, payload TEXT);")
    for r in (di.row_for(PR, "r"), {**di.row_for({**PR, "html_url": "u2"}, "r"), "status": "superseded"},
              {"kind": "research", "session": "09cd04a6", "ts": "2026-08-27T18:00:00Z"}):
        con.execute("INSERT INTO facts VALUES ('decisions', ?, ?, ?)", (r["ts"], r["ts"], json.dumps(r)))
    con.executescript(collect.SPEND_VIEW)
    got = con.execute("SELECT session, decisions, options_rejected, reversals FROM decisions_by_session").fetchall()
    assert got == [("09cd04a6", 2, 4, 1)], got


def test_decisions_source_is_declared_with_the_rows_time_field():
    srcs = json.loads((Path(__file__).resolve().parents[1] / "science/sources.json").read_text())["sources"]
    d = next(s for s in srcs if s["name"] == "decisions")
    assert d["time_field"] == "ts" and d["owner"] == "scripts/science-collect"
