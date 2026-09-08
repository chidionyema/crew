# Thirteen research loops expired on the same day and took every pull request with them

**When.** From 2026-09-07 every open pull request in this repository was red. Eleven were open
on 2026-09-08 and none of them contained the defect.

**What broke.** `scripts/verify.d/80-research-ledger.sh` fails when an entry in
`science/RESEARCH-LEDGER.jsonl` is more than fourteen days old and still carries
`metric_after: null`. Thirteen entries were written on 23 and 24 August in one sitting, so their
fourteen-day windows expired in one day. The drill runs inside the `qa` job on every pull
request, so a check that had been quiet for a fortnight became a blocker on every branch at
once, including branches that change only documentation.

**Why it went unnoticed.** The drill had exactly two states, silent and blocking, with nothing
in between. Nobody was told a measurement was due until the day it was late, and by then the
cost had already been paid on every open branch. Each session saw only its own red tick and
chased its own pull request; the shared cause was invisible from any one of them. That is the
shape LAW 38 names — a guard that refuses correct work is an outage — arriving through a guard
that was correct about the ledger and wrong about when to say so.

**The fix.** Two halves, and the second is the one that matters.

The thirteen loops are closed. Seven carry a real measurement, and three of those seven closed
red: the agent truth gate was decided in August and never wired, so its ledger still returns
zero events. Six are marked `abandoned` with the reason, because their baselines were hand
counts with no script, or artefacts that no longer exist in the shape they were counted in. No
number was invented for any of them.

The drill now warns from day seven, naming each entry and how many days are left, and keeps
passing. On its first run it named line 31 with three days to go — the entry that would have
stopped the fleet again on the Thursday.

`science/schemas/research_ledger.json` gained the `abandoned` field in the same pass. The drill
had accepted that marker since it was written, but the contract never listed it, so
`tests/test_incident_crew90_research_ledger_rows_match_contract.py` refused any row that used
it. The escape hatch existed and no row could reach it.

**The class of mistake, so it is not repeated.** A deadline gate needs a warning window, and the
window has to be longer than the work it is asking for. A gate whose only two states are silent
and blocking converts every miss into an outage, and converts a batch of entries written on one
day into a batch of failures on one day. The rule now: any check that fires on an age threshold
warns at half the threshold, by name, with the time remaining.

**Verify.**

```
$ bash scripts/verify.d/80-research-ledger.sh
WARN: 1 entry expiring
  line 31 (2026-08-28: ...) — 3 days left
PASS: 32 entries, newest 2026-09-05, 0 unmeasured past 14 days
```
