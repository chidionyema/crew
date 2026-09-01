# R72 — Adopt both harnesses: Goose and our own; the long term decides

**Founder, 2026-09-01, the record:**
`~/.claude/docs/founder/2026-09-01T2007Z-first-of-all-this-is-what-we-have-c88b745c.md`

"I like the idea of goose and also like the idea of our own harness ... I think we adopt
both and see what wins out in the long term, we should not be afraid to have tooling but
we should know when to improve and deprecate."

He also flagged the risk directly: "the claude code harness may be limiting our ethos of
not being tied to any one provider."

## The decision

1. **Goose is adopted** (Apache-2.0, Linux Foundation / Agentic AI Foundation) as the
   off-the-shelf harness lane: planner, executor and reviewer are configuration, every
   model call goes through the estate router (the laptop holds only the router key).
2. **Our own harness lane is the `verified` router model** (R67 made runnable): a DSPy
   program behind one model name on the existing LiteLLM router — strong planner, MiniMax
   executor (last hop, always), strong reviewer that is never the executor. Any client,
   including Goose and Claude Code, inherits it by typing one model name.
3. **Claude Code stays** but is now explicitly one harness among several, watched for
   provider tie-in against LAW 34.

## The bake-off is measured, or it is a wish (LAW 44)

Same tasks through both lanes; Langfuse holds the traces. The scoreboard per lane:
task pass rate (independent verifier, never self-scored), cost per passed task, and
founder-visible friction (actions he had to take). Reviewed on a stated cadence by the
CEO in the daily report; the loser is improved or deprecated — "know when to improve
and deprecate" is part of the ruling, not advice.

Related: R67 (the pattern), R71 (charter), crew#568 (model stack), crew#751 (Cursor,
stopped by the CEO consult pending founder word).
