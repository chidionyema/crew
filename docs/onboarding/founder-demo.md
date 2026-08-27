# Onboarding — bin/founder-demo

## What it is for

The founder asked for a showcase and a demo of the science lane he would never have to ask
for again (crew#403). `bin/founder-demo` is that demo: one command, three steps, ends with
its own elapsed time so a recording is a receipt.

## Who reads it

The founder, before an investor or buyer conversation. The reviewer of any science PR: the
demo is the acceptance run for the showcase page.

## The command

    cd ~/dev/code/crew && bin/founder-demo

Step 1 runs `science/showcase.py --check` and stops the demo if a capability cannot describe
itself (no docstring line or no `__main__`). Step 2 regenerates `docs/science/SHOWCASE.md`
from the stores on disk. Step 3 prints the page. The last line is
`founder-demo: <N>s, page docs/science/SHOWCASE.md, portal surface founder-showcase`.

## The failure it names

Exit 1 from step 1 means a science module was added without a description or an entry
point; the offending file is printed by name. `scripts/verify.d/27-showcase-check.sh` refuses
the same thing in CI, so the demo cannot fail on main for that reason.

## Where it is surfaced

Backstage component `founder-showcase` (idp#355) links the page and this command.
