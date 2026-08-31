---
captured: 2026-08-30T23:32:40+00:00
session: a7b41022-3074-43c7-bb13-a1d7e07adff1
cwd: /Users/chidionyema/dev/code/.wt-otto-token
chars: 5614
source: founder prompt, verbatim (founder-doc-capture.py)
---

Yes, and the pattern is sound. But two of the things in that pasted advice will actively prevent you from getting there, so let me separate them first.

The advice that undercuts the goal

remediation: strategy: uninstall and kubectl delete namespace as routine practice are the opposite of what you're asking for. Uninstalling a wedged HelmRelease turns a degraded service into a deleted one — PVCs, PDBs, Secrets created by the release, gone — and for anything stateful that's a self-inflicted outage triggered automatically at 3am by a chart bug. Namespace deletion also hangs on finalizers roughly as often as it works.

More importantly, both destroy the evidence. You cannot convert an incident into a permanent control if your first move erases the state that tells you which invariant was violated. Paving over is a way to survive incidents forever without ever eliminating a class. It's a stability strategy in direct conflict with the strategy you actually want.

Keep the ability to repave — but as a manual break-glass after capture, never as automated remediation.

The meta-class

Your three incidents are one defect:

An invariant that exists only in a person's head, enforced nowhere, discoverable only in production.

Reloader: "this annotation must list every Secret the pod consumes" — enforced by a hand-edited test in the same PR as the change.
Kyverno gridlock: "the rendered manifest must satisfy cluster policy" — checked only after merge, by the cluster.
envsubst: "this field must stay a string through the render pipeline" — checked only by the API server at dry-run.

Same shape three times. So the enforceable rule for the crew isn't "fix the class," which is vague enough that an agent will write a runbook and call it done. It's a placement rule plus a proof obligation.

The ladder

Every control gets placed at the lowest-numbered rung that's achievable, and the session must state why lower rungs were rejected:

Delete the surface. No enumerated list means no stale list. (Reloader auto instead of the explicit list.)
Make it inexpressible. Type, schema, or mutating admission that renders the wrong state unconstructible.
Fail before merge. kubeconform, kyverno apply, rendered-manifest tests in CI.
Fail at admission. Cluster-side validating policy.
Detect at runtime. Generic invariant alert.
Document it. Not a control. Counts as zero.

Both pasted answers landed on rung 2 and called it elite. Rung 2 is fine, but for envsubst the rung-0 move is available and better: stop text-substituting into typed CRDs at all. kubeconform in CI catches the integer; Kustomize replacements means there is no integer to catch.

The proof obligation

This is the part agents will skip, and it's the part that makes the difference.

A control must be demonstrated failing against the pre-fix state before the task can close.

Write the policy, then run it against the broken manifest and show it rejecting. A control nobody has watched fail is not known to work — it's a green check of unknown provenance, which is precisely what the stale expected list was. This is a red-test discipline applied to infrastructure. It's cheap, it's mechanically verifiable, and it's the single highest-value line you can add to the crew's standing instructions.

The constraint you're missing

"Every incident yields a new control" is unbounded growth, and controls rot — your stale test was a control. Without a budget you build a second system as complex as the first, with its own failure modes, and the estate gets less predictable rather than more.

Two rules bound it:

A control that names a specific service is the wrong control. Per-service assertions are O(n) rot. Estate-wide policy is O(1). If the session's fix mentions hermes-agent-langfuse, it hasn't finished — it's still at the incident, not the class.

Adding a control at rung 2 or above requires deleting a weaker one it subsumes. The Kyverno mutation makes the Reloader test redundant; delete the test. Net control count should stay roughly flat while coverage rises.

Enforcing it on agents

Prose in a CLAUDE.md is itself an invariant living in someone's head — you'd be violating your own pattern. Make it machine-checked:

A PR touching infra must either contain a change under policies/ (or wherever your controls live), or carry an explicit no-class-control label with a one-line reason. CI fails otherwise. That's rung 2 applied to the process itself, and it survives agents that skim their instructions.

Pair it with a required exit block per task — immediate fix / class statement in one sentence / control and its rung / evidence the control rejects the pre-fix state — and you have something you can grade rather than trust.

On sleeping at night

Achievable for this family. Config and manifest defects are deterministic and statically decidable; there's no reason a type error or a missing annotation should ever reach your cluster again, and driving that to zero is a finite project.

Not achievable for capacity, upstream dependency failure, or hardware. Those you absorb rather than eliminate.

The thing that will actually decide whether you sleep is different from control count: how many known-broken-but-tolerated things you're carrying. All-green is easy to fake by ignoring amber, and a dashboard you've learned to discount is worse than no dashboard. Track the count of signals you routinely dismiss and drive that to zero — by fixing them or deleting them — and green starts meaning something. That number is the one worth putting on a wall.

You’ve used 75% of your weekly limit
Write a message…




Claude is
