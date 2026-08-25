#!/usr/bin/env python3
"""Stop hook (LAW 47 / R30). A reply that says FOUNDER ACTION: must have reached the founder's
Telegram in the last 60 minutes through founder-blocker.py. Founder, 2026-08-25: "again i missed
it ... did you send to telegram also? i said it needs to be loud". The class: a founder blocker
announced only in a channel he is not watching. This guard cannot tell whether he read it; it
can tell whether a pinned message exists, and that is the receipt it demands.

Exit 2 blocks the reply; exit 0 permits. BLIND (ledger unreadable) permits and says so.
"""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

WINDOW_S = 3600.0
MARK = "FOUNDER ACTION:"


def last_assistant_text(transcript: Path) -> str:
    text = ""
    try:
        with transcript.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get("type") != "assistant":
                    continue
                parts = [c.get("text", "") for c in row.get("message", {}).get("content", [])
                         if isinstance(c, dict) and c.get("type") == "text"]
                if parts:
                    text = "\n".join(parts)
    except OSError:
        return ""
    return text


def verdict(reply: str, ledger_rows: list[dict] | None, now: float) -> tuple[int, str]:
    if MARK not in reply:
        return 0, ""
    if ledger_rows is None:
        return 0, "[blocker-guard] BLIND: telegram ledger unreadable; FOUNDER ACTION: not checked"
    for r in ledger_rows:
        if r.get("source") == "founder-blocker" and r.get("outcome") == "sent" \
                and int(r.get("msg_id", 0) or 0) > 0 and now - float(r.get("ts", 0)) <= WINDOW_S:
            return 0, ""
    return 2, ("BLOCKED by blocker-guard: the reply says FOUNDER ACTION: but no founder-blocker "
               "Telegram message landed in the last 60 minutes (LAW 47 / R30: he manages eight "
               "agents; the terminal is not where he looks).\n"
               "  run   python3 ~/.claude/scripts/founder-blocker.py \"<what he must do>\" <url-or-word>\n"
               "  then  reissue the reply with the FOUNDER ACTION: line it prints")


def main() -> int:
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    reply = last_assistant_text(Path(payload.get("transcript_path") or "/dev/null"))
    try:
        from estate import telegram_ledger
        rows = telegram_ledger.read(since_s=time.time() - WINDOW_S)
    except Exception:  # noqa: BLE001
        rows = None
    code, msg = verdict(reply, rows, time.time())
    if msg:
        print(msg, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
