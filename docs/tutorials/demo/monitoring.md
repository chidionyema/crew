# Demo — the dead-man that is not on the Mac (crew#163)

## The ninety-second version

1. `~/.claude/scripts/hc-wrap.sh estate-snapshot true` — one ping from this Mac.
2. Open `https://hc.<zone>/` — the check `estate-snapshot` shows the ping, its schedule
   and when it is next expected.
3. Stop the scheduler (`launchctl bootout gui/$(id -u)/ai.estate.scheduler`) and the check
   goes down after the grace period; the alert leaves the cluster, not the Mac. Start it
   again (`launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.estate.scheduler.plist`)
   and the next ping clears it.

## Options considered

- A GitHub Actions schedule reading STATE.md commit ages (`deadman.yml`, the first cut of
  this PR): a second dead-man with a second threshold, e-mail-only alerting, and a schedule
  GitHub switches off after 60 idle days. Rejected, LAW 43.
- A cron on a rented box curling the repository: same duplication, plus a host to keep alive.
- Chosen: the Healthchecks receiver the estate already runs on OKE, with the snapshot job
  already wrapped in `hc-wrap.sh`. The only work is enrolling each Mac once
  (`idp-hc-enroll`) and deleting the duplicate.

## What a buyer's engineer sees

One receiver, in the platform repo, with a Terraform-generated key; the Mac holds two files
it did not type. No script of ours parses git dates to decide whether a machine is alive.
