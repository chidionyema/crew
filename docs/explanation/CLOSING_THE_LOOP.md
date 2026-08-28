# Closing the loop

Received 2026-08-22. A review of the crew as built, with a verification checklist and a
three-wire plan to make it run without a person in the middle. The checklist was run on this
machine the same day; the result of every line is recorded below the plan.

The crew today tracks work and refuses bad evidence. It does not yet start work on its own.
The gap in one sentence: the machinery was built and then driven by hand.

---

## 1. Verify the claims

| Claim | Verification command | Result 2026-08-22 |
|---|---|---|
| LAW 22 is in the laws file | `grep -n "LAW 22" ~/AGENTS.md` | PASS. Line 47 (rank note) and line 532 (the law). |
| `pr-evidence` exists | `which pr-evidence` | PASS. `/Users/chidionyema/.local/bin/pr-evidence` -> `~/.claude/scripts/pr-evidence.py`. |
| The tool enforces the law | `pr-evidence check --pr <n>` on a PR with no image | PASS. Exited 1 on crew#1 before evidence was attached. |
| The tool can attach | `pr-evidence attach --pr <n> shot.png --caption "..."` | PASS. `pr-evidence check --pr 1` now prints "#1 carries 1 evidence image(s)", rc=0. The image is committed at `docs/evidence/pr-1/`. |
| Issue #1 is closed | `gh issue view 1 --repo chidionyema/survival-stack` | PASS. `survival-stack #1 CLOSED`. |
| Five checkpoints passed | the issue body | PASS. CP1 to CP5 all DONE, closed by `crew close`. |
| 14 tests green | `.venv/bin/python -m pytest -q` | PASS. `14 passed in 5.17s`. |
| The lab lease exists | `ls scripts/lab-lease.py` | PASS in `survival-stack`, 9 paths tested by hand. |
| Hermes V2 is read-only | phone app | NOT CHECKED. Needs the founder's phone. |

Three lines in the received checklist named the wrong thing and were corrected before running:

- The crew repo is `/Users/chidionyema/dev/code/crew`, not `~/crew`, and `pytest` needs its
  `.venv` because `hypothesis` is not installed globally.
- Issue #1 is in `chidionyema/survival-stack`, not `chidionyema/crew`. The crew repo has no
  issues, only PR #1.
- `lab-lease.py --test` does not exist. The script takes `acquire`, `release` and `who`. The 9
  paths were tested by hand, not by a flag.

The missing requirements file is a real trap and is fixed in the same commit as this doc.
Without it nobody else can reproduce the green run.

---

## 2. Close the loop

Three wires, easiest first.

### Wire A: the listener, chat to issue

Nothing turns a conversation into a tracked issue. The received design pipes a transcript through
a regex for "we need to", "should", "must", "fix", "build", "implement" and opens an issue per
match.

**Rejected as written.** That regex fires on ordinary sentences and would open dozens of issues an
hour, and a queue full of noise is worse than no queue. It also has no dedupe against the issues
already open.

**Taken instead:** the `pm-agent` already exists as a Claude Code agent and already writes the
spec, the issue and the BDD features. The wire is the trigger, not the parser. A hook on
`UserPromptSubmit` decides one thing: does this prompt describe work the founder wants built. When
it does, it invokes `pm-agent` on the conversation so far. The judgement stays with a model that
can read the whole exchange, which is the part a regex cannot do.

### Wire B: the engineering agent, issue to claim

Nothing claims a checkpoint on its own. The received design polls `gh issue list` every 60
seconds, assigns itself, branches, commits and opens a PR.

**Taken, with the dummy work replaced.** The polling shape is right. The `run_workflow` in the
received script writes a line to a log file and commits it, which opens a PR that proves nothing.
The real body is the `engineering` agent working the checkpoint until its BDD suite passes, then
`crew evidence`, then the PR.

Two corrections to the received script before it runs: `re` is used and never imported, and
`pr-evidence attach` has no `--branch` flag. It takes `--pr`, one or more image paths and a
`--caption`, and it must run from the PR's own branch.

### Wire C: the QA agent, PR to verify

QA never verifies without a person in the middle. A GitHub Actions workflow runs the suite on a
runner the engineering agent does not control, which is what makes it independent.

**Taken.** The two refusals move into the gate:

1. `pr-evidence check --pr <n>` exits 1 when the PR carries no screenshot. LAW 22.
2. A run that matched no scenarios is a failure, not a pass. `behave` exits 0 having matched
   nothing, which is where the first false green came from. `crew/bdd.py` already requires
   `scenarios_passed + scenarios_failed > 0`; the gate calls the same code rather than a second
   copy of the rule.

The received YAML greps for a file named `*evidence*` anywhere in the tree. That passes on this
very document. The gate calls `pr-evidence check`, which reads the PR body and counts image files
under `docs/evidence/pr-<n>/`.

---

## 3. Order of work

The lab lease goes first and is not dropped. There is one lab on this machine: one set of host
ports, one docker label namespace, one network. Two test runs at once destroy each other's boxes
and the failure reads as a real defect. Two sessions each lost a cycle to it on 2026-08-22. An
autonomous engineering agent and an autonomous QA gate running at the same time is exactly that
collision, on a schedule. Wiring the lease into `features/environment.py` and `scripts/dry-run.sh`
comes before any of the three wires above.

Then A, B, C in that order, each proved by the loop running end to end: a sentence in chat becomes
an issue, the issue becomes a PR with a screenshot, the gate merges it or refuses it.

---

## 4. What was built, 2026-08-22

All three wires, on branch `the-three-wires`, tracked as CP2, CP3 and CP4 on
[issue #2](https://github.com/chidionyema/crew/issues/2). The lease went first, as this document
said it must: `survival-stack` PR #3 wires it into `features/environment.py` and
`scripts/dry-run.sh`.

**Wire A** — `integrations/claude-code/hooks/crew-listener.py`, a `UserPromptSubmit` hook.
`decide(text)` returns a verdict and the reason for it. Vetoes run first and all of them win: a
question, an acknowledgement with no instruction after it, a status check, or talk *about* the
crew rather than an instruction *to* it. On OPEN it writes `.crew/brief-<ts>.md` and prints one
line into Claude's context asking for `pm-agent`. It does not open the issue itself. A hook cannot
spawn a subagent, and a tool that opens issues while nobody is looking is the noise queue this
document already rejected.

Two things were wrong in the first cut and are worth keeping written down. It read
"ok get all the rest done" as an acknowledgement, because "ok" matched before anything looked for
the verb behind it; acknowledgements now only veto when no instruction follows. And the checkpoint
test asserts only negatives, so `return False` passes it — `tests/test_listener.py` adds 22 unit
tests over 20 real phrases from this repository's own history, which is the half the contract was
missing.

**Wire B** — `integrations/claude-code/crew-engineer.py`. It reads the board, takes the next open
checkpoint, claims it, runs that checkpoint's suite and posts evidence. It contains the string
`crew verify` zero times, and a test asserts that. The separation is the only reason the tool
exists, so the agent that builds must not be able to reach the command that ticks.

**Wire C** — `.github/workflows/crew-qa.yml`, running as `CREW_ROLE: qa-agent` on a runner the
engineering agent does not control. Seven steps: the unit suite, `scripts/verify.sh`,
`pr-evidence check --pr <n>` for LAW 22, then one `crew verify` per checkpoint named on a
`Verifies: #2 CP2 CP3` line in the pull request body. No line means nothing is ticked, which is the
safe direction to fail in.

`scripts/pr-evidence.py` moved into this repository so the runner can reach it from the checkout.
`~/.claude/scripts/pr-evidence.py` is now a symlink to it. One copy, three paths to it, no second
implementation to drift.
