---
captured: 2026-08-21T17:32:18+00:00
session: 5a90c729-9793-4975-b91f-8c1bc967c1e7
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 4546
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

Claim: A majority of members of the Republic of Ireland's Citizens' Assembly have voted in favour of a change in the country's abortion laws.

Passages:
[s0002] These are external links and will open in a new window. The Republic of Ireland currently has strict abortion laws, which only allow a pregnancy to be terminated if there is a serious risk to a woman's life. The Citizens' Assembly voted 64% to 36% in favour of having no restrictions. Anti-abortion groups have condemned the result of the vote, but any change to the law would require a referendum. The Citizens' Assembly was set up by the Oireachtas (Irish Houses of Parliament) to advise elected representatives on a number of ethical and political dilemmas facing the Irish people. These include abortion, climate change and how the Republic of Ireland deals with the challenge of providing for its aging population. The body is made up of 99 members who were chosen at random to broadly represent the views of the Irish electorate. Its most controversial task was to consider a campaign to repeal the Eighth Amendment of the Irish Constitution - which gives an equal right to life to a pregnant woman and an unborn child. Assembly members held 10 days of intensive and emotive debates over the past five months, culminating in this weekend's series of votes. On Saturday, members voted against repealing the Eighth Amendment, but they did support change - voting to amend or replace the law. On Sunday, a majority of Citizens' Assembly members approved 13 separate grounds for legal terminations in the Republic of Ireland. Of the votes cast, 89% were in favour of allowing abortion on grounds of rape or fatal foetal abnormality - when doctors believe an unborn child is likely to die before, during or shortly after birth. There was less support for legal terminations for "socio-economic reasons" but still, 72% of members who took part voted in favour of abortion in those circumstances. However, anti-abortion campaigners dismissed the results of the ballots as a "muddled and confused farce". Cora Sherlock of the Pro Life Campaign accused the assembly of having a "chaotic" and "one-sided approach" in how it conducted its business from the beginning. She added: "There is nothing liberal or progressive about the assembly recommending a referendum to strip unborn babies of their right to life in law and also ignoring the negative consequences of abortion for women." The Citizens' Assembly is chaired by the Supreme Court judge, Ms Justice Mary Laffoy, who will now present a report on members' recommendations to the Oireachtas by late June. In a statement, the chair said members had "reached a conclusion of sorts" and she thanked them for having "engaged with some of the most complex pieces of legislation, immersed themselves in medical and ethical discourse, and listened with respect to the voices and opinions of others". "I also wish to acknowledge those whose perspectives or opinions did not emerge in the final vote," the judge added. "This is an exercise in deliberative democracy and their vote remains important to me because of the very fact it captures that other perspective, that dissenting voice, the different interpretation and I wish to assure them that their votes and voices will be recorded and have a place in the report." On receipt of her report, elected representatives will consider members' calls for a change in the law, and whether or not to hold a referendum.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
