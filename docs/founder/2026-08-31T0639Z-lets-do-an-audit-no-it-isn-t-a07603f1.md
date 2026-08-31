---
captured: 2026-08-31T06:39:35+00:00
session: a7b41022-3074-43c7-bb13-a1d7e07adff1
cwd: /Users/chidionyema/dev/code/.wt-secrets-rotation
chars: 2479
source: founder prompt, verbatim (founder-doc-capture.py)
---

lets do an audit No, it isn't normal, and I've been treating each break as a case to analyse rather than saying the obvious thing: this rate of breakage means the tooling around the work is broken, not the work.

Look at what just happened. A push failed. The hook that failed it **swallowed its own error output through a broken pipe**, so the reason was lost. Now a 27-directory sweep is running purely to rediscover information the tool already had and threw away.

That's the whole picture in one incident. Not a hard problem — a tool that can't report its own failure. And it sits alongside a pre-commit router that silently disabled itself, a test selector that dragged in 397 files, a realm importer that's create-only, 13 scripts each parsing the same tree differently, a 60-second timeout that fails under load. None of these are subtle. They're all the same thing: **a homegrown control plane that nobody has ever tested against failure.**

That's why something breaks at every step. Every guard in that estate was written, assumed to work, and never once watched failing. So the guards are as unreliable as the thing they guard, and each one adds a new way for a normal change to detonate.

The honest engineering answer, since you asked for one:

**Stop adding guards. Start deleting them.** You have more custom tooling than the estate warrants — a router symlinked as every hook, bespoke renderers, 13 parsers, an idp-tests-for selector, a verification plane, a blocker guard, a mistake ledger. Each was reasonable. Together they're a second system larger than the first, unmaintained, and it's where your nights go.

The subtraction the agent identified — one shared loader, delete 13 parsers — is right, and it should be the template, not the exception. For each piece of that tooling: does a standard thing do this? Pre-commit framework instead of a custom router. `pytest --testmon` or plain path filters instead of idp-tests-for. Flux's own status instead of a bespoke state page. Standard tools have been watched failing by thousands of people. Yours haven't been watched failing once.

And the one rule that stops it regrowing: **no new guard ships without a test that watches it fail.** Not that it passes — that it correctly rejects a bad input. Every single failure tonight would have been caught by that one rule, at write time, for free.

That's the answer. It's subtraction, and it's boring, and it's why you keep ending up here at 7:30 in the morning.
