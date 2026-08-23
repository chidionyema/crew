# Silent side effects

## What it is for

The estate runs about twenty-five guards. Each one ends by writing a line
somewhere: a ledger row, a state file, a message. If that write fails inside a
`try` with an empty `except`, the guard keeps its green tier and stops doing
its job, and there is no signal anywhere that says so. This finds those places
before they cost a week.

## What it costs

One read pass over the scripts directory. No network, no model calls, under a
second, nothing written.

## What it watches or changes

It reads `~/.claude/scripts` by default, or any directory given as an argument.
It changes nothing. It is report-only on purpose: the repair is a judgement
about what each handler should do instead, and that is not a machine's call.

## Where it lives

`~/.claude/scripts/silent_side_effect.py`, in the claude-guards repository,
beside the guards it protects. It started here in crew and moved on 2026-08-23
when `hooks/pre-commit` began importing it: a check whose implementation lives
in a different checkout is one missing clone away from passing everything.

## How to turn it off

It runs inside the commit gate for the claude-guards checkout only. For a
single commit, `ESTATE_GUARDS_OFF=1 git commit`. To stop it everywhere,
`git config --global --unset core.hooksPath`, which also stops the credential
check, so prefer the single-run switch.

## How to turn it back on

Nothing to do — it is part of the commit gate. To check the whole estate at
any time rather than only what is being committed, the demo page has the
command.

## What goes wrong

It reports a handler that is deliberately best-effort. Deleting a leftover
temporary file is the common case, so those are counted separately and hidden
unless `--all` is passed. If a genuinely intentional silent write shows up in
the main list, the honest fix is a one-line comment in the handler saying why,
not a change to this script: a detector that learns to ignore things is a
detector that will one day ignore the thing that matters.
