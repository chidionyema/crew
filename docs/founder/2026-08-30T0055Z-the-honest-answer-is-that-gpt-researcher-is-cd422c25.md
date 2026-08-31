---
captured: 2026-08-30T00:55:59+00:00
session: 14ed6c8b-f0a9-40d7-82a8-895f336f9b78
cwd: /Users/chidionyema/dev/code/.wt-tone-audit/store_platform/src/Store.Web
chars: 1868
source: founder prompt, verbatim (founder-doc-capture.py)
---

The honest answer is that GPT Researcher is still the reasonable default and the alternatives solve different problems rather than doing the same job better.

It's Apache-2.0, around 28,900 stars, and still actively maintained as of mid-July 2026, which matters because it predates the vendor deep-research modes it now gets compared against. Its architecture is a clean three-role split: a planner turns the brief into research questions, execution agents crawl in parallel one per question, and a publisher aggregates. If you haven't already, report_type="deep" turns on recursive tree exploration with configurable breadth and depth, and report_source="hybrid" mixes web results with your own documents. Most people run it in its shallow default and conclude it's weak.

The three worth switching to, each for a specific reason:

Stanford STORM if you want structured article-style synthesis rather than a report answering a brief. It's a knowledge-curation system, and GPT Researcher actually cites STORM's paper as an influence on its own multi-agent workflow, so they're closer to cousins than competitors.

Local Deep Research if external API calls are the constraint and everything must stay on your own hardware.

Open Deep Research if you want a smaller codebase to modify rather than a framework to configure.

The thing that should actually decide it for you, given the last few hours: the 2026 "Cited but Not Verified" benchmark found open-source models scored lower on fact-check accuracy than frontier models. Self-hosting moves the citation-quality risk onto you. If you point any of these at a local model to save cost, you get a well-structured report with worse-verified claims, which is precisely the failure mode you spent tonight building a spec against. Run them against a frontier API rather than a local model, or you've automated the problem.
