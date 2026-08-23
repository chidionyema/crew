# Onboarding: law-enforcement

## What this is for

The 32 laws are prose. Prose does not stop anything. This measures how many of
them a machine actually enforces, so the answer to "is the estate following its
own rules" stops being a claim and becomes a number. Today that number is 6 of
17 laws that a machine could decide. The other 11 are written down and nothing
checks them.

## What it costs

Nothing per run beyond a few seconds of local CPU. No model calls, no network,
no API spend. It reads files on this machine and prints a table. Running it a
hundred times a day would cost nothing measurable.

## What it watches, and what it changes

It watches three things and changes one.

It reads `~/AGENTS.md` for the law headings, `~/.claude/settings.json` for which
guards are wired into a hook, and every guard script under `~/.claude/scripts`
and `~/Library/LaunchAgents` to work out which of them anything still calls. It
also checks six tracking files for how long since anything was written to them.

The only thing it writes is `~/.claude/state/law-enforcement.json`, which is the
same verdict in a form another program can read. It never edits a law, a guard,
a setting or a hook. It cannot break anything, because it only reads.

## Where it lives

`science/law_enforcement.py` in the crew repository, with its translation table
next to it at `science/enforcement-map.json`. That JSON file is the part worth
knowing about: it holds, for each law, whether a machine can decide it at all,
the exact check that would decide it, where that check belongs, and whether such
a check exists today. When a law changes, that file is what needs editing.

## How to turn it off

It is a script that runs when something calls it. Nothing calls it on a schedule
yet, so there is nothing running to stop. If it is later put on a schedule and
you want it gone:

```
launchctl bootout gui/$(id -u)/com.chidionyema.law-enforcement
```

## How to turn it back on

```
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.chidionyema.law-enforcement.plist
```

## What goes wrong

Two things, both by design rather than by accident.

It exits 1 whenever a gap exists, which is almost always, so anything that treats
a nonzero exit as a crash will report it as broken when it is working correctly.
Read the exit code as the verdict, not as an error.

It can also drift. If a guard is added to the estate and nobody adds it to
`enforcement-map.json`, the probe prints a line saying so rather than quietly
ignoring it. That line is the thing to act on: it means the map has stopped
describing the estate, and a map that has stopped describing the estate is worse
than no map because it still reads like a record.
