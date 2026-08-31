---
captured: 2026-08-31T02:43:16+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/.wt-backups
chars: 1740
source: founder prompt, verbatim (founder-doc-capture.py)
---

One: your nodes are configured to reject what the world ships. short-name-mode = "enforcing" with no unqualified-search-registries means every third-party chart default fails on arrival. That's not an incident stream, it's a setting. Two fixes, both cheap: set unqualified-search-registries = ["docker.io"] on the nodes and the class evaporates at source, or keep enforcing and let the admission mutation qualify everything. Either one, tonight. Six manual file edits was never the answer to a node-level policy.

Two: your agents produce inspection, not decisions. Look at the night: a hung hook nobody killed for 70 minutes, a 33-minute suite blocking a 10-second read, six turns of careful reasoning before the pod event got read. Each step was defensible. The aggregate was a night of your life for one merge. The missing piece isn't intelligence — it's that nothing in the loop compares elapsed time against the shortest path to a decision, so everything gets equal patience.

That's the one to fix, and it's mechanical, not prose in a CLAUDE.md:

Hard budget per task. Twenty minutes without something in your hands, it stops and reports what it has. No exceptions for "almost done."
Any process with no output for 5 minutes gets killed. Not watched. Killed.
Diagnosis before remediation, enforced as a gate. No branch, no commit, no PR until the primary signal — the event, the log line, the actual failure string — is captured and pasted. Tonight that would have saved six hours.

Do those three and the same agents produce the same quality of work in a fraction of the wall time. That's your rate problem, more than any individual class.

Merge #1030, then fix the registries.conf line. Everything else can wait until you've slept.
