# Onboarding — the Lanes section of the science showcase

## What it is for

crew#508. The showcase page used to answer "is the science lane healthy". It now answers
"is every lane feeding the machine", because a lane that emits nothing looked identical to a
lane that was quiet and fine.

## Where it lives

`science/showcase.py`: `LANE_SOURCES` (the mapping), `lanes()` (the counts and grades),
the `"Lanes"` entry in `SECTIONS`, and the `title == "Lanes"` branch of `render()`.

## The commands

    python3 science/showcase.py --print          # the page, written nowhere
    python3 science/showcase.py                  # writes docs/science/SHOWCASE.md
    python3 -m pytest -q tests/test_crew508_lanes_section.py

## Adding a source to a lane

A source is counted only where `LANE_SOURCES` names it. An unrecognised source is **not**
absorbed into a nearby lane; it lands in a row called `unmapped` and the page prints
"add them to LANE_SOURCES in science/showcase.py" underneath. That is the whole maintenance
loop: run the page, read the unmapped row, add the name to the lane it belongs to.

## Checkpoints

Counted from `- [x]` lines in the ledgers the page already reads (`CHECKPOINT_LEDGERS`), and
only from a ledger written inside the 24h window — a ticked box carries no timestamp of its
own, and dating it any other way would be a number the page cannot reproduce. When no ledger
qualifies, every lane shows 0 and the page prints the reason with the files it searched.

## The refusal you should expect

No warehouse, or a warehouse with no `facts` table, renders
`BLIND: science/warehouse.db has no readable facts table (...)`. It never renders six zeroes.
