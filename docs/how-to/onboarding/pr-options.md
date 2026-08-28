# Every pull request proves it exhausted the options

## What it is for

To stop the first workable idea from being the only idea. An agent that finds something that works
will ship it, and the cheaper option that was sitting next to it never gets looked for. This gate
asks, on the record, what else was considered and why it lost.

It pairs with the budget on the ticket. The budget catches work that cost more than it should have.
This catches work that took the expensive road when a cheap one existed, which is the thing that
usually causes it.

## What it costs

Nothing to run. It reads text that is already in the pull request body. Three extra lines to write
per pull request.

## What it watches

The body of any pull request that `pr-evidence.py check` is run against. It refuses when there is
no `## Options considered` section, when that section names fewer than two real options, or when it
never says which one was chosen.

It changes nothing. It reads a body and returns an exit code.

## What to write

```
## Options considered
- Rewrite the sweep as a separate scheduled job of its own
- Fold the sweep into the tick that already runs every five minutes
- Chosen: the tick, because a second scheduler is a second thing to go quiet
```

Two options minimum, each a real sentence, and a `Chosen:` line. Bullets under 40 characters are
not counted, because a two-letter bullet satisfies a word search and satisfies no reader.

## Where it lives

`~/dev/code/crew/scripts/pr-evidence.py`, in the `options_considered` function, called from
`check`.

## How to turn it off

```
git revert <the commit that added options_considered>
```

There is no flag, deliberately. A gate with an off switch on it is a gate that is off, and the
whole reason this is mechanical rather than a rule in a document is that a rule agents remember is
a rule agents forget.

## How to turn it back on

Nothing to do. It runs whenever `check` runs.

## What goes wrong

The likely annoyance is a genuinely obvious change — a typo fix, a one-line revert — where there
honestly was only one road. Write the second option as the one you rejected without thinking about
it ("leave it broken", "fix it at the call site instead"), because that is what actually happened
and writing it down costs a line.
