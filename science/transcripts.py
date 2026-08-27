"""Read Claude Code session transcripts incrementally, by byte offset (crew#319, crew#74 row 4).

`~/.claude/projects/**/*.jsonl` is the largest thing the estate writes and, until this
file, nothing read its content: only per-day spend was extracted. A transcript is an
append-only log that a running session writes to and that never changes again once the
session ends, so the cheap way to read 6.5 GB is to read each byte once:

* `manifest` remembers every file seen: inode, size, `bytes_consumed`, mtime, `sealed`.
* A file whose mtime is older than SEAL_SECONDS and that is fully consumed is sealed; a
  later run stats it and reads nothing. A sealed file whose inode or size changed is
  reopened from the offset it was last read at.
* An unsealed file is opened at `bytes_consumed` and read forward. Only complete lines
  (ending in a newline) are consumed, so a line the session is still writing is read
  whole on the next run, never as two halves.
* A file that shrank or changed inode was rewritten: its events are dropped and it is
  read again from zero.

What lands, per line, is the small part that answers "what did agents do": the event
type, the tool a call named, whether a result was an error and the first line of the
error, the session, the timestamp. The raw text stays in the JSONL, which is the system
of record; the whole store can be rebuilt from offset zero by deleting the database.

Second run after no new sessions reads zero bytes: that is the row on crew#74 and the
property `tests/test_incident_crew319_transcripts_ingest_by_byte_offset.py` holds.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from dataclasses import dataclass
from pathlib import Path


def _env_path(var: str, default: Path) -> Path:
    v = os.environ.get(var)
    return Path(v).expanduser() if v else default


HOME = _env_path("ESTATE_HOME", Path.home())
TRANSCRIPTS = _env_path("ESTATE_TRANSCRIPTS", HOME / ".claude/projects")
STORE = _env_path("SCIENCE_TRANSCRIPTS_DB", Path(__file__).parent / "transcripts.db")

#: A session that has not written for this long is over. Measured on the founder Mac
#: 2026-08-27: the gap between two writes of a live session is seconds; a session that
#: is idle for 30 minutes has been compacted, cleared or closed.
SEAL_SECONDS = 30 * 60
ERROR_HEAD = 200
#: events.line_no is line * BLOCKS_PER_LINE + block index, so one line may carry up to this
#: many content blocks before two events share a key; a message with more is not a shape
#: the CLI writes (measured max 2026-08-27: 20 blocks) and INSERT OR REPLACE keeps the last.
BLOCKS_PER_LINE = 1000

SCHEMA = """
CREATE TABLE IF NOT EXISTS manifest (
    path TEXT PRIMARY KEY,
    inode INTEGER NOT NULL,
    size INTEGER NOT NULL,
    bytes_consumed INTEGER NOT NULL,
    mtime REAL NOT NULL,
    sealed INTEGER NOT NULL DEFAULT 0,
    last_read_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    path TEXT NOT NULL,
    line_no INTEGER NOT NULL,
    session_id TEXT,
    at TEXT,
    kind TEXT NOT NULL,
    tool TEXT,
    tool_use_id TEXT,
    is_error INTEGER NOT NULL DEFAULT 0,
    error_head TEXT,
    chars INTEGER NOT NULL,
    PRIMARY KEY (path, line_no)
);
CREATE INDEX IF NOT EXISTS events_session ON events (session_id);
CREATE INDEX IF NOT EXISTS events_tool ON events (tool, is_error);
CREATE TABLE IF NOT EXISTS runs (
    at TEXT NOT NULL,
    files_seen INTEGER NOT NULL,
    files_read INTEGER NOT NULL,
    bytes_read INTEGER NOT NULL,
    events INTEGER NOT NULL,
    sealed INTEGER NOT NULL
);
"""


@dataclass(frozen=True)
class Event:
    kind: str
    tool: str | None = None
    tool_use_id: str | None = None
    is_error: bool = False
    error_head: str | None = None


def _head(content: object) -> str:
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        text = " ".join(
            b.get("text", "") for b in content if isinstance(b, dict) and isinstance(b.get("text"), str)
        )
    else:
        text = json.dumps(content)[:ERROR_HEAD]
    return text.strip().splitlines()[0][:ERROR_HEAD] if text.strip() else ""


def events_of(obj: dict) -> list[Event]:
    """The events one transcript line carries. A line is one event unless it is a
    message whose content holds tool_use / tool_result blocks, which are each one."""
    kind = obj.get("type")
    if not isinstance(kind, str):
        return [Event("unknown")]
    message = obj.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if kind not in ("user", "assistant") or not isinstance(content, list):
        return [Event(kind)]
    out: list[Event] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        btype = block.get("type")
        if btype == "tool_use":
            out.append(Event("tool_use", tool=block.get("name"), tool_use_id=block.get("id")))
        elif btype == "tool_result":
            err = bool(block.get("is_error"))
            out.append(Event("tool_result", tool_use_id=block.get("tool_use_id"), is_error=err,
                             error_head=_head(block.get("content")) if err else None))
        elif btype == "text":
            out.append(Event(f"{kind}_text"))
    return out or [Event(kind)]


def transcript_files(root: Path) -> list[Path]:
    """Every .jsonl under root, in a stable order. os.walk, not rglob: 16k directories
    on the founder Mac and rglob stats every entry twice."""
    found: list[Path] = []
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith(".jsonl"):
                found.append(Path(dirpath) / f)
    return sorted(found)


def read_forward(path: Path, offset: int) -> tuple[list[tuple[int, str]], int]:
    """Complete lines after `offset`, as (byte_offset_of_line_end, text), and the new
    offset. A trailing partial line is left for the next run."""
    lines: list[tuple[int, str]] = []
    with open(path, "rb") as fh:
        fh.seek(offset)
        pos = offset
        for raw in fh:
            if not raw.endswith(b"\n"):
                break
            pos += len(raw)
            lines.append((pos, raw.decode("utf-8", "replace")))
    return lines, pos


def ingest(conn: sqlite3.Connection, root: Path = TRANSCRIPTS, now: float | None = None) -> dict[str, int]:
    now = time.time() if now is None else now
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    conn.executescript(SCHEMA)
    known = {r[0]: r for r in conn.execute(
        "SELECT path, inode, size, bytes_consumed, mtime, sealed FROM manifest")}
    stats = {"files_seen": 0, "files_read": 0, "bytes_read": 0, "events": 0, "sealed": 0}
    for path in transcript_files(root):
        stats["files_seen"] += 1
        st = path.stat()
        key = str(path)
        row = known.get(key)
        offset = 0
        if row is not None:
            _p, inode, _size, consumed, _mtime, sealed = row
            rewritten = inode != st.st_ino or st.st_size < consumed
            if rewritten:
                conn.execute("DELETE FROM events WHERE path = ?", (key,))
            else:
                offset = consumed
                if sealed and st.st_size == consumed:
                    stats["sealed"] += 1
                    continue
        line_no = (conn.execute("SELECT COALESCE(MAX(line_no), 0) FROM events WHERE path = ?",
                                (key,)).fetchone()[0] // BLOCKS_PER_LINE) if offset else 0
        lines, new_offset = read_forward(path, offset)
        if lines:
            stats["files_read"] += 1
            stats["bytes_read"] += new_offset - offset
        #: An incremental run starts mid-session: the sessionId sits on an earlier line that
        #: was consumed last time, so seed it from the last event already stored (crew#432 review).
        session_id: str | None = None
        if offset:
            prev = conn.execute("SELECT session_id FROM events WHERE path = ? AND session_id IS NOT NULL "
                                "ORDER BY line_no DESC LIMIT 1", (key,)).fetchone()
            session_id = prev[0] if prev else None
        for _end, text in lines:
            line_no += 1
            try:
                obj = json.loads(text)
            except ValueError:
                obj = None
            if not isinstance(obj, dict):
                evs, at = [Event("bad_json")], None
            else:
                evs = events_of(obj)
                at = obj.get("timestamp") if isinstance(obj.get("timestamp"), str) else None
                sid = obj.get("sessionId") or obj.get("session_id")
                session_id = sid if isinstance(sid, str) else session_id
            for i, ev in enumerate(evs):
                conn.execute(
                    "INSERT OR REPLACE INTO events VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (key, line_no * BLOCKS_PER_LINE + i, session_id, at, ev.kind, ev.tool, ev.tool_use_id,
                     int(ev.is_error), ev.error_head, len(text)),
                )
                stats["events"] += 1
        fully = new_offset == st.st_size
        sealed_now = int(fully and now - st.st_mtime > SEAL_SECONDS)
        stats["sealed"] += sealed_now
        conn.execute(
            "INSERT OR REPLACE INTO manifest VALUES (?,?,?,?,?,?,?)",
            (key, st.st_ino, st.st_size, new_offset, st.st_mtime, sealed_now, now_iso),
        )
    conn.execute("INSERT INTO runs VALUES (?,?,?,?,?,?)",
                 (now_iso, stats["files_seen"], stats["files_read"], stats["bytes_read"],
                  stats["events"], stats["sealed"]))
    conn.commit()
    return stats


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Read session transcripts incrementally by byte offset")
    ap.add_argument("--root", type=Path, default=TRANSCRIPTS)
    ap.add_argument("--db", type=Path, default=STORE)
    args = ap.parse_args(argv)
    if not args.root.is_dir():
        print(f"transcripts: root {args.root} is not a directory")
        return 1
    conn = sqlite3.connect(args.db)
    try:
        started = time.time()
        s = ingest(conn, args.root)
        total = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        errors = conn.execute("SELECT COUNT(*) FROM events WHERE is_error = 1").fetchone()[0]
    finally:
        conn.close()
    print(f"transcripts: files_seen={s['files_seen']} files_read={s['files_read']} "
          f"bytes_read={s['bytes_read']} events={s['events']} sealed={s['sealed']} "
          f"store_events={total} store_errors={errors} in {time.time() - started:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
