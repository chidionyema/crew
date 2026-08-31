---
captured: 2026-08-07T21:06:16+00:00
session: 90a3f90b-279b-4a51-b04c-0589f4fb4bb5
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4060
source: founder prompt, verbatim (founder-doc-capture.py)
---

and the rest? the provious agent should have done a lot of work 

P0 and P1 are complete. Final state:

┌─────────┬───────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────┐
│    §    │                       Item                        │                                   Receipt                                    │
├─────────┼───────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 1       │ Numbers from one source                           │ Every remaining 1285/1331/1412/1168/… hit is a code comment or a pixel value │
├─────────┼───────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 2       │ Publish pass                                      │ 400 entries × 4 fields: all five defect classes 0; 78 tests pass             │
├─────────┼───────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 5.2     │ Vocabulary                                        │ catalog(US)/shot/grounded/gauntlet/dossier all 0                             │
├─────────┼───────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 5.3     │ Say it once                                       │ Manifest on Home only; /pricing bare filenames; pack page its own            │
├─────────┼───────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────┤
│ 6.1–6.6 │ Home, how-it-works, about, pricing, faq, kill-log │ tsc 0                                                                        │
└─────────┴───────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────┘

Three things worth your attention.

1. I found a live defect the green suite hid. The publish pass was shipped and passing, and the kill log still published "with a low confidence (0.43)". Every confidence rule demanded the digits sit adjacent to the word, so a single ( slipped past all five. The defect class was closed; one spelling of it wasn't. Fixed at the pass, pinned with four non-firing guards, data regenerated. The lesson is in the doc: re-run the four-field scan over all 400 entries after any pass change, because the suite alone did not catch this.

2. The context loss has a mechanical cause, now fixed. The spec lived only in a chat transcript — the previous handoff literally told the next session to go read a .jsonl. It's now docs/SITE_SPEC_PROGRAM.md, versioned with the code, with a ledger where every ✅ names the command that proves it, and CLAUDE.md:7-12 routes to it as the third tracked programme. Status stops being prose.

3. Parallelism cost us something, and you should know how. Two agents ran concurrently on index.tsx, each told to remove the duplicated pack-contents section. Home had two; each deleted a different one; both reported success and tsc passed — and the manifest ended up on no page. Your call restored it to Home. The rule I've written down: name the survivor by file:line, never the duplicate, and never run two agents against one file in one pass. That's the collaboration fix with teeth — it's saved as memory, not just noted here.

Remaining: §3/§4/§7, the entire P2 design system. tokens.css does not exist; that's the visual rebuild and it's untouched. Also open: kill-log taxonomy viz (§6.6), intent search (§6.7), and FOUNDER.bio duplicating the /about story.

Per your instruction I ran no UI/e2e tests. Be aware the sample-CTA, pack-contents and checks-strip changes moved selectors, so those suites will fail on stale selectors — not regressions, but they need a pass before they mean anything again. Nothing is committed or staged.

Safe point — type /clear (state saved, nothing will be lost). address the issues rised paralellisn also
