---
captured: 2026-08-21T18:35:38+00:00
session: 6449136e-becd-47c3-af7e-00cbfabfb08d
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 5688
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

Claim: The driver's seat is positioned on the side of the car to allow the driver to see traffic coming from both directions.

Passages:
[s0102] When you are driving in a foreign country, it can be confusing to know which side of the road the driver should be on. In some countries, like the United States, the driver sits on the left and stays on the right side of the road unless overtaking.
In other countries, like England, the drivers sit on the right and keep left in traffic unless overtaking.
The driver sits on the left side of the car on the American continents, continental Europe, Africa, and parts of Asia, making up roughly two-thirds of world countries. In Britain and its former colonies, the driver sits on the right side of the vehicle.
The RHD cars were first introduced in the 18th century. Some 35% of the globe’s population now drives on the left side, representing over 55 nations. The reason behind it dates back several hundreds of years.
Interestingly, it is because most people were right-handed, by being on the left side of the road, two cavalrymen could swing swords at each other. Furthermore, mounting a horse from the left side is easier since the sword is positioned on the left side of the body.
The majority of the former British colonies, such as India, Pakistan, and Australia, have their driver’s controls on the right side of the vehicle and kept left while driving unless overtaking.
The LHD cars were first introduced in the United States. The primary reason is that Americans wanted to eradicate any reminders of British domination, while the second reason is due to the antiquated horse vehicle’s engineering.
After the introduction of the revolutionary Ford Model T by Henry Ford with a left-hand drive, this custom has been firmly established. Almost every vehicle sold in the United States has been an LHD car since then.
When you consider why the driver’s side can be either left or right, keep in mind that there’s a connection between which side of the car the driver sits in and which side of the road cars drive on.
To drive effectively, the driver must be able to see traffic coming from both directions. In countries where people drive on the left, that means the driver’s side is on the right side, and while those where people drive on the right it is on the left.
The position of the driver’s seat also allows cars to “merge” into traffic more easily. When two cars approach each other head-on, the driver on the left can easily see the driver on the right and vice versa.
But if they were driving on opposite sides of the road (with the driver’s seat on the wrong side for the country they’re in), then one driver would have to crane his or her neck around to see traffic coming from the other direction, which would be dangerous.
If you ever find yourself wondering why the driver sits close to the middle of the road, think of how dangerous it would be if you tried to overtake a truck while sitting on the passenger’s side. You’d have to steer the entire car into the opposite lane before you can even see if anyone’s coming.
If you’re planning on driving a right-hand drive car in a left-hand drive country (or vice versa), there are some things you should keep in mind.
You’ll need to be extra careful when merging onto highways and other roads. It can be easy to misjudge the speed and distance of oncoming traffic when you’re not used to driving on the opposite side of the road.
Also, you’ll need to be aware of your blind spots. Since the engine and other components will be on the opposite side of the car, your blind spots will be in different places than they would be in a left-hand drive car.
Despite these challenges, it is possible to drive a right-hand drive car in a left-hand drive country (and vice versa). Just be sure to take extra care and drive slowly until you get used to the differences.
Most countries have laws that require drivers to have at least one mirror on the driver’s side of the car. This is so that the driver can see what is behind them while they are driving. A driver’s side mirror typically gives a wider view than the rearview mirror, which is why it is required by law in most countries.
Generally, the driver’s side of the car can either be the left or right side depending on the country you are driving in. LHD cars are meant to drive on the right side of the road while RHD cars are meant to drive on the left side of the road.
You should ensure that you are familiar with the laws of the country you are driving in before getting behind the wheel.
Here are some other related topics for you to check out:

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
