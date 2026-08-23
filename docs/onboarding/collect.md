# Onboarding — science/collect.py

## What it is for

The estate writes sixteen separate data stores. Each one is written by a single
script and read back by that same script, and nothing reads across them. That is
a pile of silos, not a pipeline, and it means every question that spans two
stores costs a throwaway script written from scratch. This collector copies all
sixteen into one table so a question costs one line of SQL instead.

It also answers a question nobody was asking: how long since each store was last
written. Two collectors had been silent for two days when it first ran, and no
alert anywhere had fired.

## What it costs

Nothing per run beyond a few seconds of local disk. It calls no model and no
network. The database it builds is about 3 MB and is rebuilt from scratch each
time, so it never grows without bound.

## What it watches, and what it does not change

It reads sixteen files under `~/.claude`, `~/Documents/code/prospector/store` and
`crew/science`. It writes exactly one file, `crew/science/warehouse.db`, and
touches nothing else. It cannot corrupt a source, because it only ever opens
sources for reading.

The warehouse is not a second ledger and must never become one. It holds no
original data. Every row in it is a copy of a row that still lives in its source
file, and the whole database can be deleted and rebuilt by running the command
again. If a source and the warehouse ever disagree, the source is right.

## Where it lives

    ~/dev/code/crew/science/collect.py      the collector
    ~/dev/code/crew/science/warehouse.db    what it builds, not in git

## Who reads it

`scripts/estate-snapshot` reads the `spend_daily` view and puts the estate's
seven-day spend rate into `STATE.md`, which is the page the founder actually
reads. That is the whole point: a number he would have to run a query to see is a
number he will never see (LAW 31). An instrument with no reader gets deleted
rather than kept (LAW 28), and this one had its reader named before it was
written.

## How to turn it off

    git -C ~/dev/code/crew revert <the commit that added science/collect.py>

Nothing schedules it yet, so there is no daemon to stop and no job to unload. If
you only want the STATE.md row gone and the collector kept, delete the `spend`
entry from the tuple in `main()` in `scripts/estate-snapshot`; the snapshot will
carry on without it and print no error.

## How to turn it back on

    python3 ~/dev/code/crew/science/collect.py

That rebuilds the warehouse from the live sources. There is no state to restore
and no migration to run, because the sources are the only truth and the warehouse
is derived from them every time.

## What goes wrong

**A source disappears or is renamed.** The run prints `ABSENT` for that source and
carries on with the rest. It does not fail, because one dead collector should not
blind you to the other fifteen. Use `--check` to make that an exit code instead.

**A source file has an unparseable line.** The line is counted in the `bad`
column and skipped. It is never guessed at and never silently dropped.

**The spend series has bad rows.** It does. There are rows stamped `1970-01-01`
from an epoch-zero bug in whatever writes that file, and the `spend_daily` view
filters them out with a date floor rather than pretending they are not there.
That filter is a workaround; the writer is still wrong and fixing it belongs to
whoever owns the spend collector.

**The staleness thresholds are wrong.** They are set per source in `STALE_HOURS`,
at roughly three times each source's own cadence, with a two-day default for
event-driven stores that are legitimately quiet. If a source reports STALE when it
is healthy, that number is the thing to change.
