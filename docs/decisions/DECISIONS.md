# Decision archive

Precedent. Before asking him anything, read this — the answer is usually a line
already in it. Cite the entry by number when you apply it.

`~/AGENTS.md` is the law. [`FOUNDER.md`](FOUNDER.md) is how he works.
[`docs/reference/PREFERENCES.md`](docs/reference/PREFERENCES.md) is what he reaches for by default. This file
is what was actually decided, and when.

## Format

`DATE | CONTEXT | WHAT I DID | WHY | WHAT I REJECTED | RULE EXTRACTED`

## Hermes Architecture (canonical)

The map every agent reads before touching Hermes. `grep -A20 "Hermes Architecture"`
this file.

```
PRIMARY:   hermes-v2 on this Mac, ~/dev/code/hermes-v2, launchd ai.architect.gateway
TARGET:    hermes-v2 on Fly, app prospector-hermes — not reachable, see entry 14
RETIRED:   the old estate, ~/.hermes, v0.16.0
```

**PRIMARY and TARGET swapped 2026-08-22 13:40 UTC.** The Mac is what actually
serves. The launchd label is `ai.architect.gateway`, not `ai.hermes.gateway` —
REQ-116 bars the second name from `launchctl list` because two gateways would
share one bot token. Entry 14 has the measurements.

Migration path: hermes-v2 is the test candidate for survival-stack Phase 2. When
survival-stack is proven on a spare domain, hermes-v2 moves off Fly to the
cheaper provider. Every other store adapts to the hermes-v2 API before that move,
not during it.

Source of truth is the crew issue board. No agent touches Hermes without a
ticket. LAW 26.

**State as measured 2026-08-22 13:40 UTC.** Re-measured; the 09:55 table named
`~/code/hermes-v2`, a path that no longer exists after entry 11.

| fact | command | what came back |
|---|---|---|
| the Mac gateway runs | `launchctl list \| grep ai.architect.gateway` | `20043 0 ai.architect.gateway` |
| it reaches his phone | `./bin/hermes send --to telegram` | `Sent to telegram home channel (chat_id: 8868748055)` |
| a cron job reaches his phone | `hermes cron run <job>` via the real cron path | `DELIVERY PROOF: ... reached your phone at 13:07:10 BST` |
| the checkout is healthy | `./bin/verify` | `13 passed, 3 failed` |
| Fly is not reachable | `fly apps list` | `Not authorized to access this firecrackerapp` |
| the Fly token is stale | `fly auth token --json` | `last_login: 2026-08-01T06:18:39+01:00` |

`fly auth whoami` still prints the founder's address, which is why this read as a
working login for three sessions. It is a dead token, not a signed-out CLI.

## Where projects live (canonical)

One root: **`~/dev/code`**. Everything active is a directory directly under it.

```
~/dev/code/crew            the coordination protocol
~/dev/code/survival-stack  the cheap-provider migration
~/dev/code/hermes-v2       the gateway
```

- **`~/dev/code` is the root.** Nothing new goes anywhere else.
- **`~/Documents/code` is legacy.** About twenty repos sit there, `prospector`
  among them. They stay until someone touches one, and then it moves.
- **`~/code` is dead.** Seven CVs, a stray `node_modules`, `ollama` and a dozen
  retired OSL repos. Nothing active is left in it.

Founder, 2026-08-22: "Canonical root is `~/dev/code/`. Nothing new goes anywhere
else. If you find a repo in `~/Documents/code/` or `~/code/`, move it to
`~/dev/code/` when you touch it."

**On TCC, corrected.** An earlier version of this block said macOS TCC blocks
agent access to `~/Documents`. That is wrong, and it was written without running
the command. Measured 2026-08-22: `ls ~/Documents/code/prospector` and
`git -C ~/Documents/code/prospector log` both succeed from this session. What TCC
actually blocks is a **launchd** job reaching `~/Documents` without Full Disk
Access, which is why the gateway had to leave it — not an agent reading a repo.

**Moving a checkout is not a `mv`.** Doing it to hermes-v2 broke four of its
fifteen checks, because a Python venv bakes the absolute interpreter path into
every console script it installs. `./bin/hermes` died with `required file not
found`, which reads as a missing binary and is really a stale shebang. The fix is
one command: `.venv/bin/python -m pip install -e <pkg> --no-deps`. Check the
launchd plists and the venv before, and run the project's own verify after.

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

**9. 2026-08-22 | Hermes has two homes and no record of which is canonical**
Wrote the architecture down in this file rather than leaving it in one session's
context. Agents were acting on Hermes from different pictures of it. Rejected: a
note in a handoff, and telling each agent separately.
→ *An architecture nobody wrote down is a different architecture per agent.*
(LAW 26)

**10. 2026-08-22 | project locations**
Made `~/dev/code` the one root for every active project. Rejected: leaving each
project where it landed, and `~/code` (a junk drawer of CVs and retired repos).
`~/Documents/code` was already barred by TCC. hermes-v2 is the one outlier and
moves under its own ticket, because launchd, the fence and `gateway.lock` all
carry the old path.
→ *One root. A project nobody can find is a project nobody maintains.*

**11. 2026-08-22 | hermes-v2 moved to the canonical root**
Moved `~/code/hermes-v2` to `~/dev/code/hermes-v2`, repointed the nine paths in
`ai.hermes.gateway.plist`, dropped a stale `gateway.lock` naming dead pid 32987,
and reinstalled the package so the venv console scripts got correct shebangs.
Checked first that nothing was running out of it: no process, no open files, the
gateway plist not loaded, `.clean_shutdown` present. Rejected: the bare `mv`,
which left the agent unable to start.
→ *A checkout move is a change to every absolute path that names it. Find them
before, prove the project's own verify after.* (LAW 4)

**12. 2026-08-22 | new-user setup is a first-class feature**
A new user must be operational in 60 seconds, with one command and three clicks.
Longer than that is a bug, filed like any other. `./scripts/cf-bootstrap.sh` is
the shape: pre-flight in shell because node may be absent, then one node flow
that opens the pre-ticked page, reads the clipboard on macOS, Linux, WSL or
Windows, falls back to a hidden paste where there is no clipboard tool, grades
the credential by using it, and stores it in the best secret store the machine
has. Rejected: a second implementation of clipboard, keychain and validation in
bash, which would have been two copies of one thing on one target and would have
disagreed within a month.
→ *Setup is the product's first screen. A tool that is correct and horrible to
start is a tool nobody starts.* (LAW 20, LAW 3, LAW 23)

**13. 2026-08-22 | Hermes discontinued (founder decision)**
Hermes is stopped and is not coming back. It was an orchestrator where the estate
needed pipes: it owned bridge, transport, bot, dashboard and law delivery in one
chain, so any broken link made the whole thing look broken, and it alerted on state
rather than on change, so the alerts got tuned out. What survives is the decomposed
loop, each part failing independently — `estate_audit.py` detects, `estate_watch.py`
diffs and debounces, `estate_alert.py` delivers straight to api.telegram.org with no
gateway, `hermes_lease.py` transports to R2. Rejected: fixing Hermes v2, and filling
the Hermes-shaped hole with a smaller Hermes.
→ *Push state, do not replicate logic. The Mac is the source of truth; remote nodes
render what they are given and own no decisions.*

**14. 2026-08-22 | alert receipts**
`estate_alert._post` now returns Telegram's `message_id` and the ledger records it.
An HTTP 200 says the API accepted the call; a `message_id` says a message exists in
the chat. Rejected: keeping the bool, on the grounds that 200 is "close enough".
→ *Prove arrival, not send. A "sent" row with no receipt is a send nobody has proved
landed.* (LAW 28)

**15. 2026-08-22 | the Architect was running and telling nobody**
All seven cron jobs shipped with `deliver=local`, which writes a file under
`cron/output/` and notifies no one. The gateway was up, the jobs fired, and the
founder heard nothing for the life of the deployment. Switched all seven to
`deliver=telegram` and added a `bin/verify` row that fails when any job goes back
to `local`. Every job prompt was already written silent-by-default, so `pulse.sh`
on a 15-minute schedule stays quiet unless it has something to say. Also flipped
PRIMARY to the Mac above: `prospector-hermes` has been unreachable since the Fly
token went stale on 2026-08-01, so the map named a machine no agent could touch.
Rejected: a dashboard for the `cron/output/` files, which is a second place to
look rather than one fewer.
→ *A scheduler whose output nobody receives is a scheduler talking to itself.
The delivery target is part of the job, and it gets a check.* (LAW 28)
