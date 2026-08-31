---
captured: 2026-08-31T04:04:21+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/hermes-v2
chars: 2310
source: founder prompt, verbatim (founder-doc-capture.py)
---

Yes — and this is the answer to your actual question, not the incident.

A rolling update interrupts you because Kubernetes' definition of "ready" and yours have diverged. Kubernetes rolls the new pod in, sees the readiness probe pass, and deletes the old one. If the container reports ready at 03:44:45 but doesn't hold a Telegram connection until minutes later, then the API server thinks the handover succeeded while the thing you actually depend on is dark. The gap isn't a rollout flaw. It's the probe lying.

That's the class, and it's the same one as everything else tonight: an invariant that exists in your head — "ready means answering Telegram" — enforced nowhere.

For this pod, three things fix it and only the first one is really a fix:

Make readiness mean what you mean. The readiness probe must fail until the Telegram connection is established. Then the old pod stays alive through the new one's four-minute boot, and the rollout genuinely has no gap. That's a probe change in the container, not a Kubernetes setting.

Then maxUnavailable: 0 with maxSurge: 1 on the Deployment strategy, so the old pod is only deleted after the new one is truly ready. Without the probe fix this changes nothing, because "ready" is already wrong.

But a single-holder token means both pods can't poll at once — and that's a real constraint that surge-before-delete will collide with. Two pods, one token: the new one either fails to connect or steals the session. So the honest answer is that zero downtime isn't reachable by rollout strategy alone here; it needs the app to hand off, or the boot to shrink, or you accept a short gap. Worth knowing before you spend the night chasing a config that can't deliver it.

The four-minute boot is the other lever, and probably the cheaper one. Something before the DNS-over-HTTPS discovery is eating that time — shrinking it shrinks the gap regardless of everything above.

Evolution lane: one-character JSON fault in cron/evolution.jobs:5, failing every boot. Fix the file, and put a JSON schema check in the pre-commit or CI gate — that's a rung-2 control for a file class that will otherwise break again silently. It's an unrelated bug that happened to surface in the same log; don't let it get bundled into the rollout fix.

You’ve used 75% of your weekly limit
