# R75 — Spread to every surface: WhatsApp, Slack, as many as it takes

**Founder, 2026-09-01 ~21:50Z, verbatim:**
`docs/founder/2026-09-01T2150Z-spread-everywhere-whatsapp-slack.md`. Sister rulings: R73
(no command line for the founder), R74 (the All-Seeing Eye).

## The ruling

The company's reports, digests and decision requests reach the founder — and later
customers and partners — on whatever surface they already use. Telegram is not the
strategy; it is the first surface.

## The shape (inventory first: the platform's messaging layer is an internal event
library, not a fan-out — this capability is genuinely missing, so one adoption is allowed)

1. **One outbound fan-out layer: Apprise (open source).** Every digest, alert and release
   line is published once; Apprise fans it to Telegram, Slack, email, push and ~100 other
   services as configuration lines, not code. Adding a surface becomes a one-line change.
   Rejected: Novu — a whole notification server where a library does the job (LAW 23);
   rejected: one hand-written sender per surface — the script-per-problem habit the
   headline bans.
2. **Two-way (buttons, voice, replies): Telegram now** — already building under R74.
   **WhatsApp and Slack two-way come via Matrix bridges** (mautrix), self-hosted, no
   per-message vendor fees, when the founder asks for the second two-way surface; WhatsApp's
   official business API is rejected for founder use — Meta charges per conversation and
   reviews the account (LAW 34).
3. **Credentials per R52:** one Slack bot token minted once, one WhatsApp pairing (a QR
   scan on his phone — a physical step, requested loudly only when that stage starts);
   everything else code-minted.
4. Every surface obeys the standing digest rule: one clean message per beat, never a flood.
