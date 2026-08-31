---
captured: 2026-08-06T01:20:38+00:00
session: cbd294d8-015f-49ba-b74b-ccbcfbedeed6
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2669
source: founder prompt, verbatim (founder-doc-capture.py)
---

ok letss do this first and then next steps 
1. Prospector generates four marketing pieces per pack. Only listing_page reaches the storefront — it supplies cardLine, headline, subhead, whatYouGet. Across 258 non-KILL dossiers it survives 18 times (7%), the worst of the four despite getting an extra repair attempt (artifacts.py:452).
2. Root cause is mechanical, not a quality problem: _listing_check_text joins all eight+ fields into one blob (artifacts.py:435-438), takes one claim-check verdict, and a single violation anywhere returns None for the whole piece (artifacts.py:461-469, 479-480). At 90% per-string cleanliness, eight strings clear together ~43% of the time. The truth standard is right; the granularity is wrong.
3. So publish falls back to raw internals. Live on api.mumchimp.com/catalog, n=61: cardLine 6/61, headline byte-identical to title 34/61, market 24/61, timeToFirstRevenue 0/61, and 28/61 proof points literally begin value durability: or buyer intent: — your internal gate vocabulary, printed to customers.
4. Titles are never rewritten for sale (bridge.py:640). Median 77 chars, max 176. 8/61 carry a benefit clause; 34/61 use the same "The ⟨persona⟩'s ⟨noun⟩" construction.

On personas — you're further along than you think, and the gap is precise. Eight audiences are already injected into every generation (generate.py:172-219) and populated on 395/400 sampled dossiers. But selection is deterministic hash rotation (generate.py:467-472) — a diversity axis, never a targeting decision, with no feedback. It appears in none of the 22 catalogue fields and is absent from the SQLite index. The dossiers.persona column is a different concept entirely (analyst persona — shark/minimalist) and is empty on 1,600 of 1,601 rows. Worth fixing the naming before any code lands.

And adaptive.py is a live closed learning loop (run.py:537-564) — exploration level, exemplars, fertile-cell boosting. Its reward is gate survival. Nothing in it has ever seen a sale.

Two constraints that shaped the design rather than decorating it: variants must be minted after PASS, because dedup fingerprints on title + one_liner at 0.85/0.34 (dedup.py:54-78) and title variants are near-duplicates by construction. And the storefront already has beacons, an events table, and a 3-way sticky A/B mechanism (useCopyVariant.ts) — hand-authored, site-wide, with nothing reading outcomes back. Plumbing exists; loop was never closed.

My recommendation: S1 alone, proven, before designing further. Per-field claim check. No ML, no schema change, no storefront work — and it converts the ~240 dossiers already on disk without listing copy into an immediate backfill.
