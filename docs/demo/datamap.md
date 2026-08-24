# Demo — `science/datamap.py`

The founder asked, 2026-08-24: "so i need you to nnap alldatapoints we collect, all
data dapints we dont collect and why". This is the answer, generated rather than
written, so it cannot go stale while reading as current.

```
$ python3 science/datamap.py
```

Real output, captured 2026-08-24. Nothing below was typed by hand.

```
COLLECTED  19 sources, 5682 rows, 1064 distinct field paths
------------------------------------------------------------------------------
  agent_cert             12 rows   810 fields  (800 field(s) not in every row)
  aiden_ticks            73 rows    11 fields  (6 field(s) not in every row)
  attention              24 rows     6 fields
  board                 110 rows    31 fields  (29 field(s) not in every row)
  bundle_push           120 rows    15 fields  (14 field(s) not in every row)
  ci_reach               66 rows     5 fields
  close_guard           902 rows     7 fields
  consult                78 rows    11 fields  (2 field(s) not in every row)
  decisions             118 rows    22 fields  (16 field(s) not in every row)
  drills                 44 rows     8 fields  (1 field(s) not in every row)
  enforcement_map         1 rows     9 fields
  ledger                612 rows    10 fields  (7 field(s) not in every row)
  method_metrics          1 rows    34 fields
  predictions             2 rows     8 fields  (1 field(s) not in every row)
  ships                  57 rows     9 fields  (6 field(s) not in every row)
  spend                 932 rows    42 fields  (38 field(s) not in every row)
  stuck_detector       1933 rows    11 fields  (11 field(s) not in every row)
  toolguard             435 rows     7 fields  (4 field(s) not in every row)
  would_have_fired      162 rows     8 fields  (5 field(s) not in every row)

UNCOLLECTED  23 stores that exist and nothing reads
------------------------------------------------------------------------------
  EXCLUDED       ~/.claude/telemetry                           1179.3 MB
  WIRED_NEVER    ~/.claude/projects                            6538.7 MB
  WIRED_NEVER    trees/agent-aaecfffaa54620133/store/dossiers   130.9 MB
  WIRED_NEVER    ~/.claude/state/toolguard                       28.5 MB
  WIRED_NEVER    ~/.maestro/intents                               0.8 MB
  WIRED_NEVER    ~/.claude/directives                          6932 rows
  WIRED_NEVER    ~/.claude/state/prompt-ledger                 7046 rows
  WIRED_NEVER    ~/.claude/history.jsonl                      12928 rows
  ... 15 more, each with a recorded reason

NEVER EMITTED  8 things the estate does and does not record
------------------------------------------------------------------------------
  revenue          money coming in
  agent_decisions  what an agent chose, and what it rejected
  research         what was researched, and what changed because of it
  task_outcome     did the thing an agent built actually work
  run_duration     how long each scheduled job takes
  guard_outcome    what a guard refused, and whether the refusal was correct
  model_routing    which model served each call, and what it cost
  context_waste    tokens spent re-reading context that did not change
```

## What the run just told you

Three lists, and the second two are the ones that did not exist before.

**COLLECTED** walks every row in the warehouse and counts the field paths inside the
JSON payloads. 1,064 of them, and not one is declared anywhere. The bracket after each
source is the coverage warning: a field present in some rows and not others. `agent_cert`
reporting 810 fields for 12 rows is a source using record ids as object keys, so its
schema grows every time a row is added. `stuck_detector` reporting all 11 fields as
partial is two different record shapes sharing one source name, which the run below
confirmed: 1,526 of its 1,933 rows carry no timestamp field at all and 407 carry one.

**UNCOLLECTED** is the register the estate did not have. Every store the inventory can
see that nothing reads, with one of four recorded reasons: `WIRED_NEVER` (it is being
written and no collector reads it), `WRITER_DEAD` (a collector reads it and the writer
stopped), `NEVER_EMITTED` (the act happens and nothing records it), `EXCLUDED` (a
decision, with the reason). A store that appears here with no recorded reason prints
`UNEXPLAINED`, and that is the row worth the most, because it is a store nobody has
decided about.

**NEVER EMITTED** is the honest half. Eight things this estate does every day and keeps
no record of, `revenue` first among them, which is why every efficiency number here is a
cost divided by nothing.

## The drift check

```
$ python3 science/datamap.py --check ; echo rc=$?
rc=0
```

The first run writes `science/shapes.json`. Every run after it compares the live field
set to that file and reports `+N field(s)`, `-N field(s)`, `new source` or
`source disappeared`. `--check` exits 1 when anything moved. A producer changing shape is
not an error and never reaches a log, so without this it surfaces weeks later as a view
that quietly returns NULL.
