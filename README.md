# crew

A conversation becomes a tracked, verified build. The GitHub issue is the shared
brain; this is the only thing that writes to it.

Read [`CREW_ORCHESTRATION_SPEC.md`](CREW_ORCHESTRATION_SPEC.md) for the shape.
This file is how to run it.

## Install

```bash
ln -sf ~/dev/code/crew/bin/crew ~/.local/bin/crew
crew --version
```

Python 3.11+, stdlib only. The one external dependency is the `gh` CLI, which is
already authenticated on this machine. `behave` is a dependency of the repo being
built, not of this tool.

## Wire a repo

```bash
cd ~/dev/code/survival-stack
crew init --bdd-command '.venv/bin/behave --no-capture --no-skipped -f plain --tags={tag}'
crew doctor
```

`crew init` writes `.crew.json` (committed — every agent needs it) and adds
`.crew/` to `.gitignore` (the active issue number is per-checkout state).

## The loop

| Who | Command |
|---|---|
| pm-agent | `crew plan brief.md --author chidionyema` |
| engineering | `crew claim CP2` → build → `crew evidence CP2 --result pass --summary "…"` |
| qa-agent | `CREW_ROLE=qa-agent crew verify CP2` |
| anyone | `crew block "CP2: …"`, `crew comment "…"`, `crew status` |
| hermes | `crew status --format telegram` |

## Why a tick means something

- `crew evidence` cannot tick a box. Only `crew verify` can.
- `crew verify` refuses when the caller posted the evidence.
- A run that matched zero scenarios is a FAIL, not a pass — `behave` exits 0 on
  an unmatched tag, and a tick from an empty run is the worst outcome available.

## Leaving GitHub

`crew/gh.py` is the only file that knows GitHub exists. It is 60 lines wrapping
the `gh` CLI. A GitLab or Gitea adapter is that file again. The issue body is
plain markdown in your repo's issue tracker, and `crew status --format json`
exports the whole board.

## Tests

```bash
.venv/bin/python -m pytest tests -q
```

Property tests for the board round trip, incident tests for each way a green tick
could be a lie. No example tests of orchestration.
