---
captured: 2026-08-30T23:26:25+00:00
session: a7b41022-3074-43c7-bb13-a1d7e07adff1
cwd: /Users/chidionyema/dev/code/.wt-otto-token
chars: 2404
source: founder prompt, verbatim (founder-doc-capture.py)
---

1. Delete the enumerated list. secret.reloader.stakater.com/reload: "a,b,c" is the bug surface — a hand-maintained list of names, unvalidated, silently wrong when stale. Switch to reloader.stakater.com/auto: "true", which watches whatever the pod spec actually references (envFrom, secretKeyRef, volumes). Nothing to maintain, nothing to typo, nothing to drift. If someone wanted the explicit list to avoid rolling on every change, invert it: auto everywhere, reloader.stakater.com/ignore on the specific noisy Secret. Failure mode flips from silently never rolls to rolls more than you wanted. One is an outage, the other is a shrug.

2. Move the invariant to admission, not the test suite. One Kyverno mutate policy across the estate: any Deployment/StatefulSet referencing a Secret or ConfigMap gets reloader.stakater.com/auto: "true" injected unless it carries an explicit opt-out with a reason. Not a validation that rejects — a mutation that makes it correct. Then it holds for every workload you have and every one you haven't written yet, and a service repo can't get it wrong because the service repo no longer decides.

That's the actual lesson from the stale test: an assertion a developer can green by editing the expectation is not a control. It lived in the same repo, same PR, same reviewer as the change that broke it. Controls have to sit outside the blast radius of the thing they guard.

3. Where you can, drop Reloader from the path entirely. Content-hash the secret into the pod template (checksum/secrets in Helm, or kustomize secretGenerator with hash suffixes) and rollout is API-server semantics, not a controller behaving correctly. Doesn't work for externally-rotated keys pulled by ESO — which Langfuse probably is — so this is for the subset where the renderer knows the content. Use it there, and the surface needing Reloader at all shrinks.

4. One detection backstop, since prevention is never total: alert on any Secret whose resourceVersion is newer than the creation time of every pod referencing it. Generic query, catches this class regardless of cause — bad annotation, Reloader crashlooped, webhook down. Fiddly to build off kube-state-metrics but you build it once.

Do 1 and 2 and this specific failure can't recur without someone deliberately opting out in writing. The current PR then becomes trivial — you're not fixing an annotation, you're deleting the list.
