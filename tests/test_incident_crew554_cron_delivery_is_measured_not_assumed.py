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
"""
import datetime as dt
import importlib.util
import os
import pathlib
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "scripts" / "cron-delivery"
UTC = dt.timezone.utc


def _mod():
    """Load the extensionless script as a module."""
    spec = importlib.util.spec_from_loader(
        "cron_delivery", importlib.machinery.SourceFileLoader("cron_delivery", str(TOOL)))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
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
    env = dict(os.environ, PATH="%s:%s" % (tmp_path, os.environ["PATH"]))
    p = subprocess.run(["python3", str(TOOL), "--owner", "nobody", "--repos", "a,b"],
                       capture_output=True, text=True, env=env)
    assert p.returncode == 2, "a report built on refused calls exited %d: %s" % (
        p.returncode, p.stdout)
    assert "refused" in p.stdout, p.stdout
    assert "NOT RUN" in p.stdout, p.stdout


def test_a_missing_owner_is_not_an_empty_healthy_report(tmp_path):
    """Rule 3. With no --owner and a `gh` that cannot say who is logged in, the tool must
    say so and exit non-zero rather than print a clean header over nothing."""
    fake = tmp_path / "gh"
    fake.write_text("#!/bin/sh\nexit 1\n")
    fake.chmod(0o755)
    env = dict(os.environ, PATH="%s:%s" % (tmp_path, os.environ["PATH"]))
    p = subprocess.run(["python3", str(TOOL)], capture_output=True, text=True, env=env)
    assert p.returncode == 2, p.stdout
    assert "NOT RUN" in p.stdout, p.stdout


def test_no_owner_repo_or_account_is_a_literal(cd):
    """Rule 4, LAW 46."""
    src = TOOL.read_text()
    body = "\n".join(l for l in src.splitlines()
                     if not l.strip().startswith("#") and "chidionyema" not in l.split("--")[0])
    for literal in ["haworks-platform", "prospector", "hermes-v2"]:
        assert literal not in body, "%s is hardcoded; discover it instead" % literal
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
    p = subprocess.run(["python3", str(TOOL), "--help"], capture_output=True, text=True)
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
