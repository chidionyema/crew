---
captured: 2026-08-08T19:12:20+00:00
session: da21cd3a-d3e7-47ad-9d96-1739d3f58a9b
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2512
source: founder prompt, verbatim (founder-doc-capture.py)
---

Fixed and verified, and I stopped there rather than burning credits on the rest.

Shipped — index.tsx:1825-1839 deleted. From 640px up, the page stated one fact twice, ~14px apart, under the same <h2>What survived</h2>, both linking "Why prices differ" to /pricing. Kept :1107 because SITE_SPEC_PROGRAM.md §6.1 pins its exact wording. Gates in one run: tsc=0, vitest 57 files / 829 tests passed, lint=0, build=0.

Also fixed — your repo had core.bare = true, which made every git command die with "must be run in a work tree". .git was touched at 19:57, during this session, so suspect a concurrent session or a stray worktree call. Restored with git config core.bare false. Worth watching in case it returns.

What the audit found before I stopped (production, 6 viewports, via your own scripts/design-audit/audit.mjs):

┌──────┬────────┬────────────────┐
│  vp  │  LCP   │ contrast fails │
├──────┼────────┼────────────────┤
│ 360  │ 804ms  │ 80/267         │
├──────┼────────┼────────────────┤
│ 1440 │ 4964ms │ 207/412        │
├──────┼────────┼────────────────┤
│ 2560 │ 4672ms │ 207/412        │
└──────┴────────┴────────────────┘

Desktop LCP is 5-7× worse than mobile against a 1200ms bar. It was never caught because measure-lcp.mjs:96 runs only at 360×780 and playwright.config.ts:18 runs only at 1280 with no perf assertion — each instrument covers the other's blind spot. I have not identified the element, so I have no fix to propose, only the measurement.

The other unlogged one: HeroEvidenceStrip is hidden md:block and the featured pack hidden lg:block, so a phone gets no evidence above the fold at all — visible in home-360-fold.png, and confirmed by the heading list (no "New this week", no "Newest survivors" at ≤390).

I withdrew one finding on inspection: the 240s animation is deliberate, documented at globals.css:199.

Not done: the user story. It needs the desktop LCP element identified first — otherwise its acceptance criteria would be guesses, and your bar is "objectively better", the same bar PR 134 failed. Everything is in checkpoints/LATEST.md with exact next steps, so a fresh session picks up without re-measuring.

Two notes: the audit PNGs are in the session scratchpad and will be garbage-collected — re-run the harness to regenerate. And your Chrome MCP extension is installed in Profile 1 only, not Default; that's why the browser tools failed.

Safe point — type /clear (state saved, nothing will be lost).

✻ Cogitated for 5m 34s fi the user story quickly and cheaply
