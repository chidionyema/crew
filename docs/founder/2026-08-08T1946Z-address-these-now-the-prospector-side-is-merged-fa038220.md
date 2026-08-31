---
captured: 2026-08-08T19:46:09+00:00
session: da21cd3a-d3e7-47ad-9d96-1739d3f58a9b
cwd: /Users/chidionyema/Documents/code/prospector
chars: 1562
source: founder prompt, verbatim (founder-doc-capture.py)
---

address these now . The prospector side is merged. #160 merged at 19:39Z as e871889; prospector/scheduler/status.py and tests/unit/test_tick_digest.py are on origin/main. (#161, my audit work, merged at 19:28Z as cfce689.)

2. The running daemon does not have the code. Daemon pid 77892, started 20:29:58 today, cwd = /Users/chidionyema/Documents/code/prospector — and this checkout is on chore/noncritical-chain-standardcompute-first at 2e93172, 2 commits behind origin/main, with git ls-tree HEAD | grep -c scheduler/status.py = 0. It restarted after the merge and still came up without the file, because the checkout it runs from was never moved to main. Consistent with that, grep -c tick_digest across store/scheduler/ = 0: no digest has ever been emitted.

3. The Hermes side was never committed. gateway/operator_shell/prospector_now.py is ?? — untracked — in ~/.hermes/.worktrees/feat-prospector-now, along with its test and edits to estate.py/mission.py. feat/prospector-now-on-telegram exists only as a local branch; the remote has just main, and there's no PR (hermes-agent's open PRs are 10 dependabot bumps). The gateway process has been up 8.8h, so it predates all of it.

To make it real: merge main into the live checkout and restart the daemon, then commit/push/deploy the Hermes half. I haven't touched either — switching branches under a running daemon on the fenced main checkout isn't something to do unasked.

Separately, the estate probe reports ai.hermes.rsi last exit=2 and not running — failing every run, and the verdict is ❌ DEGRADED.
