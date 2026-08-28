# Research ledger page

**What it is for.** LAW 35 says the estate researches the world before building
from memory, and records where it looked. LAW 30 says a lesson that leaves no
queryable trace taught nobody. The ledger satisfies both and is unreadable by a
person. This page is the readable end of it.

**What it costs.** Nothing recurring. It is a static HTML file generated from a
file already in the repository. No service, no database, no account.

**What it watches or changes.** Nothing. It only reads
`science/RESEARCH-LEDGER.jsonl` and writes `science/research-ledger.html`. It
never edits the ledger.

**Where it lives.** `scripts/research-ledger-page.py` in the crew repository.
The published page is at
https://claude.ai/code/artifact/10b8f6b6-7fdb-4300-9611-b89ef93b8f1c

**How to turn it off.**

```
rm ~/dev/code/crew/scripts/research-ledger-page.py
```

Nothing else depends on it. The ledger and its verifier keep working.

**How to turn it back on.** `git checkout scripts/research-ledger-page.py`.

**What goes wrong.** The page is a snapshot, so it is only as fresh as the last
time somebody regenerated and republished it. The ledger's own verifier fails
when the newest entry is over 7 days old, so a stale ledger is caught. A stale
*page* over a fresh ledger is not caught yet, and that is the known gap.
