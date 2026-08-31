# Demo — the audit register and roadmap on the showcase page

Founder, 2026-08-31: what the science lane collects from the estate "must be transparent,
critical for auditing", and the lane needs "a living document detailing their assets and
roadmap".

Both were already on disk — the register in `science/sources.json` (enforced by
`collect.py --check`), the roadmap in `science/PLAN.md` — but neither was on a page a
person reads. Now `docs/science/SHOWCASE.md`, regenerated on every collector run, carries
two more sections.

    $ cd ~/dev/code/crew && python3 science/showcase.py

    wrote docs/science/SHOWCASE.md
      ...
      Datasets collected from the estate  ok
      Roadmap                             ok

## Datasets collected from the estate

One row per dataset the lane copies out of the estate: where it lives, which script
writes it, how it is pulled, its sensitivity, how long rows are kept, its freshness SLA,
and the newest row actually in the warehouse. Below it, every store the machine crawl
found that the lane deliberately does not collect, with the reason. A store in neither
table fails `python3 science/collect.py --check`, so an omission is red in CI, never
silent.

## Roadmap

The goals from `science/PLAN.md`, re-read on every run with the file's last-changed date,
each printed with its `now`, its `target`, and the command that grades it. A goal without
a grading command does not appear.

## Reproduce any number

    $ python3 -m json.tool science/sources.json        # the register itself
    $ sqlite3 science/warehouse.db \
        "select source, max(at) from facts group by source"   # the Newest row column
