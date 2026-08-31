---
captured: 2026-08-21T18:23:10+00:00
session: 144b398c-76b3-4e78-98d6-5c07e57e43fa
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 7223
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

Claim: The Palestinian ambassador condemned the U.S. move of its embassy to Jerusalem.

Passages:
[s0077] BLITZER: This just coming in to CNN. The actress, Margot Kidder, has died. She had been a staple on movies and television since breaking into the business as a 20-year-old in 1968. She's best known playing Lois Lane in all four of the Christopher Reeve “Superman“ films.
MARGOT KIDDER, ACTRESS: Do you have a girlfriend?
CHRISTOPHER REEVE, ACTOR: No, I don't. But if I did, you would be the first to know about it.
KIDDER: Um.
BLITZER: Her family says she passed away quietly in her home in Montana. Margot kidder was 69 years old. Other news we're following, dozens of Palestinians were killed today during protests in Gaza along the border with Israel. The demonstrations were aimed at the United States' opening a new embassy in Jerusalem, moving the new embassy from Tel Aviv to Jerusalem. The Palestinian ambassador to the United Nations says today's violence means there's no chance at peace. Let's get perspective from the Palestinians right now. Joining us, Ambassador Husam Zomlot. He's the head of the Palestinian authorities' delegation to the United States. Mr. Ambassador, thank you very much for joining us. Give us immediate reaction, if you can, to what the latest developments are, the impact of the U.S. moving the embassy, and what it means for the Israeli-Palestinian peace process?
AMB. HUSAM ZOMLOT, DIRECTOR, PLO DELEGRATION TO THE UNITED STATES: Just the U.S. administration has gave up on the peace process and its role as a mediator international towards achieving the internationally endorsed two-state solution. And it also means the U.S. has gave in for the voices of extremism, for the voices we'll see a zero-sum game, the fanatics, politically speaking. It was telling today that the ones who opened the ceremony of moving the U.S. embassy are religious leaders of the Christian Zionists who interpret politics and legality and world map from a very contested, to say the least, religious implications. This is not only encouraging Israel to cross the line. It's very encouraging to Israel to cross the line towards Armageddon and the end-of-time prophecy.
BLITZER: Ambassador, are you at all, Mr. Ambassador, in touch with Trump administration officials? They keep saying they're about to release their peace plan, Israeli-Palestinian peace plan, and they still have hope for the two-state solution, Israel alongside a new state of Palestine. Have you had conversations with these American officials?
ZOMLOT: We don't know what they're talking about, really. We don't know. Peace is a very firm vision by the U.S. That vision has been drawn by all previous administrations, with the 1968 borders, establishing a sovereign state with each in the U.S. capital. The U.S. law is very clear. It was presented in 1991 by former administrator, James Baker. It is very clear. The U.S. intervention and vision is about Israel's occupation, implementing U.N. Security Council resolutions and respecting them in Jerusalem, never recognizing Israel's control of annexations. So what the U.S. administration has done is reneging on these promises and violating international law. There is a U.N. Security Council resolution that the U.S. voted for and that presents any state from moving its embassy from Tel Aviv to Jerusalem. And also the U.S. has stated that Jerusalem is outside the negotiating table. You know it, Wolf, very well. You have been there for many decades. But Jerusalem is the heart of the two states solution --
BLITZER: Let me just interrupt, Ambassador, because they say they're not necessarily concluding all final status of all parts of Jerusalem. Yes, the U.S. is moving the embassy to west Jerusalem, but they're not completely ruling out the possibility of the Palestinians having control of parts of east Jerusalem and having a U.S. embassy in east Jerusalem for the new Palestinian state. When you hear that from the administration, what do you think?
ZOMLOT: No, I only have it from you now. Jerusalem is the capital of the Jewish people. It's not even the capital of Israel. As I said earlier, a clear religious interpretation of international relations and legal matters on one hand. On the other hand, there was a reason why all previous American presidents, from President Truman to President Obama, why they decided not to move the embassy. They knew, by doing so, you actually remove the U.S. from the role of the mediator and dictate the terms of reference and dictate the outcome of Jerusalem being an issue. Of course, we would be fine if the U.S. has -- when there are two embassies after reaching a peace agreement. Before that, it is -- it will only be seen as urgent on the Palestinians. President Trump himself says removing the Jerusalem from the table, taking it off the table. And then they wanted to remove the administration off the table that services the refugees. And then they are not even criticizing or condemning the illegal settlement expansion, which has been the major obstacle on the part of the two-state solution. And they are not even criticizing or condemning the murder by Israeli forces of the Palestinian peaceful demonstrators. So the bottom line, what peace process this administration is talking about? We believe that peace --
ZOMLOT: -- can be found now in the international community, in a multilateral forum. Peace can only be found based on legality, based on politics, not based on ideology, and some very twisted religious interpretations of reality.
BLITZER: Ambassador Zomlot, let's see what this -- if they do release a plan, the Trump administration, what specifically it spells out. We'll continue our conversations. Ambassador Zomlot, thanks so much for joining us.
ZOMLOT: Thank you.
BLITZER: We're going to hear from the White House about these deadly protests in Gaza, along the border with Israel in a few minutes. I'm sure there will be plenty of questions on that, plenty of questions on a lot of other issues as well. The White House press briefing set to begin at the top of the hour. We'll have live coverage. We'll be right back.

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
