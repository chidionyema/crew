# Demo: foresight report

## The command

    cd ~/dev/code/crew && python3 science/foresight.py report

## What it printed (2026-08-27)

```
BLIND: /private/tmp/claude-501/-Users-chidionyema-dev-code/09cd04a6-12cd-4d9b-84af-10b1620739d1/scratchpad/wt-474/science/foresight-state.json absent; run train first
exit 0
```

## What that run established

The hit rate is printed with the base rate beside it, so a model that only predicts the
majority class cannot look good. Every row it counts is a line in `science/predictions.jsonl`
with the real run's conclusion next to the forecast.

## What it looks like when it cannot measure

With no `science/ci/` history the report exits 2 and prints BLIND; the showcase page carries
the same word in the foresight row.
