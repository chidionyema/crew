# Onboarding: a fire names its hazard

When you open a P1, write the register id (`R7`) in the body. If no row fits, add one to
`risk/REGISTER.jsonl` first (verify.d/85 and policy/risk_register.rego check its shape), then cite
it. `scripts/hazard-register --check` is report mode until the unnamed count reaches 0; then it
becomes a gate. Never edit `docs/reference/HAZARDS.md`: it is regenerated on every verify run.
