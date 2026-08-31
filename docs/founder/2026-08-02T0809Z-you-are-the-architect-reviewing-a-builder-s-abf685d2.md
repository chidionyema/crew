---
captured: 2026-08-02T08:09:45+00:00
session: 9952474e-ad16-43e4-85db-3b3b36294cf9
cwd: /Users/chidionyema/Documents/code/prospector
chars: 4977
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are the Architect reviewing a Builder's diff against the task contract. The project's verify command already exits 0.

TASK:
Implement the Unified Cockpit for Hermes per the spec at `.plans/unified-cockpit-build.md`.

The test file at `tests/test_unified_cockpit.py` has 23 tests — currently 19 fail, 4 pass. Your job: make ALL 23 pass.

## Files to change

1. **`gateway/operator_shell/mission.py`** — Rewrite `render_mission_card()` as the unified Home screen:
   - Headline: "🏠 *Otto*" (not "🎛 *Cockpit*")
   - Keep: estate health, concerns, blocker (reuse existing helpers)
   - Add: in-flight work section (from code_remote + missions)
   - Add: SDLC summary line with `[💻 Full SDLC pipeline]` button → `estate:sdlc`
   - Add: daemon controls row (coordinator, gateway, watchdog, TIE)
   - Add: quick actions row (Restart, Status, Assign, Inbox)
   - Keep: nav spine at bottom
   - The function signature stays: `render_mission_card() -> Tuple[str, bool, List[ButtonRow]]`

2. **`gateway/operator_shell/sdlc.py`** — NEW file. Function `render_sdlc() -> Tuple[str, List[ButtonRow]]`:
   - 6 stages: Assign, Board, Fleet, Review, Ship, Learn
   - Reuse existing render helpers from code_remote, mission, fleet, builds, inbox, rsi_panel
   - Every section has a button to open the full panel
   - Graceful degradation — if a data source fails, show "—" not crash
   - Nav spine at bottom

3. **`gateway/operator_shell/natural_ops.py`** — Change the "sdlc" regex entry (line ~299):
   - Change from `"room", "code"` to `"sdlc", ""` so typing "sdlc" opens the SDLC panel
   - Add a separate `"pipeline"` → `"sdlc"` entry

4. **`gateway/operator_shell/estate.py`** — Add `if action == "sdlc"` handler:
   ```python
   if action == "sdlc":
       from gateway.operator_shell.sdlc import render_sdlc
       text, buttons = render_sdlc()
       return _finish(PanelView(text=text, buttons=buttons, toast="SDLC", ...))
   ```

5. **`gateway/operator_shell/panel_chrome.py`** — Fix nav spine labels:
   - `_NOW = ("🏠 Home", "estate:refresh")`
   - `_RUN = ("⚡ Actions", "estate:run")`
   - Add `_SDLC = ("💻 SDLC", "estate:sdlc")`
   - `_TUNE` stays the same
   - `_MAP = ("🗺 Browse", "estate:find")`
   - Update `nav()` to include `_SDLC` in the spine

## Key patterns

- `render_mission_card()` returns `Tuple[str, bool, List[ButtonRow]]`
- `render_sdlc()` returns `Tuple[str, List[ButtonRow]]` (like most panels)
- Nav spine: `nav()` returns `ButtonRow` — a list of (label, callback) tuples
- Panel view: `PanelView(text=text, buttons=buttons, toast=..., ok=True, ...)`
- Estate dispatch: `_finish(PanelView(...))` 
- Graceful: wrap data fetches in try/except, show "—" on failure

## Verification

Run: `python3 -m pytest tests/test_unified_cockpit.py -v`
Target: 23 passed, 0 failed

Judge whether the diff fully and correctly satisfies the task with no scope creep, no security/correctness regressions, and adequate tests. Respond with a FIRST LINE of exactly "VERDICT: APPROVE" or "VERDICT: REJECT", then a brief rationale.

--- git diff ---
diff --git a/storage/durable_ledger.md b/storage/durable_ledger.md
index 108d07d..b5f5883 100644
--- a/storage/durable_ledger.md
+++ b/storage/durable_ledger.md
@@ -831,4 +831,13 @@
 * LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
 * LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
 * LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not build wrappers on transparent markets.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc123 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to abc after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-2 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
+* LAW: Do not generate concepts related to test-3 after multiple failed wedge pivots.
 * LAW: Do not build wrappers on transparent markets.
\ No newline at end of file
diff --git a/store/control_center/config_history.jsonl b/store/control_center/config_history.jsonl
index f4229a6..dfcd7c6 100644
--- a/store/control_center/config_history.jsonl
+++ b/store/control_center/config_history.jsonl
@@ -550,3 +550,7 @@ backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidi
 hash: 78814b94251c
 moat_affecting: false
 ts: '2026-07-31T02:44:57.846125+00:00'
+backup: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/pytest-of-chidionyema/pytest-693/test_write_config_creates_back0/backups/config.yaml.bak.20260802T080752
+hash: 78814b94251c
+moat_affecting: false
+ts: '2026-08-02T08:07:52.596025+00:00'
