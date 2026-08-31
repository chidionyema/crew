---
captured: 2026-08-31T05:05:14+00:00
session: a7b41022-3074-43c7-bb13-a1d7e07adff1
cwd: /Users/chidionyema/dev/code/.wt-secrets-rotation
chars: 1898
source: founder prompt, verbatim (founder-doc-capture.py)
---

at's the correct diagnosis and a well-built PR. runAsNonRoot: true against an image whose config declares no USER is a kubelet-level refusal — no pull, no start, 86 refusals — and it explains the rate-limit exhaustion as a downstream symptom rather than a cause. Reading the registry config blob rather than assuming is exactly right. So is rejecting the helm-retry break-glass: retrying into a kubelet refusal produces the same refusal.

The upstream reference (tailscale#10638) also settles the runAsUser branch properly rather than by argument.

Merge it.

Three things worth saying, none blocking.

The exception is scoped correctly but it's an accumulating surface. You now have two — Lago's and this one. Two is fine; the shape to watch is that each PolicyException is a permanent hole with no expiry, and nothing rereads them when upstream fixes the image. The exception file header apparently states when it's reconsidered, which is better than most, but a reconsider-by date that no job checks is a document. If these keep accruing, a scheduled check that reruns the policy against current image configs and flags exceptions that are no longer needed is the version that doesn't rot.

The class here is worth naming, because it will recur. Estate-wide runAsNonRoot against third-party images is guaranteed to produce this — most upstream images run as root and declare no USER. So every new chart is a candidate. The cheap detector: your existing render pass can read the image config blob and fail when a workload asserts runAsNonRoot against an image with no USER. That catches it at CI instead of at 86 kubelet refusals, and it's the same measurement you just did by hand.

Sequencing: this unblocks tailscale, tailscale unblocks guacamole's dependsOn. Worth confirming after Flux reconciles that guacamole actually clears rather than having accumulated its own failure while it waited.
