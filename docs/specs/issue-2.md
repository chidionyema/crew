# Build: the crew runs itself

Issue: https://github.com/chidionyema/crew/issues/2
Written by pm-agent on 2026-08-22 from conversation with @chidionyema.

## What the founder asked for

The crew tracks builds in other repos and was never pointed at its own. Five
commits went straight to main on 2026-08-22, including two bug fixes, with no
issue, no checkpoint and no independent verification. The tool that exists to
stop that was sitting in the same directory.

This build points the crew at the crew, then closes the three wires in
docs/CLOSING_THE_LOOP.md so a conversation reaches a merged pull request without
a person typing each command.

The runner here is pytest, not behave. crew/bdd.py reads both, chosen off the
configured command. Gherkin feature files describing python were the bigger road
and are not cancelled, only lower priority: they are worth writing when a
non-engineer needs to read what the crew guarantees.

The lab lease is survival-stack's work and is tracked there, not here.

## Checkpoints

### CP1: The crew tracks its own work through the crew

Verified by `@pytest.mark.cp1` in `checkpoints/`.

### CP2: A conversation becomes a tracked issue with no person typing `crew plan`

Verified by `@pytest.mark.cp2` in `checkpoints/`.

### CP3: Engineering claims a checkpoint and posts evidence with no person typing

Verified by `@pytest.mark.cp3` in `checkpoints/`.

### CP4: QA verifies on a runner engineering does not control

Verified by `@pytest.mark.cp4` in `checkpoints/`.

