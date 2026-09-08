## RESUME HERE

**2026-09-07 ~21:55Z — idp session 5af3f159.** Why the estate snapshot stopped: the one
scheduler (Dagster) has not started since 2026-09-03 14:11. `idp/bin/scheduler-up` refuses to
boot when code location `estate-facts` is absent, and its file
`crew/science/scheduler/estate_dagster/facts.py` exists only on the crew branch
`docs/adr0002-diataxis-sweep` — it was never merged to crew main. So all 37 jobs, the hourly
`com.founder.estatesnapshot` among them, have ticked zero times and `crew/STATE.md` has been
stale since 2026-09-03 02:35.

In flight on branch `fix/estate-facts-code-location-missing-on-main`: restore
`science/scheduler/**` (9 files, 537 lines, all additions) onto main, then start the scheduler
and prove a real tick.

Also open, in idp: `bin/scheduler-up` treats one missing location as a reason to run none of
the 37 jobs (LAW 38 — a guard that refuses correct work is an outage). A missing location must
warn and still start; a location that fails to import may still refuse.

Left where it was: idp PR #2338 (draft, checks settled) and #2386, both needing founder review.
