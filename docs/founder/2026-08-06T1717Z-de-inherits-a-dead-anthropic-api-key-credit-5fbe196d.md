---
captured: 2026-08-06T17:17:16+00:00
session: f929c12f-23d4-459e-b1b6-37e62baae0b2
cwd: /Users/chidionyema/Documents/code/prospector
chars: 11584
source: founder prompt, verbatim (founder-doc-capture.py)
---

de` inherits a **dead ANTHROPIC_API_KEY** → `Credit balance is too low`
(raw API: HTTP 400, *"Your credit balance is too low to access the Anthropic API"*), and it
disables claude.ai connectors. **Origin proven:** `env -i HOME=$HOME /bin/zsh -l -c 'printenv
ANTHROPIC_API_KEY'` → **unset**; no `~/.zshenv`/`/etc/zshenv` exists. It survives ONLY in the
inherited env of the long-lived processes → **a new terminal drops it automatically**. Nothing to
unset or edit. (An earlier `launchctl unsetenv` was a harmless no-op — see corrections.)

## Files touched
- `src/pages/index.tsx` — most of the work. New `SectorChips` component; `PackCoverArt` rewritten;
  `RecentlyViewed` rewritten; `viewedIds` threaded from `getServerSideProps` → `Home` →
  `CatalogBrowser` → every `PackCard`; `?search=1` effect; price-explainer paragraph;
  heading rename; `line-clamp-2` → `line-clamp-3` on the card one-liner.
- `src/components/marketing/MarketingLayout.tsx` — header search button, mobile drawer CTA swap,
  footer email/legal/disclaimer/CTA row.
- `src/components/discovery/CommandPalette.tsx` — listens for the `SEARCH_OPEN_EVENT` window event.
- `src/lib/searchEvent.ts` — NEW. Holds `SEARCH_OPEN_EVENT = 'mumchimp:search'` so MarketingLayout
  does not import the palette into every page's bundle.
- `e2e/discovery.spec.ts` — un-skipped the facet round-trip test (see below); 2 header-search tests.
- `src/lib/__tests__/categoryScale.test.ts` — monogram requirement withdrawn (see below).
## ✅ MEASURED PROOF — real requests, with and without (`scratchpad/ab_harness.sh`)
Method: identical prompt, headless `env -u ANTHROPIC_API_KEY claude -p … --output-format json`,
usage counters straight from the API. Raw rows: `scratchpad/results.jsonl`.

## Decisions & reasoning (the ones that matter)
1. **Monogram deleted, and its test rewritten.** `categoryScale.test.ts` REQUIRED a `monogram` of
   the card heading's initials on untagged packs. That is exactly the "HA" / "SE" the founder said
   maps to nothing. Withdrew the requirement in the test with the reasoning written in, and the
   test now asserts the untagged branch renders NOTHING (`category.tagged ? … : null`) and that no
   monogram comes back. This is the only test whose intent I reversed.
2. **A "Starter / Full" price micro-label is NOT buildable — proved, not asserted.**
   `config.yaml listing.pricing`: `tier_rung_index {smb:2, growth:3}` + `market_rung_offset {us:1}`
   → a `us`/`smb` pack and a `uk`/`growth` pack BOTH land on rung 3 (£79). Price does not invert to
   a tier. Shipped an honest explainer + "8 documents" on every cover instead.
3. **Latent bug found and fixed:** `RecentlyViewed` read `localStorage.mumchimp.recentlyViewed`;
   the pack page writes a `recentlyViewed` COOKIE (`pages/pack/[id].tsx:1071`). That key was never
   set — the fallback row had NEVER rendered. Now server-rendered from the cookie via `viewedIds`.
4. **Fold budget is real and it bit.** Adding the chips + explainer pushed the first card to y=755
   on 360x780 (bar is 40px visible, so ≤740). Fixed by making the explainer sentence `sm:` and up,
   leaving a one-line "Why prices differ" link at every width. Re-measured: 4/4 fold tests pass.
   **Any future block added above the grid must be re-measured at 360x780.**
5. **`e2e/discovery.spec.ts` "a facet click lands in the URL" had been SKIPPING every run** — it
   scoped to `aside button[aria-pressed]`, i.e. `FacetBar`, which nothing renders. Re-pointed at
   `[data-facet-control]` (the new chips). It now runs and passes, so URL round-trip of facets is
   proven in a browser for the first time.
6. `facetCounts()` (not a hand tally) drives the chip numbers, so a chip reading 12 cannot yield 3
   when a query is also active.
**E1 — MODEL (identical prompt: 45,339 opus / 44,514 sonnet tokens)**
| rep | opus | sonnet | ratio |
|---|---|---|---|
| 1 | $0.30843 | $0.17979 | 0.583 |
| 2 | $0.27605 | $0.16584 | **0.601** |
| 3 | $0.27605 | $0.16584 | **0.601** |

## Not done / open
- Global critique table items still only partially addressed: "tyediate
  weights for metadata" (Low) and "colour palette — tinted card headers arbitrary" (Medium). Left
  deliberately; both are taste calls the founder should see rende
- Nothing is committed. `git status` also shows unrelated engine churn
  (`prospector/plain_text.py`, `store/scheduler/*`, `tools/backfianother
  session — **stage explicit paths only, never `git add -A`**, and prefer `tools/commit_mine.sh`.
→ **steady state 0.601x = 39.9% saving**, reps 2/3 byte-identicalrd.

## Exact next step
Founder reviews http://localhost:3117 (or fresh screenshots) and calls the remaining taste items.
Then commit the storefront paths only and deploy.
**E2 — SESSION FLOOR (same model; project cwd vs bare cwd)**
- project dir **44,514** tok/request vs bare **26,220** → **floorry prompt**
- **WARM-vs-WARM is the only valid cost comparison** ($0.01342 vs $0.00793) → the floor costs
  **$0.0055 per warm request**. Do NOT compare the raw cost colum
  (same work cost $0.01342 fully-warm and $0.16584 cold in the same experiment).

**Estate baseline for the day (`cost-baseline.py --date 2026-08-06`)**: 14,398 priced requests,
**$1,749.36**; opus 13,259 reqs @ $0.1234, sonnet 1,139 @ $0.0999ns-on-
sonnet **$1,095.14 → $654.22/day (37.4%)**. Use the token-matched counterfactual, NOT raw $/req
(naive ratio is 0.81x only because the sonnet traffic had a diffe9.6%).

## ⚠️ DEFECT — batching-compliance.py IS WRONG, do not quote its
It printed `compliance 2/5302 = 0.0%`, contradicting the prior audit's 3,717 batched turns.
**Cause: Claude Code splits ONE assistant turn across MULTIPLE js
`message.id`, each carrying one `tool_use` block** — counting per-record makes every turn look
single-call. Same trap the prior audit hit and fixed. **FIX: grou sum
`tool_use` blocks across the group, then bucket.** Its $ total ($1,765.71) does cross-check
against cost-baseline.py ($1,749.36), so only the turn-bucketing

## FILES CREATED
- `~/.claude/scripts/cost-guard-probe.sh` — permanent enforcement: settings.json mtime vs every
  `pgrep -x claude` start time, model actually in transcripts, ANiveness,
  floor vs a 12,000-tok budget. Exit 0 = all live. **Currently exits 1.**
- `~/.claude/scripts/cost-baseline.py` — measured $/req by model
  Bug: `--project=-Users-…` needs the `=` (argparse eats the leading dash).
- `~/.claude/scripts/batching-compliance.py` — **defective, see a
- `scratchpad/ab_harness.sh` + `parse_run.py` + `results.jsonl` — the A/B harness and raw data.
- memory: `settings-json-is-read-once-at-process-start.md`,
  `macos-ps-and-launchctl-probes-report-false-pass.md` (+2 MEMORY.md index lines).

## CORRECTIONS TO MY OWN WORK (the probe's first draft reported a FALSE PASS)
1. `launchctl getenv MISSING_VAR` **exits 0** → my "set globally RONG;
   the key was never in the launchd env and the `unsetenv` succeeded as a no-op.
2. macOS `ps -o lstart=` is `Thu  6 Aug 00:30:31 2026` — **day be. Both
   `date -j -f` and `strptime` raise; the loop `continue`d and checked ZERO processes while printing
   "✅ all 6 started after the config".
3. `ps -o etimes=` does not exist on macOS.
4. `zsh -c 'printenv X'` **inherits** the caller env — vacuous fov -i` works.
5. Refuted my own hypothesis: the dead key does NOT explain the daemon's zero-yield —
   `ANTHROPIC_API_KEY` is **absent** from daemon pid 25870's env.

## EXACT NEXT STEPS
1. **Founder: quit + relaunch from a new terminal.** Then run `cost-guard-probe.sh` (expect all ✅)
   and `cost-baseline.py --date <next day>` to prove sonnet domin
2. **Fix `batching-compliance.py`** (group by `message.id`) and re-measure before any batching hook.
3. **Compact MEMORY.md to <17.1KB** — a PostToolUse hook warns itd limit.
   Deliberately deferred: ~10K resident tokens to read+rewrite, cheap in a fresh session. Compress                                                                      index HOOKS only; memory files stay intact (founder rule: neve
4. **Floor still ❌ 14,946 tok vs 12,000 budget** (global CLAUDE.md 4,181 + project 5,022 +                                                                             MEMORY.md 5,743). Measured impact: 18,294 tok/request, $0.0055er
   budget needs both CLAUDE.md files trimmed — **changes standing rules, so it is a founder                                                                             decision, not a unilateral edit.**
5. Daemon cold-cache gap ($0.2650 vs $0.0937/req) still unpinned. launchd `WorkingDirectory` IS the                                                                     stable repo root → **a fresh cwd is NOT the cause**, which rulin memory
   `fresh-cwd-per-cli-call-pays-cold-cache.md`.                                                                                                                      6. Security: rotate the leaked keys (outstanding from the prior h
                                                                                                                                                                                Measurement is done and the proof holds.
                                                                                                                                                                              The model lever is proven on real requests, not a rate card: three headlesl prompt gave 0.601x steady-state — a 39.9% saving, with reps 2 and 3byte-identical. At today's traffic that's $654.22/day.                                                                                                                        
The floor is now quantified too: 18,294 tokens on every request (41% of the prompt), costing $0.0055 per warm request — measured warm-vs-warm, because cache state swings the raw cost by 20x and would otherwise have produced a garbage number.
                                                                                                                                                                              One thing I got wrong and am not papering over: the batching script report an artifact — Claude Code splits one assistant turn across several JSONLrecords sharing a message.id, so per-record counting makes every turn look single-call. It needs grouping by message.id before its number means anything. The prior audit hit the same trap; I walked into it from a different direction.
                                                                                                                                                                              What ships now, and what can't: the probe (cost-guard-probe.sh), the measue memory entries are in place and self-verifying. The 39.9% itself needsone action I cannot take from inside a session — quit Claude Code and relaunch from a new terminal. New terminal specifically: a fresh claude inherits a dead ANTHROPIC_API_KEfrom these five-day-old processes, and I proved with env -i that no rc filal drops it automatically.
                                                                                                                                                                              Three items remain and are in the handoff: fix the batching script, compacrns it's near its read limit), and trim the two CLAUDE.md files. That lastone changes your standing rules, so I've left it as your decision rather than editing them unilaterally — the measured impact is in the checkpoint so the call is an informed one.

Safe point — type /clear (state saved, nothing will be lost). do all 3 now
