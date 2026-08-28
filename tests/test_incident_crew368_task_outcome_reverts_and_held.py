"""crew#368, 2026-08-28: act/task_outcome was NEVER_EMITTED — commits and PRs were counted,
never whether a change held. dora.py now reads reverts and held_7d from the same PR listing
and writes the row as the `dora` source.

Both ways: a merged PR titled `Revert "<t>"` counts one revert and the PR it names is not
held; a merged PR 7+ days old that nothing reverted is held; a merged PR younger than 7 days
is not held yet; a window shorter than 8 days holds nothing; the row lands in the source.
"""
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "science"))
import dora

NOW = datetime(2026, 8, 28, 0, 0, tzinfo=UTC)
SINCE = NOW - timedelta(days=14)


def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _pr(days_ago, title):
    return {"createdAt": _iso(NOW - timedelta(days=days_ago, hours=1)),
            "mergedAt": _iso(NOW - timedelta(days=days_ago)), "baseRefName": "main", "title": title}


def test_revert_counts_and_unreverts_the_change_it_names():
    prs = [_pr(10, "feat: gateway refusal rule"), _pr(9, 'Revert "feat: gateway refusal rule"'),
           _pr(8, "fix: collect exits 0"), _pr(2, "fix: young change")]
    k = dora.four_keys(prs, [], SINCE, 14, NOW)
    assert k["deploys"] == 4 and k["reverts"] == 1
    assert k["held_7d"] == 1  # only "fix: collect exits 0": reverted one out, revert itself out, young one out


def test_revert_by_number_unholds_the_pr_it_names():
    # d5ae1960 on crew#547: idp#514 is titled `revert: Cilium chained ... (idp#505)`; the title it
    # undoes is not quoted, the number is. Without the number rule idp#505 reads as held in a week.
    prs = [dict(_pr(10, "crew#539 CP12: Cilium chained after OKE's flannel"), number=505),
           dict(_pr(9, "revert: Cilium chained over flannel took the pod network down (idp#505)"), number=514),
           dict(_pr(8, "fix: unrelated, still held"), number=506)]
    k = dora.four_keys(prs, [], SINCE, 14, NOW)
    assert k["reverts"] == 1 and k["held_7d"] == 1


def test_short_window_holds_nothing():
    prs = [_pr(3, "fix: a"), _pr(1, "fix: b")]
    k = dora.four_keys(prs, [], NOW - timedelta(days=7), 7, NOW)
    assert k["deploys"] == 2 and k["reverts"] == 0 and k["held_7d"] == 0


def test_reverted_title_shapes():
    assert dora.reverted_title('Revert "fix: x"') == "fix: x"
    assert dora.reverted_title("revert: fix: x") == "fix: x"
    assert dora.reverted_title("fix: revert the revert guard") is None
    assert dora.reverted_title("") is None


def test_jsonl_row_lands_in_the_source(tmp_path, monkeypatch):
    out = tmp_path / "dora.jsonl"
    monkeypatch.setattr(dora, "fetch", lambda repo, since: ([_pr(10, "fix: held"), _pr(9, 'Revert "fix: gone"'), _pr(9, "fix: gone")], []))
    assert dora.main(["--repo", "x/y", "--days", "14", "--jsonl", str(out), "--json"]) == 0
    row = json.loads(out.read_text().splitlines()[-1])
    assert row["repo"] == "x/y" and row["deploys"] == 3 and row["reverts"] == 1 and row["held_7d"] == 1
    assert row["at"][:4] == row["day"][:4] and "T" in row["at"]


def test_dora_is_a_declared_source():
    srcs = json.loads((Path(__file__).resolve().parents[1] / "science" / "sources.json").read_text())
    srcs = srcs if isinstance(srcs, list) else srcs["sources"]
    d = next(s for s in srcs if s["name"] == "dora")
    assert d["path"] == "dora.jsonl" and d["time_field"] == "at"
