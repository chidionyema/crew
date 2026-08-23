# Onboarding: science

## What this is for

The estate has 32 laws and no measurement of whether they are followed. The
science function exists to make claims about this estate falsifiable: to measure
what is actually enforced, run experiments with the threshold written down in
advance, and keep a record so the second time a question is asked it costs less
than the first.

It is a research function, not a build function. It does not ship product code
and it does not change how any other agent works without that change being
proposed, measured and agreed first.

## What it costs

Almost nothing to run. The probe is local file reading, a few seconds of CPU, no
model calls and no network. The experiments in `PLAN.md` are the only part that
costs money, and each one has its cost written into the plan before it starts.
Nothing in `science/` spends anything on a schedule.

## What it watches, and what it changes

It reads the laws, the hook wiring, the guard scripts, the tracking streams and
the session transcripts. It writes findings and plans into `science/`, and one
machine-readable verdict to `~/.claude/state/law-enforcement.json`.

It changes nothing else. It does not edit `~/AGENTS.md`, because adopting or
retiring a law is the founder's decision, not a research output. When an
experiment needs a law changed, it runs against a copy and the result is a
recommendation.

## Where it lives

`science/` in the crew repository. Five files, listed in the demo. The plan and
the goals are in `science/PLAN.md`, which is the file to read if you want to
know what this function is going to do next and by when.

## How to turn it off

There is nothing running. Every file in `science/` is inert until a person or a
scheduler calls it. To stop the function entirely, delete the directory:

```
git rm -r science/ && git commit -m "retire the science function"
```

Nothing else in the estate imports from it or depends on it, by design, so
removing it breaks nothing.

## How to turn it back on

```
git revert <the commit that removed it>
```

## What goes wrong

The probe exits 1 whenever a gap exists, and a gap almost always exists. That is
the intended signal, not a crash, and anything that treats a nonzero exit as a
failure will misreport it.

The larger risk is the one this function is most likely to fall into itself: a
measurement nobody reads. A finding written into `science/` and never opened has
cost time and changed nothing. The test of whether this function is working is
not how many findings it has produced. It is whether a number in one of them has
ever changed a decision.
