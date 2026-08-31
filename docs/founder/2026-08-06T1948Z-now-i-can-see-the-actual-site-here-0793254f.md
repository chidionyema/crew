---
captured: 2026-08-06T19:48:13+00:00
session: 266e9014-edbd-4473-8cf5-9315db9161f5
cwd: /Users/chidionyema/Documents/code/prospector
chars: 7080
source: founder prompt, verbatim (founder-doc-capture.py)
---

Now I can see the actual site. Here's my real design critique of every page and section visible in your screenshots.
1.  Homepage / Catalogue Feed
What's working:
•  Clean, confident minimalism. The white space, single-column card stack, and bold sans-serif typography give it an editorial, no-nonsense feel that matches the "zero fluff" brand promise.
•  Card hierarchy is clear. Price → Title → Description → CTA reads in the right order. The £49/£29 is bold and scannable.
•  Category pills with icons ("Housing and tenancy", "Care and benefits claims") are a nice touch — they add color coding and quick context without clutter.
•  "Based on your browsing" with green checkmarks is a smart trust signal. It makes the site feel alive and personalized.
What's not working:
•  The watermark letters (HA, SE) are cryptic. In the first card, "HA" floats in the header area. In the second, "SE". Are these initials? Random decoration? They don't map to anything the user understands and look like placeholder art. Either make them meaningful (e.g., category abbreviations with a legend) or remove them.
•  The card header backgrounds waste prime real estate. The top 30% of each card is a tinted block with a giant icon or letter. On mobile, that's a lot of thumb-scroll distance spent on decoration instead of information. The "Housing and tenancy" card has a house icon watermark that's so light it's barely visible — it's neither beautiful nor informative.
•  "The rest of the catalogue, newest first" is a weak section header. It sounds apologetic. "Newest survivors" (further down) is much better copy — use that voice everywhere.
•  Price inconsistency is visually jarring. £49 then £29 then £29 then £49 with no visual explanation. The user has to infer why one pack costs more. A small micro-label like "Starter" vs "Full" or a tooltip would fix this.
----
2.  "Based on Your Browsing" Section
What's working:
•  The green checkmark icon is a nice semantic choice — "these are verified/good."
•  Source count ("28 sources") adds credibility.
What's not working:
•  These items get a worse treatment than catalogue cards. They're plain text rows with no card container, no imagery, and a much smaller tap target. If the algorithm thinks these are relevant, they should get better treatment, not worse.
•  The truncation is aggressive. "UV strips plus a paper log for gel ..." and "Sells California shops a kit to fix A..." — the ellipses cut off before the value proposition lands. The card format below shows you can fit more text; use it.
•  No CTA on these rows. I can't tap to view the pack directly from here? That seems like a conversion leak.
----
3.  Pack Cards (Individual)
What's working:
•  The black "View pack →" button is a strong, consistent CTA. The arrow suggests forward motion. Good.
•  Category pills (the rounded tag with icon + label) are well-executed. The blue for housing and mint-green for care create a loose color system.
•  Price and CTA are right-aligned together — smart grouping of "cost" and "action."
What's not working:
•  No preview of the deliverable. For a digital research product, the card shows me nothing of what I'm buying. Not a blurred screenshot, not a page count, not a "includes 8 documents" badge. The user is buying blind.
•  The description text gets truncated awkwardly. "A no-app, no-subscription fridge sensor that auto-prints a pre-formatte..." — the word break is ugly. Consider slightly smaller font size or two-line clamping with better CSS.
•  The header iconography is inconsistent. Some cards have letters (HA, SE), some have icons (house, handshake). Pick one system. If you're using icons, make them category-specific and recognizable. The handshake for "Care and benefits claims" is a stretch.
----
4.  Navigation / Hamburger Menu
What's working:
•  Clean two-column layout (Store/Content on left, Legal on right) is organized.
•  "Kill log" and "Who makes this" in the main nav reinforce the brand's transparency and personality.
What's not working:
•  The email address is broken across lines: support@mumchimp. / com. This is a classic responsive text-wrap bug. Use white-space: nowrap or a <wbr>/soft hyphen. It looks unprofessional.
•  "Store" and "Catalogue" are redundant. If I'm on the homepage, I see the catalogue. Do I need both? "Store" might imply a different experience.
•  No visual hierarchy in the menu. "Kill log" (a unique brand page) and "Terms of Service" (boring legal) have the same weight. The legal links could be smaller, greyer, or in a collapsed sub-section.
•  The hamburger icon itself is fine, but there's no "X" close state shown. Standard pattern, but worth checking if the close animation feels native.
•  Missing: Search. With 63 packs, a search icon in the header would be more useful than the hamburger alone.
----
5.  Footer / Legal Disclaimer
What's working:
•  The disclaimer is human-readable. "Mumchimp packs are digital research products sold for information only..." — clear, not buried in legalese.
•  "Payments are processed securely by Stripe" is a good trust signal at the point of purchase anxiety.
What's not working:
•  The footer is very tall for mobile. The disclaimer paragraph is long and unstyled. Consider collapsing it behind a "Read disclaimer" link, or at least reducing the font size and line-height.
•  No secondary CTAs at the bottom. I've scrolled through the whole catalogue and there's no "Not sure? Browse the kill log" or "Get notified of new packs" prompt. The scroll just ends.
----
6.  Global / System-Level Issues
Issue    Severity    Notes
No search    High    63 packs is enough that browsing becomes tedious. A search bar in the header would help.
No filter chips    Medium    I see "Newest" dropdown, but no category filters. The pills exist on cards — why not let me filter by them?
Typography scale    Low    Everything is bold or regular. No intermediate weights for metadata ("28 sources · £29"). It all competes for attention.
Color palette    Medium    The tinted card headers (light blue, light mint) are pleasant but arbitrary. They don't map to a broader system the user can learn.
No empty state / onboarding    Medium    First-time visitors see "Based on your browsing" with... nothing? Or generic picks? An empty state explaining how browsing works would help.
No "purchased" or "viewed" state    Low    If I come back, there's no visual indication of which packs I've already looked at.
----
Top 3 Fixes
1.  Replace the cryptic watermark letters with actual pack previews. Even a small thumbnail of the Executive Summary or a "Pages: 12 · Sources: 28" metadata row would be more useful than "HA" floating in space.
2.  Fix the menu email wrap and demote legal links. support@mumchimp.com should never break. Legal links should be smaller/greyed so "Kill log" and "Who makes this" stand out.
3.  Add a search bar and category filters. At 63 packs, the catalogue is too big to scroll. A sticky search/filter bar would transform the UX from "browse and hope" to "find my niche." i suspect a lot of the work is done but verify
