# Demo: the hazard register

    scripts/hazard-register --check

Renders `docs/HAZARDS.md` from `risk/REGISTER.jsonl` and the open P1 issues of crew and idp:
open hazards first, most likely first, each with the fire that realised it. Exit 1 lists every
open P1 that names no hazard. `scripts/verify.sh` runs it in report mode (`verify.d/87`).
