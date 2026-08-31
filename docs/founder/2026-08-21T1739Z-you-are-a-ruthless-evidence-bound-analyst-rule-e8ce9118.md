---
captured: 2026-08-21T17:39:42+00:00
session: 0ab49618-cb0f-41fe-9372-9f207c99b994
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3373
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

Claim: ESPN reporter Britt McHenry faced backlash for her behavior on camera after having her car towed.

Passages:
[s0015] Han and Chewie are back. An ESPN reporter went on a regrettable rant. And we all taxed our brains trying to deduce the date of Cheryl's damn birthday. Here are pop culture's most talked-about stories of the week. Producers of "Star Wars: The Force Awakens" unveiled a nearly two-minute trailer for the upcoming movie, arriving in December. When Harrison Ford shows up with Chewbacca at the end, you can almost hear the Internet's collective squeals. A logic problem from a Singapore math test somehow spread across the Web, leaving millions trying to figure out the hypothetical birthday of someone named Cheryl. We're guessing that most of us cheated and peeked at the answer. Who retires at age 34? Supermodel Gisele Bundchen, who walked what she says was her last fashion-show runway this week in her native Brazil. She'll still keep modeling, though -- and hanging out with her husband, who is apparently a football player of some kind. Oh, Britt McHenry. We all hate having our car towed. But for someone who's on air at ESPN, you don't seem to understand how to behave on camera. Speaking of McHenry, a new book by Jon Ronson explores how social media may go too far in encouraging haters to shame people who make public missteps. Ronson told CNN, "It's so corrosive to create that kind of society." The first set of female quintuplets in the world since 1969 was born in Houston, Texas. Just imagine how fun it'll be for their parents 16 years from now when they all start dating. Fire department, I need you now. Singer Hillary Scott of country band Lady Antebellum had to vacate her tour bus when it caught fire outside of Dallas. Most of her stuff was burned, but her Bible survived. To infinity and beyond. Famed physicist Stephen Hawking, known for his sense of humor, partnered with the silly lads of Monty Python to recreate the "Galaxy Song" from their 1983 film "The Meaning of Life." Duckie dances! Remember Duckie from "Pretty in Pink?" Of course you do. Actor Jon Cryer charmed fans on CBS's "Late Late Show" by reprising his character's record-store dance to Otis Redding's "Try a Little Tenderness," right down to the wall-dancing and counter-bashing.


Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
