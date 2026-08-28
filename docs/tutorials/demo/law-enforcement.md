# Demo: law-enforcement

What this shows: which of the 32 laws a machine actually enforces right now, and
which ones are prose that nothing checks. Run it and you get a verdict, not an
opinion. Every line below is real output from the run whose command is printed
above it. Nothing here was typed by hand.

## The command

```
python3 science/law_enforcement.py
```

## What came back

```
==========================================================================
GUARD ENFORCEMENT TIER
==========================================================================
  PREVENTIVE  directive-capture        UserPromptSubmit       -
  PREVENTIVE  jargon-guard             Stop                   -
  PREVENTIVE  laws-link-guard          SessionStart+Stop      LAW 24
  PREVENTIVE  peer-loop-fence          SessionStart           LAW 12
  PREVENTIVE  prompt-ledger            Stop                   -
  PREVENTIVE  secret-scrub             Stop                   LAW 21,28
  DETECTIVE   batching-compliance      via tool-drip-guard.py -
  DETECTIVE   context-guard-hook       scheduled              -
  DETECTIVE   hang-guard               via rule-guard.py      -
  DETECTIVE   rule-guard               scheduled              -
  DETECTIVE   tool-drip-guard          scheduled              -
  DEAD        agent-fleet-fence        no caller              -
  DEAD        canonical-root-guard     no caller              -
  DEAD        close-guard              no caller              -
  DEAD        dupe-work-fence          no caller              -
  DEAD        goal-guard               no caller              LAW 1,2,9
  DEAD        guard-autocommit         no caller              LAW 6
  DEAD        idle-guard               no caller              -
  DEAD        repeat-guard             no caller              LAW 1,5,6,16
  DEAD        role-guard               no caller              LAW 11
  DEAD        scope-guard              no caller              LAW 1
  DEAD        tmp-shadow-guard         no caller              -
  DEAD        worktree-git-guard       no caller              -

  23 guards: PREVENTIVE=6  DETECTIVE=5  DEAD=12

==========================================================================
LAW COVERAGE
==========================================================================
  laws declared          : 32
  cited by a live guard  : 4   [12, 21, 24, 28]
  PROSE ONLY (no guard)  : 28   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 25, 26, 27, 29, 30, 31, 32]

==========================================================================
LAW -> CHECK
==========================================================================
  mechanical (a machine can decide it) : 17
  partial    (a smell, not a verdict)  : 9
  judgement  (will never be code)      : 6

  mechanical AND live                  : 6 of 17
  THE GAP                              : [3, 5, 7, 13, 16, 17, 22, 23, 25, 30, 31]
    LAW 3   PreToolUse   Write creates a new path whose distinctive symbol ne
    LAW 5   Stop         reply contains 'founder action' or an ask aimed at h
    LAW 7   pre-push     git fetch origin main && test $(git rev-list --count
    LAW 13  Stop         reply to the founder carries neither a platform line
    LAW 16  Stop         the session dropped a thread and wrote no checkpoint
    LAW 17  Stop         reply opens with DONE and contains no command output
    LAW 22  pre-push     scripts/pr-evidence.py check --pr N
    LAW 23  Stop         reply ends by naming two options and their costs ins
    LAW 25  PreToolUse   work starts on a new issue while the previous one's
    LAW 30  Stop         a run produced a result and appended nothing to the
    LAW 31  Stop         reply to the founder contains an imperative aimed at

==========================================================================
TRACKING FRESHNESS
==========================================================================
  STALE     43.1h      434 lines  state/toolguard/events.jsonl
  STALE     43.1h      760 lines  state/close-guard-observe.jsonl
  STALE     42.0h      162 lines  state/one-branch/would-have-fired.jsonl
  STALE     43.1h      303 lines  state/ledger.jsonl
  live       0.2h      149 lines  ESTATE_BOARD.jsonl
  live       0.2h      899 lines  estate-spend-history.jsonl

  4 stream(s) silent >24h

wrote /Users/chidionyema/.claude/state/law-enforcement.json
```

Exit code was 1. That is the design: it exits 1 while any mechanical law sits
unenforced or any tracking stream has gone silent, so a scheduler can read the
verdict without reading the text.

## What it just did

It read the 32 law headings out of `~/AGENTS.md`, read the hook wiring out of
`settings.json`, then walked the call graph of every guard script on disk to
decide whether each one can refuse a mistake in flight, only notice it later,
or never runs at all. It compared that against `science/enforcement-map.json`,
which is the line-by-line translation of each law into the check that would
decide it. The gap it printed is the list of laws a machine could enforce today
and does not.
