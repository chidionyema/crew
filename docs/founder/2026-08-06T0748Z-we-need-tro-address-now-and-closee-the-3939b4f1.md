---
captured: 2026-08-06T07:48:09+00:00
session: 4ace033b-dab9-43e7-915c-120c1da5f506
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2440
source: founder prompt, verbatim (founder-doc-capture.py)
---

we need tro address now and closee the loop 
Two defects, both measured, not argued:

A. vet --resume sorts DEFER and provisional rows together oldest-first (run.py:1144). On the live index the drainable backlog is 350 — 166 provisional KILL, 113 DEFER, 72 provisional PASS. Of the oldest 100, the rows a --limit pass actually takes: 51 provisional KILL, 47 DEFER, 1 provisional DEFER, and 1 provisional PASS. Reaching the 72 required draining all 350 ≈ 32h. Added --only {all,defer,provisional,provisional-pass}, filtering before the sort and slice. Default all is unchanged, and the daemon's resume_deferred() has no only attribute, so its per-tick drain is untouched.

B. Found while running (A): --title was required=True, so python -m prospector.run vet --resume — documented at RUN.md:97 — exited 2 in argparse before _cmd_vet (run.py:972) could read args.resume. That command has never once run. It stayed invisible because the daemon calls resume_deferred() in-process and never touches the parser.

Proof: 9 new tests. 4 fail with _resume_selects neutered to return True; the invocability test fails with required=True restored. POPDD python lane PASS, chain valid. Commit verified with git log, not an exit code.

Four things I got wrong earlier, corrected

- The moat is not down. 11/11 dossiers 06:33–07:22 UTC were provider=claude_cli, 0 provisional, 2 real PASSes.
- claude_cli auth is fine. My env -i HOME= PATH= probe reporting "Not logged in" was a false negative — the daemon's full 11-var env returns OK, exit 0.
- PR #111 is MERGEABLE, blocked only on CI. The CONFLICTING/DIRTY was a stale gh read.
- Slot isolation was backwards. PROSPECTOR_CLI_SLOTS is a directory, not a count (cli_governor.py:104); leaving it unset is what shares the machine-wide ceiling with the daemon. I ran the drain unset, and isolated only the test gate.

One live trap: this session's env carries a zero-credit ANTHROPIC_API_KEY that overrides the claude.ai login. Local claude calls need env -u ANTHROPIC_API_KEY. The daemon doesn't inherit it.

Still open, in your hands

1. Publishing — deliberately not done; no --publish. Only decision=pass, provisional=0 survivors are eligible, and so far there are none.
2. Daemon restart — pid 6049 started 06:22:13 UTC; eacd55f (06:38:06), 1a6cced and ac6c5e1 all landed after, so all three are inert. eacd55f is the one that makes a failed CLI call state its reason.
3. PR #111 merge on your word.
