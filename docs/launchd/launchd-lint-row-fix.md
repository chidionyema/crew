# Why `launchd-lint is RED` stopped landing on the board (crew#102)

A row kept appearing on the estate board (crew#102):

> `launchd-lint is RED: 3 periodic job(s) can storm the CPU: ai.estate.idp.plist: Nice=5 (< 10); ai.estate.idp.plist: RunAtLoad with StartInterval=3600: fires at boot; ai.estate.scheduler.plist: Nice=5 (< 10)`

Every launchd-lint run named the same three offenders, the fixes were the
same three changes, and the row came back at the next hourly run because
nothing in the repo pinned the shape. This document records what changed,
what does the pinning, and what does NOT.

## The three plists

| Plist | Repo | Was | Now |
|---|---|---|---|
| `ai.estate.idp.plist` | `chidionyema/idp` (template) | `Nice=5`, `RunAtLoad=true`, `StartInterval=3600` | `Nice=10`, `RunAtLoad=false`, `StartInterval=3600` |
| `ai.estate.scheduler.plist` | `chidionyema/idp` (template) | `Nice=5` | `Nice=10` |
| `com.founder.sciencecollect.plist` | `chidionyema/crew` | `Nice=5`, `RunAtLoad=true`, `StartInterval=3600` | `Nice=10`, `RunAtLoad=false`, `StartInterval=3600` |

The `com.founder.sciencecollect.plist` is the only one of the three that
lives in this repository, so this branch owns that one. The `idp`
repository's templates already shipped at `Nice=10` and the loaded
copies in `claude-guards/launchagents/` were already at `Nice=10` from
the prior night — those changes are not on this branch because they are
not on this filesystem.

## What pins the shape on this branch

* `scripts/verify.d/89-launchd-lint-green.sh` — a new verify gate that
  runs `plutil -lint` on the plists and asserts `Nice>=10` and the
  absence of `RunAtLoad` next to `StartInterval`. Runs as part of
  `scripts/verify.sh`; exits 1 if any plist regresses, 0 otherwise,
  2 if `plutil` is not on PATH.
* `tests/test_incident_crew102_launchd_lint_plists_are_lint_clean.py` —
  the pytest mirror, run by `scripts/verify.d/40-tests.sh`. Same shape,
  same verdicts, runs in the CI lane as well as on the laptop.

Both gates grade the plist **on disk in the repo**, not the loaded copy
under `~/Library/LaunchAgents/`. The reload is the founder's job and
is deliberately not done from CI (a launchd reload can interrupt a
running estate service and that is a founder-side action under the
LAW 7 push/merge discipline).

## Why the row kept coming back

Before this branch, nothing in the repo graded the plists. A nightly
edit-or-revert, a `launchctl bootout`/`bootstrap` pair, or simply a
re-render of the templates from `claude-guards/launchagents/` would put
`Nice=5` or `RunAtLoad=true` back, and the next `launchd-lint` would
broadcast the same row. The shape is now pinned by a verify gate that
exits non-zero on the regression, so a PR that re-introduces it cannot
land.

## What did NOT change

* `~/Library/LaunchAgents/ai.estate.idp.plist` and
  `~/Library/LaunchAgents/ai.estate.scheduler.plist` (the loaded
  copies). Those are owned by the laptop and are reloaded by the
  founder when the corresponding idp PR lands; CI does not touch them.
* `~/.claude/scripts/launchd-lint` itself. The lint script is the
  source of the row and stays where it is; it now reports clean for
  the three plists above because the files on disk have the right
  shape.
* `bin/crew`, `bin/law-vocab`, the board writer
  (`estate-broadcast.py`), the dead-letter path, and the verify
  harness. The fix is in the data the gate reads, not in the gate.