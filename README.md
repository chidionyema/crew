# crew

A conversation becomes a tracked, verified build. The GitHub issue is the shared
brain, and this tool is the only thing that writes to it.

Three roles. The PM writes the spec and cannot build. Engineering builds and
cannot tick a box. QA runs the tests and is the only role that can tick one.

Read [`CREW_ORCHESTRATION_SPEC.md`](CREW_ORCHESTRATION_SPEC.md) for the shape and
[`docs/CLOSING_THE_LOOP.md`](docs/CLOSING_THE_LOOP.md) for what is not built yet.
This file is how to run it.

## Install

```bash
git clone git@github.com:chidionyema/crew.git && cd crew
ln -sf "$PWD/bin/crew" ~/.local/bin/crew
crew --version
```

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

Today a person types those commands. Nothing listens to a conversation and opens
the issue by itself, and nothing claims a checkpoint by itself.
`docs/CLOSING_THE_LOOP.md` names the three wires that would change that and the
order they go in.

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

`pr-evidence` is an estate-wide tool at `~/.claude/scripts/pr-evidence.py`, not
part of this repo. A clone on another machine needs it on `PATH` before the
`check` gate can run. This repo carries the evidence, not the camera.

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
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

`hypothesis` is not in the standard library, so the suite does not collect
without that install. Expect `14 passed`.

Property tests for the board round trip, incident tests for each way a green tick
could be a lie. No example tests of orchestration, per the testing policy in
`~/AGENTS.md`.
