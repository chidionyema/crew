---
captured: 2026-08-21T18:50:17+00:00
session: 30120924-5333-4e3c-a1aa-dd6119057049
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 6201
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

Claim: The British government has stated that Scotland would not be allowed to use the pound, while the Scottish government has said that it would be possible for Scotland to join the euro.

Passages:
[s0131] BERMAN: Tensions building in Scotland this morning and much of the United Kingdom as voters get ready for an historic vote on whether to split from the rest of the United Kingdom. Tomorrow's vote could see Scots declare independence, potentially splitting up Great Britain after 300 years. Now, some U.K. officials in Britain are pledging to give Scots new powers in an effort to sway a vote against independence. I want go to Max Foster right now who has the latest from Edinburgh. And, Max, these polls are so, so close.
MAX FOSTER, CNN CORRESPONDENT: Yes, three out today, John, and they're all too close to call. And you can really tell the story here from Edinburgh, by looking at the front pages of the newspapers. So, one of the polls on “Scotsmen“ saying the polls has “no“ in the land. But actually the “yes“ campaign is closing the gap. And “The Herald“, the only newspaper in Scotland supporting the “yes“ campaign, is making the point that yes the pro-independent campaign is closing the gap and has the momentum and could overtake no by tomorrow. That's the suggestion, at least. Very clear on the front of “The Daily Mail“, 24 hours to save Britain or to go independent. It really is a date with destiny tomorrow. We talked a bit about how there's a lot of attention to the run-up to tomorrow's poll. You know, this has been two years of campaigning and a lot of aggression, particularly on the yes side. And a very simple message here, keep the heat and carry on. That's the Scottish play on keep calm and carry campaigning, and to keep things calm really, because it is pretty tense here at the moment.
BERMAN: Max, I think we have about a thousand questions here in the United States for you about this referendum. Can't possibly ask them all the time we have. But let me ask one that I think is surprising to many Americans. Scots want independence, they want to break away. But they want to keep the queen. They want to keep the monarchy. It seems as if they don't quite under this independence thing.
FOSTER: I think this is a huge thing for the queen. I mean, she only came close to commenting. She can't get involved in politics. You know, she has to stay above politics. That's her constitutional rule. But she did say to a churchgoer recently she really hope that Scots consider this. You can imagine there was a very big British empire. Empires come and go. And the empire's really been cut back, of course. But now, you're talking about home turf, and her home state being split. I think she's pretty concerned about this. We have to say, in all essence, we're not talking about a big change in her role in Scotland, because the yes campaign they do want to keep her as head of state. But I certainly think that she's concerned about what's happening here. A breakup of the U.K., it's a huge moment in British history.
BERMAN: It would be colossal, after more than 300 years, that vote is tomorrow. If they do vote to split, it would take 18 months to implement. Max Foster, great to have you here for us this morning. Thanks so much.
ROMANS: Big questions before the referendum of what a yes vote could mean for both economies. Harvard economist Ken Rogoff told me there are a lot of unknowns, the biggest being currency.
KENNETH ROGOFF, PROFESSOR OF ECONOMICS, HARVARD UNIVERSITY: When you got through with this divorce, suddenly you don't have the currency. What currency do you have? That's one of the first questions people will have, it's one of the first questions investors have. You really don't have an answer. They say it's the pound. The British say it's not the pound. People say, well, maybe Scotland will join the euro. That creates a lot of problems for the rest of the eurozone. And they could have their own currency, but that's not a magic elixir when you don't have long credibility.
ROMANS: It's a really big deal. Rogoff also said a yes vote could be -- maybe good for Scotland in the long run, he said like in a hundred years. But it's the short term uncertainly that is so concerning about this. He said, basically, it would be a mild negative for the U.K. and very big -- very big negative for Scotland. He also said, look, when Americans say why does this matter to me? I've heard this, why do I care? He says, because the U.K. and U.S. have the strongest alliance in the world. And this is our best friend breaking apart. It's a very big deal.
BERMAN: It has huge implications for international relations as well. Again, what do you do to every other separatist movement in the world?
ROMANS: To say nothing of America's nuclear position in northern Europe, it's in Scotland.
BERMAN: Fascinating. It will all be decided tomorrow. Twenty-seven minutes after the hour. Could U.S. troops end up fighting on the ground against ISIS? A new warning from a top U.S. general as there is skepticism now about the president's plan to battle the terrorists. We're live next.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
