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
