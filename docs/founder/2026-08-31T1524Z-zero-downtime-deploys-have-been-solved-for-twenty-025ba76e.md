---
captured: 2026-08-31T15:24:34+00:00
session: ef0354ef-fa6b-4b6b-a5e2-5d6f7889b3b8
cwd: /Users/chidionyema/dev/code/hermes-v2
chars: 1615
source: founder prompt, verbatim (founder-doc-capture.py)
---

Zero-downtime deploys have been solved for twenty years and there’s no reason a Telegram gateway gets an exemption.

The specific thing blocking it: if Otto’s gateway uses long polling (getUpdates), it’s a single-consumer design. Telegram will only hand updates to one poller, so you can’t run old and new side by side — you have to stop one before starting the other, and that gap is your downtime. That’s the actual root cause, not the shutdown handler. The handler is just narrating it.

Switch to webhook mode and the gateway becomes an ordinary HTTP service. Then you get the standard playbook: new instance up, readiness probe green, service starts routing to it, old instance stops accepting and drains in-flight work to completion before exiting. Telegram retries on non-2xx, so anything caught mid-flight redelivers. No banner, no interruption, nothing user-visible.

Two things that survive from before, though, because rolling deploys only cover planned exits:

Draining requires in-flight work to be finishable in bounded time. If a task can run for minutes, the old instance either blocks the deploy or gets killed anyway. That’s the argument for handing execution off rather than holding it in the request.
OOM kills, panics and laptop sleep don’t drain. A zero-downtime website still needs work to be recoverable when a process dies without warning.
The message itself should be deleted outright. It’s a user-facing admission that process lifetime and task lifetime are the same thing — if the architecture is right there’s nothing to announce.

Do you know whether it’s polling or webhook currently?
