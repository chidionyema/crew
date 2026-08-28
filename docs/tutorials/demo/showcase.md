# Demo — science/showcase.py

Founder, 2026-08-27: "we need more transparency the capabilities and progress from the
science / research data and machine learning lane, we need a proper showcase."

The showcase is one page, `docs/science/SHOWCASE.md`, generated from the stores the lane
writes. Nothing on it is typed by hand.

    $ cd ~/dev/code/crew && python3 science/showcase.py

    wrote docs/science/SHOWCASE.md
      Capabilities         ok
      Warehouse            ok
      Data map (LAW 50)    ok
      Research ledger      ok
      Delivery outcomes    ok
      Predictions          ok

Open the page. Six sections, each headed by the command that reproduces its numbers, and a
progress section at the top listing every number that moved since the previous run.

## When a store is missing

    $ mv science/RESEARCH-LEDGER.jsonl /tmp/ && python3 science/showcase.py
      Research ledger      BLIND: .../science/RESEARCH-LEDGER.jsonl absent

The section renders `BLIND:` with the path, never an empty table. Incident test:
`tests/test_incident_crew403_showcase_absent_source_is_blind.py`.

## Scheduled

`scripts/science-collect` (launchd `com.founder.sciencecollect`, four times a day) runs the
generator as its last step, so the page is at most six hours behind the stores.
