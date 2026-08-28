# Demo: founder-demo

## The command

    cd ~/dev/code/crew && bin/founder-demo

## What it printed (2026-08-27, page body elided)

```
== 1/3 every capability can describe and demo itself
showcase --check: 0 refused
== 2/3 the page, regenerated now
wrote docs/science/SHOWCASE.md
== 3/3 the page

Generated 2026-08-27T09:25Z by `python3 science/showcase.py`. Every number is read at generation
time; the command under each heading reproduces it. A section that cannot see its source says BLIND.
```

## What that run established

Every science module carries a description and an entry point, the page was rebuilt from
disk in the same run, and the elapsed time is on the last line. A number on the page that
is not on disk cannot appear.

## What it looks like when it cannot run

Step 1 prints the module that cannot self-describe and exits 1 before any page is written;
the old page stays untouched.
