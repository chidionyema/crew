# Demo: silent side effects

Run:

```
python3 science/silent_side_effect.py
```

Real output from this machine on 2026-08-23, trimmed to the head and the tail
because the middle is twenty more rows of the same shape:

```
==========================================================================
SILENT SIDE EFFECTS  (a guard that cannot report its own failure)
==========================================================================
  ~/.claude/scripts/close-guard.py:177
      swallows : Exception
      hiding   : mkdir(), replace(), write_text()
  ~/.claude/scripts/context-guard-hook.py:170
      swallows : Exception
      hiding   : dump(), open(...,w)
  ~/.claude/scripts/session-recorder.py:240
      swallows : Exception
      hiding   : open(...,w), write()
  ~/.claude/scripts/tool-drip-guard.py:203
      swallows : Exception
      hiding   : makedirs(), open(...,w), write(), writelines()

  24 place(s) where a failed act looks exactly like a successful one.
  8 more are cleanup only (a leftover temp file), listed with --all.
```

## What it just did

It read every Python file under `~/.claude/scripts` and looked for one shape:
a `try` that writes a file, sends a message or runs a command, wrapped in an
`except` whose entire body is `pass`. When that combination is present the
script cannot fail out loud. It carries on, returns normally, and the next
thing to look at it sees a guard that ran.

The third row is the one that started this. `session-recorder.py` rebuilds the
founder's recovery file after every turn. It had been swallowing its own
exceptions since 21 August, which means a broken recorder and a working
recorder produced identical evidence: nothing.

Twenty-four is not a list of bugs. It is a list of places where, if a bug ever
appears, nobody will hear about it.
