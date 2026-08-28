
## RESUME HERE — session 14ed6c8b, 2026-08-28 ~17:45Z

**Switching from:** crew#488 CP4 (done bar the founder's word) and crew#583 (idp#621, idp#622 both merged).
**Switching to:** crew#437 — the live-checkout row narrates a detached HEAD instead of moving it.

Measured this turn, not remembered:
- `~/dev/code/.crew-state` is the cwd of `com.founder.estatesnapshot` (idp/scheduler/schedule.yml:376-388,
  every 2h). It was detached at `870a04f` (2026-08-27 11:30), **129 commits behind origin/main**, and
  `grep -c "def portability_row" scripts/estate-snapshot` returned **0**. The board the founder reads was
  generated every two hours by a 31-hour-old copy of the generator. Refreshed by hand to `43541c2`.
- `~/dev/code/crew` is also detached, 17 behind origin/main.
- `live_checkout_row()` (scripts/estate-snapshot:433) already watches this, and has been printing
  `| live checkout | RED | on detached HEAD, N commit(s) behind ... the scheduled jobs run that |`
  — then returning without moving anything. Detached-at-an-ancestor is the *safest* case to
  fast-forward (no branch to lose), and it is the one case the function refuses. LAW 28.

**Next step:** worktree `$SCRATCH/detach` off origin/main, branch `fix/crew437-detached-checkout-moves`;
make the detached-at-an-ancestor case take the existing dirty-file/ancestor checks and then
`git checkout --detach origin/<branch>`; keep RED for a *named* branch that is not main (that is a
person's work). Tests + 2 mutations.

**Open elsewhere:** crew#587 (portability row dead-clock fix) is green except review-gate — waiting on
code-5d's `REVIEW:` comment. idp#622 merged. Do not touch `$SCRATCH/tsacl` (stopped crew#562 work).
