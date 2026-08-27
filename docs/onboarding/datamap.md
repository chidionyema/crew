# Onboarding — the data map (LAW 50)

**What it is.** A closed-world register of every producer of data in the estate. Three files
in `science/`:

| File | Role |
|------|------|
| `producers.py` | One function per domain. Each enumerates every producer of its kind from the world itself. A domain raises when its world is missing; it never returns an empty list. |
| `verdicts.json` | The register. Each entry: `key` glob, optional `kind` glob, `verdict`, and either `reader` (COLLECTED), `why` (EXCLUDED) or `ticket` (a gap). First match wins. `blind_allowed` names domains allowed to be BLIND, each with a ticket. |
| `datamap.py` | Grades every producer against the register and prints the map. `--check` exits 1 on one UNEXPLAINED producer, one gap without a ticket, one BLIND domain not allowed, or one domain that shrank by more than half against `census.json`. |

**Run it.**

```
python3 science/datamap.py --check                 # the full gate, about a minute
python3 science/datamap.py --check --domains act   # one domain, seconds
python3 science/datamap.py --check --file-tickets  # open a crew ticket per unticketed gap entry
python3 science/datamap.py --json                  # machine-readable, used by estate-snapshot
```

**When the gate goes red.**

1. `UNEXPLAINED` rows: a producer appeared that no entry matches. Add an entry to
   `verdicts.json`. COLLECTED needs `reader`; EXCLUDED needs `why`; a gap needs `ticket`
   (run `--file-tickets` to open it).
2. `BLIND`: a domain cannot read its world. Fix the world, or add the domain to
   `blind_allowed` with the ticket that restores sight. Never catch the exception inside the
   domain.
3. `SHAPE CHANGED`: a domain returned less than half of what `census.json` recorded. Either
   the world shrank (commit the new census) or the discoverer broke (fix it).

**When you add a new kind of world** (a scheduler, a store, a cloud account, a listener class):
add a domain function to `producers.py` and register it in `DOMAINS` in the same PR. This is
the one residual the gate cannot see for you; LAW 50 rule 4 binds the PR.

**Where it is enforced.** `scripts/verify.d/26-datamap-register.sh` in CI;
`scripts/estate-snapshot` writes the `data map` row into `STATE.md` hourly. Incident tests:
`tests/test_incident_datamap_was_a_hand_typed_list.py`. Law text: `~/AGENTS.md`, LAW 50.
