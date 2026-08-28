# crew

**Start at [`STATE.md`](STATE.md).** It is the estate right now: The Architect, maestro,
Fly, and the open P1 fires. Every row is a command and its output, rebuilt hourly, and a
row that could not be measured says NOT RUN rather than PASS. Read it before you measure
anything yourself and before you ask the founder anything.

**Who we are to each other:** [`docs/explanation/ROAD-TO-9D.md`](docs/explanation/ROAD-TO-9D.md) is the two-stage road
from the [depth-psychology audit](docs/audits/depth-psychology-founder-and-crew-2026-08-28.md)
of the founder and the crew to one organism; [`roles/founder.md`](roles/founder.md) is who he
is. Pinned as crew#596. Read them when you wonder why a rule exists.

A conversation becomes a tracked, verified build. The GitHub issue is the shared
brain, and this tool is the only thing that writes to it.

Three roles. The PM writes the spec and cannot build. Engineering builds and
cannot tick a box. QA runs the tests and is the only role that can tick one.

Read [`docs/explanation/CREW_ORCHESTRATION_SPEC.md`](docs/explanation/CREW_ORCHESTRATION_SPEC.md) for the shape and
[`docs/explanation/CLOSING_THE_LOOP.md`](docs/explanation/CLOSING_THE_LOOP.md) for how the three wires
that run it without a person came to be built. This file is how to run it.

## Install

One command sets up the machine. Run it again after a pull; it does the same
thing the second time as the first.

```bash
curl -fsSL https://raw.githubusercontent.com/chidionyema/crew/main/scripts/install-crew -o /tmp/install-crew
bash /tmp/install-crew
```

Or from a checkout you already have: `./scripts/install-crew`.

It checks `python3`, `git` and `gh`, clones the repo if it is not there, builds
`.venv`, puts `crew`, `pr-evidence`, `lab-lease` and `crew-triage` on your
`PATH`, writes `~/.crew/config`, and finishes by running `crew health` so you
see the state rather than a claim about it.

Python 3.11+, standard library only. The one external dependency is the `gh` CLI,
authenticated against the repo you are tracking. `behave` belongs to the repo
being built, not to this tool.

## Wire a repo

```bash
cd ../survival-stack
crew init --bdd-command '.venv/bin/behave --no-capture --no-skipped -f plain --tags={tag}'
crew doctor
```

`crew init` writes `.crew.json`, which is committed because every agent needs it,
and adds `.crew/` to `.gitignore`, because the active issue number is state that
belongs to one checkout.

`crew doctor` checks `gh` auth, the BDD command and the issue before you rely on
any of them.

## The loop

| Who | Command | What it does |
|---|---|---|
| pm-agent | `crew plan brief.md --author chidionyema` | Opens the issue with one checkbox per checkpoint and writes one feature file per tag. |
| engineering | `crew claim CP2` | Puts your name on the checkpoint so two people do not build it at once. |
| engineering | `crew evidence CP2 --result pass --summary "…"` | Runs the BDD suite for `@cp2` and posts the counts. Cannot tick the box. |
| qa-agent | `CREW_ROLE=qa-agent crew verify CP2` | Runs the same suite independently. Ticks the box only on a real green run. |
| anyone | `crew block "CP2: …"` | Marks the checkpoint blocked with a reason. |
| anyone | `crew comment "…"`, `crew status` | Adds to the thread, or prints the board. |
| anyone | `crew close` | Closes the issue. Refuses while any box is unticked. |
| hermes | `crew status --format telegram` | The phone view. Read only. |

A person can type all of those. Three wires also drive them without one, and
they are described under "The loop with nobody typing" below.

## The loop with nobody typing

Three wires. Each one does exactly one handoff and stops.

**The listener** — `integrations/claude-code/hooks/crew-listener.py`. A Claude
Code `UserPromptSubmit` hook. It reads what you just typed and decides one
thing: does this describe work you want built. A question, an acknowledgement,
a status check or a remark about the crew is vetoed, and vetoes beat matches.
When it opens, it writes the brief to `.crew/brief-<timestamp>.md` and asks for
`pm-agent` in the conversation. It does not open the issue itself, on purpose: a
tool that files issues while nobody is looking fills the queue with noise.

```bash
echo "we need a retry on the webhook" | integrations/claude-code/hooks/crew-listener.py --dry-run
```

Wire it by adding the script as a `UserPromptSubmit` hook in
`~/.claude/settings.json`.

**The engineer** — `integrations/claude-code/crew-engineer.py`. Reads the board,
takes the next open checkpoint, claims it, runs that checkpoint's suite, posts
the evidence. It contains the words `crew verify` zero times and a test asserts
that, because the whole point is that the thing which builds cannot tick.

```bash
integrations/claude-code/crew-engineer.py --dry-run     # says what it would take
```

**The QA gate** — `.github/workflows/crew-qa.yml`. Runs on every pull request as
`qa-agent`, on a runner the engineer does not control. The unit suite,
`scripts/verify.sh`, then `pr-evidence check` for LAW 22, then one `crew verify`
for each checkpoint named on a line in the pull request body:

```
Verifies: #2 CP2 CP3 CP4
```

No such line, nothing is ticked. That is the safe direction to fail in.

## Every command, in plain English

One word does both halves of the job. The board verbs come from the python CLI
in `bin/crew`; the machine verbs come from the wrapper the installer writes.
Neither shadows the other, so `crew status` and `crew start` are both just
`crew`.

### The board — what the crew is building

| Command | What it does |
|---|---|
| `crew plan brief.md --author you` | Reads a brief, writes a spec, opens the GitHub issue with one checkbox per checkpoint. This is the only way a tracked build is created. |
| `crew status` | Prints the board: which checkpoints are done, which failed, when. |
| `crew claim CP2` | Puts your name on a checkpoint so two people do not build it at once. |
| `crew evidence CP2 --result pass --summary "…"` | Posts what you built and what the suite said. It cannot tick the box. |
| `crew verify CP2` | Runs the suite again, independently, and ticks the box only on a real green run. Refuses if you are the one who posted the evidence. |
| `crew block "CP2: waiting on X"` | Says out loud that a checkpoint is stuck, and why. |
| `crew comment "…"` | Adds a note to the issue thread. |
| `crew close` | Closes the issue. Refuses while any box is unticked. |
| `crew doctor` | Checks the five things the loop needs — `gh` auth, config, the test runner, the marked tests, the issue — and prints PASS or FAIL for each. |
| `crew init` | Wires a new repo: writes `.crew.json`, which is committed so every agent agrees. |

### This machine — is the plumbing up

| Command | What it does |
|---|---|
| `crew health` | The whole picture in one screen: prerequisites, tools on `PATH`, the suite, services, then `crew doctor`. Exits non-zero if anything is wrong, so a script can call it. |
| `crew test` | Runs the unit suite in the venv. Extra arguments go straight to pytest. |
| `crew start` | Starts the notification listener on `127.0.0.1:8081` and prints the board. |
| `crew stop` | Stops it. |
| `crew logs` | Follows what the listener has been told. |
| `crew notify "CP2 is green"` | Pops a desktop notification. For when hermes is down and something still needs to reach you. |
| `crew open` | Opens the tracked issue in a browser. The issue is the board; there is no second dashboard to keep alive. |
| `crew update` | Pulls, then re-runs the installer. |

### The other scripts

**`scripts/install-crew`** — the one command above. Sets this machine up from
nothing, and is safe to run again.

**`scripts/verify.sh`** — proves a checkout is sound. Every file in
`scripts/verify.d/` runs, prints the commands it ran and their raw output, and
exits 0, 1 or 2. The harness counts those and prints `PASS=n FAIL=n CANNOT
RUN=n`. Nothing states a result in prose, so the count cannot drift from what
the commands did.

```bash
scripts/verify.sh            # everything
scripts/verify.sh 40 70      # only the checks whose names start 40 or 70
scripts/verify.sh --log run.log
```

**`scripts/crew-triage`** — opens one issue that shows its work: what was asked,
what was found, what was decided and why, what proves it, what is left. Use it
for a single decision. Use `crew plan` for a build with checkpoints — that shape
is parsed by `crew status` and must not be hand-written.

```bash
crew-triage --title "Drop the second config loader" \
    --origin "he asked why doctor named a file that was not there" \
    --decision "one loader, LAW 23: the other path was four times the work" \
    --evidence "$(git rev-parse --short HEAD)" --dry-run
```

`--dry-run` prints the body and opens nothing, so you can read it before
spending an issue number.

**`scripts/notify.py`** — one desktop notification.
`scripts/notify-server.py` is the same thing behind
`POST 127.0.0.1:8081/notify`, for an agent that cannot pop a window itself. It
binds to loopback only, on purpose: it runs `osascript` with text from the
request and must never be reachable from a network.

**`scripts/pr-evidence.py`** — the camera for LAW 22. See the pull request
section below. `~/.claude/scripts/pr-evidence.py` is a symlink to this file, so
the estate-wide tool and the copy CI checks out are the same bytes.

**`lab-lease`** — one lab, one holder. It lives in `survival-stack` and the
installer only puts it on your `PATH`. Two test runs at once destroy each
other's containers and the failure reads as a real defect.

### The documents

**`FOUNDER.md`** — how he works and what he will not sit through. Read it before
working an issue. `~/AGENTS.md` is the law and outranks it.

**`docs/decisions/DECISIONS.md`** — what was decided and why, numbered. Read it before asking
anything; the answer is usually already a line in it. Cite the entry number when
you apply it.

**`docs/reference/PREFERENCES.md`** — what he reaches for when nothing forces the choice.
Python for tools, bash for glue, property tests over example tests, raw output
over a summary.

**`docs/decisions/CORRECTIONS.md`** — every time he had to say something twice. A correction
here already cost him a turn. One that keeps happening becomes a law or a guard,
never a note.

**`.github/ISSUE_TEMPLATE/crew_task.md`** and
**`.github/pull_request_template.md`** — GitHub fills these in for you.
`docs/reference/ISSUE_TEMPLATE.md` and `docs/reference/PR_TEMPLATE.md` at the root are pointers at those two,
not copies, because two copies of one template drift apart.

## Why a tick means something

- `crew evidence` cannot tick a box. Only `crew verify` can.
- `crew verify` refuses when the caller is the role that posted the evidence.
- A run that matched zero scenarios is a FAIL. `behave` exits 0 on an unmatched
  tag, so `crew/bdd.py` requires `scenarios_passed + scenarios_failed > 0`. A tick
  from an empty run is the worst outcome available, and it has happened.
- Every verification, pass or fail, is appended to a log in the issue body. The
  failures stay visible after the box goes green.

## Evidence on a pull request

LAW 22: a pull request carries a screenshot of the run that proves it, committed
into the pull request's own branch under `docs/evidence/pr-<n>/`. Not GitHub's
attachment store, which does not survive leaving GitHub.

```bash
.venv/bin/python -m pytest -q > /tmp/run.log 2>&1
pr-evidence shot - --out /tmp/p.png --title "pytest -q" < /tmp/run.log
pr-evidence attach --pr 4 /tmp/p.png --caption "14 tests green on this branch"
pr-evidence check --pr 4     # exits 1 when the pull request carries nothing
```

The tool lives at `scripts/pr-evidence.py` in this repo, and
`~/.claude/scripts/pr-evidence.py` is a symlink to it. It is in the repo so a CI
runner gets it from the checkout instead of needing the estate installed; it is
on `PATH` so any repo on this machine can call it. One copy either way.

## Verify a checkout

```bash
scripts/verify.sh                                   # every check
scripts/verify.sh 40 50                             # only these
scripts/verify.sh --log run.log                     # tee it, ready for a screenshot
CREW_PR=4 CREW_ISSUE_REPO=owner/name CREW_ISSUE=1 scripts/verify.sh
```

Each check in `scripts/verify.d/` prints the commands it runs and their raw
output, then exits 0 for PASS, 1 for FAIL, 2 for CANNOT RUN. The harness counts
those exit codes and prints the total. Nothing states a result in prose, so the
count cannot drift from what the commands did.

CANNOT RUN is a third state on purpose. A check that needs `gh` auth, a pull
request number or a laws file this machine does not have reports that it did not
run, rather than passing quietly. Only a FAIL makes the harness exit 1.

To reuse the harness in another repo, copy `scripts/verify.sh` and write your own
`verify.d/`. The harness knows nothing about crew.

`35-evidence-gate-refuses.sh` is a negative control: it strips the evidence off a
real pull request, proves `pr-evidence check` refuses it, and restores the body
from a trap. It edits a live pull request, so it only runs with
`VERIFY_ALLOW_MUTATION=1`.

## Roles and agents

`roles/` holds the three role definitions in plain markdown, which is what a
human or any agent tool reads to know what it may and may not do.

`integrations/claude-code/agents/` holds `pm-agent.md` and `qa-agent.md` as Claude
Code subagents. `integrations/hermes/skills/crew-orchestration/SKILL.md` is the
phone surface, and it is read only by design.

## Leaving GitHub

`crew/gh.py` is the only file that knows GitHub exists. It wraps the `gh` CLI. A
GitLab or Gitea adapter is that one file written again. The issue body is plain
markdown in your own tracker, and `crew status --format json` exports the whole
board in one command.

## Tests

```bash
python3.11 -m venv .venv          # the version matters -- see below
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

Name the version. This said `python3 -m venv .venv` until 2026-08-24, and on this
laptop `python3` was anaconda's 3.10.9 while `crew-qa.yml` pinned 3.11 and the line
above said "Python 3.11+". Nothing could see the disagreement, so `ruff check --fix`
rewrote `timezone.utc` into `datetime.UTC` — correct for the 3.11 it was configured
for, unimportable on the 3.10 that actually ran it — and the code-standard gate
printed PASS over code that crashed on import.
`tests/test_incident_linter_target_newer_than_the_interpreter.py` now fails instead.

`hypothesis` is not in the standard library, so the suite does not collect without
that install. The count is not written here because a number in prose goes stale and
then gets believed; `pytest -q` prints it.

The checkpoint suites are separate and are not in the default run:
`.venv/bin/python -m pytest -q -m cp2 checkpoints`.

Property tests for the board round trip, incident tests for each way a green tick
could be a lie. No example tests of orchestration, per the testing policy in
`~/AGENTS.md`.
