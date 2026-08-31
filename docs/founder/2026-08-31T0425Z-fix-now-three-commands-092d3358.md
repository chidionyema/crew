---
captured: 2026-08-31T04:25:50+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/idp
chars: 1740
source: founder prompt, verbatim (founder-doc-capture.py)
---

Fix now, three commands:

flux suspend hr tailscale -n flux-system
flux resume hr tailscale -n flux-system

If it re-wedges with the same message:

helm rollback tailscale-operator -n tailscale
flux reconcile hr tailscale -n flux-system --with-source

That clears a stuck Helm release. The upgrade failed because the pods couldn't come up (the image name), Helm timed out, and the release is now parked in failed — it does not retry itself. With #1030 merged the manifest is correct, so a clean retry should succeed. Guacamole's dependsOn clears automatically the moment the HelmRelease reports Ready.

Fix forever, one field on every HelmRelease in the estate:

yaml
upgrade:
  remediation:
    retries: 3

Retries, not strategy: uninstall. Retry re-attempts the upgrade after a failure; uninstall deletes the release and takes your PVCs and Secrets with it. With retries set, a transient failure self-heals and you never hand-clear a wedged release again. Without it, every failed upgrade in your estate is a permanent block requiring you at a terminal — which is exactly what happened tonight.

Put it in the base HelmRelease patch so it applies to all of them, not per-release. Then add the admission rule: reject any HelmRelease without upgrade.remediation. That's the class killed — no release in this estate can wedge silently and wait for a human.

The dependsOn cascade is the second half. It's correct behaviour, but it means one wedged chart takes down everything downstream. Worth knowing which of your services sit behind Tailscale's readiness, because that's your blast radius for any future Tailscale failure — and if Guacamole doesn't genuinely need Tailscale ready to start, the dependency is costing you more than it buys.
