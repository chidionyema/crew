# Demo — `science/dora.py`

crew#495 CP9. The founder asked, 2026-08-27, how the estate gets to NASA/military grade at zero
spend, then "platformops". The four DORA keys are the ops grade everyone else uses, so they are
measured from GitHub on demand, never quoted from memory (THE FOUR HARD RULES, rule 2).

```
$ python3 science/dora.py
```

Real output, captured 2026-08-27T11:27Z from the command above:

```
DORA, last 7 days to 2026-08-27T11:27Z, from the GitHub API (merges to main; P1 by label)
chidionyema/idp: deploys=334 (47.71/day) | lead time median=0.14h p90=1.23h | change failure rate=0.3% (P1 opened=1) | MTTR median=n/a (P1 closed=0)
chidionyema/crew: deploys=137 (19.57/day) | lead time median=0.2h p90=1.19h | change failure rate=29.2% (P1 opened=40) | MTTR median=3.5h (P1 closed=17)
```

Deploy frequency is pull requests merged to main per day. Lead time is PR created to merged.
Change failure rate is issues labelled P1 opened in the window over merges in the window. MTTR
is P1 created to closed. Every page of the listing is read, so a count is a count; the first
baseline on crew#495 stopped at a 200-row page cap and this does not.
