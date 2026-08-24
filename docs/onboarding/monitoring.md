# Onboarding — the dead-man that is not on the Mac

Owner: the platform lane
Last true: 2026-08-24

## What this is for

Every monitor in this estate runs on the machine it monitors. When the Mac stops, the jobs
stop, and so does the thing that would have told you.

That is not hypothetical. Measured on 2026-08-24:

```
$ docker inspect estate-healthchecks --format '{{.State.ExitCode}} {{.State.FinishedAt}}'
137 2026-08-24T11:14:35Z
```

The Healthchecks receiver — the thing whose whole job is to notice silence — was itself
silent for hours and nothing said so. Jobs wrapped in `hc-wrap.sh` went on pinging an
address that answers HTTP 000, and each one reported success, because a ping that fails to
send is not a job that failed.

You cannot fix that from inside the Mac. Whatever watches has to be somewhere else.

## What it actually watches

One heartbeat, not forty-six jobs.

`com.founder.estatesnapshot` has `StartInterval 3600` and commits `STATE.md` to `main`
every hour. That commit landing on GitHub is proof the Mac is alive, is running launchd
jobs, and can still reach the network. If it stops, everything below it is unmonitored
too.

Per-job monitoring stays with the local Healthchecks receiver. That is the right place for
it. Per-job detail from inside a dead machine is not worth having, and the first fact you
need is not "job 31 is late", it is "the machine is gone".

## Why the threshold is 180 minutes and not 90

The hourly snapshot is not reliably hourly. Over the 30 hours to 2026-08-24 12:45 it missed
four runs:

```
  01:48  +96m
  03:29  +100m
  07:29  +144m
  10:20  +170m
```

A dead-man set tight enough to catch those would fire several times a day on an estate that
is merely flaky, and would be muted inside a week. A muted alert is worse than no alert,
because it looks like coverage. So the gate fires only on sustained silence, and the
missed-run count is printed on every single run without gating anything.

The late snapshots are a real defect. They belong to whoever owns
`com.founder.estatesnapshot`, and this check exists partly to keep printing the number until
someone does.

## What it costs

Nothing. No account, no secret, no webhook, no service to keep alive. It is a GitHub Actions
workflow on a repository the estate already pushes to hourly, running two shell commands
twice an hour. This satisfies R14: free tier only, no paid infrastructure.

It was chosen over healthchecks.io hosted for exactly that reason — the hosted free tier
caps at 20 checks and requires an account, and neither the account nor the cap was needed to
answer the question "is the Mac alive".

## Where it lives

```
.github/workflows/deadman.yml   the schedule, 7 and 37 past the hour
scripts/deadman-check.sh        the check, runnable by hand anywhere
```

The check is a plain shell script with no GitHub in it, so it runs identically on your
laptop, in CI, or on any box you later move it to. That is deliberate (LAW 19: portability
outranks detection). Moving it off GitHub Actions is a scheduler change, not a rewrite.

## How to run it yourself

```
$ ./scripts/deadman-check.sh
```

Two environment variables, both for testing:

| Variable | Does |
|---|---|
| `DEADMAN_MAX_MINUTES` | silence past this is a failure. Default 180. |
| `DEADMAN_AGE_MINUTES` | pretend the heartbeat is this old instead of reading git. |

## How to stop it

Disable the `deadman` workflow in the repository's Actions tab, or delete
`.github/workflows/deadman.yml`. Nothing else in the estate depends on it, and stopping it
breaks nothing — it only stops the reporting.

## What it still cannot see

Three things, stated here rather than discovered during an outage.

1. **GitHub queues scheduled runs at best effort.** They are commonly minutes late under
   load. The 180-minute threshold absorbs that. It is not a precise clock and must not be
   used as one.
2. **GitHub disables a schedule after 60 days without commits.** So a genuinely abandoned
   estate goes quiet rather than loud. This is the one residual that matters and it is not
   closed. Anything that commits to the repository on any cadence keeps it alive, which the
   hourly snapshot currently does — but that is the same heartbeat being watched, so the two
   are not independent.
3. **It watches the heartbeat, not the jobs.** A Mac that is up and running launchd while
   every individual job fails will read ALIVE here, correctly. That is the local receiver's
   question, and it is a different question.
