# Demo: the research ledger as a page

The ledger is a JSONL file. Nobody reads a JSONL file on a phone, which is why
the founder asked twice where the research had gone. This turns it into one page.

```
$ python3 scripts/research-ledger-page.py
/Users/chidionyema/dev/code/crew/science/research-ledger.html  22962 bytes  4 entries
```

Published: https://claude.ai/code/artifact/10b8f6b6-7fdb-4300-9611-b89ef93b8f1c

What the page shows, taken from the ledger and nothing else:

- 4 entries, 56 sources read, 4 awaiting a measurement.
- Each entry gives the question, the decision it fed, the findings, and the
  metric with its before and after values.
- An entry whose `metric_after` is still null shows an amber "not yet measured"
  chip, so a claimed improvement that was never measured is visible rather than
  buried.
- Sources are collapsed behind a count and expand to the real URLs. The tooling
  entry carries 40 of them.

The verifier that grades the underlying ledger, run in the same session:

```
$ bash scripts/verify.d/80-research-ledger.sh
PASS: 4 entries, newest 2026-08-24, every entry carries sources, none unmeasured past 14 days
```
