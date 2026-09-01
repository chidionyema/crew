# crew#659 reset — Research Engine v2: walking skeleton first

Founder, 2026-09-01, verbatim. Record: `~/.claude/docs/founder/2026-09-01T1221Z-add-to-both-boad-reseach-lanes-repo-and-62c4d187.md` (claude-estate repo). Board: https://github.com/chidionyema/crew/issues/659

**Status:** PROPOSED — no crew work starts until the founder rulings in §6 land.
**Supersedes:** the current crew#659 CP1–CP5 definitions. Amends R34 (pending ruling 6.1).
**Lane:** research. **Owner:** unassigned until CP0 mode is ruled (6.4).

---

## 1. Why the reset

The engine graded GAP because governance was built around a vacuum: an input
registry (the catalogue) and an output bureaucracy (grade pages, checkpoints)
with nothing in the middle. Generality lives in the representation of research
itself, not in enumerating subjects. The 2026-08-30 incident (worker out of
credit, routed to MiniMax/Groq, shipped reports with no sources) proved quality
is currently enforced nowhere structural. This ticket fixes both: a claim
ledger as the spine, and provenance as an admission gate rather than a model
policy.

## 2. The invariant (non-negotiable, applies from CP1 forward)

**No claim enters the ledger without provenance.** Admission requires all of:

1. ≥1 source with a snapshot stored in R2, URL resolved at retrieval time;
2. a locator (quote or offset) tying the statement to the snapshot;
3. a verifier model **distinct from the producer** returning `supported`.

Rejected claims are kept and counted — degradation surfaces as a throughput
drop, never a silent quality drop. Model choice becomes a cost dial; the gate
is the quality floor. This is the class-level elimination of the sourceless-
report incident. No lexical or model ban-lists (founder ruling, 2026-09-01):
gates judge output in context, not inputs by name.

## 3. Data model

**Claim** — `id` (content hash of statement+sources+retrieved_at) ·
`statement` (one sentence, falsifiable) · `question_id` · `target_id` ·
`sources[] {url, retrieved_at, snapshot_ref, locator}` ·
`producer {model, version, run_id}` ·
`verification {verifier_model, verdict: supported|contradicted|not_found, checked_at}` ·
`confidence` (derived, never asserted) · `status: admitted|rejected`.

**Question** — `id` · `target_id` · `text` · `profile_id` ·
`posture` (default **disproof**: phrased as a hypothesis to kill) ·
`status` · `answered_by[]` (claim ids).

**Artifact** — synthesis text + `manifest[]` of admitted claim ids only ·
`renderer_profile` · grade attached exclusively by the grader session.

**DeliveryEvent** — emitted by the *consumer* on use (verdict issued, pack
sold, founder decision citing a claim id). Outward grade is computed from
these and nothing else.

**Storage:** Postgres = system of record (outbox-ready per the backbone spec) ·
R2 = snapshots + artifacts · ClickHouse = metrics. **No MLflow. No Windmill.**

## 4. Pipeline

`compile → retrieve → extract → verify → synthesize → grade`

- **compile**: profile × target → question set. The catalogue is one target
  adapter; external subjects (a market, a company) are another. ClickHouse
  telemetry is a *source adapter*, not a lane — science-facts folds in here.
- **retrieve**: three-tier search (SearXNG → DDG → metered), snapshot to R2.
- **extract**: producer model → candidate claims with locators.
- **verify**: cross-model entailment — does the snapshot actually support the
  statement? Verifier ≠ producer, enforced in code, logged per claim.
- **synthesize**: admitted claims → artifact + manifest.
- **grade**: separate credentialed session signs the verdict. Workers have no
  write path to grades (verification-plane pattern).

CP1 runs this as **one process** with stages as functions. Stage boundaries
are the future JetStream consumer boundaries; the schema is fixed now so the
CP2+ split is mechanical, not a rewrite.

## 5. Checkpoints (replace existing CP0–CP5)

**CP0 — Trace capture.** One target, run by hand per ruling 6.4, every step
recorded to `docs/research-engine/TRACE-<target>.md`: the questions asked,
searches run, sources kept/discarded, claims formed, the artifact. The trace
*is* the pipeline spec. Exit: founder receipt. (This converts the crew#508
condition — "I run the lane myself" — into the requirements-capture step.)

**CP1 — Skeleton.** `make skeleton TARGET=<id>` reproduces the trace end to
end: questions compiled, sources snapshotted, every claim through the §2 gate,
one artifact with a manifest. Exit: a second session independently resolves
every claim id → snapshot → verifier log and signs; founder word to merge
(R60). Target: inside one week of CP0 receipt.

**CP2 — Staging.** The skeleton runs on the staging cluster via idp as a
scheduled job. Same evidence, re-signed from cluster reads in the same turn.

**CP3 — Profile #1: prospector.** Contingent on ruling 6.2. Prospector's
disproof loop expressed as a profile; its verdicts consume engine claims and
emit DeliveryEvents on use. Revenue becomes the built-in outward signal.

**CP4 — Unattended volume.** Catalogue sweep live; N targets/week with no
hand on it. Admission and rejection rates on the grade page straight from
ClickHouse — measurements, not testimony.

**CP5 — Outward reality.** Grade page computes Outward from DeliveryEvents
only; first external consumption recorded (a pack sale, a verdict used, a
founder decision citing a claim id).

Every CP handoff carries `Built: / Use: / Expect: / Not done: / Evidence:`;
DONE additionally carries `Founder receipt:` (DoD v2.1). No CP self-certifies.

## 6. Founder rulings requested (blocking)

- **6.1 — R34 amendment.** Stack = Postgres + ClickHouse + R2, JetStream from
  CP2/3. MLflow and Windmill removed. Argo deferred until sweep fan-out
  measurably exceeds what a JetStream consumer group handles.
- **6.2 — One project.** The prospector core rebuild and this engine are the
  same build; prospector is profile #1, not a customer. (Alternative if
  declined: engine ships standalone, prospector integrates later at higher
  total cost.)
- **6.3 — Lane inference budget.** Flat-rate provider assignment for the lane
  so credit exhaustion cannot recur as an incident trigger; name the
  producer/verifier model pairing.
- **6.4 — CP0 mode.** Founder-run trace with a session scribing (default), or
  crew-run under live founder receipt.

## 7. Non-goals for this ticket

Mumchimp renderer (follow-on once CP3 proves the profile mechanism) · any UI ·
Argo · MLflow · Backstage sweep automation before CP4 · phrase blocklists in
the grader.

## 8. Charter wording fix (in place, no ban-list)

Replace "…one-sentence explanation, for any catalogue target" with:
"…one-sentence explanation, for any subject we register — a product, a
service, a market, a company, or the estate itself."

## 9. What counts as progress

`claims admitted/day` · `rejection rate` · `time-to-artifact` ·
`delivery events/week`. Charters, grade scaffolding and checkpoint edits do
not count. Admitted claims do.
