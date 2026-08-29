# Requirements, then spec, then pull request

Founder, 2026-08-29: *"good idea to have reqs -> spec -> pr"*.

Three documents, in order, each answering the one before it. The point is that by
the time code is written, nobody is guessing what was asked for.

| Stage | Question it answers | Where it lives | Who writes it |
|---|---|---|---|
| **Requirements** | What did he ask for, and what did he flag? | `docs/requirements/<date>-<subject>.md` | Whoever heard him say it, in the same turn |
| **Spec** | How will that be built? | `docs/specs/<subject>.md` | A session, from the requirements |
| **Pull request** | Is it built, and does it hold? | one PR, one CI run, one merge | The session that builds it |

Rules that make the chain worth having:

1. **The requirements document quotes him.** It does not summarise him. A summary
   is a session's reading of the founder, and readings drift — the estate has lost
   his words to paraphrase before.
2. **The spec cites the requirements document by path.** A spec that cannot name
   which requirement it satisfies is a session's own idea wearing a spec's clothes.
3. **The pull request cites both.** So a reviewer can check the built thing against
   what was asked, not against what the author remembered.
4. **A flag is a requirement.** When he says "this is worth flagging before you hand
   it to a session", that is not colour. It goes in the table.
5. **An unanswered question blocks only what depends on it.** Everything else proceeds.

Worked example: `2026-08-29-verification-layer.md` → `../specs/verification-layer.md` → crew#656.
