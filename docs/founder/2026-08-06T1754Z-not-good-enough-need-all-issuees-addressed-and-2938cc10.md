---
captured: 2026-08-06T17:54:12+00:00
session: a6e5ac22-949a-4e65-8c5b-f0bc15862d6c
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2927
source: founder prompt, verbatim (founder-doc-capture.py)
---

not good enough need all issuees addressed and shipped, we neeed to lanuch 
Done. The three failing tests are repaired and the full sweep is green.

Verification (all run after the last edit):
npx tsc --noEmit                                          exit 0
npx vitest run                    54 files, 779 tests      exit 0
npm run lint                      0 errors, 1 warning      exit 0
NEXT_PUBLIC_API_URL=… npm run build                        exit 0
WEB_BASE_URL=http://localhost:3117 npx playwright test e2e/
                                  31 passed (43.4s)        exit 0
  ✓ the first pack card is above the fold at 390x844
  ✓ the first pack card is above the fold at 360x780
  ✓ the first pack card is above the fold at 430x932
The one warning is pre-existing: src/pages/pack/[id].tsx:151, react-hooks/exhaustive-deps missing pack.

The three test repairs
- src/lib/copy.ts:95 — em-/en-dash now written as \u2014\u2013 inside the character class, so nothing literal remains in the file including the comment. dashFree.test.ts passes.
- categoryScale.test.ts — the chip guard assertion now accepts {cat.tagged && or {category.tagged &&. The chip moved into PackCoverArt, where the same object arrives as a prop; the guard is what the test protects, not the identifier.
- usTwoPackArt.test.ts — the two assertions encoding the seeded per-pack cover jitter are withdrawn with the reasoning written in place, same treatment the monogram got. Replaced with a literal-class-string assertion on COVER_WEAVE, because the Tailwind-scans-source constraint that motivated the original still holds. The Math.random ban stays.

Scratch scripts (shots.mjs, shots2.mjs, measure.mjs) are deleted.

Two things found and not fixed — they're yours to call:
1. 23 of 63 packs have no cardLine, so their card heading is a bare brand name ("RateRebase"). That's a content backfill, not a UI bug. I deliberately left cardHeading() alone — its docblock records a measured rejection of promoting the 90+ char descriptor instead ("twenty cards of wrapped bold text").
2. The 34 truncated oneLine rows are now invisible to readers, but only because the storefront repairs them at the boundary. The database is still dirty; only a re-publish actually fixes it, and that's a money-rail operation (upsert ignores PricePence on update, bundle keys are content-addressed).

Nothing is committed. Mine to stage: src/pages/index.tsx, src/pages/pack/[id].tsx, src/components/marketing/DossierExcerptPlate.tsx, src/lib/copy.ts (untracked — needs git add first), the two test files, and prospector/bridge.py. Also dirty but not mine — a concurrent session's search work, modified 17:43–18:01 against my 18:30+: e2e/discovery.spec.ts, CommandPalette.tsx, MarketingLayout.tsx, src/lib/searchEvent.ts. Say the word and I'll commit only my paths.

Handoff written to checkpoints/2026-08-06-storefront-design-review.md with a pointer appended to LATEST.md.
