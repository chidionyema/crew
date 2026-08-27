# R34: the new research and science paradigm (founder directive, 2026-08-25)

Founder, 2026-08-25, verbatim, as posted to the crew:

> We are changing our approach entirely.
>
> I want to be clear on our vocabulary moving forward: we are officially banning the words
> "refactor," "rewrite," or "update" regarding the engine. We are not cleaning up duct tape. We
> are introducing a net-new paradigm to build a world-class, autonomous research and science
> capability that can be purposed to any part of the platform.
>
> 1. The Architecture (How we build)
> From "Opaque" to "Verifiable": We are done just generating text. From now on, every single
> claim must have a per-claim source reference tied to an append-only, object-locked R2 bucket.
> We must be able to prove exactly what the internet looked like the second the AI read it.
> From "Vibes" to "Science": We used to guess if the AI was right based on spot-checks. Now, we
> use MLflow and standard Data Science primitives (Brier scores) to mathematically prove our
> accuracy against real-world outcomes.
> From "Duct Tape" to "Enterprise-Grade": We are officially stopping the hand-rolling of
> distributed systems. We are adopting the exact same foundation-backed science plane (Argo,
> MLflow, Kubernetes) used by top-tier ML teams.
>
> 2. The Measurement (How we prove we are better)
> Comparing our new engine to the old generated dossiers is like measuring a spaceship by how
> well it pedals. "Differential replay" against the old system is dead.
> The Golden Corpus: We are no longer benchmarking the new AI against the old AI. We are
> benchmarking against reality and human expert consensus. We are building a Golden Corpus of
> 50-100 perfect, hand-researched dossiers. The only metric that matters is: How closely do we
> replicate the human expert?
> Calibration is the Moat: Every check is a forecast. When reality resolves that claim, we score
> it. When a buyer asks how good our system is, we will hand them a mathematical calibration
> curve, not a block rate.
>
> TL;DR: We realized our old architecture couldn't prove it was right; it could only generate
> text. To build a world-class autonomous research capability, we didn't just need better
> prompts. We needed an entirely new scientific foundation where every claim is verifiable, every
> source is locked, and every model is calibrated against reality.

## Requirements, as held

1. Vocabulary: "refactor", "rewrite", "update" are banned for the engine. It is net-new.
2. Every claim carries a per-claim source reference into an append-only, object-locked R2
   bucket holding the fetched bytes at read time.
3. Every check is a forecast; resolved against reality; Brier scored; tracked in MLflow.
4. Science plane is Argo Workflows + MLflow + Kubernetes. No hand-rolled distributed systems.
5. Differential replay against the old engine is dead. Old dossiers are not a yardstick (R32).
6. A Golden Corpus of 50-100 hand-researched dossiers is the second yardstick: closeness to
   human expert consensus.
7. The buyer-facing quality artefact is a calibration curve.

## Friction points named, not resolved here

- Requirement 6 versus R32 and R35 behaviour 1. R32 says the engine should generate ideas that
  beat what any human on the old process produced; "how closely do we replicate the human expert"
  measures agreement with humans, which caps the engine at the expert. Held resolution, pending
  founder confirmation: the Golden Corpus grades the *checks* (facts, sources, claims) against
  expert consensus; the *hypotheses* are graded only by reality (Brier). Two yardsticks, two
  jobs, and the second cannot be capped by the first.
- Requirement 6 cost. Founder, 2026-08-25, second message: "no founder friction, research
  online for existing dossiers, you should be recommending." Resolved: the crew builds the
  Golden Corpus itself, by online research with locked sources. The target list is the titles of
  existing dossiers (topics only; their content is never read, R32). Recommendation, adopted:
  first 10 are the 10 most recent dossier titles, each researched from primary public sources,
  every claim carrying its R2 object key; a dossier enters the corpus only when two independent
  runs (different models) agree on every fact, and a disagreement is a finding, not a tie-break.
- Requirement 4 versus the STANDARDS.md rows for scheduling and traces: they must name Argo and
  MLflow as the one answer, or the rows are wrong. To be reconciled in the standard.
