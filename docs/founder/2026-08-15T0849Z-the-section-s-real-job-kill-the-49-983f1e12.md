---
captured: 2026-08-15T08:49:41+00:00
session: b750280e-3c05-4c33-8647-b5fd6f756487
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2453
source: founder prompt, verbatim (founder-doc-capture.py)
---

The section's real job: kill the "£49 for a two-page Google Doc" fear. Nine titles with a sentence under each can't do that — a list of nouns is a claim about contents; a page you can read is evidence.

The one move, four lenses agreeing: show a single real page from the free sample, cropped by its own frame, sheets stacked behind it — and make the page we show the one with the failed check on it.

---
Psych — why the failed check is the whole trick

Eight green ticks read as marketing. One refuted reads as a document. sample-report.json:146 has claims_verifiable: "refuted" sitting in the free sample already — nobody fabricates a flaw in their own product, so it is the cheapest credibility we will ever buy. Second lever, same file, premortem.strongestAlternative (:20): "a structural engineer, £500–1000 per inspection". That is a price anchor written by the engine, cited, sitting unused 6,000px from a £49 button.

Designer — the object, not the inventory

One artefact, big, cropped so the eye reads "this continues"; a full small preview says "this is all there is". Paper ground, running head, page number, real margins, the site's own type at document scale — the typography is the proof. Two sheets offset behind give the count without printing a number. The nine-row tree survives as one quiet line underneath, not as the hero.

Marketing — sell the argument, not the file list

The differentiator is not nine documents; it is that the pack argues against itself and publishes the source either way. Headline the transformation, and put the zero-risk step next to the paid one: "Read this exact pack, free." They meet the product before the price.

UX — where it fails in practice

Two hazards: the section sits at pages/index.tsx:2379, ~6,000px down, so most buyers never reach it — the specimen wants a compressed twin near the shelf. And on mobile the crop must still show three real rows above the fade or it reads as a decorative box. No accordion: progressive disclosure has already made guard tests vacuous on this site once.

Build order: PackSpecimen.tsx from sample-report.json (static import, every line real) → replaces the hero role of PackContentsSection, which demotes to a one-line manifest.

Handoff written to checkpoints/LATEST.md — PR #199, the specimen spec, and the unfixed orphan ( in kill-log.json are all in it.

Safe point — type /clear (state saved, nothing will be lost). ok get it done quickly, no ui tests
