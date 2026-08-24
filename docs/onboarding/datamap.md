# Onboarding — the data map

## What it is for

It answers three questions about the estate's data that nobody could answer before, and
it answers them by measurement rather than by description, so the answer cannot drift
away from the truth while still reading as current.

1. What do we collect, and what is actually inside it?
2. What exists on this machine that nothing collects, and why not?
3. What does the estate do every day and keep no record of at all?

The third list is the one that matters most. A gap you have written down is a decision.
A gap nobody has written down is a surprise waiting for whoever needs the number.

## What it costs

Nothing recurring. It is one Python file with no dependencies outside the standard
library. It reads the warehouse that already exists and the inventory that already runs,
and it holds both in memory for about a second. It writes one small file,
`science/shapes.json`, roughly 30 KB, which is the record of what the data looked like
last time so the next run can tell you what moved.

## What it watches or changes

It reads `science/warehouse.db` and `~/.estate/state/inventory.json`. It changes
nothing anywhere. The only file it writes is `science/shapes.json`, and that file exists
solely so the drift comparison has something to compare against.

It does not read the contents of your transcripts, your credentials or anything under
`~/.claude/telemetry`. It reads the sizes and row counts the inventory already recorded
for those, and nothing more.

## Where it lives

`science/datamap.py` in the crew repository. The reasons a store is uncollected are a
table at the top of that file, `WHY_UNCOLLECTED`, so adding a reason is one line and the
reason travels with the code rather than living in a document that rots.

## How to turn it off

It is not scheduled and it changes nothing, so there is nothing running to stop. If it
is later wired into the hourly collection and you want it out:

```
launchctl unload ~/Library/LaunchAgents/com.founder.sciencecollect.plist
```

## How to turn it back on

```
launchctl load ~/Library/LaunchAgents/com.founder.sciencecollect.plist
```

## What goes wrong

**It says the warehouse is missing.** The collector has not run. `python3
science/collect.py` builds it from the sources on disk in a few seconds.

**It says a store is `UNEXPLAINED`.** That is the tool working, not failing. Something
exists on this machine that nothing reads and nobody has recorded a decision about. Add
a line to `WHY_UNCOLLECTED` saying what it is and why it is not collected, or wire a
collector to it.

**`--check` exits 1 and reports fields appearing or vanishing.** A producer changed its
output. That is not automatically a problem, but nothing else on the estate would have
told you, so look at what changed before accepting it into `shapes.json`.

**The counts disagree with a number you remember.** Trust the run. The numbers here are
computed from the rows that exist at the moment you ask, which is the whole reason the
map is generated rather than written.
