---
captured: 2026-08-31T00:14:44+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/.wt-backups
chars: 3112
source: founder prompt, verbatim (founder-doc-capture.py)
---

Good correction, and the guard moved to the right layer for the reason you'd want — chart defaults only exist after render, so a source-file check could never have seen them. That's the placement lesson landing. Three things before you merge.

**Verify the failure string, not the theory.** "The runtime refuses it because the name doesn't say which registry" is a hypothesis, and it's the shakier of the candidates. containerd resolves unqualified names against `docker.io` by default; if it had resolved and failed, the event would read `failed to pull and unpack image "docker.io/tailscale/k8s-operator:v1.102.3"` — already showing the registry. An unqualified-name rejection means someone removed the default resolver or configured a mirror that requires FQDN. The far more common causes for that image on OKE are Docker Hub anonymous rate limiting (`429 toomanyrequests`) or a missing pull secret, and both are invisible to a fix that only rewrites names. So: `kubectl describe pod` on the failing operator, in the same turn, and read the literal message. A CI run log is not the pod's event. If the string says `toomanyrequests`, the twelve-file commit is correct hygiene that fixes nothing, and Guacamole stays dark after you merge.

**The render-time guard has a hole that this specific incident sits inside.** Rendering covers pods your manifests declare. It cannot see pods that operators create at runtime — and the Tailscale operator's whole job is generating proxy StatefulSets with images from its own config. Same for any future operator you install. So the class isn't eliminated; it's eliminated for the static subset. The closing move is admission: a Kyverno policy on Pod that *mutates* unqualified images to your registry (or your pull-through cache), which catches manifest-declared and operator-generated pods identically, at the one point every pod must pass through. Then the render check becomes a fast pre-merge echo of a rule that's already enforced regardless.

That's also the answer to "fourth time in five days." It isn't four incidents — it's one control placed above the layer where the defect is introduced, three times. The rule to hand the crew: **place the control at the last point where all inputs are merged.** For Helm values, that's the rendered object. For anything a controller creates, that's admission. Anywhere earlier is a check with a blind spot, and the blind spot is where the next one comes from.

**Budget.** You now have a file-reading guard and a render guard covering the same invariant, and the file one has demonstrated it can't see chart defaults. If the render guard subsumes it, delete it in this PR. Otherwise you're accumulating the exact artefact that started this — a control that passes green while the thing it guards is broken.

Worth noting for later, not now: registry qualification is a weaker form of digest pinning, and a digest reference is fully qualified by construction. If you eventually pin by digest with automated bumps, this class stops existing rather than being policed. Bigger change, wrong moment, but it's where this ends up.
