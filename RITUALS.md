# Rituals

Scheduled reviews the estate runs on its own clock. Each section is what a job reads before it runs — if the file and the job disagree, the file wins; fix the job.

## Sunday review (weekly, `sunday-review` cron)

Most of the job is deleting lessons that did not help. Read `CORRECTIONS.md` and `DECISIONS.md` since the last review. For each entry: has it actually changed behavior since it was written, or is it dead prose nobody checks anymore? Delete what never got used. Keep what did, and say what evidence proves it's still in force.

## Architecture drift review (weekly, same `sunday-review` slot)

Added 2026-08-26, founder: "we need regular scheduled catchups to ensure architecture never drifts as we are moving so fast."

CI (`bin/idp-ci`, OPA/conftest against `idp/policy/*.rego`) enforces architecture mechanically, per-PR, against rules someone already wrote a gate for. This section is the check for everything CI can't see: drift in direction, decisions nobody wrote a gate for yet, and duplication CI has no way to detect because it isn't a syntax rule.

Each run, answer with real commands, not memory:
1. **New parallel systems.** `gh issue list` across crew/idp/hermes-v2/prospector for tickets opened this week proposing new infrastructure. For each: does it duplicate something crew#126's standard-stack table, or an existing service, already covers? Flag duplicates as comments on the older ticket, don't silently let both proceed.
2. **Master tickets still open, still current.** crew#126 (platform migration), crew#227 (auth v2), crew#284 (KINI spec) — read their checkpoint state. Which checkpoints moved this week, which stalled, is the direction still right or has reality moved past the plan.
3. **New `.rego` gates needed.** Any incident this week that a human had to catch by eye, that a machine check could catch next time — LAW 45's own protocol (name the class, gate it, prove it both ways, sweep existing instances). List what's missing, don't just note it happened.
4. **Cron/job drift.** `hermes cron list` — any job whose prompt references a file, label, or command that no longer exists (the exact bug crew#316 found in this job's own prompt). Verify each job's actual dependencies still resolve.
5. **Vendor lock-in additions.** Anything adopted this week that's a new external dependency — does it earn its place under LAW 19, or was it added without checking whether the standard tool already covers it (crew#309's audit).

Report: what moved, what's stalled, what's now duplicated, what's now gated that wasn't. Not a status essay — each line names a ticket or a command output.

## Sunday proposals (weekly, `sunday-proposals` cron)

Three issues on `chidionyema/prospector`, the three things most worth doing next. Unrelated to the two sections above; kept separate because proposals are forward-looking and the reviews above are backward-looking — mixing them buries the "what's next" signal under a retrospective.
