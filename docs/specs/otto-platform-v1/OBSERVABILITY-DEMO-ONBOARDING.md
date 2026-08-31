# Otto v1 — day-0 observability, spec-proving demo, estate onboarding (founder word 2026-08-31)

Founder, verbatim intent: monitoring, logging, tracing — full setup at day 0, no gaps allowed; a
demo that proves the spec is fulfilled; full capability to onboard the estate. Earlier the same
evening: "OTTO NEEDS TOTAL COVERAGE... WE DONT LIKE ANY BLACK BOX."

## What "no gaps" means, measurably (LAW 50)

Coverage is proved by QUERYING the backend, never by scanning files:

- **Gate `otto-obs-coverage`**: before anything is called launched, a check queries SigNoz for
  spans from EVERY otto component (spine, gateway, verify, memory, router, obs itself) and
  Langfuse for at least one model-call trace carrying the same task ULID end-to-end. Any
  component absent from the backend = gate red = no launch. The gate is config-driven
  (component list generated from the signed capability inventory, never hand-kept).
- **Admission**: the otto-staging namespace inherits the estate rule — a workload that does not
  emit to the central collector is refused at admission, not discovered later.
- **No black box**: every task is reconstructable from its ULID alone — trace search (SigNoz),
  model calls (Langfuse), decisions (`otto replay`), verdicts (signed ledger). One id, four
  mirrors, all queryable.

## Optimised plan (LAW 51)

Naive: retrofit instrumentation after launch, write a narrative demo, onboard services by hand —
3 serial retrofits, ~12 steps, every one re-opening merged lanes, rework guaranteed.

Optimised — 4 workstreams, 7 steps, nothing re-opened:

1. **W1 `otto/obs` library (starts NOW, parallel, disjoint dir)**: structured JSON logging,
   OpenTelemetry tracing with ULID propagation, metrics (cost by lane, verdict pass/fail rate,
   budget consumption, taint hits), one `instrument(component)` entrypoint every package calls.
   Exporter endpoint from env (`OTEL_EXPORTER_OTLP_ENDPOINT`), never a literal (LAW 46). BDD:
   emission proven against a local OTLP collector double; a component that starts without
   instrumentation fails its own boot contract (fail closed, not silent).
2. **W2 wiring (integration wave)**: the six packages adopt `otto/obs` on `otto/v1-integration`;
   staging manifests point at the estate collector (SigNoz, observability namespace) and
   Langfuse via ExternalSecrets — the existing backends, no second collector (headline rule).
3. **W3 spec-proving demo (after integration green)**: `bin/otto-demo` — ONE command (R31)
   that replays the falsification set and one full task E2E, then prints a spec-conformance
   matrix: every spec section → the BDD scenario that proves it → the fresh run's result.
   Output is captured into `docs/demo/otto.md` (generated, never narrated) and the launch pin
   carries picture evidence (R66). A spec section with no covering scenario renders as a RED
   row — the matrix cannot lie by omission.
4. **W4 estate onboarding (after integration green)**: `otto onboard <service>` — registers the
   service's tools with the gateway at an explicit tier, signs its capability inventory (CP1's
   Ed25519 inventory reused), allocates budgets, stamps trace attributes, emits the Backstage
   catalog entity, and refuses to finish unless the obs-coverage gate can see the service.
   Onboarding IS the admission ticket: not onboarded = not admitted.

Count: 12+ retrofit steps → 7; re-opened lanes → 0; new proof surfaces → 0 (the demo reuses the
BDD evidence, onboarding reuses the signed inventory, coverage reuses the estate collector).

## Order and gates

W1 runs now beside the verifiers. W2 folds into `otto/v1-integration`. W3+W4 start on
integration green. The launch gate becomes: all verifier verdicts clean + integration green +
`otto-obs-coverage` green + demo matrix all-green. Founder words stay batched as before.
