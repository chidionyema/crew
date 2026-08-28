"""crew#554: the estate assumed GitHub runs its crons, and nothing measured it.

Over the 24h to 2026-08-28T12:00Z, GitHub delivered 31 of 1,457 due occurrences across the
account, and the 31 that arrived were a median of 10 minutes and a p90 of 675 minutes late.
Every `max_age_hours` bar in `drills/catalogue.yaml` was graded against a clock nobody had
checked. `scripts/cron-delivery` is the instrument; these are the rules it must keep.

  1. Lateness is not absence. A run that arrives 11 hours after its due minute has to be
     matched to that minute, not counted as a drop. This is the mistake the first crew#554
     comment made -- a 15-minute matching window turned deferral into "GitHub is not creating
     these runs" -- and it was retracted in comment 5452180718. The search window for due
     minutes therefore reaches back further than the reporting window.
  2. A push is not the clock. `by_the_clock` is one predicate: a `schedule` event, or a
     `workflow_dispatch` by a `[bot]` actor. It must agree with the drill dispatcher and with
     `bin/idp-drills-row`, which idp#579 aligned; a fourth opinion is how they drift.
  3. A refused API call is reported and changes the exit status. "We did not look" must never
     render as "the estate is healthy" -- that is the silence this file exists to end. But a
     404 on a DYNAMIC workflow's file (dependabot's, the default security scan) is an answer,
     not a refusal: the first live run listed 67 of them and would have exited 2 on a sound
     measurement. Crying wolf and staying silent are the same failure from either side.
  4. No account, owner or repository is a literal (LAW 46). The owner comes from the
     authenticated login and the repositories are discovered.
  5. Cron expansion covers the forms the estate actually writes: `*`, `a`, `a-b`, `*/n`,
     `a-b/n` and comma lists, on all five fields.
  6. Nothing leaves the measurement in silence (review finding, session 78caaa17 on crew#571).
     The headline is a SHARE, so a workflow dropped from the denominator RAISES the delivered
     percentage. Three paths used to drop one without a word: a cron with the wrong field
     count, a cron field that does not parse, and a `schedule:` block whose entries the line
     reader cannot see. Each is now named under the table, with the direction stated, and the
     one omission that bends the other way -- a run list that came back short of what GitHub
     matched, which removes DELIVERIES and so invents misses -- is exit 2 beside a refusal,
     because a false alarm is the one thing this instrument may not raise. The `gh run list
     -L 400` cap that used to cause that is gone: the window is now a `created=>=` filter the
     server applies, so old runs never crowd the window's own deliveries off the list.
  7. Deliveries join to workflows by FILE PATH, never by name (review finding, session 78caaa17
     on crew#574). A run object's `name` is the name of the run, which `run-name:` can set to
     anything; the workflows API answers with the name of the workflow. Key on those and one
     `run-name:` line silently zeroes a workflow's deliveries and turns every occurrence it
     promised into a miss -- a false alarm, which rule 6 forbids. `.path` is the same string on
     both sides and is present on every run.
  8. The frequency bands cover every count with no gap and no overlap, and a band nobody is in
     is omitted rather than printed as 0%. The bands are the CP1 finding -- share falls from
     92% to 1% as a cron asks more often, while delivered-per-workflow stays inside 0.7-2.1 --
     so a workflow that falls between two of them is a row quietly missing from the answer.
"""
import datetime as dt
import importlib.machinery
import importlib.util
import os
import pathlib
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "cron-delivery"
UTC = dt.UTC


def _mod():
    """Load the extensionless script as a module."""
    loader = importlib.machinery.SourceFileLoader("cron_delivery", str(TOOL))
    spec = importlib.util.spec_from_loader("cron_delivery", loader)
    assert spec is not None, f"could not build a module spec for {TOOL}"
    m = importlib.util.module_from_spec(spec)
    loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def cd():
    return _mod()


def test_a_run_hours_late_is_matched_to_its_due_minute_not_called_a_drop(cd):
    """Rule 1. The 02:00 daily cron that GitHub delivered at 12:15 is 615 minutes late,
    and it is a delivery. Nothing in the instrument may round that into an absence."""
    now = dt.datetime(2026, 8, 27, 18, 0, tzinfo=UTC)
    start = now - dt.timedelta(hours=24)
    due = cd.occurrences(["0 2 * * *"], start - dt.timedelta(hours=24), now)
    arrived = dt.datetime(2026, 8, 27, 12, 15, tzinfo=UTC)
    prior = [t for t in due if t <= arrived]
    assert prior, "a run at 12:15 found no due minute at or before it"
    gap = (arrived - max(prior)).total_seconds() / 60
    assert gap == 615, gap
    # and the search reaches back beyond the reporting window, or the match is unreachable
    assert min(due) < start


def test_the_due_search_reaches_back_further_than_the_report_window(cd):
    """Rule 1, in the source: a same-width search cannot match a run deferred past midnight."""
    src = TOOL.read_text()
    assert "start - dt.timedelta(hours=24)" in src, \
        "the due-minute search no longer widens; lateness will read as absence again"


@pytest.mark.parametrize("event,actor,expected", [
    ("schedule", None, True),
    ("schedule", "somebody", True),
    ("workflow_dispatch", "estate-agents[bot]", True),
    ("workflow_dispatch", "chidionyema", False),
    ("push", "estate-agents[bot]", False),
    ("pull_request", "estate-agents[bot]", False),
])
def test_a_push_is_not_the_clock(cd, event, actor, expected):
    """Rule 2."""
    assert cd.by_the_clock(event, actor) is expected


def test_the_clock_predicate_matches_the_one_idp_579_settled(cd):
    """Rule 2. Three places implement this; they agree here or they drift in production."""
    src = TOOL.read_text()
    assert 'event == "schedule"' in src
    assert '"[bot]"' in src
    assert "pull_request" not in src.split("def by_the_clock")[1].split("def ")[0]
    assert '== "push"' not in src.split("def by_the_clock")[1].split("def ")[0]


def test_a_refused_call_is_named_and_changes_the_exit_status(tmp_path):
    """Rule 3. Silence is the failure mode, so this runs the real tool against a `gh` that
    refuses everything and asserts the OUTCOME, not the source. Grepping the file for
    `return 2` passes even when the caller has been rewired to return 0 -- a proxy, and
    proxies are how this estate has shipped four guards that graded nothing."""
    fake = tmp_path / "gh"
    fake.write_text("#!/bin/sh\necho 'refused: no token' >&2\nexit 1\n")
    fake.chmod(0o755)
    env = dict(os.environ, PATH=f'{tmp_path}:{os.environ["PATH"]}')
    p = subprocess.run(["python3", str(TOOL), "--owner", "nobody", "--repos", "a,b"],
                       capture_output=True, text=True, env=env, check=False)
    assert p.returncode == 2, f"a report built on refused calls exited {p.returncode}: {p.stdout}"
    assert "refused" in p.stdout, p.stdout
    assert "NOT RUN" in p.stdout, p.stdout


def test_a_missing_owner_is_not_an_empty_healthy_report(tmp_path):
    """Rule 3. With no --owner and a `gh` that cannot say who is logged in, the tool must
    say so and exit non-zero rather than print a clean header over nothing."""
    fake = tmp_path / "gh"
    fake.write_text("#!/bin/sh\nexit 1\n")
    fake.chmod(0o755)
    env = dict(os.environ, PATH=f'{tmp_path}:{os.environ["PATH"]}')
    p = subprocess.run(["python3", str(TOOL)], capture_output=True, text=True, env=env, check=False)
    assert p.returncode == 2, p.stdout
    assert "NOT RUN" in p.stdout, p.stdout


def test_no_owner_repo_or_account_is_a_literal(cd):
    """Rule 4, LAW 46."""
    src = TOOL.read_text()
    body = "\n".join(line for line in src.splitlines()
                     if not line.strip().startswith("#")
                     and "chidionyema" not in line.split("--")[0])
    for literal in ["haworks-platform", "prospector", "hermes-v2"]:
        assert literal not in body, f"{literal} is hardcoded; discover it instead"
    assert 'gh", "api", "user", "-q", ".login"' in src, "the owner is no longer discovered"
    assert '"gh", "repo", "list"' in src, "the repositories are no longer discovered"


@pytest.mark.parametrize("expr,lo,hi,expected", [
    ("*/5", 0, 59, set(range(0, 60, 5))),
    ("0", 0, 59, {0}),
    ("1-4", 0, 23, {1, 2, 3, 4}),
    ("1-9/3", 0, 23, {1, 4, 7}),
    ("0,30", 0, 59, {0, 30}),
    ("*", 0, 6, {0, 1, 2, 3, 4, 5, 6}),
])
def test_every_cron_form_the_estate_writes_expands(cd, expr, lo, hi, expected):
    """Rule 5."""
    assert cd.field(expr, lo, hi) == expected


def test_a_five_minute_cron_is_due_twelve_times_an_hour(cd):
    """Rule 5, end to end: the count that made idp/ping the worst row on the account."""
    now = dt.datetime(2026, 8, 28, 12, 0, tzinfo=UTC)
    due = cd.occurrences(["*/5 * * * *"], now - dt.timedelta(hours=24), now)
    assert len(due) == 24 * 12 + 1, len(due)


def test_a_malformed_cron_is_skipped_not_crashed_on(cd):
    """A four-field or non-numeric cron in some repo must not take the whole report down."""
    assert cd.parse(["bogus", "0 2 * *", "* * * * *", "a b c d e"]) == cd.parse(["* * * * *"])


def test_the_tool_runs_and_explains_itself(cd):
    """--help works without touching the network, so the instrument is discoverable."""
    p = subprocess.run(["python3", str(TOOL), "--help"],
                       capture_output=True, text=True, check=False)
    assert p.returncode == 0, p.stderr
    assert "--heartbeat" in p.stdout and "--owner" in p.stdout


def test_a_dynamic_workflow_with_no_file_is_absent_not_refused(cd, monkeypatch):
    """Rule 3, the other side. GitHub lists dependabot and the default security scan as
    workflows; reading their path 404s because no such file exists. That is an answer.
    The first live run counted 67 of them as refusals and exited 2 on a good measurement."""
    calls = []

    class Fake:
        def __init__(self, code, err):
            self.returncode, self.stderr, self.stdout = code, err, ""

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return Fake(1, "gh: Not Found (HTTP 404)\n")

    monkeypatch.setattr(cd.subprocess, "run", fake_run)
    cd.REFUSED.clear()
    assert cd.crons_of("owner/repo", "dynamic/dependabot/dependabot-updates") == []
    assert cd.REFUSED == [], "a 404 on an absent workflow file was recorded as a refusal"


def test_a_real_refusal_is_still_recorded(cd, monkeypatch):
    """Rule 3. Absent-ok must not swallow a 401, a 403 or a rate limit."""
    class Fake:
        def __init__(self, code, err):
            self.returncode, self.stderr, self.stdout = code, err, ""

    monkeypatch.setattr(cd.subprocess, "run",
                        lambda cmd, **kw: Fake(1, "gh: API rate limit exceeded (HTTP 403)\n"))
    cd.REFUSED.clear()
    assert cd.crons_of("owner/repo", ".github/workflows/real.yml") == []
    assert len(cd.REFUSED) == 1, "a 403 was swallowed by the 404 exemption"
    cd.REFUSED.clear()


@pytest.mark.parametrize("values,q,expected", [
    ([6, 12], 0.9, 12),          # the live n=2 run that printed a p90 BELOW the median
    ([1], 0.9, 1),
    ([1, 2], 0.5, 1),
    (list(range(1, 11)), 0.9, 9),
    (list(range(1, 101)), 0.9, 90),
])
def test_the_percentile_is_nearest_rank_not_a_floored_index(cd, values, q, expected):
    """`int(q * (n - 1))` floors to the FIRST element on a small sample. A live run with
    two data points printed `median 9m  p90 6m` -- a p90 under the median. It agrees with
    nearest-rank at n=61, so the 670m published on crew#554 stands, but it is wrong on
    exactly the thin sample a first look at a new repository produces."""
    assert cd.percentile(sorted(values), q) == expected


def test_the_p90_is_never_below_the_median(cd):
    """The property the floored index broke, over every sample size the tool can meet."""
    import statistics
    for n in range(1, 40):
        vals = sorted(x * 7 % 23 for x in range(n))
        assert cd.percentile(vals, 0.9) >= statistics.median(vals), n


# --- rule 6: no silent shrink of the denominator (review 78caaa17 on crew#571) --------------


def test_a_cron_with_the_wrong_field_count_is_named_not_dropped(cd):
    cd.DROPPED.clear()
    assert cd.parse(["0 3 * *"], where="acme/repo nightly") == []
    assert len(cd.DROPPED) == 1
    line = cd.DROPPED[0]
    assert "acme/repo nightly" in line and "0 3 * *" in line and "not 5" in line


def test_a_cron_field_that_does_not_parse_is_named_not_dropped(cd):
    cd.DROPPED.clear()
    assert cd.parse(["0 3 * * mon"], where="acme/repo weekly") == []
    assert len(cd.DROPPED) == 1
    assert "acme/repo weekly" in cd.DROPPED[0] and "does not parse" in cd.DROPPED[0]


def test_a_good_cron_beside_a_bad_one_is_still_counted(cd):
    """The drop is per-cron. One unreadable expression must not take the workflow with it."""
    cd.DROPPED.clear()
    assert len(cd.parse(["0 3 * * *", "nonsense"], where="acme/repo mixed")) == 1
    assert len(cd.DROPPED) == 1


def test_a_readable_cron_records_nothing(cd):
    """Rule 3's other half: an instrument that cries wolf is one nobody reads."""
    cd.DROPPED.clear()
    assert len(cd.parse(["*/15 * * * *"], where="acme/repo quarter")) == 1
    assert cd.DROPPED == []


def test_a_schedule_block_the_reader_cannot_see_is_named_not_silently_empty(cd, monkeypatch):
    """Flow style is valid YAML the line reader does not handle. It must not vanish."""
    cd.DROPPED.clear()
    monkeypatch.setattr(cd, "gh", lambda *a, **k: "on:\n  schedule: [{cron: '0 3 * * *'}]\n")
    assert cd.crons_of("acme/repo", ".github/workflows/nightly.yml") == []
    assert len(cd.DROPPED) == 1
    assert ".github/workflows/nightly.yml" in cd.DROPPED[0]
    assert "not counted as promising anything" in cd.DROPPED[0]


def test_a_workflow_with_no_schedule_at_all_is_not_reported_as_a_drop(cd, monkeypatch):
    """`schedule:` absent is an ANSWER. Only a declared-but-unreadable block is a drop."""
    cd.DROPPED.clear()
    monkeypatch.setattr(cd, "gh", lambda *a, **k: "on:\n  push:\n    branches: [main]\n")
    assert cd.crons_of("acme/repo", ".github/workflows/ci.yml") == []
    assert cd.DROPPED == []


def test_a_run_list_cut_short_is_reported_and_is_not_a_conservative_drop(cd, monkeypatch):
    """Fewer rows than GitHub matched removes DELIVERIES, so it invents misses: exit-2 territory."""
    cd.TRUNCATED.clear()
    page = {"total_count": 900,
            "workflow_runs": [{"created_at": "2026-08-28T00:00:00Z",
                               "path": ".github/workflows/nightly.yml"}] * 100}
    monkeypatch.setattr(cd, "gh_pages", lambda *a, **k: [page])
    cd.scheduled_runs("acme/repo", "2026-08-27T00:00:00Z")
    assert len(cd.TRUNCATED) == 1
    assert all(x in cd.TRUNCATED[0] for x in ("acme/repo", "900", "100"))


def test_a_complete_run_list_reports_nothing_and_still_bounds_the_window(cd, monkeypatch):
    """The server filters by day; the run from the day before the window is still not a delivery."""
    cd.TRUNCATED.clear()
    page = {"total_count": 2, "workflow_runs": [
        {"created_at": "2026-08-28T00:00:00Z", "path": ".github/workflows/nightly.yml"},
        {"created_at": "2026-08-27T00:00:00Z", "path": ".github/workflows/older.yml"}]}
    monkeypatch.setattr(cd, "gh_pages", lambda *a, **k: [page])
    out = cd.scheduled_runs("acme/repo", "2026-08-27T13:00:00Z")
    assert cd.TRUNCATED == []
    assert [n for n, _ in out] == [".github/workflows/nightly.yml"]


def test_the_window_is_asked_of_the_server_not_carved_out_of_a_row_cap(cd, monkeypatch):
    """The cap that invented misses is gone: the event and the day are in the query GitHub answers."""
    seen = []
    monkeypatch.setattr(cd, "gh_pages",
                        lambda path, **k: (seen.append(path), [{"total_count": 0,
                                                                "workflow_runs": []}])[1])
    cd.scheduled_runs("acme/repo", "2026-08-27T13:00:00Z")
    assert "event=schedule" in seen[0]
    assert "created=%3E%3D2026-08-27" in seen[0]
    assert not hasattr(cd, "RUN_CAP"), "a newest-N row cap is back; the window must stay server-side"


def test_a_paginated_path_that_already_carries_a_query_keeps_it(cd, monkeypatch):
    """`?per_page=` onto a path that already has `?` drops the filter, and the window with it."""
    seen = []
    monkeypatch.setattr(cd, "gh", lambda args, **k: (seen.append(list(args)), "{}")[1])
    cd.gh_pages("repos/acme/repo/actions/runs?event=schedule")
    assert seen[0][2] == "repos/acme/repo/actions/runs?event=schedule&per_page=100"


def test_a_paginated_path_with_no_query_still_opens_one(cd, monkeypatch):
    seen = []
    monkeypatch.setattr(cd, "gh", lambda args, **k: (seen.append(list(args)), "{}")[1])
    cd.gh_pages("repos/acme/repo/actions/workflows")
    assert seen[0][2] == "repos/acme/repo/actions/workflows?per_page=100"


def _sound(cd, dropped=(), refused=(), truncated=()):
    cd.DROPPED[:], cd.REFUSED[:], cd.TRUNCATED[:] = list(dropped), list(refused), list(truncated)
    said = []
    rc = cd.soundness(said.append)
    return rc, "\n".join(said)


def test_a_conservative_drop_is_loud_but_does_not_fail_the_run(cd):
    rc, out = _sound(cd, dropped=["acme/repo nightly: cron '0 3 * *' has 4 fields, not 5"])
    assert rc == 0
    assert "acme/repo nightly" in out
    assert "RAISES the delivered share" in out


def test_a_refusal_still_fails_the_run(cd):
    rc, out = _sound(cd, refused=["gh api repos/acme/repo -> exit 1"])
    assert rc == 2
    assert "cannot be trusted" in out


def test_a_truncated_run_list_fails_the_run_the_same_way_a_refusal_does(cd):
    """It removes deliveries, so it invents misses. Direction is the whole reason for exit 2."""
    rc, out = _sound(cd, truncated=["acme/repo: the runs API matched 900 but 100 arrived."])
    assert rc == 2
    assert "acme/repo" in out


def test_a_clean_measurement_says_nothing_and_exits_zero(cd):
    assert _sound(cd) == (0, "")


def test_a_drop_beside_a_refusal_reports_both_and_still_exits_two(cd):
    rc, out = _sound(cd, dropped=["d1"], refused=["r1"])
    assert rc == 2
    assert "d1" in out and "r1" in out


def test_a_long_drop_list_is_capped_and_says_how_many_it_did_not_print(cd):
    rc, out = _sound(cd, dropped=[f"drop {i}" for i in range(25)])
    assert rc == 0
    assert "... and 15 more" in out
    assert out.count("#   drop ") == 10


def test_a_run_renamed_by_run_name_is_still_counted_as_delivered(cd, monkeypatch):
    """Rule 7. The join key is the workflow FILE, because a run's name is not the workflow's.

    `run-name:` lets a run call itself anything. Keyed on name, such a run does not join to the
    workflow that promised it: its deliveries vanish, every occurrence becomes a miss, and the
    census raises a false alarm -- the one direction this instrument may not fail in (rule 6).
    Here the workflow is `nightly` and its run calls itself "nightly for main @ abc123"; the
    delivery must still land.
    """
    now = dt.datetime(2026, 8, 28, 12, 0, tzinfo=cd.UTC)
    monkeypatch.setattr(cd, "gh_pages", lambda *a, **k: [{"workflows": [
        {"state": "active", "name": "nightly", "path": ".github/workflows/nightly.yml"}]}])
    monkeypatch.setattr(cd, "crons_of", lambda *a, **k: ["0 * * * *"])
    monkeypatch.setattr(cd, "scheduled_runs", lambda *a, **k: [
        (".github/workflows/nightly.yml", now - dt.timedelta(minutes=60))])
    out = cd.measure_repo("acme/repo", now, 2)
    assert out["promised"] >= 1
    assert out["delivered"] == 1, "a renamed run stopped joining: the census now invents misses"


def test_the_join_key_is_the_workflow_file_on_both_sides(cd, monkeypatch):
    """Rule 7, stated against the code rather than one scenario, so a revert cannot be silent.

    Both halves of the join must read `path`: the run list that builds `fired`, and the workflow
    row that looks into it. A run object whose `path` is absent joins to nothing -- which is why
    the live check that every run carries one is recorded in `scheduled_runs`' docstring.
    """
    src = (ROOT / "scripts/cron-delivery").read_text()
    assert 'out.append((r.get("path")' in src, "the run half of the join left `path`"
    assert 'fired.get(w["path"]' in src, "the workflow half of the join left `path`"
    assert 'fired.get(w["name"]' not in src, "keyed on run name again; `run-name:` breaks it"


# --- crew#554 CP1: the bands, and the gap they must not have -------------------------------


def test_every_row_lands_in_exactly_one_band(cd):
    """Rule 8. The first draft read (12, 48) and (2, 11) and dropped every workflow due exactly
    12 times a day: no error, no row, a smaller `due` total than the estate really asked for.
    An allow-list with a silent miss case is this estate's own listed failure, so the bounds are
    checked across the whole range rather than at the four values someone thought of.
    """
    for due in range(0, 400):
        hit = cd.bands([{"due": due, "got": 0}])
        assert len(hit) == 1, f"due={due} landed in {len(hit)} bands"


def test_a_band_nobody_is_in_is_omitted_rather_than_printed_as_zero(cd):
    """"No workflow asks that often" and "every workflow that asks that often was dropped" are
    opposite findings, and a 0% row cannot be read as either. The band is left out."""
    assert [b["band"] for b in cd.bands([{"due": 1, "got": 1}])] == ["asks <=1/day"]
    assert all(b["wfs"] for b in cd.bands([{"due": d, "got": 0} for d in (1, 5, 24, 288)]))


def test_the_bands_separate_a_ration_per_workflow_from_a_share_of_what_was_asked(cd):
    """The CP1 finding itself. Two workflows handed the SAME number of runs, one asking 288 times
    a day and one asking once: report only a share and they read as a catastrophe and a success,
    when what happened is one ration handed out twice.
    """
    out = {b["band"]: b for b in cd.bands([{"due": 288, "got": 1}, {"due": 1, "got": 1}])}
    assert out["asks >48/day (<=30m apart)"]["per_wf"] == 1.0
    assert out["asks <=1/day"]["per_wf"] == 1.0
    assert out["asks >48/day (<=30m apart)"]["share"] < 1
    assert out["asks <=1/day"]["share"] == 100


def test_measure_repo_hands_back_the_per_workflow_rows_it_already_built(cd, monkeypatch):
    """--per-workflow costs no extra API call: measure_repo already expands the crons and joins
    the runs per workflow, then summed them away. Each row must carry its own workflow's due and
    got, or the bands are graded on an average of a */30 cron and a daily one -- the ecological
    inference the repo table could not escape, which is why this flag exists.
    """
    now = dt.datetime(2026, 8, 28, 12, 0, tzinfo=cd.UTC)
    monkeypatch.setattr(cd, "gh_pages", lambda *a, **k: [{"workflows": [
        {"state": "active", "name": "fast", "path": ".github/workflows/fast.yml"},
        {"state": "active", "name": "slow", "path": ".github/workflows/slow.yml"}]}])
    monkeypatch.setattr(cd, "crons_of",
                        lambda repo, path: ["*/30 * * * *"] if "fast" in path else ["0 6 * * *"])
    monkeypatch.setattr(cd, "scheduled_runs", lambda *a, **k: [
        (".github/workflows/fast.yml", now - dt.timedelta(minutes=10))])
    out = cd.measure_repo("acme/repo", now, 24)
    rows = {r["path"].split("/")[-1]: r for r in out["rows"]}
    # 49, not 48: a 24h window that includes both endpoints holds 49 half-hour marks.
    assert rows["fast.yml"]["due"] == 49 and rows["fast.yml"]["got"] == 1
    assert rows["slow.yml"]["due"] == 1 and rows["slow.yml"]["got"] == 0
    assert sum(r["due"] for r in out["rows"]) == out["promised"], "rows must sum to the total"
    assert sum(r["got"] for r in out["rows"]) == out["delivered"]


def test_the_per_workflow_flag_exists_and_is_off_by_default(cd):
    """The census's default answer is the repo table; --per-workflow is the CP1 detail behind it.
    A flag that turned itself on would put 42 rows in front of every reader of the summary."""
    src = (ROOT / "scripts/cron-delivery").read_text()
    assert '"--per-workflow", action="store_true"' in src
    assert "if a.per_workflow and rows:" in src
