# crew#631 Verification Plane: no work item closes without a fresh signed verdict

Founder, 2026-08-29: "agents are doing half baked work and can no longer be trusted" and "what we have we cant prove it works".

**What this guarantees.** A work item cannot reach CLOSED without a fresh, signed verdict, produced by a process the agent cannot run, bound to the exact artifact that was running. It removes self-certification, not error. The boundary is credential separation: the agent has neither the signing key nor the probe credentials. Cannot, not must not.

**Three planes.** Actor (agents: read, edit, open PRs, propose state). Verification (the prover: a GitHub runner on the estate's machine identity; owns probe credentials and the signing key; emits signed verdicts). Control (ticket state and merge gate; reads verdicts only, never prose).

**Verdict record.** check_id, target, commit_sha, artifact_digest, config_revision, nonce, started_at, completed_at, ttl_seconds, outcome PASS|FAIL|BLOCKED|ERROR, assertions [{name, expected, actual, ok}], evidence_ref, prover_id, prover_run_id, sig (HMAC-SHA256 over the canonical form). Expired, unsigned or wrong-digest verdicts count as absent.

**Probe levels.** L0 reachability, L1 liveness (says nothing about auth, ever), L2 machine plane (API key; does not touch OIDC), L3 human plane (cold SSO handshake; assert on the session identity, never on a cookie; paired negative control mandatory: a fresh context must not get a user), L4 journey (emit a trace over OTLP, read it back through the authenticated API).

**Corrections to the draft spec, each a standing ruling.** (1) No test ids or layout words in a probe: LAW 53. The L3 check is the session identity plus the negative control. (2) The stale file to remove is the state snapshot, not `idp/drills/catalogue.yaml`, which the merge gate reads. (3) No CODEOWNERS approval: probes live where the agent token cannot write, loaded at a pinned digest. (4) Rollout in hours and blockers, never days.

**Already in the estate, reused, not rebuilt.** L0/L1: `idp/platform/monitoring/rules/founder-surfaces-probe.yaml`. L3 cold handshake: `bin/idp-login-drill` (front door into Langfuse, hourly on a runner). Merge gate: rulesets `idp-required-checks`, bypass list 0. Repo `chidionyema/idp` is personal: the gate binds every agent token, and is advisory on the founder himself.

Optimised: naive 9 PRs x (CI run + browser sign-in + vault round trip) = 27 round trips; bottleneck is the browser handshake and the vault. Batched: one prover run yields L1+L2+L3 in one verdict; the probe reuses the drill's cold handshake (no second sign-in); probes are graded locally against a stub Langfuse in open-auth and closed-auth modes (no cluster needed to prove the probe can fail); CP1 stores the verdict as a signed artifact plus check-run, so nothing waits on a database network path. CP1 = 1 PR, 1 CI run, 1 prover run = 3 round trips.

## Checkpoints
- [ ] CP1 Verdict record + HMAC signer (`bin/idp-verdict`), the prover (`bin/idp-prove langfuse`: L1, L2, L3 with negative control, one signed verdict), the prover workflow with a check-run per sha, stub-Langfuse tests proving each probe FAILs when auth is open. Accept when: `bin/idp-verdict verify <file>` prints `ok` on a runner-produced verdict and `FAIL` on the same file with one byte changed; `pytest tests/test_incident_verification_plane_*.py` green.
- [ ] CP2 Signing key readable by the runner identity only: vault policy scoped to the CI dynamic group; a laptop `secret get verdict-hmac-key` is refused. Accept when: the refusal is printed from the Mac and the runner run is green.
- [ ] CP3 Verdict table in the estate Postgres, append-only, `agent_role` SELECT only; the prover writes; `bin/idp-verdict list` reads. Accept when: an INSERT as agent_role is refused and a runner row lands.
- [ ] CP4 Baseline: every agent claim on the board is paired with the verdict of the moment; the false-success rate is a number on the showcase. Accept when: the number is on the page with the query that made it.
- [ ] CP5 Ticket state machine: `RESOLVED_PENDING_VERIFICATION` label; only the prover App moves to VERIFIED/REJECTED; no fresh verdict in 24h reverts. Accept when: an agent label to VERIFIED is reverted by the workflow.
- [ ] CP6 Required check `verify/verdict-fresh` on idp: enforce on Langfuse only. Accept when: a PR touching `platform/observability/langfuse*` cannot merge without a verdict younger than its TTL on its digest.
- [ ] CP7 L4 journey: OTLP trace emitted, read back through the authenticated API inside 60 s. Accept when: the assertion `returned id == emitted id` is in a signed verdict.
- [ ] CP8 Mutation harness: weekly, each probe against a broken target (auth off, wrong digest, DB down) must return FAIL; a probe that passes is quarantined; new probes start UNPROVEN and graduate on one real FAIL and one real PASS. Accept when: the quarantine list is printed by the workflow.
- [ ] CP9 Extend, one surface at a time (catalogue, hermes, SigNoz); each needs L2 + L3 + negative control before it gates. Accept when: three surfaces carry verdicts.

Spec: docs/specs/issue-631.md (this repo).
