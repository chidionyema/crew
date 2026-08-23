# Demo — a pull request has to show the roads it did not take

`pr-evidence.py check` already refused a pull request that carried no screenshot of a green run. It
now also refuses one that never says what else was considered.

## The gate, proved on literal bodies

```
$ python3 scripts/pr-evidence.py selftest-options
  ok   two options and a choice pass
  ok   no section fails
  ok   one option is not exhausting the options
  ok   two options and no verdict fails
  ok   stub bullets do not count as options
  ok   the section ends at the next heading
selftest-options: 6/6 passed
```

Every one of those is paired with its opposite. A gate that passes everything looks exactly like a
gate that works, and this estate has already shipped one that graded 968 replies and passed 98.7%
of them because it was checking formatting rather than evidence.

The two controls worth naming:

- **stub bullets do not count.** `- a` and `- b` under the heading is the obvious way to satisfy a
  word search. The gate counts letters and digits in each bullet and wants 40 of them.
- **the section ends at the next heading.** A `Chosen:` line further down the body, under some
  other heading, does not count as the verdict on these options.

## What a refusal actually says

```
$ python3 -c '... p.options_considered(body_with_no_section)[1]'
no '## Options considered' section. Name at least two options, one line each, and a 'Chosen:' line saying which won and why
```

It says what to write, not that something is missing.

## What a passing section looks like

This is the one from the self-test, and it is a real decision taken while building the ticket
closer:

```
## Options considered
- Rewrite the sweep as a separate scheduled job of its own
- Fold the sweep into the tick that already runs every five minutes
- Chosen: the tick, because a second scheduler is a second thing to go quiet
```

Three lines. The bar is not a design document. It is that a cheaper option was named and rejected
on the record rather than never looked for.
