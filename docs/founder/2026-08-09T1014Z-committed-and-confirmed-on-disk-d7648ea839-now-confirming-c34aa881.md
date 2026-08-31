---
captured: 2026-08-09T10:14:21+00:00
session: 00fd1592-0e4b-4a58-960c-3aa4280b42a6
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2147
source: founder prompt, verbatim (founder-doc-capture.py)
---

Committed and confirmed on disk (d7648ea839). Now confirming it's actually live in the running gateway — not just committed — per the "state is a probe" discipline:

  Searched for 1 pattern, ran 3 shell commands

Confirmed live, cleanly this time: gateway pid 31788 has been running continuously since 11:04:44 (no crash, no restart since — same pid ps shows now), and that restart followed source-watch's "change detected... settled" cycle at 11:02:49–11:04:27, which is after both panel_chrome.py and daemons.py were saved to disk. So the running process has the fix, not just the git history.

Summary — fully resolved and verified, not asserted:

1. Root cause: panel_chrome.py's nav() dropped _TUNE from the spine in commit 39402e463f (2026-08-02), invisibly, for 7 days — the constant, docstring, and 15+ panels' links all still pointed at it; only the one list that renders it disagreed.
2. Fix + blast radius: restoring _TUNE exposed two more places that had quietly baked the bug in as "correct" — daemons.py's MAX_BUTTONS cap (9→10, its own comment miscounted the spine) and a hardcoded SPINE test fixture (5→6 items) that caused 8 of 12 test failures. Proved causality by stashing the fix and showing all 12 failures pass on pre-fix code.
3. Verification: full 679-test suite green (674 passed, 5 skipped, 0 failed) before commit.
4. Landed: commit d7648ea839, and confirmed live in the running gateway process by process-start-time vs. source-change-time, not assumption.
5. Prevention: two new regression tests (test_panel_chrome_spine.py, test_declared_buttons_are_wired.py) that fail CI if this defect class — a declared button constant never wired into its rendering list — recurs anywhere in gateway/operator_shell/.
6. Standing lesson saved to memory (applies across agents/sessions per your instruction): don't carry an unverified claim from one repo's memory into another without grepping the target repo first — caught myself doing exactly that mid-task and corrected it.

Tune should now show up in /panel on Telegram — worth a quick tap to confirm on your end since that's the one check I can't run myself.
 nerge and deply
