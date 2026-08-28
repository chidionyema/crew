# Decision rights

**The founder edits this page. A session may not.** Road Stage 1.6 (crew#596), from audit §4 and R49.
It exists so that "don't wait on me" and "only I decide" stop being a bind: three things are his, and
everything else is the crew's, done at once, announced, and undoable.

## His — the only three `FOUNDER ACTION:` may name

| row | what it means | examples |
|---|---|---|
| **Money** | anything that charges a card, signs a contract, or changes a recurring bill | a new paid plan, a cloud budget above the one set, an invoice |
| **Identity** | anything only a human account holder can grant | a device in his hand (2FA, a phone), sole-admin console steps with no API (R30, crew#281) |
| **Irreversible** | anything with no undo inside the estate | deleting a repository or a tenancy, a public statement, a customer contract term |

Everything not in a row above is the crew's. `founder-blocker.py` refuses a `FOUNDER ACTION:` that
names none of the three (Stage 1.6 gate). A crew decision is announced once in the feed and on the
issue, with its undo command; he may reverse it by saying so (R40, R49).

## Trade-offs he has chosen (the five binds from the audit, named so they stop being traps)

Each row is the default the crew acts on until he edits it here. The right-hand column is his to change.

| the bind | the side taken now | why (his own ruling) |
|---|---|---|
| autonomy vs "only I declare done" | **crew ships to `INVENTORY:`; `DONE:` is one tap on the digest** (Stage 1.7), never a sentence he must write | R5 "out of the loop"; R27 "merged is inventory" |
| speed vs zero-repeat | **speed, with one memory** (Stage 1.2): a mistake is recorded once and queried, not guarded a second time | R40 "no just go"; R2 "durable memory" |
| never ask vs `FOUNDER ACTION:` | **ask only for the three rows above; at most three a day** | R5, R47, crew#281 |
| hive mind vs two sub-agents | **two sub-agents stays; the hive is the shared memory, not the process count** | `.claude.md` governor; R33 |
| enterprise vs the Mac as substrate | **the cluster is the substrate; the Mac is a client** (crew#516 Mac exit) | R26, R43, R44 |

## How to change a row

Edit this file on main. That commit is the ruling; friction-relay reads the table at session start
once Stage 1.6 CP2 lands. Until then a session that finds a conflict between this page and a ruling
follows this page and says so with a `PUSHBACK:` line (Stage 1.5).
