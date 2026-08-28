# Onboarding — science/outcomes.py

## What it is for

The estate measures itself thoroughly and measures its results not at all. Sixteen
data stores record guards, laws, complaints and tokens; none records what any of
it produced. That is why the spend number had no denominator: $854/day is
frightening or fine depending entirely on what came out the other side, and
nothing anywhere said.

This collects two kinds of outcome. Delivery — commits, pull requests merged, per
day, per repository — which divides into spend. And predictions — a causal claim
written down before a repair and scored after it, which is the only way the estate
ever learns whether it can tell what caused what.

## What it costs

Nothing per run except a few seconds. `ship` shells out to `git log` in six
repositories and once to `gh pr list`. No model calls. The two ledgers it writes
are a few hundred kilobytes and `ships.jsonl` is rewritten rather than appended,
so it cannot grow without bound.

## What it watches, and what it changes

It reads git history in `crew`, `maestro`, `hermes-v2`, `prospector-main`,
`survival-stack` and `~/.claude`, and the merged pull requests on the crew board.
It writes two files, `science/ships.jsonl` and `science/predictions.jsonl`, and
nothing else. It changes no repository and cannot: it only ever runs `git log`.

`predictions.jsonl` is append-only and a score is never revised. Scoring is a
separate subcommand from predicting for the same reason: a prediction you can edit
after seeing the answer is not a prediction.

## Why these are new files rather than an append to something existing

LAW 30 says prefer one line appended to what exists over a new store, and this
estate has built two half-filled ledgers before. The exception here is narrow and
worth stating. `method_metrics.json` has a `predictions` slot, but `reflect.py`
regenerates that file wholesale every four hours, so anything appended to it is
erased within the hour. There is no existing store of delivery outcomes at all.
These are the first of their kind, not a second copy of one.

## Where it lives

    ~/dev/code/crew/science/outcomes.py          the collector
    ~/dev/code/crew/science/ships.jsonl          delivery, rewritten each run
    ~/dev/code/crew/science/predictions.jsonl    predictions, append-only

Both ledgers are ingested by `science/collect.py` into the warehouse, where the
`value_daily` view joins delivery against spend.

## Who reads it

`value_daily` is read by whoever asks what the money bought — today that is this
role and the cost work on P1 #26. The delivery half has a reader before it was
built. The predictions half does not yet, and that is stated plainly rather than
dressed up: it exists to give LAW 29 a denominator, and if sixty days pass with
nothing scored, delete it (LAW 28) rather than keep an empty table that reads as a
system which keeps evidence.

## How to turn it off

    git -C ~/dev/code/crew revert <the commit that added science/outcomes.py>

Nothing schedules it, so there is no daemon to stop. Deleting the two `.jsonl`
files removes the collected data; `ship` rebuilds its half from git on the next
run, and predictions cannot be rebuilt because they are original data. That is the
one thing here worth backing up.

## How to turn it back on

    python3 ~/dev/code/crew/science/outcomes.py ship

## What goes wrong

**`gh` is missing or not authenticated.** The pull-request half returns nothing and
the commit half still works. It fails quiet on purpose, because losing the PR
column should not cost you the commit column.

**A repository in `REPOS` is moved or deleted.** It is skipped silently. The list
is hard-coded and is the six trees with a commit in the last seven days as of
2026-08-23; when that stops being true, edit the list.

**Someone reads `usd_per_commit` as a productivity score.** This is the real
hazard. Commits are trivially gameable and the number improves if you simply
commit more often. It is an upper bound on cost per change and nothing more. If it
ever appears in an argument about whether work was worth doing, the number is
being misused.

**Nobody ever scores a prediction.** Then the hit rate stays unmeasurable, which is
exactly the state the estate was already in, and the ledger should be deleted
rather than kept as decoration.

## The founder cost series

**What it is for.** LAW 36 says the founder is one of the platform's two customers and that
his complaint is a measurement, not a mood. Nothing kept the measurement. This collects it:
how many messages the estate needed from him each day, and what share of them were
complaints, since 28 July 2026.

**What it costs.** Nothing new is written by anybody. It reads `~/.claude/directives`, which
`directive-capture.py` has been filling since July, and derives one row per day. It runs
inside the hourly `com.founder.sciencecollect` job that was already running.

**Where it lives.** `science/attention.jsonl`, ingested into `warehouse.db` as the
`attention` source and joined to money and delivery by the `attention_daily` view. He sees
it as the `founder cost` row on `STATE.md`.

**How to turn it off.** `launchctl bootout gui/$(id -u)/com.founder.sciencecollect` stops the
whole collector. To stop only this part, delete the `attention` line from `SOURCES` in
`science/collect.py`; the rest of the warehouse is unaffected.

**What goes wrong.**

**The complaint count is a proxy and a crude one.** It matches 43 words borrowed from
`founder_board.py`. It counts an angry word, not an unmet need, so a calm sentence saying
the same thing scores zero and a joke containing a swear word scores one. It is published
as a rate over his own volume because the trend is the part worth reading; a single day's
number means very little.

**The lexicon can fail to load.** `founder_board.py` is imported at runtime rather than
copied, so two lists of his own words cannot drift apart. If that import fails, every
complaint count is zero, which would read as a calm week. The command prints a warning
saying the zeros mean "not measured" for that reason, and the count is never silently clean.

**Nobody looks at the row.** Then it is not an instrument (LAW 28) and it should be deleted
rather than left on the page implying somebody is watching.
