---
captured: 2026-07-31T07:05:42+00:00
session: 80aa453b-22f8-45bb-9214-d7389d17300f
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2139
source: founder prompt, verbatim (founder-doc-capture.py)
---

The Matchmaker collapse alone was not enough — I wrote the falsifiable test first and it failed with the router already collapsed:

Expected: < 720
Received:   1094.34375

Measured breakdown at 1280×720: hero 606px, "What survived" heading block 206px, full-width three-question form 107px. So I cut all three.

Changes
- Matchmaker.tsx — open state lifted out; new exported MatchmakerTrigger sits in the toolbar row beside search and sort, where it costs zero vertical space. The panel (three fieldsets, canSubmit, AC-8 never-fabricate-a-winner, URL round-trip) is untouched and mounts only once opened, never unmounts after — so "Change my answers" still lands on the form.
- pages/index.tsx — hero padding/h1 trimmed, pitch paragraph cut to two lines, trust pills moved down into "What you get for £49"; heading and Heartbeat share one row with the survivorship ratio folded into the pill (the duplicate success-coloured pill deleted).
- pages/index.tsx:499,501 — the "four documents" drift you'd have hit next: now ${PACK_CONTENTS.length}, and launch copy added to the assets row.
- e2e/discovery.spec.ts — new test asserts fold - box.y > 40, i.e. 40px of card actually visible, not merely y < 720 which a 1px sliver satisfies. The router test clicks the trigger first.

Verdicts
- npx tsc --noEmit → exit 0
- npx vitest run → 6 files, 124 passed
- prove_web.sh (real API + next build) → 11 passed, 1 skipped, 2 failed; first card now at y=651 (was 1094)

The 2 failures are stale local data, not code: sqlite3 store.db shows IsListed=1 for 54f775d91cbe09d8 and f7783abea10a4216 — the two packs quarantined in production for the DeepSeek moat breach. The local dev snapshot predates that withdrawal; nothing this session touched listing state.

Two live-catalog writes still need your explicit go-ahead before I run them: backfill_facets.py --apply (G2, 13 facet values already resolved with evidence) and the a03a2ba029b408a7 bundle repair (G4, and it must wait for pid 43521 to release store/.backfill_listings.lock).

Remaining: G3, G6, G5, G7. Handoff written to checkpoints/LATEST.md. ok get the rest done, ad we need to go faster
