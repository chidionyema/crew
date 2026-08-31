---
captured: 2026-08-16T15:25:06+00:00
session: 0c5421cf-3f28-415a-99ac-a6381ae54271
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2698
source: founder prompt, verbatim (founder-doc-capture.py)
---

also First, a free win before any algorithm: your <title> is better than your <h1>. “Business ideas that survived a filter built to kill them” has an actor, a verb, and tension. “Business ideas with the research already done” is a noun phrase with the verb amputated. You’ve already written the newspaper headline — it’s just in the wrong slot.

The objective mismatch you need to price in

Newspaper headlines optimise for click in a feed where the reader has zero prior intent and the article is the product. Your H1 optimises for “am I in the right place, and do I believe this” ahead of a £49.99 payment. Curiosity-gap forms transfer badly across that line — they raise clicks and lower purchase, because the gap gets paid off by a checkout page rather than by prose.

What does transfer, and is worth mining:

Verb-first construction. Nearly all your 64 pack titles are noun stacks: “Abandoned-vendor alerts for UK software operations managers.” No actor, no verb, no event. A sub-editor writes “Councils refuse Blue Badges. This reverses it.”
The number in the headline, not the metadata. You have “42 cited sources”, “13× the price back” sitting beside the title instead of inside it.
Head + standfirst as a pair. This is the real prize. Your card copy is currently one undifferentiated 30-word lump doing both jobs badly.
Anglo-Saxon over Latinate. Papers do this reflexively; it’s also the single strongest lever on your “sounds like an LLM” problem.
The algorithm, honestly

A newspaper corpus has no conversion label. There’s no y-variable in it, so you can’t rank forms against your objective — you can only extract a grammar. So split it:

Generator from newspapers: parse ~2,000 headlines, extract structural templates (actor-verb-object, number-lead, contrast pair, imperative), plus measurable features — word count, syllables, verb position, concrete noun ratio, withholds-vs-discloses. Output is a constrained candidate space, not a winner.
Selector from your own traffic. This is the only source of truth about your buyer.
Where you actually have statistical power

Not the H1. One page, pre-launch traffic, purchase as the outcome — you’d need thousands of conversions to separate two headlines. You’d be reading noise for months.

The pack titles are the opposite: 64 items, every catalogue impression is a trial, and click-to-pack-page is a fast intermediate signal. Run it as a multi-armed bandit over title variants generated from your templates, measure card CTR, and let the winning structural features — not the winning strings — propagate up to the H1. That’s how you get an algorithmic answer with the traffic you actually have.

 needs analysis an pipeline integration
