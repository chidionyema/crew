# Incident: crew#95 - goal-guard.py tmp->json rename race

## Issue Description
Issue #95 describes a `FileNotFoundError` occurring in `goal-guard.py` at line 236 during a `tmp` to `json` file rename operation. This error is attributed to a race condition where concurrent hook invocations in the same session attempt to write to the same temporary file path. The first `replace()` operation succeeds, but subsequent concurrent operations find the temporary file missing.

## Proposed Fix
The proposed fix is to modify `goal-guard.py` to use a unique temporary file name per writer, for example, by incorporating the process ID (`os.getpid()`) into the temporary file suffix. This would ensure that each concurrent writer uses a distinct temporary file, preventing the race condition.

## Repository Status of `goal-guard.py`
During the execution of the plan for issue #95, it was determined that `goal-guard.py` is not present in the `crew` repository. The file path mentioned in the issue description (`/Users/chidionyema/.claude/state/goal/<session>.tmp`) indicates that `goal-guard.py` is a local file managed by another session.

## Action Taken
Due to `goal-guard.py` not being part of the `crew` repository, a direct code fix within this repository is not feasible. This documentation file is created to record the findings and the proposed solution for future reference, should `goal-guard.py` be integrated into version control. The issue also notes that `goal-guard.py` is currently held dirty by another session, further preventing direct modification.

## Next Steps
The resolution of this issue requires the owner of the local `goal-guard.py` file to incorporate the proposed fix and, ideally, to bring the file under version control within a suitable repository.
