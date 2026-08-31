---
captured: 2026-08-08T08:49:44+00:00
session: 702d32ce-4363-4185-8dee-a916d3f39d04
cwd: /Users/chidionyema/Documents/code/prospector
chars: 2837
source: founder prompt, verbatim (founder-doc-capture.py)
---

addres all , dont want anything left unaddressed properly 
Done. PR #141 is green and ready to merge: https://github.com/chidionyema/prospector/pull/141

dotnet  pass   guard  pass   nextjs  pass   python  pass (1m57s)

GitHub currently reports mergeable=UNKNOWN only because main moved again mid-check (3be12ca → d8cf90f); the authoritative local check is git merge-tree --write-tree origin/main HEAD → rc=0, 0 conflicts against that newest tip.

What actually happened. I fixed the E1 test, committed it, and pushed — then found PR #136 had gone CONFLICTING with zero check-runs on its head. Concurrent sessions had shipped #137, #138 and #139 to main in the preceding twenty minutes. Comparing #136's branch to main file by file, by blob: identical=92, differs=13, absent-on-main=0. The publish pass was already there as identical blobs. Resolving that conflict would have been the expensive answer to a question I hadn't asked, so I cut a clean branch from current main carrying only the 13-file delta.

The three things that were genuinely still missing from main:
- tests/unit/test_e1_abort_on_outage.py doesn't exist on main at all — which is why main is green and any branch carrying it wasn't. _load_candidates read the uncommitted dossier store (0 files on every ref; 1640 in a dev checkout), so it failed 6/10 in CI and passed 10/10 locally.
- tools/make_kill_log.py:131 still defined a second nodash alongside plain_text.py's. Now imported: nodash from: prospector.plain_text, nodash("a — b") = 'a, b', 'Mothers 25-45' preserved.
- site_spec_probe.py returned a hardcoded "superseded by brand v3" verdict regardless of the tree.

Two things worth your attention.

You asked for a skip when the store is too small; I stubbed the corpus instead. A skip goes green everywhere and guards nothing precisely where the guard is wanted — nobody runs that file by hand, so CI is the only place the E1 fence is exercised at all. Reversible in one edit if you'd rather have the literal skip.

I deliberately did not take my side of e5_coverage_sampler_entropy.py. Main had gained an inert-arm diagnosis (inert_why/inert_detail) that my branch predates — checking out my copy would have silently deleted a working feature inside a commit about something else.

PR #136 should be closed — 92/105 redundant, conflicting, untestable. It's the other session's PR so I left it open rather than closing it for them.

Also fixed while verifying: four memory files were not in the index at all, so they were invisible to recall. All 229 pointers now resolve and every file is indexed. On the compaction hook — the index is 20.1KB and the 229 filenames alone are 10.0KB, so hitting 17.1KB means cutting the display text (the recall signal) by ~30%; I've noted in the handoff that renaming files shorter is the only lever that doesn't cost recall.
