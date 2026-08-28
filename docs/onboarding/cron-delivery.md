# cron-delivery

## What it is for

To answer, with a measurement rather than a belief, whether GitHub is running the estate's
scheduled workflows. A cron that never fires produces **no failure — only silence**, and a cron
that fires eleven hours late still reports success. Every `max_age_hours` bar in
`drills/catalogue.yaml`, and every "runs nightly" sentence in our docs, assumes a delivery rate
nobody had ever measured.

It answers three questions in one pass:

| | |
|---|---|
| **share** | of the occurrences the crons were due, how many became runs |
| **lateness** | of the runs that did arrive, how far past their due minute |
| **heartbeat** | for named workflows, how many of the last N hours had a *clock* run (a `schedule`, or a `workflow_dispatch` by a bot) rather than only somebody's push |

`--per-workflow` adds one row per scheduled workflow plus a banding by how often the cron asks.
Use it whenever the question is *why* a share is low; the repo aggregate cannot tell a
per-repository cap from a per-workflow ration, because it averages a `*/5` cron with a daily one.

## Where it lives

`scripts/cron-delivery` in the crew repo. One file, standard library plus `gh`. Nothing is
hardcoded to an account (LAW 46): the owner comes from the authenticated `gh` login unless
`--owner` overrides it, and the repositories are discovered, not listed.

## How to run it

```
scripts/cron-delivery                                   # every repo the owner has
scripts/cron-delivery --repos idp,crew --per-workflow   # two repos, per-workflow rows
scripts/cron-delivery --hours 168                       # a week instead of a day
scripts/cron-delivery --heartbeat idp:login-drill.yml   # clock runs per hour for one workflow
```

Exit `0` means the measurement ran. Exit `2` means it came back **unsound** — a `gh` call was
refused, or the run list hit its cap — so a caller can tell "the estate is healthy" apart from
"we did not look". That distinction is the failure this file exists to end; treat a `2` as a
missing measurement, never as a passing one.

## What it costs

Read-only GitHub API calls: one workflow listing and one paginated run listing per repository.
The three-repo run above took about 40 seconds. It writes nothing, changes nothing, and needs no
cluster, no OCI session and no secret beyond the `gh` token already on the machine. Running it
against every repo the owner has is a few minutes and is safe to do at any time.

## How to stop it

Nothing to stop. It is a script you run, not a service — no daemon, no launchd job, no workflow
firing it on a schedule. Delete the file and nothing else changes.

## What it found

2026-08-28: GitHub delivers each scheduled workflow **0.71–2.11 runs a day regardless of what its
cron asks for**. Share collapses from 100% (daily crons) to 1% (`*/5`); runs per workflow stay
flat. It is a ration, not a share, and it is not a per-repository cap — the one-cron repo does no
better than the eleven-cron one. Lateness, n=62: median 12m, p90 680m, max 701m.

The consequence for anything you build here: **a cron finer than hourly is not a heartbeat.**
Put it on a CronJob in the cluster. And no `max_age_hours` under roughly 12 is a bar our own
GitHub schedules can clear.

Demo with real output: `docs/demo/cron-delivery.md`. Incident and full measurement: crew#554.
