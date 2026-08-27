# Demo — `science/datamap.py`

The founder asked, 2026-08-26: "map all the data points in the estate, anything that
produces data and anything that can be measured ... find a creative way to automate this so
this is the first and last time we ever need to do this ... this needs to be encapsulated in
law." This is LAW 50. The map is discovered, never typed.

```
$ python3 science/datamap.py --check
```

Real output, captured 2026-08-26 from the command above. The COLLECTED block (warehouse
tables, row and field counts) is unchanged from the previous demo and omitted here; the
DATA MAP, GAPS and GATE blocks are the new part.

```
DATA MAP  8292 producers in 10 domains, 78306 measurables
------------------------------------------------------------------------------
  domain         total  COLLECTED  WIRED_NEV  WRITER_DE  NEVER_EMI   EXCLUDED  UNEXPL
  act                8          0          0          0          8          0       0
  cluster           99          5         80          0          0         14       0
  cluster_live   BLIND   RuntimeError: Unable to connect to the server: getting crede
  endpoint           5          0          5          0          0          0       0
  github            79         46          0          0         33          0       0
  hook              34          0          0          0         34          0       0
  mac              548         93        252          0         64        139       0
  mcp                3          0          0          0          3          0       0
  transcript      7484          0       7484          0          0          0       0
  warehouse         32         32          0          0          0          0       0

GAPS  7963 producers under 47 register entries; each entry carries a ticket
------------------------------------------------------------------------------
  WIRED_NEVER   transcript/*                              7484  crew#319
  WIRED_NEVER   mac/*.claude/directives*                    73  crew#354
  WIRED_NEVER   mac/data/*temporal/dev.db                   49  crew#377
  NEVER_EMITTED mac/guard/*                                 43  crew#374
  WIRED_NEVER   mac/scheduled_job/*                         39  crew#373
  WIRED_NEVER   cluster/*                                   38  crew#388
  NEVER_EMITTED hook/*                                      34  crew#391
  NEVER_EMITTED github/workflow/*                           33  crew#393
  NEVER_EMITTED mac/listener/*                              21  crew#375
  WIRED_NEVER   mac/*experience_graph.db*                   20  crew#352
  WIRED_NEVER   mac/data/*dagster*                          18  crew#376
  WIRED_NEVER   cluster/*/Kustomization/*                   18  crew#344
  WIRED_NEVER   mac/*state/prompt-ledger*                   17  crew#355
  WIRED_NEVER   mac/*jobs/*                                 12  crew#358
  WIRED_NEVER   cluster/*/ExternalSecret/*                  11  crew#387
  WIRED_NEVER   cluster/*/HelmRelease/*                      9  crew#344
  WIRED_NEVER   endpoint/*                                   5  crew#390
  WIRED_NEVER   cluster/*/GitRepository/*                    4  crew#344
  WIRED_NEVER   mac/*state/coord/jobs.sqlite*                3  crew#353
  NEVER_EMITTED mcp/*                                        3  crew#392
  WIRED_NEVER   mac/*.claude/state/toolguard*                2  crew#350
  WIRED_NEVER   mac/data/*sovereign/budget.db                2  crew#378
  WIRED_NEVER   mac/*state/tickets*                          1  crew#357
  WIRED_NEVER   mac/*.claude/history.jsonl*                  1  crew#356
  WIRED_NEVER   mac/*estate-push.j*                          1  crew#360
  WIRED_NEVER   mac/*estate-worktr*                          1  crew#361
  WIRED_NEVER   mac/ledger/*board-deadletter*                1  crew#379
  WIRED_NEVER   mac/*founder-actio*                          1  crew#362
  WIRED_NEVER   mac/ledger/*would-have-fired*                1  crew#380
  WIRED_NEVER   mac/ledger/*.estate/registry.jsonl           1  crew#381
  WIRED_NEVER   mac/ledger/*.estate/REQUIREMENTS.jsonl       1  crew#382
  WIRED_NEVER   mac/ledger/*capability_receipts.jsonl        1  crew#383
  WIRED_NEVER   mac/ledger/*alerts/inbox.jsonl               1  crew#384
  WIRED_NEVER   mac/*estate-board.jsonl*                     1  crew#359
  WIRED_NEVER   mac/ledger/*sovereign/receipts.jsonl         1  crew#385
  WIRED_NEVER   mac/*.claude/projects*                       1  crew#319
  WIRED_NEVER   mac/*.maestro/intents*                       1  crew#351
  WIRED_NEVER   mac/*prospector/store*                       1  crew#363
  WIRED_NEVER   mac/*prospector/.claude/worktrees*           1  crew#349
  NEVER_EMITTED act/revenue                                  1  crew#365
  NEVER_EMITTED act/agent_decisions                          1  crew#366
  NEVER_EMITTED act/research                                 1  crew#367
  NEVER_EMITTED act/task_outcome                             1  crew#368
  NEVER_EMITTED act/run_duration                             1  crew#369
  NEVER_EMITTED act/guard_outcome                            1  crew#370
  NEVER_EMITTED act/model_routing                            1  crew#371
  NEVER_EMITTED act/context_waste                            1  crew#372

GATE  GREEN  every producer has a verdict, every gap has a ticket, no domain silently blind
```

How to read it:

- **DATA MAP**: one row per domain in `science/producers.py`. A domain enumerates every
  producer of its kind from the world (inventory rows and sqlite tables on the Mac, warehouse
  tables, Kubernetes manifests, the live cluster, public hostnames, hooks, MCP servers, repos
  and workflows, transcript directories, the act register). `UNEXPL` is the number of producers
  no register entry matches; one is a red gate.
- **BLIND**: the domain could not read its world. `cluster_live` is blind while the laptop has
  no OKE credential (crew#345) and is allowed by name in `science/verdicts.json`
  `blind_allowed`; any other blind domain is red.
- **GAPS**: every gap verdict (WIRED_NEVER, WRITER_DEAD, NEVER_EMITTED) grouped by the register
  entry that explains it, with the crew ticket that owns closing it. An entry with no ticket is
  red; `--file-tickets` opens the ticket and writes the number back.
- **GATE**: the line CI (`scripts/verify.d/26-datamap-register.sh`) and `STATE.md`
  (`scripts/estate-snapshot`, row `data map`) both print.

## The source contract (crew#71)

```
$ python3 -c "import sys; sys.path.insert(0,'science'); import datamap; print(datamap.contract_violations())"
[]
$ python3 -c "import json; d=json.load(open('science/sources.json')); print(sum('owner' in s for s in d['sources']), 'of', len(d['sources']), 'sources declare owner, method, retention_days, sensitivity')"
28 of 28 sources declare owner, method, retention_days, sensitivity
```

Remove `sensitivity` from one entry and run `python3 science/datamap.py --check --domains act`:
the gate prints `source <name>: no contract field sensitivity` and exits 1.
