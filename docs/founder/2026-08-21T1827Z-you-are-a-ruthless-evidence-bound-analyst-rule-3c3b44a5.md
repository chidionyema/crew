---
captured: 2026-08-21T18:27:14+00:00
session: f3b8211e-1656-4c9c-833d-15b4a28017cc
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 4313
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

Claim: They continue to discuss family matters and are dedicated to their children's well-being.

Passages:
[s0086] Arnold Schwarzenegger Opens Up About His Relationship with Maria Shriver, New Action Hero Series
Arnold Schwarzenegger, the former governor of California and beloved Hollywood action star, recently provided a candid glimpse into various facets of his life. This revealing conversation touched on his evolving relationship with his ex-wife, Maria Shriver, his latest venture into the world of action hero series, and his civic endeavors, particularly his efforts to combat the menace of potholes in Los Angeles.
Schwarzenegger and Shriver officially divorced two years ago, marking a significant turning point in their relationship. However, they have entered a new phase, particularly as they embrace their roles as grandparents to their daughter Katherine's two children. Schwarzenegger made it clear that their connection never truly severed, and their separation was not characterized by animosity or conflict, but rather by his own acknowledged mistakes.
During this conversation, centered around the promotion of his book, Schwarzenegger offered insight into the ongoing communication between him and Shriver, specifically concerning their family. Despite their divorce, which transpired in 2011 following Schwarzenegger's admission of fathering a child with their housekeeper, Mildred Baena, they have remained in regular contact. Schwarzenegger shared details of attending counseling sessions with Shriver, where he disclosed his paternity of Joseph Baena. He candidly acknowledged the immense pain and devastation his revelation caused for Shriver and their family.
However, their unwavering commitment to their children's well-being has remained steadfast. Schwarzenegger emphasized that they continue to discuss family matters, including holidays, birthdays, and other significant events. He expressed his enduring love for Shriver, affirming that their relationship, while different in nature now, will endure indefinitely.
In his personal life, Schwarzenegger has moved forward and is presently in a relationship with Heather Milligan, a physical therapist. This partnership, which began in 2013, has been a source of joy and companionship for the actor. Schwarzenegger spoke highly of Milligan, praising her independence, work ethic, and determination. He openly shared his deep affection for her and their shared interests, highlighting the positive aspects of their relationship.
Beyond his personal life, Schwarzenegger remains actively engaged in his professional pursuits. He is currently immersed in a new action hero series, a project that aligns seamlessly with his enduring passion for the entertainment industry. Additionally, Schwarzenegger has taken on a civic duty close to home by addressing the pervasive issue of potholes in Los Angeles.
Despite the inevitable highs and lows in his personal journey, Arnold Schwarzenegger continues to navigate the delicate balance between his professional commitments and his responsibilities as a father and grandfather with characteristic grace and resilience. His willingness to share his experiences and lessons learned serves as an inspiration to many.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
