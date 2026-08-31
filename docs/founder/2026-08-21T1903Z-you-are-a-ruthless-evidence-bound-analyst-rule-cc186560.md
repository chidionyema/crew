---
captured: 2026-08-21T19:03:33+00:00
session: b2509ba3-e8fe-4a37-8381-045210a96545
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 2189
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

Claim: Use multimedia resources, games, and role-plays to stimulate interest and motivation .

Passages:
[s0157] Roles for Multimedia in the Response-based Literature Classroom �@ Carla Meskill and Karen Swan University at Albany, State University of New York �@

Introduction

Imagine a tool, a database of information, whose use promotes and supports rich conversation around works of literature; a tool that helps students make connections, build meaning and articulate their thinking. Imagine a class of twenty-seven high school students assigned to read Shakespeare for the first time. A large video monitor at the front of the classroom displays a vivid color image of pastoral Stratford-on-Avon. Their teacher selects many additional still images and video sequences from a computer-generated menu to facilitate a discussion that sets the scene for the play. These images cue and serve to illustrate students' discourse. The teacher may select scenes that depict the life and times of the playwright, the mise en scene for a variety of stage productions, thematic works of art, segments from today's media,

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
