---
captured: 2026-08-08T14:10:49+00:00
session: 2bf08fb4-0d81-401d-a212-bf7cdeff2bfa
cwd: /Users/chidionyema/Documents/code/prospector
chars: 3386
source: founder prompt, verbatim (founder-doc-capture.py)
---

1. The em-dash unlisting was a false unlist. Receipts: store/dossiers/13d41ccee9e96e2d.lint.json and 3e72d5a5f1a60068.lint.json each carry exactly one error, house_dashes | headline, and the offending text is the pack title. That same title passed the same check as title — because bridge.py:832 normalises it — and failed as headline because bridge.py:544 did not. Meanwhile the value that actually ships is normalised at bridge.py:1330, and the control confirms it: 0 of 71 written listings contain a house dash in headline. Two packs were held off the shelf for a defect that does not exist in what a buyer receives.

Fixed by moving the rule into _card_field (bridge.py:57), the single boundary every one-line catalogue field passes through — before the [:140] slice, so the slice counts the characters that ship. The later choke point stays as the backstop; nodash is idempotent.

One trap I had to design around: check_truncation decides a mid-word cut with source.startswith(final). Normalising only the rendered half wouldn't make it wrong, it would make it vacuous — a genuinely mid-word slice would pass in silence. So both halves move together (bridge.py:819-827), and there's a test pinning exactly that vacuity as the shape not to ship.

2. The Stripe idempotency failure was a real dead end, and safe to fix. The product key was prospector-product-<pack_id> with no parameter fingerprint, while create_price has always keyed on (product, amount, currency). A Stripe key replayed inside 24h with different parameters is a hard error — and name/description are the pack's copy, so our copy fix made those packs permanently unprovisionable. Before changing it I checked whether the burned key had left an orphan: Product.search on metadata['pack_id'] returns 0 products for both 13795bea31feee47 and 2abc23c3c0d05bab, so minting under a fresh key creates nothing duplicate. The retry property is preserved — identical request, identical key — and publish_pass:706 only reaches this call when the catalogue holds no product id.

3. The dead citation URLs are genuinely dead — the linter is right. https://www.oconnors.law/people/kathryn-howard/ returns 404 on HEAD and GET, with both a default and a browser User-Agent. I also checked whether the doubled path in blog.factorfunding.com/blog/blog/... was a systemic URL-joining bug: 64 of 6,253 URLs match that shape and most are legitimate gov.uk /publications/<slug>/<slug> attachment pages, so it isn't. The single-/blog/ variant does return 200, but auto-repairing a citation into a different URL is not something I'll do on a source-or-die storefront — that is silently re-pointing evidence. Those two packs need their citations re-grounded, which costs model calls; I haven't done it.

Tests green:

tests/unit/test_bridge_house_dash_and_idempotency.py   8 passed
bridge / lint / publish / truncation suites          239 passed

Republish is at 23/42 written, 19 rail reuses, 0 rail moves. I'll let it finish before committing — a POPDD pytest run alongside it would contend for the same cores and the gate has already died twice that way. Once it's done I'll commit these two fixes and re-run the four packs that this unblocks: the two dash-unlisted and, now that the key includes a fingerprint, the two that could not provision.

✻ Worked for 11m 34s · 2 shells still running joinging bug needs fiing and pack fied also
