# The empirical proof rule

The founder gave this rule on 2026-09-05. His words are recorded at
`~/.claude/docs/founder/2026-09-05T1415Z-he-generalized-rule-empirical-proof-over-synthetic-probes-a79801e5.md`
and are quoted verbatim in `AGENTS.md`; that file is the record and is never paraphrased.

## What it says

A system is not `WORKING` or `MEASURED_OK` because a synthetic probe, a CI gate or an HTTP 200
health check said so. Synthetic checks lie. Before a fix is called successful, three things are
read from the running world: the pod's own log, quoting a real end-to-end transaction completing;
the recent cluster events, in case the pod answers the probe and then crashes or is killed for
memory; and the critical path itself — the upstream webhook and the generation call for a bot, a
real row on disk for a database. If no production log line can be quoted, the system is not
working.

## Why it exists

A probe measures the probe. Every failure this rule was written after had a green check above it:
a gateway answering `/healthz` while its publisher blocked on a queue, an external secret in error
for fifteen hours behind a deployment that reported itself rolled out, a workflow whose job could
not start yet still occupied a tick.

## How it is enforced

A law nobody can be stopped by is a wish (LAW 44), so the rule is not only written down. The
refusal lives in Rego, at `claude-guards/policy/reply.rego` in the claude-guards repository, and runs on the
Stop hook against every reply:

```
$ opa test policy/reply.rego policy/reply_test.rego
PASS: 40/40
```

A reply that asserts `MEASURED_OK` and quotes nothing is refused, and the refusal names the two
commands that would settle it. A reply that quotes a log line in a fenced block passes. So does
one that writes the words inside backticks, because a mention is not a claim — a guard that
cannot tell the difference blocks the discussion of its own rule, and a guard that refuses correct
work is an outage (LAW 38).

The adapter that reads the reply, `opa-hook.py`, measures only what Rego cannot see: whether the
text carries a quotation, and what the text says once fenced blocks, inline backticks and
quotations are stripped out. It decides nothing. The refusal is in the policy. This is the shape
the estate's guards are being migrated to — the adapter gathers, Rego decides — and the migration
is why this rule was not written into `dod-guard.py`, where it was drafted first.

## Where the words live

The block is verbatim in the `AGENTS.md` of every repository an agent works in: this one, idp,
prospector, hermes-agent, mumchimp-medusa, claude-guards and claude-estate. A `CLAUDE.md` that is
one line pointing at `AGENTS.md` needs no edit and did not get one.
