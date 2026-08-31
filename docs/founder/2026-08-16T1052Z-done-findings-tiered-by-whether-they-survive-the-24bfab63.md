---
captured: 2026-08-16T10:52:22+00:00
session: c7d73d37-dddd-4acd-8985-f080f2495f85
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2171
source: founder prompt, verbatim (founder-doc-capture.py)
---

DONE: Findings tiered by whether they survive the genre difference, and the platform integration plan is written down. Commit 382400e, pushed to PR #236.

You're right that FOS adjudicates disputed facts between two parties and we don't. So only some of it transfers:

Tier A — act on these. Genre-independent, wrong in any register: hyphens at 12x, the passages / the passages meta-commentary (we describe our own retrieval instead of the world), comma and semicolon density, and retiring the 25-word ceiling because it's stricter than professional English.

Tier B — direction right, number wrong. Hedging. We're 4x more assertive than a writer accountable for the verdict, which matters. But an ombudsman hedges because facts are contested and both parties read it, and we already have unverifiable for what we don't know. No gate until a target between 3.5 and 13.6 has an argument next to it.

Tier C — don't touch. The vocabulary finding is now labelled a hypothesis, not a finding: type/token falls as documents grow and ours average ~654 words against FOS's ~1,724. The check that settles it is written down and not run — you stopped that probe. Paragraph length is a builder artefact. And uk, nhs, ai, data in the keyness table are subject matter; a rule cut from them would ban what we write about.

Three surfaces, three genres, no shared target: packs take FOS; the storefront needs its own corpus before any gate; ops surfaces are out of scope.

Production fences, written down before anything gates a run: the target is a committed versioned artifact, lint time does no network I/O, the target carries the corpus fingerprint that produced it, a test fails when shipped target and reader disagree, and enforcement arms per measure — Tier A may arm, B and C may not.

Next is stage 6, Tier A only: delete the two invented constants in register_lint.py:353-355 and read measured intervals, behind those fences.

Safe point — type /clear (state saved, nothing will be lost). just to be clear we need to integrate as nuch as possible wwith the only nuance that we are no juding conplaints hunan writing patterns is what we need to adopt ad enforce not conplaints
