# Onboarding — science/foresight.py

## What it is for

Founder, 2026-08-27: "lets get to Self-aware estate now asap." Foresight is the first
self-grading prediction in the estate (crew#405): it predicts whether an open PR's first CI
run will be red, writes the prediction to `science/predictions.jsonl`, then scores it
against the real run.

## Who reads it

The science lane, the showcase page (which prints the hit rate beside the base rate), and
anyone deciding whether to trust the estate's own forecasts.

## The commands

    python3 science/foresight.py pull      # runs + PRs from four repos into science/ci/
    python3 science/foresight.py train     # logistic regression, time-ordered holdout
    python3 science/foresight.py predict   # one row per open PR
    python3 science/foresight.py score     # grade every unscored row
    python3 science/foresight.py report    # what the model knows and how often it was right

## The failure it names

A model that cannot beat the base rate says so in `science/foresight-state.json` and the
page prints that sentence. No history on disk is BLIND (exit 2), never a model: a forecast
with no data is a refusal, not a guess.

## Scheduling

`com.founder.sciencecollect` (crew scheduler) runs pull, predict and score before the showcase
regenerates, so the page never shows a stale hit rate.
