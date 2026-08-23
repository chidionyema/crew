# Demo: science

What this shows: the science function has one job in its first month, which is
to say whether the estate follows its own rules, with a number rather than an
opinion. Everything in `science/` exists to produce that number and to record
how it was got. Below is what is actually in there and what it says today. Every
block is real output from the command printed above it.

## What is in the function

```
$ ls science/
CORPUS.md
FINDINGS-01-enforcement.md
PLAN.md
enforcement-map.json
law_enforcement.py

$ wc -l science/*
      46 science/CORPUS.md
      84 science/FINDINGS-01-enforcement.md
      99 science/PLAN.md
     326 science/enforcement-map.json
     214 science/law_enforcement.py
     769 total
```

## The number it produces

```
$ python3 science/law_enforcement.py

  laws declared          : 32
  cited by a live guard  : 4   [12, 21, 24, 28]
  PROSE ONLY (no guard)  : 28   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 25, 26, 27, 29, 30, 31, 32]

  mechanical (a machine can decide it) : 17
  partial    (a smell, not a verdict)  : 9
  judgement  (will never be code)      : 6

  mechanical AND live                  : 6 of 17
  THE GAP                              : [3, 5, 7, 13, 16, 17, 22, 23, 25, 30, 31]

  23 guards: PREVENTIVE=6  DETECTIVE=5  DEAD=12
  4 stream(s) silent >24h
```

## What each file is for

`law_enforcement.py` is the probe. It answers the question and exits 1 while the
answer is bad, so a machine can read the verdict.

`enforcement-map.json` is the translation table from a law written in prose to
the check that would decide it. It is the part that makes the number mean
something, because without it "enforced" is a matter of taste.

`FINDINGS-01-enforcement.md` is the first finding, written to the rule that a
claim needs two measurements that could have disagreed and did not.

`PLAN.md` holds four goals with dates and three experiments with thresholds
written down before the experiments run, so a result cannot be graded after the
fact against a bar that moved.

`CORPUS.md` records the research data itself: 81,091 session transcripts,
6.3 GB, captured and verified, with the one command that restores them.

## What it just told us

Twelve of the twenty-three guard scripts on this machine are dead code that
nothing calls. Four of the six tracking streams have had nothing written to them
in over forty hours. Eleven laws could be enforced by a machine today and are
not. None of that was known before the probe existed, and all of it is now a
command anyone can re-run.
