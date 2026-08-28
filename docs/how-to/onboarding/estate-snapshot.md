# Onboarding: estate-snapshot

## What is this for

Six agent sessions run on this estate and none of them can see the others. Before this existed,
every session that wanted to know whether something was working measured it again from scratch,
and when it could not find out cheaply it asked the founder. He had usually answered the same
question earlier that day. The crew issues record decisions and the git history records changes,
but nothing recorded the live state of the estate at this moment.

`STATE.md` at the root of this repo is that record. It is one page, it lives in git, it has a
URL, and anyone with the repo can read it without running anything.

## What it costs

Roughly forty seconds of wall clock per run and no money. It shells out to `bin/verify` in
hermes-v2, reads two files under `~/.maestro`, and makes two network calls, one to Fly and one
to GitHub. Every call has a timeout, so a hung provider produces a `NOT RUN` row rather than a
hung script.

## What it watches, and what it never changes

It watches four things: The Architect, through `bin/verify` in `~/dev/code/hermes-v2`; maestro,
through the newest file in `~/.maestro/intents` and the `skills` table of its experience graph;
Fly, through `flyctl apps list`; and the open P1 issues on the crew board.

It changes nothing. It runs no repair, starts no machine, edits no config. The only file it
writes is `STATE.md` in this repository. That is deliberate: a page that both measures and
repairs cannot be trusted about either.

## Where it lives

The generator is `scripts/estate-snapshot` in this repository. Its output is `STATE.md`, also in
this repository, so the snapshot travels with the git bundle and survives losing any single
provider.

## How to turn it off

```
git rm scripts/estate-snapshot STATE.md
```

Nothing else depends on it. It is a reader, so deleting it removes a view and breaks no other
part of the estate.

## How to turn it back on

```
git checkout HEAD~1 -- scripts/estate-snapshot && ./scripts/estate-snapshot
```

## What goes wrong

The most likely failure is that a row says `NOT RUN`. That means the measurement itself could
not be taken, not that the thing is broken, and the row names which command failed. Treat a
`NOT RUN` on The Architect as urgent, because it means `bin/verify` has stopped producing a
verdict, and a verify that cannot report is indistinguishable from an estate nobody is checking.

The second failure is staleness. The page is only true at the timestamp in its header. If that
timestamp is hours old, regenerate it rather than believing it.
