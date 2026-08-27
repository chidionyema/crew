# Demo: is the research capability actually feeding the machine?

Founder, 2026-08-27: "everything needs to be feeding the machine to have real intelligence, how
is our general purpose research capability" and "we have to be inwardly facing as well as
outwardly facing".

Two directions, graded separately, both from stores that already exist.

```
python3 science/research_grade.py --print
```

Expect the two-row grade table first — **Outward** (25 questions, 25 fed a decision, 245 sources,
0 stale) and **Inward** (foresight trained on 565 labelled PRs, 0 of 11 predictions scored, so
GAP) — then a block for each. Any question over 7 days with no decision renders as a `RED <n>d`
row with its ticket and owner; today there are none.

The guard, for CI or a hook:

```
python3 science/research_grade.py --check    # exit 1 when a question has gone stale
```

The inward number underneath it:

```
python3 science/foresight.py report          # what the model knows and how often it was right
```

Run 2026-08-27: holdout accuracy 0.602 against a base rate of 0.593 on 113 unseen PRs — a thin
edge, printed next to the base rate so it can never read as a claim it is not. The committed
record is `science/foresight-model.json`; `science/foresight-state.json` and `science/ci/` are
gitignored working files.
