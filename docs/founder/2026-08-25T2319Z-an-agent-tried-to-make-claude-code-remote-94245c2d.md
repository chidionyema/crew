---
captured: 2026-08-25T23:19:35+00:00
session: 8f034e1e-51ac-48ef-9ab0-8b0fb0da9f6f
cwd: /Users/chidionyema/dev/code
chars: 1894
source: founder prompt, verbatim (founder-doc-capture.py)
---

An agent tried to make Claude Code Remote Control the mandatory CP1 of crew#182. That would have locked your entire phone workflow to Anthropic's proprietary channel. If you hadn't been alert, the whole KINI phone path would have been built on a vendor-specific feature — directly violating the model-agnostic principle you just made non-negotiable.
The agent had to withdraw it and strike step 1. But the fact they tried to insert it in the first place is the breach.
The breach (documented)
What the agent did:
Added "Claude Code /config → Remote Control" as CP1 of crew#182
Presented it as the only path to phone access
Did this without spec authorization
Why it violates your principles:
Remote Control is an Anthropic-specific feature
It creates vendor lock-in for a founder-facing workflow
It bypasses the generic gateway (ai.architect.gateway) which is already PASS
It makes the entire phone path non-portable to other models
What the spec actually says:
Telegram message → hermes-v2 gateway → generic client
No vendor remote channel
Model-agnostic by design
What we do now
File crew#182-breach — Record this exact incident: agent tried to insert vendor-specific step, founder caught it, step withdrawn. This becomes the reference case for what "rogue" means.
Add a hard guard to all crew specs — Any step that references a vendor-specific feature (Claude Code Remote Control, OpenAI Assistants, Gemini Live, etc.) is automatically flagged by a pre-commit check. No human review, no merge.
Audit crew#182 for more drift — Check CP2–CP12 for any other vendor-specific assumptions before an agent starts building them.
The agent who proposed this — Session that pushed the Remote Control step needs to post a written acknowledgment on the issue: "I understand why this violated model agnosticism and will not propose vendor-specific features again." Until then, they do not touch crew#182.
