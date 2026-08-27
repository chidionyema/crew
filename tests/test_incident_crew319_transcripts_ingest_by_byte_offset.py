"""crew#319 / crew#74 row 4: 6.5 GB of session transcripts were never read because the
only reader would have reread all of it every run. Rule: every byte of a transcript is
read once. A second run over the same files reads zero bytes; an appended line costs its
own length; a half-written line waits; a rewritten file is read again from zero. Rung 4,
incident test, proved both ways."""
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

from science import transcripts as T

HERE = Path(__file__).parent
NOW = 1_800_000_000.0


def line(**kw) -> str:
    return json.dumps(kw) + "\n"


def tool_call(tid: str, name: str) -> str:
    return line(type="assistant", sessionId="s1", timestamp="2026-08-27T04:00:00Z",
                message={"content": [{"type": "tool_use", "id": tid, "name": name, "input": {}}]})


def tool_result(tid: str, err: bool, text: str = "ok") -> str:
    return line(type="user", sessionId="s1", timestamp="2026-08-27T04:00:01Z",
                message={"content": [{"type": "tool_result", "tool_use_id": tid,
                                      "is_error": err, "content": text}]})


def make_root(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "projects" / "-Users-x-dev"
    root.mkdir(parents=True)
    f = root / "a.jsonl"
    f.write_text(tool_call("t1", "Bash") + tool_result("t1", True, "rc=1: no such file\nmore"))
    os.utime(f, (NOW - 10, NOW - 10))
    return tmp_path / "projects", f


def test_every_byte_is_read_once(tmp_path):
    root, f = make_root(tmp_path)
    conn = sqlite3.connect(":memory:")
    first = T.ingest(conn, root, now=NOW)
    assert first["bytes_read"] == f.stat().st_size and first["files_read"] == 1
    rows = conn.execute("SELECT kind, tool, is_error, error_head FROM events ORDER BY line_no").fetchall()
    assert rows == [("tool_use", "Bash", 0, None), ("tool_result", None, 1, "rc=1: no such file")]

    # the row: a second run with nothing new reads zero bytes
    second = T.ingest(conn, root, now=NOW + 60)
    assert (second["files_read"], second["bytes_read"], second["events"]) == (0, 0, 0)

    # an appended complete line costs exactly its own length; a half line waits
    extra = tool_call("t2", "Read")
    with open(f, "a") as fh:
        fh.write(extra + '{"type": "assistant", "half')
    third = T.ingest(conn, root, now=NOW + 120)
    assert third["bytes_read"] == len(extra.encode()) and third["events"] == 1
    consumed = conn.execute("SELECT bytes_consumed FROM manifest").fetchone()[0]
    assert consumed == f.stat().st_size - len('{"type": "assistant", "half')

    # the other way: a shrunk file was rewritten and is read again from zero
    f.write_text(tool_call("t9", "Edit"))
    fourth = T.ingest(conn, root, now=NOW + 180)
    assert fourth["bytes_read"] == f.stat().st_size
    assert conn.execute("SELECT tool FROM events").fetchall() == [("Edit",)]


def test_a_sealed_file_is_never_opened_again(tmp_path, monkeypatch):
    root, f = make_root(tmp_path)
    os.utime(f, (NOW - T.SEAL_SECONDS - 1, NOW - T.SEAL_SECONDS - 1))
    conn = sqlite3.connect(":memory:")
    assert T.ingest(conn, root, now=NOW)["sealed"] == 1
    opened: list[Path] = []

    def spy(path, offset):
        opened.append(path)
        return [], offset
    monkeypatch.setattr(T, "read_forward", spy)
    again = T.ingest(conn, root, now=NOW + 1)
    assert again["sealed"] == 1 and again["bytes_read"] == 0 and opened == []


def test_cli_prints_the_run_and_counts_errors(tmp_path):
    root, _f = make_root(tmp_path)
    db = tmp_path / "t.db"
    env = dict(os.environ, PYTHONPATH=str(HERE.parent))
    r = subprocess.run([sys.executable, str(HERE.parent / "science/transcripts.py"),
                        "--root", str(root), "--db", str(db)],
                       capture_output=True, text=True, env=env, check=False)
    assert r.returncode == 0 and "files_read=1" in r.stdout and "store_errors=1" in r.stdout, r.stdout + r.stderr
    r2 = subprocess.run([sys.executable, str(HERE.parent / "science/transcripts.py"),
                         "--root", str(tmp_path / "nowhere"), "--db", str(db)],
                        capture_output=True, text=True, env=env, check=False)
    assert r2.returncode == 1
