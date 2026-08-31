---
captured: 2026-08-14T09:50:15+00:00
session: 0c5421cf-3f28-415a-99ac-a6381ae54271
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4099
source: founder prompt, verbatim (founder-doc-capture.py)
---

update fron aother agent You switched generation off at 09:38 today because the packs aren't sellable. That was right, and I was working the wrong thing: I spent this session trying to make more ideas pass, when the decided problem is what the buyer receives. That's the looping you're feeling.

So I stopped and measured. I pulled all 62 live packs from the real store (not from this laptop — the local copies are stale) and counted each fault you listed. Two faults are in 62/62. Five more are in 46–52 of 62. None of this is "fix a bad pack". It's the generator, and everything on sale is affected.

---
What a buyer gets today, counted

tools/pack_defect_census.py (new, read-only, reads the same bytes the buyer downloads) → receipt at tools/experiments/pack_defect_census_receipts.json:

┌──────────────────────────────────────────────────────────────────┬───────┬─────────────────┐
│                      Fault, in plain words                       │ Packs │    Certain?     │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ The pack's ID field prints blank                                 │ 62/62 │ proven          │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ It's eight markdown files in a zip — no designed document        │ 62/62 │ proven          │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ Sentences cut off mid-word                                       │ 62/62 │ pattern-matched │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ "Sources used:" prints , , , , — commas, no sources              │ 52/62 │ proven          │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ Buyer is shown our internal judge chain (fallback(cursor_cli+…)) │ 52/62 │ proven          │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ Whole sentences repeated across three documents                  │ 51/62 │ proven          │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ Cites a Pinterest board / YouTube / blog as evidence             │ 46/62 │ proven          │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ Financial model ships "(not specified)"                          │ 20/62 │ proven          │
├──────────────────────────────────────────────────────────────────┼───────┼─────────────────┤
│ Prints "cleared every check" next to a check that failed         │ 11/62 │ proven          │
└──────────────────────────────────────────────────────────────────┴───────┴─────────────────┘

The two "62/62 proven" rows and the blank-sources row are one and the same bug: the renderer throws away anything the generator wrapped in backticks. One fix, three symptoms, most visible thing in the product.

What I'd do, in order (estimates, not measurements)

1. The renderer bug — blank ID + empty sources + cut-off text. ~1 day. Cheapest, most visible.
2. Kill the markdown zip — one typeset PDF + a one-page "first fortnight" card. This is the "50x" and the big one. ~1 week.
3. Source quality rule — a primary source must beat a blog restating it; refuse mood boards and videos as evidence. ~2 days.
4. Stop selling the same 2,500 words three times — one shared evidence document the three plans point at. Folds into (2).
5. Financial model — compute it properly for a one-off product, or drop it from the eight rather than ship an empty document.
6. Then re-publish all 62 from the fixed generator, then turn generation back on.

The one decision I'm taking rather than asking you: on the 11 packs that claim "cleared every check" next to a failed check, I'll print the truth instead — "passed 6 of 8; two came back against it, here's why we still list it" — rather than deleting those packs. Deleting culls the catalogue by an amount nobody has measured. Say the word and I'll flip it the other way.
