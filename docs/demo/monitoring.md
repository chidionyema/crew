# Demo — the dead-man that is not on the Mac

Owner: the platform lane
Last true: 2026-08-24

Every block below is real output, captured on 2026-08-24 by running the command above it.

## The normal case: the Mac is alive

```
$ ./scripts/deadman-check.sh
heartbeat: STATE.md last changed 2026-08-24 11:45 UTC
heartbeat age: 15m
threshold: 180m of silence

last 30h: 19 heartbeats, 4 gap(s) over 90m, worst 170m   (reported, not gating)

ALIVE: last heartbeat 15m ago, inside the 180m threshold.
$ echo $?
0
```

The middle line gates nothing. It is there because the hourly snapshot missed four runs
in the last 30 hours and a number nobody prints is a number nobody fixes.

## The case it exists for: the Mac has gone silent

There is no way to make the real Mac disappear for a demo, so the age is forced. Everything
downstream of the age is the real code path.

```
$ DEADMAN_AGE_MINUTES=999 ./scripts/deadman-check.sh
heartbeat age: 999m (forced by DEADMAN_AGE_MINUTES, not measured)
threshold: 180m of silence

DEAD: the Mac has been silent for 999m, past the 180m threshold.
      Every job on it is unmonitored right now, including the monitors.
$ echo $?
1
```

## The boundary, both sides

```
$ DEADMAN_AGE_MINUTES=179 ./scripts/deadman-check.sh | tail -1
ALIVE: last heartbeat 179m ago, inside the 180m threshold.
  exit 0
$ DEADMAN_AGE_MINUTES=180 ./scripts/deadman-check.sh | tail -1
ALIVE: last heartbeat 180m ago, inside the 180m threshold.
  exit 0
$ DEADMAN_AGE_MINUTES=181 ./scripts/deadman-check.sh | tail -1
      Every job on it is unmonitored right now, including the monitors.
  exit 1
```

## What GitHub runs

The workflow proves the refuse direction before it trusts the permit direction, on every
run. A dead-man only ever seen passing has never been shown to be able to fail.

```
$ DEADMAN_AGE_MINUTES=999 ./scripts/deadman-check.sh && echo 'not a dead-man' || echo 'refuses as it should.'
refuses as it should.
```

## What a real failure looks like to you

The `deadman` workflow goes red and GitHub mails the repository owner. There is no other
channel, no secret and no service to keep alive. The body of the failing step is the DEAD
block above.
