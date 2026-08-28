# Demo: does GitHub actually run our crons?

One command. No setup, no cluster, no secrets — it uses the `gh` login already on the machine.

```
scripts/cron-delivery --repos idp,crew,maestro --per-workflow
```

Real output, 2026-08-28T15:18Z:

```
# window: the 24h to 2026-08-28T15:18:00Z, owner chidionyema

repo                               sched wf        due  delivered    share
chidionyema/idp                         11        535         16       3%
chidionyema/crew                         6        171          7       4%
chidionyema/maestro                      1        144          3       2%

# lateness of the runs that DID arrive, n=26
#   median 9m   p90 675m   max 683m
#   on time (<=5m) 6   late >30m 8   late >2h 6
#   a bar of max_age_hours=N is safe only while N exceeds 11.2h

repo                     workflow                     cron                     due  got  share
idp                      ping.yml                     */5 * * * *              288    1     0%
crew                     merge-when-green.yml         */10 * * * *             144    2     1%
maestro                  merge-when-green.yml         */10 * * * *             144    3     2%
idp                      drill-heartbeat.yml          3-59/15 * * * *           97    2     2%
idp                      wake-blocked.yml             7-59/30 * * * *           48    2     4%
idp                      login-drill.yml              7 * * * *                 24    2     8%
idp                      stale.yml                    17 * * * *                24    2     8%
idp                      trace-drill.yml              23 * * * *                24    2     8%
idp                      verify-drill.yml             23 * * * *                24    2     8%
crew                     stale.yml                    17 * * * *                24    2     8%
idp                      catalog-render.yml           58 1,7,13,19 * * *         4    1    25%
idp                      kyverno-secrets-drill.yml    41 7 * * *                 1    1   100%
idp                      oke-check.yml                17 6 * * *                 1    1   100%
crew                     ci-runs.yml                  41 5 * * *                 1    1   100%
crew                     datamap-tickets.yml          17 6 * * *                 1    1   100%
crew                     revenue.yml                  17 5 * * *                 1    1   100%
idp                      portability-drill.yml        23 5 * * 1                 0    0    n/a
crew                     self-grade.yml               0 6 * * 1                  0    0    n/a

how often the cron asks       wfs    due   got  share  got per wf
asks >48/day (<=30m apart)      4    673     8     1%        2.00
asks 12-48/day                  6    168    12     7%        2.00
asks 2-11/day                   1      4     1    25%        1.00
asks <=1/day                    7      5     5   100%        0.71
```

## What to look at

The last block is the finding, and it is the reason `--per-workflow` exists. Read the two
right-hand columns against each other:

- **`share` collapses** from 100% to 1% as the cron asks more often.
- **`got per wf` does not move.** 0.71, 1.00, 2.00, 2.00 — every scheduled workflow gets between
  half a run and two runs a day, whatever its cron says.

GitHub hands each workflow a **ration, not a share**. `idp/ping.yml` asks 288 times a day and
receives 1. `crew/revenue.yml` asks once and receives it.

The repo table above cannot show you this. `maestro` has one cron and delivers 2%; `idp` has
eleven and delivers 3%. Read on its own that looks like a per-repository cap, and it is not — the
aggregate is averaging a `*/5` cron with a daily one. That is why the per-workflow rows are here.

## What it means for the estate

Any `max_age_hours` under about 12 is a bar our own schedules cannot clear (p90 lateness 675m).
A cron finer than hourly is not a heartbeat — it is a lottery ticket. If something must happen
every five minutes, it belongs in the cluster on a CronJob, not in GitHub Actions.

## Try the smallest version

```
scripts/cron-delivery --repos crew --hours 24 --per-workflow
```

Under a minute, one repo, same shape.
