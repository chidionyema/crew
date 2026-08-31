---
captured: 2026-08-08T00:25:06+00:00
session: 3be0f089-8bd0-4ab9-9d75-c8f34f180ec6
cwd: /Users/chidionyema/Documents/code/prospector
chars: 5511
source: founder prompt, verbatim (founder-doc-capture.py)
---

's live arm are both **not affordable as specified**. If they are to run,
   they need re-specifying first (E2: a different hypothesis than payer class; E5: narrow to the two
   high-cardinality axes).
## Proof (computed values in a real browser, not greps)
Playwright over `/`, `/sample`, `/kill-log`, `/pricing`, `/how-it-works` at 1280×900:
`fontFamily[0]` = **Switzer**; `--shadow-1` = **none** and elements with a non-`none` boxShadow =
**0**; only non-zero `borderRadius` = **2px**; `--accent` = **#171717**. Built sheet: `2563EB` × 0,
`Geist` × 0, `text-mega` × 0. `npx tsc --noEmit` **exit 0**, `npm run build` **exit 0**.
Screenshots: `<scratchpad>/shots/*.png`. Script: `<scratchpad>/shot.mjs` — **must be copied into
Store.Web to run** (node can't resolve `@playwright/test` from the scratchpad).

## Constraints in force
- Money rail / identity / contract / migrations never leave Claude; `pi_execute` refuses them.
- Only key *names* and lengths may be printed from `.env`, never values.
- Live experiments run via `tools/experiments/runner.py run <NAME> --live` — that is what persists
  receipts (`runner.py:223`).
- Commits are backgrounded (POPDD is slow, ~9 min, and races HEAD).
## Probe fixes made this pass (state is a probe, not a paragraph)
- `scripts/site_spec_probe.py`: `_globals_css()` now reads **globals.css + tokens.css** — the split
  made §3.5 report FAIL on a 120ms token that had merely moved to `tokens.css:99`.
- `PROBES["3"]` was hardcoded `probe_not_started("superseded by brand v3")` — replaced with a real
  `probe_design_system()` that reads the tree. It deliberately does not check the dark palette.
- That probe first failed on `next/font` matching its own explanatory **comment**; now matches an
  import statement. Same trap made the ledger's §6.1 bullet look live (both hits were comments
  recording their own removal) — bullet retired with that evidence.

## Next steps (none started)
1. **Mono-vs-grotesk split (§3.2)** — the semantic split ("prices, counts, verdicts, sources,
   filenames, dates → mono") is NOT swept sitewide. `.text-data` / `.text-label` classes exist in
   `globals.css` for it. Visible gap: `/sample`'s stat strip renders counts in sans semibold.
2. **§3.5 resolve sequence** — the six marks it needs now exist. Probe row is 🟡, FAIL-free.
3. **§6.7 intent search** — the only remaining **P1**. §4b, §6.8 P2. §7 LCP still unmeasured.
4. **Commit.** Nothing is committed. `git commit --only <paths>` ONLY — never `git add -A`
   (`store/`, `storage/` are tracked runtime state) and a concurrent session is live in this
   checkout (do not touch E1: `prospector/claude_cli.py`, `tests/unit/test_e1_abort_on_outage.py`,
   `tools/experiments/e1_hybrid_query_arms.py`).

## Environment note
The API at `localhost:5291` is DOWN, so the catalogue renders 0 packs — marketing pages, `/sample`
and `/kill-log` render from local data and were sufficient. **`:3117` is another session's server —
do not measure it.** I used `:3428` and stopped it.

§3 is implemented and proven. The last two open claims from before are now settled with receipts rather than reasoning.

The shadow question is answered. --shadow-1 computes to none, not just declares it: the @theme inline self-reference sits in @layer theme while :root's none is unlayered, and unlayered wins. Confirmed at the DOM — 0 elements with a non-none box-shadow across five pages.

Everything else, measured in a real browser (Playwright, getComputedStyle, 1280×900, on /, /sample, /kill-log, /pricing, /how-it-works): body renders in Switzer, --accent is #171717 (ink), and the only non-zero border-radius anywhere is 2px. tsc --noEmit exit 0, npm run build exit 0.

§3.3 is no longer decoration. Glyph.tsx was written but unused; the six ma— sample.tsx (×4), kill-log.tsx (×2), pack/[id].tsx (×5), DossierCard,EvidenceExcerptPlate. Two lucide icons were checked and deliberately kept: the 14-day refund shield is a commercial policy we chose, and FacetBar's tick counts filter matches.
Neither is a verdict.

Two things I changed that reverse earlier deliberate decisions — flagging
- The homepage hero dropped 96px → 48px. --text-mega was a seventh size on a six-step scale; §3.2 puts the hero at 3rem. The fold measurement that justified it isn't
invalidated (going down only gives the fold more room), and the hero is noOne line reverts it if you disagree.
- --text-h1 2rem → 2.25rem, reversing a v3 drop made for Geist's x-height. Both top steps are now clamp()s carrying their own mobile size, and both max out at 1000px — so
every measurement previously taken at 1280 still holds.

The probe was lying in two directions and is fixed. §3's row was hardcodederseded by brand v3") — it could never change no matter what shipped; itnow reads the tree. And my token split made §3.5 report FAIL on a 120ms value that had merely moved files. python3 scripts/site_spec_probe.py → "Ledger agrees with the tree",
§3 PASS.

One correction to something I'd assumed: the ledger's §6.1 bullet looked sto contradict that — "What you get, at every price" and engineGateIds eachreturn 1 hit in index.tsx. Both are inside comments recording their own removal. It was genuinely stale; I retired it with that evidence attached.

Not done, not claimed: the mono-vs-grotesk sweep (§3.2's semantic split — /sample's stat strip still renders counts in sans), the dark palette, and the --verdict-* rename.
Nothing is committed.

Safe point — type /clear (state saved, nothing will be lost).
 we need to ship
