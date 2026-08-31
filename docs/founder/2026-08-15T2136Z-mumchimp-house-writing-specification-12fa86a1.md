---
captured: 2026-08-15T21:36:16+00:00
session: 1d10f0b0-43d4-427f-82c2-251c6f75cac0
cwd: /Users/chidionyema/Documents/code/prospector
chars: 13418
source: founder prompt, verbatim (founder-doc-capture.py)
---

# Mumchimp — house writing specification

For the generation pipeline and the editing pass. Every rule is testable. Every example is taken from the live sample at mumchimp.com/sample.

The target register is **trade journalism**: Construction News, Building, Farmers Weekly, the FT's sector desks. Not blog, not consultancy deck, not textbook. A trade reporter writes for a reader who knows the industry and has ten minutes, is legally exposed if they invent a figure, and has a subeditor who will cut any sentence carrying two ideas.

---

## PART ONE — THE PARAGRAPH MODEL

Trade reporters build a paragraph the same way every time:

1. **One fact per sentence.** If a sentence contains two facts, it is two sentences.
2. **Attribution rides with the fact, in the same sentence.** Not collected at the end of the paragraph, not implied by a link.
3. **The actor is the grammatical subject.** Somebody does something to somebody. Not "the collapse of large main contractors has left retention money trapped" but "large main contractors collapsed, and retention money is trapped in their estates".
4. **Figures carry a unit, a date and a source, or they do not appear.**
5. **Paragraphs run two to four sentences.** A fifth sentence means a new paragraph.
6. **No forward references.** Never "as discussed below" or "this shape decides more than it looks like it does".

---

## PART TWO — HARD RULES

Numbered so the editing pass and the linter can cite them.

**R1.** Maximum 28 words per sentence. Target average 16–18.

**R2.** Maximum two clauses per sentence. No semicolons in claim text.

**R3.** One factual claim per sentence.

**R4.** Maximum three items in any parallel construction. Four-item lists are the strongest single tell of generated prose.

**R5.** Every sentence containing a figure names its source in the same sentence.

**R6.** No quantity word without a quantity. Banned unless a number follows: *significant, substantial, numerous, considerable, a trail of, dozens of, a fraction of.*

**R7.** Active voice, named actor. Nominalisations get unpacked.

**R8.** No sentence may begin with `that`, `which`, `and that`, or `so that`.

**R9.** Banned register — replace or cut:

> wedge · compounds · leverage · landscape · ecosystem · robust · seamless · unlock · durable advantage · moat · flywheel · at scale · game-changing · increasingly · rapidly evolving · it is worth noting · delve · foster · underscore · pivotal · crucial · testament to

**R10.** Any claim about the future or about competitor behaviour is either sourced, or labelled as an assumption in the assumptions block. It never appears as flat assertion.

**R11.** The pack's own one-line description appears exactly once per document.

---

## PART THREE — QUOTE HANDLING

Journalism has settled conventions here, and your current output breaks all of them. This section matters more than the prose rules, because quotes are the evidence proposition.

**Q1.** A quote is a complete grammatical unit. Minimum eight words, must parse as a sentence or a clean clause.

**Q2.** Never splice. Two retrieved fragments joined by a full stop or an ellipsis is not a quote. If the retrieval returns fragments, paraphrase and cite instead.

**Q3.** No navigation text, no meta descriptions, no SEO boilerplate, no cookie banners, no "Logo" strings. If the passage names the site in the third person, it is boilerplate.

**Q4.** Attribution format: publication, then date where the page carries one.

**Q5.** If no clean quote exists, say so. "We found no page stating this in its own words" is publishable. A mangled quote is not.

### Failing quotes currently on the sample page

> "retention and their effects on construction subcontractors in the UK. chasing the final retention on its due date."

Two fragments, neither a sentence, joined by a full stop. Fails Q1 and Q2. **Replace with:** a one-sentence paraphrase of the paper's finding, cited to ResearchGate with its date.

> "Payapps Logo Payapps Software Review 2026: Features, Integrations, Pros & Cons."

Page furniture scraped from a listing site. Fails Q3. **Cut entirely.** Capterra's category page is not evidence that a competitor serves this market.

---

## PART FOUR — BEFORE AND AFTER

All "before" text is live on the sample page today.

### 1. Broken clause chain after a question stem

**Before**
> **Is the problem real?** Main contractors in the UK routinely withhold a percentage of subcontractors' money — commonly 5% of the subcontract sum — until milestones are met, that unpaid subcontractors cause serious cash flow problems, and that Carillion's 2018 collapse left a trail of unpaid retentions with money outstanding across the UK.

The governing verb ("We found that…") was dropped and the sentence never recovered. Two orphan `that` clauses. Also fails R6 — "a trail of" with no number.

**After**
> **Is the problem real?** Yes. Main contractors commonly hold back 5% of the subcontract sum until milestones are met. That money is a recognised cause of cash-flow failure among subcontractors, according to [source]. When Carillion collapsed in 2018 it left £[X]m of unpaid retentions outstanding, [source] reported.

Four sentences, one fact each, every figure attributed. If the Carillion figure cannot be sourced, the sentence is cut — not softened.

### 2. The four-item escalating list

**Before**
> The courts and the regulator can publish guidance and run free first-party templates, but they cannot run a commercial retention chaser, cannot take a commercial side against a main contractor, cannot hold the cross-main-contractor dataset that RetainRelease builds, and cannot serve the subbie adversarially to the duty-imposer.

Fails R4. The fourth item invents vocabulary ("adversarially to the duty-imposer") to fill the rhythm — the model had run out of content but not out of pattern.

**After**
> Courts and regulators publish guidance and free templates. Neither will chase a subcontractor's money for them, and neither takes sides in a payment dispute.

Two sentences, 26 words, nothing invented.

### 3. Everything in one sentence

**Before**
> The FMB/CIOB State of Trade Survey shows UK construction SMEs are still growing, though momentum is slowing, so these firms are trading businesses rather than failing ones; and with the UK sector reported at the world's lowest average margin of 3.9%, a 3-5% sum held back is worth more than a typical job's entire profit, which gives owners a strong reason to chase it.

66 words, four facts, a semicolon, three subordinate clauses. Fails R1, R2, R3.

**After**
> The FMB/CIOB State of Trade Survey reports that construction SMEs are still growing, though more slowly than last year. These are trading firms, not failing ones. Average margin across the sector is 3.9%, the lowest of any major market, [source] reported in [year]. A retention of 3–5% is therefore worth more than the entire profit on a typical job.

Four sentences, 62 words. Barely shorter — the gain is that a reader can disagree with each sentence separately, which is the whole point of the product.

### 4. Deck vocabulary asserting an unverified claim

**Before**
> The durable wedge is the proprietary dataset of main contractor retention release behaviour. […] Late copiers cannot catch up because the data compounds with every contract.

Fails R9 twice and R10. "Late copiers cannot catch up" is a prediction dressed as an observation, on a site whose proposition is that nothing here is invented. This is the most damaging category of error you have.

**After**
> Each release produces a record of how one main contractor behaved: paid on time, disputed, or paid only after adjudication. Whether that record is hard for a competitor to rebuild, we did not test.

The second sentence is the product working as advertised. It should appear far more often than it does.

### 5. Nominalisation with the actor buried

**Before**
> The collapse of large main contractors since 2018 (Carillion, Berkeley, ISG, numerous mid-tier firms) has left retention money trapped in insolvent estates, with subbies waiting years for a fraction of what they are owed.

Fails R6 twice ("numerous", "a fraction of") and R7.

**After**
> Carillion, ISG and other large contractors have gone under since 2018. Their subcontractors' retention money sits in the insolvent estates, where secured creditors are paid first. [Source] found subcontractors waiting [X] years and recovering [Y]%.

Named actors, active verbs, and the vague quantifiers replaced with figures or cut.

---

## PART FIVE — PIPELINE SPEC

The single biggest cause of the failures above is that retrieval and prose happen in one pass. The model tries to discharge all its evidence inside one sentence. Split it.

### Stage 1 — Extract

Output structured data only. No prose.

```json
{
  "claim": "Main contractors commonly hold back 5% of the subcontract sum",
  "figure": { "value": 5, "unit": "percent", "of": "subcontract sum" },
  "source_url": "https://…",
  "source_name": "…",
  "source_date": "2024-03-11",
  "quote": "…",            // null if no clean quote (see Q1–Q3)
  "confidence": "high|medium|unsettled"
}
```

Rule: if `figure` is present and `source_url` is null, the record is dropped. Not softened — dropped.

### Stage 2 — Write

Prompt fragment:

> Write from the supplied claim records only. One claim per sentence. Maximum 28 words per sentence, maximum two clauses, no semicolons. Every sentence containing a figure names its source in that sentence. Never use more than three items in a list. Never begin a sentence with "that" or "which". If a claim record is marked unsettled, write it as unsettled — do not assert it.
>
> Register: UK trade journalism. Named actors, active verbs, concrete nouns. No business-strategy vocabulary.
>
> Below are four paragraphs in the target voice. Match them.
>
> [paste four paragraphs of Chidi's own chrome copy]

The exemplars do more work than the instructions. "Sound more human" gives the model nothing to aim at. Your own sentences give it a target.

### Stage 3 — Edit

A separate pass that receives the draft *and the rule list*, and is asked to cite the rule number for each change. Rule citation forces it to find actual violations rather than reword at random.

### Stage 4 — Lint

Fails the build. See Part Six.

---

## PART SIX — VALE RULES

`.vale.ini`

```ini
StylesPath = styles
MinAlertLevel = warning
Packages = proselint, write-good

[*.md]
BasedOnStyles = Vale, Mumchimp, proselint
```

`styles/Mumchimp/SentenceLength.yml`

```yaml
extends: occurrence
message: "Sentence over 28 words (R1). Split it."
level: error
scope: sentence
token: '\b\w+\b'
max: 28
```

`styles/Mumchimp/Semicolon.yml`

```yaml
extends: existence
message: "Semicolon in claim text (R2). Use a full stop."
level: error
tokens:
  - ';'
```

`styles/Mumchimp/Register.yml`

```yaml
extends: existence
message: "'%s' is banned register (R9)."
level: error
ignorecase: true
tokens:
  - wedge
  - compounds?
  - leverage
  - landscape
  - ecosystem
  - robust
  - seamless
  - unlock
  - moat
  - flywheel
  - at scale
  - game.changing
  - increasingly
  - delve
  - foster
  - underscores?
  - pivotal
  - testament to
```

`styles/Mumchimp/VagueQuantity.yml`

```yaml
extends: existence
message: "'%s' with no figure (R6). Give the number or cut the sentence."
level: error
ignorecase: true
tokens:
  - numerous
  - a trail of
  - a fraction of
  - dozens of
  - significant(ly)?
  - substantial(ly)?
  - considerable
```

`styles/Mumchimp/OrphanClause.yml`

```yaml
extends: existence
message: "Sentence begins with a relative pronoun (R8)."
level: error
raw:
  - '(?m)^\s*(That|Which|And that|So that)\b'
```

**What Vale cannot check** — put these in a pipeline validator instead:

- Quote length and grammatical completeness (Q1)
- Fragment splicing (Q2)
- Boilerplate detection (Q3) — flag quotes containing the source domain name, "Logo", "Review 20", "Pros & Cons", "Features,"
- Parallel-list item count (R4) — needs a parser
- Figure-without-source (R5) — regex a number, then check for a link in the same sentence
- Duplicate paragraph detection (R11)

---

## PART SEVEN — EXEMPLAR CORPUS

Feed the writing stage real examples, not adjectives. In priority order:

1. **Your own chrome copy.** Highest value, because it is already the house voice and already approved. Four to six paragraphs.
2. **Trade press in the relevant sector.** Construction News and Building for the construction packs; the equivalent title for each category. One or two paragraphs, refreshed per pack.
3. **Reuters or FT company coverage** for the attribution habit — every figure sourced in-sentence, no editorialising.

Do not use general business blogs, Medium, LinkedIn, or consultancy reports. They are the source of the register you are trying to remove.

---

## REVIEWER CHECKLIST

- [ ] No sentence over 28 words
- [ ] No semicolons in claim text
- [ ] Every figure has a source in the same sentence
- [ ] No four-item lists
- [ ] No banned register terms
- [ ] Every quote is a complete grammatical unit of eight words or more
- [ ] No quote contains page furniture or the site's own name in third person
- [ ] No sentence begins with "that" or "which"
- [ ] No prediction stated as fact
- [ ] The pack description appears once

 needs rigorous adotio and enforcing acros the platforn  neds ddep analysis and review
