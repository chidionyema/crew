---
captured: 2026-08-21T19:13:08+00:00
session: ded7ec0f-e49a-4adc-b8ad-afd818263430
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3026
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are a ruthless, evidence-bound analyst. Rule ONLY from the passage
provided. No prior knowledge. If the passage does not address the claim, verdict
is "unverifiable". NEVER "supported" without a passage that directly supports it.
Cite the source_ids you relied on. Confident wrongness is the worst outcome.

VERDICT AXIOM:
  "supported"    = the passage AFFIRMS the claim.
  "refuted"      = the passage NEGATES the claim.
  "unverifiable" = the passage does not address the claim.

A claim is "supported" when it follows from the passage as a safe human
deduction. Do not demand that the passage restate the claim word for word.
A claim is "refuted" when the passage states something that makes the claim
false, even if the passage "confirms" some other fact along the way.

Return ONLY valid JSON. No prose, no code fences.

Claim: Be aware of eBay's fees and factor them into your pricing (Passage 3).

Passages:
[s0176] {'question': 'how do i sell stuff on ebay', 'passages': "passage 1:Basics. Getting started selling on eBay Set up your seller account, and then create and manage your listing. Using the quick listing tool The quick listing tool helps you get your item up for sale quickly by providing guidance on how to price and ship your item.elling with a reserve price Learn how to set a minimum or reserve price on your item. [ more… ]. Selling multiple items Find out how to sell multiple items. Selling Get It Fast items Get quick sales when you give buyers the option to receive your item within one business day.\n\npassage 2:Many old items can be worth serious cash. But to really get the eBay cash rolling in, you need to know the etiquette and shortcuts. This is a crash course on how to sell. It explains how to cut fees, the best time to close auctions, profit from bizarre items you never thought you'd sell and more.any old items can be worth serious cash. But to really get the eBay cash rolling in, you need to know the etiquette and shortcuts. This is a crash course on how to sell. It explains how to cut fees, the best time to close auctions, profit from bizarre items you never thought you'd sell and more.\n\npassage 3:1 For example, if you're selling an iPod, put  MP3 player  in your title. 2  However, eBay's search will automatically account for variant phrasings; it will also sometimes check category names in addition to the auction title. 3  Do a search on specific terms and look at the titles of the auctions that come up.et your price according to how much you paid for the item, your time, eBay fees, and how much it costs to ship. Remember that once someone buys an item from you or the auction ends, it constitutes a binding agreement to sell, and it is difficult to get past this unless both parties agree to cancel the sale.\n\n"}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
