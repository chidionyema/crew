---
captured: 2026-08-30T04:13:48+00:00
session: 41fd24d8-96a0-417e-bc3f-b7b15aceb026
cwd: /Users/chidionyema/dev/code
chars: 2658
source: founder prompt, verbatim (founder-doc-capture.py)
---

Assuming you mean where Hermes sits relative to the orchestration question rather than a general rundown — it isn't a substitute for either, and the distinction matters more here than in most stacks.

Hermes gives you a persistent process with memory, self-created skills, a messaging gateway and natural-language scheduling. What it doesn't give you is durable execution. Its cron runs unattended through the gateway, but there's no checkpointed step state, no retry semantics you can reason about, no idempotency contract. If a run dies at step four you don't resume at step four — you get whatever the agent reconstructs from memory, which is a different and worse thing. And the execution path is LLM-mediated, so it's non-deterministic by construction. That's the exact opposite property from the one you were shopping for with Temporal.

So the composition is: Hermes is the interface and judgment layer, Windmill flows or your .NET services are the execution layer, and Hermes calls them rather than being them. A skill fires an HTTP route into a flow, the flow does the actual work with checkpoints and retries, the result comes back to the gateway. Non-determinism sits at the edges, never in the path that touches money or production state. For the commodity execution system in particular, nothing LLM-mediated goes anywhere near the execution path — the agent's job there is monitoring, reconciliation and telling you about it, not pulling triggers.

Two things worth checking given what you've said you want out of Otto:

**Memory across local and cloud.** Hermes stores memory in a local SQLite database on the machine it's running on. If you run one instance on the MacBook and one in the cloud, you have two memory stores and no sync story out of the box. That's the concrete blocker on "local and cloud, not one or the other" — it's a design problem you'll have to solve rather than a config flag.

**Silent delivery failures across profile boundaries.** There's a paper (arXiv 2606.04896) documenting cross-boundary reliability failures in multi-agent Hermes deployments — messages that vanish between profiles without erroring. Given your whole stateless-daemon design exists to eliminate self-certified false successes, that's worth reading properly before you commit the orchestrator/autonomous-engineer split to the profiles system. I've only seen the abstract, so take that as a pointer rather than a finding.

One genuine advantage over the Windmill discussion: Hermes is MIT. If agent capability ever becomes part of what you sell, that's one less licence conversation.

If you were actually asking something narrower, say which bit.
