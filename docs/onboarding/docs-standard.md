# Onboarding: the documentation standard

Owner: claude/science
Last true: 2026-08-24

## What this is for

Documents were being written faster than anybody could keep track of them, and nothing
counted them. On 2026-08-24 the estate held 190 documents across seven repositories, not
one of which named a maintainer, and four of which existed only on one laptop. A page
nobody owns rots, and a rotted page is worse than a missing one because it still reads
as current. This turns that from a complaint into something a machine refuses.

## What it costs

Nothing recurring. `science/docsmap.py` is standard-library Python plus `git`, and the
gate is bash. A full run over all seven repositories takes about two seconds. There is
no service, no account, no daemon and nothing to renew.

## What it watches

Every `.md` file in the seven repositories this estate owns. Vendored trees, plugin
caches and archived checkouts are excluded on purpose, because grading somebody else's
README teaches this estate nothing and would bury the real number under fifteen thousand
files from `node_modules`.

It grades four rules:

- **persisted** — the file is tracked by git, so it survives the disk and shows a diff.
- **owned** — the file carries a line naming who maintains it.
- **dated** — the file carries a `YYYY-MM-DD` a machine can read.
- **substantial** — over 200 characters of prose once headings and code fences are
  stripped, so a heading with nothing under it cannot satisfy the gate.

It never edits a file. It reports, and the gate refuses.

## Where it lives

```
science/docsmap.py             the inventory
science/DOCS-BASELINE.json     the tolerated backlog, shrink it, never grow it
scripts/verify.d/95-docs.sh    the gate, run by scripts/verify.sh and by CI
```

## How to turn it off

One command, and it takes effect immediately:

```bash
chmod -x scripts/verify.d/95-docs.sh
```

The suite skips any check in `verify.d` that is not executable. To remove it entirely,
delete that one file; nothing else depends on it.

## How to turn it back on

```bash
chmod +x scripts/verify.d/95-docs.sh && bash scripts/verify.d/95-docs.sh
```

## What goes wrong

**It refuses a document you just wrote.** That is the design: new work is held to the
standard from the day it is written. Add the owner line, add the date, and stage the
file. If it refused something it genuinely should not have, that is an outage under
LAW 38 and the gate is what gets changed, not the document.

**It says the baseline is missing.** Somebody deleted `science/DOCS-BASELINE.json`.
Regenerate it with `python3 science/docsmap.py --write-baseline
science/DOCS-BASELINE.json`, but read the diff first: regenerating it against a worse
tree silently forgives every failure introduced since the last one.

**The count drops in CI.** Expected. Only this repository is checked out on a runner, so
only its documents are graded there. The baseline is keyed by repository as well as
path, so an absent repository contributes nothing rather than reading as fixed.

## How the backlog goes away

By deleting lines from the baseline, never by adding them. `owned` is the cheapest of
the four rules and closes all 190 on its own, one repository at a time.
