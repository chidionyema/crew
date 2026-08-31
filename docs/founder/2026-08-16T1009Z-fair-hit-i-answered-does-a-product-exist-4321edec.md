---
captured: 2026-08-16T10:09:34+00:00
session: 30ddb23e-b972-4f17-8298-f0630c524826
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2541
source: founder prompt, verbatim (founder-doc-capture.py)
---

Fair hit. I answered “does a product exist” when you asked “how do I solve it”. The corpus route is right, and there’s a near-perfect one sitting in public.

Financial Ombudsman Service final decisions. Every final decision published since April 2013, in a searchable and downloadable format — over 384,000 of them, across banking, insurance, mortgages, investments, pensions and consumer credit, each carrying an outcome of upheld or not upheld, with the full text as a PDF. They’re anonymised and written so the complainant can’t be identified.

Why it’s the right corpus rather than just a large one: it’s the same genre you’re generating. A claim, the evidence considered, a verdict, reasons. Written by a professional for a lay reader who may be about to disagree with them. UK English, no marketing register, no house-style flourish, and the writer is legally accountable for every sentence — which is exactly the constraint your packs claim to operate under. Nothing else public matches that shape at that volume.

Secondary, for the narrative sections: Legal Ombudsman decisions, ASA adjudications, and GOV.UK guidance (Open Government Licence, so no licensing question). Check the FOS terms before you train on it rather than just measure from it — measuring is a much safer footing than fine-tuning.

Then the actual reverse-engineering, which is keyness analysis. Build two corpora: 500k words of FOS decisions, and 500k words of your own generated packs. Tokenise both, then rank every word and n-gram by log-likelihood ratio between them. What falls out is an empirical list of what your generator over-uses relative to a human writing the same genre — not my guesses, not a blog’s list of AI words. Yours. Standard corpus linguistics; AntConc does it out of the box, or fifty lines of Python with spaCy and scipy.

Do the same for the structural distributions rather than the vocabulary. Sentence length mean and σ, clause counts, paragraph length, opener diversity, hedge density per thousand words, punctuation rates, attribution density. You now have a target distribution instead of a rule I invented. Generated output gets scored against it and fails outside the human corpus’s interval.

That’s the loop that ends this: not a linter someone else wrote, a measured target with a distance metric. And it retrains itself the moment you swap the corpus for a different genre.

  also did we inplenet this as part of our pack corpus and  sitewide language and tone tinprovenent , if not nneeds analsis and spec and build also]
