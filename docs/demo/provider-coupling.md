# Demo: the provider coupling gate

Real output from real runs on 2026-08-23. Nothing here is invented; each block names the command
that produced it.

## The gate on its own selftests

```
$ python3 scripts/pr-evidence.py selftest-options
  ok   two options and a choice pass
  ok   no section fails
  ok   one option is not exhausting the options
  ok   two options and no verdict fails
  ok   stub bullets do not count as options
  ok   the section ends at the next heading
  ok   a diff with no vendor name passes with nothing written
  ok   a model id with no section fails
  ok   a vendor sdk import with no section fails
  ok   a model id with a declared swap passes
  ok   prose and docs are exempt
  ok   removing a vendor import is not adding coupling
  ok   an empty heading does not count
  ok   a coupling named with no Swap line fails
  ok   claude gets no exemption from the law it is named in
selftest-options: 15/15 passed
```

Nine of those fifteen are the new LAW 34 checks, and they are paired: every refusal has a pass
sitting next to it, so a gate that refuses everything fails the suite just as loudly as one that
refuses nothing.

## How noisy it is on real history

The worry with any new gate is that it starts asking every author for paperwork. Measured against
the last 40 real commits in this repository:

```
real commits scanned : 40
would be refused     : 0  (0%)
pass untouched       : 40
```

Zero. A pull request that adds no vendor name never sees this gate and its author writes nothing.

## But 0% is only good news if the gate is alive

So the same detector was pointed at real estate files, treated as if newly added:

```
  FIRES  ticket-gate.py             1 hit(s)  transcript layout
           transcript layout  ~/.claude/projects and its rows are still in observe's own `_CAC
  FIRES  tick.py                    1 hit(s)  transcript layout
           transcript layout  #: ~/.claude/projects -- measured 16.6s on 2026-08-23 against a
```

That is issue #53 — the ticket gate reads one vendor's transcript directory, so a session on codex
or gemini changes files and the board never sees it. The gate finds the estate's actual, named
day-0 lock-in, not a hypothetical one.

## What it caught in itself

On the first real run it flagged its own source six times, because the pattern table is by
definition a list of vendor names:

```
  FIRES  pr-evidence.py             6 hit(s)  model id,transcript layout
```

Left alone, the first pull request this gate refuses would have been the one adding it. After the
self-exemption:

```
  ticket-gate.py   1 hit(s)  ['transcript layout']
  pr-evidence.py   0 hit(s)  []
```

The real incident still fires. The self-reference does not.

## What an author sees when it refuses

```
#61 adds provider coupling (model id in scripts/tick.py) with no '## Provider coupling'
section. LAW 34: name what is coupled and add a 'Swap:' line saying what replaces it and
how long that takes
```

And what makes it pass:

```
## Provider coupling
The daily summary calls claude-opus-5 directly.
- Swap: any chat model behind providers.chat, about an hour to move
```

Three lines. The gate is not trying to stop the dependency — it is making sure somebody wrote down
the exit on the day the dependency went in, which is the only day it is cheap to know.
