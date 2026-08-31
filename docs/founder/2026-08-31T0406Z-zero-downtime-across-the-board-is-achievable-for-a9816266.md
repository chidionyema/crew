---
captured: 2026-08-31T04:06:08+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/hermes-v2
chars: 2475
source: founder prompt, verbatim (founder-doc-capture.py)
---

Zero downtime across the board is achievable for most of your estate. It is not achievable for the Telegram gateway as currently designed, and no amount of Kubernetes configuration will make it so. Worth being precise about why, because the boundary is the useful part.

Where zero downtime is a config problem — solvable, do it estate-wide:

Any stateless service, anything behind a Service with multiple endpoints, anything that can run two replicas at once. maxUnavailable: 0, maxSurge: 1, honest readiness probes, PDBs, preStop sleep to drain connections. That's a policy you apply once across the estate and it holds. Most of what you run falls here. This is a genuine "all green, stays green" target and you should enforce it as admission policy: reject any Deployment with Recreate unless it carries an explicit opt-out.

Where it's an architecture problem — the gateway:

One Telegram token admits one poller. That's an upstream constraint, not yours. Two pods means one gets 409s. So Recreate isn't a mistake someone made — it's the only correct strategy given the constraint, and swapping it for RollingUpdate would trade a clean gap for a broken overlap.

Zero downtime here requires one of:

Webhook instead of long-polling. Telegram pushes to an endpoint behind a Service; the endpoint is stateless, so N replicas, rolling updates, no gap. This is the actual answer, and it's the only one that gets you true zero.
Two tokens, two bots, one draining while the other takes over. Ugly, visible to users.
A leader-election handoff where the new pod signals readiness and the old releases the poll loop before exiting. Real engineering, and still a sub-second gap.

Webhook is the one. It converts the gateway from a special case into an ordinary stateless service that your estate-wide policy covers, which is exactly the shape you keep asking for — eliminate the exception rather than manage it.

Until then, the four-minute boot is your outage. Not the rollout. A Recreate on a service that boots in three seconds is a three-second gap nobody notices. Same strategy, same token constraint, 98% less downtime — and it's the cheapest thing on this list.

So the honest answer: yes to zero downtime across the board, as a target, enforced by policy. The gateway needs a design change to join that set, and shrinking the boot is what makes it tolerable in the meantime.

Merge #1030 first. Tailscale and Guacamole have been down for hours and that PR is sitting there.
