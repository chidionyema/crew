---
captured: 2026-08-25T02:58:45+00:00
session: 130c903b-056b-4580-b5c6-8e80ec1fabdc
cwd: /Users/chidionyema/dev/code/crew
chars: 3929
source: founder prompt, verbatim (founder-doc-capture.py)
---

dont forget this features, critical for estte Feature 1: Atomic Time Travel Rollback
What it means: One command rewinds the entire estate — code, DB, policies, configs — to any previous hash. No downgrade scripts. No data loss.
How we deliver it:
cp9 (Shadow Root): Every state change writes a Merkle node. The root hash IS the checkpoint.
cp13 (The Flip): DAG becomes primary. The root hash is now the live truth, not a shadow.
cp15 (Cross-Stack Root): One root points to code_root, db_root, policy_root. Fast-forward that root = fast-forward everything.
CLI: sb rewind <hash> — stops services, snaps root pointer, rebuilds projection views from DAG.
Delivered by: End of Phase 2 (cp13 + cp15 green).
Feature 2: Zero-Cost Parallel Staging
What it means: sb fork staging creates a full copy of production state in under a second, runs tests, then sb drop staging. Zero database copies. Zero server provisioning.
How we deliver it:
cp12 (AI Sandbox): In-memory fork of DB state from the DAG. Copy-on-write for branches.
cp14 (Projection Views): Forked branches compile to temporary SQLite/Redis views for fast reads.
cp19 (Receipt Chain): Every action on the fork is signed and logged separately from main.
CLI: sb fork <branch_name> — branches the root hash. sb switch <branch_name> — moves the working pointer.
Mac constraint: Binary blobs (images, code) are zero-cost via CAS. DB state forks are in-memory; we cap at 3 parallel branches. If you need more, we spill to disk. This is a config key (max_parallel_forks), default 3.
Delivered by: End of Phase 2 (cp12 + cp14 green).
Feature 3: Cryptographic Auditing (SOC2 by Default)
What it means: Every user action, every agent action, every DB diff is an unbroken signed chain. Auditor points at a hash, you prove who did what, when, under which policy.
How we deliver it:
cp19 (Signed Receipt Chain): Append-only. Each entry = prev_hash + payload + signature from macOS Keychain / Windows Credential Manager. This is the audit log.
cp8–11 (DB Sidecar + Dual-Read): Every legacy DB write generates a diff hash. The sidecar logs it to the chain.
cp20 (Trust Anchor): Touch ID / Windows Hello / FIDO2 signs the receipt. Proves human presence for destructive ops.
Output: A single file .estate/audit.chain. Any auditor can verify it with sb audit --verify.
Delivered by: cp19 green (Phase 1 gate). This is the first feature you get.
Feature 4: Recover Last Estate Checkpoint
What it means: System crashes? sb recover restores the last known good root hash and rebuilds everything.
How we deliver it:
cp9 (Shadow Root) + cp13 (The Flip): The DAG is the source of truth. The latest root hash in .estate/heads/main is the checkpoint.
cp14 (Projection Views): On recover, the system rebuilds hot SQLite/Redis views from the immutable DAG. Crash = rebuild, no data loss.
Auto-recovery: On boot, the kernel checks if projection views match the root hash. Mismatch = automatic rebuild from DAG.
Delivered by: End of Phase 2.
Build Order (No Debates)
Table
Phase    Checkpoints    Output
Phase 1    cp1–7 (baseline) + cp18 (budget wall) + cp19 (receipt chain) + cp20 (trust anchor) + cp21 (estate attach) + cp22 (config)    Auditable, signed, budget-governed agent OS
Phase 2    cp8–17 (sidecar → flip → projections → cross-stack root)    Time travel, zero-cost forks, full checkpoint recovery
cp18 and cp19 are gates. They do not block features — they block Phase 2 start. The features in Phase 2 are committed. The gate exists because you cannot let agents fork production state until you can prove they are budget-contained and every action is signed.
What to Tell the Engine Builder Right Now
"Stop debating scope. The 3 superpowers + checkpoint recovery are in the ticket. Build cp18 and cp19 now. Then build cp8–17 in order. No cuts. If Mac memory limits fork count, make it a config key. If legacy DB consistency is hard, build the sidecar. The features are the spec. Deliver them."
