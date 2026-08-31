---
captured: 2026-08-26T23:20:19+00:00
session: c62c545a-5643-4b98-8936-1b0f68347cbd
cwd: /Users/chidionyema/dev/code/crew/.worktrees/agent-go-345
chars: 2055
source: founder prompt, verbatim (founder-doc-capture.py)
---

Issue #345 on chidionyema/crew: Platform-level: OCI session expires every ~1-2h, blocking all live verification — durable identity, not repeated founder logins

**Founder, 2026-08-26: 'think bigger now.' Real pattern across tonight, not a one-off.**

Counted: OCI session-token auth (`estate-bootstrap`/`otto` profiles) expired and required a fresh founder browser login at least 5 separate times tonight, each time stopping live cluster verification cold (crew#286 CP2/CP3, crew#308, CP4/SPIFFE audit, this exchange). Session lifetime is short (observed: valid ~50min from a 20:00 login, expired by 21:08).

**This is a platform durability problem, not friction to route around per-incident.** A platform whose own maintainers/agents cannot check its health without an hourly human re-login is not durable -- it fails the R35 'tear down and rebuild with confidence' standard (crew#250) by making 'confidence' contingent on the founder being awake and present.

**Real, structural fix, not yet chosen:** crew#227 CP3's own direction (instance-principal / workload identity, zero static keys) already solves this for machine identities -- the same durable pattern should extend to whatever performs live verification (agent sessions), not leave them on short-lived interactive session tokens as the only path. Needs real design: possibly a scoped, longer-lived service identity for read-only verification specifically, separate from the founder's own identity, least-privilege.

## Acceptance criteria
- [ ] Root-cause the actual session TTL (confirm whether ~50min is OCI's default or a local config choice)
- [ ] Decide and build the durable verification-identity path (scoped service principal, not founder session reuse)
- [ ] Prove it: a real cluster health check runs successfully with zero founder interaction for a stated period (e.g. 24h), not just immediately after a fresh login

You are in an isolated git worktree on branch agent-go/345. Do the work here, commit, and open a pull request naming chidionyema/crew#345. Never merge, never deploy.
