---
captured: 2026-08-24T19:53:04+00:00
session: a6b4167c-c8f2-43e2-9d31-d26e66f642c9
cwd: /Users/chidionyema/Library/LaunchAgents
chars: 1775
source: founder prompt, verbatim (founder-doc-capture.py)
---

The three tiers:
Table
Approach    What it is    Your current state
Amateur    30 launchd plists, 30 Python scripts, prime intervals    You are here
Better    One scheduler daemon, one policy file, one launchd job    This is the fix
Enterprise    Linux + systemd timers or k8s CronJobs on a server    Where this belongs
The "better" way — one scheduler:
Replace 30 plists with one launchd job: ai.estate.scheduler
It reads a single config — ~/dev/code/estate/schedule.yml:
yaml
jobs:
  estate-snapshot:
    interval: 2h
    command: bin/estate-snapshot
    max_load: 4.0
    depends_on: [in-git-verify]
    
  in-git-verify:
    interval: 1h
    command: bin/in-git.py
    max_load: 2.0
    
  graphify-sweep:
    interval: 6h
    command: bin/graphify --root ~/dev/code
    max_load: 3.0
    skip_if_battery: true
What this gives you that 30 plists cannot:
Dependency chains — snapshot only runs if in-git passes
Resource awareness — skip if load > 4, skip if on battery
Circuit breakers — fail 3 times, stop running, alert you
One log — not 30 scattered logs
One place to see everything — not 30 plists to grep
Why it is more enterprise: This is what Kubernetes CronJobs does. One scheduler, declarative config, resource constraints. You're just running it locally.
The real enterprise answer: This does not belong on your Mac. It belongs on a $5/month VPS (Oracle Always Free, Hetzner, DigitalOcean) running Linux + systemd or k3s. Your Mac is the dev environment. The estate scheduler is infrastructure. Infrastructure does not sleep when you close the lid.
Your constraint says "Mac substrate." Fine. But be honest with yourself: 30 background jobs on a laptop is not a platform. It is a pile. The scheduler daemon is the band-aid that makes the pile look like a system.
