# crew#102 — board contract landed, ten rows named

**Standup.** Single PR, branch `agent-workforce/102`, closes crew#102.

## What landed

One new incident test that names the ten rows of the board contract in
one place, by importing the existing modules and reading the existing
tests' text. No new behaviour, no fork of `scripts/estate-board-sync.py`.

## The ten rows

1. **Board target: chidionyema/crew#102** — `BOARD_REPO`/`BOARD_ISSUE` in
   `tests/test_incident_crew102_estate_board_is_issue_102.py`.
2. **Issue OPEN with "ESTATE BOARD" or "BROADCAST" title** — assertion in
   `test_board_target_is_repo_issue_102`.
3. **Comment rows follow `ts **from** (kind/priority): message`** —
   `COMMENT_FORMAT` in 102-target, `ROW_PATTERN` in 102-read, and
   `COMMENT_FULL_RE` / `COMMENT_SIMPLE_RE` in `scripts/estate-board-sync.py`.
4. **Dead-letter path `~/.claude/state/board-deadletter.jsonl` creatable** —
   `DEAD_LETTER` + `test_dead_letter_path_exists_or_creatable`.
5. **Documented `gh issue view 102 --repo chidionyema/crew --comments
   --json number,state,comments` runs clean** —
   `test_read_command_documented_in_board_doc_runs_clean`.
6. **At least one comment matches the declared format** —
   `test_comment_format_matches_issue_body` and
   `test_a_board_row_matches_the_declared_row_format`.
7. **`parse_comment` handles both full and simple row formats** —
   `test_parse_comment_full_format` and
   `test_parse_comment_simple_format_defaults_kind_and_priority`.
8. **Backfill headers (prose) are not rows — `parse_comment` returns None** —
   `test_a_backfill_header_is_not_a_row`.
9. **Rows come back oldest-first** —
   `test_rows_come_back_oldest_first`.
10. **Cache is one JSON object per real newline; failed read is loud
    non-zero exit (LAW 28)** —
    `test_sync_writes_one_json_object_per_line` and
    `test_a_failed_read_is_a_loud_non_zero_exit`.

## Constants

- `BOARD_REPO = "chidionyema/crew"`
- `BOARD_ISSUE = 102`
- `DEAD_LETTER = ~/.claude/state/board-deadletter.jsonl`

## Read command

```
gh issue view 102 --repo chidionyema/crew --comments --json number,state,comments
```

## Option chosen

(A) Pin the contract in a single new incident test that imports the
existing modules and asserts the ten rows. The per-row diagnosis in the
older tests (`test_incident_crew102_*` and `test_incident_crew101_*`)
stays where it was; this PR only names the rows in one place so a future
reader sees the whole contract top-to-bottom.

## What this PR did NOT change

- `CREW-BOARD-VISIBILITY.md` — already on target.
- `scripts/estate-board-sync.py` — already correct.
- The existing incident tests (`test_incident_crew101_*`, `test_incident_crew102_*`)
  — unchanged. They carry the per-row diagnosis this PR only summarises.
- `bin/board-target` — does not exist on main; not added.
