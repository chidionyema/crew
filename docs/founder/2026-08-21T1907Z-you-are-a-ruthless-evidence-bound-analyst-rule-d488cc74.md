---
captured: 2026-08-21T19:07:45+00:00
session: 49aa0f99-892f-4a02-ab07-8fc3117a2a66
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 5182
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

Claim: Pippa, 31, looked glamorous in a tweedy skirt, black blouse and cropped blazer. Accessorised with £ 159 black pumps by Jemima Vine and oversized sunglasses. Just last week, Pippa was glowing in a tailored plum dress at Spectator's annual party.

Passages:
[s0165] It was recently revealed that she will be designing a dress for charity and Pippa Middleton proved she knows a thing or two about fashion as she stepped out in a chic ensemble in London on Thursday. . The 31-year-old sister of the Duchess of Cambridge looked glamorous as she strolled through the sunny streets of London. Pippa looked as chic as ever in a tweedy skirt, black blouse and cropped black blazer. The brunette writer accessorised her look with a black tote, £159 black pumps by Jemima Vine and oversized sunglasses. Scroll down for video . Pippa Middleton looked glamorous as she strolled through the sunny streets of London on Thursday. Just last week, Pippa was positively glowing in a tailored plum dress at the Spectator's annual party at Belgraves Hotel in London, on Tuesday night. The 31-year-old, who is a regular columnist for the weekly cultural and political magazine, appeared relaxed and happy at the event. Pippa looked as chic as ever in a tweedy skirt, black blouse and cropped black blazer. Pippa, known for her impeccable sense of style, accessorised her look with a black tote, £159 black pumps by Jemima Vine and oversized sunglasses. Jemima Vine Edie Lizard Flats. Steal Pippa's style! Visit site. When it comes to flat shoes, Jemima Vine rules the roost. And although the brand is a favorite with celebs, it seems Pippa Middleton has a particularly soft spot for the flat shoe experts. She's been spotted previously wearing at least four different variations on their signature pointed flat design, with this lizard material style being the latest to catch her eye. We can understand why Pippa is so obsessed with them. After all, flat shoes are a staple item in any stylista's wardrobe, so why wouldn't you invest in a luxe-looking pair like these that are guarantee to endure season after season? Take a leaf out of Pippa's stylish and practical book, and click right to snap them up. But if you're after a budget buy, then get the look with our edit below - Forever 21's style could easily pass as a designer pair! Forever 21 Faux Suede Smoking Slippers (now $14.99) Visit site. Sperry Top-Sider Smoking Slipper at Nordstrom Rack (now $49.97) Visit site. J. Crew Celo Suede Loafers. Visit site. Charlotte Russe Perforated Smoking Slippers (now $14.99) Visit site. Pippa's brunette locks blew in the breeze as she made her way through the busy London streets . Just weeks away from the birth of a new niece or nephew, she looked demure in the purple number by with a coral belt and matching high heels, which served to showcase her slim physique. The Spectator was first launched in 1828, making it the oldest published magazine in the English language. Spectator Life is the lifestyle supplement from the main magazine and the Duchess of Cambridge's sister has contributed columns about food, truffle hunting and wine tasting since December 2012. Pippa joined other celebrity guests to celebrate the supplement's third birthday at the swanky Belgravia venue. . Pippa is just weeks away from welcoming a new niece or nephew to the family as her sister, the Duchess of Cambridge, prepares to give birth for the second time. At the party, Pippa revealed that she is having a stab at a new career - this time as a dress designer. Pippa, whose plans to be a presenter on US TV fell flat, told the Mail on Sunday that she is teaming up with an old pal, designer Tabitha Webb, to bring out a ‘Pippa Dress’ in time for a charity ball she will host in November. Her plan is to sell it to friends in lieu of donations for a cycle trek across Europe that Pippa, is doing with brother James. ‘I’m feeling guilty asking my friends to donate again,’ Pippa, a regular fundraiser, said. . Pippa was positively glowing in a tailored plum dress at the Spectator Life magazine's third birthday at the Belgraves Hotel.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
