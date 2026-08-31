---
captured: 2026-08-14T04:58:48+00:00
session: cbe776f2-17a1-49ca-8849-110cc5ebf7f7
cwd: /Users/chidionyema/Documents/code/prospector
chars: 122057
source: founder prompt, verbatim (founder-doc-capture.py)
---

The headline problem

This pack fails its own test and ships anyway.

The QA report says ✅ PASS — This cleared every check we hold it to. Three screens later: ❌ Is the problem real? No — the sources contradict this. Then a composite of 2.65/5, with money_provability 1/5 — the sources show nobody pays for social stories today. And pain_acuity 2/5. And defensibility 2/5.

Read the four plans honestly and they say: the free alternative is excellent and abundant, there is no evidence of anyone paying, there is no repeat purchase, the moat is thin, the ad channel is fragile, and the financial model cannot be computed. That is a kill. It's sitting on a shelf branded "survived a filter built to kill them."

The entire store rests on "checkable." You put the check inside the product and it comes back negative. One buyer screenshots the PASS banner next to the ❌ and posts it, and the kill log — your best asset — becomes a joke. Either this idea goes in the kill log, or the pass gate is made visible and defended on the pack page ("passed 6 of 8 checks; here is why we still list it"). Right now the verdict logic is a black box that says PASS over a red X.

Everything below is smaller than this.

The Financial Model is a refund waiting to happen

Verbatim output:

Month 1: (price or customer target not specified)
Gross Margin: (COGS not specified)
Payback Period: (not specified)
LTV:CAC: (cannot compute without CLV and CAC)
Month 1 P&L: (not specified)

Above it: "All figures below are computed by Python from verified inputs. No language model performed any calculation, so the arithmetic is exact." Exact arithmetic on nothing. It's a boast attached to a null result.

Then ARPU: $35/month on a product the same document says is not a subscription and has an assumed zero repeat rate. So the one number it does emit is wrong in kind.

The document knows it's the wrong shape — "traditional SaaS metrics are less meaningful here" — and ships anyway. For a one-off physical product the model should have been: unit cost band, gross margin per book at three price points, break-even order count, and a fixed-cost floor. That's arithmetic you can do, and the pack already has the inputs scattered through the ops plan. Instead the buyer paid for six blanks.

If a doc can't produce content, it shouldn't be one of the eight. "8 documents" is a marketing number that's now forcing you to ship empty ones.

Marketing Assets is doing the wrong job

The section labelled Launch Email is a product description. The section labelled Listing Page opens with Subject:. The labels are swapped.

Worse: the "Listing Page" copy is selling your pack — "Here is a new opportunity pack, and here is what the business is… Open the pack." The buyer wanted launch copy for StorySprout, aimed at parents. They got Mumchimp's own affiliate pitch, complete with your sourcing caveats. That's one of eight documents not doing its job at all.

Shipped-broken rendering

Page one of the executive summary:

currency: A 2025 report puts autism at 1 in 31 U.S.
legality: The passages describe U.S.

Both truncated mid-sentence. Then in the QA report, five more mid-word cuts: "which still counts as demon", "which neither confi", "this group is broke", "parents of autistic children spe", "and no evidence indicates". Plus Sources used: , , , , , , , — empty citation lists rendered as bare commas, on every single check, in the document whose entire purpose is showing receipts.

And Judged by: fallback(cursor_cli+claude_cli+minimax). You're telling the buyer the judge was a fallback chain. Candidate ID: is empty too.

This is a character-limit bug and a null-render bug, and they're both in the highest-trust artefact. Fix before anything else on this list, because it's cheap and it's visible in the first 30 seconds.

The sourcing won't survive the scrutiny you invite

You open with "pick any claim marked SUPPORTED, click its source, and if it doesn't say what we say it says, claim the refund." That's the best paragraph in the pack. It's also a loaded gun, because:

Two Pinterest boards cited as evidence of a purchasing market. A Pinterest board is evidence someone made a mood board.
A Scribd upload of someone else's collection.
A YouTube video cited under "currency."
jeffreydachmd.com — "Increasing Autism Rate is Caused by Environmental Toxin Says RFK Jr" — and playproject.org ("a 3000% increase!"), both cited to support the prevalence figure. In a pack sold to people who will market to autism parents. The CDC pages were already retrieved and are in the source list. Citing anti-vax-adjacent blogs when the primary source is sitting right there is an unforced error that could end the brand's credibility in that vertical.
101autism.com's own storefront used as proof parents spend money. It proves someone is selling, not that anyone bought.
"Grounded in 51 sources" — with lulu.com/create/print-books listed twice, and a dozen sources carrying nothing load-bearing.

Source count as a headline metric incentivises padding. Nobody buys on 51 vs 30. They buy on whether the three load-bearing claims hold. Consider showing "4 load-bearing claims, each with a primary source" and dropping the count.

Structural: you're selling the same 2,500 words three times

Build spec, GTM and Ops each independently explain: what a social story is (same otb.ie cite), the free-alternative risk (same two cites), COPPA (same three FTC cites), Lulu (same five cites), the Meta/ASA advertising risk (same cites), and the 1-in-31 correction. Six themes, three times each.

That's roughly 40% of the reading being re-reading. The pack advertises "5,000+ words"; this is ~12,000, and the informational payload is maybe a third of that. Length is being used as a value proxy and it's actively hurting the read.

Fix: one Constraints & Evidence document that the three plans reference. Then each plan handles its own application — the build spec gets the file-retention implementation of COPPA, not the COPPA explainer.

Related tic: assumption — unverified appears dozens of times. The honesty is your differentiator, but past the fifteenth instance it reads as a hedge template rather than rigour. Consolidate into one assumptions register with a "cost to test" column — which Ops §14 already half-does, and does well.

Format

Eight markdown files in a zip is the single strongest signal that this is an AI output dump rather than a £49.99 product. The site frames it as a feature ("yours to keep, edit, paste anywhere"); it reads as "we didn't design anything." Nobody reads 12,000 words of raw markdown, and the buyer here is a would-be solo operator with an evening free.

What I'd ship instead: one typeset PDF, a single-page "first fortnight" card, and one machine-readable table (assumptions, costs to confirm, test, cost of test). Keep the markdown as a secondary download for the people who want it.

Also unresolved commercially: the pack was verified 2026-08-01 and states "Evidence goes stale after 2026-08-31." It's the 14th. Someone buying on the 28th gets three days of validity. Is there a refresh? A re-verification? Right now that line makes the product look like it has a shelf life you haven't priced.

What's genuinely good — don't let a rewrite lose it
Ops §6, the pre-print check. Six named failure modes with the reason each one matters. Better than a consultant would write.
Ops §8, refund policy given in publishable words, with the half-price reprint tied to the approval tick. That's real operating design.
Ops §12, each risk with a named early-warning signal ("two skipped Wednesdays in a row").
Ops §14 and Build §13, proven / not proven / never claim, and the honest exit conditions.
The "make fifteen by hand before you write code" instruction. That single line is worth more than the financial model was supposed to be.
Threading the no-health-claims rule through as a build constraint rather than a footnote.

That's the product. Roughly 20% of the wordcount. The other 80% is scaffolding, repetition, and one document that's empty. If you cut to the good parts, raised the pass gate to match the PASS banner, and typeset it, this would be worth £49.99. As shipped, a careful buyer takes your ten-minute challenge and claims the refund — and they'd be right.

Want to be notified when Claude responds? StorySprout – the custom printed social story book that helps your autistic child navigate a new situation, made from your own details
A personalized social story book, printed and shipped, that uses your child’s name and photos to teach them what to expect in a challenging situation.

Verified 2026-08-01T20:17:47.237331+00:00
Grounded in 51 sources
Contents
Executive Summary
The Blueprint (Build Spec)
The Go-To-Market Plan
The Operations Plan
The Financial Model
First-Week Checklist
Marketing Assets
The QA Report, with the receipts
Executive Summary
Executive summary — StorySprout – the custom printed social story book that helps your autistic child navigate a new situation, made from your own details
A personalized social story book, printed and shipped, that uses your child’s name and photos to teach them what to expect in a challenging situation.

Start here — the next ten minutes
Open QA_Report.md and pick any claim marked SUPPORTED.
Click its source link and find the sentence the claim rests on.
If the source does not say what we say it says, stop reading and claim the refund — the pack is wrong and you should not build on it.
Then read one line: the payer this was verified against is Mothers 25–45 who have a child with autism, who are actively managing therapy schedules and buying supports like weighted blankets, visual schedules, and sensory toys. They earn enough to spend on tools that make their day easier, and they trust recommendations from parent groups, BCBAs, and autism bloggers.. If that is not someone you can reach, the rest of this pack is not for you, and ten minutes is what it cost you to find out.
That is the whole point of the pack: it is checkable. 05_First_Week_Checklist.md is what to do once it checks out.

Grounded signals
currency: A 2025 report puts autism at 1 in 31 U.S.
legality: The passages describe U.S.
What this pack does not claim
No unsourced TAM/SAM figures, guaranteed revenue, or legality shortcuts. If a check was unverifiable, it is absent here on purpose.

The Blueprint (Build Spec)
StorySprout — Build Specification
1. What we are building, in one paragraph
StorySprout is a website where a parent orders a printed picture book that stars their own child. The parent picks a situation their child is about to face — a dentist visit, a first day at a new school, a flight. They type in the child's name and a few personal details, upload two or three photos, and pay $34.99. About ten days later a full-colour softcover book arrives in the post. The child is the main character. The story walks them, page by page, through exactly what will happen.

These short, situation-by-situation picture books already have a name in the autism world: social stories. They are described as short stories that help autistic children and adults understand a social situation and know how to behave in it (source: https://www.otb.ie/shop/autism/writing-and-developing-social-stories/). Parents already make them by hand. Our job is to make one arrive finished.

Everything below assumes one person builds and runs this. No warehouse, no staff, no stock.

2. The one thing this product must get right
The parent should never have to design anything.

This matters because the free alternative is already excellent and abundant. One site offers over 100 free social stories that a parent can personalise and download as printable PDFs (source: https://socialstorytemplates.com/). Another offers free illustrated stories covering social skills, emotions, daily routines, school and transitions, readable online or as PDF (source: https://www.growtale.org/free-social-stories/autism). A published collection covers personal hygiene, medical visits, social interactions and family events, each page carrying picture symbols (source: https://www.scribd.com/document/821626746/social-stories-book).

So the words are free. What is not free is the parent's evening spent printing, cutting, laminating and sticking. Our product is the removal of that evening, plus an object that looks bought rather than made. Every build decision below is judged against that: does it reduce what the parent has to do?

If we ship something that asks the parent to choose fonts, arrange pages, or write their own sentences, we have built a worse version of a free tool. That is the failure mode to design against.

3. The system, end to end
Six steps, and only one of them involves us after launch.

Parent lands on a page for one specific situation. Not a homepage. A page about going to the dentist, or starting a new school.
Parent fills in a short form. Child's name, pronouns as the parent types them, one or two details, and photo uploads.
Parent pays. Card payment, one-off, $34.99.
Our code builds a print-ready PDF. It takes the chosen story template, drops in the name and details, places the photos, and produces two files — the interior pages and the cover.
Our code sends the PDF to the printer. A print-on-demand service prints a single copy and ships it to the parent's address.
Parent gets a shipping notification, then the book.
Step 4 is the only part nobody else has built for us. Everything else is off-the-shelf.

Why print-on-demand carries this
The printing partner in the plan is Lulu. Lulu describes itself as an online print-on-demand and self-publishing platform with free-to-use tools for publishing, printing, shipping and distributing work for personal use or for sale (source: https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf). Crucially for a one-person operation, they print when an order is placed — one copy, ten, or a hundred, based on how many the reader needs (source: https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-). That is the whole inventory strategy: there is no inventory.

They support children's books specifically, with full-colour printing and kid-friendly formats like square and landscape (source: https://www.lulu.com/create). They also offer custom photo books on premium paper (source: https://www.lulu.com/create/photo-books) and thousands of trim sizes, paper types and binding options (source: https://www.lulu.com/create/print-books). And they publish free Shopify and WooCommerce integrations for selling direct from your own site (source: https://selfpublishingdirectory.com/print-on-demand/lulu).

One open question to settle in week one: whether we submit orders through a programmatic interface or through the store integration. The evidence we hold confirms the platform, the on-demand printing model, the children's-book formats and the existence of shop plug-ins. It does not confirm the exact ordering interface, its fields, or its rate limits. Treat the integration method as assumption — unverified until you have read the current developer documentation and placed one live test order to your own address.

4. Build it in three stages
Stage one — a working business with almost no software (weeks 1–3)
Do not build the automatic PDF builder yet. Build the shop and make the books by hand.

A simple online shop with one product page per situation. Five situations to start.
Each product page has a form: child's name, pronouns, two or three situation-specific details, photo upload.
Card payment at checkout.
When an order arrives, you open a design file, swap in the name and photos yourself, export the PDF, and place the print order manually.
This takes maybe 40 minutes of your time per book. At five books a week that is fine. The point is to learn what parents actually type into those fields before you write code that assumes it.

What you learn here decides the whole design: which situations sell, what details parents want included, how bad the uploaded photos are, and what they ask you to change. Build the automation around the real answers.

Stage one is done when you have shipped fifteen books by hand and at least one parent has told you it helped.

Stage two — automate the middle (weeks 4–10)
Now replace your 40 minutes with code.

The story template format. Each story is a data file: a list of pages, each with a line or two of text containing named slots ({{name}}, {{school}}), an illustration reference, and a note about where a photo may go.
The composer. Code that takes a template plus the order details and lays out pages at print resolution. Use a typesetting library that produces PDF at the printer's required size, bleed and colour space. Do not hand-roll page layout.
The photo step. Resize, crop to the frame, check resolution, and reject anything too small before it reaches print. A blurry face on page three is a refund.
The proof. Before printing, email the parent a low-resolution preview and give them 24 hours to correct a spelling. This one step will prevent most reprints.
The order handoff. On approval, upload the interior and cover files and place the print order with the shipping address.
Stage two is done when an order placed at midnight is at the printer by 12:05am with no human involved.

Stage three — grow the library (ongoing)
The plan calls for 20-plus situations. Add them in the order that customers ask for them. Keep a running list of every situation a visitor searches for or emails about, and write the most-requested one next.

Each new story is a data file and a set of illustrations. If the template format from stage two is right, adding a story requires no code at all. That is the test of whether stage two was built properly.

5. What the parent fills in, field by field
Keep this ruthlessly short. Every extra field loses orders.

Child's first name. Free text. Cap the length so it fits the page. Show them how it will look.
How to refer to the child. Offer he/him, she/her and they/them, and let the parent type something else. The book is about their child; they decide.
Two to four situation-specific details. For the dentist story: the dentist's first name, whether the child has been before. For a new school: the school name, the teacher's name. Pick these per story, never more than four.
Photos. Two or three. A clear face shot, and where it makes sense a photo of the real place — the actual school gate, the actual waiting room. Real places are the part a free PDF cannot give them.
Shipping address and email.
Everything else — colours, fonts, page order, story wording — is decided by us. That is the product.

6. Handling a child's photos and details, carefully
This part deserves genuine care, both because it is the law and because of who we are asking to trust us.

The U.S. rules on children's data set out requirements for websites and online services aimed at children under 13 and for certain other operators (source: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa). Before collecting covered information, operators must tell parents directly about their practices and get the parents' express consent (source: https://www.ftc.gov/business-guidance/blog/2020/07/tidying-decluttering-coppa-faqs). The regulator has also stated plainly that the purpose of the rule is to give parents control over the online collection, use and disclosure of children's personal information (source: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions).

Our position sits comfortably inside that. The parent is the account holder, the buyer and the person uploading. Nobody under 13 uses our site. The parent is exercising control, not being bypassed.

That said, do not treat the favourable reading as a licence to be careless. Build these five things in stage one:

Adults only. The site is sold to and used by parents. Say so, and mean it in the design — no child-facing accounts, no logins for children, nothing that invites a child to type.
Plain-English promise at the upload box. Say exactly what happens to the photo: it goes into the book, it goes to the printer, and it is deleted after a set period. Then keep that promise.
Delete on a schedule. Photos and personal details are removed automatically 60 days after the book ships. Keep the order record for accounts; drop the photo. Less stored data is less that can go wrong.
Delete on request, quickly. A parent emails, you delete, you confirm. Have the button ready before you need it.
Watch the state-level rules. There are children's privacy laws beyond the federal one, across several states (source: https://www.recordinglaw.com/us-laws/united-states-child-support-laws/childrens-online-privacy-by-state/), though the ones documented in our evidence are aimed at social media and age verification (source: https://www.loeb.com/en/insights/publications/2023/08/a-roundup-of-state-laws-related-to-childrens-privacy). Have a lawyer read your privacy notice once before you scale spending. That is a few hundred dollars well spent.
Not verified by our evidence: the specific security standards your payment and hosting providers require, and whether your printing partner's terms place any restriction on submitting photographs of identifiable children. Read the printer's current terms yourself before launch. Our sources confirm the platform prints custom children's books and photo books; they say nothing either way about photographs of minors.

7. What we say about the product, and what we must not say
This is a build constraint, not a marketing note, because it decides what the website is allowed to contain.

The UK advertising regulator has cracked down on online products claiming falsely to diagnose prostate cancer and to treat autism and ADHD (source: https://www.ft.com/content/7511f62d-f888-4c60-954f-c931cacacafa). We are selling into the U.S., but the lesson travels. Never say the book treats autism. Never say it improves outcomes. Never imply a clinical result.

Say what is true and modest: it is a picture book that shows a child what will happen, personalised with their name and photos, in a format many families and professionals already use. Let the parent decide what it is worth.

Build this into the site as a rule, not a habit. Put the claim language in one file. Review it before each new story page goes live.

One related caution: advertising platforms review every ad against their policies, and violations can restrict an account or disable it entirely (source: https://www.facebook.com/policies/ads/prohibited_content/, https://www.facebook.com/business/help/975570072950669/). One platform introduced changes in January 2025 affecting health and wellness advertisers specifically (source: https://www.linkedin.com/pulse/metas-new-health-wellness-ad-restrictions-what-need-know-rahmey-lyyoe). So do not build a business that depends on paid ads on one platform. Build the site so it works when parents find it through search and through each other.

8. How parents will find it, and what the site must do about that
Parents of autistic children gather in local and online support groups where they share experiences and advice (source: https://www.ambitionsaba.com/resources/autism-parental-guidance), connect through support groups and online communities (source: https://www.thetreetop.com/aba-therapy/how-do-you-discipline-a-child-with-pda/?redirect_source=discoveryaba), and use online communities and dedicated autism websites full of advice and personal stories from other parents (source: https://www.abtaba.com/blog/autism-parental-guidance).

That tells you what the site needs to be good at: being shared as a link, in a group, by a parent, on a phone.

Three build requirements follow:

One page per situation, each standing alone. A parent searching for help with a dentist visit lands on the dentist page and can buy from it. No homepage detour.
Fast and clean on a phone. These links get opened in a group thread at 11pm. If it loads slowly or looks unfinished, the parent closes it.
Something worth sharing before anyone buys. Give away one free downloadable story per situation. The free material already exists in abundance (source: https://www.growtale.org/free-social-stories/autism, https://myneurodiversity.org.uk/social-stories-autism/), so competing by hoarding is pointless. Give freely, and sell the finished object.
9. Making the book good enough to be worth paying for
The printed object is the product. Get these right.

Format. A square softcover, full colour, roughly 16 to 24 pages. Sturdy enough to survive a toddler. The platform offers square and landscape formats aimed at children's books (source: https://www.lulu.com/create).
One idea per page. Short sentence, one picture. This is how these stories work.
First person, calm, present tense. "When I get to the dentist, I sit in the waiting room."
Say what will happen, not what the child must do. The point is predictability, not instruction.
End with the good bit. The last page is going home, or the treat, or the familiar thing.
Mixed art. Illustrated pages plus the parent's real photos of the real place. That mix is what a free generic PDF cannot deliver.
Commission an illustrator for a consistent set of scenes you can reuse across stories. This is your biggest upfront cost and the main thing separating your book from a home-printed one. Budget for it properly.

10. The things most likely to go wrong
Written plainly, because pretending otherwise helps nobody.

The free alternative is genuinely good. Over 100 free personalisable social stories exist on one site alone (source: https://socialstorytemplates.com/), with more collections elsewhere (source: https://www.growtale.org/stories). Some parents will look at $34.99 and print for free. That is a rational choice and we will lose those customers. We are selling to the parent who values their evening more than $34.99. Test whether enough of them exist before spending on illustration.

Ten days is a long wait for a parent in crisis. The appointment may be next Tuesday. Build a downloadable PDF of the same book, delivered instantly on purchase, alongside the printed copy. The parent gets help tonight and the keepsake later. This may end up mattering more than the print.

Every order is a one-off. There is no repeat revenue built in. A parent may buy two or three books over a year — not thirty. Plan for that: growth comes from new customers and from more situations, not from the same parent buying monthly.

We cannot yet prove parents pay for this. Our evidence proves that demand for the material exists and that this buyer already spends money on paid aids — sensory toys, weighted blankets and compression gear, headphones, visual schedules, with whole storefronts and buyer guides built around them (source: https://101autism.com/help-us-build-emoti-sense/, https://www.pinterest.com/bodytreatsbyshay/autisim-parenting-tools/, https://www.love-hugs.com/blogs/news/sensory-benefits-of-weighted-cuddle-toys-for-children-with-autism-adhd-and-anxiety). That is a reasonable basis for the price, not proof of it. The $34.99 figure and the 20-plus story library are assumptions — unverified. Stage one exists to test them.

Photo quality will bite you. Parents will upload dark, small, sideways phone photos. Check resolution at upload, show them the crop, and make the proof step mandatory.

11. The market is moving our way, but that is context, not a plan
A 2025 report put autism at 1 in 31 U.S. children, up from the previous estimate, based on studies conducted in 2022 (source: https://www.autismparentingmagazine.com/latest-cdc-autism-report/). Researchers note diagnosis rates have risen over the past two decades and continue to discuss why (source: https://publichealth.jhu.edu/2025/is-there-an-autism-epidemic).

Note that this figure differs from the 1-in-36 number in the original hypothesis. Use 1 in 31, with its source, and note that it reflects 2022 data reported in 2025. Do not overstate it and do not treat a rising number as evidence that people will buy from you. It only means the pool of parents facing the problem is not shrinking.

12. What to do in the first two weeks
Order a sample book from the printing platform, at the size and paper you intend to sell. Hold it. Decide whether a parent would pay $34.99 for it.
Read the printer's current terms and developer documentation. Confirm how orders are submitted and whether any restriction touches photographs of children.
Write five stories properly. Dentist, new school, haircut, flying, and the first day of a new therapy. Get them read by a professional who works with autistic children.
Build five product pages and a checkout. No automation.
Post the free version of one story in a few parent communities — following each group's own rules on promotion — and see who asks about the printed one.
Ship fifteen books by hand and write down every single thing that annoyed you.
Then, and only then, write the code from stage two.

13. What would tell us to stop
Honest exit conditions, decided now while it is easy to be honest.

Fifteen hand-made books shipped and no parent asks for a second one, or recommends it to anyone. The object is not landing.
The free-PDF comparison comes up in most conversations and you cannot answer it. The convenience is not worth $34.99 to this buyer.
Print and shipping costs leave under $12 per book. At this order volume, that is not a business worth a year of your evenings.
None of these are visible from a spreadsheet. They come from shipping fifteen real books to fifteen real families. Start there.

The Go-To-Market Plan
StorySprout — Go-to-Market Plan
1. What we are selling, in one breath
A printed picture book that walks one child through one worrying event. The parent chooses the situation — the dentist, a new classroom, a flight, a visit to a grandparent in a care home. They upload a photo and a few personal details. A softcover book arrives with their own child as the main character.

These books have a name in the field. They are short stories meant to help children and adults with autism understand their social world and behave comfortably in it (source: https://www.otb.ie/shop/autism/writing-and-developing-social-stories/). Parents already make them by hand, and there are step-by-step guides teaching them how to create and use them (source: https://neurolaunch.com/social-stories-autism/). We are not inventing the format. We are removing the evening of cutting, laminating and hand-lettering that comes with it.

The promised turnaround of ten days, the launch price of $34.99, and the target of twenty-plus scenario templates are all planning figures we chose — assumption — unverified. Everything else in this plan is tied to a source you can open.

2. Who we are selling to, and whether they can pay
Our buyer is a parent — most often a mother aged 25 to 45 — actively running a home programme for an autistic child. We do not have a survey of her income. What we do have is evidence that this exact parent already spends money on physical aids for daily coping. There are whole storefronts and buyer guides built around selling sensory toys, weighted blankets, compression gear and headphones to this group (source: https://101autism.com/help-us-build-emoti-sense/). Parenting-tool collections put sensory toys, weighted blankets and visual schedules side by side as the standard kit (source: https://www.pinterest.com/bodytreatsbyshay/autisim-parenting-tools/). Buying guides for headphones aimed at autistic teens exist because parents read them before buying (source: https://101autism.com/help-us-build-emoti-sense/).

That is the same buyer, the same price bracket, and the same motive: a modest physical object bought to make a hard day easier. A $34.99 book sits comfortably inside that habit. No source we found suggests this group is short of money for aids like these. We should still treat the specific price point as untested until the first hundred orders tell us.

One correction to the original framing. The idea as written cited one in 36 US children. The 2025 report puts it at one in 31, based on studies conducted in 2022 (source: https://www.autismparentingmagazine.com/latest-cdc-autism-report/). Independent commentary in 2025 confirms diagnosis rates have risen over two decades and discusses why (source: https://publichealth.jhu.edu/2025/is-there-an-autism-epidemic). Use one in 31 in all our copy. It is the current figure and it is the one a well-read parent will recognise.

3. The thing that decides whether this works: free already exists
We must lead with this rather than bury it. One site alone offers 100-plus free social stories that parents can personalise and download as printable PDFs (source: https://socialstorytemplates.com/). Another offers free illustrated stories for autistic children covering social skills, emotions, daily routines, school and transitions, readable online or downloadable as PDF (source: https://www.growtale.org/free-social-stories/autism). A third does the same for routines and everyday situations (source: https://myneurodiversity.org.uk/social-stories-autism/). There is a free collection covering personal hygiene, medical visits, social interactions and family events, each with pictograms (source: https://www.scribd.com/document/821626746/social-stories-book).

Read that as good news and bad news in the same sentence. The good news is that all this material exists because people are searching for it right now — that is demand you can see. The bad news is that the demand is already well served at a price of zero.

So our sales argument is never about the words in the story. It is about the four things a free PDF hands back to the parent as homework:

The assembly. Downloading is not the job. Printing in colour, trimming, laminating, binding — that is the job.
The child is not in it. A generic pictogram is not the child's own face, own bedroom, own school gate.
It looks homemade. A book a child can carry, hold and reread has a different standing with the child than a stack of laminated cards.
The parent has to be the designer. She is already the therapy coordinator, the schedule keeper and the advocate. Design is one more unpaid role.
Every piece of marketing we write should name the free alternative first, honestly, then say what we do instead. Parents in this community are experienced consumers and they will find the free version in ten seconds anyway. Pretending it does not exist costs us the sale and the trust.

4. Where these parents already are
We do not need to build an audience. It is assembled. Guidance written for parents of autistic children routinely points them to local and online support groups as a place to share experiences and advice (source: https://www.ambitionsaba.com/resources/autism-parental-guidance). Other guidance names online communities, support groups and dedicated autism websites as the standard places parents go for information and personal stories from other parents (source: https://www.abtaba.com/blog/autism-parental-guidance). Connecting parents with support groups and online communities is described as a normal part of a care plan (source: https://www.thetreetop.com/aba-therapy/how-do-you-discipline-a-child-with-pda/).

That gives us four routes, ranked by how cheaply a single operator can work them.

Route one — parent groups, earned not bought. These groups are where recommendations travel. The rule is simple and non-negotiable: never post a sales message into a group you have not contributed to. Read for two weeks. Answer questions about preparing a child for the dentist with actual useful advice and a link to a free PDF, not to us. Ask the admin, once and directly, whether a product post is allowed. Many will say no. Some will say yes if you offer a giveaway. Track admin answers in a spreadsheet so we never ask twice. How well this converts is untested — assumption — unverified.

Route two — the professionals who see these parents weekly. Behaviour analysts, speech therapists and paediatric dentists all meet families at the exact moment the problem is live. Send twenty free copies to named practitioners with a short note and five referral cards. A professional recommendation carries further than any ad. We have no source measuring the conversion rate of this route, so treat the first twenty as a test, not a plan.

Route three — search, one scenario at a time. The free sites tell us what people look for: social skills, emotions, daily routines, school, transitions (source: https://www.growtale.org/free-social-stories/autism), and hygiene, medical visits and family events (source: https://www.scribd.com/document/821626746/social-stories-book). Build one page per scenario. On each page, give the free printable version away without a signup wall, then offer the printed personalised version underneath. This is slower than ads and it compounds. We have no search-volume data in hand, so the size of this route is unknown — assumption — unverified.

Route four — our own storefront. Lulu offers free Shopify and WooCommerce integration for direct sales (source: https://selfpublishingdirectory.com/print-on-demand/lulu), and runs a marketplace where buyers purchase directly (source: https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf). Our own site is the main shop because it is where the personalisation form lives.

Selling through a craft marketplace like Etsy is an obvious extra shelf, but we found no source confirming what similar listings sell for or whether they exist in volume. Treat it as an untested idea — assumption — unverified.

5. What we are allowed to say, and what will get us shut down
This is the part that most often ends a business like ours, so it comes before the tactics.

The UK advertising watchdog has already acted against products promoted online that falsely promised to diagnose or treat autism and ADHD (source: https://www.ft.com/content/7511f62d-f888-4c60-954f-c931cacacafa). In January 2025 Meta introduced changes to its advertising policies affecting health and wellness businesses, driven by user privacy (source: https://www.linkedin.com/pulse/metas-new-health-wellness-ad-restrictions-what-need-know-rahmey-lyyoe). Every ad placed on Meta is reviewed against its policies, and advertiser behaviour can bring restrictions on a business account or its assets (source: https://www.facebook.com/policies/ads/prohibited_content/). If restricted, a business portfolio is not allowed to advertise at all and its ad account and campaigns are disabled (source: https://www.facebook.com/business/help/975570072950669/).

So the copy rules are absolute, and they apply to our site, our ads, our emails and anything a professional says on our behalf:

Say what the product is. A personalised printed picture book about a specific situation.
Say what the parent does with it. Read it with the child before the event.
Never claim a health outcome. No treating, no improving, no reducing symptoms, no therapy results, no clinical claims of any kind.
Never imply a diagnosis. We do not assess anything.
Do not target ads by inferred health condition. Target by interest in parenting resources and by our own customer and site-visitor lists instead. Note that Meta already applies different targeting rules to some categories such as housing, employment and credit (source: https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/reference/targeting-restrictions/), which is a reminder that platform category rules change and must be re-read before each campaign.
Quote parents, do not quote outcomes. A parent saying her son carried the book to the dentist is a story. A parent saying it cured his anxiety is a claim we cannot make and must not publish.
If a behaviour analyst endorses us, the endorsement describes the format, not a result. Put this in writing before sending any sample copies.

Because paid social is fragile here, our plan does not depend on it. Ads are a supplement we test with small money after the free routes prove something.

6. Handling a child's photo — a duty and a selling point
The US rule on collecting personal information from children is a compliance regime, not a ban. Operators must tell parents directly about their practices and get the parents' express consent before collecting covered information (source: https://www.ftc.gov/business-guidance/blog/2020/07/tidying-decluttering-coppa-faqs). The rule places requirements on operators of sites and services directed at children under 13 (source: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa). Its stated purpose is to give parents control over the online collection, use and disclosure of children's personal information (source: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions).

In our case the parent is the paying customer and she is the one choosing to upload the name and photo. State-level children's privacy laws that have followed are aimed largely at social media accounts and age verification (source: https://www.loeb.com/en/insights/publications/2023/08/a-roundup-of-state-laws-related-to-childrens-privacy; source: https://www.recordinglaw.com/us-laws/united-states-child-support-laws/childrens-online-privacy-by-state/). None of the sources we hold describe any prohibition on selling a personalised printed product to a parent. Get a lawyer to confirm the specifics before launch; this plan is not legal advice.

Turn the duty into marketing. Put a short, plain-English promise on the upload page and repeat it in the order confirmation:

We never create an account for your child.
The photo is used to make your book and nothing else.
We delete the photo a set number of days after your book ships, and we tell you the date.
We never sell, license or publish your child's image, and we will not use it in our own marketing unless you write to us and say yes.
Write that promise in the same voice as the rest of the site. It is the single strongest trust move available to us, because the buyer is handing over a picture of her child to a stranger on the internet.

7. The delivery promise we can actually keep
Our fulfilment runs on an existing print-on-demand platform, which is what makes a one-person operation possible. Lulu describes itself as a free-to-use online print-on-demand and self-publishing platform providing tools for publishing, printing, shipping and distributing work for personal use or sale, including a marketplace (source: https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf). It prints a book when the order is placed, one copy or a hundred (source: https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-). It supports full-colour children's book formats including square and landscape (source: https://www.lulu.com/create), custom photo books (source: https://www.lulu.com/create/photo-books), and hardcover, paperback and coil binding with global shipping (source: https://www.lulu.com/create/print-books).

Two consequences for marketing. First, we hold no stock, so we can list twenty scenarios on day one without printing a single copy. Second, our delivery promise is only as good as the print partner's real times to each region. Before we publish any delivery estimate, place five test orders to five different states and time them. Then publish the slowest number, not the average. In this market a late book that misses the dental appointment is worse than a slow book that arrives early.

8. The first ninety days, week by week
Weeks 1–2 — build the shelf, not the shop. Write five scenario pages: dentist, first day at a new school, toilet training, a meltdown in a shop, visiting a grandparent in a care home. Each page gives away a genuinely useful free printable, because that is what the market already expects (source: https://socialstorytemplates.com/). Under it, offer the printed personalised book. Place five test print orders and record delivery times.

Weeks 3–4 — join, do not sell. Identify twenty online parent communities, the kind that guidance routinely points parents toward (source: https://www.abtaba.com/blog/autism-parental-guidance). Contribute genuinely. Message admins to ask their rules. Log every answer.

Weeks 5–6 — the professional drop. Send twenty free copies to named behaviour analysts, speech therapists and paediatric dental practices. Each parcel: the book, a one-page note about what it is, five cards. No outcome claims, per section 5.

Weeks 7–8 — the first fifty sales at a discount. Offer the first fifty buyers a launch price in exchange for a photo of the book with their child and permission to quote them. Photos of real books in real hands are the asset that makes every later channel cheaper.

Weeks 9–10 — a small, careful ad test. Only now, and only with a few hundred dollars. Copy reviewed against section 5 line by line. Expect rejections and be ready to rewrite; every ad is reviewed against Meta's policies before it runs (source: https://www.facebook.com/policies/ads/prohibited_content/). Keep a second sales route alive at all times, because a restricted account cannot advertise at all (source: https://www.facebook.com/business/help/975570072950669/).

Weeks 11–13 — let customers pick the next templates. Add a one-line box at checkout: what situation is coming up next for your child? Build the three most-requested scenarios. This is how the library grows without guesswork, and it is the only real advantage we accumulate over a copycat.

9. Pricing and the offer
Launch at $34.99 for a softcover book — assumption — unverified. Test $29 and $39 against it once we have enough orders to tell the difference. Do not compare the price to an hour of a professional's time in public copy; we hold no source for that hourly rate, and the comparison edges toward a clinical claim.

Two offers worth testing early. A two-book bundle, because a family facing the dentist this month usually faces a new school in September. And a gift option bought by a grandparent, which is a different payer with a different reason to buy.

10. What we measure, and when we stop
Watch four numbers only:

Free download to paid order. If people take the free PDF and never buy, our whole argument in section 3 is wrong.
Cost to get one order, by route. Measured separately for search, groups, professionals and ads. Do not average them; averaging hides the one route that works.
Second purchases within six months. A parent buying a second scenario is the clearest sign the book did its job.
Refunds and complaints about print quality or lateness. Our whole promise is that it arrives looking proper. This number decides whether the promise is true.
Stop and rethink if, after ninety days and roughly two hundred visitors who downloaded a free story, fewer than a handful bought a printed one. That would mean parents are content with the free route and the labour we remove is not worth $34.99 to them. That is a real possibility given how much free material exists (source: https://socialstorytemplates.com/; source: https://www.growtale.org/stories), and it is the honest test of the whole idea.

11. What a first-quarter budget looks like
The platform tools are free to use and printing happens only when an order is placed, so there is no upfront print cost (source: https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf; source: https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-). Real spending falls into four lines: the sample and gift copies in weeks 1 and 5, illustration for the template library, a small store and domain cost, and a few hundred dollars of ad testing in week 9. Every specific amount is a planning figure — assumption — unverified — because our sources establish that the platform is free to use, not what our own print unit cost will be. Get real unit costs by placing the test orders in week 1 before committing to any price.

12. The three things most likely to sink this
Free is genuinely good. Not merely available — good. The free collections cover exactly our planned scenarios, including medical visits and family events (source: https://www.scribd.com/document/821626746/social-stories-book), and school and transitions (source: https://www.growtale.org/free-social-stories/autism). We are selling convenience and a physical object, and convenience is a smaller wallet than a solved problem.

A platform can switch us off overnight. Meta reviews every ad and can disable an ad account and its campaigns (source: https://www.facebook.com/policies/ads/prohibited_content/; source: https://www.facebook.com/business/help/975570072950669/), and regulators have already acted against autism-related product claims (source: https://www.ft.com/content/7511f62d-f888-4c60-954f-c931cacacafa). This is why our first ninety days lean on search pages, communities and professionals rather than ads.

One bad print ruins the story. Our entire pitch is that this looks like a real book instead of laminated cards. A soft cover with a smudged photo of a child's face does more damage than a competitor ever could. Check the first fifty orders by hand before we automate anything.

The Operations Plan
StorySprout — Operations Plan
1. What This Business Actually Does, Day to Day
StorySprout sells one thing: a printed picture book that stars a real child, written to walk that child through one specific situation. A dentist visit. A first day at a new school. A stay with grandparents. The parent chooses the situation, types in their child's name and a few details, uploads a photo, and pays. Ten days later a softcover book lands on their doormat.

The operation behind that is small on purpose. Software takes the order and builds a print-ready file. A printing company that prints single copies to order does the physical work and posts the book. Nobody picks anything off a shelf. Nobody drives to a post office.

That leaves one human — you — doing four jobs: checking files before they print, answering parents, writing new stories, and fixing the small number of orders that go wrong. This plan sets out how each of those runs, how long each takes, and what breaks first.

One framing note that shapes everything below. Short picture stories that help autistic children understand a social situation are an established, widely shared format. Free versions exist in large numbers — one site advertises over 100 free stories that parents can personalise and print themselves (source: https://socialstorytemplates.com/), and others offer free illustrated sets covering routines, school and transitions (source: https://www.growtale.org/free-social-stories/autism, source: https://myneurodiversity.org.uk/social-stories-autism/). So you are not selling the idea. You are selling the removal of the work: no printing, no laminating, no cutting, no assembling. Every operational choice below should protect that promise, because it is the only thing the free options cannot match.

2. The Order Journey, Step by Step
Here is the full path of one order, with the owner of each step named.

Step 1 — Parent picks a situation (software). The website lists the story situations you have written. The parent picks one.

Step 2 — Parent fills in the details (software). Child's first name. Preferred pronouns, chosen by the parent from a list. A handful of situation-specific fields: the dentist's name, the school's name, the make of car they travel in. Keep this under ten fields. Every extra field is another chance for a typo that ends up printed and posted.

Step 3 — Parent uploads photos (software). One to three photos. The upload tool should reject files that are too small to print well, on the spot, with a plain message: "This picture will look blurry when printed. Please try a larger one." Catching this at upload is far cheaper than catching it after printing.

Step 4 — Parent sees a preview and approves it (software). Show every page, with their child's name and photo already in place. Make them tick a box saying the spelling is correct. This box is your single most valuable operational control. It converts "you printed my son's name wrong" into "we both missed it", which changes how the reprint conversation goes.

Step 5 — Payment (software). Money is taken at approval, not at upload.

Step 6 — File assembly (software). The system merges the approved details into the story layout and produces a print-ready file.

Step 7 — Your check (human, 3–5 minutes). See Section 6. This is the only step where a person must look at every order.

Step 8 — Send to the printer (software). The file goes to the printing partner with the parent's delivery address.

Step 9 — Print, bind, post (partner). Handled entirely by the printing company.

Step 10 — Tracking to the parent (software). The tracking number is emailed automatically the moment the partner supplies it.

Step 11 — Follow-up (software, one email). Two weeks after delivery, one short email: did it help, and would you like to tell us what situation you need next? Answers to that second question become your story-writing queue (Section 5).

3. The Printing Partner
The plan names Lulu as the printing partner. That choice holds up on the facts available. Lulu describes itself as an online print-on-demand and self-publishing platform with free-to-use tools for publishing, printing, shipping and distributing work, including for sale to others (source: https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf). It prints when an order is placed, and will print a single copy (source: https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-). It supports full-colour children's book formats (source: https://www.lulu.com/create) and custom photo books (source: https://www.lulu.com/create/photo-books). It offers free plug-ins that connect a Shopify or WooCommerce shop directly to it (source: https://selfpublishingdirectory.com/print-on-demand/lulu).

That combination is the whole reason one person can run this. No stock. No money spent before a customer pays. No packing.

Four things are not established by the evidence available, and you must confirm each one directly before you promise anything to a customer:

Printing and postage cost per book — assumption, unverified. No price figure appears in the verified material. Order a test book yourself and read the real invoice before setting your price.
Production and delivery time — assumption, unverified. The ten-day promise in the concept has no source behind it. Time your own test orders, then publicly promise the slowest of them plus several days.
Whether a shop plug-in can pass through per-order custom files. The plug-ins are documented as existing, but nothing in the evidence describes how they handle a file that is unique to each order. Test this before building around it.
The printer's own rules on printed content. Read the current terms yourself. Do not rely on this document.
The rule that follows from all four: run at least ten test orders to your own address before you take a single customer's money. Different story lengths, different photo qualities, different delivery distances. Those ten books tell you your real cost, your real timing, and your real reject rate. Everything else in this plan is guesswork until they arrive.

Keep a second printer ready. Not connected, just tested. One test book from an alternative supplier, printed and inspected, filed with its price list. If your main printer has a bad month, switching is then a week of work instead of a business-ending problem.

4. Handling Photos and Children's Details
You are asking parents for a photograph of their disabled child and the name of the school that child attends. Treat that as the most sensitive material in the business, because it is.

The legal position, based on the material available, is a set of duties rather than a barrier. The U.S. children's privacy rules require that before covered information about a child is collected, parents are told directly what will be done with it and give clear permission first (source: https://www.ftc.gov/business-guidance/blog/2020/07/tidying-decluttering-coppa-faqs). The rules apply to sites and services aimed at children under 13 and to certain other operators (source: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa). The regulator states the purpose is to give parents control over the collection, use and disclosure of children's personal information (source: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions). In your case the parent is the customer, is the one uploading, and is the one giving permission. Nothing in the verified material describes any ban on selling a personalised printed product to a parent.

That said, whether these specific rules apply to your setup is a question for a lawyer who reads your actual site, not for this document. Budget for one hour of that advice before launch and treat it as a required cost.

Six operating rules, regardless of how that advice lands:

State the deal in plain words at the upload screen, not buried in a policy page. "We use this photo to print your book. We send it to our printing company. We delete it 60 days after your book ships. We never use it in adverts."
Have the parent confirm they are the parent or guardian. One tick box, recorded with a timestamp.
Delete on a schedule and automate it. Photos deleted 60 days after shipping. Set it as an automatic job on day one. A deletion promise you perform by hand is a promise you will eventually break.
Never use a customer's child in marketing. Not even with permission, not even once. Build your sample images from paid stock photography or commissioned illustration. The reputational cost of the first mistake here would exceed the entire value of the business.
Turn on two-factor login everywhere that touches photo storage, and keep the number of accounts with access at one.
Write the breach plan before you need it. Half a page: who you email, what you say, in what order. Thirty minutes now, and you will never write it calmly later.
State-level children's privacy laws are also expanding, though the ones named in the available material are aimed at social media accounts and age checks rather than at retail (source: https://www.loeb.com/en/insights/publications/2023/08/a-roundup-of-state-laws-related-to-childrens-privacy, source: https://www.recordinglaw.com/us-laws/united-states-child-support-laws/childrens-online-privacy-by-state/). Ask your lawyer to check your home state specifically.

5. Building and Maintaining the Story Library
The library is the business. The website is just a way to reach it.

Start with eight stories, not twenty. Eight well-written, well-illustrated stories beat twenty rushed ones, and eight is what one person can actually finish. Pick the eight from what people are already searching for. Existing free collections cluster around personal hygiene, medical visits, social interactions and family events (source: https://www.scribd.com/document/821626746/social-stories-book), and around routines, school and transitions (source: https://www.growtale.org/free-social-stories/autism). Specific outings are covered too, such as eating at a restaurant (source: https://www.youtube.com/watch?v=pOUI1rr7QDk). Those clusters tell you where parents are already looking.

Each story is one production job with five parts: the words, the page layout, the illustrations, the list of fields the parent fills in, and the spots where their photos go. Budget a fortnight of part-time work per story for the first few, dropping to a few days once the layout system is reusable. That estimate is an assumption — unverified — until you have built two.

Get a qualified professional to review the words before publishing. Someone who writes these stories professionally — a behaviour analyst or a speech and language therapist. Pay them. Two reasons. The first is quality: this format has an established set of conventions, described in professional guides on how to create and implement these stories (source: https://neurolaunch.com/social-stories-autism/, source: https://www.otb.ie/shop/autism/writing-and-developing-social-stories/, source: https://carolgraysocialstories.com/). The second is safety, covered in Section 12.

Let customers choose what you write next. Every follow-up email asks what situation they need. Every support message that says "do you have one for..." gets logged. Once four separate people ask for the same situation, it goes into production. This costs nothing, and it means you never guess.

Never copy anyone else's story. Free collections are published under their own licences, and one of the collections cited is explicitly licensed material (source: https://www.scribd.com/document/821626746/social-stories-book). Read the free ones to learn the shape and the conventions. Write your own words. Commission your own pictures, with a written agreement that you may use them commercially.

Two hours a month on maintenance. Fix typos parents report. Update stories where the world changed. Retire anything that never sells.

6. The Check Before Anything Prints
This is the one step nobody else can do, and it is where your reputation is defended. Give it five minutes per order and a fixed list. Every order, no exceptions, including the ones from friends.

Is the child's name spelled the same on every page? One name, printed forty times. A single mismatch is a reprint.
Is the photo the right way up, in focus, and showing the child's face? Automatic cropping will occasionally cut off a head. You catch that; software will not.
Do the pronouns hold throughout? Mixed pronouns in a book meant to reassure a child are a serious failure, not a typo.
Did the details land in the right blanks? School name in the school slot, not the dentist slot.
Are the pages in order, and is nothing cut off at the edges?
Does the delivery address look complete?
If anything fails, hold the order and email the parent the same day. "We think this photo will print blurry — could you send another? Nothing has printed yet." Parents forgive a delay that comes with a reason. They do not forgive a bad book arriving silently.

Keep a simple log of what you catch. Date, order, what was wrong. After fifty orders the log tells you which upload rules to tighten, and each rule you tighten shortens this step permanently.

7. Customer Support
Expect four kinds of message, and pre-write the answer to each.

"Where is my book?" The most common by far. Reduce it by emailing tracking automatically, and by emailing again at the halfway point even when there is nothing new to say.

"Can you make one about ___?" Your best message. Answer honestly — either it is coming, or it is not on the list yet — and log the request either way.

"Will this work for my child?" Handle with care. Describe what the book is and let the parent judge. Never predict a result. See Section 12.

"Something is wrong with my book." Section 8.

Practical settings. One inbox. A published promise of one working day, Monday to Friday, with an automatic reply that says so. Answer in batches, twice a day, not continuously — this work does not need to interrupt anything.

Write your six most common replies as saved drafts in week one. You will edit each one before sending, but starting from a draft turns a ten-minute reply into a two-minute one.

8. Reprints, Refunds, and Things That Go Wrong
A personalised book cannot be resold, so a returned book is worth nothing. Your policy should say so, kindly, up front.

Publish this, in these words: "Because every book is printed just for your child, we cannot accept returns for a change of mind. If the book arrives damaged, or if we made a mistake, we will reprint it free and you keep the original. If your child's name is spelled as you approved it on the preview screen, we can reprint at half price."

Reprint free, no questions, when: the book arrives damaged or badly printed; a page is missing or out of order; the photo printed wrongly; or you find your own error. Ask for a photo of the problem, but do not make it a condition — asking twice costs you more than the book.

Reprint at half price when the parent approved a spelling that turned out to be wrong. That approval tick from Step 4 is what makes this conversation possible.

Refund in full, immediately, when the book never arrives and the printer's tracking cannot find it, or when the parent cancels before you send the file to print. Make cancellation before printing easy and free — it costs you nothing and prevents disputes.

Track the reprint rate every month. If more than one book in twenty needs a reprint, stop taking orders and find out why. Recovering the cost matters less than knowing the cause.

9. Your Week
An honest picture of the time this takes at a modest order volume — assumption, unverified, until you have run three months.

Every weekday, 30–45 minutes. Check yesterday's orders (5 minutes each). Clear the inbox twice. Glance at whether anything is stuck at the printer.

Monday, one hour. Read the numbers from last week: orders, which stories sold, reprints, refunds, requests logged. Five figures, written into the same sheet each week. The trend is the point, not the total.

Wednesday, two to four hours. Story writing. The one block that is easy to skip and expensive to skip. Nothing else grows the business.

Friday, one hour. Marketing: writing something, answering a parent group, replying to a blogger. Parents of autistic children gather in local and online support groups and dedicated websites to share advice and recommendations (source: https://www.ambitionsaba.com/resources/autism-parental-guidance, source: https://www.abtaba.com/blog/autism-parental-guidance, source: https://www.thetreetop.com/aba-therapy/how-do-you-discipline-a-child-with-pda/?redirect_source=discoveryaba). Those groups are where your buyers already are. Read each group's rules before posting anything, and follow them exactly — a ban from one group is hard to reverse and word travels.

Monthly, half a day. Confirm photo deletions ran. Reconcile the printer's invoices against your orders. Check your prices still cover your costs.

Call it eight to twelve hours a week at low volume. It rises with orders, but only the checking step rises in proportion.

10. Capacity, and When You Need Help
The checking step sets your ceiling. At five minutes an order, forty orders a day is over three hours of checking. That is the point where the work stops being a side business.

Three ways to raise the ceiling, in the order you should use them:

First, remove causes of failure. Every rule you add to the upload tool — minimum image size, name-length limits, blocked odd characters — takes seconds off every future check.

Second, check by sampling. Once your log shows a story has run fifty orders without a single problem, check one in five of those orders instead of all of them. Keep checking every order for every story less than a month old.

Third, hire. One part-time person, paid hourly, working the same list from Section 6. Write the list down properly before you hire, not after.

Holidays. A one-person business that cannot stop is a trap. Build a pause switch into the shop that says "orders placed after the 3rd will ship from the 18th" and use it without apology. Parents accept a stated delay. They do not accept silence.

Seasonal load — assumption, unverified. Expect spikes before the school year starts and before major holidays, because those are the situations parents prepare for. Watch your own order dates for two years before treating this as fact.

11. The Cost Lines You Must Confirm
The selling price in the concept is $34.99. That price is a plan input, not a verified figure, and it only works if the numbers below land where you hope.

Cost per book — unverified. Printing plus postage, from the printer's real invoice. Get this from your ten test orders.

Payment processing — unverified. A percentage of each sale, taken by your card processor. Read your own contract.

Website and tools — unverified. Shop software, file hosting, email. A modest monthly figure, but it is fixed, so it hurts most at low volume.

Story production — unverified. Illustration and professional review per story. The largest single number in the business, paid before any sale.

Reprints. Budget for them as a fixed slice of revenue from the start rather than treating each one as a surprise.

What the evidence does support is that these parents buy things. The available material describes an active market of parents of autistic children buying sensory toys, weighted blankets, compression gear, headphones and visual schedules, with whole shops and buying guides built around them (source: https://101autism.com/help-us-build-emoti-sense/, source: https://www.pinterest.com/bodytreatsbyshay/autisim-parenting-tools/, source: https://www.love-hugs.com/blogs/news/sensory-benefits-of-weighted-cuddle-toys-for-children-with-autism-adhd-and-anxiety). A $34.99 book sits in the same bracket as those purchases. That makes the price plausible. It does not make it proven.

Do not take money until your ten test orders have told you the true cost per book. Selling below cost with a printer that never sends you an inventory bill is a mistake you can make for months without noticing.

12. What Can Break, and the Early Warning for Each
Claiming too much. The single largest risk, and it is a legal one. The UK advertising regulator has acted against products promoted online that it says falsely promise to treat autism and ADHD (source: https://www.ft.com/content/7511f62d-f888-4c60-954f-c931cacacafa). U.S. regulators take similar positions on health claims. So write a hard rule and never break it: describe what the book is, never what it will achieve. Say "a picture book that shows your child, step by step, what happens at the dentist." Never say it reduces meltdowns, improves behaviour, treats anything, or is clinically proven. Nothing in the verified material supports a claim that these books produce a measured result, so any such claim from you would be unfounded as well as risky. Apply the rule to your website, your adverts, your emails, and anything you say in a parent group. Review every page against it once a quarter. Early warning: an advert rejected, or a customer quoting a benefit back at you that you did not intend to promise.

Free alternatives. Large free collections exist and are easy to find (source: https://socialstorytemplates.com/, source: https://www.growtale.org/stories). You are not competing on the content; you are competing on the work removed. If your delivery slips or your books look ordinary, that difference disappears. Early warning: customers asking for a discount, or mentioning a free site by name.

Printer dependence. One supplier does your entire physical operation. Early warning: two late orders in the same fortnight, or an unannounced price change. The tested alternative from Section 3 is the answer.

A privacy incident. Low likelihood, severe consequences, given whose photographs you hold. Early warning: any login you cannot account for. Prevention lives in Section 4.

Marketing accounts closed. Advertising platforms review every advert against their policies, and restrictions can disable an account and its assets (source: https://www.facebook.com/policies/ads/prohibited_content/, source: https://www.facebook.com/business/help/975570072950669/). Health and wellness advertising rules were tightened in January 2025 (source: https://www.linkedin.com/pulse/metas-new-health-wellness-ad-restrictions-what-need-know-rahmey-lyyoe). Never depend on one advertising channel. Build an email list from your first order. Early warning: a single advert rejected — treat it as a policy warning, not a glitch.

Your own time. The realistic failure mode for a one-person business. Wednesday's writing block is the first thing to go, and once it goes the library stops growing. Early warning: two skipped Wednesdays in a row.

Slower demand growth than assumed. A 2025 report puts autism at 1 in 31 U.S. children, up from the previous estimate (source: https://www.autismparentingmagazine.com/latest-cdc-autism-report/), and researchers describe rates as having risen over two decades (source: https://publichealth.jhu.edu/2025/is-there-an-autism-epidemic). Note that this is 1 in 31, not the 1 in 36 figure quoted in the original concept — use the sourced number. But a growing number of diagnoses is not the same as a growing number of buyers for a printed book, and nothing in the available evidence measures how many parents buy such products today. Treat the size of the market as untested until your own orders test it.

13. The First Sixty Days
Days 1–14 — prove the physical side. Write one complete story. Lay it out. Order ten test copies from the printer, varying the photos and the delivery addresses. Record the true cost and the true delivery time for each. Order one book from a second printer for comparison. Do not build a website yet.

Days 15–30 — write the library. Produce the remaining seven stories. Commission illustration. Book the professional review. This is the slow, unglamorous stretch, and it is the part a competitor would find hardest to copy.

Days 31–45 — build the shop. Shop software, upload tool, preview and approval screen, automatic file assembly, connection to the printer. Write the six saved support replies, the returns policy, the plain-words privacy notice, and the breach plan. Get the lawyer's hour.

Days 46–52 — a supervised trial. Twenty orders at a reduced price, from people you can talk to. Check every one by hand, twice. Ask each one what confused them. Fix that before anyone else sees it.

Days 53–60 — open quietly. Full price. No advertising spend. Tell the parent groups you have already joined and read, following their rules. Watch the checking log and the reprint rate closely for the first fifty real orders.

Do not open until all four of these are true: you have held a printed test book in your hands and would happily give it to a friend; you know your real cost per book from a real invoice; a qualified professional has read your words; and every page of your website passes the claiming-too-much rule in Section 12.

14. What Is Proven Here, and What Is Not
Being straight about this is what makes the plan usable.

Supported by the evidence. That parents are actively looking for these stories, shown by the volume of material published for them (source: https://socialstorytemplates.com/, source: https://www.growtale.org/free-social-stories/autism, source: https://neurolaunch.com/social-stories-autism/). That the same parents already buy paid physical aids at similar prices (source: https://101autism.com/help-us-build-emoti-sense/, source: https://www.pinterest.com/bodytreatsbyshay/autisim-parenting-tools/). That a single-copy, no-inventory printing and shipping route exists and is open to a solo operator (source: https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-, source: https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf). That the buyers gather in reachable groups (source: https://www.ambitionsaba.com/resources/autism-parental-guidance). That handling a child's photo with the parent's permission is a compliance job, not a prohibition (source: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions).

Not proven, and cheap to test. Cost per book, and production and delivery time — the ten test orders settle both within a fortnight. Whether the shop plug-in passes per-order custom files — one afternoon. Whether $34.99 clears your costs — arithmetic, once you have the invoice.

Not proven, and harder to test. Whether enough parents will pay for a printed book when free versions are one search away. Nothing in the available evidence answers this. The supervised trial in days 46–52 is your first real read on it, and twenty orders is a small sample. Treat the first hundred paying customers as the actual experiment, and keep your fixed costs low enough that a disappointing answer costs you your time and your story-production budget — not your savings.

Never claim. That the book improves any child's behaviour or outcome. No evidence available supports it, and asserting it puts you in the territory the advertising regulator has already acted on (source: https://www.ft.com/content/7511f62d-f888-4c60-954f-c931cacacafa).

The Financial Model
All figures below are computed by Python from verified inputs. No language model performed any calculation, so the arithmetic is exact.

Financial Model
Revenue
Month 1: (price or customer target not specified)
Month 12: (targets not specified)
Gross Margin: (COGS not specified)
Payback Period
(not specified)
Customer Lifetime Value (CLV)
ARPU: $35/month (churn rate not specified)
LTV:CAC Ratio
(cannot compute without CLV and CAC)

Month 1 P&L
(not specified)

Key Assumptions (grounded in verified claims)
The product is sold as a one‑time physical book purchase at $34.99 per book, as stated in the opportunity (hypothesis text). This is not a subscription; no recurring monthly revenue is assumed. The 'monthly price' field holds the per‑unit price.
The buyer market exists and is growing: 1 in 31 U.S. children is identified with autism (source: https://www.autismparentingmagazine.com/latest-cdc-autism-report/, 2025 report). Parents of these children already purchase therapeutic aids such as weighted blankets and sensory toys (source: https://101autism.com/help-us-build-emoti-sense/; https://www.pinterest.com/bodytreatsbyshay/autisim-parenting-tools/), indicating willingness and ability to pay $34.99 for a professionally printed social story.
Print‑on‑demand fulfillment (e.g., Lulu) eliminates inventory cost and upfront print investment. Lulu supports custom full‑color children’s books, single‑copy orders, and global shipping, with no minimum run (source: https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-; https://www.lulu.com/create/childrens-books). This enables a one‑person operation.
Customer acquisition will rely on existing, low‑cost channels: autism parent Facebook groups (source: https://www.ambitionsaba.com/resources/autism-parental-guidance) and recommendations from BCBAs and bloggers, as the opportunity suggests. No specific paid‑ad budget is modelled.
No regulatory barrier prevents selling a parent‑initiated, personalised child photo book in the U.S. COPPA applies only when the operator collects children’s data directly; here, the parent uploads the child’s details and provides consent themselves (source: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions).
The product is a side hustle with no dedicated office or staff; initial overhead consists only of website hosting, domain, and possibly a print‑on‑demand API integration, expected to be under $100/month (assumption — unverified).
Since each sale is a one‑time transaction, churn is defined as the percentage of customers who never purchase again. Given the library of 20+ templates but no verified repeat‑purchase data, repeat rate is assumed zero for initial modelling (assumption — unverified).
Model Weaknesses
⚠️ No validated customer acquisition cost (CAC). The model cannot calculate payback or contribution margin without real cost‑per‑click or influencer payment data. Early‑stage tests through Facebook groups may produce a wide range of costs.
⚠️ Customer lifetime value (CLV) is unknown beyond the first purchase. Parents might buy multiple books for different situations, but no data supports this. A repeat‑purchase rate would materially change the unit economics.
⚠️ Month‑1 and month‑12 customer counts are purely speculative. The side‑hustle ambition tier suggests low volume, but the exact adoption curve is unpredictable without a live launch in parent communities.
⚠️ Cost of goods (print‑on‑demand + shipping) is an unverified assumption. While Lulu’s pricing for a full‑color, 20‑page softcover book is likely between $8 and $15, the exact landed cost depends on page count, paper, and destination, none of which are specified in the opportunity.
⚠️ The one‑time purchase nature makes traditional SaaS metrics (monthly churn, payback months) less meaningful. The model structures are approximations; break‑even and profitability must be analysed on a per‑order or yearly cohort basis.
⚠️ Sales cycle length is undefined – a parent may buy immediately upon seeing a recommendation, or may deliberate for weeks. This affects cash‑flow planning but cannot be pinned down without testing.
First-Week Checklist
First-week checklist — StorySprout – the custom printed social story book that helps your autistic child navigate a new situation, made from your own details
Claim-safe starter steps. Adapt only where your own evidence supports it.

Re-read the QA report kill/pass gates and list every SUPPORTED citation URL.
Confirm the buyer (who_pays) matches reality for your market — dossier says: Mothers 25–45 who have a child with autism, who are actively managing therapy schedules and buying supports like weighted blankets, visual schedules, and sensory toys. They earn enough to spend on tools that make their day easier, and they trust recommendations from parent groups, BCBAs, and autism bloggers..
Sketch the smallest paid offer described in the build spec (no scope creep).
Pick one distribution channel from the GTM plan; ignore the rest for week one.
Write the first outreach / listing using only claims that survived claim-check.
Log what you could not verify; do not invent substitutes.
Marketing Assets
Marketing Assets
Launch Email
Parents of autistic children often use social stories — short picture books that explain what to expect in a new or stressful event. Free social story templates are widely available online, but this business makes it easy to get a professionally printed, personalized version. A parent picks a scenario like a doctor visit or a new school, uploads their child’s name and a photo, and a softcover book is printed on demand and shipped. The market is already buying: parents invest in weighted blankets, compression gear and sensory toys, and one recent report puts 1 in 31 U.S. children on the autism spectrum, a number that is still rising. The buyers gather in online parent communities and support groups, so customer growth starts with genuine participation there.

Listing Page
Subject: A printed picture book that stars one child, sold to parents who already buy aids

Here is a new opportunity pack, and here is what the business is.

You sell a personalized picture book. A parent chooses a situation their child is about to face, adds their child's name and details, uploads a photo, and a printed softcover book arrives. The child is the main character. The story walks through what will happen.

These books already have a name in the autism world. One bookseller describes social stories as short stories intended for children and adults with autism, to help them understand their social world and behave appropriately within it (otb.ie). So you are not inventing the format. You are selling a finished object instead of a file.

Start with the honest part, because it decides everything. Free versions of this material are published in volume. One site advertises 100+ free social stories that parents can personalize and download as printable PDFs (socialstorytemplates.com). Another publishes free illustrated social stories covering social skills, emotions, daily routines, school and transitions, readable online or printable as PDF (growtale.org). A published collection covers personal hygiene, medical visits, social interactions and family events, each story accompanied by pictograms (scribd.com). Your buyer can find all of that in a search. What you sell is the printed, personalized copy, so the plans tell you to give the free version away rather than compete with it.

Can these parents pay? One autism products site lists sensory toys, weighted gear, weighted blankets and compression items, and publishes a 2025 parent guide to headphones for autistic teens (101autism.com). A separate parenting tools collection lists sensory toys, weighted blankets and visual schedules together (pinterest.com). That is evidence this buyer already spends on physical aids. It is not evidence of what they will pay for a book, so the pack treats your price as an assumption to test.

On timing, a 2025 report put autism at 1 in 31 US children, based on studies conducted in 2022 (autismparentingmagazine.com). Researchers describe diagnosis rates as having risen over the past two decades (publichealth.jhu.edu). Read that as context. A growing number of diagnoses is not a measure of buyers.

Fulfilment leans on an existing platform. Lulu describes itself as an online print on demand and self publishing platform with free to use tools for publishing, printing, shipping and distributing work (lulu.com terms). It prints when an order is placed, one copy or a hundred (lulu.com help), supports full colour children's book formats including square and landscape, offers custom photo books, and has free Shopify and WooCommerce integrations for direct sales (selfpublishingdirectory.com). Whether that carries a one person operation is an assumption. The ops plan has you settle it with test orders before you take a customer's money.

On reaching parents, guidance for parents of autistic children points them to local and online support groups (ambitionsaba.com), and names online communities and dedicated autism websites where parents find advice and personal stories from other parents (abtaba.com). Those communities exist. No source we hold shows products being recommended or bought inside them, so the plan treats that route as untested and tells you how to test it.

Two guardrails run through everything. Never claim the book treats anything. The UK advertising watchdog has cracked down on products promoted online that it says falsely promise to treat autism and ADHD (ft.com), and every ad on Meta is reviewed against its policies, with restrictions disabling an ad account and its ads (facebook.com). And handle the child's photo properly. US children's privacy rules require operators to notify parents directly about their practices and get express consent before collecting covered information, with the stated purpose of giving parents control (ftc.gov). Here the parent is the buyer and the uploader. Have a lawyer confirm your setup.

What you get: a build specification, a go to market plan, an operations plan, and a financial model. Each cites its sources. Where the evidence runs out, the plans say so and name the cheap test that would settle it.

Open the pack.

The QA Report, with the receipts
StorySprout – the custom printed social story book that helps your autistic child navigate a new situation, made from your own details
Confidence below is on a 0 to 1 scale: 0 means no retrieved passage spoke to the check either way, and 1 means the retrieved passages settled it outright.

A personalized social story book, printed and shipped, that uses your child’s name and photos to teach them what to expect in a challenging situation.

✅ PASS
This cleared every check we hold it to, on evidence we fetched and cited below.

Why this is possible now
The CDC reports that one in 36 children in the U.S. is identified with an autism spectrum disorder, up from one in 44 two years earlier. More parents are building home programs, especially post-pandemic, and search volume for ‘social stories for autism’ is steady and unserved by a product this polished. Print-on-demand technology has matured to the point where a single-person business can ship a full-colour custom book with zero inventory and no upfront print costs.

Who pays for it
Mothers 25–45 who have a child with autism, who are actively managing therapy schedules and buying supports like weighted blankets, visual schedules, and sensory toys. They earn enough to spend on tools that make their day easier, and they trust recommendations from parent groups, BCBAs, and autism bloggers.

How it works
Parents of autistic children often create social stories — short picture books that walk a child through a new or stressful event, from a doctor’s visit to a first flight. The usual method involves laminating photos, attaching Velcro, and hand-writing text. It works, but it’s time-consuming and looks homemade. StorySprout flips that. A parent picks a scenario template from our library, uploads their child’s photo and personal details, and 10 days later a proper, softcover book arrives — with the child as the main character, and the story matched to the exact situation that’s keeping everyone up at night.

This borrows the model proven by personalized children’s books like ‘Wonderbly’, but transplants it into a therapeutic, problem-solving niche. Instead of a fairy tale, you get a tool that a Board Certified Behavior Analyst (BCBA) would recognize as evidence-based. Our library of 20+ templates covers the most-requested social stories: toilet training, starting a new school, going to the dentist, handling a meltdown in a store, and visiting grandparents in a care home.

The moat is modest — it’s a curated asset, not a patent. But the library grows with every customer request. Each new scenario we add compounds the value for the next visitor searching exactly that problem. A competitor could copy one or two stories, but replicating the whole curated set plus the customisation engine is a lot of unglamorous work for a niche most startups overlook. Parents pay $34.99 per book, which is less than the cost of an hour with a BCBA, and the book lasts. Print-on-demand fulfillment (via a service like Lulu xPress) makes this a one-person operation, from order to doorstep.

What we checked
✅ Are people already looking for this?
Yes — the sources back this. Confidence 0.65. (check: buyer_intent)

Multiple passages show an active, existing audience for exactly this product: sites offering '100+ free social stories' that parents can personalize and print, collections covering medical visits, hygiene and family events, and how-to guides on creating and implementing social stories for autistic children. That much material exists only because people are looking for it now; the fact that most of it is free means the demand is well-served rather than absent, which still counts as demon

Sources used: , , , , , , ,

What those sources said:

"Social stories are short stories intended for children and adults with autism to help them understand their social world and behave appropriately within it...." — https://www.otb.ie/shop/autism/writing-and-developing-social-stories/
"Social stories for children | Stranger social story, Social story about waiting, Students with autism...." — https://www.pinterest.com/pin/language-learning-canvas-course-ideas--41869471524312702/
"Discover the power of social stories for autism. Learn how to create, implement, and measure their impact effectively...." — https://neurolaunch.com/social-stories-autism/
"Free illustrated social stories designed for children with autism (ASD). Topics include social skills, emotions, daily routines, school, and transitions. Read online or print as PDF...." — https://www.growtale.org/free-social-stories/autism
"Free illustrated social stories for children with autism and special needs. Read online or download as PDF...." — https://www.growtale.org/stories
"Discover 100+ free social stories for kids with autism. Personalize each story and download printable PDFs to support social skills, routines, and emotional learning...." — https://socialstorytemplates.com/
"My Book of Social Stories is a collection of social stories aimed at helping individuals, particularly those with autism, understand various everyday activities and situations. The stories cover topics such as personal hygiene, medical visits, social interactions, and family events, each accompanied..." — https://www.scribd.com/document/821626746/social-stories-book
"A collection of free, supportive social stories to help children understand routines, emotions, and everyday situations...." — https://myneurodiversity.org.uk/social-stories-autism/
✅ Is this live right now?
Yes — the sources back this. Confidence 0.60. (check: currency)

A 2025 report puts autism at 1 in 31 U.S. children, up from the previous estimate, and 2025 commentary describes diagnosis rates as still climbing, so the pool of parents facing this problem is growing right now rather than shrinking. Passages also show current material aimed at helping autistic children prepare for specific outings such as eating at a restaurant, indicating the need for situation-by-situation preparation is live, though the passages say nothing about how many parents are buying such products today [736b8

Sources used: , , , , ,

What those sources said:

"Key findings: 1 in 31 children diagnosed with autism. The obvious finding from the 2025 report is the increased prevalence estimates compared to the previous report. The numbers released in 2025 were based on studies conducted in 2022...." — https://www.autismparentingmagazine.com/latest-cdc-autism-report/
"Autism diagnosis rates have risen over the past two decades—but why? An autism researcher explains what's behind the increase. Published. June 06, 2025. By. Public Health On Call...." — https://publichealth.jhu.edu/2025/is-there-an-autism-epidemic
"Autism is increasing and is now 1 in 31 children says HHS Secretary Robert F Kennedy Jr. in a recent press conference yesterday.One thought on “Increasing Autism Rate is Caused by Environmental Toxin Says RFK JR”. sffkeller on April 17, 2025 at 8:55 AM said..." — https://jeffreydachmd.com/2025/04/increasing-autism-rate-is-caused-by-environmental-toxin-says-rfk-jr/
"Autism has increased from 1 in a 1000 in the 1990s to 1 in 31 in 2025, a 3000% increase!1 Why is autism increasing SO much? Ever since Bob Wright, former president of NBC, became the grandfather of a child with autism and created Autism Speaks......" — https://playproject.org/why-is-autism-increasing-so-much/
"Charting the Path of Social Stories. The thoughts, perspectives, and experiences of someone with autism deserve our utmost attention and understanding...." — https://carolgraysocialstories.com/
"• Going to a Restaurant/Autism Social Skills.Helps #autistic toddlers and children overcome sensory and social challenges to enjoy dining out at a restaurant in a fun educational video!..." — https://www.youtube.com/watch?v=pOUI1rr7QDk
✅ Could a beginner reach buyers?
Yes — the sources back this. Confidence 0.66. (check: route_to_market)

Several passages describe parents of autistic children gathering in local and online support groups and dedicated ASD websites where they share advice and recommendations, which is exactly the existing-audience route a novice seller can reach without special skill. Nothing here bans marketing this kind of product: the one advertising crackdown named concerns products falsely claiming to diagnose or treat autism in the UK, and the Meta policy passages only describe general ad review, health-sector privacy changes, and hou

Sources used: , , , , , , ,

What those sources said:

"Essential Autism Parental Guidance. March 11, 2025.Parent support groups: Joining local or online support groups allows parents to connect with others who are facing similar challenges, providing a sense of community and opportunities for sharing experiences and advice...." — https://www.ambitionsaba.com/resources/autism-parental-guidance
"February 26, 2025. Autism Parental Guidance for Effective ABA.Parent Support Groups: Connecting parents with support groups or online communities can provide a valuable network of individuals who are going through similar experiences...." — https://www.thetreetop.com/aba-therapy/how-do-you-discipline-a-child-with-pda/?redirect_source=discoveryaba
"Other resources available to parents include online communities, support groups, and websites dedicated to autism spectrum disorder (ASD) support. These platforms provide a wealth of information, advice, and personal stories from other parents who have experienced similar challenges...." — https://www.abtaba.com/blog/autism-parental-guidance
"When advertisers place an order, each ad is reviewed against our policies. Our Advertising Standards also provide guidance on advertiser behavior that may result in advertising restrictions being placed on a Business Account or its assets (an ad account, Page or user account)...." — https://www.facebook.com/policies/ads/prohibited_content/
"The UK’s advertising watchdog has cracked down on products being promoted online that it says falsely promise to diagnose prostate cancer and treat autism and ADHD...." — https://www.ft.com/content/7511f62d-f888-4c60-954f-c931cacacafa
"Advertisers running housing, employment, and credit ads, who are based in the United States or running ads targeted to the United States have different sets of restrictions. See Special Ad Category...." — https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/reference/targeting-restrictions/
"In January 2025, Meta introduced significant changes to its advertising policies, particularly impacting businesses in the health and wellness sector. These updates aim to enhance user privacy......" — https://www.linkedin.com/pulse/metas-new-health-wellness-ad-restrictions-what-need-know-rahmey-lyyoe
"If restricted, your business portfolio isn't allowed to advertise. Ad account: An account used for managing ads across Meta platforms, which allows advertisers to create ads and campaigns, pay for ads, and see insights and analytics. If restricted, your ad account, its ads and some of its advertisin..." — https://www.facebook.com/business/help/975570072950669/
✅ Is it legal?
Yes — the sources back this. Confidence 0.55. (check: legality)

The passages describe U.S. rules on collecting personal information from children as a compliance regime, not a ban: a company must tell parents what it does with the data and get the parent's clear permission first, and the law's stated purpose is to give parents control over that data — here the parent is the paying customer who chooses to upload the child's name and photo. No passage describes any prohibition on selling a personalized printed product to parents, and the state-level laws mentioned are aimed at social media accounts and

Sources used: , , , ,

What those sources said:

"No. COPPA is meant to give parents control over the online collection, use, or disclosure of personal information from children. It was not designed to protect......" — https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions
"COPPA imposes certain requirements on operators of websites or online services directed to children under 13 years of age, and on operators of other......" — https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
"Jul 22, 2020... Before collecting COPPA-covered information, they must notify parents directly about their practices and get parents' express consent. They must......" — https://www.ftc.gov/business-guidance/blog/2020/07/tidying-decluttering-coppa-faqs
"Mar 28, 2026 · State-by-state guide to children's online privacy laws beyond COPPA, covering California AADC, Utah SB 152, Texas HB 18, Florida HB 3, and age verification requirements...." — https://www.recordinglaw.com/us-laws/united-states-child-support-laws/childrens-online-privacy-by-state/
"Finally, Texas recently passed a children’s privacy law directed at social media (effective July 1, 2024). Unlike the Louisiana, Utah, and Arkansas laws, the Texas law does not require verifiable parental consent for a child to have a social media account...." — https://www.loeb.com/en/insights/publications/2023/08/a-roundup-of-state-laws-related-to-childrens-privacy
⚠️ Can the claims be checked?
Can't tell — the sources don't say. Confidence 0.57. (check: claims_verifiable)

The passages show the CDC does publish retrievable U.S. autism prevalence data — a 2023 community report and a prevalence summary table for children aged 4 and 8 — so the claim is the kind of thing a public source could settle, but none of them actually states the '1 in 36' or the earlier '1 in 44' figure; one table entry is only a placeholder reading 'about 1 in X children'. The one concrete number here, 'about 1 in 127 persons' in 2021, covers all people rather than U.S. children, so it neither confi

Sources used: , , , ,

What those sources said:

"Centers for Disease Control and Prevention. CDC twenty four seven. Saving Lives, Protecting People. Autism Spectrum Disorder (ASD).Combined Prevalence per 1,000 Children (Range Across ADDM Sites). This is about 1 in X children...." — https://www.cdc.gov/autism/data-research/index.html
"This report describes autism spectrum disorder prevalence and early identifications patterns among children aged 4 and 8 years old...." — https://www.cdc.gov/mmwr/volumes/74/ss/ss7402a1.htm
"Community report on autism 2023. Autism and Developmental Disabilities Monitoring (ADDM) Network. A Snapshot of Autism Spectrum Disorder (ASD) among 4-year-old and 8-year-old Children in Multiple Communities across the United States in 2020...." — https://archive.cdc.gov/www_cdc_gov/ncbddd/autism/addm-community-report/index.html
"Centers for Disease Control and Prevention. CDC twenty four seven. Saving Lives, Protecting People. Autism Spectrum Disorder (ASD). Explore This Topic.Summary and table of prevalence of ASD among children in the United States...." — https://www.cdc.gov/autism/addm-network/index.html
"Autism – also referred to as autism spectrum disorder constitutes a diverse group of conditions related to development of the brain. In 2021 about 1 in 127 persons had autism. Characteristics may be detected in early childhood, but autism is often n......" — https://www.who.int/news-room/fact-sheets/detail/autism-spectrum-disorders
✅ Can the customer afford it?
Yes — the sources back this. Confidence 0.58. (check: payer_solvency)

The passages describe a market of parents of autistic children who already buy paid products for daily coping — sensory toys, weighted blankets and compression gear, headphones, and visual schedules — with whole storefronts and buyer guides built around selling them. Since this is the same buyer and the same kind of purchase (a modest-priced physical aid for a difficult situation), it follows that these parents have both the money and the motive to buy a $34.99 printed book; no passage suggests this group is broke

Sources used: , , , ,

What those sources said:

"Autism Products Hub 2025 | Sensory Toys, Weighted Gear & Learning Tools. Weighted Blankets & Compression.Best Headphones for Teens with Autism (2025): A Parent’s Honest Guide. Understanding the Process: What Happens After a Referral for an Autism Evaluation...." — https://101autism.com/help-us-build-emoti-sense/
"Grounding for Autism and Sensory Processing: What Parents Should Know.If you've landed here, you've probably already explored sensory diets, sleep hygiene protocols, weighted blankets, and any number of other tools...." — https://premiumgrounding.com/en-uk/blogs/news/grounding-for-autism-and-sensory-processing-what-parents-should-know
"Weighted toys, also known as sensory cuddle toys or comforters, have been carefully designed to provide a soothing and calming effect on children who struggle with sensory processing challenges...." — https://www.love-hugs.com/blogs/news/sensory-benefits-of-weighted-cuddle-toys-for-children-with-autism-adhd-and-anxiety
"May 9, 2025Jaco de Goede. (From Autism Parenting Magazine) Aggression in autistic children, such as hitting, can be a deeply challenging experience for parents and caregivers. It’s crucial to understand that these behaviors often stem......" — https://www.autismresources.co.za/blogs/one-day-at-a-time
"From sensory toys and weighted blankets to visual schedules and calming spaces, these autism parenting tips can help make daily life easier. Perfect for moms raising autistic children who need practical ideas and sensory tools...." — https://www.pinterest.com/bodytreatsbyshay/autisim-parenting-tools/
✅ Can you actually reach the customer?
Yes — the sources back this. Confidence 0.70. (check: distribution)

The passages show an existing, free-to-use online platform where anyone can design a custom full-colour children's book, have single copies printed only when an order is placed, and ship them worldwide, including a marketplace where buyers purchase directly and free Shopify/WooCommerce plug-ins for selling from your own site. That is a self-serve, no-inventory ordering and delivery path a single operator can run, though the passages say nothing about how parents of autistic children spe

Sources used: , , , , , , ,

What those sources said:

"Lulu Press Inc (also referred to as “Lulu.com,” “Lulu,” and the “Site”) is an online print-on-demand and self-publishing platform providing free-to-use tools for publishing, printing, shipping, and distributing your work for personal use and/or sale to others. Lulu’s platform includes a marketplace..." — https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf
"Apr 23, 2026 · Lulu uses print-on-demand to print your book when an order is placed. We print one, ten, or one hundred copies per order, based on how many you or your reader needs...." — https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-
"Design & create a high quality custom photo book online with print on demand options to buy or sell! Easily create a stunning hardcover photo album on premium paper...." — https://www.lulu.com/create/photo-books
"Custom book printing & creation for personal or professional use. Print a hardcover, paperback, or coil bound book! Print on demand books with global shipping...." — https://www.lulu.com/create/print-books
"Established print-on-demand platform offering specialty formats — comics, photo books, linen-wrap hardcovers, and wire-O calendars — plus free Shopify and WooCommerce integration for direct author sales. Compare pricing, features, and alternatives in the Self-Publishing Directory...." — https://selfpublishingdirectory.com/print-on-demand/lulu
"lulu children's book. Children’s Books. Bring your story to life with full-color printing and kid-friendly formats like square and landscape...." — https://www.lulu.com/create
"Children's Books.Publish, print, and sell professional-quality custom books and materials for yourself or for your business. Self-publish a book with Lulu’s easy-to-use tools and global print-on-demand network...." — https://www.lulu.com/
"Children's Books.Custom Book Printing. With print-on-demand technology, choose from thousands of trim sizes, paper types, and binding options to create a book and have your book professionally printed...." — https://www.lulu.com/create/print-books
❌ Is the problem real?
No — the sources contradict this. Confidence 0.64. (check: pain_reality)

The passages show the underlying need is widely recognized — parents and teachers use social stories to prepare autistic children for everyday situations — but every source describing how people actually get these stories points to no-cost options: free printable libraries, apps with free tiers and printable PDFs, and a site that generates a custom story with AI for free alongside 200 ready-made ones. No passage shows anyone paying money for a social story today, an

Sources used: , , , , , ,

What those sources said:

"Charting the Path of Social Stories. The thoughts, perspectives, and experiences of someone with autism deserve our utmost attention and understanding. Social Stories are not just tools; they are windows into connection, clarity, and compassion...." — https://carolgraysocialstories.com/
"Through parental guidance, children with autism can develop essential life skills, improve their communication abilities, and enhance their social interactions...." — https://www.supportivecareaba.com/aba-therapy/crucial-insights-unlocking-the-potential-of-autism-parental-guidance
"Jun 2, 2026 · We tested the top social story apps for children with autism and ADHD. Compare GrowTale, Pictello, and others — free options included, printable PDFs available...." — https://www.growtale.org/blog/best-social-story-apps-autism-2026
"May 16, 2026 · Access our free printable social stories library for children with autism, ADHD, and anxiety. Organized by topic with instructions for home and school use...." — https://www.growtale.org/blog/free-printable-social-stories-autism-library
"Free Social Stories for Kids Help your child prepare for everyday situations with simple, visual step-by-step stories. Generate a custom story with AI or browse our library of 200 ready-made stories...." — https://talaaac.com/social-stories
"Jun 28, 2026 · What social stories are, how to write one with the Carol Gray method, real examples, common mistakes to avoid, and where to get free printable social stories...." — https://www.spectrumunlocked.com/blog/social-stories-for-autism
"Customizable social story templates for teachers supporting students with autism and special needs. Includes ready-made examples and printable worksheets...." — https://www.storyboardthat.com/social-storyboards
How it scored
Overall: 2.6500 (each line is rated out of 5, then weighted)

What we rated    Score    Why
How badly it hurts (pain_acuity)    2/5    Passages show free printable libraries, apps with free tiers, and an AI-powered free story generator satisfy the need without payment, suggesting the problem is not severe enough to break spending habits.
How provable the money is (money_provability)    1/5    Although parents buy related items like sensory toys and weighted blankets, the passages show no one pays for social stories today, as free alternatives dominate.
How much one person can automate (automatability)    5/5    A print-on-demand platform supports automated order routing and single-copy printing via API, and web form-to-PDF generation is well within current capabilities, making full automation achievable today.
How easy buyers are to reach (distribution)    4/5    A print-on-demand platform supports one-off custom children's books with global shipping and e-commerce plug-ins, giving a single operator a working fulfillment path.
How hard it is to copy (defensibility)    2/5    The passages show free alternatives like printable PDFs and an AI story generator that provide similar functionality without payment, and no evidence indicates a durable moat beyond the candidate's claim of a growing library.
How buildable it is (build_feasibility)    4/5    Print-on-demand platforms provide the necessary fulfillment infrastructure, and a simple customization engine to merge templates with customer inputs is technically straightforward, indicating high build feasibility.
Why this passed
Survived all gates; composite 2.6500; 6 grounded-supported check(s) (moat grounded: 1).

Every source we used
Every claim above traces back to one of these. Follow any of them and check us.

Source
URL: https://www.otb.ie/shop/autism/writing-and-developing-social-stories/

Source
URL: https://www.pinterest.com/pin/language-learning-canvas-course-ideas--41869471524312702/

Source
URL: https://neurolaunch.com/social-stories-autism/

Discover the power of social stories for autism.

Source
URL: https://www.growtale.org/free-social-stories/autism

Free illustrated social stories designed for children with autism (ASD). Topics include social skills, emotions, daily routines, school, and transitions.

Source
URL: https://www.growtale.org/stories

Free illustrated social stories for children with autism and special needs.

Source
URL: https://socialstorytemplates.com/

Discover 100+ free social stories for kids with autism.

Source
URL: https://www.scribd.com/document/821626746/social-stories-book

My Book of Social Stories is a collection of social stories aimed at helping individuals, particularly those with autism, understand various everyday activities and situations. The stories cover topics such as personal hygiene, medical visits, social interactions, and family events, each accompanied by pictograms for better comprehension.

Source
URL: https://myneurodiversity.org.uk/social-stories-autism/

Source
URL: https://www.autismparentingmagazine.com/latest-cdc-autism-report/

Key findings: 1 in 31 children diagnosed with autism. The obvious finding from the 2025 report is the increased prevalence estimates compared to the previous report.

Source
URL: https://publichealth.jhu.edu/2025/is-there-an-autism-epidemic

Autism diagnosis rates have risen over the past two decades—but why? An autism researcher explains what's behind the increase. Published. June 06, 2025. By.

Source
URL: https://jeffreydachmd.com/2025/04/increasing-autism-rate-is-caused-by-environmental-toxin-says-rfk-jr/

Autism is increasing and is now 1 in 31 children says HHS Secretary Robert F Kennedy Jr. in a recent press conference yesterday.One thought on “Increasing Autism Rate is Caused by Environmental Toxin Says RFK JR”.

Source
URL: https://playproject.org/why-is-autism-increasing-so-much/

Autism has increased from 1 in a 1000 in the 1990s to 1 in 31 in 2025, a 3000% increase!1 Why is autism increasing SO much?

Source
URL: https://carolgraysocialstories.com/

Charting the Path of Social Stories. The thoughts, perspectives, and experiences of someone with autism deserve our utmost attention and understanding.

Source
URL: https://www.youtube.com/watch?v=pOUI1rr7QDk

• Going to a Restaurant/Autism Social Skills.Helps #autistic toddlers and children overcome sensory and social challenges to enjoy dining out at a restaurant in a fun educational video!

Source
URL: https://www.ambitionsaba.com/resources/autism-parental-guidance

Essential Autism Parental Guidance.

Source
URL: https://www.thetreetop.com/aba-therapy/how-do-you-discipline-a-child-with-pda/?redirect_source=discoveryaba

February 26, 2025.

Source
URL: https://www.abtaba.com/blog/autism-parental-guidance

Other resources available to parents include online communities, support groups, and websites dedicated to autism spectrum disorder (ASD) support.

Source
URL: https://www.facebook.com/policies/ads/prohibited_content/

When advertisers place an order, each ad is reviewed against our policies.

Source
URL: https://www.ft.com/content/7511f62d-f888-4c60-954f-c931cacacafa

Source
URL: https://developers.facebook.com/documentation/ads-commerce/marketing-api/audiences/reference/targeting-restrictions/

Advertisers running housing, employment, and credit ads, who are based in the United States or running ads targeted to the United States have different sets of restrictions.

Source
URL: https://www.linkedin.com/pulse/metas-new-health-wellness-ad-restrictions-what-need-know-rahmey-lyyoe

In January 2025, Meta introduced significant changes to its advertising policies, particularly impacting businesses in the health and wellness sector.

Source
URL: https://www.facebook.com/business/help/975570072950669/

If restricted, your business portfolio isn't allowed to advertise. Ad account: An account used for managing ads across Meta platforms, which allows advertisers to create ads and campaigns, pay for ads, and see insights and analytics.

Source
URL: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions

No. COPPA is meant to give parents control over the online collection, use, or disclosure of personal information from children.

Source
URL: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa

Source
URL: https://www.ftc.gov/business-guidance/blog/2020/07/tidying-decluttering-coppa-faqs

Jul 22, 2020... Before collecting COPPA-covered information, they must notify parents directly about their practices and get parents' express consent.

Source
URL: https://www.recordinglaw.com/us-laws/united-states-child-support-laws/childrens-online-privacy-by-state/

Source
URL: https://www.loeb.com/en/insights/publications/2023/08/a-roundup-of-state-laws-related-to-childrens-privacy

Finally, Texas recently passed a children’s privacy law directed at social media (effective July 1, 2024).

Source
URL: https://www.cdc.gov/autism/data-research/index.html

Centers for Disease Control and Prevention. CDC twenty four seven. Saving Lives, Protecting People. Autism Spectrum Disorder (ASD).Combined Prevalence per 1,000 Children (Range Across ADDM Sites).

Source
URL: https://www.cdc.gov/mmwr/volumes/74/ss/ss7402a1.htm

Source
URL: https://archive.cdc.gov/www_cdc_gov/ncbddd/autism/addm-community-report/index.html

Community report on autism 2023. Autism and Developmental Disabilities Monitoring (ADDM) Network.

Source
URL: https://www.cdc.gov/autism/addm-network/index.html

Centers for Disease Control and Prevention. CDC twenty four seven. Saving Lives, Protecting People. Autism Spectrum Disorder (ASD).

Source
URL: https://www.who.int/news-room/fact-sheets/detail/autism-spectrum-disorders

Autism – also referred to as autism spectrum disorder constitutes a diverse group of conditions related to development of the brain. In 2021 about 1 in 127 persons had autism.

Source
URL: https://101autism.com/help-us-build-emoti-sense/

Autism Products Hub 2025 | Sensory Toys, Weighted Gear & Learning Tools. Weighted Blankets & Compression.Best Headphones for Teens with Autism (2025): A Parent’s Honest Guide.

Source
URL: https://premiumgrounding.com/en-uk/blogs/news/grounding-for-autism-and-sensory-processing-what-parents-should-know

Source
URL: https://www.love-hugs.com/blogs/news/sensory-benefits-of-weighted-cuddle-toys-for-children-with-autism-adhd-and-anxiety

Source
URL: https://www.autismresources.co.za/blogs/one-day-at-a-time

May 9, 2025Jaco de Goede. (From Autism Parenting Magazine) Aggression in autistic children, such as hitting, can be a deeply challenging experience for parents and caregivers.

Source
URL: https://www.pinterest.com/bodytreatsbyshay/autisim-parenting-tools/

From sensory toys and weighted blankets to visual schedules and calming spaces, these autism parenting tips can help make daily life easier.

Source
URL: https://assets.lulu.com/media/terms-and-conditions/en/lulu-terms-and-conditions-en-111124.pdf

Lulu Press Inc (also referred to as “Lulu.com,” “Lulu,” and the “Site”) is an online print-on-demand and self-publishing platform providing free-to-use tools for publishing, printing, shipping, and distributing your work for personal use and/or sale to others.

Source
URL: https://help.lulu.com/en/support/solutions/articles/64000255305-how-does-print-on-demand-work-

Apr 23, 2026 · Lulu uses print-on-demand to print your book when an order is placed.

Source
URL: https://www.lulu.com/create/photo-books

Design & create a high quality custom photo book online with print on demand options to buy or sell!

Source
URL: https://www.lulu.com/create/print-books

Custom book printing & creation for personal or professional use. Print a hardcover, paperback, or coil bound book!

Source
URL: https://selfpublishingdirectory.com/print-on-demand/lulu

Established print-on-demand platform offering specialty formats — comics, photo books, linen-wrap hardcovers, and wire-O calendars — plus free Shopify and WooCommerce integration for direct author sales.

Source
URL: https://www.lulu.com/create

lulu children's book. Children’s Books.

Source
URL: https://www.lulu.com/

Children's Books.Publish, print, and sell professional-quality custom books and materials for yourself or for your business.

Source
URL: https://www.lulu.com/create/print-books

Children's Books.Custom Book Printing.

Source
URL: https://www.supportivecareaba.com/aba-therapy/crucial-insights-unlocking-the-potential-of-autism-parental-guidance

Source
URL: https://www.growtale.org/blog/best-social-story-apps-autism-2026

Jun 2, 2026 · We tested the top social story apps for children with autism and ADHD.

Source
URL: https://www.growtale.org/blog/free-printable-social-stories-autism-library

May 16, 2026 · Access our free printable social stories library for children with autism, ADHD, and anxiety.

Source
URL: https://talaaac.com/social-stories

Free Social Stories for Kids Help your child prepare for everyday situations with simple, visual step-by-step stories.

Source
URL: https://www.spectrumunlocked.com/blog/social-stories-for-autism

Source
URL: https://www.storyboardthat.com/social-storyboards

Customizable social story templates for teachers supporting students with autism and special needs.

Run details
Judged by: fallback(cursor_cli+claude_cli+minimax)
Market: us
Candidate ID:
Created: 2026-08-01T20:17:47.237331+00:00
Evidence goes stale after: 2026-08-31T20:17:47.237331+00:00
Every factual claim in this pack cites a retrievable source.

Pack ID: 8d5e24fbe6c1f5d3 these packs are no where near ready nneeds 50x inprovenent and narkdown files is not the one
