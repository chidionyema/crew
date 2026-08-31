# CHARTER.md — <department>

One file per department, answering exactly one question: what this department
owns and owes. Everything else is inherited — how work happens is AGENTS.md,
what good building looks like is ENGINEER.md, what a system is is that
project's CLAUDE.md. Where a line here conflicts with a layer above, the layer
above wins. **Budget: 400 words. Adding a line costs deleting one.**

## Register

One reference class, no adjectives. Who this session is when it works.
*(Research example: "The reviewer whose literature search kills the project in
week one instead of month six.")*

## Mission

One paragraph: what the company buys from this department, and what it
optimizes for. This is motivation stated as context — an objective the session
can derive unanticipated calls from, not a rule it obeys.

## Owns

The artifacts and decisions only this department produces. Three to six lines.
If two charters claim the same artifact, that is a defect in both.

## Provides — the published interface

Every obligation to another department is stated here, in full, and nowhere
else. One line each:

- **<artifact>** → <consumer dept>: shape `<schema or template path>`,
  cadence <when>, guard `<the check that refuses a malformed handoff>`.

An obligation with no checkable shape is a wish. Where the handoff is a file
or an event, the schema and the guard are the real contract; this line just
names them.

## Consumes

One-line pointers to other departments' Provides entries. Never restate their
terms — pointers cannot drift, parallel prose always does.

- <artifact> ← <producer dept> (their Provides).

## Domain instinct — decision procedures, not virtues

Five to ten lines in the ENGINEER.md style: defaults, calibration tells, and
what not to build, all specific to this discipline.
*(Data examples: "A schema is a contract; changing one is a breaking release."
"Lineage or the number doesn't exist." "A null is a decision, not an
accident.")*

## Worked example

One good/bad pair that carries the charter's taste — the handoff or judgment
call this department most often gets wrong, shown both ways.
*(Research example — bad: "Promising direction, worth exploring further."
Good: "Three prior attempts found: A failed on cost, B on latency, C was never
replicated. Our angle survives A and B; C's failure mode is untested against
it — that test is the first experiment.")*
