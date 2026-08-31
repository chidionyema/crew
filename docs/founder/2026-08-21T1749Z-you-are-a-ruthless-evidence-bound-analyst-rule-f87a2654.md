---
captured: 2026-08-21T17:49:23+00:00
session: cf6cb5f6-50b1-4a35-83c5-443028fc94f6
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3161
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

Claim: Overall, animals have developed a variety of ways to deal with thorns and splinters, but if the problem persists, it is best to seek professional help.

Passages:
[s0027] [1] Use a needle to poke it out. If the thorn is just beneath a soft, thin layer of skin that has begun to heal over it, this method works well. However, it's important to follow the right technique so that you don't introduce bacteria to your skin and end up with an infection. Here's how to do it: * Make sure the area where the thorn went in is clean and dry. * Sterilize a sewing needle by wiping it with rubbing alcohol. * Press the tip of the needle over the tip of the thorn and gently loosen the new layer of skin that grew there by digging the needle under the skin. Loosen the skin around the thorn. * When enough of the thorn is exposed, remove it with tweezers * Clean the area with warm, soapy water. Put a bandaid on if necessary.

[2] Use a nail clipper or razor blade for thorns in thick skin. Thorns deeply embedded in thick, calloused skin can be removed with a razor. Only use this method for thick skin on your heels or another calloused area. Do not use this method on thinner skin, since you could easily cut yourself too deeply. If you wish to use this method, exercise extreme caution while handling the razor.

[3] To treat a dog splinter, start by gently cleaning the surrounding area with warm, soapy water so the wound doesn't get infected. Then, dip a pair of tweezers in rubbing alcohol to sterilize them, and use them to pull out the splinter. If the splinter is too deeply embedded to get a grip on, you may need to take your dog to the vet to have it removed. Once you've removed the splinter, clean the area again with warm, soapy water.

[4] A barbed thorn, like a fish hook, is difficult to remove. Avoid trying to remove it by pulling as this will on damage the soft tissue and may cause the thorn to snap with part remaining in the pad. Unfortunately, this could mean a vet visit, to sedate the dog and make a small incision so the thorn can be removed in its entirety.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
