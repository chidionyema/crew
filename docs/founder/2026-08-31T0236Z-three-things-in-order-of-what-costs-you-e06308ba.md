---
captured: 2026-08-31T02:36:27+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/.wt-backups
chars: 2661
source: founder prompt, verbatim (founder-doc-capture.py)
---

Three things, in order of what costs you most.

The diagnosis still isn't verified, and it's now hours old. Every summary still says the runtime refused an unqualified name — that's the same hypothesis from the start, never checked against the pod's own event. kubectl describe pod on the failing operator, or kubectl get events -n tailscale-system --sort-by=.lastTimestamp. Ten seconds. If it reads toomanyrequests, you're about to merge a PR that doesn't end the outage, and the mirror you've parked as "not tonight" is the actual fix. Everything else queued behind this is worth less than that one command.

I was wrong about admission-time digest resolution, and the agent's correction is right. Resolving a digest in the webhook means Kyverno calls the registry on every pod creation and fails when that call fails — so you'd have rebuilt the Docker Hub dependency at node recovery, precisely when the cluster is least able to tolerate it. Digest in Git, written by automation; admission only refuses anything that isn't a pinned reference on your registry. Same control, no live lookup. That correction stands, and the gap it names — your image automation only tracks your own six builds, while all five incidents were third-party — is the real work item.

The path-isolation advice would reintroduce the exact class you're eliminating. "Python tests must run against static mock fixtures, never the live cluster configuration files" — that's the stale expected list again, with more steps. A test that asserts against a fixture cannot catch a manifest regression; it can only catch fixture regressions, and it goes green while the estate breaks. Your render guard reads real manifests because that is the only thing that works. Don't sever that.

The other two items in that advice are fine and worth doing: path-based gating so a YAML-only diff runs Kyverno and skips pytest, and heavy suites in CI rather than pre-push. Both are sound. Just don't take item 1 with them — it's a control-integrity regression dressed as an architecture cleanup.

Two smaller things. "Ran the test on its own, so it's flaky" isn't established by one pass; a test that fails under the full suite and passes alone is usually order-dependence or shared state, which is a real bug that will bite again. And on the mirror: if OCIR genuinely has no pull-through, the cheap intermediate isn't Harbor — it's pushing those six third-party images into OCIR by hand and pointing at them. Fixed cost, no new component, no memory budget question, and it removes the Docker Hub dependency for everything that's actually hurt you. Harbor only earns its keep when the set stops being six.
