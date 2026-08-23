# Demo — science/collect.py

What it does: reads all sixteen of the estate's data stores and lands them in one
table you can query with one line of SQL. Before this, every cross-store question
needed its own throwaway script. Two were written in a single session on
2026-08-23, which is what prompted the build.

## The run

    $ cd ~/dev/code/crew && python3 science/collect.py

    warehouse: /Users/chidionyema/dev/code/crew/science/warehouse.db
    source                rows  bad  age
    --------------------------------------------------------
    stuck_detector        1775    0  fresh 0h
    spend                  920    0  fresh 0h
    close_guard            846    0  fresh 0h
    toolguard              435    0  fresh 5h
    ledger                 407    0  fresh 0h
    would_have_fired       162    0  STALE 48h
    decisions              118    0  STALE 53h
    bundle_push             95    0  fresh 0h
    consult                 78    0  fresh 6h
    ci_reach                54    0  fresh 3h
    aiden_ticks             54    0  fresh 0h
    drills                  28    0  fresh 0h
    board                   15    0  fresh 0h
    agent_cert              10    0  fresh 4h
    method_metrics           1    0  fresh 0h
    enforcement_map          1    0  fresh 3h
    --------------------------------------------------------
    TOTAL                 4999       across 16 sources
    spend_daily view:  17 days, $13647.78 total

    needs attention:
      - would_have_fired: STALE 48h
      - decisions: STALE 53h

Read the last two lines. Those are two collectors that stopped writing two days
ago and nothing anywhere had noticed. Finding them cost nothing extra — the same
pass that copies a store also reports how long since anyone wrote to it.

## What it just made answerable

The money question, which previously needed a bespoke script every time:

    $ sqlite3 -header -column science/warehouse.db \
        "select day, usd, requests, round(usd/nullif(requests,0),3) as usd_per_req
           from spend_daily order by day desc limit 8;"

    day         usd        requests  usd_per_req
    ----------  ---------  --------  -----------
    2026-08-23  587.2699   5518      0.106
    2026-08-22  535.3315   4938      0.108
    2026-08-21  1201.0313  9804      0.123
    2026-08-20  1132.7999  9395      0.121
    2026-08-19  863.5911   8418      0.103
    2026-08-18  870.0964   9092      0.096
    2026-08-17  785.7976   8237      0.095
    2026-08-16  787.44     7926      0.099

    $ sqlite3 science/warehouse.db \
        "select round(avg(usd),0) from (select usd from spend_daily order by day desc limit 7);"
    854.0

## What that number did on its first run

$854/day is the seven-day mean. Open P1 issue #26 says the estate spends
$431/day. The instrument disagreed with a live P1 the first time it ran, and the
disagreement is the finding (LAW 15). The row now sits in STATE.md, directly
above the issue that contradicts it:

    | estate spend | RED | $854/day 7-day mean against a $120 cap (`spend_daily`, warehouse.db) |
    | crew P1 | 5 open | the fires nobody has put out |
    |   #26 Estate spend is $431/day against a $120 cap and the only brake reaches 0.03% of it | | |
