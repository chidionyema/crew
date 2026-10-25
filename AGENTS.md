# AGENTS.md — the operating core

Everything is this file, a guard, or a log entry. Prose history: `~/AGENTS-FULL.md`.
Incidents and rulings: `~/.claude/LAWS-INCIDENTS.md`. Craft: `~/ENGINEER.md`. A project's
architecture: that project's `CLAUDE.md`.
**Hard budget: 500 words. Adding a rule costs deleting one. Incidents produce guards or
log entries — never rules.**

## Context — read like a brief, not a law

We are selling this. The buyer buys products (`prospector`, `hermes-v2`); products run on
one platform (`~/dev/code/idp`) with exactly one of each layer: routing, traces, identity,
secrets, scheduling, catalog, CI. A second copy of any layer is stitching and gets
deleted. A product is never deleted for living outside `idp`.

Assume a hostile buyer's engineer audits everything next week. The founder is a user, not
an operator: nothing he must invoke, configure, or babysit — anything he touches, he
touches once.

## Invariants — always-on assertions

1. **Evidence or it didn't happen.** No status without the proving output shown in the
   same turn. Self-certification is void; the Verification Plane's signed verdict is the
   only proof of done.
2. **Solve the class, never the instance.** A mistake closes only when its causal chain is
   followed to the end — chains branch — the class is named, a guard blocks the class, and
   every instance is swept clean.
3. **Adopt before you write.** New code requires naming the mature tool you rejected and
   the specific thing it cannot do — after searching branches, commits, and the inventory
   for prior art.
4. **Reversible: do it and announce `STAGED:`. Irreversible: ask.** Rulings move the
   boundary; under R60, every merge is founder-only.
5. **The stack is sacred.** An interrupt pushes a checkpoint frame; completion pops and
   resumes. Nothing is finished while the stack is non-empty.

## The loop

    frame = {goal, done_when: [commands], decisions, next_step, open_questions}

    loop:
        if fire:            interrupt(fire)                      # the only preemption
        on interrupt(msg):  stack.push(checkpoint(frame)); frame = new(msg)

        plan = optimise(frame)            # count steps, name bottleneck, batch/parallelise
        preconditions(plan)               # incl. "does this already exist?"
        execute(smallest_change(plan))
        evidence = postconditions(plan)   # verdict shown, or the claim doesn't exist

        if mistake:
            chain = causal_chain(mistake)     # to the end; branches included
            cls   = generalise(chain)         # the class, not the instance
            guard(cls); sweep(instances(cls))

        if done(frame, evidence):
            report(evidence)
            frame = stack.pop() or board.next()   # unwind fully before new work

## Interface

Reply grammar, board mechanics, and model routing live in `idp/docs/policy/` and are
enforced by guards, not by reading.


## THE EMPIRICAL PROOF RULE (founder 2026-09-05, verbatim; record: `~/.claude/docs/founder/2026-09-05T1415Z-he-generalized-rule-empirical-proof-over-synthetic-probes-a79801e5.md`)

NEVER declare a system "WORKING" or "MEASURED_OK" based solely on synthetic probes, CI gates, or HTTP 200 health checks. Synthetic checks lie.

Before claiming a fix is successful, you MUST prove it empirically:
1. **Read live traffic:** Fetch the actual pod logs (`kubectl logs --tail=100`) and quote a real, end-to-end user transaction completing successfully.
2. **Check for silent failures:** Look at the most recent cluster events (`kubectl get events`) to ensure the pod isn't crashing or OOMing immediately after answering a probe.
3. **Verify the critical path:** If it's a bot, verify the upstream webhook and LLM generation path. If it's a database, verify a real row was written.

If you cannot quote a successful production log line, the system is NOT working.

<!-- growmos:start — managed by `growmos integrate`; edits inside this block will be overwritten -->
## growmos — living knowledge graph (shared memory for humans + agents)

This repository keeps a knowledge graph in `.growmos/` (entities, typed relations, provenance,
profiles, a journal). It is the shared world model that survives context windows. Treat it as
memory you read at the start of work and write to as you develop. Zero-config commands:

1. **Session start** — run `growmos context` (a compact brief: hubs, health, pending work, latest journal).
   If it lists pending work, run the `growmos next` → apply loop (step 4) right away, without being asked —
   it is quick, needs no permission, and is how the graph stays alive.
2. **Before cross-cutting questions** ("what depends on X?", "why was Y decided?") — run
   `growmos query "<question>"`; answer from the returned subgraph and cite edge ids.
3. **When you learn or decide something durable** (new component, architectural decision, ownership,
   dependency, gotcha) — write it back immediately:
   - `growmos remember "<Name>" --type <TYPE> --desc "<one grounded sentence>"`
   - `growmos link "<A>" "<predicate>" "<B>"`   (short verb phrase predicates: "depends on", "replaces")
   - `growmos journal "<what changed and why>"`
4. **Feed the organism** — run `growmos next`. It hands you a *task packet* (extraction / resolution /
   profile / gold set / review) with the exact prompt, the JSON shape, and the `growmos apply …` command.
   Do the judgment work yourself, write the JSON, apply it. Repeat until `growmos next` says the graph is
   up to date — that loop covers everything, including the evaluation gold set and the periodic node review.
   If it reports the daily extraction cap, run `growmos next --force` (the cap only guards unattended runs).
   Never invent facts not in the source; every relation must connect two extracted entities.
5. **Before claiming facts about the repo in a summary/report** — `growmos check "<claim text>"` grounds
   your claims against edges with provenance (evaluator–optimizer loop).
6. **Session end** — `growmos journal "<summary of the session>"` so the next session picks up here.

Store files are plain JSONL under `.growmos/` — commit them with your code. Do not hand-edit
`entities.jsonl`/`relations.jsonl` (use the CLI); prompts in `.growmos/prompts/` are yours to tune.
More: `growmos --help`, docs at https://github.com/codician-team/growmos.
<!-- growmos:end -->
