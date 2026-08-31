---
captured: 2026-08-31T00:17:25+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/.wt-backups
chars: 2004
source: founder prompt, verbatim (founder-doc-capture.py)
---

Fine. One thing, once, done.

One Kyverno mutating policy on Pod. Every image gets rewritten to <your-OCI-registry>/<path>@sha256:<digest>. Registry and digest in the same rule. Not two phases.

Why that's the actual root and not another layer: every pod in the cluster passes through admission, whether you wrote it, a chart wrote it, or an operator generated it at runtime. It's the last point where all inputs are merged. Nothing gets past it. And the output has no unresolved parts left — a digest on your own registry doesn't depend on Docker Hub being up, doesn't depend on a resolver default, doesn't depend on a tag still meaning what it meant last week. All three failure modes gone in one object.

Two things have to exist for it or the rule is a lie:

Pull-through cache on your OCI registry, so the rewritten reference actually resolves. Without it you've pointed every pod at an image that isn't there and broken the cluster harder than it is now.
Digest bumps automated (Renovate or Flux image automation), or you're frozen on today's bytes forever and quietly stockpiling CVEs.

Neither is optional and neither is later. They're part of the one change.

What gets deleted in the same PR: the twelve-file image rewrite, the render-time guard, and the file-reading guard. All three are superseded. Leaving them is how you end up with a green check that means nothing.

Then the proof, before it merges: apply the policy to a Pod with tailscale/k8s-operator:v1.102.3 and show the admission response containing your registry and a digest. Watched failing against the pre-fix input, or it isn't known to work.

One caveat I'm not going to drop, because it decides whether this fixes today's outage or just makes future ones impossible: read the actual event off the failing operator pod first. Thirty seconds. If it says toomanyrequests, the cache is what unblocks you and the policy is what stops it recurring — same build either way, but you'll know which part is load-bearing when you merge.
