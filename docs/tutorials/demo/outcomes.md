# Demo — science/outcomes.py

Every instrument on this estate points inward: guards, laws, complaints, tokens.
Not one recorded an outcome, so the estate could say it spent $854 yesterday and
could not say what that bought. This collects the other half.

## Delivery

    $ cd ~/dev/code/crew && python3 science/outcomes.py ship --days 14

    /Users/chidionyema/dev/code/crew/science/ships.jsonl
    day           commits  PRs merged
    ----------------------------------
    2026-08-23        157          10
    2026-08-22        155           9
    2026-08-21        325           0
    2026-08-20        186           0
    2026-08-19        218           0
    2026-08-18         43           0
    2026-08-17         56           0
    2026-08-16         61           0
    2026-08-15         60           0
    2026-08-14         40           0
    2026-08-13         22           0
    2026-08-10         17           0
    ----------------------------------
    TOTAL            1340          19

## Joined to spend — the first cost-per-outcome the estate has had

    $ python3 science/collect.py >/dev/null
    $ sqlite3 -header -column science/warehouse.db \
        "select * from value_daily order by day desc limit 10;"

    day         usd        commits  prs_merged  usd_per_commit
    ----------  ---------  -------  ----------  --------------
    2026-08-23  676.8261   157      10          4.31
    2026-08-22  535.3315   155      9           3.45
    2026-08-21  1201.0313  325      0           3.7
    2026-08-20  1132.7999  186      0           6.09
    2026-08-19  863.5911   218      0           3.96
    2026-08-18  870.0964   43       0           20.23
    2026-08-17  785.7976   56       0           14.03
    2026-08-16  787.44     61       0           12.91
    2026-08-15  960.0449   60       0           16.0
    2026-08-14  836.2072   40       0           20.91

Read the right-hand column top to bottom. Cost per commit fell from about $20 in
the week of 14–18 August to about $4 across 19–23 August, while daily spend stayed
in the same band. The estate did not get cheaper; it got more productive per
dollar, by roughly 5x, and nobody knew because nothing divided the two numbers.

That column is a crude denominator and the code says so. A commit is not value,
and the cheapest way to improve the number is to commit more often. It is an upper
bound on cost, never a measure of merit. It is also the first denominator of any
kind this estate has ever had, and having one makes the question askable.

## Predictions — starting a ledger that has been empty for weeks

`method_metrics.json` has carried `predictions: []` since it was built, so the
estate had never once predicted a cause and then checked itself.

    $ python3 science/outcomes.py predict --issue 60 \
        --step "the guard that WROTE would-have-fired.jsonl was deleted or renamed, not
                merely left in observe mode" \
        --because "no file anywhere on this machine writes that path -- every hit is a
                   reader (law_enforcement.py, PLAN.md, FINDINGS-01)."

    prediction #1 recorded, unscored

Scoring is a separate command on purpose, so a prediction cannot be edited to fit
the result after the fact:

    $ python3 science/outcomes.py rate

    predictions logged: 1
    scored:             0
    hit rate:           unmeasurable, n = 0

n = 0 is the honest reading and it is the same one `method_metrics.json` has given
for weeks. It changes the first time a repair predicts its cause before making it.

## What it cost the founder

Added 2026-08-24. The estate measured its own money and its own output and had never once
measured the person it is for. `friction-relay.py` surfaced his complaints in a six hour
window and kept nothing, so nobody could ask whether last week was better than this one.

```
$ python3 science/outcomes.py attention --days 6
/Users/chidionyema/dev/code/crew/science/attention.jsonl
day           his messages  complaints   rate
---------------------------------------------
2026-08-17             767         100    13%
2026-08-18             786          69     9%
2026-08-19             622          26     4%
2026-08-20             735          29     4%
2026-08-21             951          53     6%
2026-08-23             306          19     6%
---------------------------------------------
TOTAL                 6917         530     8%

23 days, 2026-07-28 to 2026-08-23, lexicon 43 words
```

Joined to spend and delivery, the series says something no other row on the estate could:

```
$ sqlite3 -header -column science/warehouse.db "select * from attention_daily order by day desc limit 4;"
day         messages  complaints  complaint_rate  usd        commits  commits_per_message
----------  --------  ----------  --------------  ---------  -------  -------------------
2026-08-23  307       19          6.2             676.8261   159      0.52
2026-08-21  951       53          5.6             1201.0313  325      0.34
2026-08-18  786       69          8.8             870.0964   43       0.05
2026-08-17  767       100         13.0            785.7976   56       0.07
```

On 17 August his complaint rate was 13% and each message he sent bought 0.07 commits. On
23 August the rate was 6.2% and each message bought 0.52. That is a sevenfold change in
what his words are worth, and until this view existed neither number had ever been taken.

He reads it on `STATE.md` as the `founder cost` row, this week against last. He never runs
the command.
