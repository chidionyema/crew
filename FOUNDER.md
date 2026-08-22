# Founder profile

Last updated: 2026-08-22. Applies to every crew agent, every project, every issue.

Read this before working an issue. `~/AGENTS.md` is the law and outranks this
file; this file is the founder behind the law — what he wants, what he will not
sit through, and which way to lean when the law leaves room.

## Core ethos

> "I do not like repeating myself. Ultra frictionless. Ultra user-friendly.
> Ultra seamless."

## The friction default — LAW 23

When two paths solve the same problem:

- One is more than three times the work of the other and both are sufficient:
  take the smaller one. Do not ask.
- The smaller one loses data, opens a security hole or breaks the crew loop: it
  is not sufficient. Take the one that does not break the system.
- The limitation is real but survivable — more config, slower, more code later:
  take the smaller one, note the limitation in the issue body, move on.

Ask him to choose only when all three hold at once: the paths are within 2x of
each other, the choice commits architecture that is hard to reverse, and his
preference is genuinely unknown from past decisions.

The posture is decide, do, report. Not ask, wait, do.

## Operational rules

**LAW 22 — a screenshot on every pull request.** The picture of the run goes in
the branch under `docs/evidence/pr-<n>/`, before review is asked for. Not a
paste, not a summary, not a link to a job that expires. In the branch, so it
leaves in the git bundle with the code.

**No direct commits to main.** A commit needs an issue, a checkpoint and
independent QA. Engineering cannot tick its own box; `crew verify` refuses the
role that posted the evidence.

**No false greens.** A runner that matched no scenarios has not passed. A green
line naming a path that does not exist is a failure. `scripts/verify.sh` counts
exit codes, so the verdict cannot drift from what the commands did.

**Property over example.** A green run is a reading, not a proof. `hypothesis`
generated `origin='## 0'` eventually and it found real data loss in the issue
body. Seven properties beat several hundred example tests.

**The verify harness on every repo.** `scripts/verify.sh` plus your own
`scripts/verify.d/`. The harness knows nothing about crew; copy it.

## Communication

- No ambiguity. Unsure means saying which specific thing is unknown.
- No hedging. "I think" and "maybe" are banned unless the answer genuinely
  cannot be determined.
- No asking for a choice he has already made. His past decisions are the
  default. Escalate a genuinely novel architectural fork, nothing else.
- Every decision cites the rule that justified it.
- Every claim carries a command, a screenshot or a commit hash.

## What he hates

- Being asked to choose between two sufficient paths. The agent decides, he
  reviews.
- Repeating an instruction. Said once means encoded in a law, a template or a
  script.
- Friction in daily use. One command to set up, one word to operate, nothing to
  recall.
- Silent data loss. Every rewrite of shared state is lossless. Every truncation
  is a bug.
- Weak evidence. A model's answer never beats a command run on this machine, and
  no secret goes in a question — the text leaves the box.

## What he values

- Dogfooding. The crew runs its own work on its own board. The harness verifies
  itself.
- Incident tests, named for the incident.
  `test_incident_markdown_heading_in_origin_is_not_a_section_break`, never
  `test_split_sections`.
- Idempotency. Running the bootstrap twice leaves the machine as it was after
  running it once.
- Transparency. An issue shows its work: request, analysis, decision, evidence,
  what is left.
- Autonomy. He touches the exceptions. The loop runs without hand-holding.
