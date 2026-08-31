---
captured: 2026-08-13T14:35:13+00:00
session: cbe776f2-17a1-49ca-8849-110cc5ebf7f7
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4502
source: founder prompt, verbatim (founder-doc-capture.py)
---

1. The root cause, and why it will recur

docs/SITE_SPEC_PROGRAM.md:773 had already written down the cost of name-first titles when it chose them: "the opening characters are what a scanner reads, and a coined word spends them." We shipped it anyway. Not because anyone was careless, but because the spec had no line saying who is reading, so the cost had nothing to be weighed against.

Right now the engine writes to two different readers and doesn't know it:

- the pack's prose addresses the NHS doctor whose rota is being audited;
- the storefront addresses the person deciding whether to run that business.

HoursBack is the proof: sold for £79.99 to a prospective owner, described in copy that talks to the doctor about their own pay. That single unstated fact produced today's whole session, and it will produce the next one on descriptions, then on pack bodies, until it is written down.

The cheapest durable move on the table is one paragraph, in prompts/, read by generate, revise, refine and retitle alike:

▎ The reader is a capable adult with no background in this sector who is deciding whether to spend a year of their life and their savings running this business. They are not the customer of the service. Assume they are smart, sceptical, and have never heard of any acronym you are about to use.

That costs nothing, needs no code, and is the only thing here that removes a whole class of rework rather than one instance of it.

2. Split what a machine can check from what it cannot, and stop pretending

Half of "jargon-free and educating" is mechanically checkable and should never reach a human eye again. The other half is not, and a linter that claims to check it will give you false confidence, which is worse than no check.

Checkable, deterministic, no model call:

┌────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────┐
│             check              │                                        why it bites                                         │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────┤
│ undefined acronym on first use │ "CIS gross payment", "IEP", "COSHH", "DWP" all ship today with no expansion                 │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────┤
│ reading grade over a threshold │ computable from the text, no judgement                                                      │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────┤
│ sentence length distribution   │ the 40-word sentence is where alienation actually lives                                     │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────┤
│ an insider-word deny-list      │ adversarial review, provenance, grounded verdict, composite score, lane, moat, unverifiable │
├────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────┤
│ every figure has a citation    │ already exists, figure_check.py                                                             │
└────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────┘

Not checkable, and honest about it: whether an explanation actually teaches, whether the order of ideas makes sense, whether a sceptical reader is persuaded or patronised. That needs a rubric with worked examples inside the generation prompt, and a human spot-check of a sample. Not a gate that pretends to measure it.

You already own the proof that the register is a choice, not a capability. copyConfig.ts carries the same sentence in both registers today:

▎ c: verified market pain, quantifiable value, fragmented incumbents, a solvent payer base, viable acquisition channels, and regulatory compliance
▎ b: a real problem, proven value, room to compete, buyers who can pay, a clear way to reach them, and no legal red tape

Identical content. One alienates, one educates. Nothing had to be invented to write b; someone just decided to. That is the entire quality programme in one example, and it argues for making b's register the house standard rather than one third of an A/B test.
 wwe need to apply rather than just talk
