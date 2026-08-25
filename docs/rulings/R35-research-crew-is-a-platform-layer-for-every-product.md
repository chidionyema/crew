# R35: the research, science and ML crew is a platform layer that serves every product

Founder, 2026-08-25, verbatim: "how does the research science and machine learning crew engage
with the rest of the platform, they are here to exponentially improve all parts of the estate
including prospector, the capabilities need to be world class on their own and can be purposed to
any part of platform and beyond as we add new product and capabilities."

Then: "i need to be certain we are on the same page and you dont drift."

## Requirements, as held (founder to confirm or correct each line)

1. The research/science/ML capability is a platform layer in `idp`, on the same row as model
   routing and traces. It is not a prospector feature and not a prospector module.
2. Its job is to improve every part of the estate, prospector included, not one product.
3. It must be world class judged on its own: measured by its calibration ledger (Brier per
   source), not by any product's revenue.
4. It is purposed to any target by one contract: a target at a scale (company, market,
   product, component, estate). No question is asked of it; it generates the hypotheses,
   designs and runs the experiments, and explains in one sentence.
5. A new product or capability joins by adding a catalog entity. No integration work.
6. Prospector is customer one (R31). Old outputs are a baseline beside it, never an input (R32).
7. Provider-agnostic (LAW 34): prompt is a file, runner takes a model name.

## How it engages the rest of the platform

- In: a `research` issue naming a target; a call `research generate <target>`; a scheduled
  sweep over the Backstage catalog.
- Out: a doc in the owning repo, a ticket on the owner's board, traces in the estate collector,
  every prior written to the estate-wide forecast ledger.
- Loop: resolved forecasts are scored; the generator with the lower Brier is promoted for
  every product at once. That is the exponential part, and it is one ledger, not one per product.

## Drift guard

Any step-1 or later deliverable under #221/#242 that names prospector in the prompt, the runner,
or the ledger schema is drift. `rg -n prospector docs/research-engine/PROMPT_generate.md` must
return nothing.
