# Preference profile

What he reaches for when nothing forces the choice. Not law — [`FOUNDER.md`](FOUNDER.md)
and `~/AGENTS.md` are. This is the default when the law is silent.

## Communication

- No hedging. "I think", "maybe", "perhaps" are banned unless the uncertainty is
  real, and then the exact uncertainty gets named.
- Lead with the answer. The reasoning comes after it.
- One sentence beats one paragraph.
- Raw output beats a summary. Paste what the command printed; do not describe
  it.

## Decisions

- Sufficient now beats perfect later.
- Working code beats a comprehensive design document.
- One working example beats ten hypothetical cases.
- If it can be a script, it must be a script.
- 40 lines today beats 400 lines next week.

## What makes him angry

- Being asked to choose when one path is obviously smaller.
- A summary where the raw output should be.
- A limitation buried in prose instead of sitting in a checkbox.
- Having to repeat an instruction he already gave.
- "I believe" where "here is the command output" belongs.
- A browser step when an API exists.
- "Should I…" when the precedent is already in [`DECISIONS.md`](DECISIONS.md).

## What makes him happy

- "I decided X because LAW 23. Evidence attached."
- "Found a bug. Incident test named for it. Commit `abc123`."
- "No manual steps. Everything is API-driven."
- "This is idempotent. Run it twice, same result."
- "PASS=7 FAIL=0" — numbers, not prose.
- "I read DECISIONS.md and applied precedent 3."

## Exceeding expectations

- A limitation found is not the end. It is the start of the research.
- Before reporting "impossible", spend ten minutes on the API docs, alternative
  endpoints, OAuth flows, service accounts, root-token patterns, the vendor's
  own CLI, and what other people did about it.
- The goal is zero manual steps. Every manual step is a bug to be engineered
  away.
- "It cannot be done" is banned. "It cannot be done with X, here is Y that
  works" is required.

## Context management

- Every active issue is a frame on a stack. The agent knows which frame it is in.
- Switching frames requires a checkpoint save on the old frame.
- Returning to a frame requires reading the checkpoint, not asking the founder.
- He never repeats context. The agent reads the log.
- LAW 25 in `~/AGENTS.md` is the enforcing rule: it names the five things a
  checkpoint has to contain and when it has to be written.

## Defaults

- Python for tools, bash for glue.
- pytest over unittest. hypothesis over example tests. Property-based over
  example-based.
- Desktop notifications over email.
- One file over a package, under about 500 lines.
- `curl | bash` over "follow these twelve steps".
- A green or red dashboard over a paragraph of status.
- The machine doing the work over him doing the work.

## Architecture

Idempotent over stateful. Lossless over compressed. Explicit over implicit.
Fail loud over fail silent. Reversible over permanent. Small and working over
large and planned.

## Diagnosis rule

His words, 2026-08-22: "If the user is actively using a service, 'account
inactive' is never the real cause. Cross-check user state before accepting
vendor error messages. 'I am using X right now' overrides any 'X is
unavailable' error from the machine."

What the kimi incident added to it:

- A vendor error string is a claim. The status code is the measurement. Report
  the code and the endpoint, never the sentence the vendor chose.
- One account can hold several entitlements. Signed in to the web app and
  entitled to the coding API are different facts, and an agent that treats them
  as one will diagnose the wrong thing with total confidence.
- Split authentication from authorisation before naming a cause. A 401 is the
  token. A 402 or a 403 is the plan. They have different owners and only one of
  them is the founder's.
