---
captured: 2026-08-29T22:22:21+00:00
session: 41fd24d8-96a0-417e-bc3f-b7b15aceb026
cwd: /Users/chidionyema/dev/code/.wt-crew654
chars: 4507
source: founder prompt, verbatim (founder-doc-capture.py)
---

any reason why this was not apprived by crew 
  - **It does not make sessions reason correctly.** The Langfuse failure was a bad causal inference over real evidence. This layer forces the evidence to be real. It does not stop a session drawing too much from it.
  - **It does not cover claims about the past.** "This merged at 17:09Z" is a git fact, checkable, and outside this spec's scope. Consider extending the envelope to `evidence.kind: git`.
  - **It adds a dependency.** If Prometheus is down, the gate rejects everything. See the fail-loud requirement in §4.2 and make sure there is a documented manual override the founder can use.
  - **The prober can be wrong.** A probe asserting on the wrong identifier will report `MEASURED_OK` for a broken service. Probe definitions need review with the same seriousness as production manifests.
  - **It does not address concurrency.** Five bypass-permissions sessions cancelling each other's runs against a shared concurrency group was the operational problem at 18:19, hours before the false-claim problem. That is a separate ticket and arguably a more urgent one.

  ---

  ## 9. Open questions for the founder

  1. Freshness window: is 180s right, or does a claim need a probe from the same minute?
  2. Vetting (§6.3): are the ledger numbers the gate itself, or evidence you weigh and decide on manually?
  3. Canary honesty ratio: 40% honest windows is a guess. Higher makes the trap milder, lower makes "always distrust" a viable cheat.
  4. Does the envelope apply to founder-facing replies as well as board posts? Recommended yes — the 21:22 failure was in a reply to you, not on the board.

  Ran 2 shell commands

Optimised plan before I touch anything (LAW 51):

- Naive: 7 feature files written one call each, issue body, create, push → 10+ round trips.
- Bottleneck: serial file writes and a push-per-file wave, which is exactly what R57 (22:09Z) just banned.
- Optimised: one call writes all 7 features + the issue body; one call proves locally; one push wave; one issue. 4 calls, no CI, no cluster.

  Pushed to feat/crew628-verification-layer, ran 10 shell commands

INVENTORY: verification layer is a ticket, exact to spec, with BDD.

Built: crew#656 — your spec verbatim as docs/specs/verification-layer.md, seven BDD feature files (one per phase 0–6, 43 scenarios), all four of your flags and all four open questions carried into the ticket.
Use: https://github.com/chidionyema/crew/issues/656
Expect: seven checkpoints, CP0 blocking on nothing. Branch feat/crew628-verification-layer at cb1587a.
Not done: nothing built, nothing merged. The spec is copied, not implemented.
Evidence: ~/.claude/docs/founder/2026-08-29T2213Z-crew-628-verification-layer-4e0f20e1.md

---

Your four flags, and what I did with each

1. The prober on production. Written into CP1 as a blocking question, not a footnote: settle it before phase 1, not during. The ticket says plainly that if you disagree with §3.4's position, the whole design changes.
2. Phase 0 first. CP0, blocks on nothing, and the ticket says everything after it is refinement — your words. It is the only checkpoint with a budget on it.
3. Canary honesty ratio. Left as open question 3, unresolved, with your reasoning attached: all-lies makes blanket distrust a winning strategy, and the behaviour wanted is check, not distrust. There's a scenario in verification_canary.feature that grades exactly that — a session that always disbelieves the gauge scores no better than one that checks.
4. §8 concurrency. Recorded in the ticket as "not a caveat, the more urgent ticket" rather than buried in a limitations list. It is not in scope of #656 and needs its own.

One thing I did beyond the ask. Before opening it I checked the board: crew#631 already exists — closure verdicts, signing keys, a prover the agent cannot run. It overlaps §3.4's prober. I did not merge them, because they answer different questions (yours is live-state claims, #631 is work-item closure), but I cross-linked #628, #631, #638 and #656 to each other with a note to read all four first, so nobody builds the prober and the prover twice.

Two honest notes. The 21:22 failure in §0 was mine — that's why open question 4, whether the envelope covers replies to you and not just board posts, is the one I'd answer yes to without hesitating. And nothing here reaches a cluster: spec and feature files only, one push wave per R57 (22:09Z), freeze intact.

✻ Churned for 5m 24s · done 23:18 · 1 shell still running
