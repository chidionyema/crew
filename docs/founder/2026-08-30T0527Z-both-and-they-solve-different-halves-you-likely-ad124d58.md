---
captured: 2026-08-30T05:27:29+00:00
session: 14ed6c8b-f0a9-40d7-82a8-895f336f9b78
cwd: /Users/chidionyema/dev/code/.wt-tone-audit/store_platform/src/Store.Web
chars: 1982
source: founder prompt, verbatim (founder-doc-capture.py)
---

Both, and they solve different halves — you likely want both, not a choice.

**Flux rolls back at the Git/release layer.** `HelmRelease` has native support:

```yaml
spec:
  install:
    remediation: { retries: 3 }
  upgrade:
    remediation:
      retries: 3
      remediateLastFailure: true
  rollback:
    enable: true
    cleanupOnFail: true
```

Helm reverts to the previous release revision if the upgrade fails. Real, works today, no extra components.

The catch: **"fails" means Helm's definition of failure** — bad manifest, failed hook, pods not reaching Ready within timeout. It cannot detect a deployment that starts perfectly and then returns 500s to 20% of requests. Kustomization has no equivalent at all; its remediation is retrying the apply, and "rollback" means reverting the Git commit. Flux's health checks are readiness, not correctness.

**Argo Rollouts rolls back at the traffic layer**, on metrics or test results, in seconds, before most users notice. That's the gap Flux can't fill.

They compose cleanly because Rollouts is just a controller reconciling a CRD — no Argo CD, no second GitOps engine. Install it via a Flux `HelmRelease`, then have Flux reconcile your `Rollout` and `AnalysisTemplate` manifests like anything else.

One wrinkle that bites people: after Rollouts aborts a canary, the cluster is serving the old version but Git still says new. Flux will keep reconciling the `Rollout` spec — which is fine, since Rollouts owns the abort state and won't re-promote on its own — but your Git and running state have diverged, and nothing tells you. Wire the abort to an alert, and treat the fix as a Git revert. Otherwise the next unrelated reconcile is where you discover it.

Sequence I'd suggest: turn on `HelmRelease` remediation today — it's free and catches the dumb failures. Add Rollouts to one service on staging afterwards, starting with a `pause` step and no analysis so you learn the promotion mechanics before you add metric gating.
