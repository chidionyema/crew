---
captured: 2026-08-15T15:24:08+00:00
session: 0c5421cf-3f28-415a-99ac-a6381ae54271
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2280
source: founder prompt, verbatim (founder-doc-capture.py)
---

and address the ui fi also All three are in the “A page from the free sample” section — the one whose H2 reads “9 documents. Here is one page of one of them.” Locators below are by visible copy so your agent can grep for them.

1. Horizontal overflow in the free-sample section (iPhone width, ~390px). Three things break the viewport edge: the H2 “9 documents. Here is one page of one of them.” loses the end of line 1; the bordered preview card below the “8 checks · 8 sources · 5,000+ words” meta line has its right border off-screen; and the italic pull quote further down (“The homeowner can hire a structural engineer (e.g., £500-1000 per inspection)…”) runs past the right edge on every line. The whole document scrolls sideways. Likely a fixed px width or min-width on the preview card and blockquote, or a non-wrapping child inside them.

2. The floating “Narrow it down” search pill overlaps body copy. It’s the persistent pill with a magnifier icon and a “1” badge. It floats over whatever is behind it — in one scroll position it sits on top of the preview excerpt (”…that a route to market exists and is executable by businesses”), in another it covers a full line of the REFUTED explanation. It’s white with a hairline border and no shadow or backdrop blur, so it reads as a rendering artefact rather than a layer. Either dock it and reserve bottom padding on the page, or give it real elevation.

3. The preview card is a nested scroll region with a fade that cuts sentences dead. Inside the card (tabs “The Solo Builder’s…” / “Evidence and Constraints”), the content has its own scrollbar and a bottom gradient mask. The REFUTED text under “8 of 8 — Do its own claims hold up to checking?” fades out mid-clause on “…contradicting the hypothesis’s implicit claim that there”. Scroll-within-scroll is unreliable on touch, and there’s no expand affordance. Show N complete lines, end at a sentence boundary, let the CTA carry the rest.

Two smaller ones, same page: headings clip under the sticky header when scrolled to (fix with scroll-margin-top equal to header height) — visible on “one of them.” and on the “8 of 8” line; and there’s a ~300px empty gap between “Read the kill log →” and the “A page from the free sample” eyebrow that reads as a failed image load.
