# Corrections log

Every time he had to say something twice, or say it at all. Read this before
starting work: a correction here is an instruction that already cost him a turn.

A correction that keeps happening becomes a law, a guard or a script — never a
note. That is LAW 6, and this file is only the record, not the mechanism.

## Format

`DATE | WHAT THE AGENT DID | WHAT HE HAD TO SAY | THE RULE IT BROKE | WHAT IT SHOULD HAVE DONE`

## Entries

**2026-08-22 — asked him to choose between a pytest adapter and Gherkin**
He said: "LAW N, pick the smaller one."
Broke: the friction default — asked instead of deciding.
Should have: taken the 40-line adapter, noted the limitation in the issue body,
opened the issue.
Guard: LAW 23 is now in `~/AGENTS.md` and ranks as 5b.

**2026-08-22 — asked him to log in to Cloudflare**
He said: "Use the API."
Broke: a browser step is a bug.
Should have: used the Cloudflare API, the registrar API and `dns-diff`, then
handed him the nameservers to paste — the one thing no API covers.

**2026-08-22 — committed three bug fixes straight to main**
He said: "No main commits without a ticket and QA."
Broke: no direct commits to main.
Should have: opened crew issues and run them through the loop.

**2026-08-22 — `crew doctor` printed PASS for a `.crew.json` that did not exist**
He said: silent data loss, a false green.
Broke: no false greens.
Should have: checked the file before naming it.
Guard: `test_incident_doctor_does_not_name_a_config_file_that_is_absent`.

**2026-08-22 — built the thing, then worked around it**
He said: "Dogfood the crew on itself."
Broke: dogfooding.
Should have: run its own work through `crew plan`, `crew evidence`,
`crew verify`. It does now, on issue #2.

**2026-08-22 — asked "are you drifting?" instead of measuring**
He said: "Check the scorecard."
Broke: evidence first.
Should have: run the harness and reported PASS/FAIL before asking anything.

**2026-08-22 — stopped at a vendor wall**
`wrangler login` returned `ERROR: Invalid scope` and the agent reported the
limitation as the answer.
He said: "Find a creative workaround."
Broke: a limitation found is the start of the research, not the end.
Should have: spent ten minutes on `POST /user/tokens`, OAuth apps, service
tokens and the root-token bootstrap before saying a word. A vendor wall is
never accepted on the strength of one error message.

**2026-08-22 — committed the installer straight to main, hours after writing
the rule above into FOUNDER.md**
He said nothing; it is here because it happened.
Broke: no direct commits to main, again.
Should have: a branch and a pull request with LAW 22 evidence. This file and its
two neighbours went through one.

**2026-08-22 — reported "membership inactive" for kimi without measuring it**
The agent read the vendor's error string out of a log and repeated it as a
diagnosis. The founder was signed in to Kimi at that moment.
He said: "I am using Kimi right now. Do not report 'membership inactive' again."
Broke: proof before action. An error message is a claim by the vendor, not a
measurement of the account.
What the measurement actually showed, once it was taken: authentication works.
`POST auth.kimi.com/api/oauth/token` with the stored refresh token returns 200,
and `GET api.kimi.com/coding/v1/me` returns 200 with his name and
`USER_STATUS_NORMAL`. Three endpoints on the same host with the same working
token return 402 and 403: `/models`, `/chat/completions` and `/usages`, the last
one saying "Please subscribe to access". The Kimi web app and Kimi For Coding
are separate entitlements on one account, so being signed in to the first says
nothing about the second.
Should have: called the endpoint and reported the status codes. The 200 on `/me`
is the fact that kills the "inactive account" story, and it cost one command.

**2026-11-18 — pennyd's budget ledger was not a record of reservations, so money
could be encumbered without being written down, released at midnight, and charged
twice on a retry**
He said: (nothing; the founder asked for the financial-control corrections to be
over the line, and the earlier session's commits did not exist).
Broke: measured in `platform/llm/pennyd` (the live tree since #8192; `router/pennyd`
was the dead duplicate). The ledger kept only per-key spend and had no record of the
money encumbered for an in-flight operation, so (1) a reservation that could not be
written was still treated as money in hand and the dispatch went out against it,
(2) a restart lost the reservation and released money that was still at risk,
(3) two writers on one ledger clobbered each other's financial records,
(4) a corrupt ledger file parsed as an empty ledger -- and an empty ledger is a full
budget, (5) a client retry with the same idempotency key reserved and settled twice,
and (6) the midnight rollover released funds that were still reserved.
Should have: the ledger carries the reservations. Reserve and settle are keyed by the
operation id (`x-idempotency-key`), a reservation that cannot be written is refused
and rolled back (503 `ledger_unavailable`), a ledger that cannot be parsed poisons
the store instead of granting a fresh budget, the ledger carries a write counter and a
stale writer refuses rather than clobbering newer records, and an unsettled
reservation survives both a restart and the day boundary until it is reconciled.
Proved by eight regression tests in `crates/penny-core/src/budget.rs`, each named by
a row in `FAILURE_MODES.md` (F-BU-6..F-BU-12, FP-P0-7/8/9). Two pre-existing clippy
lints (digit grouping in `ledger.rs`, the lock file's truncate behaviour in
`instance.rs`) had kept the crate's own gate red; both are fixed in their own commit.
