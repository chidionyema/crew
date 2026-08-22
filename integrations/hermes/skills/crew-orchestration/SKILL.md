---
name: crew-orchestration
description: Read and drive the crew's GitHub issue from Telegram — build status, blockers, and requests that engineering picks up. Use for /status, "how is the build going", "what is blocked", or when the founder asks for a checkpoint to be re-run from his phone.
---

# Crew orchestration from the phone

Hermes is another surface onto the same GitHub issue. It reads the board and
posts to the thread. It does not build and it does not verify.

The `crew` CLI is at `~/.local/bin/crew`. Every command takes `--issue N`, or
uses the repo's active issue.

## Status, formatted for Telegram

```bash
cd ~/dev/code/survival-stack && crew status --format telegram
```

Send that output as-is. It is already short and already Markdown.

## Full state, when the founder asks for detail

```bash
cd ~/dev/code/survival-stack && crew status --format json
```

## Pass a request from the phone to the crew

The founder says "re-run the cold start check" or "cold start on vultr". Hermes
does not run it. Hermes posts it to the issue, where engineering picks it up:

```bash
cd ~/dev/code/survival-stack && CREW_ROLE=hermes crew comment "founder asked from Telegram: <what he said>"
```

Then reply: "Posted to #N. Engineering will pick it up."

## Rules

- Never run `crew verify` from Telegram. Verification runs on the machine with
  the repository and the lab, not from a chat handler.
- Never edit the issue body. `crew` owns it.
- If `crew status` errors, send the error text. Do not summarise it away.
