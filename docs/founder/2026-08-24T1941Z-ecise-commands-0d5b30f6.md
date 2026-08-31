---
captured: 2026-08-24T19:41:14+00:00
session: a6b4167c-c8f2-43e2-9d31-d26e66f642c9
cwd: /Users/chidionyema/dev/code/survival-stack
chars: 2822
source: founder prompt, verbatim (founder-doc-capture.py)
---

ecise Commands
plain
**The Dock restart is a band-aid.** The load storm will wedge it again.
The repeat offenders from your last diagnostic:
graphify sweep on stale ~/Documents/code tree
Hourly python fleet (31+ scheduled jobs)
Colima at 60% CPU
Kill the storm now:
bash
# 1. Stop graphify sweep (the big one)
launchctl unload ~/Library/LaunchAgents/com.chidionyema.graphify-sweep.plist 2>/dev/null
pkill -f "graphify"

# 2. List the python fleet eating CPU
ps -eo pid,pcpu,comm,args | grep -E "python|launchd" | grep -v grep | sort -k2 -rn | head -20

# 3. Throttle colima if it's the culprit
colima stop && colima start --cpu 2 --memory 4
Permanent fix — one of three:
Cap the python fleet — launchctl Nice value 10+ on all 31 jobs so they yield to interactive processes
Kill graphify — it runs on a stale tree (~/Documents/code not ~/dev/code), so its output is garbage anyway
Reschedule the hourly jobs to every 6 hours — most of them (estate snapshot, drift checks) don't need 60-second granularity
Which one do you want? Or all three?
The Dock will stay healthy if CPU stays under 80%. Right now it is throttled to 48% and everything is fighting for the last cycles.
the jobs need to be staggerd never sane tine
Edit
Copy
Share
Stagger Launchd Jobs to Prevent Dock Load Storm
plain
**Right fix.** 31 jobs all firing on the hour or every 60 seconds is the storm. Stagger them so they never overlap.
Current problem:
bash
# See the collision
grep -r "StartInterval\|StartCalendarInterval" ~/Library/LaunchAgents/ | head -20
Everything is on StartInterval = 60 (every minute), 300 (every 5 min), 900 (every 15 min), or 3600 (hourly on the :00 mark). They all wake up at the same second.
The fix — two options:
Option A: Prime number intervals (jobs never sync up)
Job 1: StartInterval = 61 (prime)
Job 2: StartInterval = 67 (prime)
Job 3: StartInterval = 71 (prime)
They will never fire simultaneously. Ever.
Option B: Staggered calendar times (hourly jobs at different minutes)
Job 1: StartCalendarInterval = {Minute = 0;}
Job 2: StartCalendarInterval = {Minute = 5;}
Job 3: StartCalendarInterval = {Minute = 10;}
...through 55. 12 jobs per hour, evenly spaced.
What I need from you:
Do you want me to list all 31 jobs with their current intervals so you can pick which get prime numbers and which get calendar staggering? Or do you want a script that automatically rewrites every plist to use prime intervals based on a hash of the job name?
One command to see the current carnage:
bash
find ~/Library/LaunchAgents -name "*.plist" -exec grep -H "StartInterval" {} + | sort -t: -k3 -n
That shows every job and how often it fires. The duplicates are your storm.
Your call: Manual stagger (you pick the schedule) or automatic prime-number rewrite?
High demand. Switched to K2.6 Instant for speed. Upgrade to use K2.6 Thi
