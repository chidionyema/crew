---
captured: 2026-08-07T12:50:27+00:00
session: f49bfc3b-b4a6-46f7-a1ee-7eeaf8cb7a08
cwd: /Users/chidionyema/Documents/code/prospector
chars: 9606
source: founder prompt, verbatim (founder-doc-capture.py)
---

needs a todolist and we need to get all done fast and cheap, forget tests for now as the ui changes are volatile I can read your markup and copy but not the rendered pixels (no screenshot access), so this is critique of structure, hierarchy and system — which is where most of the gap sits anyway.

The core problem: 46 identical cards. Every pack has the same anatomy — category · “8 documents · N sources” · title · description · price. No visual hierarchy at all, so the eye has nothing to grab. Fix by breaking the uniform grid into an editorial one: one full-bleed hero pack, two mid-weight, the rest as compact rows. Let price tier drive visual weight — a £149 pack should physically occupy more space than a £29.

Kill the dead badge. “8 documents” on every single card is zero-information ink. The only varying number is sources. Replace it with a rendered evidence bar (source count as a physical bar) so scanning the grid actually tells you something.

Your best asset is buried. The filter log — ✕ ChargeBreak, killed by incumbency — is the most distinctive thing on the page and it’s three lines next to an email form. That’s the brand. Run it as an ambient, slowly-scrolling column of struck-through names behind the hero. 1,285 dead ideas is your visual, and it costs nothing to photograph.

On the “needs images” criticism — they’re right about the symptom, wrong about the cure. Stock photography would destroy this product’s credibility. What you want instead:

Generative per-pack marks — you already have hex IDs (939b559421982379). Hash them into deterministic patterns/gradients. Every pack gets a unique visual identity, none of it fake.
Data as ornament — kill/survive ratios, category distribution sparklines, the verification dossier rendered as an actual interactive object rather than a bulleted list.
The file manifest as artifact — 00_Executive_Summary.md, QA_Report.md shown as a real file tree or terminal listing. The .md extensions are an authenticity signal; render them like one.
Typography is where 2040 vs 2015 actually shows. Current structure implies one sans at three sizes. Go extreme: a tight-tracked display cut at 96px+ against 13px monospace for every piece of metadata, category, price and source count. Mono is your structural voice — it reads forensic, which is the product. Medium-everything is what dates a site.

Commit to a kill/survive palette. You have a built-in semantic colour system and you’re probably spending it on generic red/green. Pick one survival colour and one kill colour, then use them everywhere — filter chips, dossier verdicts, the log, pack borders. That’s brand identity for free.

Surface treatment. #0A0A0A + Tailwind borders is the 2024 default look. To move past it: elevation via 3–4 subtle background steps instead of borders, hairline 1px dividers only where structural, and 2–3% grain overlay to break the flat plane.

Motion. View Transitions API for card → pack page (shared-element morph) is well-supported now and instantly reads native-app rather than website. Scroll-linked reveal on the dossier checks landing one at a time would sell the verification story better than the paragraph currently doing it.

Two structural notes:

The same-8-documents message appears four times on this page. Copy repeats when sections aren’t visually distinct enough to be remembered — solve it in layout, then delete three of them.

The skills quiz (“Suits builders 23”, “1 of 3”) interrupts the catalogue mid-scroll. It’s a filter wearing a quiz costume. Move it into the filter rail or make it a deliberate full-viewport interstitial — not a stumble.

Lastly, your hero is text plus two buttons. Put the verification dossier up there. Seven Survived, one Pushed back, with live source domains — that’s the whole proposition in one glance, and it’s currently 80% down the page.



Can’t fetch the subpages — the tool only allows URLs that came back from a search, and the site’s too new to be indexed, so I’m locked to the homepage. What follows is built from what the homepage exposes about your design system, IA and content model. If you paste the HTML or screenshots for any page I’ll do the real per-pixel pass on it.

The root cause, before the pages

You have roughly two layout primitives — bordered card in a grid, and paragraph — and one type scale. Every page will therefore render as “homepage with different words.” Most of what follows is downstream of that. Before touching individual pages, define: four surface elevations (not borders), one survive colour and one kill colour used with total consistency, mono for all metadata, a display cut for headings, and a page-header pattern so pages announce themselves as different kinds of thing.



/ideas — Categories

Highest risk of being the homepage filter with a new URL. It needs a different visual mode entirely: a taxonomy map, not a link list. Mosaic tiles sized by pack count, each carrying price range, survival rate, and one representative kill from that category. Eleven categories is small enough to render as a single diagram that fits one screen. If a user can’t tell this page from the catalogue at a glance, delete it.

/how-it-works

The three-steps-with-icons trap is sitting right there. Your actual asset is the six fronts — pain reality, value durability, incumbency, payer solvency, distribution, legality. Build this page as a gauntlet: one real idea entering, each check firing in sequence, verdicts landing, most ideas dying. Scroll-driven, real data, real verdicts. This should be the showpiece page of the site and I’d bet it’s currently prose.

/kill-log

The single biggest unexploited asset you have. 1,285 records is a dataset, so build an instrument, not an article: dense monospace table, sortable by cause of death, filterable by category, with a distribution chart of causes at the top. Struck-through type. Brutal, sparse, scannable. Give every entry its own anchor so individual kills are linkable — that’s your share mechanic and your SEO surface. Done right this page does more brand work than the homepage.

/pack/[id] — the product page

Commercially the most important page on the site, and two things in the card copy worry me:

Your titles have inconsistent grammar. Some are product brands (PackProof, Kerb Cut, DustHalt Hold), some are verb phrases (Reviews your telematics data after a policy cancellation), some are descriptive labels (Data report on HMRC IHT valuation settlements). Pick one convention. Mixed naming reads as unfinished, not varied.

Some descriptions run 60+ words in a card slot. Truncation with “…” mid-sentence is visible in your own markup. Write a hard 20-word card line separate from the full description.

Page structure: verification dossier as hero, the 8-document manifest as a file tree, price justification inline where the price is (not on a separate /pricing page), a visible sample excerpt, sticky buy rail on desktop and sticky bottom bar on mobile, generative mark from the pack hash, and sibling packs from the same category at the foot.

/sample

Your highest-leverage conversion page. It should feel like a reading application, not a web page — document sidebar with the 8 files, in-document nav, source citations as footnote chips that reveal the domain on hover, sticky “packs like this from £29” rail. The bar here is Stripe or Linear docs. If it’s a rendered markdown dump you’re wasting the strongest thing you offer.

/pricing

The whole page is one idea: price follows opportunity size, not document count. Draw it. A ladder of £29 / £49 / £79 / £99 / £149 with the specific criteria that place a pack in each tier, or a plot of price against opportunity size using your real catalogue. One diagram lets you delete that paragraph from the four other places it currently appears.

/about

Chidi, this is the best copy on your site by a distance — the bit about talking yourself out of ideas. It’s currently a paragraph wedged between badges and a CTA. Give it a full page in large type, single column, generous measure, with a real photo or a strong personal mark. Put “1,285 killed” here as evidence of temperament rather than as a marketing stat. This page is why someone trusts the engine.

/account

Nobody polishes the post-purchase surface and it’s exactly where trust decays. Purchased packs as a library shelf with the generative marks, permanent re-download, visible receipts. The empty state should sell the catalogue rather than say “no orders.”

/faq

Group it — Before you buy / What’s in a pack / Refunds / How the engine works — and make it searchable. Answers should link into how-it-works and pricing rather than restating them, or you get a fourth copy of the same paragraph.

/terms, /privacy, /refund

Legal pages are a disproportionate polish signal because almost nobody styles them. Same type scale and measure as the rest of the site, a sticky table-of-contents rail, a visible last-updated date. Costs an hour, reads as institutional.



Cross-page

Your catalogue is the homepage, so “Catalogue” in the nav and the logo both point to /. Give the catalogue its own route — you need a canonical URL for filtered states anyway. Nav needs a visible active state. Footer currently duplicates nav verbatim; make it a different kind of thing (contact, legal, one line of positioning). And your wordmark renders duplicated alt text — MumchimpMumchimp — which is a small accessibility bug that appears on every page.

Send me the HTML or screenshots for whichever pages matter most and I’ll go properly deep on those.


 focus on quick lauch and beig thorough
