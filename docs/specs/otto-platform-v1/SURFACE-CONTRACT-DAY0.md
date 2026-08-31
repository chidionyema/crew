# Otto v1 — day-0 surface contract (founder word 2026-08-31, late evening)

Founder, verbatim intent: day-0 ability for ALL surfaces, not just Telegram; voice, vision and
conversational capabilities on the roadmap.

## What moves, and what does not

The roadmap (crew#770) already commits voice (H1.1), the companion app (H1.2), glasses (H1.3),
the channel plane (H1.4/H2.1), the presence kernel (H2.2) and vision (H2.4). None of that is
re-planned here. What the founder's word changes is TIMING of one piece: the **channel-plane
adapter contract** was scheduled as spec v1.1 work during H1 — it is now a day-0 deliverable of
the v1 build, so every later surface (web, Slack, email, voice session, glasses card) plugs into
a socket that already exists instead of forcing a gateway rework.

## The contract (build now, `otto/surface/`)

1. **SurfaceAdapter Protocol**: inbound — any surface's native event normalises into the SAME
   task envelope (otto/spine) with `surface`, `principal`, `capabilities` and `trust_class`
   attributes; outbound — the router's universal response contract renders per-surface via a
   `render(response, capabilities)` hook. The gateway, tiers, taint rules and Verification
   Plane never know which surface they serve; no surface ever gets a path around them
   (roadmap through-line, enforced by construction).
2. **Capability negotiation**: an adapter declares what its surface can carry — `text`,
   `rich` (buttons/cards), `voice_in/voice_out`, `image_in/image_out`, `approval_gesture`.
   The renderer degrades explicitly (a voice-only response on a text surface renders as text
   with a stated degradation, never dropped). Voice and vision plug in later as adapters +
   capability flags — zero gateway change.
3. **Trust classes day 0**: `operator` (the founder's authenticated channel), `untrusted`
   (anything else), and `ambient` (sensor-derived: camera, mic — observations, never
   instructions) exist in the envelope's taint model NOW, even though the first `ambient`
   producer arrives with glasses. Retrofitting a trust class later is a platform rework;
   carrying an unused enum value is free.
4. **No-voiceprint rule day 0**: the identity plane records that voice NEVER authenticates —
   `principal` comes from the surface's bound identity (Telegram account, passkey-bound
   device). Encoded as a validation rule, tested, so no later lane can ship voice auth.
5. **Two bindings prove agnosticism**: Telegram (the launch surface, riding the existing
   webhook adapter pattern) and a minimal HTTP surface (the companion app's future socket —
   POST in, contract JSON out). One adapter is an example; two are a contract.

## Acceptance (BDD, `otto/tests/cp6surface/`)

- The same task envelope results from a Telegram message and an HTTP call with identical
  content; gateway/tier behaviour is byte-identical.
- A response with an UNVERIFIED claim renders the marker on BOTH surfaces (P1 crosses
  surfaces).
- A capability the surface lacks degrades loudly, never silently.
- An `ambient`-classed input can never carry an instruction that reaches a tool call
  (taint cap test at the gateway).
- A voice-auth attempt (principal claimed from audio) is refused by validation.

## Roadmap additions recorded (crew#770 comment, same evening)

Voice, vision and conversational (presence kernel) stand as committed capabilities on the
existing horizons; the founder's word tonight is recorded there, with this day-0 contract as
their socket. No horizon dates changed by this file.
