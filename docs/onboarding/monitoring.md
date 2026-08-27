# Onboarding — the dead-man that is not on the Mac

Tracked item: crew#163. Standard row: Job monitoring (`docs/STANDARDS.md`).

## What this is for

Every monitor this estate had ran on the Mac it was monitoring. When the Mac stopped, the
jobs stopped, and so did the thing that would have said so. On 2026-08-24 the local
Healthchecks container exited 137 and stayed down for hours; 12 of 40 wrapped jobs pinged
it into nothing and every one of them reported success.

The receiver now lives on the cluster, outside the Mac's failure domain: Healthchecks on
OKE at `https://hc.<zone>` (idp `platform/healthchecks/healthchecks.yaml`). The Mac only
pings it. When the pings stop, the receiver — not the Mac — raises the alert.

## What it watches

One heartbeat, not 46 jobs. `com.founder.estatesnapshot` (idp `scheduler/schedule.yml`)
runs every two hours and commits STATE.md to crew main; it is already wrapped:

    ~/.claude/scripts/hc-wrap.sh estate-snapshot <checkout>/scripts/estate-snapshot --commit

`hc-wrap.sh` pings `<base>/<ping-key>/estate-snapshot/start?create=1` before the run and
`<base>/<ping-key>/estate-snapshot` (or `/fail`) after it. `create=1` makes the check the
first time it is pinged, so nothing is clicked in a UI. A Mac that goes quiet misses the
next ping and the check goes down; per-job detail from inside a dead machine is not worth
having, so the other wrapped jobs are detail, this one is the dead-man.

## Enrol a Mac, once

The receiver's address and the project's ping key are two files under
`~/.estate/healthchecks/` (`base`, `ping_key`). `idp-hc-enroll` writes them from the vault
entry the server enrols itself with, so the Mac and the server never disagree and nobody
copies a key from a screen:

    ~/dev/code/idp/bin/idp-hc-enroll
    # ok      hc-enroll  base=https://hc.<zone>/ping ping_key=<8 chars>... (33 bytes)

It reads the vault through `idp-cloud`, which needs a live OCI session on this Mac. When
it prints `BLIND   hc-enroll` the session has expired; that is the one hand a person gives
(identity, crew#325 register row): `oci session authenticate --profile-name otto --region
uk-london-1`, then run enrol again. Nothing else waits on a person.

A Mac that is not enrolled falls back to the local container address, which is the
failure this closes — so `idp-hc-enroll` is the onboarding, not an optional step.

## Where it lives

- Receiver: idp `platform/healthchecks/healthchecks.yaml` (OKE), keys from
  `platform/oci/healthchecks.tf` via the vault.
- Wrapper: `~/.claude/scripts/hc-wrap.sh` (claude-guards), documented in
  `~/.claude/scripts/docs/onboarding/healthchecks.md`.
- Schedule: idp `scheduler/schedule.yml`, entry `com.founder.estatesnapshot`.
- Guard: `tests/test_incident_crew163_deadman_is_healthchecks_not_a_workflow.py` fails if
  anyone adds a second, hand-rolled dead-man to this repository.

## Why not a GitHub Actions dead-man

The first cut of this item was `.github/workflows/deadman.yml` reading STATE.md commit
ages on a schedule. It was a second dead-man with its own threshold, alerting only by
GitHub's failure e-mail, and GitHub disables a schedule after 60 days without commits.
Healthchecks already answers all of that (grace periods, escalation through Apprise,
a status page, an API) and is already deployed. LAW 43: never reinvent the wheel and do a
worse job. The rejected option is recorded in `docs/demo/monitoring.md`.

## How to prove it yourself

    ~/.claude/scripts/hc-wrap.sh estate-snapshot true
    # then open https://hc.<zone>/ — the estate-snapshot check shows a fresh ping

## What it still cannot see

A Mac that is alive but whose scheduler is stopped looks identical to a dead Mac: both go
quiet. That is correct — the question the dead-man answers is "is the snapshot landing",
and in both cases it is not.
