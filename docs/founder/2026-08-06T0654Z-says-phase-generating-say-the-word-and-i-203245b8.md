---
captured: 2026-08-06T06:54:36+00:00
session: 37a7db29-4849-4e4e-804e-2c1fabb470c8
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2702
source: founder prompt, verbatim (founder-doc-capture.py)
---

says phase=generating) — say the word and I'll do it, or it can wait.

2. n=20 re-measurement — running

Launched detached (pid 9405, SAMPLE_N=20, population 126). Nothing completed yet at 3 min; the previous run averaged ~4 min/item because it contends with the daemon and the storefront session for CLI slots, so expect 40–80 min. I'll report when it lands.

3. The choice: backfill — and the decision is now forced

S2 is already being built by another session in this checkout, right now. prospector/bridge.py, store.py, models.py and tools/backfill_audience.py were all modified in the last 20 minutes, and dossiers.audience appeared in the SQLite index during this session — absent from my PRAGMA at 06:40, present now with 1,419/1,625 rows populated. Starting S2 would be a collision.

The backfill also earns it on its own evidence. The live catalogue is mostly running the deterministic floor, not real copy:

┌────────────────────────────────────────────────┬───────┐
│          live check (re-fetched now)           │ value │
├────────────────────────────────────────────────┼───────┤
│ live packs                                     │ 61    │
├────────────────────────────────────────────────┼───────┤
│ clean passes live, lacking a real listing_page │ 45/61 │
├────────────────────────────────────────────────┼───────┤
│ headline == title                              │ 34/61 │
├────────────────────────────────────────────────┼───────┤
│ cardLine populated                             │ 6/61  │
├────────────────────────────────────────────────┼───────┤
│ proofPoint starting with a gate name           │ 28/61 │
└────────────────────────────────────────────────┴───────┘

That is the exact signature of pack_floors.claim_safe_marketing — headline = title[:140], no card_line at all, proof_point = bullets[0] (a raw check rationale): prospector/pack_floors.py:71-90. The floor fires whenever listing_page was dropped, which is the bug S1 fixed. So 74% of what customers see today is degraded copy that S1 makes recoverable.

Only 16 clean passes aren't live (14 lacking copy) — this is a copy upgrade job, not new supply.

One hazard to settle before anything touches prod: publish_pass re-runs price_for (bridge.py:515) and mints a fresh provider price (bridge.py:570-576) on every publish. Re-publishing a live pack is therefore a money-rail event, and per the recorded failure mode a price move both charges and refuses delivery. The backfill must go via the copy-only route (PATCH /internal/catalog/{id}/content, the pattern in tools/backfill_bundle_html.py:200,268) with a price-invariance assertion — not tools/backfill_missing_listings.sh, which publishes.
 ned to adress carefully
