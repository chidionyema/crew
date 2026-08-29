# Requirements — verification layer

**Source:** the founder, 2026-08-29, in conversation. Captured verbatim on arrival at
`~/.claude/docs/founder/2026-08-29T2213Z-crew-628-verification-layer-4e0f20e1.md`,
committed to the claude-estate repository as `162b9d9`.

**Status:** requirements. The spec that answers them is `docs/specs/verification-layer.md`.
The work is crew#656.

---

## What he asked for, in his words

> "for our unified model, i want to trail out another verification layer ticket and get
> done exact to spec pls bdd"

Three requirements sit inside that sentence and none of them is optional:

| # | Requirement | Why it is here |
|---|---|---|
| R1 | It serves the **unified model**, not a repo. One layer, every crew session, every estate repository. | A second verification stack is the stitching the headline bans. |
| R2 | **Exact to spec.** The spec is copied, not interpreted, not summarised, not improved in passing. | He wrote it. A session that paraphrases it has replaced his requirement with its own. |
| R3 | **BDD.** One feature per rollout phase, in plain English, gradeable. | A checkpoint with no feature file cannot be ticked by anyone but its author, which is the failure this whole layer exists to remove. |

## What he flagged before it reaches a session

These are requirements, not commentary. Each one changes the work if ignored.

| # | Flag | Consequence if ignored |
|---|---|---|
| F1 | The prober must live on the production cluster. That only holds if **the prober is infrastructure, not crew**. §3.4 takes that position. | If he disagrees, the whole design changes. This is settled **before** phase 1, not during it. |
| F2 | **Phase 0 first.** The vocabulary ban and the banned-token check are an afternoon and would have caught both of 2026-08-29's failures alone. | Building phase 1 first spends the budget on refinement and leaves the failure mode live. |
| F3 | The **canary honesty ratio matters more than it looks.** All-lies makes "never trust the gauge" a winning strategy, which is not the behaviour wanted. | A trap that rewards blanket distrust trains the opposite of measuring. Open question 3. |
| F4 | **§8's concurrency problem is the more urgent ticket.** Five sessions cancelling each other's runs against one concurrency group was the live problem at 18:19, hours before any false claim. | Left as a footnote it stays unowned. It needs its own ticket. |

## Questions he has not answered

Work that depends on these waits. Work that does not, proceeds.

1. Freshness window: 180 seconds, or a probe from the same minute?
2. Vetting: are the ledger numbers the gate, or evidence he weighs by hand?
3. Canary honesty ratio: 40% is a guess.
4. Does the envelope cover replies to him, not only board posts? The spec recommends yes; the 21:22 failure was in a reply to him.

## Acceptance

The requirement is met when a session cannot emit an unverified claim about live
state without being refused, and when the founder can read who measures and who
guesses without asking any session.

Not met by: merged code, green CI, or a passing feature file. Those are inventory.
