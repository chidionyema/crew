# Decision archive

Precedent. Before asking him anything, read this — the answer is usually a line
already in it. Cite the entry by number when you apply it.

`~/AGENTS.md` is the law. [`FOUNDER.md`](FOUNDER.md) is how he works.
[`PREFERENCES.md`](PREFERENCES.md) is what he reaches for by default. This file
is what was actually decided, and when.

## Format

`DATE | CONTEXT | WHAT I DID | WHY | WHAT I REJECTED | RULE EXTRACTED`

## Entries

**1. 2026-08-22 | crew loop wiring**
Chose a pytest adapter over Gherkin feature files. 40 lines against a much
larger build, both sufficient. Rejected: Gherkin describing python.
→ *Take the smallest sufficient path. Do not ask.* (LAW 23)

**2. 2026-08-22 | DNS migration**
API first, browser last. Only the registrar paste is manual, because no API
covers it. Rejected: "log in to Cloudflare and tell me what you see".
→ *A browser step is a bug. Use the API. The only manual step is the one no API
exists for.*

**3. 2026-08-22 | issue triage**
`crew-triage` writes the full context into the issue body. No agent picking the
work up should ever have to ask what was originally requested. Rejected: short
issue bodies.
→ *Every issue carries origin, analysis, decision, evidence, remaining.*

**4. 2026-08-22 | notification**
A desktop fallback rather than waiting for hermes. Rejected: "wait for
Hermes V2".
→ *A downstream dependency is not a blocker. A fallback is mandatory.*

**5. 2026-08-22 | verify harness**
`scripts/verify.sh` counts exit codes and prints `PASS=n FAIL=n`. Rejected: a
human-written summary of what happened.
→ *Raw output only. A number cannot drift from what ran; a sentence can.*

**6. 2026-08-22 | incident tests**
Named the test after the bug:
`test_incident_markdown_heading_in_origin_is_not_a_section_break`, for silent
data loss in the issue body. Rejected: `test_split_sections`.
→ *Every bug gets one incident test, named for the incident.*

**7. 2026-08-22 | the installer**
His draft wrote a bash script over `~/.local/bin/crew`, a symlink to the python
CLI, deleting all twelve loop verbs. Kept the draft's shape and made the wrapper
exec the CLI for any verb it does not own. Rejected: two commands, and dropping
the local verbs.
→ *One word for the whole job. A wrapper that shadows the thing it wraps is a
deletion.*

**8. 2026-08-22 | the lab lease**
`scripts/lab-lease.py` existed and nothing called it, so it protected nothing.
Called it from `features/environment.py` and `scripts/dry-run.sh`. Rejected: a
docker-level lock, and a lock file per test.
→ *A guard nothing calls is not a guard. Wire it at the entry point.* (LAW 3,
LAW 23)
