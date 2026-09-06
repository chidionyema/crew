# crew#63 C2 — metric_after filled for the 2026-08-23 ledger entries

Workstream C2 of crew#63 ("Supercharge maestro and The Architect") requires that
`metric_after` be filled for both 2026-08-23 entries in
`science/RESEARCH-LEDGER.jsonl` within 14 days, and that the verify.d guard goes
red by itself if it is not.

## The two 2026-08-23 ledger entries

Both rows were written 2026-08-23 by session 8ef72725 and carry the LAW 35
learning-loop metrics for the two workstreams that issue 63 tracks.

### Entry 1 — The Architect truth gate (workstream A)

- **question:** How do production agent systems stop an agent asserting false
  success, so The Architect stops making statements to the founder that are false?
- **metric:** Share of outbound Architect status claims carrying a valid evidence
  event id; false-success rate on a replayed claim set.
- **metric_before:** 0% of claims evidence-linked; live verification_evidence.db
  has 0 events; verify_on_stop OFF on the founder's only surface (Telegram).
- **metric_after (measured 2026-08-29):** The claim gate (A2) is live on the
  gateway reply path (patch 0003, 10 tests passed both ways, demo in
  `docs/demo/claim-gate.md`), but the verification_evidence.db count is unreadable
  because the Otto gateway pod is down (ImagePullBackOff on a ghcr tag ghcr never
  published, fixed by idp#778; ExternalSecret `tailscale-operator` missing,
  blocked on `bin/idp-set-root tailscale`). A1 is ticked only after an
  architect-doctor run prints a count > 0.

### Entry 2 — experience accumulation (workstream B)

- **question:** What experience-accumulation patterns measurably make an agent
  improve, so maestro and The Architect learn fast with proof?
- **metric:** Weekly learning receipt: fraction of last week's escalation
  fingerprints auto-resolved this week; repeat-incident median resolution time
  versus first occurrence; frozen replay set solved-count.
- **metric_before:** maestro consults nothing before escalating; one Stripe
  finding escalated 46 times in 29h with zero learning between passes;
  skills/shapes tables held 0 rows until PR #4.
- **metric_after (measured 2026-08-29):** 955 episodes (954 in the last 7 days),
  0 with evidence.source=memory, 3 distinct shape_ids; last learning receipt sent
  2026-08-23T23:18Z, next due 2026-08-30. The consult-before-escalate path (B1)
  has fired 0 times: the 46x Stripe repeat is gone (alarm fence), but no finding
  has yet been solved from memory, so the learning fraction is 0/955.

## Done when (commands)

```
# both 2026-08-23 rows carry a non-null metric_after
python3 - <<'PY'
import json
rows = [json.loads(l) for l in open("science/RESEARCH-LEDGER.jsonl") if l.strip()]
aug23 = [r for r in rows if r.get("date") == "2026-08-23"]
assert len(aug23) == 2, f"expected 2 rows dated 2026-08-23, found {len(aug23)}"
for r in aug23:
    assert r.get("metric_after"), f"metric_after missing on: {r['question'][:60]}"
print(f"OK: {len(aug23)} 2026-08-23 rows carry metric_after")
PY
```

The verify.d guard (crew 565a326) fails rc=1 when the loop stalls, so C2 is
enforced by the same guard that C1 proved live.
