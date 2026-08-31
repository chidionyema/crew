---
captured: 2026-08-07T16:41:53+00:00
session: 0de0ee9d-dbb6-419c-bb8d-8ea865e727fc
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2651
source: founder prompt, verbatim (founder-doc-capture.py)
---

Both tasks are complete and on the branch.

§23.6 — all six defects closed, four of them as one class. prospector/paths.py resolves per call from a __file__ anchor with PROSPECTOR_REPO_ROOT/PROSPECTOR_STORE_ROOT overrides; tests/unit/test_paths.py pins the property a module constant cannot have by importing a consumer first and then moving the root — the exact binding that put fixture rows in the production audit log and 1,874 fixture LAW: lines in the durable ledger. 19 call-time literals converted in prospector/control_center/, plus config_editor.py, decay.py and unlist_killed.py. jsonl_atomic.consume_jsonl replaces QUEUE.write_text("") with an flock-serialised read-and-rewrite, proved by a test that demonstrates the loss before the fix and by 4 subprocess producers × 150 records (subprocesses because flock is per open file description). pytest.ini gained pythonpath = .; ruff 0.16.2 is installed with its rule set pinned and a baseline of 393.

Backups — both P0 gaps closed, with live R2 receipts, not reasoning: REMOTE quarantine_ungrounded=9 local=9, LOCAL FILES NOT IN BUCKET: 0, db/prospector-2026-08-07.db.gz 493891 bytes gz, dossiers=1760, STORE_BACKUP RESTORE PASS files=1701, RESTORE_DRILL PASS checks=12 failures=0. No new launchd job was needed — the installed plist already runs the script daily at 03:40.

Two things I'd flag as the honest edges of this:

The drill was asserting the wrong property, and it took a false FAIL to find that. It failed the live payload on restored=1701 source=1588 while index_vs_tree passed. Count-equality is not coverage — it passes just as happily when N live files are missing and N stale ones are present. Now checks membership of every live source file and reports the surplus as a note.

I left 9 module-level constants alone deliberately (audit.py:134, health.py:31/37, pipeline/middleware.py:26, prompts.py:17, retrieval.py:36, run.py:167, 2 in tools/experiments/). They are import-bound but already __file__-anchored — the lesser half of the class — and audit.py is fenced by tests/conftest.py:37-38. Churning the audit hot path to remove a hazard a fence already covers buys nothing, but it is a judgement call, not a proof, and §24.3 says so.

Still uncommitted in the shared tree, and not mine to land: S5's prospector/retrieval.py changes with tests/unit/test_retrieval_cross_tick_cache.py untracked beside them, and prospector/prescreen_prefilter.py + its test in the same state.

Handoff written to checkpoints/2026-08-07-defect-class-and-backups.md and LATEST.md.

Safe point — type /clear (state saved, nothing will be lost).
 whatscleft to do fro the connnercial readiness?
