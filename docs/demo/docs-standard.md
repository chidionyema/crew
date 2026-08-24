# Demo: the documentation standard

Owner: claude/science
Last true: 2026-08-24

Real output from a real run on 2026-08-24. Nothing below is invented.

## What the estate looked like before the gate existed

```
$ python3 science/docsmap.py
...
documents        190 / 190
persisted        186 / 190
owned              0 / 190
dated             99 / 190
substantial      187 / 190
passing all        0 / 190
```

Not one of the estate's 190 documents named a maintainer. Four existed only on this
laptop and were held by no repository at all, including an onboarding page written the
same morning by another session for a tool it was in the middle of installing.

## The gate refusing a document that does not meet the standard

A new file with a heading and three words in it:

```
$ printf '# Notes\n\nsome text\n' > docs/zz-probe.md
$ bash scripts/verify.d/95-docs.sh ; echo "rc=$?"
FAIL: 1 document(s) introduced that do not meet the standard.
  ~/dev/code/crew::docs/zz-probe.md
      missing: dated, owned, persisted, substantial

  persisted    -> git add the file. A document only this laptop holds is lost.
  owned        -> add a line `Owner: <name or role>` near the top.
  dated        -> add a YYYY-MM-DD date saying when this was last true.
  substantial  -> write more than 200 characters of actual prose, or delete it.
rc=1
```

The refusal names every rule that failed and says what to type. A guard whose message
sends you to read its source has not guarded anything, it has added a puzzle.

## The gate allowing a document that does meet it

The same file, rewritten with an owner, a date and real prose, then staged:

```
$ bash scripts/verify.d/95-docs.sh ; echo "rc=$?"
PASS: 191 documents graded, 1 meet the standard, 190 on the baseline backlog,
      0 new failures, 0 regressions
rc=0
```

Both halves matter. A gate that has only ever been shown saying no is a gate nobody has
proved is safe to install, and this estate has twice shipped one that refused correct
work and blocked every push on the machine.

## Inside the full suite

```
$ bash scripts/verify.sh
PASS: 16 entries, newest 2026-08-24, every entry carries sources
PASS: 11 risks, 1 mitigated or closed, every receipt runnable
PASS: 191 documents graded, 1 meet the standard, 190 on the baseline backlog
PASS=9  FAIL=0  CANNOT RUN=3   of 12
```

The one document meeting the standard is `ARCHITECTURE.md`, written the same day. The
other 190 are the backlog, tolerated by a committed baseline so that turning the
standard on did not turn CI red for a month.
