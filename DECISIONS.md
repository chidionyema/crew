# Decision archive

Precedent. Before asking him anything, read this — the answer is usually a line
already in it. Cite the entry by number when you apply it.

`~/AGENTS.md` is the law. [`FOUNDER.md`](FOUNDER.md) is how he works.
[`PREFERENCES.md`](PREFERENCES.md) is what he reaches for by default. This file
is what was actually decided, and when.

## Format

`DATE | CONTEXT | WHAT I DID | WHY | WHAT I REJECTED | RULE EXTRACTED`

## Hermes Architecture (canonical)

The map every agent reads before touching Hermes. `grep -A20 "Hermes Architecture"`
this file.

```
PRIMARY:   hermes-v2 on Fly, app prospector-hermes
STANDBY:   hermes-v2 on this Mac, ~/dev/code/hermes-v2, launchd-ready, fence ON
RETIRED:   the old estate, ~/.hermes, v0.16.0
```

Migration path: hermes-v2 is the test candidate for survival-stack Phase 2. When
survival-stack is proven on a spare domain, hermes-v2 moves off Fly to the
cheaper provider. Every other store adapts to the hermes-v2 API before that move,
not during it.

Source of truth is the crew issue board. No agent touches Hermes without a
ticket. LAW 26.

**State as measured 2026-08-22 09:55 UTC, which is not yet the target.** The
PRIMARY line above is where this is going. What is actually running:

| fact | command | what came back |
|---|---|---|
| `prospector-hermes` is deployed | `fly releases -a prospector-hermes` | v12, 11h ago |
| it serves no HTTP on the usual paths | `curl -o /dev/null -w '%{http_code}' https://prospector-hermes.fly.dev/health` | `000` |
| its `HERMES_HOME` is a Mac path | `fly config show -a prospector-hermes` | `"HERMES_HOME": "/Users/chidionyema/.hermes"` |
| neither checkout can deploy | `ls ~/code/hermes-v2/fly.toml ~/code/hermes-v2/Dockerfile` | neither exists |
| the standby is real | `git -C ~/code/hermes-v2 log --oneline -1` | `6a64105 evidence: CI green on a public runner` |

So `prospector-hermes` is deployed from something that is not either checkout on
this machine, and it carries a container env pointing at a macOS path that cannot
exist inside a Linux container. Both are open questions on the ticket, not
findings — nobody has yet read what that image actually runs.

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
