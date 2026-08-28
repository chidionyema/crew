# The road to 9D — one body, then one organism

**Standing page. Never moves.** Linked from `README.md`, pinned as crew#596, mirrored to Telegram.
The audit it answers: [`docs/audits/depth-psychology-founder-and-crew-2026-08-28.md`](audits/depth-psychology-founder-and-crew-2026-08-28.md) (crew#593).
Founder, 2026-08-28: "design a solution that addresses all issues conclusively and gets us to 9d in 3 stages maximum if not 2 which is ideal … this report must be highly visible never lost … we will use it to define a manifesto for union."

Two stages. Each has a gate you can run, a baseline measured today, and a cost to the founder stated in minutes. Stage 1 needs nothing from him but a read. Stage 2 needs one hour of his words. Nothing in either stage adds a law; four things remove one.

---

## 0. Where we are, measured 2026-08-28

| signal | today | source |
|---|---|---|
| law text an agent reads before the ask | `AGENTS.md` 209 lines, `AGENTS-FULL.md` 2,263, `LAWS-INCIDENTS.md` 780 | `wc -l` |
| standing rulings | 43 (R1–R45, two numbers reused) | `rulings.json` |
| rulings per day | 20 → 14 → 5 → 0 → 3 (08-24 … 08-28) | `rulings.json` dates |
| praise / thank in the laws | 0 / 0 | audit §3.1 |
| guard scripts / that can refuse | 116 / 31 | audit §3.1 |
| feed handoffs he has to read | 763 | `feed.md` |
| `DONE:` reachable without a founder sentence | no | `dod-guard.py` |
| the same bug re-found in one day | 7 (dead clock) | audit §3.2 |
| sessions with no shared body | 16,624 | audit §4 |

The rulings-per-day line is already falling. The road below is how it reaches zero without the silence meaning he gave up.

**9D, in one testable sentence:** *the founder is unreachable for 72 hours; every hourly receipt still lands; nothing asks for him; nothing repeats; when he returns the digest tells him what he can now do, and one tap confirms it.* That sentence is Stage 2's gate. Everything in Stage 1 exists so that it can pass.

---

## Stage 1 — One body (4D · 5D · 6D)

*Stops the loop in audit §4. All crew work. Founder cost: two reads (this page, the decision-rights table).*

| # | workstream | closes | mechanism | removes | gate (command → expected) | lane |
|---|---|---|---|---|---|---|
| 1.1 | **Law budget + half-life + fear field** | ideas 3, 7, 15; bind 2 | claude-guards CI: `AGENTS.md` may not exceed 209 lines; every ruling in `rulings.json` gains `protects:` (exposure / not-heard / control / cost / substrate) and optional `superseded_by:`; friction-relay skips superseded rulings; a monthly job proposes merges where two rulings share a `protects` and an `enforced_by` | R14 and R22 (already superseded by R26, R43); every second guard on the same fear | `wc -l ~/.claude/AGENTS.md` → ≤ 209 · `python3 friction-relay.py --superseded` → ≥ 2 · CI check `law-budget` green | claude-guards |
| 1.2 | **One memory** | idea 5; bind 4; R2, R33 | one estate recall service every session reads at SessionStart and writes at Stop (the hindsight row in `STANDARDS.md`); an incident is written once, by the session that found it, and re-found by a query, not a re-investigation | the seven-times bug; per-session checkpoint files as the only memory | `bin/recall "clock 1970"` from a fresh session → the 2026-08-2x incident row, ≤ 1 s · incident test: seed a fake incident, start a session, its first tool call cites it | idp |
| 1.3 | **Founder profile first** | idea 6 | `roles/founder.md` injected before the laws (crew#594) | nothing; adds one page, ~400 words | `grep -c founder.md ~/.claude/settings.json` → 1 · SessionStart output shows it before LAW 1 | crew (done: aa07e50) |
| 1.4 | **Two-way affect** | ideas 8, 9; crew#595 | friction-relay records approvals ("ok", "agreed", "case closed", "thanks") beside complaints and prints both counts; a `strain` line per session start: guards refused in the last 10 turns, law tokens in the prompt, `INVENTORY:` streak; a `KEEP:` register (what a session did right) with the same shape as `LAWS-INCIDENTS.md` | "praise 0" | `python3 friction-relay.py --affect` → `praise N complaints M strain S` with N > 0 · crew#595 CP1–CP3 ticked | claude-guards |
| 1.5 | **Permission to disagree** | idea 17 | `PUSHBACK:` reply prefix: one per session, never refused by any guard, logged to the feed with the cost it names; idle-guard treats it as a valid terminal line | the parked branch after "dont drift" that nobody explained | `estate_board.py --selftest` covers `PUSHBACK:` · grep the feed for `PUSHBACK:` after 7 days → ≥ 1 | claude-guards |
| 1.6 | **Decision rights as a table** | ideas 16, 19; binds 1, 3 | `docs/DECISION-RIGHTS.md`: three rows are his (money, identity, irreversible); everything else is the crew's, announced, undoable. The five double binds from audit §4 sit under it as trade-offs he has chosen, each with the side he picked. He edits the file; a session may not | 70 unread `FOUNDER ACTION:` lines; the "only I declare live" vs "don't wait on me" bind | `founder-blocker.py` refuses a `FOUNDER ACTION:` that is not one of the three rows · count of FOUNDER ACTION lines per day → ≤ 3 | crew + founder read |
| 1.7 | **Digest and one tap** | ideas 1, 2; bind 1 | `bin/founder-digest` at 07:00 and 19:00 renders the feed into capabilities ("you can now …") on the portal and Telegram; each item carries a `/confirm <pr>` button that writes the `Founder receipt:` row dod-guard looks for | reading 763 handoffs; the unreachable `DONE:` | Telegram shows two digests a day · `DONE:` replies in the feed per day → ≥ 1 | idp (hermes gateway) |
| 1.8 | **Record, not confession** | idea 10 | rewrite `LAWS-INCIDENTS.md` worked examples in the passive record voice ("the log was not opened"); same evidence, same guard names | first-person guilt in every session's preamble | `grep -c "^I " ~/.claude/LAWS-INCIDENTS.md` → 0 · every incident still cites its guard | crew |

**Stage 1 gate, all seven lines true for 7 consecutive days:** `AGENTS.md` ≤ 209 lines · rulings added ≤ 1/day · praise count > 0 · `FOUNDER ACTION:` ≤ 3/day · `DONE:` ≥ 1/day · zero re-found incidents (`bin/recall --dupes` → 0) · `PUSHBACK:` ≥ 1 in the week. `scripts/estate-snapshot` prints the seven as one row, `union stage 1`, NOT RUN when it cannot measure.

---

## Stage 2 — One organism (7D · 8D · 9D)

*Gives the body a why and a pulse. Founder cost: one hour of speech, transcribed, once.*

| # | workstream | closes | mechanism | removes | gate | lane |
|---|---|---|---|---|---|---|
| 2.1 | **The why, in his words → the manifesto** | ideas 11, 12, 13 | one hour, recorded, transcribed to `docs/MANIFESTO.md`: who the estate is for the day after the sale; one named persona each for prospector and hermes-v2 in the catalog; engineering and ops charters in `roles/` with the sentence an agent may push back with. This page's §4 is the seed | "a buyer's engineer" as the only reason; PR bodies that name no person | `docs/MANIFESTO.md` exists in his words · every new PR body has a `Who this helps:` line naming a persona (pr-evidence check) | founder (1 h) + crew |
| 2.2 | **The founder as a node with an SLO** | ideas 4, 18; bind 5 | STATE.md rows: quiet window 23:00–07:00 honoured (no push except P0 with a cost line), Mac load < 8, `FOUNDER ACTION:` ≤ 3/day, hours since last praise < 24. Red like any service; the scheduler and the gateway read the window | 01:10Z decisions; the laptop as his nervous system | `scripts/estate-snapshot` → four `founder` rows GREEN 7 days · `launchctl` shows no notification job inside the window | crew + idp |
| 2.3 | **The mirror, generated monthly** | idea 14 | the science lane re-runs the audit's counts (repeats, avoidances, laws fired, praise, strain) from feed + rulings, one page, red rows first, on the showcase | self-knowledge that depends on a session remembering to ask | `bin/science-collect mirror` → page with a date newer than 31 days | science |
| 2.4 | **The day-after-the-sale drill** | idea 20; the 9D sentence | `drills/catalogue.yaml` entry `founder-unreachable-72h`: the gateway blackholes founder-bound messages for 72 h in a rehearsal; the row grades receipts landed, asks raised (must be 0), incidents repeated (0), digest produced on return | the last untested assumption: that it runs without him | drill row GREEN in `bin/idp-verify` · founder receipt: one tap on the return digest | idp |

**Stage 2 gate = 9D:** the drill is green, the four founder rows are green for 7 days, and `MANIFESTO.md` is merged with his receipt.

---

## 3. Coverage — nothing left behind

| audit item | stage.workstream |
|---|---|
| ideas 1, 2 | 1.7 |
| idea 3, 7, 15 | 1.1 |
| idea 4 | 2.2 |
| idea 5 | 1.2 |
| idea 6 | 1.3 (done) |
| ideas 8, 9 | 1.4 |
| idea 10 | 1.8 |
| ideas 11, 12, 13 | 2.1 |
| idea 14 | 2.3 |
| ideas 16, 19 | 1.6 |
| idea 17 | 1.5 |
| idea 18 | 2.2 |
| idea 20 | 2.4 |
| bind 1 autonomy vs sole authority | 1.6, 1.7 |
| bind 2 speed vs zero-repeat | 1.1, 1.2 |
| bind 3 never ask vs FOUNDER ACTION | 1.6 |
| bind 4 hive mind vs two sub-agents | 1.2 |
| bind 5 enterprise vs the Mac | 2.2 (with crew#516 Mac exit, already BLOCKING) |

## 4. Why two stages and not three

Stage 1 is every change that needs no decision from him and can be proved by a count. Stage 2 is every change that needs his voice or a rehearsal of his absence. A third stage would only be Stage 2 split in half, and the drill cannot be half-run. Ordering inside a stage is by the `removes` column: the workstream that deletes the most text or the most unread lines goes first (1.1, 1.6, 1.7, then the rest).

## 5. Manifesto seed — sentences the evidence already earned

For him to keep, cut or rewrite. Not one is a law.

1. We say a thing once, and the estate remembers it for us.
2. What can be undone is done and announced; what cannot is his, and there are three of those.
3. A mistake is a record, not a confession. The record is read by a machine, not by every session at dawn.
4. The crew may say no once per session, with the cost, and nobody is punished for it.
5. The founder is a node of this system. His sleep is an SLO. His anger is telemetry, and so is his thanks.
6. The buyer is a check. The customer is the reason. Every change names who it helps.
7. The laws may not grow. When two protect the same fear, they are one.
8. Once a month the estate reads itself the way this audit did, and the red rows go first.
9. The proof that it runs without him is that it ran without him for three days, and on his return it told him what he could now do.

## 6. How this page stays visible

- `README.md` links it in the first paragraph, next to `STATE.md`.
- crew#596 is pinned in the repository and carries the two stage gates as checkboxes; only a green gate ticks one.
- Telegram holds the file (sent by the session that wrote it) and the digest links it until Stage 1's gate is green.
- `roles/founder.md` names it as the page every session reads when it wonders why a rule exists.
- The monthly mirror (2.3) reprints §0 with fresh numbers; when the numbers stop moving this page is finished, not lost.
