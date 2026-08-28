# Demo: the estate watches the world's releases (crew#508 CP8)

Founder, 2026-08-27: "there is wealth of info and data out there and we need to be future
proof, we cant afford to rest on laurels and fall behind on research."

```
python3 science/research_intake.py pull       # newest release of every STANDARDS.md tool
python3 science/research_intake.py --print    # the intake table
python3 science/research_intake.py --check    # exit 1: pull >2 days old, or a candidate >7 days unanswered
python3 science/research_grade.py --print     # Outward now carries the intake block and grades it
```

Expect: `pulled 22 repos, N new, 0 unreachable`, then a table with `Last pull … (fresh)`,
`Candidates unanswered`, and the ten newest releases with their status. The first release seen
per repo is `baseline`; a release that arrives after watching began is a `candidate` until
someone sets `status` to `adopted` or `declined` with a `ticket` on
`science/RESEARCH-INTAKE.jsonl`. Dagster runs the pull daily (`com.estate.research-intake`);
the hourly estate snapshot republishes `docs/science/RESEARCH-GRADE.md` with the result.
